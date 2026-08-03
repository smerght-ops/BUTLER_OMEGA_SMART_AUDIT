#!/usr/bin/env python3
"""
Unified document writer for Butler Omega Smart infrastructure.

Small documents are written normally. Large documents are still written to the
requested path, then a Butler text transport package is generated beside the
workspace reports so the same document can be moved safely through PowerShell.
"""

from __future__ import annotations

import hashlib
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any

from butler_transport import DEFAULT_CHARS_PER_BLOCK, pack


DOCUMENT_TRANSPORT_THRESHOLD_BYTES = 65536
DOCUMENT_TRANSPORT_ROOT = Path("A_06_WORKSPACE") / "TRANSPORT_OUT" / "AUTO_DOCUMENTS"
DOCUMENT_TEXT_ENCODING = "utf-8"


def _project_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _to_bytes(content: str | bytes | bytearray | Any) -> bytes:
    if isinstance(content, bytes):
        return content
    if isinstance(content, bytearray):
        return bytes(content)
    if isinstance(content, str):
        return content.encode(DOCUMENT_TEXT_ENCODING)
    return str(content).encode(DOCUMENT_TEXT_ENCODING)


def _safe_package_name(path: Path, data: bytes) -> str:
    stem = re.sub(r"[^A-Za-z0-9._-]+", "_", path.name).strip("._") or "document"
    digest = hashlib.sha256(data).hexdigest()[:12]
    return f"{stem}_{digest}"


def _transport_package_dir(path: Path, data: bytes) -> Path:
    root = _project_root()
    return root / DOCUMENT_TRANSPORT_ROOT / _safe_package_name(path, data)


def write_document(path: str | Path, content: str | bytes | bytearray | Any) -> dict[str, Any]:
    """
    Write a document through the Butler infrastructure writer.

    Returns metadata describing the selected mode. Existing callers may ignore
    the return value.
    """

    target = Path(path)
    if not target.is_absolute():
        target = _project_root() / target
    data = _to_bytes(content)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(data)

    result: dict[str, Any] = {
        "path": str(target),
        "bytes": len(data),
        "sha256": hashlib.sha256(data).hexdigest(),
        "mode": "direct",
        "transport_package": None,
        "written_at": datetime.now().isoformat(timespec="seconds"),
    }

    if len(data) > DOCUMENT_TRANSPORT_THRESHOLD_BYTES:
        package_dir = _transport_package_dir(target, data)
        manifest = pack(target, package_dir, target.name, DEFAULT_CHARS_PER_BLOCK)
        result["mode"] = "transport"
        result["transport_package"] = str(package_dir)
        result["transport_blocks"] = manifest["chunk_count"]
        result["transport_format"] = manifest["format"]

        metadata_path = package_dir / "writer_metadata.json"
        metadata_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding=DOCUMENT_TEXT_ENCODING)

    return result
