# -*- coding: utf-8 -*-

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from A_03_ORCHESTRATION.butler_harness import ButlerHarness


class HarnessScanner:
    """
    Discovery adapter over the official ButlerHarness.
    """

    def scan(self):
        harness = ButlerHarness()

        return [{
            "type": "HARNESS",
            "name": harness.__class__.__name__,
            "module": "A_03_ORCHESTRATION.butler_harness",
            "source": "A_03_ORCHESTRATION/butler_harness.py",
        }]


if __name__ == "__main__":

    scanner = HarnessScanner()

    print("=== HARNESS SCANNER TEST ===")
    print()

    objects = scanner.scan()

    print("OBJECTS :", len(objects))

    if objects:
        print("FIRST   :", objects[0]["name"])
