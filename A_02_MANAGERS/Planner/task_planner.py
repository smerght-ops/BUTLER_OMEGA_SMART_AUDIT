# -*- coding: utf-8 -*-

"""
Stage 8.2

Task Planner

Goal
    ↓
Recipe
"""

from A_02_MANAGERS.Planner.goal_interpreter import Goal
from A_02_MANAGERS.TaskRunner.recipe_builder import RecipeBuilder


class TaskPlanner:

    @staticmethod
    def plan(goal: Goal):

        if goal is None:

            raise ValueError("Unknown goal")

        if goal.id == "GOAL_PYTHON_VERSION":

            return RecipeBuilder.python(
                "--version"
            )

        if goal.id == "GOAL_POWERSHELL_VERSION":

            return RecipeBuilder.powershell(
                "$PSVersionTable.PSVersion"
            )

        if goal.id == "GOAL_RUN_AUDIT":

            return RecipeBuilder.python(
                ".\\run_audit.py"
            )

        raise ValueError(
            f"Planner has no recipe for {goal.id}"
        )


if __name__ == "__main__":

    from A_02_MANAGERS.Planner.goal_interpreter import GoalInterpreter

    goal = GoalInterpreter.interpret(
        "python version"
    )

    recipe = TaskPlanner.plan(goal)

    print(recipe)

