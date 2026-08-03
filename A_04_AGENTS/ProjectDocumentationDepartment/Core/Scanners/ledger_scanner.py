# -*- coding: utf-8 -*-

from pathlib import Path


class LedgerScanner:
    """
    Discovers Engineering Objects directly from PROJECT_LEDGER.txt.
    """

    def scan(self, ledger_path):
        ledger_path = Path(ledger_path)

        if not ledger_path.exists():
            return []

        objects = []

        for line in ledger_path.read_text(encoding="utf-8-sig").splitlines():
            line = line.strip()

            if not line or not line.startswith("["):
                continue

            tag = line.split("]", 1)[0][1:]

            objects.append({
                "type": "LEDGER",
                "name": tag,
                "record": line,
                "source": str(ledger_path),
            })

        return objects


if __name__ == "__main__":
    scanner = LedgerScanner()

    ledger = Path(__file__).resolve().parents[3] / "A_08_LOGS" / "PROJECT_LEDGER.txt"

    print("=== LEDGER SCANNER TEST ===")
    print()

    objects = scanner.scan(ledger)

    print("LEDGER :", ledger.exists())
    print("OBJECTS:", len(objects))

    if objects:
        print("FIRST  :", objects[0]["name"])
