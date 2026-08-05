# -*- coding: utf-8 -*-

class GoalAnalyzer:
    """
    Architect Agent V1

    Deterministic Goal Analyzer.

    Reads current project state and decides ONLY the next task.
    Does not execute anything.
    Does not generate patches.
    """

    def analyze(self, context):

        goals = context.get("goals_registry", {})

        active_goal = goals.get("active_goal", "UNKNOWN")
        active_phase = goals.get("current_phase", "UNKNOWN")
        status = goals.get("status", "UNKNOWN")

        completed = []
        pending = []

        for subgoal in goals.get("subgoals", []):

            if subgoal.get("id") != active_phase:
                continue

            for task in subgoal.get("tasks", []):

                task_id = task.get("id")

                state = str(task.get("status","")).upper()

                if state == "COMPLETED":
                    completed.append(task_id)
                else:
                    pending.append(task_id)

        next_task = pending[0] if pending else None

        if next_task:

            decision = "GENERATE_RECIPE"

            reason = (
                f"Next unfinished task detected: {next_task}"
            )

        else:

            decision = "WAIT"

            reason = (
                "Current phase has no unfinished tasks."
            )

        return {

            "active_goal": active_goal,

            "active_phase": active_phase,

            "status": status,

            "completed_tasks": completed,

            "pending_tasks": pending,

            "next_task": next_task,

            "decision": decision,

            "reason": reason,

            "confidence": 1.0
        }


if __name__ == "__main__":

    from .context_provider import ContextProvider
    import pprint

    ctx = ContextProvider().build_context()

    result = GoalAnalyzer().analyze(ctx)

    print("=" * 70)
    print("GOAL ANALYZER V1")
    print("=" * 70)

    pprint.pp(result)

    print("=" * 70)
