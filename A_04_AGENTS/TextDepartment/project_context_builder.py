# -*- coding: utf-8 -*-

import json
from pathlib import Path

class ProjectContextBuilder:
    def __init__(self):
        self.project_root = Path(__file__).resolve().parents[2]
        self.exec_reg_path = self.project_root / "A_07_CONFIG" / "execution_registry.json"
        self.goals_reg_path = self.project_root / "A_07_CONFIG" / "goals_registry.json"
        self.ledger_path = self.project_root / "A_08_LOGS" / "PROJECT_LEDGER.txt"

    def get_execution_context(self, limit=5) -> str:
        if not self.exec_reg_path.exists():
            return "Реестр задач отсутствует."
        try:
            with open(self.exec_reg_path, "r", encoding="utf-8-sig") as f:
                data = json.load(f)
            tasks = data.get("tasks", {})
            if not tasks:
                return "Нет выполненных задач в реестре."
            sorted_tasks = sorted(tasks.items(), key=lambda x: x[1].get("timestamp", ""), reverse=True)
            lines = ["=== ПОСЛЕДНИЕ ЗАДАЧИ ИЗ EXECUTION_REGISTRY ==="]
            for name, info in sorted_tasks[:limit]:
                lines.append(f"- [{info.get('status', 'UNKNOWN')}] {name} ({info.get('timestamp', '')})")
            return "\n".join(lines)
        except Exception as e:
            return f"Ошибка чтения реестра задач: {str(e)}"

    def get_goals_context(self) -> str:
        if not self.goals_reg_path.exists():
            return "Реестр целей отсутствует."
        try:
            with open(self.goals_reg_path, "r", encoding="utf-8-sig") as f:
                data = json.load(f)
            lines = ["=== ТЕКУЩИЕ ЦЕЛИ ИЗ GOALS_REGISTRY ==="]
            lines.append(f"Активная цель: {data.get('active_goal', 'UNKNOWN')}")
            lines.append(f"Текущая фаза: {data.get('current_phase', 'UNKNOWN')}")
            subgoals = data.get("subgoals", [])
            for sg in subgoals:
                lines.append(f"- Фаза [{sg.get('status', 'UNKNOWN')}]: {sg.get('id', 'UNKNOWN')}")
            return "\n".join(lines)
        except Exception as e:
            return f"Ошибка чтения реестра целей: {str(e)}"

    def get_ledger_context(self, limit=5) -> str:
        if not self.ledger_path.exists():
            return "Журнал проекта отсутствует."
        try:
            with open(self.ledger_path, "r", encoding="utf-8") as f:
                lines = [line.strip() for line in f if line.strip()]
            return "=== ПОСЛЕДНИЕ ЗАПИСИ ЖУРНАЛА (PROJECT_LEDGER) ===\n" + "\n".join(lines[-limit:])
        except Exception as e:
            return f"Ошибка чтения журнала: {str(e)}"

    def build_full_context(self) -> str:
        return f"{self.get_goals_context()}\n\n{self.get_execution_context()}\n\n{self.get_ledger_context()}"

if __name__ == "__main__":
    builder = ProjectContextBuilder()
    print(builder.build_full_context())
