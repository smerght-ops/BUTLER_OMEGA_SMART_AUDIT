# -*- coding: utf-8 -*-

from .dependency_graph import DependencyGraph
from .dependency_closure import DependencyClosure


class DependencyAnalyzer:

    """
    Stage 4.

    Full impact analyzer.

    Graph
        +
    Transitive Closure
        ↓
    Impact Report
    """

    def __init__(self, root=None):

        self.graph = DependencyGraph(root).build()
        self.closure = DependencyClosure(root)

    def analyze(self, goal_report, context):

        impacts = {}

        for module in sorted(self.graph):

            impacts[module] = self.closure.closure(module)

        return {

            "graph_nodes": len(self.graph),

            "graph_edges": sum(len(v) for v in self.graph.values()),

            "impact_graph": impacts,

            "safe_execution": True
        }


if __name__=="__main__":

    from pprint import pprint

    da = DependencyAnalyzer()

    report = da.analyze({},{})

    print("="*70)
    print("DEPENDENCY ANALYZER V2")
    print("="*70)

    pprint(
        report["impact_graph"].get(
            "A_02_MANAGERS/recipe_generator.py",
            []
        )
    )

    print("="*70)
    print("NODES :",report["graph_nodes"])
    print("EDGES :",report["graph_edges"])
    print("="*70)
