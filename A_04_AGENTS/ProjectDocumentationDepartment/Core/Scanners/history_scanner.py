# -*- coding: utf-8 -*-

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from A_07_MEMORY.project_history import ProjectHistory


class HistoryScanner:
    """
    Discovery adapter over ProjectHistory.
    Converts validated history records into Engineering Objects.
    """

    def __init__(self):
        self.history = ProjectHistory()

    def scan(self):
        objects = []

        for record in self.history.get_closed_milestones():
            objects.append({
                "type": "HISTORY",
                "name": record["tag"],
                "status": record["status"],
                "stage": record["stage"],
                "date": record["date"],
                "source": "A_08_LOGS/PROJECT_LEDGER.txt",
                "payload": record,
            })

        return objects


if __name__ == "__main__":
    scanner = HistoryScanner()
    print("=== HISTORY SCANNER TEST ===")
    print()
    objects = scanner.scan()
    print("OBJECTS :", len(objects))
    if objects:
        print("FIRST   :", objects[0]["name"])
