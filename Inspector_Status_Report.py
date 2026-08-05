#!/usr/bin/env python3
"""
Unified Inspector Status Report v1.0
READ ONLY.
Только отображение фактов проекта.
"""

import json
from pathlib import Path

INPUT = "UnifiedInspectorFacts.json"

def main():
    path = Path(INPUT)

    if not path.exists():
        print("ERROR: FACTS FILE NOT FOUND")
        return

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    stats = data["metadata"]["statistics"]

    print("=" * 60)
    print("BUTLER UNIFIED INSPECTOR STATUS")
    print("=" * 60)

    print(f"FILES          : {stats.get('total_files',0)}")
    print(f"ERRORS         : {stats.get('total_errors',0)}")
    print()

    print(f"CLASSES        : {stats.get('total_classes',0)}")
    print(f"FUNCTIONS      : {stats.get('total_functions',0)}")
    print(f"VARIABLES      : {stats.get('total_variables',0)}")
    print()

    print(f"IMPORTS        : {stats.get('total_imports',0)}")
    print(f"REGISTRATIONS  : {stats.get('total_registrations',0)}")
    print(f"CALLS          : {stats.get('total_calls',0)}")

    print("=" * 60)

if __name__ == "__main__":
    main()
