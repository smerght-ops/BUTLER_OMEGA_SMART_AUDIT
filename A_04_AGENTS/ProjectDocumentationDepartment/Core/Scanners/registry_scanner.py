# -*- coding: utf-8 -*-

import json
from pathlib import Path


class RegistryScanner:
    """
    Discovers Engineering Objects from JSON registries.
    """

    def scan(self, registry_path):
        registry_path = Path(registry_path)

        if not registry_path.exists():
            return []

        with registry_path.open("r", encoding="utf-8-sig") as f:
            data = json.load(f)

        objects = []

        if isinstance(data, dict):
            iterable = data.items()
        else:
            iterable = enumerate(data)

        for key, value in iterable:
            objects.append({
                "type": "REGISTRY_ENTRY",
                "name": str(key),
                "value": value,
                "source": str(registry_path),
            })

        return objects


if __name__ == "__main__":
    print("=== REGISTRY SCANNER READY ===")
