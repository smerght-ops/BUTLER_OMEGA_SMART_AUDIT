import re
import sqlite3
import json
from pathlib import Path
from A_01_CORE.config_loader import config

class ToolBridge:
    def __init__(self, db_path=None):
        self.db_path = Path(db_path or config['paths']['db'])

    def extract_tags(self, task_description):
        words = re.findall(r'\b\w+\b', task_description)
        return [w for w in words if len(w) > 3]

    def find_documents(self, tags):
        if not tags:
            return []
        query = "SELECT filepath FROM documents WHERE " + " OR ".join(["tags LIKE ?" for _ in tags])
        params = [f"%{tag}%" for tag in tags]
        try:
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()
            cursor.execute(query, params)
            results = cursor.fetchall()
            return [row[0] for row in results]
        except sqlite3.Error as e:
            print(f"Ошибка БД: {e}")
            return []
        finally:
            conn.close()

    def get_file_paths(self, task_description):
        tags = self.extract_tags(task_description)
        file_paths = self.find_documents(tags)
        return json.dumps(file_paths, ensure_ascii=False)
