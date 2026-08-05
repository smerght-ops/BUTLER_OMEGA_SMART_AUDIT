#!/usr/bin/env python3
"""
LinkMapBuilder — строит нормализованный список связей между артефактами.
Не инспектирует файлы. Работает только с JSON-артефактами.
Не делает выводов. Только факты.
"""

import json
import sys
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, List, Any

class LinkMapBuilder:
    SCHEMA = "link_map"
    SCHEMA_VERSION = "1.0"
    GENERATOR = "LinkMapBuilder"
    GENERATOR_VERSION = "1.0"

    def __init__(self, output_path: str):
        self.output_path = Path(output_path)
        self.links: List[Dict] = []
        self.total_links = 0
        self.metadata: Dict = {}

    def load_json(self, path: Path) -> Dict:
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"ERROR: Cannot load {path}: {e}", file=sys.stderr)
            return {}

    def build(self):
        # Загружаем все артефакты
        physical_map = self.load_json(Path("Inspector0_PhysicalMap.json"))
        entity_map = self.load_json(Path("Inspector1_EntityMap.json"))
        import_map = self.load_json(Path("Inspector2_ImportMap.json"))
        registration_map = self.load_json(Path("Inspector3_RegistrationAST.json"))
        call_graph = self.load_json(Path("Inspector4_CallGraph.json"))

        # Проверяем, что все файлы загружены
        if not physical_map or not entity_map or not import_map or not registration_map or not call_graph:
            print("ERROR: One or more input files missing.", file=sys.stderr)
            sys.exit(1)

        # Собираем связи из импортов
        for file_entry in import_map.get("payload", []):
            file_id = file_entry.get("id")
            imports = file_entry.get("imports", [])
            for imp in imports:
                self.links.append({
                    "source": file_id,
                    "target": imp.get("module"),
                    "type": "import",
                    "metadata": {
                        "kind": imp.get("kind"),
                        "name": imp.get("name"),
                        "alias": imp.get("alias"),
                        "line": imp.get("line"),
                    }
                })

        # Связи из вызовов
        for file_entry in call_graph.get("payload", []):
            file_id = file_entry.get("id")
            calls = file_entry.get("calls", [])
            for call in calls:
                self.links.append({
                    "source": file_id,
                    "target": call.get("callee"),
                    "type": "call",
                    "metadata": {
                        "context": call.get("context"),
                        "line": call.get("line"),
                    }
                })

        # Связи из регистраций
        for file_entry in registration_map.get("payload", []):
            file_id = file_entry.get("id")
            registrations = file_entry.get("registrations", [])
            for reg in registrations:
                self.links.append({
                    "source": file_id,
                    "target": reg.get("function"),
                    "type": "registration",
                    "metadata": {
                        "kind": reg.get("kind"),
                        "args": reg.get("args"),
                        "line": reg.get("line"),
                    }
                })

        # Дополнительно: связи из сущностей (класс наследует, функция принадлежит классу и т.д.)
        # Пока пропустим, но можно добавить позже.

        self.total_links = len(self.links)

        # Формируем метаданные
        self.metadata = {
            "schema": self.SCHEMA,
            "schema_version": self.SCHEMA_VERSION,
            "generator": self.GENERATOR,
            "generator_version": self.GENERATOR_VERSION,
            "generated_utc": datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
            "input": {
                "physical_map": "Inspector0_PhysicalMap.json",
                "entity_map": "Inspector1_EntityMap.json",
                "import_map": "Inspector2_ImportMap.json",
                "registration_map": "Inspector3_RegistrationAST.json",
                "call_graph": "Inspector4_CallGraph.json",
            },
            "statistics": {
                "total_links": self.total_links,
            }
        }

        # Запись выходного JSON
        output = {
            "metadata": self.metadata,
            "payload": self.links,
        }
        try:
            with open(self.output_path, 'w', encoding='utf-8') as f:
                json.dump(output, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"ERROR: Failed to write output: {e}", file=sys.stderr)
            sys.exit(1)

        # Итоговый отчёт в консоль
        print(f"STATUS  : SUCCESS")
        print(f"OUTPUT  : {self.output_path}")
        print(f"LINKS   : {self.total_links}")
        print(f"ERRORS  : 0")


if __name__ == "__main__":
    import sys
    output_path = sys.argv[1] if len(sys.argv) > 1 else "LinkMap.json"
    builder = LinkMapBuilder(output_path)
    builder.build()
