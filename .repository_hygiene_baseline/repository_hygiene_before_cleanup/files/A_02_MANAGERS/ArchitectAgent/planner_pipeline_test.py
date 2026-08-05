# -*- coding: utf-8 -*-

from pprint import pprint

from .recipe_generator import RecipeGenerator
from .task_contract_builder import TaskContractBuilder


planner = {

    "decision":"GENERATE_RECIPE",

    "next_task":"recipe_generator",

    "impact":[

        "A_07_CONFIG/recipe_schema.py",

        "A_07_CONFIG/task_registry.py"

    ]

}

recipe = RecipeGenerator().generate(planner)

contract = TaskContractBuilder().build(recipe)

print("="*70)
print("PIPELINE FORCED TEST")
print("="*70)

print()
print("RECIPE")
pprint(recipe)

print()
print("CONTRACT")
pprint(contract)

print("="*70)
