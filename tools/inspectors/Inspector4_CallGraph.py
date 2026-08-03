#!/usr/bin/env python3
"""
Inspector 4 — Call Graph v1.0
READ ONLY. Собирает все вызовы функций и методов в .py-файлах (через AST).
Не делает выводов. Только факты.
"""

import ast
from pathlib import Path
from typing import Dict, List

from BaseInspector import BaseInspector

class Inspector4_CallGraph(BaseInspector):
    SCHEMA = "call_graph"
    SCHEMA_VERSION = "1.0"
    GENERATOR = "Inspector4_CallGraph"
    GENERATOR_VERSION = "1.0"
    TARGET_KIND = "python"

    def __init__(self, input_path: str, output_path: str):
        super().__init__(input_path, output_path)
        self.total_calls = 0

    def process_file(self, file_info: Dict) -> Dict:
        file_path = file_info["path"]
        try:
            source = file_path.read_text(encoding='utf-8-sig', errors='ignore')
            tree = ast.parse(source)
        except Exception as e:
            return {"id": file_info["id"], "error": str(e)}

        extractor = CallExtractor()
        extractor.visit(tree)

        self.total_calls += len(extractor.calls)

        return {
            "id": file_info["id"],
            "calls": extractor.calls,
        }

    def _add_statistics(self):
        self.metadata["statistics"]["total_calls"] = self.total_calls


class CallExtractor(ast.NodeVisitor):
    def __init__(self):
        self.calls: List[Dict] = []
        self.current_function = None
        self.current_class = None

    def visit_FunctionDef(self, node):
        previous_function = self.current_function
        self.current_function = node.name
        self.generic_visit(node)
        self.current_function = previous_function

    def visit_ClassDef(self, node):
        previous_class = self.current_class
        self.current_class = node.name
        self.generic_visit(node)
        self.current_class = previous_class

    def visit_Call(self, node):
        # Определяем имя вызываемой функции/метода
        if isinstance(node.func, ast.Name):
            callee = node.func.id
        elif isinstance(node.func, ast.Attribute):
            callee = node.func.attr
        else:
            callee = '<complex>'

        # Определяем контекст (внутри какой функции или класса)
        context = None
        if self.current_class and self.current_function:
            context = f"{self.current_class}.{self.current_function}"
        elif self.current_function:
            context = self.current_function
        elif self.current_class:
            context = self.current_class

        self.calls.append({
            "callee": callee,
            "line": node.lineno,
            "context": context,
        })

        self.generic_visit(node)


if __name__ == "__main__":
    import sys
    input_path = sys.argv[1] if len(sys.argv) > 1 else "Inspector0_PhysicalMap.json"
    output_path = sys.argv[2] if len(sys.argv) > 2 else "Inspector4_CallGraph.json"
    inspector = Inspector4_CallGraph(input_path, output_path)
    inspector.run()
