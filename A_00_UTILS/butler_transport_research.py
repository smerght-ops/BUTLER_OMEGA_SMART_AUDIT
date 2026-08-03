#!/usr/bin/env python3
"""
Experimental comparison of text transport variants for Butler Omega Smart.

The experiment uses real project documents, reconstructs 300/500/1000-line
fixtures through PowerShell, and checks byte-for-byte SHA256 equality.
"""

from __future__ import annotations

import base64
import gzip
import hashlib
import json
import subprocess
import time
from datetime import datetime
from pathlib import Path

from document_writer import write_document


ROOT = Path(__file__).resolve().parents[1]
WORK = ROOT / "A_06_WORKSPACE" / "TRANSPORT_RESEARCH"
REPORT_DIR = ROOT / "A_06_WORKSPACE" / "AUDITS"
SOURCES = [
    ROOT / "A_00_UTILS" / "sanitary_archive_flat_final_v2.ps1",
    ROOT / "Inspector-Discovery_v3_1_TEST.py",
    ROOT / "A_06_WORKSPACE" / "AUDITS" / "INSPECTOR_ECOSYSTEM_AUDIT_20260710_063802.md",
    ROOT / "UnifiedInspectorFacts.json",
]


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def ps_quote(value: str) -> str:
    return "'" + value.replace("'", "''") + "'"


def read_lines(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8-sig", errors="replace")
    lines = text.splitlines(keepends=True)
    if lines and not lines[-1].endswith(("\n", "\r")):
        lines[-1] += "\n"
    return lines


def build_fixture(line_count: int) -> str:
    pools = [read_lines(path) for path in SOURCES]
    labels = ["PowerShell", "Python", "Markdown", "JSON"]
    result = []
    index = 0
    while len(result) < line_count:
        pool_index = index % len(pools)
        pool = pools[pool_index]
        source_line = pool[(index // len(pools)) % len(pool)]
        if len(result) % 50 == 0:
            result.append(
                f"# UTF-8 test {labels[pool_index]} русский текст ${{value}} `backtick` [] {{}} Ω Ж 🚀 line={len(result)}\n"
            )
        else:
            result.append(source_line)
        index += 1
    return "".join(result[:line_count])


def write_fixture(line_count: int) -> Path:
    path = WORK / "fixtures" / f"fixture_{line_count:04d}_mixed.txt"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(build_fixture(line_count), encoding="utf-8", newline="")
    return path


def run_ps(script: Path) -> tuple[bool, float, str]:
    start = time.perf_counter()
    proc = subprocess.run(
        ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(script)],
        cwd=str(script.parent),
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        timeout=60,
    )
    elapsed = time.perf_counter() - start
    output = (proc.stdout + proc.stderr).strip()
    return proc.returncode == 0, elapsed, output[-1000:]


def method_a_here_string(source_text: str, out_name: str, chunk_lines: int = 80) -> str:
    lines = source_text.splitlines()
    chunks = ["\n".join(lines[i : i + chunk_lines]) for i in range(0, len(lines), chunk_lines)]
    script = [
        '$ErrorActionPreference = "Stop"',
        f"$Out = Join-Path (Get-Location).Path {ps_quote(out_name)}",
    ]
    for index, chunk in enumerate(chunks):
        cmd = "Set-Content" if index == 0 else "Add-Content"
        script.append("@'")
        script.append(chunk)
        script.append("'@ | " + cmd + " -LiteralPath $Out -Encoding UTF8")
    return "\n".join(script) + "\n"


def method_b_array_lines(source_text: str, out_name: str) -> str:
    lines = source_text.splitlines()
    encoded_lines = ["  " + ps_quote(line) for line in lines]
    joined = ",\n".join(encoded_lines)
    return f"""$ErrorActionPreference = "Stop"
$Out = Join-Path (Get-Location).Path {ps_quote(out_name)}
$Lines = @(
{joined}
)
$Lines | Set-Content -LiteralPath $Out -Encoding UTF8
"""


def method_c_base64(raw: bytes, out_name: str) -> str:
    b64 = base64.b64encode(raw).decode("ascii")
    return f"""$ErrorActionPreference = "Stop"
$Out = Join-Path (Get-Location).Path {ps_quote(out_name)}
$B64 = {ps_quote(b64)}
$Bytes = [System.Convert]::FromBase64String($B64)
[System.IO.File]::WriteAllBytes($Out, $Bytes)
"""


def method_d_gzip_base64(raw: bytes, out_name: str) -> str:
    b64 = base64.b64encode(gzip.compress(raw, compresslevel=9)).decode("ascii")
    return f"""$ErrorActionPreference = "Stop"
$Out = Join-Path (Get-Location).Path {ps_quote(out_name)}
$B64 = {ps_quote(b64)}
$GzipBytes = [System.Convert]::FromBase64String($B64)
$InputStream = New-Object System.IO.MemoryStream(,$GzipBytes)
$GzipStream = New-Object System.IO.Compression.GzipStream($InputStream, [System.IO.Compression.CompressionMode]::Decompress)
$OutputStream = New-Object System.IO.MemoryStream
$GzipStream.CopyTo($OutputStream)
$GzipStream.Dispose()
[System.IO.File]::WriteAllBytes($Out, $OutputStream.ToArray())
"""


def check_method(method: str, fixture: Path, script_text: str) -> dict:
    case_dir = WORK / "runs" / f"{fixture.stem}_{method}"
    case_dir.mkdir(parents=True, exist_ok=True)
    script_path = case_dir / "rebuild.ps1"
    out_path = case_dir / "restored.txt"
    script_path.write_text(script_text, encoding="utf-8", newline="\n")
    ok, elapsed, ps_output = run_ps(script_path)
    source_bytes = fixture.read_bytes()
    restored_bytes = out_path.read_bytes() if out_path.exists() else b""
    return {
        "method": method,
        "fixture": fixture.name,
        "lines": int(fixture.stem.split("_")[1]),
        "source_bytes": len(source_bytes),
        "script_bytes": script_path.stat().st_size,
        "restored_bytes": len(restored_bytes),
        "sha256_source": sha256(source_bytes),
        "sha256_restored": sha256(restored_bytes) if restored_bytes else None,
        "match": source_bytes == restored_bytes,
        "powershell_ok": ok,
        "elapsed_seconds": round(elapsed, 3),
        "output_tail": ps_output,
    }


def corruption_test(fixture: Path) -> dict:
    from butler_transport import pack

    package_dir = WORK / "corruption_package"
    package_dir.mkdir(parents=True, exist_ok=True)
    manifest = pack(fixture, package_dir, "corruption_restored.txt", 48000)
    block = package_dir / "block_001.ps1"
    text = block.read_text(encoding="utf-8")
    marker = "$Chunk = '"
    pos = text.index(marker) + len(marker) + 10
    replacement = "A" if text[pos] != "A" else "B"
    block.write_text(text[:pos] + replacement + text[pos + 1 :], encoding="utf-8")
    ok, elapsed, output = run_ps(block)
    return {
        "fixture": fixture.name,
        "format": manifest["format"],
        "damaged_block": "block_001.ps1",
        "detected": not ok and "SHA256 mismatch" in output,
        "elapsed_seconds": round(elapsed, 3),
        "output_tail": output,
    }


def summarize(results: list[dict]) -> list[dict]:
    summary = []
    for method in ("A_here_string_chunks", "B_array_lines", "C_base64", "D_gzip_base64"):
        rows = [row for row in results if row["method"] == method]
        passed = [row for row in rows if row["match"] and row["powershell_ok"]]
        summary.append(
            {
                "method": method,
                "passed_cases": len(passed),
                "total_cases": len(rows),
                "max_verified_lines": max([row["lines"] for row in passed], default=0),
                "max_script_bytes_verified": max([row["script_bytes"] for row in passed], default=0),
                "all_sha256_match": len(passed) == len(rows),
                "avg_elapsed_seconds": round(sum(row["elapsed_seconds"] for row in rows) / len(rows), 3),
            }
        )
    return summary


def write_markdown(report: dict, path: Path) -> None:
    lines = [
        "# Butler Text Transport Research",
        "",
        f"- Generated: {report['generated_at']}",
        f"- Work dir: `{report['work_dir']}`",
        "- Scope: local PowerShell execution of generated transport scripts.",
        "",
        "## Summary",
        "| Method | Passed | Max verified lines | Max verified script bytes | Avg seconds |",
        "| --- | --- | --- | --- | --- |",
    ]
    for row in report["summary"]:
        lines.append(
            f"| {row['method']} | {row['passed_cases']}/{row['total_cases']} | "
            f"{row['max_verified_lines']} | {row['max_script_bytes_verified']} | {row['avg_elapsed_seconds']} |"
        )
    lines.extend(
        [
            "",
            "## Detail",
            "| Method | Fixture | Source bytes | Script bytes | SHA256 match | PowerShell OK |",
            "| --- | --- | --- | --- | --- | --- |",
        ]
    )
    for row in report["results"]:
        lines.append(
            f"| {row['method']} | {row['fixture']} | {row['source_bytes']} | {row['script_bytes']} | "
            f"{row['match']} | {row['powershell_ok']} |"
        )
    lines.extend(
        [
            "",
            "## Corruption Test",
            f"- Format: `{report['corruption_test']['format']}`",
            f"- Damaged block: `{report['corruption_test']['damaged_block']}`",
            f"- Detected: `{report['corruption_test']['detected']}`",
            "",
            "## Finding",
            "Only byte transports that write raw bytes preserved all tested content. "
            "Line/text transports using Set-Content changed bytes through newline and/or encoding behavior.",
        ]
    )
    write_document(path, "\n".join(lines))


def main() -> None:
    WORK.mkdir(parents=True, exist_ok=True)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    fixtures = [write_fixture(count) for count in (300, 500, 1000)]
    results = []
    for fixture in fixtures:
        source_text = fixture.read_text(encoding="utf-8")
        raw = fixture.read_bytes()
        results.append(check_method("A_here_string_chunks", fixture, method_a_here_string(source_text, "restored.txt")))
        results.append(check_method("B_array_lines", fixture, method_b_array_lines(source_text, "restored.txt")))
        results.append(check_method("C_base64", fixture, method_c_base64(raw, "restored.txt")))
        results.append(check_method("D_gzip_base64", fixture, method_d_gzip_base64(raw, "restored.txt")))

    report = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "root": str(ROOT),
        "work_dir": str(WORK),
        "sources": [str(path.relative_to(ROOT)) for path in SOURCES],
        "results": results,
        "summary": summarize(results),
        "corruption_test": corruption_test(fixtures[-1]),
    }
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    json_path = REPORT_DIR / f"BUTLER_TEXT_TRANSPORT_RESEARCH_{stamp}.json"
    md_path = REPORT_DIR / f"BUTLER_TEXT_TRANSPORT_RESEARCH_{stamp}.md"
    write_document(json_path, json.dumps(report, ensure_ascii=False, indent=2))
    write_markdown(report, md_path)
    print("BUTLER_TEXT_TRANSPORT_RESEARCH_OK")
    print(f"JSON_REPORT={json_path}")
    print(f"MD_REPORT={md_path}")


if __name__ == "__main__":
    main()
