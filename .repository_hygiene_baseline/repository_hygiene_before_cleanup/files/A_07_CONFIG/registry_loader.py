# -*- coding: utf-8 -*-

import json
from pathlib import Path


class RegistryLoader:

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

    def get_modules(self):
        return self.load_registry().get("modules", [])

    def get_departments(self):
        return self.load_registry().get("departments", [])

    def get_services(self):
        return self.load_registry().get("services", [])


if __name__ == "__main__":
    loader = RegistryLoader()

    print(loader.get_modules())
