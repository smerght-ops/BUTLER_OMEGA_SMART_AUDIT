# -*- coding: utf-8 -*-

from .planner_pipeline import PlannerPipeline
from .recipe_generator import RecipeGenerator
from .task_contract_builder import TaskContractBuilder


class ArchitectBootstrap:

    def __init__(self):

        self.pipeline = PlannerPipeline()

        self.recipe = RecipeGenerator()

        self.contract = TaskContractBuilder()

    def run(self):

        result = self.pipeline.run()

        if result["planner"]["decision"] == "WAIT":

            return result

        recipe = self.recipe.generate(
            result["planner"]
        )

        contract = self.contract.build(
            recipe
        )

        result["recipe"] = recipe
        result["contract"] = contract

        return result


if __name__=="__main__":

    from pprint import pprint

    print("="*70)
    print("ARCHITECT BOOTSTRAP")
    print("="*70)

    pprint(
        ArchitectBootstrap().run()
    )

    print("="*70)
