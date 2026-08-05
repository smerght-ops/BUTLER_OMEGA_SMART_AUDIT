# -*- coding: utf-8 -*-

from .context_provider import ContextProvider
from .goal_analyzer import GoalAnalyzer
from .dependency_analyzer import DependencyAnalyzer
from .planner_decision_engine import PlannerDecisionEngine
from .recipe_generator import RecipeGenerator
from .task_contract_builder import TaskContractBuilder

errors = []

try:
    ctx = ContextProvider().build_context()
except Exception as e:
    errors.append(f"ContextProvider : {e}")

try:
    goal = GoalAnalyzer().analyze(ctx)
except Exception as e:
    errors.append(f"GoalAnalyzer : {e}")

try:
    dep = DependencyAnalyzer().analyze(goal, ctx)
except Exception as e:
    errors.append(f"DependencyAnalyzer : {e}")

try:
    planner = PlannerDecisionEngine().decide(ctx)
except Exception as e:
    errors.append(f"PlannerDecisionEngine : {e}")

try:

    recipe = RecipeGenerator().generate({

        "decision":"GENERATE_RECIPE",

        "next_task":"recipe_generator",

        "impact":[
            "A_07_CONFIG/recipe_schema.py",
            "A_07_CONFIG/task_registry.py"
        ]

    })

except Exception as e:
    errors.append(f"RecipeGenerator : {e}")

try:
    contract = TaskContractBuilder().build(recipe)
except Exception as e:
    errors.append(f"TaskContractBuilder : {e}")

print("="*70)
print("ARCHITECT RELEASE CHECK")
print("="*70)

if errors:

    print("STATUS : FAILED")

    for e in errors:
        print("-", e)

else:

    print("STATUS : PASSED")
    print("MODULES: 6/6")
    print("GRAPH  :", dep["graph_nodes"], "nodes /", dep["graph_edges"], "edges")
    print("STATE  :", planner["decision"])

print("="*70)
