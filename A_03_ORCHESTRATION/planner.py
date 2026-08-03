import json
from datetime import datetime

class Planner:

    def build_plan(self, task: str):
        task = str(task).strip()

        return {
            "created_at": datetime.utcnow().isoformat() + "Z",
            "task": task,
            "status": "planned",
            "current_step": 0,
            "steps": [
                {
                    "id": 1,
                    "name": "analyze_request",
                    "status": "pending"
                },
                {
                    "id": 2,
                    "name": "select_agent",
                    "status": "pending"
                },
                {
                    "id": 3,
                    "name": "execute",
                    "status": "pending"
                },
                {
                    "id": 4,
                    "name": "verify_result",
                    "status": "pending"
                }
            ]
        }

if __name__ == "__main__":
    planner = Planner()
    plan = planner.build_plan("demo task")

    print(json.dumps(
        plan,
        indent=2,
        ensure_ascii=False
    ))