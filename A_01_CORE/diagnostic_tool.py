import os
import sys
from pathlib import Path
from A_02_MANAGERS.catalog_manager import CatalogManager

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    RESET = '\033[0m'

class ButlerDiagnostics:
    def __init__(self):
        self.PROJECT_ROOT = Path(__file__).resolve().parent.parent
        self.catalog = CatalogManager()

    def print_check(self, title, status, details=""):
        color = Colors.GREEN if status else Colors.RED
        icon = "[✓]" if status else "[!]"
        print(f"{color}{icon}{Colors.RESET} {title}: {details}")

    def inspect_folders(self):
        print("\n--- [САМОАНАЛИЗ] ИНСПЕКЦИЯ РАБОЧИХ ЗОН (WORKSPACE) ---")
        zones = {
            "Входящие (incoming)": "A_06_WORKSPACE/incoming",
            "В обработке (processing)": "A_06_WORKSPACE/processing",
            "Готовые отчеты (reports)": "A_06_WORKSPACE/reports"
        }
        for name, rel_path in zones.items():
            full_path = self.PROJECT_ROOT / rel_path
            if full_path.exists():
                files = [f.name for f in full_path.iterdir() if not f.name.startswith('.')]
                print(f" Направление [{name}]: Найдено файлов: {len(files)} -> {files}")
            else:
                print(f" {Colors.RED}[!] Ошибка: Папка {rel_path} не существует!{Colors.RESET}")

    def test_fts5_search(self):
        print("\n--- [ТЕСТ RAG] ПРОВЕРКА СЕМАНТИЧЕСКОГО ПОЛНОТЕКСТОВОГО ПОИСКА FTS5 ---")
        test_queries = ["main", "REPORT", "py", "очередь"]
        for q in test_queries:
            try:
                results = self.catalog.full_text_search(q)
                print(f" Запрос на поиск: '{q}' -> Найдено совпадений в БД: {len(results)}")
                for row in results:
                    print(f"   [ID: {row[0]}] Файл: {row[1]} | Теги: {row[3]}")
            except Exception as e:
                print(f" {Colors.RED}[!] Ошибка поиска для '{q}': {e}{Colors.RESET}")

    def self_structure_analysis(self):
        print("\n--- [САМОАНАЛИЗ] АНАЛИЗ СОБСТВЕННОЙ АРХИТЕКТУРЫ КОРНЯ ---")
        modules = [
            "A_01_CORE/orchestrator.py", "A_01_CORE/mcp_server.py",
            "A_02_MANAGERS/catalog_manager.py", "A_02_MANAGERS/queue_manager.py",
            "A_04_AGENTS/professor.py"
        ]
        for mod in modules:
            mod_path = self.PROJECT_ROOT / mod
            if mod_path.exists():
                with open(mod_path, 'r', encoding='utf-8') as f:
                    lines = len(f.readlines())
                print(f" {Colors.GREEN}[✓]{Colors.RESET} Модуль [{mod}]: ДОСТУПЕН ({lines} строк кода)")
            else:
                print(f" {Colors.RED}[!] КРИТИЧЕСКАЯ ОШИБКА: Модуль {mod} ОТСУТСТВУЕТ!{Colors.RESET}")

    def run_all(self):
        print("=======================================================")
        print(" ЗАПУСК СИСТЕМНОГО САМОАНАЛИЗА И ДИАГНОСТИКИ BUTLER OMEGA ")
        print("=======================================================")
        self.self_structure_analysis()
        self.inspect_folders()
        self.test_fts5_search()
        print("\n=======================================================")
        print(" Диагностика завершена. ")
        print("=======================================================")

if __name__ == '__main__':
    ButlerDiagnostics().run_all()
