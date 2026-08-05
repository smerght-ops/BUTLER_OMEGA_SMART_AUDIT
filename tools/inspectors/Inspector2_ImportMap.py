#!/usr/bin/env python3
"""
Inspector 2 — Import Map v1.3
READ ONLY. Извлекает импорты из .py-файлов.
Не делает выводов. Только факты.
"""

import ast
from pathlib import Path
from typing import Dict, List

from BaseInspector import BaseInspector

class Inspector2_ImportMap(BaseInspector):
    SCHEMA = "import_map"
    SCHEMA_VERSION = "1.3"
    GENERATOR = "Inspector2_ImportMap"
    GENERATOR_VERSION = "1.3"
    TARGET_KIND = "python"

    def __init__(self, input_path: str, output_path: str):
        super().__init__(input_path, output_path)
        self.total_imports = 0

    def process_file(self, file_info: Dict) -> Dict:
        file_path = file_info["path"]
        try:
            source = file_path.read_text(encoding='utf-8-sig', errors='ignore')
            tree = ast.parse(source)
        except Exception as e:
            return {"id": file_info["id"], "error": str(e)}

        extractor = ImportExtractor()
        extractor.visit(tree)

        self.total_imports += len(extractor.imports)

        return {
            "id": file_info["id"],
            "imports": extractor.imports,
        }

    def _add_statistics(self):
        self.metadata["statistics"]["total_imports"] = self.total_imports


class ImportExtractor(ast.NodeVisitor):
    def __init__(self):
        self.imports: List[Dict] = []

    def visit_Import(self, node):
        for alias in node.names:
            self.imports.append({
                "kind": "import",
                "module": alias.name,
                "name": None,
                "alias": alias.asname,
                "line": node.lineno,
            })
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        module = node.module if node.module else ""
        for alias in node.names:
            self.imports.append({
                "kind": "from",
                "module": module,
                "name": alias.name,
                "alias": alias.asname,
                "line": node.lineno,
            })
        self.generic_visit(node)


if __name__ == "__main__":
    import sys
    input_path = sys.argv[1] if len(sys.argv) > 1 else "Inspector0_PhysicalMap.json"
    output_path = sys.argv[2] if len(sys.argv) > 2 else "Inspector2_ImportMap.json"
    inspector = Inspector2_ImportMap(input_path, output_path)
    inspector.run()
