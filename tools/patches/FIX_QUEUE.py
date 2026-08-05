import os
import sqlite3
from pathlib import Path
from A_02_MANAGERS.catalog_manager import CatalogManager

def reset_and_register():
    cm = CatalogManager()
    project_root = cm.PROJECT_ROOT
    folder = project_root / 'A_06_WORKSPACE' / 'incoming'

    if not folder.exists():
        print(f"[-] Каталог входящих не найден: {folder}")
        return

    # Сканируем поддерживаемые типы
    files = [f for f in os.listdir(folder) if f.lower().endswith(('.pdf', '.jpg', '.jpeg', '.png', '.txt', '.csv', '.xlsx', '.docx', '.html', '.json', '.webp'))]

    # Очищаем таблицу через оптимизированное соединение нового CatalogManager
    conn = cm._get_connection()
    try:
        conn.execute('DELETE FROM documents')
        conn.commit()
    except Exception as e:
        print(f"[-] Ошибка очистки СУБД: {e}")
    finally:
        conn.close()

    # Регистрируем файлы через относительные пути конвейера
    success_count = 0
    for f in files:
        rel_path = Path('A_06_WORKSPACE') / 'incoming' / f
        if cm.register_document(rel_path, status='queued'):
            success_count += 1

    print(f'[БАТЛЕР] Система синхронизирована. Файлов найдено в Workspace: {len(files)}, успешно в СУБД: {success_count}')

if __name__ == '__main__':
    reset_and_register()
