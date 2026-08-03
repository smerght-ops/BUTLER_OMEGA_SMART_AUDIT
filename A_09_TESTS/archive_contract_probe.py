# -*- coding: utf-8 -*-
import hashlib
import json
import shutil
import uuid
from pathlib import Path

from A_03_ORCHESTRATION.dispatcher_bridge_v2 import _dispatcher


REQUIRED = {"ok", "department", "model", "text", "error", "metadata"}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    root = Path("C:/Test") / f"ArchiveContractProbe_{uuid.uuid4().hex}"
    source = root / "source"
    archive = root / "dest" / "probe.zip"
    extracted = root / "extracted"
    conflict = root / "conflict"
    results = []
    try:
        (source / "nested" / "empty").mkdir(parents=True)
        (source / "root.txt").write_text("root", encoding="utf-8")
        (source / "nested" / "child.json").write_text('{"ok":true}', encoding="utf-8")
        conflict.mkdir(parents=True)
        (conflict / "root.txt").write_text("sentinel", encoding="utf-8")

        cases = (
            ("create", f"Заархивируй папку {source} в архив {archive}"),
            ("target_exists", f"Заархивируй папку {source} в архив {archive}"),
            ("inspect", f"Покажи содержимое архива {archive}"),
            ("extract", f"Распакуй архив {archive} в папку {extracted}"),
            ("extract_conflict", f"Распакуй архив {archive} в папку {conflict}"),
            ("archive_not_found", f"Покажи содержимое архива {root / 'missing.zip'}"),
            ("source_not_found", f"Заархивируй папку {root / 'missing'} в архив {root / 'missing-target.zip'}"),
            ("relative_rejected", "Покажи содержимое архива relative.zip"),
        )
        for name, query in cases:
            result = _dispatcher.dispatch(query, {"attachments": []})
            results.append({
                "name": name,
                "contract_complete": REQUIRED.issubset(result),
                "department": result.get("department"),
                "ok": result.get("ok"),
                "error": result.get("error"),
                "metadata": result.get("metadata"),
            })

        evidence = {
            "hashes_match": (
                digest(source / "root.txt") == digest(extracted / "root.txt")
                and digest(source / "nested" / "child.json") == digest(extracted / "nested" / "child.json")
            ),
            "empty_folder_preserved": (extracted / "nested" / "empty").is_dir(),
            "conflict_sentinel_preserved": (conflict / "root.txt").read_text(encoding="utf-8") == "sentinel",
            "conflict_partial_extract_absent": not (conflict / "nested" / "child.json").exists(),
        }
        passed = (
            all(item["contract_complete"] and item["department"] == "ARCHIVE" for item in results)
            and [item["error"] for item in results] == [
                None, "ARCHIVE_TARGET_EXISTS", None, None, "ARCHIVE_EXTRACT_CONFLICT",
                "ARCHIVE_NOT_FOUND", "ARCHIVE_SOURCE_NOT_FOUND", "ARCHIVE_PATH_NOT_ABSOLUTE",
            ]
            and all(evidence.values())
        )
        print(json.dumps({"status": "PASS" if passed else "FAIL", "results": results, "evidence": evidence}, ensure_ascii=False, indent=2))
        return 0 if passed else 1
    finally:
        if root.exists():
            shutil.rmtree(root)


if __name__ == "__main__":
    raise SystemExit(main())
