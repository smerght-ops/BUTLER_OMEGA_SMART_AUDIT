# -*- coding: utf-8 -*-

import importlib

modules = [

    "A_02_MANAGERS.ArchitectAgent.context_provider",
    "A_02_MANAGERS.ArchitectAgent.goal_analyzer",
    "A_02_MANAGERS.ArchitectAgent.dependency_analyzer",
    "A_02_MANAGERS.ArchitectAgent.planner_decision_engine",
    "A_02_MANAGERS.ArchitectAgent.recipe_generator",
    "A_02_MANAGERS.ArchitectAgent.task_contract_builder",
    "A_02_MANAGERS.ArchitectAgent.planner_pipeline",
    "A_02_MANAGERS.ArchitectAgent.architect_self_test",
    "A_02_MANAGERS.ArchitectAgent.architect_status",
    "A_02_MANAGERS.ArchitectAgent.architect_bootstrap",
    "A_02_MANAGERS.ArchitectAgent.architect_audit",
    "A_02_MANAGERS.ArchitectAgent.architect_release_check",
    "A_02_MANAGERS.ArchitectAgent.architect_manifest"

]

print("="*70)
print("ARCHITECT SMOKE TEST")
print("="*70)

ok = 0

for module in modules:

    importlib.import_module(module)

    print("[OK]", module)

    ok += 1

print()

print(f"RESULT : {ok}/{len(modules)}")

print("="*70)
