# -*- coding: utf-8 -*-

from .goal_analyzer import GoalAnalyzer
from .dependency_analyzer import DependencyAnalyzer


class PlannerDecisionEngine:
    """
    Stage 4.

    Final planner decision.

    Goal
        +
    Dependency
        =
    Planner Decision
    """

    def __init__(self, root=None):

        self.goal = GoalAnalyzer()
        self.dep = DependencyAnalyzer(root)

    def decide(self, context):

        goal = self.goal.analyze(context)

        dep = self.dep.analyze(goal, context)

        if goal["decision"] == "WAIT":

            return {

                "decision": "WAIT",

                "reason": goal["reason"],

                "next_task": None,

                "impact": []

            }

        impact = dep["impact_graph"].get(

            f"A_02_MANAGERS/{goal['next_task']}.py",

            []

        )

        return {

            "decision": "GENERATE_RECIPE",

            "next_task": goal["next_task"],

            "impact": impact,

            "goal": goal,

            "dependency": dep

        }


if __name__=="__main__":

    from pprint import pprint
    from .context_provider import ContextProvider

    ctx = ContextProvider().build_context()

    planner = PlannerDecisionEngine()

    result = planner.decide(ctx)

    print("="*70)
    print("PLANNER DECISION ENGINE V1")
    print("="*70)

    pprint(result)

    print("="*70)
