import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

# Импортируем синглтон-мост, на котором сидит ОС
from A_03_ORCHESTRATION.dispatcher_bridge_v2 import _dispatcher
from A_04_AGENTS.ImageDepartment.runner import ImageDepartment

print("[*] Тест: Перехватываю управление Диспетчера...")
# Инициализируем отдел напрямую
img_dept = ImageDepartment()

# Эмулируем прямой сквозной проход от SmartDispatcherV2 до execute, минуя ButlerHarness
print("[*] Тест: Имитирую прохождение BUTLER_OS -> SmartDispatcherV2 -> ImageDepartment...")
query = "нарисуй синего кита"

if img_dept.can_handle(query):
    print("[✓] can_handle() отработал успешно! Запрос распознан как IMAGE.")
    print("[*] Запуск execute() напрямую без Harness...")
    result = img_dept.execute(query)

    print("\n" + "=" * 70)
    print("DISPATCH RESULT БЕЗ HARNESS:")
    import json
    print(json.dumps(result, indent=2, ensure_ascii=False))
    print("=" * 70 + "\n")
else:
    print("[-] Ошибка: can_handle() отклонил запрос!")
