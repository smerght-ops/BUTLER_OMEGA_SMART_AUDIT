#!/usr/bin/env python3
"""
Unified Inspector Acceptance Test v1.0
READ ONLY.
Проверяет готовность UnifiedInspectorFacts.json.
"""

import json
from pathlib import Path

FACTS = "UnifiedInspectorFacts.json"

REQUIRED_FIELDS = {
    "id",
    "classes",
    "functions",
    "variables",
    "imports",
    "registrations",
    "calls",
}


def main():

    print("=" * 60)
    print("UNIFIED INSPECTOR ACCEPTANCE TEST")
    print("=" * 60)

    path = Path(FACTS)

    if not path.exists():
        print("FAIL: FACTS FILE NOT FOUND")
        return

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    metadata = data.get("metadata")
    payload = data.get("payload")

    if not metadata:
        print("FAIL: metadata missing")
        return

    if not payload:
        print("FAIL: payload missing")
        return

    stats = metadata.get("statistics", {})

    if stats.get("total_errors", 0) != 0:
        print("FAIL: errors detected")
        return

    missing = REQUIRED_FIELDS - set(payload[0].keys())

    if missing:
        print("FAIL: missing fields:", missing)
        return

    print()
    print("FILES :", stats.get("total_files"))
    print("ERRORS:", stats.get("total_errors"))
    print()

    print("FIELDS: OK")
    print("JSON  : OK")
    print("FACTS : OK")
    print()

    print("UNIFIED INSPECTOR v1.0 ACCEPTED")

    print("=" * 60)


if __name__ == "__main__":
    main()
