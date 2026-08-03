import sqlite3, os

db_path = "A_05_STORAGE/catalog.db"

def show_catalog():
    if not os.path.exists(db_path):
        print(f"[!] ОШИБКА: База данных не найдена по пути: {db_path}")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT filepath, status, summary, tags
    FROM documents
    ORDER BY id DESC
    """)

    rows = cursor.fetchall()

    print(f"\n--- ОТЧЕТ ПО DOCUMENTS ({len(rows)} записей) ---")

    for row in rows:
        print(f"\nФАЙЛ: {os.path.basename(row[0])}")
        print(f"СТАТУС: {row[1]}")
        print(f"SUMMARY: {row[2]}")
        print(f"ТЕГИ: {row[3]}")
        print("-" * 40)

    conn.close()

if __name__ == "__main__":
    show_catalog()