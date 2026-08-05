# -*- coding: utf-8 -*-

from A_07_MEMORY.semantic_reasoning_engine_v2 import SemanticReasoningEngineV2

r = SemanticReasoningEngineV2()

graph = {}

for e in r.edges:
    graph.setdefault(e["source"], []).append(e["target"])

visited = set()
stack = []
cycles = []

def dfs(node):

    if node in stack:
        i = stack.index(node)
        cycles.append(stack[i:] + [node])
        return

    if node in visited:
        return

    visited.add(node)
    stack.append(node)

    for nxt in graph.get(node, []):
        dfs(nxt)

    stack.pop()

for node in list(graph.keys()):
    dfs(node)

print("=" * 70)
print("SEMANTIC CONSTRAINT CHECK V3")
print("=" * 70)

if cycles:
    print("CYCLES FOUND")
    for c in cycles:
        print(" -> ".join(c))
else:
    print("GRAPH OK")
