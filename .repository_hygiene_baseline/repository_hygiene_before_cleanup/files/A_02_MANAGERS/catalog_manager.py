import sqlite3
from pathlib import Path
import re

class CatalogManager:
    def __init__(self):
        self.db_path = Path(__file__).resolve().parent.parent / "A_05_STORAGE/catalog.db"

    def register_document(self, filepath, file_bytes, summary, tags, file_hash, status="completed"):
        import time

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        now = int(time.time())

        status_weight = {
            "queued": 1,
            "processing": 2,
            "completed": 3,
            "failed": 3,
        }

        new_weight = status_weight.get(status, 0)

        # -------------------------------------------------
        # 1. Проверка по MD5
        # -------------------------------------------------
        if file_hash:
            cursor.execute("""
                SELECT id, status, filepath
                FROM documents
                WHERE file_hash = ?
                LIMIT 1
            """, (file_hash,))

            row = cursor.fetchone()

            if row:
                doc_id, old_status, old_path = row
                old_weight = status_weight.get(old_status, 0)

                cursor.execute("""
                    UPDATE documents
                    SET
                        status = CASE
                            WHEN ? >= ? THEN ?
                            ELSE status
                        END,
                        filepath = ?,
                        summary = CASE
                            WHEN ? <> '' THEN ?
                            ELSE summary
                        END,
                        tags = CASE
                            WHEN ? <> '' THEN ?
                            ELSE tags
                        END,
                        updated_at = ?
                    WHERE id = ?
                """, (new_weight, old_weight, status, str(filepath), summary, summary, tags, tags, now, doc_id))

                conn.commit()
                conn.close()
                print(f"    ✓ MD5 MATCH -> обновлена запись #{doc_id}")
                return doc_id

        # -------------------------------------------------
        # 2. Проверка по filepath
        # -------------------------------------------------
        cursor.execute("""
            SELECT id, status
            FROM documents
            WHERE filepath = ?
            LIMIT 1
        """, (str(filepath),))

        row = cursor.fetchone()

        if row:
            doc_id, old_status = row
            old_weight = status_weight.get(old_status, 0)

            cursor.execute("""
                UPDATE documents
                SET
                    status = CASE
                        WHEN ? >= ? THEN ?
                        ELSE status
                    END,
                    summary = CASE
                        WHEN ? <> '' THEN ?
                        ELSE summary
                    END,
                    tags = CASE
                        WHEN ? <> '' THEN ?
                        ELSE tags
                    END,
                    file_hash = CASE
                        WHEN ? <> '' THEN ?
                        ELSE file_hash
                    END,
                    updated_at = ?
                WHERE id = ?
            """, (new_weight, old_weight, status, summary, summary, tags, tags, file_hash, file_hash, now, doc_id))

            conn.commit()
            conn.close()
            print(f"    ✓ PATH MATCH -> обновлена запись #{doc_id}")
            return doc_id

        # -------------------------------------------------
        # 3. Новый документ
        # -------------------------------------------------
        cursor.execute("""
            INSERT INTO documents
            (filepath, file_hash, status, summary, tags, registered_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (str(filepath), file_hash, status, summary, tags, now, now))

        doc_id = cursor.lastrowid
        conn.commit()
        conn.close()
        print(f"    ✓ NEW DOCUMENT -> создана запись #{doc_id}")
        return doc_id

    def full_text_search(self, query):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            orig = (query or "").strip().lower()
            terms = [orig]

            if len(orig) > 3:
                base = re.sub(r"(ами|ями|ах|ях|ов|ев|ом|ем|ой|ей|ами|ями|ами|ами|а|я|ы|и|у|ю|е)$", "", orig)
                if len(base) >= 3 and base not in terms:
                    terms.append(base)

            rows = []
            seen = set()

            for term in terms:
                like = "%" + term + "%"
                cursor.execute(
                    """
                    SELECT id, filepath, summary, tags
                    FROM documents
                    WHERE lower(summary) LIKE ?
                       OR lower(tags) LIKE ?
                       OR lower(filepath) LIKE ?
                    """,
                    (like, like, like)
                )
                for row in cursor.fetchall():
                    if row[0] not in seen:
                        seen.add(row[0])
                        rows.append(row)

            conn.close()
            return rows

        except Exception:
            return []
