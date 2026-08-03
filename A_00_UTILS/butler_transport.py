#!/usr/bin/env python3
"""
Butler Omega Smart text transport utility.

Official transport payload: UTF-8 bytes -> GZip -> Base64 -> small PowerShell
blocks with per-block SHA256 and final SHA256 verification.
"""

from __future__ import annotations

import argparse
import base64
import gzip
import hashlib
import json
import math
import shutil
from datetime import datetime
from pathlib import Path


DEFAULT_CHARS_PER_BLOCK = 8000
FORMAT_VERSION = "BOS-TEXT-TRANSPORT-1.0"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def ps_single_quote(value: str) -> str:
    return "'" + value.replace("'", "''") + "'"


def safe_name(name: str) -> str:
    cleaned = []
    for ch in name:
        if ch.isalnum() or ch in (".", "-", "_"):
            cleaned.append(ch)
        else:
            cleaned.append("_")
    result = "".join(cleaned).strip("._")
    return result or "payload"


def make_manifest(source: Path, output_name: str, raw: bytes, compressed: bytes, b64: str, chunk_size: int) -> dict:
    chunks = [b64[i : i + chunk_size] for i in range(0, len(b64), chunk_size)]
    return {
        "format": FORMAT_VERSION,
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "source_name": source.name,
        "output_name": output_name,
        "source_size_bytes": len(raw),
        "gzip_size_bytes": len(compressed),
        "base64_size_chars": len(b64),
        "chunk_size_chars": chunk_size,
        "chunk_count": len(chunks),
        "sha256_original": sha256_bytes(raw),
        "sha256_gzip": sha256_bytes(compressed),
        "chunks": [
            {
                "index": index + 1,
                "name": f"block_{index + 1:03d}.ps1",
                "base64_chars": len(chunk),
                "sha256_base64_chunk": sha256_bytes(chunk.encode("ascii")),
            }
            for index, chunk in enumerate(chunks)
        ],
    }


def block_script(manifest: dict, index: int, chunk: str) -> str:
    chunk_info = manifest["chunks"][index - 1]
    total = manifest["chunk_count"]
    output_name = manifest["output_name"]
    original_hash = manifest["sha256_original"]
    chunk_hash = chunk_info["sha256_base64_chunk"]
    format_version = manifest["format"]
    return f"""# Butler Omega Smart Text Transport
# Format: {format_version}
# Block: {index}/{total}
# Target: {output_name}
$ErrorActionPreference = "Stop"
$TransportRoot = Join-Path (Get-Location).Path "_butler_transport_inbox"
$ChunkRoot = Join-Path $TransportRoot {ps_single_quote(safe_name(output_name))}
New-Item -ItemType Directory -Force -Path $ChunkRoot | Out-Null
$Chunk = {ps_single_quote(chunk)}
$ExpectedChunkSha256 = {ps_single_quote(chunk_hash)}
$BytesForHash = [System.Text.Encoding]::ASCII.GetBytes($Chunk)
$ActualChunkSha256 = [BitConverter]::ToString([System.Security.Cryptography.SHA256]::Create().ComputeHash($BytesForHash)).Replace("-", "").ToLowerInvariant()
if ($ActualChunkSha256 -ne $ExpectedChunkSha256) {{
    throw "Chunk SHA256 mismatch in block {index:03d}: $ActualChunkSha256"
}}
$ChunkPath = Join-Path $ChunkRoot ("chunk_{index:03d}.b64")
[System.IO.File]::WriteAllText($ChunkPath, $Chunk, [System.Text.Encoding]::ASCII)
$ManifestPath = Join-Path $ChunkRoot "manifest.json"
if (-not (Test-Path -LiteralPath $ManifestPath)) {{
@'
{json.dumps(manifest, ensure_ascii=False, indent=2)}
'@ | Set-Content -LiteralPath $ManifestPath -Encoding UTF8
}}
Write-Host "[OK] Butler transport block {index:03d}/{total} accepted"
"""


def assembler_script(manifest: dict) -> str:
    output_name = manifest["output_name"]
    target_hash = manifest["sha256_original"]
    chunk_count = manifest["chunk_count"]
    safe_output = safe_name(output_name)
    return f"""# Butler Omega Smart Text Transport Assembler
# Format: {manifest["format"]}
$ErrorActionPreference = "Stop"
$TransportRoot = Join-Path (Get-Location).Path "_butler_transport_inbox"
$ChunkRoot = Join-Path $TransportRoot {ps_single_quote(safe_output)}
$ManifestPath = Join-Path $ChunkRoot "manifest.json"
if (-not (Test-Path -LiteralPath $ManifestPath)) {{ throw "Missing manifest.json" }}
$Manifest = Get-Content -LiteralPath $ManifestPath -Raw -Encoding UTF8 | ConvertFrom-Json
if ($Manifest.format -ne {ps_single_quote(manifest["format"])}) {{ throw "Unsupported transport format: $($Manifest.format)" }}
if ([int]$Manifest.chunk_count -ne {chunk_count}) {{ throw "Unexpected chunk count in manifest" }}
$Builder = New-Object System.Text.StringBuilder
for ($i = 1; $i -le [int]$Manifest.chunk_count; $i++) {{
    $ChunkPath = Join-Path $ChunkRoot ("chunk_{{0:D3}}.b64" -f $i)
    if (-not (Test-Path -LiteralPath $ChunkPath)) {{ throw "Missing chunk: $ChunkPath" }}
    $Chunk = [System.IO.File]::ReadAllText($ChunkPath, [System.Text.Encoding]::ASCII)
    $Expected = $Manifest.chunks[$i - 1].sha256_base64_chunk
    $BytesForHash = [System.Text.Encoding]::ASCII.GetBytes($Chunk)
    $Actual = [BitConverter]::ToString([System.Security.Cryptography.SHA256]::Create().ComputeHash($BytesForHash)).Replace("-", "").ToLowerInvariant()
    if ($Actual -ne $Expected) {{ throw "Chunk SHA256 mismatch: chunk_$('{{0:D3}}' -f $i).b64" }}
    [void]$Builder.Append($Chunk)
}}
$GzipBytes = [System.Convert]::FromBase64String($Builder.ToString())
$InputStream = New-Object System.IO.MemoryStream(,$GzipBytes)
$GzipStream = New-Object System.IO.Compression.GzipStream($InputStream, [System.IO.Compression.CompressionMode]::Decompress)
$OutputStream = New-Object System.IO.MemoryStream
$GzipStream.CopyTo($OutputStream)
$GzipStream.Dispose()
$RawBytes = $OutputStream.ToArray()
$ActualFileSha256 = [BitConverter]::ToString([System.Security.Cryptography.SHA256]::Create().ComputeHash($RawBytes)).Replace("-", "").ToLowerInvariant()
$ExpectedFileSha256 = {ps_single_quote(target_hash)}
if ($ActualFileSha256 -ne $ExpectedFileSha256) {{ throw "Final SHA256 mismatch: $ActualFileSha256" }}
$OutPath = Join-Path (Get-Location).Path {ps_single_quote(output_name)}
[System.IO.File]::WriteAllBytes($OutPath, $RawBytes)
Write-Host "[OK] Butler transport assembled: $OutPath"
Write-Host "[OK] SHA256: $ActualFileSha256"
"""


def pack(source: Path, out_dir: Path, output_name: str | None, chunk_size: int) -> dict:
    source = source.resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    raw = source.read_bytes()
    compressed = gzip.compress(raw, compresslevel=9)
    b64 = base64.b64encode(compressed).decode("ascii")
    final_name = output_name or source.name
    manifest = make_manifest(source, final_name, raw, compressed, b64, chunk_size)
    chunks = [b64[i : i + chunk_size] for i in range(0, len(b64), chunk_size)]

    manifest_path = out_dir / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    for index, chunk in enumerate(chunks, start=1):
        (out_dir / f"block_{index:03d}.ps1").write_text(block_script(manifest, index, chunk), encoding="utf-8")
    (out_dir / "assemble.ps1").write_text(assembler_script(manifest), encoding="utf-8")
    (out_dir / "README.md").write_text(readme_text(manifest), encoding="utf-8")
    return manifest


def readme_text(manifest: dict) -> str:
    block_lines = "\n".join(f"powershell -ExecutionPolicy Bypass -File .\\{chunk['name']}" for chunk in manifest["chunks"])
    return f"""# Butler Text Transport Package

Target: `{manifest['output_name']}`
Format: `{manifest['format']}`
Original SHA256: `{manifest['sha256_original']}`
Blocks: `{manifest['chunk_count']}`

Run every block in any clean target folder, then run:

```powershell
{block_lines}
powershell -ExecutionPolicy Bypass -File .\\assemble.ps1
```

If one block is damaged, resend only that `block_NNN.ps1`.
"""


def unpack(package_dir: Path, destination_dir: Path) -> Path:
    package_dir = package_dir.resolve()
    destination_dir.mkdir(parents=True, exist_ok=True)
    manifest = json.loads((package_dir / "manifest.json").read_text(encoding="utf-8"))
    b64_parts = []
    for chunk in manifest["chunks"]:
        block_name = chunk["name"]
        block_text = (package_dir / block_name).read_text(encoding="utf-8")
        marker = "$Chunk = '"
        start = block_text.index(marker) + len(marker)
        end = block_text.index("'\n$ExpectedChunkSha256", start)
        chunk_b64 = block_text[start:end].replace("''", "'")
        if sha256_bytes(chunk_b64.encode("ascii")) != chunk["sha256_base64_chunk"]:
            raise RuntimeError(f"chunk hash mismatch: {block_name}")
        b64_parts.append(chunk_b64)
    raw = gzip.decompress(base64.b64decode("".join(b64_parts)))
    if sha256_bytes(raw) != manifest["sha256_original"]:
        raise RuntimeError("final hash mismatch")
    out_path = destination_dir / manifest["output_name"]
    out_path.write_bytes(raw)
    return out_path


def verify(source: Path, restored: Path) -> dict:
    source_bytes = source.read_bytes()
    restored_bytes = restored.read_bytes()
    return {
        "source": str(source),
        "restored": str(restored),
        "source_size": len(source_bytes),
        "restored_size": len(restored_bytes),
        "source_sha256": sha256_bytes(source_bytes),
        "restored_sha256": sha256_bytes(restored_bytes),
        "match": source_bytes == restored_bytes,
    }


def clean(path: Path) -> None:
    if path.exists():
        shutil.rmtree(path)


def main() -> None:
    parser = argparse.ArgumentParser(description="Butler Omega Smart safe text transport.")
    sub = parser.add_subparsers(dest="command", required=True)

    pack_parser = sub.add_parser("pack", help="Create PowerShell transport blocks.")
    pack_parser.add_argument("source")
    pack_parser.add_argument("--out-dir", required=True)
    pack_parser.add_argument("--output-name")
    pack_parser.add_argument("--chunk-size", type=int, default=DEFAULT_CHARS_PER_BLOCK)

    unpack_parser = sub.add_parser("unpack", help="Unpack a transport package without PowerShell.")
    unpack_parser.add_argument("package_dir")
    unpack_parser.add_argument("--dest-dir", required=True)

    verify_parser = sub.add_parser("verify", help="Compare two files byte-for-byte.")
    verify_parser.add_argument("source")
    verify_parser.add_argument("restored")

    args = parser.parse_args()

    if args.command == "pack":
        manifest = pack(Path(args.source), Path(args.out_dir), args.output_name, args.chunk_size)
        print("BUTLER_TRANSPORT_PACK_OK")
        print(f"blocks={manifest['chunk_count']}")
        print(f"sha256={manifest['sha256_original']}")
    elif args.command == "unpack":
        out_path = unpack(Path(args.package_dir), Path(args.dest_dir))
        print(f"BUTLER_TRANSPORT_UNPACK_OK {out_path}")
    elif args.command == "verify":
        result = verify(Path(args.source), Path(args.restored))
        print(json.dumps(result, ensure_ascii=False, indent=2))
        if not result["match"]:
            raise SystemExit(1)


if __name__ == "__main__":
    main()
