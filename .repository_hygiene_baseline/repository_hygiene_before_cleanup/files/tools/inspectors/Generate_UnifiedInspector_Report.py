#!/usr/bin/env python3
"""
Generate Unified Inspector Markdown Report
READ ONLY
"""

import json
from pathlib import Path
from datetime import datetime

INPUT = "UnifiedInspectorFacts.json"
OUTPUT = "BUTLER_PROJECT_INSPECTOR_REPORT.md"


def main():

    with open(INPUT, "r", encoding="utf-8") as f:
        data = json.load(f)

    stats = data["metadata"]["statistics"]
    payload = data["payload"]

    with open(OUTPUT, "w", encoding="utf-8") as f:

        f.write("# BUTLER PROJECT INSPECTOR REPORT\n\n")
        f.write(f"Generated: {datetime.now()}\n\n")

        f.write("## PROJECT STATISTICS\n\n")

        for k, v in stats.items():
            f.write(f"- {k}: {v}\n")

        f.write("\n## FILE MAP\n\n")

        for item in payload:
            f.write(f"### {item['id']}\n\n")

            f.write(f"Classes: {len(item.get('classes', []))}\n\n")
            f.write(f"Functions: {len(item.get('functions', []))}\n\n")
            f.write(f"Variables: {len(item.get('variables', []))}\n\n")
            f.write(f"Imports: {len(item.get('imports', []))}\n\n")
            f.write(f"Registrations: {len(item.get('registrations', []))}\n\n")
            f.write(f"Calls: {len(item.get('calls', []))}\n\n")

    print("REPORT CREATED")
    print(OUTPUT)


if __name__ == "__main__":
    main()
