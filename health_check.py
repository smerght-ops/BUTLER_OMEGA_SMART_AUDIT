import sqlite3
from pathlib import Path

DB_PATH = Path("A_05_STORAGE/catalog.db")

def scalar(cur, sql):
    return cur.execute(sql).fetchone()[0]

def run_health_check():
    print("=" * 50)
    print("      BUTLER OMEGA DATABASE HEALTH v2.0")
    print("=" * 50)

    if not DB_PATH.exists():
        print("❌ catalog.db не найден.")
        return

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    completed = scalar(cur, "SELECT COUNT(*) FROM documents WHERE status='completed'")
    queued = scalar(cur, "SELECT COUNT(*) FROM documents WHERE status='queued'")
    processing = scalar(cur, "SELECT COUNT(*) FROM documents WHERE status='processing'")

    modern = scalar(cur, "SELECT COUNT(*) FROM documents WHERE is_legacy=0")
    legacy = scalar(cur, "SELECT COUNT(*) FROM documents WHERE is_legacy=1")

    duplicate_hashes = scalar(cur, """
        SELECT COUNT(*)
        FROM (
            SELECT file_hash
            FROM documents
            WHERE file_hash IS NOT NULL
              AND file_hash <> ''
            GROUP BY file_hash
            HAVING COUNT(*) > 1
        )
    """)

    modern_without_hash = scalar(cur, """
        SELECT COUNT(*)
        FROM documents
        WHERE is_legacy=0
          AND status='completed'
          AND (file_hash IS NULL OR file_hash='')
    """)

    print()
    print("=== DOCUMENT STATUS ===")
    print(f"Completed : {completed}")
    print(f"Queued    : {queued}")
    print(f"Processing: {processing}")

    print()
    print("=== DATASET ===")
    print(f"Modern documents : {modern}")
    print(f"Legacy documents : {legacy}")

    print()
    print("=== INTEGRITY ===")
    print(f"Duplicate hashes            : {duplicate_hashes}")
    print(f"Modern completed w/o hash   : {modern_without_hash}")

    if legacy:
        print()
        print("=== LEGACY ARCHIVE ===")
        rows = cur.execute("""
            SELECT id, filepath
            FROM documents
            WHERE is_legacy=1
            ORDER BY id
        """).fetchall()

        for doc_id, path in rows:
            print(f"LEGACY #{doc_id}: {path}")

    print()
    print("=" * 50)

    if duplicate_hashes == 0 and modern_without_hash == 0:
        print("✓ HEALTH STATUS: EXCELLENT")
    else:
        print("❌ HEALTH STATUS: ATTENTION REQUIRED")

    print("=" * 50)

    conn.close()

if __name__ == "__main__":
    run_health_check()