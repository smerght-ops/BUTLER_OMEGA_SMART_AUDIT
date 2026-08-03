# -*- coding: utf-8 -*-

from .dependency_graph import DependencyGraph


class DependencyClosure:
    """
    Stage 4.
    Computes transitive dependency closure using DFS.
    """

    def __init__(self, root=None):

        self.graph = DependencyGraph(root).build()

    def closure(self, module):

        visited = set()

        def dfs(node):

            if node in visited:
                return

            visited.add(node)

            for dep in self.graph.get(node, []):

                target = dep.replace(".", "/") + ".py"

                for candidate in self.graph:

                    if candidate.endswith(target):

                        dfs(candidate)

        dfs(module)

        visited.discard(module)

        return sorted(visited)


if __name__=="__main__":

    from pprint import pprint

    dc = DependencyClosure()

    print("="*70)
    print("DEPENDENCY CLOSURE V1")
    print("="*70)

    pprint(
        dc.closure(
            "A_02_MANAGERS/recipe_generator.py"
        )
    )

    print("="*70)
