# -*- coding: utf-8 -*-

import json
import subprocess
from pathlib import Path


class IntegrationTestGuard:

    def __init__(self):
        # Намертво фиксируем абсолютный корень проекта (2 уровня вверх от папки guards)
        self.project_root = Path(__file__).resolve().parents[2]

    def _convert_to_module_notation(self, test_path: Path) -> str:
        """
        Превращает физический путь к файлу в нотацию модуля Python.
        Пример: A_03_ORCHESTRATION/test_passport_adapter.py -> A_03_ORCHESTRATION.test_passport_adapter
        """
        try:
            rel_path = test_path.relative_to(self.project_root)
            module_parts = list(rel_path.parts)
            # Отрезаем расширение .py у последнего элемента
            if module_parts[-1].endswith(".py"):
                module_parts[-1] = module_parts[-1][:-3]
            return ".".join(module_parts)
        except Exception:
            # Резервный вариант, если путь не относительный к корню
            return test_path.stem

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

        if not cr_data.get("test_required", False):
            return {"status": "APPROVED", "code": "200_TEST_BYPASS", "reason": "Интеграционное тестирование не требуется."}

        target_files = cr_data.get("target_files", [])
        
        default_test = self.project_root / "A_03_ORCHESTRATION" / "test_passport_adapter.py"
        test_to_run = default_test

        for file_path_str in target_files:
            target_file = self.project_root / file_path_str
            stem_name = target_file.stem
            
            possible_tests = [
                self.project_root / "A_03_ORCHESTRATION" / f"test_{stem_name}.py",
                self.project_root / "A_03_ORCHESTRATION" / f"{stem_name}_test.py",
                self.project_root / "A_09_TESTS" / f"test_{stem_name}.py"
            ]
            
            for p_test in possible_tests:
                if p_test.exists():
                    test_to_run = p_test
                    break

        if not test_to_run.exists():
            return {
                "status": "REJECTED",
                "code": "424_TEST_NOT_FOUND",
                "reason": f"Не найден ни один тестовый сценарий для верификации."
            }

        # Шаг V1.1: Перевод пути в формат python -m модульной нотации
        module_name = self._convert_to_module_notation(test_to_run)

        try:
            # Безопасный запуск в режиме модуля от корня проекта
            result = subprocess.run(
                ["python", "-m", module_name],
                capture_output=True,
                text=True,
                cwd=str(self.project_root),
                timeout=30
            )

            if result.returncode != 0:
                return {
                    "status": "REJECTED",
                    "code": "424_INTEGRATION_TEST_FAILED",
                    "reason": f"Тестовый модуль {module_name} завершился со сбоем (Код: {result.returncode}).",
                    "stderr": result.stderr.strip()
                }

        except subprocess.TimeoutExpired:
            return {"status": "REJECTED", "code": "408_TEST_TIMEOUT", "reason": f"Превышен таймаут модуля {module_name}."}
        except Exception as e:
            return {"status": "REJECTED", "code": "500_TEST_EXCEPTION", "reason": str(e)}

        return {
            "status": "APPROVED",
            "code": "200_GUARD_OK",
            "reason": f"Интеграционный тест модуля {module_name} успешно пройден (Контур стабилен)."
        }


if __name__ == "__main__":
    guard = IntegrationTestGuard()
    print("=== RUNTIME COMPONENT TEST: INTEGRATION_TEST_GUARD V1.1 (MODULE MODE) ===")

    # Тест 1: Валидация легитимного существующего CR_000_TEST.json (Ожидаем APPROVED)
    real_cr = Path("A_00_ARCHITECTURE/CHANGE_REQUESTS/CR_000_TEST.json")
    print(f"\n[Тест 1] Запуск штатного теста в режиме модуля:")
    print(json.dumps(guard.validate(real_cr), indent=2, ensure_ascii=False))

    # Тест 2: Эмуляция падающего интеграционного сценария (Ожидаем REJECTED / 424)
    broken_test_py = guard.project_root / "A_03_ORCHESTRATION" / "test_temporary_failing_logic.py"
    broken_test_py.write_text("# -*- coding: utf-8 -*-\nimport sys\nsys.exit(1)", encoding="utf-8")

    attack_cr_path = guard.project_root / "A_00_ARCHITECTURE" / "CHANGE_REQUESTS" / "CR_TEST_FAIL_ATTACK.json"
    attack_data = {
        "id": "CR_TEST_FAIL_ATTACK",
        "target_files": ["A_03_ORCHESTRATION/temporary_failing_logic.py"],
        "test_required": True
    }
    with open(attack_cr_path, "w", encoding="utf-8") as f:
        json.dump(attack_data, f, indent=2)

    print(f"\n[Тест 2] Проверка заявки с падающим модульным тестом:")
    print(json.dumps(guard.validate(attack_cr_path), indent=2, ensure_ascii=False))

    # Зачистка
    for tmp in [broken_test_py, attack_cr_path]:
        if tmp.exists():
            tmp.unlink()
    print("\n[OK] Тестирование компонента завершено.")
