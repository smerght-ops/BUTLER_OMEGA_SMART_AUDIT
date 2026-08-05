# -*- coding: utf-8 -*-

"""
Stage 8.3

Planner Facade

Goal
    ↓
GoalInterpreter
    ↓
TaskPlanner
    ↓
RecipeWriter
"""

from A_02_MANAGERS.Planner.goal_interpreter import GoalInterpreter
from A_02_MANAGERS.Planner.task_planner import TaskPlanner
from A_02_MANAGERS.TaskRunner.recipe_writer import RecipeWriter


class PlannerFacade:

    @staticmethod
    def execute(goal_text: str):

        goal = GoalInterpreter.interpret(goal_text)

        if goal is None:

            raise ValueError(
                f"Unknown goal: {goal_text}"
            )

        recipe = TaskPlanner.plan(goal)

        path = RecipeWriter.write(recipe)

        print("GOAL   :", goal.id)
        print("RECIPE :", recipe.recipe_id)
        print("QUEUE  :", path)

        return path


if __name__ == "__main__":

    PlannerFacade.execute(
        "python version"
    )
