#!/usr/bin/env python3
"""
Inspector 3 — Registration Map v1.0
READ ONLY. Находит регистрации компонентов в .py-файлах (паттерны register, Dispatcher и т.п.).
Не делает выводов. Только факты.
"""

import re
from pathlib import Path
from typing import Dict, List

from BaseInspector import BaseInspector

class Inspector3_RegistrationMap(BaseInspector):
    SCHEMA = "registration_map"
    SCHEMA_VERSION = "1.0"
    GENERATOR = "Inspector3_RegistrationMap"
    GENERATOR_VERSION = "1.0"
    TARGET_KIND = "python"

    # Паттерны регистраций (регулярные выражения)
    PATTERNS = [
        r'\bregister\s*\(',
        r'\badd_handler\s*\(',
        r'\bDispatcher\s*\(',
        r'\bregistry\b',
        r'\bfactory\b',
        r'self\.departments\b',
        r'\bregister_department\s*\(',
        r'\badd_route\s*\(',
        r'\bregister_agent\s*\(',
        r'\bregister_engine\s*\(',
        r'\bregister_skill\s*\(',
        r'\bregister_service\s*\(',
        r'\bregister_module\s*\(',
        r'\bregister_plugin\s*\(',
    ]
    # Компилируем регулярки с флагом re.IGNORECASE
    COMPILED_PATTERNS = [re.compile(p, re.IGNORECASE) for p in PATTERNS]

    def __init__(self, input_path: str, output_path: str):
        super().__init__(input_path, output_path)
        self.total_registrations = 0

    def process_file(self, file_info: Dict) -> Dict:
        file_path = file_info["path"]
        try:
            source = file_path.read_text(encoding='utf-8-sig', errors='ignore')
        except Exception as e:
            return {"id": file_info["id"], "error": str(e)}

        lines = source.splitlines()
        registrations = []

        for line_no, line in enumerate(lines, start=1):
            for pattern_obj in self.COMPILED_PATTERNS:
                if pattern_obj.search(line):
                    registrations.append({
                        "pattern": pattern_obj.pattern,
                        "line": line_no,
                        "context": line.strip(),
                    })
                    break  # только первое совпадение на строке

        self.total_registrations += len(registrations)

        return {
            "id": file_info["id"],
            "registrations": registrations,
        }

    def _add_statistics(self):
        self.metadata["statistics"]["total_registrations"] = self.total_registrations


if __name__ == "__main__":
    import sys
    input_path = sys.argv[1] if len(sys.argv) > 1 else "Inspector0_PhysicalMap.json"
    output_path = sys.argv[2] if len(sys.argv) > 2 else "Inspector3_RegistrationMap.json"
    inspector = Inspector3_RegistrationMap(input_path, output_path)
    inspector.run()
