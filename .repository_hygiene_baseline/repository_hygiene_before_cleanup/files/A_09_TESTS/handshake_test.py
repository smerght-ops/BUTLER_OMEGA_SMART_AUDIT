"""
=============================================================================
АРХИТЕКТУРНЫЙ ПАСПОРТ СВЯЗЕЙ МОДУЛЯ [handshake_test.py] (v1.1 Foundation)
=============================================================================
РОЛЬ: Автоматический тест комплексной проверки (рукопожатия) компонентов ядра.
ВХОДНЫЕ СВЯЗИ (Кто вызывает этот модуль):
  <- [Запуск тестов вручную или через CI/CD систему валидации]
ВЫХОДНЫЕ СВЯЗИ (К кому ведет дорога из этого модуля):
  -> [A_02_MANAGERS/provider_manager.py] (Проверка доступности Ollama)
  -> [A_02_MANAGERS/catalog_manager.py] (Проверка коннекта к SQLite)
  -> [A_02_MANAGERS/memory_manager.py] (Проверка подсистемы памяти)
=============================================================================
"""

import sys
from pathlib import Path

# Добавляем корень проекта в пути поиска модулей
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from A_02_MANAGERS.provider_manager import ProviderManager
from A_02_MANAGERS.catalog_manager import CatalogManager
from A_02_MANAGERS.memory_manager import MemoryManager

sys.stdout.reconfigure(encoding='utf-8')

def run_handshake():
    print("\n=========================================")
    print("[ТЕСТ] ЗАПУСК СКВОЗНОГО ТЕСТА РУКОПОЖАТИЯ (HANDSHAKE)")
    print("=========================================")
    
    # 1. Проверка СУБД
    print("[СВЯЗЬ -> Тест] Проверка CatalogManager...")
    try:
        catalog = CatalogManager()
        # Проверяем, что объект создается и база доступна
        if catalog.db_path.exists():
            print("✓ CatalogManager: База данных SQLite WAL обнаружена и доступна.")
        else:
            print("[-] CatalogManager: Предупреждение, файл БД будет создан при первой записи.")
    except Exception as e:
        print(f"✗ CatalogManager: Сбой инициализации: {e}")
        return False

    # 2. Проверка памяти
    print("[СВЯЗЬ -> Тест] Проверка MemoryManager...")
    try:
        mm = MemoryManager()
        print("✓ MemoryManager: Подсистема памяти успешно проинициализирована.")
    except Exception as e:
        print(f"✗ MemoryManager: Сбой инициализации: {e}")
        return False

    # 3. Проверка Ollama
    print("[СВЯЗЬ -> Тест] Проверка ProviderManager (Ollama)...")
    try:
        provider = ProviderManager()
        if provider.check_ollama_status():
            print("✓ ProviderManager: Локальный сервер Ollama отвечает на запросы.")
        else:
            print("[!] ProviderManager: Предупреждение, сервер Ollama сейчас недоступен.")
    except Exception as e:
        print(f"✗ ProviderManager: Ошибка при проверке статуса: {e}")
        return False

    print("\n=========================================")
    print("[ОК] ТЕСТ РУКОПОЖАТИЯ ЗАВЕРШЕН УСПЕШНО!")
    print("=========================================")
    return True

if __name__ == "__main__":
    success = run_handshake()
    sys.exit(0 if success else 1)
