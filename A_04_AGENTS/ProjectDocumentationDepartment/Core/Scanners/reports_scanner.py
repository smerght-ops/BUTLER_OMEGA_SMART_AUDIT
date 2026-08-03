# -*- coding: utf-8 -*-

from pathlib import Path


class ReportsScanner:
    """
    Discovers Engineering Objects from project reports.
    """

    def scan(self, reports_dir):
        reports_dir = Path(reports_dir)

        if not reports_dir.exists():
            return []

        objects = []

        for report in sorted(reports_dir.glob("*")):
            if not report.is_file():
                continue

            objects.append({
                "type": "REPORT",
                "name": report.name,
                "size": report.stat().st_size,
                "source": str(report),
            })

        return objects


if __name__ == "__main__":
    scanner = ReportsScanner()

    reports = Path(__file__).resolve().parents[3] / "A_06_WORKSPACE" / "reports"

    print("=== REPORTS SCANNER TEST ===")
    print()

    objects = scanner.scan(reports)

    print("REPORTS :", reports.exists())
    print("OBJECTS :", len(objects))

    if objects:
        print("FIRST   :", objects[0]["name"])
