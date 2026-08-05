# -*- coding: utf-8 -*-

from pathlib import Path


class RollbackScanner:
    """
    Discovers rollback points.
    """

    def scan(self, rollback_root):
        rollback_root = Path(rollback_root)

        if not rollback_root.exists():
            return []

        objects = []

        for item in sorted(rollback_root.iterdir()):
            if not item.is_dir():
                continue

            objects.append({
                "type": "ROLLBACK",
                "name": item.name,
                "source": str(item),
            })

        return objects


if __name__ == "__main__":

    root = Path(__file__).resolve().parents[3] / "A_00_HISTORY" / "ROLLBACK_POINTS"

    scanner = RollbackScanner()

    print("=== ROLLBACK SCANNER TEST ===")
    print()

    objects = scanner.scan(root)

    print("ROOT    :", root.exists())
    print("OBJECTS :", len(objects))

    if objects:
        print("FIRST   :", objects[0]["name"])
