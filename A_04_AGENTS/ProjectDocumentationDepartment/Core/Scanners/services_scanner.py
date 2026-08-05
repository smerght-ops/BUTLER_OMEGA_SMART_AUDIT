# -*- coding: utf-8 -*-

from pathlib import Path


class ServicesScanner:
    """
    Discovery scanner for project-level services.

    PHASE 4.4
    ROADMAP_v0.3

    В текущей архитектуре Butler отдельного ServicesManager
    не обнаружено, поэтому сервисами считаются базовые
    инфраструктурные подсистемы проекта.
    """

    def __init__(self):

        self.project_root = Path(__file__).resolve().parents[3]

        self.services = [
            ("OLLAMA", "http://127.0.0.1:11434"),
            ("COMFYUI", "http://127.0.0.1:8188"),
            ("PROJECT_LEDGER", "A_08_LOGS/PROJECT_LEDGER.txt"),
            ("OBSERVATIONS", "A_08_LOGS/OBSERVATIONS.jsonl"),
            ("PASSPORT", "A_07_CONFIG/project_passport.json"),
        ]

    def scan(self):

        objects = []

        for name, target in self.services:

            objects.append({
                "type": "SERVICE",
                "name": name,
                "target": target,
                "source": "ServicesScanner"
            })

        return objects


if __name__ == "__main__":

    scanner = ServicesScanner()

    objects = scanner.scan()

    print("=== SERVICES SCANNER TEST ===")
    print()
    print("OBJECTS :", len(objects))

    if objects:
        print("FIRST   :", objects[0]["name"])
