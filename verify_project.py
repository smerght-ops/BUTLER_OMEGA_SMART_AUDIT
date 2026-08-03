# -*- coding: utf-8 -*-
import json
import py_compile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
LOG_DIR = ROOT / "A_08_LOGS"
LOG_DIR.mkdir(parents=True, exist_ok=True)

REPORT_JSON = LOG_DIR / "verification_report.json"
REPORT_TXT = LOG_DIR / "verification_report.txt"

IGNORE_DIRS = {
    ".git",
    "__pycache__",
    "A_00_HISTORY",
    "A_08_LOGS",
}

def is_ignored(path: Path) -> bool:
    parts = set(path.relative_to(ROOT).parts)
    return bool(parts & IGNORE_DIRS)

def check_bom(path: Path):
    with path.open("rb") as f:
        return f.read(3) == b"\xef\xbb\xbf"

def main():
    started = time.time()
    py_files = []
    errors = []

    for path in ROOT.rglob("*.py"):
        if is_ignored(path):
            continue
        py_files.append(path)

    print("")
    print("=" * 60)
    print("РџР РћР’Р•Р РљРђ РџР РћР•РљРўРђ BUTLER_OMEGA_SMART")
    print("=" * 60)

    for path in sorted(py_files):
        rel = str(path.relative_to(ROOT))

        try:
            if check_bom(path):
                raise RuntimeError("РќР°Р№РґРµРЅ BOM РІ РЅР°С‡Р°Р»Рµ С„Р°Р№Р»Р°")

            py_compile.compile(str(path), doraise=True)
            print("[OK]", rel)

        except Exception as e:
            msg = str(e)
            errors.append({
                "file": rel,
                "error": msg
            })
            print("[РћРЁРР‘РљРђ]", rel)
            print("  ", msg)

    status = "SUCCESS" if not errors else "FAILED"
    elapsed = round(time.time() - started, 3)

    report = {
        "time": time.strftime("%Y-%m-%d %H:%M:%S"),
        "status": status,
        "checked_files": len(py_files),
        "errors_count": len(errors),
        "errors": errors,
        "elapsed_seconds": elapsed
    }

    REPORT_JSON.write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    lines = []
    lines.append("РџР РћР’Р•Р РљРђ РџР РћР•РљРўРђ BUTLER_OMEGA_SMART")
    lines.append("РЎРўРђРўРЈРЎ: " + status)
    lines.append("РџР РћР’Р•Р Р•РќРћ Р¤РђР™Р›РћР’: " + str(len(py_files)))
    lines.append("РћРЁРР‘РћРљ: " + str(len(errors)))
    lines.append("Р’Р Р•РњРЇ: " + str(elapsed) + " СЃРµРє.")
    lines.append("")
    for err in errors:
        lines.append("РћРЁРР‘РљРђ: " + err["file"])
        lines.append(err["error"])
        lines.append("")

    REPORT_TXT.write_text("\n".join(lines), encoding="utf-8")

    print("=" * 60)
    print("РРўРћР“:", status)
    print("РџСЂРѕРІРµСЂРµРЅРѕ С„Р°Р№Р»РѕРІ:", len(py_files))
    print("РћС€РёР±РѕРє:", len(errors))
    print("РћС‚С‡РµС‚:", REPORT_JSON)
    print("=" * 60)

    return 0 if not errors else 1

if __name__ == "__main__":
    raise SystemExit(main())
