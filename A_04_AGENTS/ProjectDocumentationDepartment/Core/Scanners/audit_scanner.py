# -*- coding: utf-8 -*-

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from A_02_MANAGERS.audit_reporter import generate_report


class AuditScanner:
    """
    Discovery adapter over audit_reporter.
    Converts audit report into Engineering Objects.
    """

    def scan(self):
        report = generate_report()

        return [{
            "type": "AUDIT",
            "name": "DOCUMENT_AUDIT_REPORT",
            "source": "A_02_MANAGERS.audit_reporter",
            "payload": report,
        }]


if __name__ == "__main__":
    scanner = AuditScanner()

    print("=== AUDIT SCANNER TEST ===")
    print()

    objects = scanner.scan()

    print("OBJECTS :", len(objects))

    if objects:
        print("FIRST   :", objects[0]["name"])
