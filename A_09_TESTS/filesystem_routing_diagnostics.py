from __future__ import annotations

import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from A_01_CORE.TaskExecutor import TaskExecutor
from A_03_ORCHESTRATION.dispatcher_bridge_v2 import _dispatcher, dispatch


QUERIES = (
    r"Проанализируй папку C:\Test",
    r"Проанализируй каталог C:\Test",
    r"Очисти папку C:\Test",
    r"Покажи, что можно удалить из папки C:\Test",
    "Удали резервные файлы",
)


def main() -> int:
    planner = TaskExecutor()
    rows = []
    for query in QUERIES:
        result = dispatch(query, {})
        rows.append({
            "query": query,
            "plan": planner.plan(query),
            "can_handle": {
                str(getattr(department, "NAME", type(department).__name__)): department.can_handle(query, context={})
                for department in _dispatcher.departments
            },
            "dispatch_result": {
                "ok": result.get("ok"), "department": result.get("department"),
                "error": result.get("error"), "action": result.get("metadata", {}).get("action"),
            },
        })
    print(json.dumps(rows, ensure_ascii=False, indent=2, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
