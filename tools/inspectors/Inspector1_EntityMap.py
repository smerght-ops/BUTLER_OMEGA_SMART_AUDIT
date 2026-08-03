#!/usr/bin/env python3
"""
Inspector 1 — Entity Map v1.3
READ ONLY. Извлекает сущности (классы, функции, переменные) из .py-файлов.
Не делает выводов. Только факты.
"""

import ast
from pathlib import Path
from typing import Dict, List

from BaseInspector import BaseInspector
REGISTRATION_NAMES = {
    "register",
    "register_handler",
    "register_department",
    "register_agent",
    "register_engine",
    "register_skill",
    "register_service",
    "register_module",
    "register_plugin",
    "add_handler",
    "add_route",
    "include_router",
    "Dispatcher"
}


class Inspector1_EntityMap(BaseInspector):
    SCHEMA = "entity_map"
    SCHEMA_VERSION = "1.3"
    GENERATOR = "Inspector1_EntityMap"
    GENERATOR_VERSION = "1.3"
    TARGET_KIND = "python"

    def __init__(self, input_path: str, output_path: str):
        super().__init__(input_path, output_path)
        self.total_classes = 0
        self.total_functions = 0
        self.total_variables = 0
        self.total_imports = 0
        self.total_registrations = 0
        self.total_calls = 0

    def process_file(self, file_info: Dict) -> Dict:
        file_path = file_info["path"]
        try:
            source = file_path.read_text(encoding='utf-8-sig', errors='ignore')
            tree = ast.parse(source)
        except Exception as e:
            return {"id": file_info["id"], "error": str(e)}

        extractor = EntityExtractor()
        extractor.visit(tree)

        self.total_classes += len(extractor.classes)
        self.total_functions += len(extractor.functions)
        self.total_variables += len(extractor.variables)
        self.total_imports += len(extractor.imports)
        self.total_registrations += len(extractor.registrations)
        self.total_calls += len(extractor.calls)

        return {
            "id": file_info["id"],
            "classes": extractor.classes,
            "functions": extractor.functions,
            "variables": extractor.variables,
            "imports": extractor.imports,
            "registrations": extractor.registrations,
            "calls": extractor.calls,
        }

    def _add_statistics(self):
        self.metadata["statistics"]["total_classes"] = self.total_classes
        self.metadata["statistics"]["total_functions"] = self.total_functions
        self.metadata["statistics"]["total_variables"] = self.total_variables
        self.metadata["statistics"]["total_imports"] = self.total_imports
        self.metadata["statistics"]["total_registrations"] = self.total_registrations
        self.metadata["statistics"]["total_calls"] = self.total_calls


class EntityExtractor(ast.NodeVisitor):
    def __init__(self):
        self.classes: List[Dict] = []
        self.functions: List[Dict] = []
        self.variables: List[Dict] = []
        self.imports: List[Dict] = []
        self.registrations: List[Dict] = []
        self.calls: List[Dict] = []
        self._current_class = None

    def visit_Import(self, node):
        for alias in node.names:
            self.imports.append({
                "kind": "import",
                "module": alias.name,
                "name": alias.asname or alias.name,
                "lineno": node.lineno,
            })
        self.generic_visit(node)
    def visit_ImportFrom(self, node):
        module = node.module if node.module else ""

        for alias in node.names:
            self.imports.append({
                "kind": "from",
                "module": module,
                "name": alias.name,
                "asname": alias.asname,
                "lineno": node.lineno,
            })

        self.generic_visit(node)
    def visit_Call(self, node):
        if isinstance(node.func, ast.Name):
            callee = node.func.id
        elif isinstance(node.func, ast.Attribute):
            callee = node.func.attr
        else:
            callee = "<complex>"

        call_record = {
            "callee": callee,
            "lineno": node.lineno,
            "context_class": self._current_class,
        }

        self.calls.append(call_record)

        if callee in REGISTRATION_NAMES:
            self.registrations.append(call_record.copy())

        self.generic_visit(node)
    def visit_ClassDef(self, node):
        methods = []
        for item in node.body:
            if isinstance(item, ast.FunctionDef):
                methods.append({
                    "name": item.name,
                    "args": [arg.arg for arg in item.args.args],
                    "lineno": item.lineno,
                })
        self.classes.append({
            "name": node.name,
            "lineno": node.lineno,
            "methods": methods,
        })
        self._current_class = node.name
        self.generic_visit(node)
        self._current_class = None

    def visit_FunctionDef(self, node):
        if self._current_class is None:
            self.functions.append({
                "name": node.name,
                "args": [arg.arg for arg in node.args.args],
                "lineno": node.lineno,
            })
        self.generic_visit(node)

    def visit_Assign(self, node):
        if self._current_class is None:
            for target in node.targets:
                if isinstance(target, ast.Name):
                    self.variables.append({
                        "name": target.id,
                        "lineno": node.lineno,
                    })
        self.generic_visit(node)


if __name__ == "__main__":
    import sys
    input_path = sys.argv[1] if len(sys.argv) > 1 else "Inspector0_PhysicalMap.json"
    output_path = sys.argv[2] if len(sys.argv) > 2 else "UnifiedInspectorFacts.json"
    inspector = Inspector1_EntityMap(input_path, output_path)
    inspector.run()










