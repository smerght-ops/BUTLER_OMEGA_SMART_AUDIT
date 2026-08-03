# -*- coding: utf-8 -*-

from .dependency_analyzer import DependencyAnalyzer

files = [

    "context_provider.py",
    "goal_analyzer.py",
    "dependency_analyzer.py",
    "planner_decision_engine.py",
    "recipe_generator.py",
    "task_contract_builder.py",
    "planner_pipeline.py",
    "planner_pipeline_test.py",
    "architect_self_test.py",
    "architect_status.py",
    "architect_bootstrap.py",
    "architect_audit.py",
    "architect_release_check.py"

]

dep = DependencyAnalyzer().analyze({}, {})

print("="*70)
print("ARCHITECT AGENT MANIFEST")
print("="*70)

print("Modules :", len(files))

for f in files:

    print("[OK]", f)

print()

print("Graph Nodes :", dep["graph_nodes"])
print("Graph Edges :", dep["graph_edges"])

print("="*70)
