# -*- coding: utf-8 -*-

import json
from pathlib import Path


class PassportScanner:
    """
    Discovers Engineering Objects from project_passport.json
    """

    def scan(self, passport_path):
        passport_path = Path(passport_path)

        if not passport_path.exists():
            return []

        with passport_path.open("r", encoding="utf-8-sig") as f:
            data = json.load(f)

        objects = []

        for key, value in data.items():
            objects.append({
                "type": "PASSPORT_FIELD",
                "name": key,
                "value": value,
                "source": str(passport_path),
            })

        return objects


if __name__ == "__main__":
    print("=== PASSPORT SCANNER READY ===")

