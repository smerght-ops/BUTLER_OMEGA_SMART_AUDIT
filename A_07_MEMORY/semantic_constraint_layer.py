# -*- coding: utf-8 -*-

"""
BUTLER OMEGA SMART
ROADMAP 6.0

Semantic Constraint Layer
Stage 1.5
"""

from A_07_MEMORY.semantic_reasoning_engine_v2 import SemanticReasoningEngineV2


class SemanticConstraintLayer:

    def __init__(self):

        self.reasoner = SemanticReasoningEngineV2()

    def validate(self):

        report = {
            "self_loops": [],
            "reverse_conflicts": [],
            "cycles": [],
            "architecture": [],
            "laws": []
        }

        edges = self.reasoner.edges

        # ---------- SELF LOOPS ----------

        for e in edges:
            if e["source"] == e["target"]:
                report["self_loops"].append(e)

        # ---------- REVERSE ----------

        table = {
            (e["source"], e["target"], e["relation"])
            for e in edges
        }

        for e in edges:

            rev = (
                e["target"],
                e["source"],
                e["relation"]
            )

            if rev in table:
                report["reverse_conflicts"].append(e)

        # ---------- CYCLES ----------

        graph = {}

        for e in edges:
            graph.setdefault(e["source"], []).append(e["target"])

        visited = set()
        stack = []

        def dfs(node):

            if node in stack:
                report["cycles"].append(stack[:] + [node])
                return

            if node in visited:
                return

            visited.add(node)
            stack.append(node)

            for nxt in graph.get(node, []):
                dfs(nxt)

            stack.pop()

        for node in graph:
            dfs(node)

        if not self.reasoner.edges:
            report["architecture"].append(
                "Knowledge graph is empty."
            )

        return report


if __name__ == "__main__":

    layer = SemanticConstraintLayer()

    r = layer.validate()

    print("=" * 70)
    print("SEMANTIC CONSTRAINT LAYER")
    print("=" * 70)

    print(r)
