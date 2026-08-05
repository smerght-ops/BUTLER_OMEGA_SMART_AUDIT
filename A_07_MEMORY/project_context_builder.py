# -*- coding: utf-8 -*-
import json
from pathlib import Path

class ProjectContextBuilder:
    def __init__(self):
        self.project_root = Path(__file__).resolve().parents[1]
        self.exec_reg_path = self.project_root / "A_07_CONFIG" / "execution_registry.json"
        self.goals_path = self.project_root / "A_07_CONFIG" / "goals_registry.json"

    def load_execution_registry(self, limit=5):
        if not self.exec_reg_path.exists():
            return "Реестр задач отсутствует."

        try:
            with open(self.exec_reg_path, "r", encoding="utf-8-sig") as f:
                data = json.load(f)

            tasks = data.get("tasks", {})
            sorted_tasks = sorted(tasks.items(), key=lambda x: x[1].get("timestamp", ""), reverse=True)

            lines = [
    "=== EXECUTION REGISTRY ===",
    f"TOTAL TASKS: {len(tasks)}",
    "",
    "=== ПОСЛЕДНИЕ ЗАДАЧИ ИЗ EXECUTION_REGISTRY ==="
]

            for name, info in sorted_tasks[:limit]:
                lines.append(f"- [{info.get('status', 'UNKNOWN')}] {name} ({info.get('timestamp', '')})")

            return "\n".join(lines)

        except Exception as e:
            return f"Ошибка чтения execution_registry: {e}"

    def load_goals_registry(self):
        if not self.goals_path.exists():
            return "Реестр целей отсутствует."

        try:
            with open(self.goals_path, "r", encoding="utf-8-sig") as f:
                data = json.load(f)

            lines = ["=== GOALS REGISTRY ==="]
            lines.append(f"ACTIVE GOAL: {data.get('active_goal', 'UNKNOWN')}")
            lines.append(f"CURRENT PHASE: {data.get('current_phase', 'UNKNOWN')}")

            for goal in data.get("subgoals", []):
                lines.append(f"- {goal.get('id', 'UNKNOWN')} [{goal.get('status', 'UNKNOWN')}]")

            return "\n".join(lines)

        except Exception as e:
            return f"Ошибка чтения goals_registry: {e}"


    def load_ledger(self):
        ledger_path = self.project_root / "A_08_LOGS" / "PROJECT_LEDGER.txt"

        if not ledger_path.exists():
            return "PROJECT_LEDGER отсутствует."

        try:
            lines = ledger_path.read_text(
                encoding="utf-8-sig",
                errors="ignore"
            ).splitlines()

            lines = [x.strip() for x in lines if x.strip()]

            return "=== PROJECT LEDGER ===\n" + "\n".join(lines[-10:])

        except Exception as e:
            return f"Ошибка чтения PROJECT_LEDGER: {e}"

    def load_observations(self):
        obs_path = self.project_root / "A_08_LOGS" / "OBSERVATIONS.jsonl"

        if not obs_path.exists():
            return "OBSERVATIONS отсутствует."

        try:
            import json

            rows = []

            with open(obs_path, "r", encoding="utf-8-sig") as f:
                for line in f:
                    line = line.strip()

                    if not line:
                        continue

                    try:
                        obj = json.loads(line)

                        rows.append(
                            f"[{obj.get('source','?')}] {obj.get('event','?')}"
                        )

                    except Exception:
                        pass

            return "=== OBSERVATIONS ===\n" + "\n".join(rows[-10:])

        except Exception as e:
            return f"Ошибка чтения OBSERVATIONS: {e}"
    def build_context(self):
        return self.load_execution_registry() + "\n\n" + self.load_goals_registry() + "\n\n" + self.load_ledger() + "\n\n" + self.load_observations()

if __name__ == "__main__":
    builder = ProjectContextBuilder()
    print(builder.build_context())
