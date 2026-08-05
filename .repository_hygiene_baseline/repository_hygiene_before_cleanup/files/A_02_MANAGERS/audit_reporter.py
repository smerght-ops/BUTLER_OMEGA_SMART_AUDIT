import os
import sqlite3
from pathlib import Path
from datetime import datetime

DB_PATH = Path("A_05_STORAGE/catalog.db")
REPORT_DIR = Path("A_06_WORKSPACE/reports")
REPORT_DIR.mkdir(parents=True, exist_ok=True)

def generate_report():
    report = []
    report.append("=" * 60)
    report.append("BUTLER OMEGA DOCUMENT AUDIT REPORT")
    report.append(f"Generated: {datetime.now().isoformat(timespec='seconds')}")
    report.append("=" * 60)
    report.append("")

    if not DB_PATH.exists():
        report.append("❌ catalog.db не найден.")
        return "\n".join(report)

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    rows = cur.execute("""
        SELECT id, filepath, file_hash, status, summary, tags, is_legacy, registered_at, updated_at
        FROM documents
        ORDER BY id DESC
    """).fetchall()

    report.append(f"Всего документов: {len(rows)}")
    report.append("")

    for row in rows:
        doc_id, filepath, file_hash, status, summary, tags, is_legacy, registered_at, updated_at = row
        report.append("-" * 60)
        report.append(f"ID       : {doc_id}")
        report.append(f"Файл     : {os.path.basename(filepath)}")
        report.append(f"Путь     : {filepath}")
        report.append(f"Хэш      : {file_hash or '[EMPTY]'}")
        report.append(f"Статус   : {status}")
        report.append(f"Legacy   : {bool(is_legacy)}")
        report.append(f"Теги     : {tags or ''}")
        report.append(f"Summary  : {summary or ''}")
        report.append(f"Created  : {registered_at}")
        report.append(f"Updated  : {updated_at}")

    conn.close()

    return "\n".join(report)

if __name__ == "__main__":
    text = generate_report()
    out = REPORT_DIR / "DOCUMENT_AUDIT_REPORT.txt"
    out.write_text(text, encoding="utf-8")
    print(text)
    print()
    print(f"✓ Отчёт сохранён: {out}")
