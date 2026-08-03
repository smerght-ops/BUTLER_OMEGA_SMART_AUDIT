#!/usr/bin/env python3
"""Inspector 0 — reproducible physical file map, schema 1.3."""

import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path


EXCLUDE_DIRS = {
    ".git", "__pycache__", "A_00_ARCHIVE_BACKUPS", "A_00_AVARIYKA",
    "A_00_HISTORY", "A_00_RESTORE", "A_00_LEGACY_ARCHIVE", "A_00_QUARANTINE",
    "AUDIT", "AUDITS", "AUDIT_PACKS", "LLM_READY", "venv",
}
EXCLUDE_FILES = {
    "local_project_audit.py", "PROJECT_AUDIT_INPUT.txt", "PROJECT_DUMP.txt",
    "PROJECT_FULL_CONTEXT_PACK.md",
}
KINDS = {
    ".py": "python", ".json": "json", ".jsonl": "json", ".md": "markdown",
    ".txt": "plaintext", ".ps1": "powershell", ".bat": "batch",
    ".csv": "csv", ".xml": "xml", ".html": "html",
}


def utc_timestamp(value=None):
    moment = datetime.fromtimestamp(value, timezone.utc) if value is not None else datetime.now(timezone.utc)
    return moment.isoformat(timespec="seconds").replace("+00:00", "Z")


def build(root: Path):
    records = []
    excluded = Counter()
    raw_total = 0
    errors = []
    for path in sorted(root.rglob("*"), key=lambda item: item.as_posix().casefold()):
        if not path.is_file():
            continue
        raw_total += 1
        relative = path.relative_to(root)
        blocked_dir = next((part for part in relative.parts[:-1] if part in EXCLUDE_DIRS), None)
        if blocked_dir:
            excluded[blocked_dir] += 1
            continue
        if path.name in EXCLUDE_FILES:
            excluded[f"file:{path.name}"] += 1
            continue
        try:
            stat = path.stat()
            extension = path.suffix.casefold()
            records.append({
                "id": len(records) + 1,
                "relative_path": relative.as_posix(),
                "filename": path.name,
                "extension": extension,
                "kind": KINDS.get(extension, "unknown"),
                "size_bytes": stat.st_size,
                "line_count": None,
                "modified_utc": utc_timestamp(stat.st_mtime),
                "sha256": None,
            })
        except OSError as exc:
            errors.append({"path": relative.as_posix(), "error": str(exc)})
    by_extension = Counter(row["extension"] for row in records)
    by_kind = Counter(row["kind"] for row in records)
    metadata = {
        "schema": "physical_map", "schema_version": "1.3",
        "generator": "Inspector0_PhysicalMap", "generator_version": "1.3",
        "generated_utc": utc_timestamp(), "project_root": root.as_posix(),
        "input": {"exclude_dirs": sorted(EXCLUDE_DIRS), "exclude_files": sorted(EXCLUDE_FILES),
                  "compute_hash": False, "count_lines": False},
        "statistics": {
            "total_raw_files": raw_total, "total_files": len(records),
            "total_bytes": sum(row["size_bytes"] for row in records), "total_line_count": None,
            "errors_count": len(errors), "excluded_total": sum(excluded.values()),
            "excluded_details": dict(sorted(excluded.items())),
            "by_extension": dict(sorted(by_extension.items())), "by_kind": dict(sorted(by_kind.items())),
        },
    }
    return {"metadata": metadata, "errors": errors, "payload": records}


if __name__ == "__main__":
    import sys
    project_root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path.cwd().resolve()
    output_path = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("Inspector0_PhysicalMap.json")
    result = build(project_root)
    output_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print("STATUS  : SUCCESS")
    print(f"OUTPUT  : {output_path}")
    print(f"FILES   : {len(result['payload'])}")
    print(f"ERRORS  : {len(result['errors'])}")
