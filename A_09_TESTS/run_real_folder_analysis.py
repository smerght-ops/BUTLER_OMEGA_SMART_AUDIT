from __future__ import annotations

import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from A_03_ORCHESTRATION.dispatcher_bridge_v2 import dispatch


def main() -> int:
    target = Path(r"C:\Users\KOS\Desktop\Butler_Agent\BUTLER_OMEGA_SMART — копия")
    result = dispatch(f'Проанализируй папку "{target}" и покажи, что можно удалить', {})
    metadata = result.get("metadata", {})
    categories = metadata.get("categories", {})
    entries = metadata.get("analysis_snapshot", {}).get("entries", [])
    markers = ("project_full_context_pack", "project_dump", "observations.jsonl", "generated_images")
    summary = {
        "ok": result.get("ok"),
        "error": result.get("error"),
        "read_only": metadata.get("read_only"),
        "path": metadata.get("path"),
        "file_count": metadata.get("file_count"),
        "folder_count": metadata.get("folder_count"),
        "total_bytes": metadata.get("total_bytes"),
        "duration_ms": metadata.get("duration_ms"),
        "categories": {
            key: {
                "files": value.get("file_count"),
                "folders": value.get("folder_count"),
                "bytes": value.get("bytes"),
                "selectable": value.get("selectable"),
                "duplicate_groups": len(value.get("groups", [])),
            }
            for key, value in categories.items()
        },
        "named_examples": [
            item["relative_path"] for item in entries
            if any(marker in item["relative_path"].casefold() for marker in markers)
        ][:40],
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0 if result.get("ok") and metadata.get("read_only") else 1


if __name__ == "__main__":
    raise SystemExit(main())
