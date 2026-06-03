import os
import sqlite3
import sys
from datetime import datetime

# Установка кодировки для корректного отображения в терминале
sys.stdout.reconfigure(encoding='utf-8')

# Абсолютный путь к корню проекта (папка BUTLER_OMEGA)
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Абсолютный путь к файлу отчета
REPORT_FILE = os.path.join(os.path.dirname(__file__), "../A_08_LOGS/project_report.txt")

# Путь к базе данных
DB_PATH = os.path.join(os.path.dirname(__file__), "../A_05_STORAGE/catalog.db")

def get_tree(path, indent=""):
    tree = ""
    try:
        items = sorted(os.listdir(path))
        for item in items:
            if item in ['A_08_LOGS', 'A_05_STORAGE']: continue
            full_path = os.path.join(path, item)
            if os.path.isdir(full_path):
                tree += f"{indent}[DIR] {item}\n"
                tree += get_tree(full_path, indent + "  |-- ")
            else:
                size = os.path.getsize(full_path) / 1024
                tree += f"{indent}{item} ({size:.1f} KB)\n"
    except Exception as e:
        tree += f"{indent}Ошибка доступа: {e}\n"
    return tree

def generate_report():
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # 1. Структура и дерево
    report = f"ОТЧЕТ АУДИТА СИСТЕМЫ\nДата: {timestamp}\n\n--- СТРУКТУРА ---\n{get_tree(ROOT)}"
    
    # 2. Зарегистрированные файлы из базы
    report += "\n--- ЗАРЕГИСТРИРОВАННЫЕ ФАЙЛЫ (DB) ---\n"
    if os.path.exists(DB_PATH):
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.execute("SELECT path, tag FROM files")
            for row in cursor.fetchall():
                report += f"Файл: {row[0]} | Тег: {row[1]}\n"
    else:
        report += "База данных не найдена.\n"
    
    # 3. Код
    report += "\n--- ВЫТЯЖКА КОДА ---\n"
    for root, _, files in os.walk(ROOT):
        for file in files:
            if file.endswith(".py"):
                path = os.path.join(root, file)
                report += f"\n[FILE: {path}]\n"
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        report += f.read() + "\n"
                except Exception as e:
                    report += f"Ошибка чтения файла: {e}\n"
    
    with open(REPORT_FILE, 'w', encoding='utf-8') as f:
        f.write(report)
    print(f"✓ Отчет создан: {REPORT_FILE}")

if __name__ == "__main__":
    generate_report()