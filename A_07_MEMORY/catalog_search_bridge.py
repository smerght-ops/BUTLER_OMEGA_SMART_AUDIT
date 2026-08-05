# -*- coding: utf-8 -*-

from pathlib import Path

from A_02_MANAGERS.catalog_manager import CatalogManager
from A_07_MEMORY.SESSION.session_manager_poly import SessionManagerPoly


class CatalogSearchBridge:
    def __init__(self):
        self.catalog = CatalogManager()
        self.session_manager = SessionManagerPoly()
        self.project_root = Path(__file__).resolve().parents[1]

    def _catalog_path_state(self, filepath):
        path = Path(str(filepath))
        resolved = path if path.is_absolute() else self.project_root / path

        if resolved.is_file():
            return str(resolved.resolve()), True

        filename = resolved.name

        search_dirs = [
            self.project_root / "A_06_WORKSPACE" / "incoming",
            self.project_root / "A_06_WORKSPACE" / "ARCHIVE_DONE",
        ]

        for folder in search_dirs:
            candidate = folder / filename
            if candidate.is_file():
                return str(candidate.resolve()), True

        return str(resolved.resolve()), False

    def search(self, query: str, limit: int = 5) -> dict:
        q = (query or "").strip()
        if not q:
            return {
                "ok": False,
                "text": "Пустой поисковый запрос.",
                "results": [],
                "error": "EMPTY_QUERY"
            }

        # ПРИБОРНЫЙ СРЕЗ (Слой 4.35.1)
        print(f"\n[DEBUG BRIDGE] RAW INPUT  : {repr(query)}")
        print(f"[DEBUG BRIDGE] SQL TARGET  : {repr(q)}")
        print(f"[DEBUG BRIDGE] TARGET LEN  : {len(q)}")

        results = self.catalog.full_text_search(q)

        # ЗАЩИЩЕННЫЙ ПРИБОРНЫЙ СРЕЗ РЕЗУЛЬТАТОВ SQL
        if results is None:
            print("[DEBUG BRIDGE] SQL returned None")
        elif not results:
            print("[DEBUG BRIDGE] SQL returned 0 rows")
        else:
            print(f"[DEBUG BRIDGE] SQL ROWS    : {len(results)}")
            for row in results[:3]:
                print(f"[DEBUG BRIDGE]   -> ID: {row[0]} | PATH: {row[1]}")
        print("-" * 50)

        if not results:
            # Если ничего не нашли, фиксируем факт пустого поиска в сессии
            self.session_manager.update_search_context(
                original_query=q,
                normalized=q,
                expanded=[],
                rich_results=[]
            )
            return {
                "ok": True,
                "text": f"В архивном каталоге ничего не найдено по запросу: {q}",
                "results": [],
                "error": None
            }

        lines = [f"Найдено в архивном каталоге по запросу: {q}"]
        packed = []
        rich_results = []

        for row in results[:limit]:
            doc_id, filepath, summary, tags = row
            canonical_path, available = self._catalog_path_state(filepath)
            packed.append({
                "id": doc_id,
                "filepath": canonical_path,
                "summary": summary,
                "tags": tags,
                "available": available,
            })
            # Наполнение богатого кэша сессии для семантического взаимодействия
            rich_results.append({
                "id": doc_id,
                "filepath": canonical_path,
                "summary": summary,
                "tags": tags,
                "available": available,
            })
            lines.append("")
            lines.append(f"- ID: {doc_id}")
            lines.append(f"  Файл: {canonical_path}")
            lines.append(f"  Доступен: {'да' if available else 'нет'}")
            lines.append(f"  Кратко: {summary}")
            lines.append(f"  Теги: {tags}")

        # Фиксируем поисковое событие в живой сессии
        self.session_manager.update_search_context(
            original_query=q,
            normalized=q,
            expanded=[],
            rich_results=rich_results
        )

        return {
            "ok": True,
            "text": "\n".join(lines),
            "results": packed,
            "error": None
        }
