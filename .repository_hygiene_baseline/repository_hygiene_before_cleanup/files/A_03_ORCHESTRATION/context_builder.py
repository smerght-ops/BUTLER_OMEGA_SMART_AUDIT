# -*- coding: utf-8 -*-
from pathlib import Path

class ButlerContextBuilder:
    def __init__(self, project_root=None):
        self.root = Path(project_root) if project_root else Path(__file__).resolve().parent.parent
        self.storage_dir = self.root / "A_05_STORAGE"
        self.memory_file = self.storage_dir / "MEMORY.md"
        self.checkpoint_file = self.storage_dir / "checkpoint.md"
        self.tasks_dir = self.storage_dir / "tasks"

    def _read_layer_safe(self, file_path: Path) -> str:
        if file_path.exists():
            try:
                return file_path.read_text(encoding="utf-8").strip()
            except Exception:
                return ""
        return ""

    def assemble_context(self, active_task_id=None, current_session_history=None) -> dict:
        constitution = self._read_layer_safe(self.memory_file)
        project_state = self._read_layer_safe(self.checkpoint_file)

        task_progress = ""
        task_summary = ""
        task_memory_block = ""

        if active_task_id:
            progress_path = self.tasks_dir / active_task_id / "progress.md"
            summary_path = self.tasks_dir / active_task_id / "summary.md"

            task_progress = self._read_layer_safe(progress_path)
            task_summary = self._read_layer_safe(summary_path)

            if task_progress or task_summary:
                task_memory_block = f"=== ХРОНОЛОГИЯ АКТИВНОЙ ЗАДАЧИ ({active_task_id}) ===\n"
                if task_progress:
                    task_memory_block += f"Текущий прогресс:\n{task_progress}\n\n"
                if task_summary:
                    task_memory_block += f"Предыдущие выводы:\n{task_summary}\n\n"

        session_block = ""
        if current_session_history:
            session_block = f"=== ЖИВОЙ ДИАЛОГ СЕССИИ ===\n{current_session_history}\n\n"

        prompt_parts = []

        if constitution:
            prompt_parts.append(f"=== КОНСТИТУЦИЯ И ПРАВИЛА (MEMORY.md) ===\n{constitution}")

        if project_state:
            prompt_parts.append(f"=== ТЕКУЩИЙ СТАТУС ПРОЕКТА (checkpoint.md) ===\n{project_state}")

        if task_memory_block:
            prompt_parts.append(task_memory_block)

        if session_block:
            prompt_parts.append(session_block)

        prompt_parts.append(
            "==================================================\n"
            "ИНСТРУКЦИЯ:\n"
            "Ты Butler Omega. Используй память, историю диалога и контекст проекта. "
            "Отвечай на вопрос пользователя напрямую и по существу. "
            "Если в истории есть ответ на вопрос пользователя — используй его."
        )

        final_prompt = "\n\n".join(prompt_parts)

        return {
            "memory": constitution,
            "checkpoint": project_state,
            "task_progress": task_progress,
            "task_summary": task_summary,
            "session": current_session_history or "",
            "assembled_prompt": final_prompt,
            "stats": {
                "memory_used": bool(constitution),
                "checkpoint_used": bool(project_state),
                "task_progress_used": bool(task_progress),
                "task_summary_used": bool(task_summary),
                "session_used": bool(current_session_history)
            }
        }

if __name__ == "__main__":
    builder = ButlerContextBuilder()
    result = builder.assemble_context(
        active_task_id="TASK-TEST",
        current_session_history="User: Проверка контекст-билдера."
    )
    print("CONTEXT_BUILDER: ВЫПОЛНЕНО")
    print(result["stats"])
    print(result["assembled_prompt"][:1200])
