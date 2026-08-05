# -*- coding: utf-8 -*-

import json
from pathlib import Path


class RegistryValidator:

    def __init__(self):
        self.registry_path = (
            Path(__file__).resolve().parent /
            "project_registry.json"
        )

    def load_registry(self):
        with open(
            self.registry_path,
            "r",
            encoding="utf-8-sig"
        ) as f:
            return json.load(f)

    def validate(self):
        try:
            registry = self.load_registry()

            modules = registry.get("modules", [])
            departments = registry.get("departments", [])
            services = registry.get("services", [])

            print("[OK] Registry loaded")
            print("[OK] JSON valid")
            print(f"[OK] Modules: {len(modules)}")
            print(f"[OK] Departments: {len(departments)}")
            print(f"[OK] Services: {len(services)}")
            print()
            print("Registry VALID")

            return True

        except Exception as e:
            print(f"[REGISTRY ERROR] {e}")
            return False


if __name__ == "__main__":
    RegistryValidator().validate()
