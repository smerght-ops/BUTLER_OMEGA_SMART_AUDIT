# -*- coding: utf-8 -*-

from .context_provider import ContextProvider
from .goal_analyzer import GoalAnalyzer
from .dependency_analyzer import DependencyAnalyzer
from .planner_decision_engine import PlannerDecisionEngine
from .recipe_generator import RecipeGenerator
from .task_contract_builder import TaskContractBuilder


print("="*70)
print("ARCHITECT AGENT AUDIT")
print("="*70)

ctx = ContextProvider().build_context()
goal = GoalAnalyzer().analyze(ctx)
dep = DependencyAnalyzer().analyze(goal, ctx)
planner = PlannerDecisionEngine().decide(ctx)

print(f"Context    : {'OK' if ctx else 'FAIL'}")
print(f"Goal       : {goal['decision']}")
print(f"Planner    : {planner['decision']}")
print(f"Nodes      : {dep['graph_nodes']}")
print(f"Edges      : {dep['graph_edges']}")

recipe = RecipeGenerator().generate({

    "decision":"GENERATE_RECIPE",

    "next_task":"recipe_generator",

    "impact":[
        "A_07_CONFIG/recipe_schema.py",
        "A_07_CONFIG/task_registry.py"
    ]

})

contract = TaskContractBuilder().build(recipe)

print(f"Recipe     : {'OK' if recipe else 'FAIL'}")
print(f"Contract   : {'OK' if contract else 'FAIL'}")

print()

if planner["decision"]=="WAIT":

    print("SYSTEM STATE : READY")
    print("EXECUTION    : IDLE")
    print("REASON       :", planner["reason"])

else:

    print("SYSTEM STATE : READY")
    print("EXECUTION    : ACTIVE")

print("="*70)
