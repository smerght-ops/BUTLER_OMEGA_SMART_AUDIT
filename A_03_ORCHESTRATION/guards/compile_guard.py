# -*- coding: utf-8 -*-

import json
import py_compile
from pathlib import Path


class CompileGuard:

    def __init__(self):
        # Абсолютный корень проекта (2 уровня вверх от папки guards)
        self.project_root = Path(__file__).resolve().parents[2]

    def validate(self, cr_path: Path) -> dict:
        cr_path = Path(cr_path)
        if not cr_path.is_absolute():
            cr_path = (self.project_root / cr_path).resolve()

        if not cr_path.exists():
            return {"status": "REJECTED", "code": "404_CR_NOT_FOUND"}

        try:
            with open(cr_path, "r", encoding="utf-8") as f:
                cr_data = json.load(f)
        except Exception as e:
            return {"status": "REJECTED", "code": "400_INVALID_JSON", "reason": str(e)}

        if not cr_data.get("compile_required", False):
            return {"status": "APPROVED", "code": "200_COMPILE_BYPASS", "reason": "Проверка синтаксиса не требуется."}

        target_files = cr_data.get("target_files", [])

        for file_path_str in target_files:
            target_file = self.project_root / file_path_str

            # Если файл не существует physically на диске (например фаза ДО создания)
            if not target_file.exists():
                continue

            # Фильтр расширений: проверяем только Python-код
            if target_file.suffix.lower() != ".py":
                continue

            try:
                # Встроенная безопасная компиляция без вызова подпроцессов OS
                py_compile.compile(str(target_file), doraise=True)
            except py_compile.PyCompileError as compile_err:
                # Фиксируем синтаксический брак
                return {
                    "status": "REJECTED",
                    "code": "422_SYNTAX_ERROR",
                    "reason": f"Обнаружена синтаксическая ошибка в файле {target_file.name}: {compile_err.msg.strip()}"
                }
            except Exception as e:
                return {
                    "status": "REJECTED",
                    "code": "500_COMPILE_EXCEPTION",
                    "reason": f"Системный сбой при компиляции {target_file.name}: {str(e)}"
                }

        return {
            "status": "APPROVED",
            "code": "200_GUARD_OK",
            "reason": "Все измененные Python-модули успешно прошли синтаксический контроль."
        }


if __name__ == "__main__":
    guard = CompileGuard()
    print("=== RUNTIME COMPONENT TEST: COMPILE_GUARD V1 ===")

    # Тест 1: Валидация легитимного стабильного файла проекта
    real_cr = Path("A_00_ARCHITECTURE/CHANGE_REQUESTS/CR_000_TEST.json")
    print(f"\n[Тест 1] Проверка легитимного Python-кода через {real_cr.name}:")
    print(json.dumps(guard.validate(real_cr), indent=2, ensure_ascii=False))

    # Тест 2: Эмуляция синтаксического брака (Ожидаем REJECTED / 422_SYNTAX_ERROR)
    broken_py = guard.project_root / "A_03_ORCHESTRATION" / "temporary_broken_module.py"
    broken_py.write_text("def unclosed_function_def(:\n    print('broken'", encoding="utf-8")

    attack_cr_path = guard.project_root / "A_00_ARCHITECTURE" / "CHANGE_REQUESTS" / "CR_SYNTAX_ATTACK.json"
    attack_data = {
        "id": "CR_SYNTAX_ATTACK",
        "target_files": ["A_03_ORCHESTRATION/temporary_broken_module.py"],
        "compile_required": True
    }
    with open(attack_cr_path, "w", encoding="utf-8") as f:
        json.dump(attack_data, f, indent=2)

    print(f"\n[Тест 2] Проверка заявки с синтаксическим браком:")
    print(json.dumps(guard.validate(attack_cr_path), indent=2, ensure_ascii=False))

    # Очистка мусора после тестов
    for tmp_file in [broken_py, attack_cr_path]:
        if tmp_file.exists():
            tmp_file.unlink()
    print("\n[OK] Тестирование компонента завершено.")
