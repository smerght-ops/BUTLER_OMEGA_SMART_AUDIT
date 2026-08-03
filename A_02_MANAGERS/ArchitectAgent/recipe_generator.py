# -*- coding: utf-8 -*-

from copy import deepcopy


class RecipeGenerator:

    """
    Converts planner decision into executable recipe.
    """

    def generate(self, planner_result):

        if planner_result["decision"] != "GENERATE_RECIPE":

            return None

        recipe = {

            "task": planner_result["next_task"],

            "action": "CREATE",

            "target": f"A_02_MANAGERS/{planner_result['next_task']}.py",

            "template": "manager_module",

            "dependencies": deepcopy(
                planner_result["impact"]
            ),

            "tests": [

                "py_compile",

                "unit_test"

            ]

        }

        return recipe


if __name__ == "__main__":

    from pprint import pprint

    rg = RecipeGenerator()

    pprint(
        rg.generate(
            {

                "decision": "GENERATE_RECIPE",

                "next_task": "recipe_generator",

                "impact": [

                    "A_07_CONFIG/recipe_schema.py",

                    "A_07_CONFIG/task_registry.py"

                ]

            }
        )
    )
