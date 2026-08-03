============================================================
BUTLER PROJECT REALITY AUDIT V2
============================================================

MANAGERS
--------
STATUS : PRESENT
PATH   : A_02_MANAGERS
PY     : 75

KEY COMPONENTS
  ✓ A_02_MANAGERS\smart_dispatcher_v2.py
  - dispatcher_bridge_v2.py (not found)
  ✓ A_02_MANAGERS\session_manager.py
  ✓ A_02_MANAGERS\model_registry.py
  ✓ A_02_MANAGERS\ExecutionPolicyEngine

MEMORY
------
STATUS : PRESENT
PATH   : A_07_MEMORY
PY     : 44

KEY COMPONENTS
  ✓ A_07_MEMORY\semantic_memory.py
  ✓ A_07_MEMORY\memory_facade_v2.py
  ✓ A_07_MEMORY\memory_orchestrator.py
  ✓ A_07_MEMORY\project_history.py
  ✓ A_07_MEMORY\change_request_manager.py

CONFIG
------
STATUS : PRESENT
PATH   : A_07_CONFIG
PY     : 14

KEY COMPONENTS
  ✓ A_07_CONFIG\project_passport.json
  ✓ A_07_CONFIG\recipe_schema.py
  ✓ A_07_CONFIG\task_registry.py

AGENTS
------
STATUS : PRESENT
PATH   : A_04_AGENTS
PY     : 130

KEY COMPONENTS
  ✓ A_04_AGENTS\ImageDepartment
  ✓ A_04_AGENTS\MemoryDepartment
  ✓ A_04_AGENTS\CodingDepartment
  ✓ A_04_AGENTS\TextDepartment

============================================================
LOCKED PIPELINE
============================================================
✓ Inspector0_PhysicalMap.json
✓ Inspector1_EntityMap.json
✓ Inspector2_ImportMap.json
✓ Inspector3_RegistrationAST.json
✓ Inspector4_CallGraph.json
✓ LinkMap.json
✓ DependencyModel.json