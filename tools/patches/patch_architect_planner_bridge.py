from pathlib import Path

# --- patch PlannerEngine ---
p=Path(r"A_02_MANAGERS\Planner\planner_engine.py")
t=p.read_text(encoding="utf-8")

if "def execute_decision" not in t:
    insert='''
    @staticmethod
    def execute_decision(decision: dict):

        if not isinstance(decision, dict):
            print("Planner: invalid decision.")
            return None

        if decision.get("decision") == "WAIT":
            print("Planner: WAIT -", decision.get("reason", "no reason"))
            return None

        goal_text = decision.get("goal_text") or decision.get("next_task")

        if not goal_text:
            print("Planner: decision has no executable goal.")
            return None

        return PlannerEngine.execute(goal_text)

'''
    t=t.replace('\n\nif __name__ == "__main__":', '\n'+insert+'\nif __name__ == "__main__":')

# make execute return path
t=t.replace(
'''        print(state)
''',
'''        print(state)

        return path
'''
)

p.write_text(t,encoding="utf-8")


# --- patch ArchitectAgent ---
p=Path(r"A_02_MANAGERS\ArchitectAgent\architect_agent.py")
t=p.read_text(encoding="utf-8")

if "from A_02_MANAGERS.Planner.planner_engine import PlannerEngine" not in t:
    t=t.replace(
        "from .queue_manager import QueueManager",
        "from .queue_manager import QueueManager\nfrom A_02_MANAGERS.Planner.planner_engine import PlannerEngine"
    )

if "def execute_goal" not in t:
    insert='''
    def execute_goal(self, goal_text: str):
        """
        Bridge: ArchitectAgent -> PlannerEngine -> RecipeWriter.
        Does not execute shell directly.
        """
        return PlannerEngine.execute(goal_text)

'''
    t=t.replace("    def plan(self):", insert+"    def plan(self):")

p.write_text(t,encoding="utf-8")

print("ARCHITECT <-> PLANNER BRIDGE OK")
