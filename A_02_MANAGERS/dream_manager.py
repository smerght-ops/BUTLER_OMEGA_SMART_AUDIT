# -*- coding: utf-8 -*-
from pathlib import Path

class ButlerDreamManager:
    def __init__(self, project_root=None):
        self.root = Path(project_root) if project_root else Path(__file__).resolve().parent.parent
        self.storage_dir = self.root / "A_05_STORAGE"
        self.tasks_dir = self.storage_dir / "tasks"
        self.checkpoint_file = self.storage_dir / "checkpoint.md"

    def consolidate_completed_task(self, dispatcher, task_id, employee="AUTO"):
        task_folder = self.tasks_dir / task_id
        progress_file = task_folder / "progress.md"
        summary_file = task_folder / "summary.md"

        if not progress_file.exists():
            print(f"DREAM_MANAGER: ПРОПУЩЕНО. progress.md не найден для {task_id}")
            return False

        raw_task_logs = progress_file.read_text(encoding="utf-8")

        system_distill = (
            "Ты аналитический модуль dream_manager.py в системе BUTLER_OMEGA_SMART.\n"
            "Извлеки из логов только техническую суть:\n"
            "1. ЧТО СДЕЛАНО.\n"
            "2. ПРИНЯТЫЕ РЕШЕНИЯ.\n"
            "3. ИСПРАВЛЕННЫЕ ОШИБКИ.\n"
            "Без лишних вступлений."
        )

        summary_content = dispatcher.execute_employee(
            employee=employee,
            system_prompt=system_distill,
            user_content=raw_task_logs
        )

        if not summary_content:
            print(f"DREAM_MANAGER: ОШИБКА. Сотрудник не подготовил summary для {task_id}")
            return False

        task_folder.mkdir(parents=True, exist_ok=True)
        summary_file.write_text(f"# SUMMARY {task_id}\n\n{summary_content}", encoding="utf-8")

        self._update_global_checkpoint(dispatcher, task_id, summary_content, employee)
        print("DREAM_MANAGER: ВЫПОЛНЕНО")
        return True

    def _update_global_checkpoint(self, dispatcher, last_task_id, last_task_summary, employee):
        system_checkpoint = (
            "Ты модуль синхронизации состояния проекта.\n"
            "Сформируй checkpoint.md строго в формате:\n"
            "# ТЕКУЩИЙ СТАТУС СИСТЕМЫ\n"
            "- **Последняя закрытая задача**: ...\n"
            "- **Что изменилось в архитектуре**: ...\n"
            "- **Ближайший шаг для Диспетчера**: ...\n"
            "Выдай только Markdown."
        )

        user_input = f"Последняя задача: {last_task_id}\nВыжимка:\n{last_task_summary}"

        new_checkpoint = dispatcher.execute_employee(
            employee=employee,
            system_prompt=system_checkpoint,
            user_content=user_input
        )

        if new_checkpoint:
            self.checkpoint_file.write_text(new_checkpoint, encoding="utf-8")
            print("checkpoint.md обновлен")
        else:
            print("checkpoint.md не изменен")

if __name__ == "__main__":
    class FakeDispatcher:
        def execute_employee(self, employee, system_prompt, user_content):
            return (
                "1. ЧТО СДЕЛАНО: тестовая консолидация выполнена.\n"
                "2. ПРИНЯТЫЕ РЕШЕНИЯ: DreamManager работает через dispatcher.execute_employee.\n"
                "3. ИСПРАВЛЕННЫЕ ОШИБКИ: прямой вызов модели исключен."
            )

    dm = ButlerDreamManager()
    test_task = dm.tasks_dir / "TASK-TEST"
    test_task.mkdir(parents=True, exist_ok=True)
    (test_task / "progress.md").write_text(
        "Тестовая задача: проверить DreamManager без прямой привязки к модели.",
        encoding="utf-8"
    )
    dm.consolidate_completed_task(FakeDispatcher(), "TASK-TEST")
