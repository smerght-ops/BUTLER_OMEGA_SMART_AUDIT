# -*- coding: utf-8 -*-

from pathlib import Path


class SnapshotScanner:
    """
    Discovers architecture snapshots.
    """

    def scan(self, snapshot_root):
        snapshot_root = Path(snapshot_root)

        if not snapshot_root.exists():
            return []

        objects = []

        for item in sorted(snapshot_root.iterdir()):
            if not item.is_dir():
                continue

            objects.append({
                "type": "SNAPSHOT",
                "name": item.name,
                "source": str(item),
            })

        return objects


if __name__ == "__main__":

    root = Path(__file__).resolve().parents[3] / "A_00_ARCHITECTURE" / "SNAPSHOTS"

    scanner = SnapshotScanner()

    print("=== SNAPSHOT SCANNER TEST ===")
    print()

    objects = scanner.scan(root)

    print("ROOT    :", root.exists())
    print("OBJECTS :", len(objects))

    if objects:
        print("FIRST   :", objects[0]["name"])
