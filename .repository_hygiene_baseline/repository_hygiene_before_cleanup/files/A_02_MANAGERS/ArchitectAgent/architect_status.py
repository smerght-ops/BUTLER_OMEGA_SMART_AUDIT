# -*- coding: utf-8 -*-

from .context_provider import ContextProvider
from .goal_analyzer import GoalAnalyzer
from .dependency_analyzer import DependencyAnalyzer
from .planner_decision_engine import PlannerDecisionEngine


ctx = ContextProvider().build_context()

goal = GoalAnalyzer().analyze(ctx)

dep = DependencyAnalyzer().analyze(goal, ctx)

planner = PlannerDecisionEngine().decide(ctx)

print("="*70)
print("ARCHITECT STATUS")
print("="*70)

print("Decision :", planner["decision"])

if planner["decision"] == "WAIT":

    print("Reason   :", planner["reason"])

else:

    print("Task     :", planner["next_task"])
    print("Impact   :", len(planner["impact"]))

print()

print("Graph Nodes :", dep["graph_nodes"])
print("Graph Edges :", dep["graph_edges"])

print("="*70)
