#!/usr/bin/env python3
"""
Inspector 3 — Registration AST v1.0
READ ONLY. Находит регистрации компонентов через AST (вызовы register, Dispatcher и т.п.).
Не делает выводов. Только факты.
"""

import ast
from pathlib import Path
from typing import Dict, List, Any

from BaseInspector import BaseInspector

class Inspector3_RegistrationAST(BaseInspector):
    SCHEMA = "registration_ast"
    SCHEMA_VERSION = "1.0"
    GENERATOR = "Inspector3_RegistrationAST"
    GENERATOR_VERSION = "1.0"
    TARGET_KIND = "python"

    REGISTRATION_NAMES = {
        'register', 'add_handler', 'register_department', 'register_agent',
        'register_engine', 'register_skill', 'register_service', 'register_module',
        'register_plugin', 'add_route', 'Dispatcher'
    }

    def __init__(self, input_path: str, output_path: str):
        super().__init__(input_path, output_path)
        self.total_registrations = 0

    def process_file(self, file_info: Dict) -> Dict:
        file_path = file_info["path"]
        try:
            source = file_path.read_text(encoding='utf-8-sig', errors='ignore')
            tree = ast.parse(source)
        except Exception as e:
            return {"id": file_info["id"], "error": str(e)}

        extractor = RegistrationExtractor(self.REGISTRATION_NAMES)
        extractor.visit(tree)

        self.total_registrations += len(extractor.registrations)

        return {
            "id": file_info["id"],
            "registrations": extractor.registrations,
        }

    def _add_statistics(self):
        self.metadata["statistics"]["total_registrations"] = self.total_registrations


class RegistrationExtractor(ast.NodeVisitor):
    def __init__(self, registration_names: set):
        self.registration_names = registration_names
        self.registrations: List[Dict] = []

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name):
            func_name = node.func.id
        elif isinstance(node.func, ast.Attribute):
            func_name = node.func.attr
        else:
            func_name = None

        if func_name and func_name in self.registration_names:
            if func_name == 'Dispatcher':
                kind = 'constructor'
            elif func_name.startswith('register'):
                kind = 'register_call'
            elif func_name.startswith('add_'):
                kind = 'add_call'
            else:
                kind = 'other'

            args = []
            for arg in node.args[:3]:
                # Исправляем устаревшее ast.Str на ast.Constant
                if isinstance(arg, ast.Constant) and isinstance(arg.value, str):
                    args.append(repr(arg.value))
                elif isinstance(arg, ast.Name):
                    args.append(arg.id)
                else:
                    args.append('<expr>')

            self.registrations.append({
                "kind": kind,
                "function": func_name,
                "line": node.lineno,
                "args": args,
                "context": ast.unparse(node)[:200],
            })

        self.generic_visit(node)


if __name__ == "__main__":
    import sys
    input_path = sys.argv[1] if len(sys.argv) > 1 else "Inspector0_PhysicalMap.json"
    output_path = sys.argv[2] if len(sys.argv) > 2 else "Inspector3_RegistrationAST.json"
    inspector = Inspector3_RegistrationAST(input_path, output_path)
    inspector.run()
