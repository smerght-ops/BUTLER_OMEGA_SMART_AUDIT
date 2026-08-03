# -*- coding: utf-8 -*-

import json
from pathlib import Path


class ProjectStateScanner:
    """
    Discovers Engineering Objects from project_state.json
    """

    def scan(self, state_path):
        state_path = Path(state_path)

        if not state_path.exists():
            return []

        with state_path.open("r", encoding="utf-8-sig") as f:
            data = json.load(f)

        objects = []

        for key, value in data.items():
            objects.append({
                "type": "PROJECT_STATE",
                "name": key,
                "value": value,
                "source": str(state_path),
            })

        return objects


if __name__ == "__main__":
    print("=== PROJECT STATE SCANNER READY ===")
