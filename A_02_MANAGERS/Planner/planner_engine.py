# -*- coding: utf-8 -*-

"""
Stage 9.1

Planner Engine
"""

from A_02_MANAGERS.ExecutionMonitor.system_state import SystemState
from A_02_MANAGERS.Planner.goal_interpreter import GoalInterpreter
from A_02_MANAGERS.Planner.task_planner import TaskPlanner
from A_02_MANAGERS.TaskRunner.recipe_writer import RecipeWriter
from A_02_MANAGERS.TaskRunner.runner_once import run_once


class PlannerEngine:

    @staticmethod
    def can_handle(goal_text: str):

        return GoalInterpreter.interpret(goal_text) is not None


    @staticmethod
    def execute(goal_text: str):

        state = SystemState.current()

        if state.pending > 0:

            print("Planner: queue is busy.")

            return

        goal = GoalInterpreter.interpret(goal_text)

        if goal is None:

            print("Planner: unknown goal.")

            return

        recipe = TaskPlanner.plan(goal)

        path = RecipeWriter.write(recipe)

        print()

        print("GOAL      :", goal.id)
        print("RECIPE    :", recipe.recipe_id)
        print("QUEUED TO :", path)

        print()

        print("SYSTEM STATE")

        print(state)

        print()
        print("AUTORUN...")

        run_once()

        return path


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


if __name__ == "__main__":

    print(PlannerEngine.can_handle("python version"))
    print(PlannerEngine.can_handle("нарисуй дракона"))

