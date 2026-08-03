# -*- coding: utf-8 -*-

from A_07_MEMORY.semantic_reasoning_engine_v2 import SemanticReasoningEngineV2

r = SemanticReasoningEngineV2()

errors=[]

edges={}

for e in r.edges:

    key=(e["source"],e["target"],e["relation"])
    edges[key]=e

for e in r.edges:

    rev=(e["target"],e["source"],e["relation"])

    if rev in edges:
        errors.append(
            f'CONFLICT: {e["source"]} <-> {e["target"]} [{e["relation"]}]'
        )

print("="*70)
print("SEMANTIC CONSTRAINT CHECK V2")
print("="*70)

if errors:
    for x in sorted(set(errors)):
        print(x)
else:
    print("GRAPH OK")
