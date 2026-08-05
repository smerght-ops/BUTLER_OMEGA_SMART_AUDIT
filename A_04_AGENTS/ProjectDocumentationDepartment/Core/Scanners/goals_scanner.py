# -*- coding: utf-8 -*-

import json
from pathlib import Path


class GoalsScanner:
    """
    Discovers Engineering Objects from goals_registry.json
    """

    def scan(self, goals_path):
        goals_path = Path(goals_path)

        if not goals_path.exists():
            return []

        with goals_path.open("r", encoding="utf-8-sig") as f:
            data = json.load(f)

        objects = []

        for key, value in data.items():
            objects.append({
                "type": "GOAL",
                "name": key,
                "value": value,
                "source": str(goals_path),
            })

        return objects


if __name__ == "__main__":
    print("=== GOALS SCANNER READY ===")
