#!/usr/bin/env python3
"""
Read-only audit of document write locations in the active Butler tree.
"""

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path

from document_writer import write_document


ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = ROOT / "A_06_WORKSPACE" / "AUDITS"
EXCLUDE_PARTS = {
    ".git",
    "__pycache__",
    "A_00_LEGACY_ARCHIVE",
    "A_00_RESTORE",
    "A_06_WORKSPACE",
}
EXTENSIONS = {".py", ".ps1", ".bat", ".cmd"}
PATTERNS = [
    ("butler_write_document", re.compile(r"\bwrite_document\s*\(")),
    ("python_write_text", re.compile(r"\.write_text\s*\(")),
    ("python_write_bytes", re.compile(r"\.write_bytes\s*\(")),
    ("python_open_write", re.compile(r"open\s*\([^#\n]*(?:['\"]w['\"]|mode\s*=\s*['\"]w['\"])")),
    ("python_path_open_write", re.compile(r"\.open\s*\([^#\n]*(?:['\"]w['\"]|mode\s*=\s*['\"]w['\"])")),
    ("python_json_dump", re.compile(r"json\.dump\s*\(")),
    ("powershell_set_content", re.compile(r"\bSet-Content\b", re.IGNORECASE)),
    ("powershell_add_content", re.compile(r"\bAdd-Content\b", re.IGNORECASE)),
    ("powershell_out_file", re.compile(r"\bOut-File\b", re.IGNORECASE)),
    ("powershell_export_csv", re.compile(r"\bExport-Csv\b", re.IGNORECASE)),
]


def excluded(path: Path) -> bool:
    return bool(set(path.relative_to(ROOT).parts) & EXCLUDE_PARTS)


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def classify(path: str, line: str) -> str:
    low_path = path.lower()
    low_line = line.lower()
    if "write_document(" in low_line:
        return "refactored_to_write_document"
    if "butler_transport.py" in low_path:
        return "not_changed_transport_core"
    if "document_writer.py" in low_path:
        return "not_changed_writer_internal"
    if any(part in low_path for part in ["memory", "registry", "session", "queue", "state"]):
        return "not_changed_runtime_state"
    if any(part in low_path for part in ["log", "cache", "tmp", "progress"]):
        return "not_changed_cache_or_log"
    if any(part in low_path for part in ["inspector", "audit", "discovery", "linkmap", "dependency"]):
        return "not_changed_forbidden_inspector_auditor"
    if any(part in low_path for part in ["planner", "provider", "runtime"]):
        return "not_changed_forbidden_architecture"
    if any(token in low_line for token in [".md", ".txt", ".json", ".py", ".ps1", "report"]):
        return "document_generation_candidate"
    return "not_changed_needs_manual_review"


def scan() -> list[dict]:
    findings = []
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file() or excluded(path) or path.suffix.lower() not in EXTENSIONS:
            continue
        try:
            lines = path.read_text(encoding="utf-8-sig", errors="replace").splitlines()
        except OSError:
            continue
        for line_no, line in enumerate(lines, start=1):
            for name, pattern in PATTERNS:
                if pattern.search(line):
                    item = {
                        "path": rel(path),
                        "line": line_no,
                        "pattern": name,
                        "code": line.strip(),
                    }
                    item["classification"] = classify(item["path"], item["code"])
                    findings.append(item)
                    break
    return findings


def write_markdown(findings: list[dict], path: Path) -> None:
    counts: dict[str, int] = {}
    for item in findings:
        counts[item["classification"]] = counts.get(item["classification"], 0) + 1

    lines = [
        "# Butler Document Write Locations Audit",
        "",
        f"- Generated: {datetime.now().isoformat(timespec='seconds')}",
        f"- Active findings: {len(findings)}",
        f"- Excluded parts: `{', '.join(sorted(EXCLUDE_PARTS))}`",
        "",
        "## Classification Counts",
        "| Classification | Count |",
        "| --- | --- |",
    ]
    for key in sorted(counts):
        lines.append(f"| {key} | {counts[key]} |")

    lines.extend(["", "## Findings", "| Path | Line | Pattern | Classification | Code |", "| --- | --- | --- | --- | --- |"])
    for item in findings:
        code = item["code"].replace("|", "\\|")
        lines.append(
            f"| `{item['path']}` | {item['line']} | {item['pattern']} | {item['classification']} | `{code}` |"
        )
    write_document(path, "\n".join(lines))


def main() -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    findings = scan()
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    json_path = REPORT_DIR / f"DOCUMENT_WRITE_LOCATIONS_{stamp}.json"
    md_path = REPORT_DIR / f"DOCUMENT_WRITE_LOCATIONS_{stamp}.md"
    write_document(json_path, json.dumps({"generated_at": datetime.now().isoformat(timespec="seconds"), "findings": findings}, ensure_ascii=False, indent=2))
    write_markdown(findings, md_path)
    print("DOCUMENT_WRITE_AUDIT_OK")
    print(f"findings={len(findings)}")
    print(f"json={json_path}")
    print(f"md={md_path}")


if __name__ == "__main__":
    main()
