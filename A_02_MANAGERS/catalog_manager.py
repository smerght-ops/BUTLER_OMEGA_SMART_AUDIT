import sqlite3
import os
from datetime import datetime

class CatalogManager:
    def __init__(self, db_path="../A_05_STORAGE/catalog.db"):
        # Приводим путь к базе к абсолютному, чтобы не зависеть от места запуска
        self.db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), db_path))
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''CREATE TABLE IF NOT EXISTS files 
                           (id INTEGER PRIMARY KEY, path TEXT UNIQUE, last_modified TEXT, tag TEXT)''')
            conn.commit()

    def register_file(self, path, tag="general"):
        # Проверяем существование файла перед регистрацией
        if not os.path.exists(path):
            print(f"✗ ОШИБКА: Файл не найден: {path}")
            return
            
        mod_time = datetime.fromtimestamp(os.path.getmtime(path)).isoformat()
        with sqlite3.connect(self.db_path) as conn:
            try:
                conn.execute("INSERT OR REPLACE INTO files (path, last_modified, tag) VALUES (?, ?, ?)", 
                             (path, mod_time, tag))
                conn.commit()
                print(f"✓ Зарегистрировано: {path}")
            except Exception as e:
                print(f"✗ ОШИБКА БД: {e}")

if __name__ == "__main__":
    cm = CatalogManager()
    # Регистрируем файл по правильному пути из папки A_02_MANAGERS
    cm.register_file("../A_01_CORE/Butler.py", "core")