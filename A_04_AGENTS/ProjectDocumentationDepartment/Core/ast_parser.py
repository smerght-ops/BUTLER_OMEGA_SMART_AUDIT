# -*- coding: utf-8 -*-
"""AST import parser — uses RepositoryKnowledgeDepartment for file enumeration.

Uses the approved gateway-backed canonical file inventory.
"""

import ast
import json
from pathlib import Path

from A_03_ORCHESTRATION.repository_knowledge_gateway import list_repository_files

ROOT = Path.cwd()
OUTPUT_FILE = ROOT / "PROJECT_FACTS_IMPORTS.json"


def parse_file(filepath):
    # utf-8-sig автоматически съедает маркер U+FEFF (BOM), если он есть
    try:
        content = filepath.read_text(encoding="utf-8-sig")
        tree = ast.parse(content, filename=str(filepath))

        imports = []
        from_imports = []

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                module = node.module if node.module else ""
                names = [alias.name for alias in node.names]
                from_imports.append({"module": module, "names": names})

        return {
            "file": filepath.relative_to(ROOT).as_posix(),
            "imports": imports,
            "from_imports": from_imports,
            "errors": []
        }
    except SyntaxError as e:
        return {
            "file": filepath.relative_to(ROOT).as_posix(),
            "imports": [],
            "from_imports": [],
            "errors": [f"SyntaxError: {e}"]
        }
    except Exception as e:
        return {
            "file": filepath.relative_to(ROOT).as_posix(),
            "imports": [],
            "from_imports": [],
            "errors": [f"Error: {e}"]
        }


def main():
    print("Запуск AST-парсера (интеграция RepositoryKnowledgeDepartment v1.1)...")

    py_files_rel = list_repository_files(ROOT, ".py")

    results = []
    excluded_zones = ["Filtered by RepositoryKnowledgeDepartment"]

    for rel_path in py_files_rel:
        full_path = ROOT / Path(rel_path)
        if not full_path.exists():
            continue
        results.append(parse_file(full_path))

    final_data = {
        "excluded_zones": excluded_zones,
        "python_imports": results
    }

    OUTPUT_FILE.write_text(json.dumps(final_data, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
