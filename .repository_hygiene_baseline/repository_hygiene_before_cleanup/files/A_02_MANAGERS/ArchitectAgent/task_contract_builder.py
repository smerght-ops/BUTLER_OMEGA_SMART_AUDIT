# -*- coding: utf-8 -*-

from copy import deepcopy


class TaskContractBuilder:

    """
    Converts Recipe into immutable Task Contract.
    """

    def build(self, recipe):

        if recipe is None:

            return None

        return {

            "contract_version": 1,

            "status": "READY",

            "task": recipe["task"],

            "action": recipe["action"],

            "target": recipe["target"],

            "template": recipe["template"],

            "dependencies": deepcopy(
                recipe["dependencies"]
            ),

            "tests": deepcopy(
                recipe["tests"]
            )

        }


if __name__=="__main__":

    from pprint import pprint

    builder = TaskContractBuilder()

    pprint(
        builder.build(
            {

                "task":"recipe_generator",

                "action":"CREATE",

                "target":"A_02_MANAGERS/recipe_generator.py",

                "template":"manager_module",

                "dependencies":[

                    "A_07_CONFIG/recipe_schema.py",

                    "A_07_CONFIG/task_registry.py"

                ],

                "tests":[

                    "py_compile",

                    "unit_test"

                ]

            }
        )
    )
