#!/usr/bin/env python3
"""
Inspector 5 — Dependency Graph v1.0
Агрегирует данные из Inspector1-4 и строит граф зависимостей.
READ ONLY. Не делает выводов. Только факты и связи.
"""

import json
from pathlib import Path
from typing import Dict, List, Any

class Inspector5_DependencyGraph:
    def __init__(self,
                 entity_path: str = "Inspector1_EntityMap.json",
                 import_path: str = "Inspector2_ImportMap.json",
                 registration_path: str = "Inspector3_RegistrationAST.json",
                 call_path: str = "Inspector4_CallGraph.json",
                 output_path: str = "Inspector5_DependencyGraph.json"):
        self.entity_path = Path(entity_path)
        self.import_path = Path(import_path)
        self.registration_path = Path(registration_path)
        self.call_path = Path(call_path)
        self.output_path = Path(output_path)
        self.graph = {
            "nodes": [],
            "edges": []
        }

    def load_json(self, path: Path) -> Dict:
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"ERROR: Cannot read {path}: {e}")
            return {}

    def build(self):
        print("Loading data...")
        entities = self.load_json(self.entity_path)
        imports = self.load_json(self.import_path)
        registrations = self.load_json(self.registration_path)
        calls = self.load_json(self.call_path)

        print(f"Entities: {len(entities.get('payload', []))} files")
        print(f"Imports: {len(imports.get('payload', []))} files")
        print(f"Registrations: {len(registrations.get('payload', []))} files")
        print(f"Calls: {len(calls.get('payload', []))} files")

        # Здесь будет логика построения графа (пока заглушка)
        self.graph["nodes"] = [{"id": "placeholder", "type": "file"}]
        self.graph["edges"] = [{"source": "placeholder", "target": "placeholder", "type": "import"}]

    def save(self):
        try:
            with open(self.output_path, 'w', encoding='utf-8') as f:
                json.dump(self.graph, f, ensure_ascii=False, indent=2)
            print(f"SUCCESS: Graph saved to {self.output_path}")
        except Exception as e:
            print(f"ERROR: Failed to write output: {e}")

if __name__ == "__main__":
    import sys
    # Можно добавить аргументы командной строки позже
    builder = Inspector5_DependencyGraph()
    builder.build()
    builder.save()
