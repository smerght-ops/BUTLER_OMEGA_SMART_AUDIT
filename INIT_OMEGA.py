import sys
from pathlib import Path
from A_02_MANAGERS.catalog_manager import CatalogManager

def register_test_job(filename):
    cm = CatalogManager()
    # Формируем корректный относительный путь для тестового файла
    rel_path = Path('A_06_WORKSPACE') / 'incoming' / filename
    
    # Создаем пустую заглушку для теста, если файла физически нет в инкаминге
    full_path = cm.PROJECT_ROOT / rel_path
    full_path.parent.mkdir(parents=True, exist_ok=True)
    if not full_path.exists():
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write("Test background document payload.")

    try:
        if cm.register_document(rel_path, status='queued'):
            print(f'✓ [БАТЛЕР] Тестовый документ [{filename}] успешно поставлен в очередь СУБД.')
        else:
            print(f'✗ [БАТЛЕР] Не удалось зарегистрировать документ [{filename}].')
    except Exception as e:
        print(f'Registration error: {e}')

if __name__ == '__main__':
    register_test_job('test_file.txt')
