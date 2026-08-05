# -*- coding: utf-8 -*-

from .context_provider import ContextProvider
from .goal_analyzer import GoalAnalyzer
from .dependency_analyzer import DependencyAnalyzer
from .planner_decision_engine import PlannerDecisionEngine
from .recipe_generator import RecipeGenerator
from .task_contract_builder import TaskContractBuilder


print("="*70)
print("ARCHITECT AGENT SELF TEST")
print("="*70)

ctx = ContextProvider().build_context()

print("[OK] ContextProvider")

goal = GoalAnalyzer().analyze(ctx)

print("[OK] GoalAnalyzer")

dep = DependencyAnalyzer().analyze(goal, ctx)

print("[OK] DependencyAnalyzer")

planner = PlannerDecisionEngine().decide(ctx)

print("[OK] PlannerDecisionEngine")

recipe = RecipeGenerator().generate({

    "decision":"GENERATE_RECIPE",

    "next_task":"recipe_generator",

    "impact":[

        "A_07_CONFIG/recipe_schema.py",

        "A_07_CONFIG/task_registry.py"

    ]

})

print("[OK] RecipeGenerator")

contract = TaskContractBuilder().build(recipe)

print("[OK] TaskContractBuilder")

assert recipe is not None
assert contract is not None
assert contract["status"]=="READY"
assert len(contract["dependencies"])==2

print()
print("ALL TESTS PASSED")

print("="*70)
