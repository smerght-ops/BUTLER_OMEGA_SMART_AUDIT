# -*- coding: utf-8 -*-

from A_07_CONFIG.recipe_schema import SCHEMA_VERSION


class RecipeBuilder:

    """
    Stage 4.
    Converts GoalAnalyzer decision into Recipe v1.0.
    """

    def build_planning_recipe(self, goal_report, dependency_report):

        decision = goal_report["decision"]

        if decision == "WAIT":

            steps = []

        elif decision == "GENERATE_RECIPE":

            task = goal_report["next_task"]

            steps = [
                {
                    "action": "execute",
                    "command": (
                        f"print('NEXT_TASK::{task}')"
                    )
                }
            ]

        else:

            raise RuntimeError(
                f"Unknown decision: {decision}"
            )

        return {

            "schema_version": SCHEMA_VERSION,

            "task_id": "architect_agent_plan",

            "steps": steps,

            "meta": {

                "active_goal":
                    goal_report["active_goal"],

                "active_phase":
                    goal_report["active_phase"],

                "decision":
                    decision,

                "next_task":
                    goal_report["next_task"],

                "completed_tasks":
                    goal_report["completed_tasks"],

                "pending_tasks":
                    goal_report["pending_tasks"],

                "dependency_report":
                    dependency_report
            }
        }


if __name__=="__main__":

    from pprint import pprint

    rb = RecipeBuilder()

    recipe = rb.build_planning_recipe(

        {
            "active_goal":"TEST",
            "active_phase":"P1",
            "decision":"GENERATE_RECIPE",
            "next_task":"task_verify_contour",
            "completed_tasks":[],
            "pending_tasks":["task_verify_contour"]
        },

        {}
    )

    print("="*70)
    pprint(recipe)
    print("="*70)
