# -*- coding: utf-8 -*-

from A_07_MEMORY.semantic_query_parser import SemanticQueryParser
from A_07_MEMORY.semantic_core import SemanticCore
from A_07_MEMORY.semantic_constraint_layer import SemanticConstraintLayer

print("="*70)
print("ROADMAP 6.0 - STAGE 1 ACCEPTANCE")
print("="*70)

SemanticQueryParser()
print("[OK] SemanticQueryParser")

SemanticCore()
print("[OK] SemanticCore")

layer=SemanticConstraintLayer()

report=layer.validate()

assert not report["self_loops"]
assert not report["reverse_conflicts"]
assert not report["cycles"]

print("[OK] SemanticConstraintLayer")

print()
print("STAGE 1 STATUS : COMPLETED")
print("="*70)
