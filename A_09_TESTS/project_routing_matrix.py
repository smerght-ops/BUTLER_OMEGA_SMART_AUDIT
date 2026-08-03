from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from A_03_ORCHESTRATION.dispatcher_bridge_v2 import _dispatcher


PROJECT = r"C:\Users\KOS\Desktop\Butler_Agent\BUTLER_OMEGA_SMART — копия"
QUERIES = (
    r"Проанализируй папку C:\Test",
    r"Проанализируй каталог C:\Test",
    r"Проанализируй директорию C:\Test",
    f'Проанализируй проект "{PROJECT}"',
    f'Проанализируй копию проекта "{PROJECT}"',
    f'Проанализируй проект "{PROJECT}" и покажи, что можно безопасно удалить',
    f'Покажи, что можно удалить из проекта "{PROJECT}"',
    f'Покажи, что можно безопасно удалить из проекта "{PROJECT}"',
    f'Очисти проект "{PROJECT}"',
    r'Проанализируй документ "C:\Test\document.txt"',
    "Подготовь документацию проекта Butler",
    "Какой статус проекта Butler?",
    "Проанализируй архитектуру проекта Butler",
    "Проанализируй проект Butler",
)


def main() -> int:
    rows = []
    for query in QUERIES:
        values = {}
        selected = None
        for department in _dispatcher.departments:
            name = str(getattr(department, "NAME", type(department).__name__))
            try:
                handled = bool(department.can_handle(query, context={}))
                values[name] = handled
            except TypeError:
                handled = bool(department.can_handle(query))
                values[name] = handled
            except Exception as exc:
                values[name] = f"{type(exc).__name__}: {exc}"
                handled = False
            if selected is None and handled:
                selected = name
        rows.append({
            "query": query,
            "filesystem": values.get("FILESYSTEM"),
            "documents": values.get("DOCUMENTS"),
            "selected": selected or "CHAT",
        })
    print(json.dumps(rows, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
