# -*- coding: utf-8 -*-

import json
from pathlib import Path


class ExecutionScanner:
    """
    Discovers Engineering Objects from execution registry.
    """

    def scan(self, execution_path):
        execution_path = Path(execution_path)

        if not execution_path.exists():
            return []

        with execution_path.open("r", encoding="utf-8-sig") as f:
            data = json.load(f)

        objects = []

        for key, value in data.items():
            objects.append({
                "type": "EXECUTION",
                "name": key,
                "value": value,
                "source": str(execution_path),
            })

        return objects


if __name__ == "__main__":
    print("=== EXECUTION SCANNER READY ===")
