# -*- coding: utf-8 -*-

from pprint import pprint

from .context_provider import ContextProvider
from .planner_decision_engine import PlannerDecisionEngine
from .recipe_generator import RecipeGenerator
from .task_contract_builder import TaskContractBuilder


class PlannerPipeline:

    def __init__(self, root=None):

        self.context = ContextProvider()

        self.planner = PlannerDecisionEngine(root)

        self.recipe = RecipeGenerator()

        self.contract = TaskContractBuilder()

    def run(self):

        ctx = self.context.build_context()

        planner = self.planner.decide(ctx)

        recipe = self.recipe.generate(planner)

        contract = self.contract.build(recipe)

        return {

            "planner": planner,

            "recipe": recipe,

            "contract": contract

        }


if __name__=="__main__":

    pipeline = PlannerPipeline()

    print("="*70)
    print("PLANNER PIPELINE")
    print("="*70)

    pprint(
        pipeline.run()
    )

    print("="*70)
