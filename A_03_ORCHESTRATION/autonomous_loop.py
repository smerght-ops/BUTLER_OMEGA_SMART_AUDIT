import json

class AutonomousLoop:

    def execute(self, plan: dict):

        for step in plan.get("steps", []):

            if step["status"] == "completed":
                continue

            step["status"] = "running"

            # LAB SIMULATION
            step["status"] = "completed"

        plan["status"] = "completed"

        return plan


if __name__ == "__main__":

    planner_plan = {
        "plan_id": "lab_demo",
        "status": "pending",
        "steps": [
            {
                "step_id": 1,
                "agent": "memory",
                "task": "demo",
                "status": "pending"
            },
            {
                "step_id": 2,
                "agent": "coder",
                "task": "demo2",
                "status": "pending"
            }
        ]
    }

    loop = AutonomousLoop()

    result = loop.execute(planner_plan)

    assert result["status"] == "completed"

    for s in result["steps"]:
        assert s["status"] == "completed"

    print("AUTONOMOUS LOOP LAB OK")