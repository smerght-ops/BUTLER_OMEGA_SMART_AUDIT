# -*- coding: utf-8 -*-

from A_07_MEMORY.semantic_reasoning_engine_v2 import SemanticReasoningEngineV2

r = SemanticReasoningEngineV2()

errors = []

for e in r.edges:

    if e["source"] == e["target"]:
        errors.append(f'SELF LOOP: {e}')

print("="*70)
print("SEMANTIC CONSTRAINT CHECK")
print("="*70)

if errors:
    for x in errors:
        print(x)
else:
    print("GRAPH OK")
