from A_02_MANAGERS.catalog_manager import CatalogManager
from pathlib import Path

def test_catalog_update():
    cm = CatalogManager()
    # Создадим фиктивный файл для теста, если его нет
    test_file = Path("test_doc.txt")
    test_file.profile_manager.set_fact("Это тестовый документ для проверки БД.")
    
    # Пытаемся записать с новыми полями
    success = cm.register_document(
        relative_path="test_doc.txt", 
        summary="Тестовое резюме", 
        tags="тест, база, проверка"
    )
    
    if success:
        print("✓ Успех: Данные с Summary и Tags записаны в БД.")
    else:
        print("✗ Ошибка: Запись не удалась.")

if __name__ == "__main__":
    test_catalog_update()