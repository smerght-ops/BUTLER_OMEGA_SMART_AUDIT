============================================================
AUTO CAPABILITY REGISTRY
============================================================

Total capabilities detected: 59

## LOCKED CAPABILITIES
The following capabilities have sufficient evidence and are considered implemented:
### Memory
- Evidence count: 521
- file_paths:
  - A_00_ARCHITECTURE/PROJECT_MEMORY_INDEX.json
  - A_00_ARCHIVE_SCRIPTS/memory_manager.txt
  - A_01_CORE/memory_core.py
  - A_01_CORE/memory_guardian.py
  - A_01_CORE/memory_guardian.py.BAK_CLEAN_20260625_121239
  ... and 129 more
- classes:
  - MemoryCore (file: 218)
  - MemoryManager (file: 300)
  - MemoryManager (file: 366)
  - MemoryLoop (file: 447)
  - MemorySidecar (file: 448)
  ... and 17 more
- functions:
  - run_memory_guardian (file: 219)
  - route_memory (file: 1161)
  - rebuild_user_memory (file: 1165)
  - get_memory_summary (file: 1165)
  - rebuild_user_memory (file: 1166)
- imports:
  - A_07_MEMORY.profile_manager (file: 205)
  - A_01_CORE.memory_core (file: 208)
  - A_07_MEMORY.profile_manager (file: 218)
  - A_07_MEMORY.project_context_builder (file: 270)
  - A_04_AGENTS.MemoryDepartment.runner (file: 324)
  ... and 73 more
- calls:
  - MemoryCore (file: 208)
  - build_memory_packet (file: 208)
  - build_memory_packet (file: 218)
  - MemoryCore (file: 218)
  - run_memory_guardian (file: 219)
  ... and 65 more
- link_targets:
  - A_07_MEMORY.profile_manager (type: import)
  - A_01_CORE.memory_core (type: import)
  - A_07_MEMORY.profile_manager (type: import)
  - A_07_MEMORY.project_context_builder (type: import)
  - A_04_AGENTS.MemoryDepartment.runner (type: import)
  ... and 143 more
- dependency_nodes:
  - node: A_07_MEMORY.profile_manager
  - node: A_01_CORE.memory_core
  - node: A_07_MEMORY.project_context_builder
  - node: A_04_AGENTS.MemoryDepartment.runner
  - node: A_07_MEMORY.semantic_memory
  ... and 59 more

### Agent
- Evidence count: 498
- file_paths:
  - A_01_CORE_BACKUP/agent_interface.py
  - A_02_MANAGERS/ArchitectAgent/__init__.py
  - A_02_MANAGERS/ArchitectAgent/architect_agent.py
  - A_02_MANAGERS/ArchitectAgent/architect_agent.py.BAK_BRIDGE
  - A_02_MANAGERS/ArchitectAgent/architect_audit.py
  ... and 181 more
- classes:
  - ArchitectAgent (file: 261)
  - AgentPlanner (file: 393)
  - AgentRouter (file: 394)
  - AgentRouter (file: 395)
  - DispatcherAgent (file: 508)
  ... and 19 more
- imports:
  - A_04_AGENTS.professor (file: 116)
  - A_03_ORCHESTRATION.agent_router (file: 123)
  - A_04_AGENTS.professor (file: 241)
  - architect_agent (file: 260)
  - A_04_AGENTS.CodingDepartment.runner (file: 324)
  ... and 101 more
- calls:
  - DispatcherAgent (file: 116)
  - AgentRouter (file: 123)
  - DispatcherAgent (file: 241)
  - ArchitectAgent (file: 261)
  - AgentPlannerV2 (file: 352)
  ... and 19 more
- link_targets:
  - A_04_AGENTS.professor (type: import)
  - A_03_ORCHESTRATION.agent_router (type: import)
  - A_04_AGENTS.professor (type: import)
  - architect_agent (type: import)
  - A_04_AGENTS.CodingDepartment.runner (type: import)
  ... and 125 more
- dependency_nodes:
  - node: A_04_AGENTS.professor
  - node: A_03_ORCHESTRATION.agent_router
  - node: architect_agent
  - node: A_04_AGENTS.CodingDepartment.runner
  - node: A_04_AGENTS.MemoryDepartment.runner
  ... and 23 more

### Department
- Evidence count: 468
- file_paths:
  - A_02_MANAGERS/department_registry.py
  - A_04_AGENTS/ArchiveDepartment/__init__.py
  - A_04_AGENTS/ArchiveDepartment/runner.py
  - A_04_AGENTS/ArchiveDepartment/runner.py.BAK_4_22_ARCHIVE_STUB
  - A_04_AGENTS/AudioDepartment/__init__.py
  ... and 145 more
- classes:
  - ArchiveDepartment (file: 483)
  - AudioDepartment (file: 486)
  - BaseDepartment (file: 487)
  - CodingDepartment (file: 491)
  - DocumentsDepartment (file: 493)
  ... and 13 more
- imports:
  - A_04_AGENTS.CodingDepartment.runner (file: 324)
  - A_04_AGENTS.MemoryDepartment.runner (file: 324)
  - A_04_AGENTS.VisionDepartment.runner (file: 324)
  - A_04_AGENTS.ImageDepartment.runner (file: 324)
  - A_04_AGENTS.AudioDepartment.runner (file: 324)
  ... and 68 more
- calls:
  - SearchDepartment (file: 324)
  - OpenDocumentDepartment (file: 324)
  - DocumentsDepartment (file: 324)
  - ProjectDocumentationDepartment (file: 324)
  - CodingDepartment (file: 324)
  ... and 58 more
- link_targets:
  - A_04_AGENTS.CodingDepartment.runner (type: import)
  - A_04_AGENTS.MemoryDepartment.runner (type: import)
  - A_04_AGENTS.VisionDepartment.runner (type: import)
  - A_04_AGENTS.ImageDepartment.runner (type: import)
  - A_04_AGENTS.AudioDepartment.runner (type: import)
  ... and 131 more
- dependency_nodes:
  - node: A_04_AGENTS.CodingDepartment.runner
  - node: A_04_AGENTS.MemoryDepartment.runner
  - node: A_04_AGENTS.VisionDepartment.runner
  - node: A_04_AGENTS.ImageDepartment.runner
  - node: A_04_AGENTS.AudioDepartment.runner
  ... and 23 more

### Core
- Evidence count: 338
- file_paths:
  - !!!_CONSTITUTION_SECURITY_CORE.txt
  - A_01_CORE/__init__.py
  - A_01_CORE/alarm.py
  - A_01_CORE/bootstrap_guard.py
  - A_01_CORE/butler_drawer.py
  ... and 179 more
- classes:
  - ChatCoreBridge (file: 205)
  - CoreKernel (file: 207)
  - CoreOrchestrator (file: 208)
  - MemoryCore (file: 218)
  - FactoryCoreBridge (file: 434)
  ... and 4 more
- imports:
  - A_01_CORE.manifest_loader (file: 124)
  - A_01_CORE.manifest_loader (file: 201)
  - A_01_CORE.memory_core (file: 208)
  - A_01_CORE.manifest_loader (file: 212)
  - A_01_CORE.orchestrator (file: 217)
  ... and 41 more
- calls:
  - MemoryCore (file: 208)
  - CoreOrchestrator (file: 208)
  - MemoryCore (file: 218)
  - FrozenCoreGuard (file: 399)
  - CoreOrchestrator (file: 434)
  ... and 9 more
- link_targets:
  - A_01_CORE.manifest_loader (type: import)
  - A_01_CORE.manifest_loader (type: import)
  - A_01_CORE.memory_core (type: import)
  - A_01_CORE.manifest_loader (type: import)
  - A_01_CORE.orchestrator (type: import)
  ... and 55 more
- dependency_nodes:
  - node: A_01_CORE.manifest_loader
  - node: A_01_CORE.memory_core
  - node: A_01_CORE.orchestrator
  - node: A_01_CORE.safety_gate
  - node: A_01_CORE.butler_drawer
  ... and 20 more

### Log
- Evidence count: 310
- file_paths:
  - A_00_ARCHITECTURE/audit.log
  - A_00_ARCHIVE_SCRIPTS/catalog_manager.txt
  - A_01_CORE/logger_config.py
  - A_01_CORE_BACKUP/logger_config.py
  - A_02_MANAGERS/catalog_manager.py
  ... and 79 more
- classes:
  - CatalogManager (file: 285)
  - CatalogManager (file: 364)
  - EngineeringObjectCatalog (file: 522)
  - EngineeringObjectCatalog (file: 577)
  - CatalogSearchBridge (file: 1125)
- functions:
  - log (file: 204)
  - setup_logger (file: 215)
  - write_audit_log (file: 223)
  - log (file: 225)
  - test_catalog_update (file: 236)
  ... and 4 more
- imports:
  - A_02_MANAGERS.catalog_manager (file: 209)
  - logging (file: 214)
  - logging (file: 215)
  - A_02_MANAGERS.catalog_manager (file: 217)
  - A_02_MANAGERS.catalog_manager (file: 221)
  ... and 28 more
- calls:
  - log (file: 204)
  - log (file: 204)
  - log (file: 204)
  - log (file: 204)
  - CatalogManager (file: 209)
  ... and 60 more
- link_targets:
  - A_02_MANAGERS.catalog_manager (type: import)
  - logging (type: import)
  - logging (type: import)
  - A_02_MANAGERS.catalog_manager (type: import)
  - A_02_MANAGERS.catalog_manager (type: import)
  ... and 93 more
- dependency_nodes:
  - node: A_02_MANAGERS.catalog_manager
  - node: logging
  - node: A_01_CORE.logger_config
  - node: engineering_object_catalog
  - node: A_07_MEMORY.catalog_search_bridge
  ... and 11 more

### Runner
- Evidence count: 235
- file_paths:
  - A_02_MANAGERS/TaskRunner/automatic_verifier.py
  - A_02_MANAGERS/TaskRunner/execution_result.py
  - A_02_MANAGERS/TaskRunner/ExecutionAdapters/__init__.py
  - A_02_MANAGERS/TaskRunner/ExecutionAdapters/base_adapter.py
  - A_02_MANAGERS/TaskRunner/ExecutionAdapters/powershell_adapter.py
  ... and 41 more
- classes:
  - TaskRunner (file: 352)
- imports:
  - A_02_MANAGERS.TaskRunner.recipe_writer (file: 305)
  - A_02_MANAGERS.TaskRunner.runner_once (file: 305)
  - A_02_MANAGERS.TaskRunner.recipe_writer (file: 308)
  - A_02_MANAGERS.TaskRunner.recipe_builder (file: 309)
  - A_04_AGENTS.CodingDepartment.runner (file: 324)
  ... and 75 more
- calls:
  - TaskRunner (file: 352)
- link_targets:
  - A_02_MANAGERS.TaskRunner.recipe_writer (type: import)
  - A_02_MANAGERS.TaskRunner.runner_once (type: import)
  - A_02_MANAGERS.TaskRunner.recipe_writer (type: import)
  - A_02_MANAGERS.TaskRunner.recipe_builder (type: import)
  - A_04_AGENTS.CodingDepartment.runner (type: import)
  ... and 76 more
- dependency_nodes:
  - node: A_02_MANAGERS.TaskRunner.recipe_writer
  - node: A_02_MANAGERS.TaskRunner.runner_once
  - node: A_02_MANAGERS.TaskRunner.recipe_builder
  - node: A_04_AGENTS.CodingDepartment.runner
  - node: A_04_AGENTS.MemoryDepartment.runner
  ... and 21 more

### Config
- Evidence count: 186
- file_paths:
  - A_00_ARCHIVE_SCRIPTS/check_config.py
  - A_01_CORE/config_loader.py
  - A_01_CORE/logger_config.py
  - A_01_CORE_BACKUP/config_loader.py
  - A_01_CORE_BACKUP/logger_config.py
  ... and 52 more
- imports:
  - A_07_CONFIG.project_state_v2 (file: 270)
  - A_07_CONFIG.recipe_schema (file: 279)
  - A_07_CONFIG.execution_policy_schema (file: 296)
  - A_07_CONFIG.execution_policy_schema (file: 296)
  - A_07_CONFIG.execution_policy_schema (file: 296)
  ... and 36 more
- calls:
  - reconfigure (file: 210)
  - basicConfig (file: 214)
  - reconfigure (file: 217)
  - reconfigure (file: 217)
  - reconfigure (file: 231)
  ... and 12 more
- link_targets:
  - A_07_CONFIG.project_state_v2 (type: import)
  - A_07_CONFIG.recipe_schema (type: import)
  - A_07_CONFIG.execution_policy_schema (type: import)
  - A_07_CONFIG.execution_policy_schema (type: import)
  - A_07_CONFIG.execution_policy_schema (type: import)
  ... and 53 more
- dependency_nodes:
  - node: A_07_CONFIG.project_state_v2
  - node: A_07_CONFIG.recipe_schema
  - node: A_07_CONFIG.execution_policy_schema
  - node: A_07_CONFIG.task_registry
  - node: A_01_CORE.config_loader
  ... and 8 more

### Task
- Evidence count: 184
- file_paths:
  - A_01_CORE/task_feeder.py
  - A_02_MANAGERS/ArchitectAgent/task_contract_builder.py
  - A_02_MANAGERS/Planner/task_planner.py
  - A_02_MANAGERS/TaskRunner/automatic_verifier.py
  - A_02_MANAGERS/TaskRunner/execution_result.py
  ... and 27 more
- classes:
  - TaskFeeder (file: 235)
  - TaskContractBuilder (file: 281)
  - TaskPlanner (file: 309)
  - TaskRunner (file: 352)
- functions:
  - run_guarded_task (file: 1420)
- imports:
  - task_contract_builder (file: 263)
  - task_contract_builder (file: 264)
  - task_contract_builder (file: 266)
  - task_contract_builder (file: 267)
  - task_contract_builder (file: 276)
  ... and 27 more
- calls:
  - fetch_task (file: 211)
  - fetch_task (file: 235)
  - TaskFeeder (file: 235)
  - TaskContractBuilder (file: 263)
  - TaskContractBuilder (file: 264)
  ... and 24 more
- link_targets:
  - task_contract_builder (type: import)
  - task_contract_builder (type: import)
  - task_contract_builder (type: import)
  - task_contract_builder (type: import)
  - task_contract_builder (type: import)
  ... and 56 more
- dependency_nodes:
  - node: task_contract_builder
  - node: A_02_MANAGERS.Planner.task_planner
  - node: A_02_MANAGERS.TaskRunner.recipe_writer
  - node: A_02_MANAGERS.TaskRunner.runner_once
  - node: A_02_MANAGERS.TaskRunner.recipe_builder
  ... and 20 more

### Recipe
- Evidence count: 179
- file_paths:
  - A_02_MANAGERS/ArchitectAgent/recipe_builder.py
  - A_02_MANAGERS/ArchitectAgent/recipe_generator.py
  - A_02_MANAGERS/recipe_generator.py
  - A_02_MANAGERS/recipe_validator.py
  - A_02_MANAGERS/TaskRunner/recipe_builder.py
  ... and 11 more
- classes:
  - RecipeBuilder (file: 279)
  - RecipeGenerator (file: 280)
  - RecipeGenerator (file: 317)
  - RecipeValidator (file: 318)
  - RecipeBuilder (file: 347)
  ... and 6 more
- imports:
  - recipe_builder (file: 261)
  - recipe_generator (file: 263)
  - recipe_generator (file: 264)
  - recipe_generator (file: 266)
  - recipe_generator (file: 267)
  ... and 28 more
- calls:
  - RecipeBuilder (file: 261)
  - build_planning_recipe (file: 261)
  - RecipeGenerator (file: 263)
  - RecipeGenerator (file: 264)
  - RecipeGenerator (file: 266)
  ... and 28 more
- link_targets:
  - recipe_builder (type: import)
  - recipe_generator (type: import)
  - recipe_generator (type: import)
  - recipe_generator (type: import)
  - recipe_generator (type: import)
  ... and 61 more
- dependency_nodes:
  - node: recipe_builder
  - node: recipe_generator
  - node: A_07_CONFIG.recipe_schema
  - node: A_02_MANAGERS.TaskRunner.recipe_writer
  - node: A_02_MANAGERS.TaskRunner.recipe_builder
  ... and 15 more

### Semantic
- Evidence count: 169
- file_paths:
  - A_02_MANAGERS/smart_dispatcher_v2.py.BAK_SEMANTIC_CONTEXT
  - A_03_ORCHESTRATION/semantic_layer.py
  - A_04_AGENTS/SearchDepartment/runner.py.BAK_SEMANTIC_CONTEXT
  - A_06_WORKSPACE/ARCHIVE_DONE/semantic_memory_test.txt
  - A_07_MEMORY/semantic_compression.py
  ... and 27 more
- classes:
  - SemanticLayer (file: 471)
  - SemanticSearchEngine (file: 1173)
  - SemanticCompressor (file: 1176)
  - SemanticConstraintLayer (file: 1177)
  - SemanticCore (file: 1179)
  ... and 6 more
- imports:
  - A_03_ORCHESTRATION.semantic_layer (file: 205)
  - A_03_ORCHESTRATION.semantic_layer (file: 207)
  - A_03_ORCHESTRATION.semantic_layer (file: 208)
  - A_07_MEMORY.semantic_memory (file: 324)
  - A_07_MEMORY.semantic_reasoning_engine (file: 324)
  ... and 16 more
- calls:
  - SemanticLayer (file: 205)
  - SemanticLayer (file: 207)
  - SemanticLayer (file: 208)
  - SemanticMemory (file: 324)
  - SemanticReasoningEngine (file: 324)
  ... and 27 more
- link_targets:
  - A_03_ORCHESTRATION.semantic_layer (type: import)
  - A_03_ORCHESTRATION.semantic_layer (type: import)
  - A_03_ORCHESTRATION.semantic_layer (type: import)
  - A_07_MEMORY.semantic_memory (type: import)
  - A_07_MEMORY.semantic_reasoning_engine (type: import)
  ... and 48 more
- dependency_nodes:
  - node: A_03_ORCHESTRATION.semantic_layer
  - node: A_07_MEMORY.semantic_memory
  - node: A_07_MEMORY.semantic_reasoning_engine
  - node: A_07_MEMORY.semantic_compression
  - node: A_07_MEMORY.semantic_reasoning_engine_v2
  ... and 15 more

### Registry
- Evidence count: 164
- file_paths:
  - A_02_MANAGERS/department_registry.py
  - A_02_MANAGERS/ExecutionPolicyEngine/policy_registry.py
  - A_02_MANAGERS/model_registry.py
  - A_02_MANAGERS/RuntimeCapabilityRegistry/capability_schema.py
  - A_02_MANAGERS/RuntimeCapabilityRegistry/runtime_registry.py
  ... and 26 more
- classes:
  - PolicyRegistry (file: 297)
  - RuntimeCapabilityRegistry (file: 320)
  - HandlerRegistry (file: 387)
  - RegistryBrain (file: 466)
  - RouterRegistry (file: 469)
  ... and 14 more
- imports:
  - A_03_ORCHESTRATION.router_registry (file: 123)
  - A_07_CONFIG.task_registry (file: 317)
  - A_02_MANAGERS.RuntimeCapabilityRegistry.capability_schema (file: 320)
  - A_07_CONFIG.task_registry (file: 352)
  - A_03_ORCHESTRATION.router_registry (file: 467)
  ... and 14 more
- calls:
  - RouterRegistry (file: 123)
  - HandlerRegistry (file: 387)
  - RegistryBrain (file: 466)
  - RouterRegistry (file: 467)
  - RouterRegistry (file: 468)
  ... and 22 more
- link_targets:
  - A_03_ORCHESTRATION.router_registry (type: import)
  - A_07_CONFIG.task_registry (type: import)
  - A_02_MANAGERS.RuntimeCapabilityRegistry.capability_schema (type: import)
  - A_07_CONFIG.task_registry (type: import)
  - A_03_ORCHESTRATION.router_registry (type: import)
  ... and 41 more
- dependency_nodes:
  - node: A_03_ORCHESTRATION.router_registry
  - node: A_07_CONFIG.task_registry
  - node: A_02_MANAGERS.RuntimeCapabilityRegistry.capability_schema
  - node: A_03_HANDLERS.registry
  - node: registry_scanner
  ... and 17 more

### Check
- Evidence count: 153
- file_paths:
  - A_00_ARCHITECTURE/DAILY_START_CHECKLIST.md
  - A_00_ARCHIVE_SCRIPTS/check_config.py
  - A_01_CORE/healthcheck.py
  - A_01_CORE_BACKUP/healthcheck.py
  - A_02_MANAGERS/ArchitectAgent/architect_release_check.py
  ... and 6 more
- functions:
  - check_system (file: 214)
  - check_code_layer (file: 219)
  - check_system (file: 248)
  - check_comfyui (file: 409)
  - check_comfyui (file: 410)
  ... and 13 more
- calls:
  - check_system (file: 214)
  - check_code_layer (file: 219)
  - check_ollama_status (file: 231)
  - check_loop (file: 234)
  - health_check (file: 234)
  ... and 48 more
- link_targets:
  - check_system (type: call)
  - check_code_layer (type: call)
  - check_ollama_status (type: call)
  - check_loop (type: call)
  - health_check (type: call)
  ... and 48 more
- dependency_nodes:
  - node: check_system
  - node: check_code_layer
  - node: check_ollama_status
  - node: check_loop
  - node: health_check
  ... and 13 more

### Catalog
- Evidence count: 149
- file_paths:
  - A_00_ARCHIVE_SCRIPTS/catalog_manager.txt
  - A_02_MANAGERS/catalog_manager.py
  - A_02_MANAGERS/catalog_manager.py.BAK_4_26_SMART_SEARCH
  - A_02_MANAGERS/catalog_manager.py.BAK_4_27_SMART_SEARCH
  - A_02_MANAGERS/catalog_manager.py.BAK_4_27_SUMMARY_TAGS
  ... and 14 more
- classes:
  - CatalogManager (file: 285)
  - CatalogManager (file: 364)
  - EngineeringObjectCatalog (file: 522)
  - EngineeringObjectCatalog (file: 577)
  - CatalogSearchBridge (file: 1125)
- functions:
  - test_catalog_update (file: 236)
  - test_catalog_update (file: 257)
  - show_catalog (file: 1455)
- imports:
  - A_02_MANAGERS.catalog_manager (file: 209)
  - A_02_MANAGERS.catalog_manager (file: 217)
  - A_02_MANAGERS.catalog_manager (file: 221)
  - A_02_MANAGERS.catalog_manager (file: 231)
  - A_02_MANAGERS.catalog_manager (file: 236)
  ... and 20 more
- calls:
  - CatalogManager (file: 209)
  - CatalogManager (file: 217)
  - CatalogManager (file: 221)
  - CatalogManager (file: 231)
  - CatalogManager (file: 236)
  ... and 27 more
- link_targets:
  - A_02_MANAGERS.catalog_manager (type: import)
  - A_02_MANAGERS.catalog_manager (type: import)
  - A_02_MANAGERS.catalog_manager (type: import)
  - A_02_MANAGERS.catalog_manager (type: import)
  - A_02_MANAGERS.catalog_manager (type: import)
  ... and 52 more
- dependency_nodes:
  - node: A_02_MANAGERS.catalog_manager
  - node: engineering_object_catalog
  - node: A_07_MEMORY.catalog_search_bridge
  - node: CatalogManager
  - node: test_catalog_update
  ... and 3 more

### Passport
- Evidence count: 140
- file_paths:
  - A_03_ORCHESTRATION/passport_commands.py
  - A_03_ORCHESTRATION/passport_commands.py.BACKUP_BEFORE_FACADE
  - A_03_ORCHESTRATION/passport_commands.py.BACKUP_MEMORY_FACADE
  - A_03_ORCHESTRATION/passport_commands.py.bak_20260623_125058
  - A_03_ORCHESTRATION/passport_commands.py.bak_20260623_132219
  ... and 29 more
- classes:
  - PassportCommandHandler (file: 453)
  - PassportDiscoveryAgent (file: 530)
  - PassportScanner (file: 556)
  - PassportDiscoveryAgent (file: 585)
  - PassportScanner (file: 604)
  ... and 2 more
- imports:
  - A_03_ORCHESTRATION.passport_commands (file: 123)
  - A_07_CONFIG.project_passport_loader (file: 399)
  - A_07_CONFIG.project_passport_loader (file: 405)
  - A_03_ORCHESTRATION.passport_commands (file: 467)
  - A_03_ORCHESTRATION.passport_commands (file: 468)
  ... and 7 more
- calls:
  - PassportCommandHandler (file: 123)
  - ProjectPassportLoader (file: 399)
  - ProjectPassportLoader (file: 405)
  - load_passport (file: 405)
  - passport_summary (file: 405)
  ... and 26 more
- link_targets:
  - A_03_ORCHESTRATION.passport_commands (type: import)
  - A_07_CONFIG.project_passport_loader (type: import)
  - A_07_CONFIG.project_passport_loader (type: import)
  - A_03_ORCHESTRATION.passport_commands (type: import)
  - A_03_ORCHESTRATION.passport_commands (type: import)
  ... and 38 more
- dependency_nodes:
  - node: A_03_ORCHESTRATION.passport_commands
  - node: A_07_CONFIG.project_passport_loader
  - node: passport_scanner
  - node: A_07_CONFIG.passport_report
  - node: PassportCommandHandler
  ... and 8 more

### Image
- Evidence count: 132
- file_paths:
  - A_03_HANDLERS/image_handler.py
  - A_03_ORCHESTRATION/ConversationContext/ImageSession/__init__.py
  - A_03_ORCHESTRATION/ConversationContext/ImageSession/image_session.py
  - A_04_AGENTS/ImageDepartment/__init__.py
  - A_04_AGENTS/ImageDepartment/runner.py
  ... and 55 more
- classes:
  - ImageHandler (file: 382)
  - ImageSession (file: 428)
  - ImageDepartment (file: 499)
  - ImageDepartment (file: 1389)
- functions:
  - process_image (file: 373)
- imports:
  - A_04_AGENTS.ImageDepartment.runner (file: 324)
  - A_04_AGENTS.ImageDepartment.runner (file: 338)
  - A_03_HANDLERS.image_handler (file: 387)
  - A_04_AGENTS.ImageDepartment.runner (file: 414)
  - A_03_ORCHESTRATION.ConversationContext.ImageSession.image_session (file: 426)
  ... and 6 more
- calls:
  - ImageDepartment (file: 324)
  - ImageDepartment (file: 338)
  - generate_image (file: 371)
  - image_to_string (file: 383)
  - ImageHandler (file: 387)
  ... and 12 more
- link_targets:
  - A_04_AGENTS.ImageDepartment.runner (type: import)
  - A_04_AGENTS.ImageDepartment.runner (type: import)
  - A_03_HANDLERS.image_handler (type: import)
  - A_04_AGENTS.ImageDepartment.runner (type: import)
  - A_03_ORCHESTRATION.ConversationContext.ImageSession.image_session (type: import)
  ... and 23 more
- dependency_nodes:
  - node: A_04_AGENTS.ImageDepartment.runner
  - node: A_03_HANDLERS.image_handler
  - node: A_03_ORCHESTRATION.ConversationContext.ImageSession.image_session
  - node: ImageDepartment
  - node: generate_image
  ... and 6 more

### Search
- Evidence count: 124
- file_paths:
  - A_02_MANAGERS/catalog_manager.py.BAK_4_26_SMART_SEARCH
  - A_02_MANAGERS/catalog_manager.py.BAK_4_27_SMART_SEARCH
  - A_04_AGENTS/SearchDepartment/runner.py
  - A_04_AGENTS/SearchDepartment/runner.py.BAK_SEMANTIC_CONTEXT
  - A_07_CONFIG/project_passport.json.BAK_4_23_SEARCH_LAYER_20260625
  ... and 15 more
- classes:
  - SearchDepartment (file: 616)
  - CatalogSearchBridge (file: 1125)
  - SemanticSearchEngine (file: 1173)
- imports:
  - A_04_AGENTS.SearchDepartment.runner (file: 324)
  - A_07_MEMORY.catalog_search_bridge (file: 616)
  - A_07_MEMORY.search_engine (file: 1141)
  - A_04_AGENTS.SearchDepartment.runner (file: 1285)
  - A_04_AGENTS.SearchDepartment.runner (file: 1287)
  ... and 3 more
- calls:
  - full_text_search (file: 209)
  - test_fts5_search (file: 209)
  - full_text_search (file: 217)
  - rebuild_search_index (file: 217)
  - full_text_search (file: 241)
  ... and 30 more
- link_targets:
  - A_04_AGENTS.SearchDepartment.runner (type: import)
  - A_07_MEMORY.catalog_search_bridge (type: import)
  - A_07_MEMORY.search_engine (type: import)
  - A_04_AGENTS.SearchDepartment.runner (type: import)
  - A_04_AGENTS.SearchDepartment.runner (type: import)
  ... and 38 more
- dependency_nodes:
  - node: A_04_AGENTS.SearchDepartment.runner
  - node: A_07_MEMORY.catalog_search_bridge
  - node: A_07_MEMORY.search_engine
  - node: full_text_search
  - node: test_fts5_search
  ... and 10 more

### Dispatcher
- Evidence count: 118
- file_paths:
  - A_02_MANAGERS/smart_dispatcher.py
  - A_02_MANAGERS/smart_dispatcher.py.pre_guarded_write_backup
  - A_02_MANAGERS/smart_dispatcher_v2.py
  - A_02_MANAGERS/smart_dispatcher_v2.py.BAK_4_26_DOCUMENTS_BRIDGE
  - A_02_MANAGERS/smart_dispatcher_v2.py.BAK_DOCTOR_DISPATCH
  ... and 23 more
- classes:
  - FakeDispatcher (file: 291)
  - SmartDispatcher (file: 322)
  - SmartDispatcherV2 (file: 324)
  - SmartDispatcherV2 (file: 338)
  - Dispatcher (file: 365)
  ... and 8 more
- imports:
  - A_02_MANAGERS.smart_dispatcher (file: 227)
  - A_03_ORCHESTRATION.dispatcher_bridge_v2 (file: 414)
  - A_02_MANAGERS.smart_dispatcher_v2 (file: 430)
  - A_02_MANAGERS.smart_dispatcher_v2 (file: 534)
  - A_02_MANAGERS.smart_dispatcher_v2 (file: 549)
  ... and 7 more
- registrations:
  - Dispatcher (file: 365)
- calls:
  - DispatcherAgent (file: 116)
  - SmartDispatcher (file: 227)
  - DispatcherAgent (file: 241)
  - FakeDispatcher (file: 291)
  - SmartDispatcherV2 (file: 324)
  ... and 16 more
- link_targets:
  - A_02_MANAGERS.smart_dispatcher (type: import)
  - A_03_ORCHESTRATION.dispatcher_bridge_v2 (type: import)
  - A_02_MANAGERS.smart_dispatcher_v2 (type: import)
  - A_02_MANAGERS.smart_dispatcher_v2 (type: import)
  - A_02_MANAGERS.smart_dispatcher_v2 (type: import)
  ... and 29 more
- dependency_nodes:
  - node: A_02_MANAGERS.smart_dispatcher
  - node: A_03_ORCHESTRATION.dispatcher_bridge_v2
  - node: A_02_MANAGERS.smart_dispatcher_v2
  - node: DispatcherAgent
  - node: SmartDispatcher
  ... and 4 more

### Router
- Evidence count: 114
- file_paths:
  - A_00_BACKUPS/router_integration_STAGE_4_11_3_20260620_144201.py
  - A_02_MANAGERS/smart_dispatcher_v2.py.BAK_REASONING_ROUTER
  - A_03_ORCHESTRATION/agent_router.BAK_20260623_113044.py
  - A_03_ORCHESTRATION/agent_router.py
  - A_03_ORCHESTRATION/agent_router.py.BAK_UTF8_GARBAGE_20260705_183143
  ... and 26 more
- classes:
  - RouterIntegration (file: 123)
  - AgentRouter (file: 394)
  - AgentRouter (file: 395)
  - ChatRouterMirror (file: 419)
  - RouterIntegration (file: 467)
  ... and 4 more
- imports:
  - A_03_ORCHESTRATION.agent_router (file: 123)
  - A_03_ORCHESTRATION.router_registry (file: 123)
  - A_03_ORCHESTRATION.router_integration (file: 414)
  - A_03_ORCHESTRATION.router_integration (file: 417)
  - A_03_ORCHESTRATION.agent_router (file: 467)
  ... and 7 more
- calls:
  - AgentRouter (file: 123)
  - RouterRegistry (file: 123)
  - RouterIntegration (file: 123)
  - AgentRouter (file: 394)
  - AgentRouter (file: 395)
  ... and 16 more
- link_targets:
  - A_03_ORCHESTRATION.agent_router (type: import)
  - A_03_ORCHESTRATION.router_registry (type: import)
  - A_03_ORCHESTRATION.router_integration (type: import)
  - A_03_ORCHESTRATION.router_integration (type: import)
  - A_03_ORCHESTRATION.agent_router (type: import)
  ... and 28 more
- dependency_nodes:
  - node: A_03_ORCHESTRATION.agent_router
  - node: A_03_ORCHESTRATION.router_registry
  - node: A_03_ORCHESTRATION.router_integration
  - node: AgentRouter
  - node: RouterRegistry
  ... and 3 more

### Generate
- Evidence count: 96
- file_paths:
  - A_06_WORKSPACE/GENERATED_IMAGES/BUTLER_OMEGA_SMART_00009_.png
  - A_06_WORKSPACE/GENERATED_IMAGES/BUTLER_OMEGA_SMART_00010_.png
  - A_06_WORKSPACE/GENERATED_IMAGES/BUTLER_OMEGA_SMART_00011_.png
  - A_06_WORKSPACE/GENERATED_IMAGES/BUTLER_OMEGA_SMART_00012_.png
  - A_06_WORKSPACE/GENERATED_IMAGES/BUTLER_OMEGA_SMART_00013_.png
  ... and 43 more
- functions:
  - generate_plan (file: 254)
  - generate_report (file: 283)
  - generate_report (file: 363)
- calls:
  - generate_plan (file: 254)
  - generate (file: 263)
  - generate (file: 264)
  - generate (file: 266)
  - generate (file: 267)
  ... and 15 more
- link_targets:
  - generate_plan (type: call)
  - generate (type: call)
  - generate (type: call)
  - generate (type: call)
  - generate (type: call)
  ... and 15 more
- dependency_nodes:
  - node: generate_plan
  - node: generate
  - node: generate_report
  - node: generate_image
  - node: generate_content

### Builder
- Evidence count: 88
- file_paths:
  - A_01_CORE/project_state_builder.py
  - A_02_MANAGERS/ArchitectAgent/recipe_builder.py
  - A_02_MANAGERS/ArchitectAgent/task_contract_builder.py
  - A_02_MANAGERS/context_builder.py
  - A_02_MANAGERS/TaskRunner/recipe_builder.py
  ... and 11 more
- classes:
  - RecipeBuilder (file: 279)
  - TaskContractBuilder (file: 281)
  - RecipeBuilder (file: 347)
  - ButlerContextBuilder (file: 422)
  - ProjectContextBuilder (file: 619)
  ... and 1 more
- imports:
  - recipe_builder (file: 261)
  - task_contract_builder (file: 263)
  - task_contract_builder (file: 264)
  - task_contract_builder (file: 266)
  - task_contract_builder (file: 267)
  ... and 8 more
- calls:
  - RecipeBuilder (file: 261)
  - TaskContractBuilder (file: 263)
  - TaskContractBuilder (file: 264)
  - TaskContractBuilder (file: 266)
  - TaskContractBuilder (file: 267)
  ... and 10 more
- link_targets:
  - recipe_builder (type: import)
  - task_contract_builder (type: import)
  - task_contract_builder (type: import)
  - task_contract_builder (type: import)
  - task_contract_builder (type: import)
  ... and 23 more
- dependency_nodes:
  - node: recipe_builder
  - node: task_contract_builder
  - node: A_07_MEMORY.project_context_builder
  - node: A_02_MANAGERS.TaskRunner.recipe_builder
  - node: A_03_ORCHESTRATION.context_builder
  ... and 5 more

### Archive
- Evidence count: 85
- file_paths:
  - A_00_ARCHIVE_SCRIPTS/catalog_manager.txt
  - A_00_ARCHIVE_SCRIPTS/check_config.py
  - A_00_ARCHIVE_SCRIPTS/memory_manager.txt
  - A_00_ARCHIVE_SCRIPTS/project_tree.txt
  - A_00_ARCHIVE_SCRIPTS/requeue.py
  ... and 33 more
- classes:
  - Archiver (file: 282)
  - Archiver (file: 362)
  - ArchiveHandler (file: 377)
  - ArchiveDepartment (file: 483)
- imports:
  - A_04_AGENTS.ArchiveDepartment.runner (file: 324)
  - A_04_AGENTS.ArchiveDepartment.runner (file: 338)
  - A_03_HANDLERS.archive_handler (file: 387)
  - A_03_HANDLERS.archive_handler (file: 483)
  - A_04_AGENTS.ArchiveDepartment.runner (file: 1285)
  ... and 2 more
- calls:
  - Archiver (file: 282)
  - ArchiveDepartment (file: 324)
  - ArchiveDepartment (file: 338)
  - Archiver (file: 362)
  - ArchiveHandler (file: 387)
  ... and 6 more
- link_targets:
  - A_04_AGENTS.ArchiveDepartment.runner (type: import)
  - A_04_AGENTS.ArchiveDepartment.runner (type: import)
  - A_03_HANDLERS.archive_handler (type: import)
  - A_03_HANDLERS.archive_handler (type: import)
  - A_04_AGENTS.ArchiveDepartment.runner (type: import)
  ... and 13 more
- dependency_nodes:
  - node: A_04_AGENTS.ArchiveDepartment.runner
  - node: A_03_HANDLERS.archive_handler
  - node: Archiver
  - node: ArchiveDepartment
  - node: ArchiveHandler
  ... and 2 more

### Manifest
- Evidence count: 83
- file_paths:
  - A_00_ARCHIVE_SCRIPTS/system_manifest.txt
  - A_01_CORE/manifest_loader.py
  - A_01_CORE_BACKUP/manifest_loader.py
  - A_02_MANAGERS/ArchitectAgent/architect_manifest.py
  - A_07_CONFIG/llm_context_manifest.json
  ... and 9 more
- classes:
  - ManifestLoader (file: 216)
  - ManifestLoader (file: 250)
- functions:
  - load_manifest (file: 206)
  - verify_lock_manifest (file: 219)
  - rebuild_lock_manifest (file: 223)
  - load_manifest (file: 244)
- imports:
  - A_01_CORE.manifest_loader (file: 124)
  - A_01_CORE.manifest_loader (file: 201)
  - A_01_CORE.manifest_loader (file: 212)
  - A_01_CORE.manifest_loader (file: 224)
  - A_01_CORE.manifest_loader (file: 231)
  ... and 17 more
- calls:
  - load_manifest (file: 206)
  - verify_lock_manifest (file: 219)
  - rebuild_lock_manifest (file: 223)
  - rebuild_lock_manifest (file: 223)
  - load_manifest (file: 244)
  ... and 2 more
- link_targets:
  - A_01_CORE.manifest_loader (type: import)
  - A_01_CORE.manifest_loader (type: import)
  - A_01_CORE.manifest_loader (type: import)
  - A_01_CORE.manifest_loader (type: import)
  - A_01_CORE.manifest_loader (type: import)
  ... and 24 more
- dependency_nodes:
  - node: A_01_CORE.manifest_loader
  - node: load_manifest
  - node: verify_lock_manifest
  - node: rebuild_lock_manifest
  - node: inspect_manifest_models

### Vision
- Evidence count: 82
- file_paths:
  - A_03_ENGINES/Vision_Engine/__init__.py
  - A_03_ENGINES/Vision_Engine/GO.py
  - A_03_ENGINES/Vision_Engine/vision_tool.py
  - A_03_HANDLERS/ollama_vision_backend.py
  - A_03_HANDLERS/vision_analyzer.py
  ... and 7 more
- classes:
  - OllamaVisionBackend (file: 384)
  - VisionAnalyzer (file: 390)
  - VisionEngine (file: 391)
  - VisionDepartment (file: 625)
- imports:
  - A_04_AGENTS.VisionDepartment.runner (file: 324)
  - A_04_AGENTS.VisionDepartment.runner (file: 338)
  - A_03_HANDLERS.vision_engine (file: 382)
  - A_03_HANDLERS.vision_engine (file: 385)
  - A_03_HANDLERS.vision_engine (file: 386)
  ... and 9 more
- calls:
  - VisionDepartment (file: 324)
  - VisionDepartment (file: 338)
  - VisionEngine (file: 382)
  - _extract_scanned_pdf_with_vision (file: 385)
  - VisionEngine (file: 385)
  ... and 9 more
- link_targets:
  - A_04_AGENTS.VisionDepartment.runner (type: import)
  - A_04_AGENTS.VisionDepartment.runner (type: import)
  - A_03_HANDLERS.vision_engine (type: import)
  - A_03_HANDLERS.vision_engine (type: import)
  - A_03_HANDLERS.vision_engine (type: import)
  ... and 23 more
- dependency_nodes:
  - node: A_04_AGENTS.VisionDepartment.runner
  - node: A_03_HANDLERS.vision_engine
  - node: A_03_HANDLERS.ollama_vision_backend
  - node: A_03_ENGINES.Vision_Engine.GO
  - node: A_03_HANDLERS.vision_analyzer
  ... and 5 more

### Comfy
- Evidence count: 82
- file_paths:
  - A_03_ENGINES/Generation_Engine/comfy_bridge.py
  - A_06_WORKSPACE/exports/last_comfy_negative.txt
  - A_06_WORKSPACE/exports/last_comfy_positive.txt
  - A_06_WORKSPACE/exports/last_comfy_prompt.txt
  - A_07_CONFIG/comfy_api_autodiscovered.json
  ... and 4 more
- classes:
  - ComfyUIBridge (file: 371)
- functions:
  - check_comfyui (file: 409)
  - check_comfyui (file: 410)
  - check_comfyui (file: 411)
  - check_comfyui (file: 412)
  - check_comfyui (file: 413)
  ... and 7 more
- imports:
  - A_03_ENGINES.Generation_Engine.comfy_bridge (file: 408)
- calls:
  - check_comfy_status (file: 371)
  - ComfyUIBridge (file: 371)
  - ComfyUIBridge (file: 408)
  - check_comfyui (file: 409)
  - check_comfyui (file: 409)
  ... and 22 more
- link_targets:
  - A_03_ENGINES.Generation_Engine.comfy_bridge (type: import)
  - check_comfy_status (type: call)
  - ComfyUIBridge (type: call)
  - ComfyUIBridge (type: call)
  - check_comfyui (type: call)
  ... and 23 more
- dependency_nodes:
  - node: A_03_ENGINES.Generation_Engine.comfy_bridge
  - node: check_comfy_status
  - node: ComfyUIBridge
  - node: check_comfyui

### Report
- Evidence count: 82
- file_paths:
  - A_01_CORE_BACKUP/register_report.py
  - A_02_MANAGERS/audit_reporter.py
  - A_02_MANAGERS/audit_reporter.py.BAK_FIX_WRITE_20260628
  - A_02_MANAGERS_BACKUP/audit_reporter.py
  - A_03_ORCHESTRATION/passport_commands.py.BAK_PASSPORT_REPORT_20260627
  ... and 25 more
- classes:
  - ReportsScanner (file: 559)
  - ReportsScanner (file: 607)
  - PassportReport (file: 1088)
- functions:
  - process_report (file: 255)
  - generate_report (file: 283)
  - generate_report (file: 363)
- imports:
  - reports_scanner (file: 536)
  - A_02_MANAGERS.audit_reporter (file: 548)
  - reports_scanner (file: 591)
  - A_02_MANAGERS.audit_reporter (file: 596)
  - A_07_CONFIG.passport_report (file: 1145)
  ... and 1 more
- calls:
  - process_report (file: 255)
  - generate_report (file: 283)
  - generate_report (file: 363)
  - ReportsScanner (file: 536)
  - generate_report (file: 548)
  ... and 8 more
- link_targets:
  - reports_scanner (type: import)
  - A_02_MANAGERS.audit_reporter (type: import)
  - reports_scanner (type: import)
  - A_02_MANAGERS.audit_reporter (type: import)
  - A_07_CONFIG.passport_report (type: import)
  ... and 14 more
- dependency_nodes:
  - node: reports_scanner
  - node: A_02_MANAGERS.audit_reporter
  - node: A_07_CONFIG.passport_report
  - node: process_report
  - node: generate_report
  ... and 3 more

### Guardian
- Evidence count: 79
- file_paths:
  - A_01_CORE/memory_guardian.py
  - A_01_CORE/memory_guardian.py.BAK_CLEAN_20260625_121239
  - A_01_CORE/system_guardian.py
  - A_01_CORE/system_guardian.py.BAK_TEXT
  - A_01_CORE/system_guardian.py.CURED_BAK
  ... and 57 more
- functions:
  - run_memory_guardian (file: 219)
  - run_guardian (file: 231)
- imports:
  - A_01_CORE.memory_guardian (file: 1486)
- calls:
  - run_memory_guardian (file: 219)
  - run_guardian (file: 231)
  - run_memory_guardian (file: 1486)
  - run_memory_guardian (file: 1486)
  - run_memory_guardian (file: 1486)
- link_targets:
  - A_01_CORE.memory_guardian (type: import)
  - run_memory_guardian (type: call)
  - run_guardian (type: call)
  - run_memory_guardian (type: call)
  - run_memory_guardian (type: call)
  ... and 1 more
- dependency_nodes:
  - node: A_01_CORE.memory_guardian
  - node: run_memory_guardian
  - node: run_guardian

### History
- Evidence count: 77
- file_paths:
  - A_02_MANAGERS/ExecutionMonitor/execution_history.py
  - A_04_AGENTS/ProjectDocumentationDepartment/Core/Scanners/history_scanner.py
  - A_04_AGENTS/ProjectDocumentationDepartment/Core_BACKUP_UTF8SIG/Scanners/history_scanner.py
  - A_05_STORAGE/session_history.jsonl
  - A_05_STORAGE/session_history.jsonl.bad_backup_20260612_193723.jsonl
  ... and 5 more
- classes:
  - ExecutionHistory (file: 292)
  - HistoryScanner (file: 553)
  - HistoryScanner (file: 601)
  - ProjectHistory (file: 1169)
- imports:
  - A_02_MANAGERS.ExecutionMonitor.execution_history (file: 294)
  - A_07_MEMORY.project_history (file: 453)
  - history_scanner (file: 536)
  - A_07_MEMORY.project_history (file: 553)
  - history_scanner (file: 591)
  ... and 4 more
- calls:
  - ProjectHistory (file: 453)
  - HistoryScanner (file: 536)
  - ProjectHistory (file: 553)
  - HistoryScanner (file: 553)
  - HistoryScanner (file: 591)
  ... and 14 more
- link_targets:
  - A_02_MANAGERS.ExecutionMonitor.execution_history (type: import)
  - A_07_MEMORY.project_history (type: import)
  - history_scanner (type: import)
  - A_07_MEMORY.project_history (type: import)
  - history_scanner (type: import)
  ... and 23 more
- dependency_nodes:
  - node: A_02_MANAGERS.ExecutionMonitor.execution_history
  - node: A_07_MEMORY.project_history
  - node: history_scanner
  - node: ProjectHistory
  - node: HistoryScanner
  ... and 2 more

### Runtime
- Evidence count: 76
- file_paths:
  - A_00_ARCHITECTURE/CHANGE_REQUESTS/CR_RUNTIME_AUTOMATION.json
  - A_02_MANAGERS/RuntimeCapabilityRegistry/capability_schema.py
  - A_02_MANAGERS/RuntimeCapabilityRegistry/runtime_registry.py
  - A_04_AGENTS/ProjectDocumentationDepartment/Core/Discovery/runtime_departments_discovery_agent.py
  - A_04_AGENTS/ProjectDocumentationDepartment/Core_BACKUP_UTF8SIG/Discovery/runtime_departments_discovery_agent.py
  ... and 3 more
- classes:
  - RuntimeCapability (file: 319)
  - RuntimeCapabilityRegistry (file: 320)
  - RuntimeDepartmentsDiscoveryAgent (file: 534)
  - RuntimeDepartmentsDiscoveryAgent (file: 589)
- imports:
  - A_02_MANAGERS.RuntimeCapabilityRegistry.capability_schema (file: 320)
  - A_02_MANAGERS.RuntimeCapabilityRegistry.runtime_registry (file: 1081)
- calls:
  - RuntimeError (file: 279)
  - RuntimeError (file: 317)
  - RuntimeError (file: 317)
  - RuntimeCapability (file: 319)
  - RuntimeCapability (file: 320)
  ... and 23 more
- link_targets:
  - A_02_MANAGERS.RuntimeCapabilityRegistry.capability_schema (type: import)
  - A_02_MANAGERS.RuntimeCapabilityRegistry.runtime_registry (type: import)
  - RuntimeError (type: call)
  - RuntimeError (type: call)
  - RuntimeError (type: call)
  ... and 25 more
- dependency_nodes:
  - node: A_02_MANAGERS.RuntimeCapabilityRegistry.capability_schema
  - node: A_02_MANAGERS.RuntimeCapabilityRegistry.runtime_registry
  - node: RuntimeError
  - node: RuntimeCapability

### Loop
- Evidence count: 74
- file_paths:
  - A_01_CORE/execution_loop.py
  - A_01_CORE/self_healing_loop.py
  - A_01_CORE/self_healing_loop.py.backup_20260615_094811
  - A_01_CORE/self_healing_loop.py.pre_guarded_write_backup
  - A_02_MANAGERS/TaskRunner/runner_loop.py
  ... and 12 more
- classes:
  - ExecutionLoop (file: 211)
  - AntiLoopBudget (file: 397)
  - AutonomousLoop (file: 398)
  - MemoryLoop (file: 447)
  - AgentLoopExecutor (file: 1114)
  ... and 3 more
- imports:
  - A_07_MEMORY.goal_loop_engine (file: 1117)
  - A_07_MEMORY.goal_loop_engine (file: 1118)
  - A_03_ORCHESTRATION.anti_loop_budget (file: 1338)
  - A_01_CORE.execution_loop (file: 1495)
  - A_01_CORE.execution_loop (file: 1505)
- calls:
  - mainloop (file: 204)
  - ExecutionLoop (file: 211)
  - check_loop (file: 234)
  - AutonomousLoop (file: 398)
  - MemoryLoop (file: 447)
  ... and 8 more
- link_targets:
  - A_07_MEMORY.goal_loop_engine (type: import)
  - A_07_MEMORY.goal_loop_engine (type: import)
  - A_03_ORCHESTRATION.anti_loop_budget (type: import)
  - A_01_CORE.execution_loop (type: import)
  - A_01_CORE.execution_loop (type: import)
  ... and 13 more
- dependency_nodes:
  - node: A_07_MEMORY.goal_loop_engine
  - node: A_03_ORCHESTRATION.anti_loop_budget
  - node: A_01_CORE.execution_loop
  - node: mainloop
  - node: ExecutionLoop
  ... and 8 more

### Chat
- Evidence count: 71
- file_paths:
  - A_01_CORE/chat_core_bridge.py
  - A_03_ORCHESTRATION/chat_router.BAK_CURRENT.py
  - A_03_ORCHESTRATION/chat_router.CLEAN_UTF8.py
  - A_03_ORCHESTRATION/chat_router.HYBRID_WORK.after_import.py
  - A_03_ORCHESTRATION/chat_router.HYBRID_WORK.after_resolver.py
  ... and 13 more
- classes:
  - ChatCoreBridge (file: 205)
  - ButlerInteractiveChat (file: 241)
  - ChatRouterMirror (file: 419)
- functions:
  - handle_chat (file: 409)
  - handle_chat (file: 410)
  - handle_chat (file: 411)
  - handle_chat (file: 412)
  - handle_chat (file: 413)
  ... and 8 more
- calls:
  - ask_ollama_free_chat (file: 241)
  - ButlerInteractiveChat (file: 241)
  - handle_chat (file: 409)
  - handle_chat (file: 410)
  - handle_chat (file: 411)
  ... and 11 more
- link_targets:
  - ask_ollama_free_chat (type: call)
  - ButlerInteractiveChat (type: call)
  - handle_chat (type: call)
  - handle_chat (type: call)
  - handle_chat (type: call)
  ... and 11 more
- dependency_nodes:
  - node: ask_ollama_free_chat
  - node: ButlerInteractiveChat
  - node: handle_chat
  - node: ChatRouterMirror
  - node: chat

### Orchestrator
- Evidence count: 67
- file_paths:
  - A_01_CORE/core_orchestrator.py
  - A_01_CORE/orchestrator.py
  - A_01_CORE_BACKUP/A_03_ORCHESTRATION/orchestrator.py
  - A_01_CORE_BACKUP/orchestrator.py
  - A_03_ORCHESTRATION/orchestrator.py
  ... and 2 more
- classes:
  - CoreOrchestrator (file: 208)
  - MainOrchestrator (file: 221)
  - MainOrchestrator (file: 253)
  - Orchestrator (file: 452)
  - LoopOrchestratorV3_MASTER_TRUTH (file: 1117)
  ... and 3 more
- imports:
  - A_01_CORE.orchestrator (file: 217)
  - A_01_CORE.orchestrator (file: 251)
  - A_01_CORE.core_orchestrator (file: 434)
  - A_07_MEMORY.memory_orchestrator (file: 468)
  - A_07_MEMORY.memory_orchestrator (file: 1136)
  ... and 3 more
- calls:
  - CoreOrchestrator (file: 208)
  - Orchestrator (file: 217)
  - Orchestrator (file: 251)
  - CoreOrchestrator (file: 434)
  - MemoryOrchestrator (file: 468)
  ... and 8 more
- link_targets:
  - A_01_CORE.orchestrator (type: import)
  - A_01_CORE.orchestrator (type: import)
  - A_01_CORE.core_orchestrator (type: import)
  - A_07_MEMORY.memory_orchestrator (type: import)
  - A_07_MEMORY.memory_orchestrator (type: import)
  ... and 16 more
- dependency_nodes:
  - node: A_01_CORE.orchestrator
  - node: A_01_CORE.core_orchestrator
  - node: A_07_MEMORY.memory_orchestrator
  - node: CoreOrchestrator
  - node: Orchestrator
  ... and 5 more

### Lock
- Evidence count: 65
- file_paths:
  - A_00_ARCHITECTURE/ARCHITECTURE_LOCK.backup.json
  - A_00_ARCHITECTURE/ARCHITECTURE_LOCK.corrupted.json
  - A_00_ARCHITECTURE/ARCHITECTURE_LOCK.json
  - A_00_ARCHITECTURE/SNAPSHOTS/snapshot_20260609_235135/ARCHITECTURE_LOCK.json
  - A_00_ARCHITECTURE/SNAPSHOTS/snapshot_20260610_000227/ARCHITECTURE_LOCK.json
  ... and 30 more
- functions:
  - verify_lock_manifest (file: 219)
  - load_lock_source (file: 223)
  - rebuild_lock_manifest (file: 223)
- calls:
  - verify_lock_manifest (file: 219)
  - load_lock_source (file: 223)
  - rebuild_lock_manifest (file: 223)
  - load_lock_source (file: 223)
  - rebuild_lock_manifest (file: 223)
  ... and 5 more
- link_targets:
  - verify_lock_manifest (type: call)
  - load_lock_source (type: call)
  - rebuild_lock_manifest (type: call)
  - load_lock_source (type: call)
  - rebuild_lock_manifest (type: call)
  ... and 5 more
- dependency_nodes:
  - node: verify_lock_manifest
  - node: load_lock_source
  - node: rebuild_lock_manifest
  - node: detect_deadlock
  - node: RLock
  ... and 2 more

### Bridge
- Evidence count: 64
- file_paths:
  - A_01_CORE/chat_core_bridge.py
  - A_02_MANAGERS/ArchitectAgent/architect_agent.py.BAK_BRIDGE
  - A_02_MANAGERS/Planner/planner_engine.py.BAK_BRIDGE
  - A_02_MANAGERS/smart_dispatcher_v2.py.BAK_4_26_DOCUMENTS_BRIDGE
  - A_02_MANAGERS/tool_bridge.py
  ... and 20 more
- classes:
  - ChatCoreBridge (file: 205)
  - ToolBridge (file: 360)
  - ToolBridge (file: 369)
  - ComfyUIBridge (file: 371)
  - DispatcherBridge (file: 429)
  ... and 2 more
- imports:
  - A_02_MANAGERS.tool_bridge (file: 365)
  - A_03_ENGINES.Generation_Engine.comfy_bridge (file: 408)
  - A_03_ORCHESTRATION.dispatcher_bridge_v2 (file: 414)
  - A_07_MEMORY.catalog_search_bridge (file: 616)
  - A_03_ORCHESTRATION.dispatcher_bridge_v2 (file: 1363)
  ... and 2 more
- calls:
  - ToolBridge (file: 365)
  - ComfyUIBridge (file: 371)
  - ComfyUIBridge (file: 408)
  - FactoryCoreBridge (file: 434)
  - CatalogSearchBridge (file: 616)
- link_targets:
  - A_02_MANAGERS.tool_bridge (type: import)
  - A_03_ENGINES.Generation_Engine.comfy_bridge (type: import)
  - A_03_ORCHESTRATION.dispatcher_bridge_v2 (type: import)
  - A_07_MEMORY.catalog_search_bridge (type: import)
  - A_03_ORCHESTRATION.dispatcher_bridge_v2 (type: import)
  ... and 7 more
- dependency_nodes:
  - node: A_02_MANAGERS.tool_bridge
  - node: A_03_ENGINES.Generation_Engine.comfy_bridge
  - node: A_03_ORCHESTRATION.dispatcher_bridge_v2
  - node: A_07_MEMORY.catalog_search_bridge
  - node: ToolBridge
  ... and 3 more

### Dependency
- Evidence count: 64
- file_paths:
  - A_00_ARCHITECTURE/DEPENDENCY_MAP.md
  - A_02_MANAGERS/ArchitectAgent/dependency_analyzer.py
  - A_02_MANAGERS/ArchitectAgent/dependency_closure.py
  - A_02_MANAGERS/ArchitectAgent/dependency_graph.py
  - A_07_CONFIG/dependency_internal.json
  ... and 4 more
- classes:
  - DependencyAnalyzer (file: 271)
  - DependencyClosure (file: 272)
  - DependencyGraph (file: 273)
- imports:
  - dependency_analyzer (file: 261)
  - dependency_analyzer (file: 263)
  - dependency_analyzer (file: 265)
  - dependency_analyzer (file: 266)
  - dependency_analyzer (file: 267)
  ... and 5 more
- calls:
  - DependencyAnalyzer (file: 261)
  - DependencyAnalyzer (file: 263)
  - DependencyAnalyzer (file: 265)
  - DependencyAnalyzer (file: 266)
  - DependencyAnalyzer (file: 267)
  ... and 8 more
- link_targets:
  - dependency_analyzer (type: import)
  - dependency_analyzer (type: import)
  - dependency_analyzer (type: import)
  - dependency_analyzer (type: import)
  - dependency_analyzer (type: import)
  ... and 18 more
- dependency_nodes:
  - node: dependency_analyzer
  - node: dependency_graph
  - node: dependency_closure
  - node: DependencyAnalyzer
  - node: DependencyGraph
  ... and 1 more

### Provider
- Evidence count: 63
- file_paths:
  - A_02_MANAGERS/ArchitectAgent/context_provider.py
  - A_02_MANAGERS/provider_manager.py
  - A_02_MANAGERS_BACKUP/provider_manager.py
  - A_10_BUTLER_OS/00_PRODUCTION/providers/model_registry.py
  - A_99_TEST_DATA/test_context_provider.py
  ... and 2 more
- classes:
  - ContextProvider (file: 270)
  - ProviderManager (file: 315)
  - ProviderManager (file: 367)
- imports:
  - A_02_MANAGERS.provider_manager (file: 231)
  - context_provider (file: 261)
  - context_provider (file: 263)
  - context_provider (file: 266)
  - context_provider (file: 267)
  ... and 6 more
- calls:
  - ProviderManager (file: 231)
  - ContextProvider (file: 261)
  - ContextProvider (file: 263)
  - ContextProvider (file: 266)
  - ContextProvider (file: 267)
  ... and 8 more
- link_targets:
  - A_02_MANAGERS.provider_manager (type: import)
  - context_provider (type: import)
  - context_provider (type: import)
  - context_provider (type: import)
  - context_provider (type: import)
  ... and 19 more
- dependency_nodes:
  - node: A_02_MANAGERS.provider_manager
  - node: context_provider
  - node: A_02_MANAGERS.ArchitectAgent.context_provider
  - node: ProviderManager
  - node: ContextProvider

### Adapter
- Evidence count: 53
- file_paths:
  - A_02_MANAGERS/TaskRunner/ExecutionAdapters/__init__.py
  - A_02_MANAGERS/TaskRunner/ExecutionAdapters/base_adapter.py
  - A_02_MANAGERS/TaskRunner/ExecutionAdapters/powershell_adapter.py
  - A_02_MANAGERS/TaskRunner/ExecutionAdapters/python_adapter.py
  - A_02_MANAGERS/TaskRunner/ExecutionAdapters/python_adapter.py.BAK_UTF8
  ... and 8 more
- classes:
  - BaseExecutionAdapter (file: 342)
  - PowerShellExecutionAdapter (file: 343)
  - PythonExecutionAdapter (file: 344)
  - ButlerOSAdapter (file: 405)
  - DreamDispatcherAdapter (file: 432)
  ... and 1 more
- imports:
  - A_02_MANAGERS.TaskRunner.ExecutionAdapters.base_adapter (file: 343)
  - A_02_MANAGERS.TaskRunner.ExecutionAdapters.base_adapter (file: 344)
  - A_02_MANAGERS.TaskRunner.ExecutionAdapters.python_adapter (file: 346)
  - A_02_MANAGERS.TaskRunner.ExecutionAdapters.powershell_adapter (file: 346)
  - A_03_ORCHESTRATION.butler_os_adapter (file: 474)
  ... and 3 more
- calls:
  - adapter_class (file: 346)
  - ButlerOSAdapter (file: 474)
  - ButlerOSAdapter (file: 476)
  - ProfessorAdapter (file: 477)
  - ButlerOSAdapter (file: 1277)
- link_targets:
  - A_02_MANAGERS.TaskRunner.ExecutionAdapters.base_adapter (type: import)
  - A_02_MANAGERS.TaskRunner.ExecutionAdapters.base_adapter (type: import)
  - A_02_MANAGERS.TaskRunner.ExecutionAdapters.python_adapter (type: import)
  - A_02_MANAGERS.TaskRunner.ExecutionAdapters.powershell_adapter (type: import)
  - A_03_ORCHESTRATION.butler_os_adapter (type: import)
  ... and 8 more
- dependency_nodes:
  - node: A_02_MANAGERS.TaskRunner.ExecutionAdapters.base_adapter
  - node: A_02_MANAGERS.TaskRunner.ExecutionAdapters.python_adapter
  - node: A_02_MANAGERS.TaskRunner.ExecutionAdapters.powershell_adapter
  - node: A_03_ORCHESTRATION.butler_os_adapter
  - node: A_03_ORCHESTRATION.professor_adapter
  ... and 3 more

### Policy
- Evidence count: 48
- file_paths:
  - A_00_ARCHITECTURE/LAB_POLICY.md
  - A_00_ARCHITECTURE/LEGACY_POLICY.md
  - A_02_MANAGERS/ExecutionPolicyEngine/policy_loader.py
  - A_02_MANAGERS/ExecutionPolicyEngine/policy_registry.py
  - A_02_MANAGERS/ExecutionPolicyEngine/policy_validator.py
  ... and 1 more
- classes:
  - PolicyLoader (file: 296)
  - PolicyRegistry (file: 297)
  - PolicyValidator (file: 298)
  - ScopePolicy (file: 562)
  - ExecutionPolicy (file: 1082)
- imports:
  - A_07_CONFIG.execution_policy_schema (file: 296)
  - A_07_CONFIG.execution_policy_schema (file: 296)
  - A_07_CONFIG.execution_policy_schema (file: 296)
  - A_07_CONFIG.execution_policy_schema (file: 296)
  - A_07_CONFIG.execution_policy_schema (file: 296)
  ... and 4 more
- calls:
  - ExecutionPolicy (file: 296)
  - default_policy (file: 296)
  - default_policy (file: 297)
  - default_policy (file: 298)
  - ScopePolicy (file: 562)
  ... and 2 more
- link_targets:
  - A_07_CONFIG.execution_policy_schema (type: import)
  - A_07_CONFIG.execution_policy_schema (type: import)
  - A_07_CONFIG.execution_policy_schema (type: import)
  - A_07_CONFIG.execution_policy_schema (type: import)
  - A_07_CONFIG.execution_policy_schema (type: import)
  ... and 11 more
- dependency_nodes:
  - node: A_07_CONFIG.execution_policy_schema
  - node: A_02_MANAGERS.ExecutionPolicyEngine.policy_loader
  - node: ExecutionPolicy
  - node: default_policy
  - node: ScopePolicy

### Schema
- Evidence count: 48
- file_paths:
  - A_02_MANAGERS/RuntimeCapabilityRegistry/capability_schema.py
  - A_07_CONFIG/execution_context_schema.py
  - A_07_CONFIG/execution_policy_schema.py
  - A_07_CONFIG/recipe_schema.py
  - patch_recipe_schema_version.py
- imports:
  - A_07_CONFIG.recipe_schema (file: 279)
  - A_07_CONFIG.execution_policy_schema (file: 296)
  - A_07_CONFIG.execution_policy_schema (file: 296)
  - A_07_CONFIG.execution_policy_schema (file: 296)
  - A_07_CONFIG.execution_policy_schema (file: 296)
  ... and 15 more
- link_targets:
  - A_07_CONFIG.recipe_schema (type: import)
  - A_07_CONFIG.execution_policy_schema (type: import)
  - A_07_CONFIG.execution_policy_schema (type: import)
  - A_07_CONFIG.execution_policy_schema (type: import)
  - A_07_CONFIG.execution_policy_schema (type: import)
  ... and 15 more
- dependency_nodes:
  - node: A_07_CONFIG.recipe_schema
  - node: A_07_CONFIG.execution_policy_schema
  - node: A_02_MANAGERS.RuntimeCapabilityRegistry.capability_schema

### Resolver
- Evidence count: 47
- file_paths:
  - A_03_ORCHESTRATION/chat_router.HYBRID_WORK.after_resolver.py
  - A_03_ORCHESTRATION/hybrid_resolver.py
  - A_04_AGENTS/ProjectDocumentationDepartment/Core/ast_path_resolver.BAK.py
  - A_04_AGENTS/ProjectDocumentationDepartment/Core/ast_path_resolver.py
  - A_04_AGENTS/ProjectDocumentationDepartment/Core_BACKUP_UTF8SIG/ast_path_resolver.BAK.py
  ... and 2 more
- classes:
  - HybridResolver (file: 446)
  - Resolver (file: 514)
  - Resolver (file: 515)
  - Resolver (file: 569)
  - Resolver (file: 570)
  ... and 1 more
- imports:
  - A_03_ORCHESTRATION.hybrid_resolver (file: 410)
  - A_03_ORCHESTRATION.hybrid_resolver (file: 411)
  - hybrid_resolver (file: 412)
  - hybrid_resolver (file: 413)
  - A_07_MEMORY.SESSION.reference_resolver (file: 507)
- calls:
  - HybridResolver (file: 411)
  - HybridResolver (file: 412)
  - HybridResolver (file: 413)
  - HybridResolver (file: 446)
  - ReferenceResolver (file: 507)
  ... and 4 more
- link_targets:
  - A_03_ORCHESTRATION.hybrid_resolver (type: import)
  - A_03_ORCHESTRATION.hybrid_resolver (type: import)
  - hybrid_resolver (type: import)
  - hybrid_resolver (type: import)
  - A_07_MEMORY.SESSION.reference_resolver (type: import)
  ... and 9 more
- dependency_nodes:
  - node: A_03_ORCHESTRATION.hybrid_resolver
  - node: hybrid_resolver
  - node: A_07_MEMORY.SESSION.reference_resolver
  - node: HybridResolver
  - node: ReferenceResolver
  ... and 1 more

### Validate
- Evidence count: 46
- calls:
  - invalidate_caches (file: 219)
  - validate (file: 298)
  - validate (file: 318)
  - validate (file: 318)
  - validate (file: 359)
  ... and 16 more
- link_targets:
  - invalidate_caches (type: call)
  - validate (type: call)
  - validate (type: call)
  - validate (type: call)
  - validate (type: call)
  ... and 16 more
- dependency_nodes:
  - node: invalidate_caches
  - node: validate
  - node: validate_file_syntax
  - node: validate_profile

### Genie
- Evidence count: 43
- file_paths:
  - A_09_GUARDIANS/genie.ps1
  - A_09_GUARDIANS/genie_architecture_diff.ps1
  - A_09_GUARDIANS/genie_auto_restore_advisor.ps1
  - A_09_GUARDIANS/genie_bark_engine.ps1
  - A_09_GUARDIANS/genie_bone_cache.ps1
  ... and 38 more

### Pipeline
- Evidence count: 43
- file_paths:
  - A_00_ARCHITECTURE/STRICT_MODULE_PIPELINE.md
  - A_02_MANAGERS/ArchitectAgent/planner_pipeline.py
  - A_02_MANAGERS/ArchitectAgent/planner_pipeline_test.py
  - A_03_HANDLERS/pdf_ocr_pipeline.py
  - A_04_AGENTS/ProjectDocumentationDepartment/Core/engineering_pipeline.py
  ... and 7 more
- classes:
  - PlannerPipeline (file: 276)
  - PDFOCRPipeline (file: 386)
  - EngineeringPipeline (file: 536)
  - EngineeringPipeline (file: 591)
- functions:
  - run_pipeline (file: 1485)
  - run_pipeline (file: 1486)
- imports:
  - planner_pipeline (file: 264)
  - A_04_AGENTS.ProjectDocumentationDepartment.Core.engineering_pipeline (file: 611)
  - A_03_HANDLERS.pdf_ocr_pipeline (file: 1349)
- calls:
  - PlannerPipeline (file: 264)
  - PlannerPipeline (file: 276)
  - EngineeringPipeline (file: 611)
  - PDFOCRPipeline (file: 1349)
  - run_pipeline (file: 1485)
  ... and 1 more
- link_targets:
  - planner_pipeline (type: import)
  - A_04_AGENTS.ProjectDocumentationDepartment.Core.engineering_pipeline (type: import)
  - A_03_HANDLERS.pdf_ocr_pipeline (type: import)
  - PlannerPipeline (type: call)
  - PlannerPipeline (type: call)
  ... and 4 more
- dependency_nodes:
  - node: planner_pipeline
  - node: A_04_AGENTS.ProjectDocumentationDepartment.Core.engineering_pipeline
  - node: A_03_HANDLERS.pdf_ocr_pipeline
  - node: PlannerPipeline
  - node: EngineeringPipeline
  ... and 2 more

### Contract
- Evidence count: 42
- file_paths:
  - A_02_MANAGERS/ArchitectAgent/task_contract_builder.py
  - A_07_MEMORY/project_context_builder.CONTRACT.txt
  - A_09_GUARDIANS/Config/build_contracts.ps1
  - A_10_BUTLER_OS/00_PRODUCTION/core/department_contract.py
- classes:
  - TaskContractBuilder (file: 281)
- imports:
  - task_contract_builder (file: 263)
  - task_contract_builder (file: 264)
  - task_contract_builder (file: 266)
  - task_contract_builder (file: 267)
  - task_contract_builder (file: 276)
  ... and 1 more
- calls:
  - TaskContractBuilder (file: 263)
  - TaskContractBuilder (file: 264)
  - TaskContractBuilder (file: 266)
  - TaskContractBuilder (file: 267)
  - TaskContractBuilder (file: 276)
  ... and 6 more
- link_targets:
  - task_contract_builder (type: import)
  - task_contract_builder (type: import)
  - task_contract_builder (type: import)
  - task_contract_builder (type: import)
  - task_contract_builder (type: import)
  ... and 12 more
- dependency_nodes:
  - node: task_contract_builder
  - node: TaskContractBuilder
  - node: _check_contract

### Generator
- Evidence count: 41
- file_paths:
  - A_02_MANAGERS/ArchitectAgent/recipe_generator.py
  - A_02_MANAGERS/recipe_generator.py
- classes:
  - RecipeGenerator (file: 280)
  - RecipeGenerator (file: 317)
- imports:
  - recipe_generator (file: 263)
  - recipe_generator (file: 264)
  - recipe_generator (file: 266)
  - recipe_generator (file: 267)
  - recipe_generator (file: 276)
  ... and 3 more
- calls:
  - RecipeGenerator (file: 263)
  - RecipeGenerator (file: 264)
  - RecipeGenerator (file: 266)
  - RecipeGenerator (file: 267)
  - RecipeGenerator (file: 276)
  ... and 4 more
- link_targets:
  - recipe_generator (type: import)
  - recipe_generator (type: import)
  - recipe_generator (type: import)
  - recipe_generator (type: import)
  - recipe_generator (type: import)
  ... and 12 more
- dependency_nodes:
  - node: recipe_generator
  - node: A_02_MANAGERS.recipe_generator
  - node: RecipeGenerator

### Logger
- Evidence count: 28
- file_paths:
  - A_01_CORE/logger_config.py
  - A_01_CORE_BACKUP/logger_config.py
  - A_09_GUARDIANS/genie_change_logger.ps1
- functions:
  - setup_logger (file: 215)
  - setup_logger (file: 249)
- imports:
  - A_01_CORE.logger_config (file: 477)
  - A_01_CORE.logger_config (file: 480)
- calls:
  - getLogger (file: 214)
  - getLogger (file: 215)
  - getLogger (file: 248)
  - getLogger (file: 249)
  - setup_logger (file: 477)
  ... and 3 more
- link_targets:
  - A_01_CORE.logger_config (type: import)
  - A_01_CORE.logger_config (type: import)
  - getLogger (type: call)
  - getLogger (type: call)
  - getLogger (type: call)
  ... and 5 more
- dependency_nodes:
  - node: A_01_CORE.logger_config
  - node: getLogger
  - node: setup_logger

### Validator
- Evidence count: 28
- file_paths:
  - A_02_MANAGERS/ExecutionPolicyEngine/policy_validator.py
  - A_02_MANAGERS/recipe_validator.py
  - A_02_MANAGERS/TaskRunner/security_validator.py
  - A_07_CONFIG/registry_validator.py
  - A_09_GUARDIANS/genie_freeze_validator.ps1
  ... and 1 more
- classes:
  - PolicyValidator (file: 298)
  - RecipeValidator (file: 318)
  - SecurityValidator (file: 359)
  - RegistryValidator (file: 1107)
  - FeedbackValidatorV2 (file: 1115)
  ... and 1 more
- imports:
  - A_02_MANAGERS.recipe_validator (file: 352)
  - A_02_MANAGERS.recipe_validator (file: 1420)
- calls:
  - RecipeValidator (file: 318)
  - RegistryValidator (file: 1107)
  - LocalFeedbackValidatorV2 (file: 1117)
  - RecipeValidator (file: 1420)
- link_targets:
  - A_02_MANAGERS.recipe_validator (type: import)
  - A_02_MANAGERS.recipe_validator (type: import)
  - RecipeValidator (type: call)
  - RegistryValidator (type: call)
  - LocalFeedbackValidatorV2 (type: call)
  ... and 1 more
- dependency_nodes:
  - node: A_02_MANAGERS.recipe_validator
  - node: RecipeValidator
  - node: RegistryValidator
  - node: LocalFeedbackValidatorV2

### Map
- Evidence count: 25
- file_paths:
  - A_00_ARCHITECTURE/DEPENDENCY_MAP.md
  - A_00_ARCHITECTURE/ROADMAP_DMITRY_v1_2.md
  - A_00_ARCHITECTURE/ROADMAP_STATUS.md
  - A_07_CONFIG/dependency_map.json
  - A_08_LOGS/ARCHITECTURE/FACTORY_FLOW_MAP.txt
  ... and 10 more
- calls:
  - get_pixmap (file: 385)
  - get_pixmap (file: 386)
  - roadmap (file: 1103)
  - get_pixmap (file: 1350)
- link_targets:
  - get_pixmap (type: call)
  - get_pixmap (type: call)
  - roadmap (type: call)
  - get_pixmap (type: call)
- dependency_nodes:
  - node: get_pixmap
  - node: roadmap

### Storage
- Evidence count: 25
- file_paths:
  - A_05_STORAGE/__init__.py
  - A_05_STORAGE/catalog.db
  - A_05_STORAGE/checkpoint.md
  - A_05_STORAGE/handshake.txt
  - A_05_STORAGE/MEMORY.md
  ... and 20 more

### Factory
- Evidence count: 23
- file_paths:
  - A_02_MANAGERS/TaskRunner/executor_factory.py
  - A_03_ORCHESTRATION/factory_core_bridge.py
  - A_06_WORKSPACE/queue/completed/recipe_factory_test.json
  - A_08_LOGS/ARCHITECTURE/FACTORY_FLOW_MAP.txt
  - A_08_LOGS/BUTLER_FACTORY_AUDIT_20260615_134633/01_ALL_FILES.csv
  ... and 6 more
- classes:
  - ExecutorFactory (file: 346)
  - FactoryCoreBridge (file: 434)
- functions:
  - latest_rollback_has_factory (file: 1487)
- imports:
  - A_02_MANAGERS.TaskRunner.executor_factory (file: 348)
- calls:
  - FactoryCoreBridge (file: 434)
  - latest_rollback_has_factory (file: 1487)
- link_targets:
  - A_02_MANAGERS.TaskRunner.executor_factory (type: import)
  - FactoryCoreBridge (type: call)
  - latest_rollback_has_factory (type: call)
- dependency_nodes:
  - node: A_02_MANAGERS.TaskRunner.executor_factory
  - node: FactoryCoreBridge
  - node: latest_rollback_has_factory

### Event
- Evidence count: 22
- file_paths:
  - A_01_CORE/event_bus.py
  - A_01_CORE_BACKUP/event_bus.py
  - A_08_LOGS/safety_gate_events.jsonl
  - A_08_LOGS/system_events.jsonl
- classes:
  - EventBus (file: 210)
  - EventBus (file: 246)
- calls:
  - add_event (file: 448)
  - score_event (file: 1124)
  - search_event (file: 1158)
  - add_event (file: 1158)
  - log_event (file: 1158)
  ... and 1 more
- link_targets:
  - add_event (type: call)
  - score_event (type: call)
  - search_event (type: call)
  - add_event (type: call)
  - log_event (type: call)
  ... and 1 more
- dependency_nodes:
  - node: add_event
  - node: score_event
  - node: search_event
  - node: log_event

### Executor
- Evidence count: 21
- file_paths:
  - A_02_MANAGERS/TaskRunner/executor_factory.py
  - A_02_MANAGERS/TaskRunner/recipe_executor.py
  - A_03_EXECUTORS/executor.py
  - A_07_MEMORY/agent_loop_executor.py
- classes:
  - ExecutorFactory (file: 346)
  - RecipeExecutor (file: 348)
  - Executor (file: 375)
  - AgentLoopExecutor (file: 1114)
- functions:
  - sample_executor (file: 399)
- imports:
  - A_02_MANAGERS.TaskRunner.executor_factory (file: 348)
  - A_02_MANAGERS.TaskRunner.recipe_executor (file: 358)
- calls:
  - Executor (file: 375)
  - executor (file: 399)
- link_targets:
  - A_02_MANAGERS.TaskRunner.executor_factory (type: import)
  - A_02_MANAGERS.TaskRunner.recipe_executor (type: import)
  - Executor (type: call)
  - executor (type: call)
- dependency_nodes:
  - node: A_02_MANAGERS.TaskRunner.executor_factory
  - node: A_02_MANAGERS.TaskRunner.recipe_executor
  - node: Executor
  - node: executor

### Store
- Evidence count: 21
- file_paths:
  - A_00_UTILS/butler_restore_v2.ps1
  - A_03_ORCHESTRATION/chat_router_test_restore.py
  - A_09_GUARDIANS/genie_auto_restore_advisor.ps1
  - A_09_GUARDIANS/genie_restore_advisor.ps1
  - A_09_GUARDIANS/genie_restore_map.ps1
  ... and 3 more
- functions:
  - restore_backup (file: 225)
  - restore (file: 1475)
  - restore (file: 1476)
- calls:
  - restore_backup (file: 225)
  - restore_backup (file: 225)
  - restore (file: 1475)
  - restore (file: 1476)
- link_targets:
  - restore_backup (type: call)
  - restore_backup (type: call)
  - restore (type: call)
  - restore (type: call)
- dependency_nodes:
  - node: restore_backup
  - node: restore

### Watch
- Evidence count: 18
- file_paths:
  - A_02_MANAGERS/TaskRunner/recipe_queue_watcher.py
  - A_09_GUARDIANS/genie_file_watcher.ps1
  - A_09_GUARDIANS/genie_watchdog.ps1
  - A_09_GUARDIANS/watch_manifest.json
  - A_09_GUARDIANS/watch_state.json
- classes:
  - RecipeQueueWatcher (file: 350)
- imports:
  - A_02_MANAGERS.TaskRunner.recipe_queue_watcher (file: 357)
  - A_02_MANAGERS.TaskRunner.recipe_queue_watcher (file: 358)
- calls:
  - RecipeQueueWatcher (file: 350)
  - RecipeQueueWatcher (file: 357)
  - RecipeQueueWatcher (file: 358)
- link_targets:
  - A_02_MANAGERS.TaskRunner.recipe_queue_watcher (type: import)
  - A_02_MANAGERS.TaskRunner.recipe_queue_watcher (type: import)
  - RecipeQueueWatcher (type: call)
  - RecipeQueueWatcher (type: call)
  - RecipeQueueWatcher (type: call)
- dependency_nodes:
  - node: A_02_MANAGERS.TaskRunner.recipe_queue_watcher
  - node: RecipeQueueWatcher

### Message
- Evidence count: 17
- file_paths:
  - A_03_ORCHESTRATION/message_network.py
- classes:
  - MessageNetwork (file: 449)
- imports:
  - A_03_ORCHESTRATION.message_network (file: 1495)
  - A_03_ORCHESTRATION.message_network (file: 1505)
- calls:
  - MessageNetwork (file: 449)
  - create_message (file: 449)
  - MessageNetwork (file: 1495)
  - MessageNetwork (file: 1505)
- link_targets:
  - A_03_ORCHESTRATION.message_network (type: import)
  - A_03_ORCHESTRATION.message_network (type: import)
  - MessageNetwork (type: call)
  - create_message (type: call)
  - MessageNetwork (type: call)
  ... and 1 more
- dependency_nodes:
  - node: A_03_ORCHESTRATION.message_network
  - node: MessageNetwork
  - node: create_message

### Change_Request
- Evidence count: 16
- file_paths:
  - A_00_ARCHITECTURE/CHANGE_REQUESTS/CR_000_TEST.json
  - A_00_ARCHITECTURE/CHANGE_REQUESTS/CR_RUNTIME_AUTOMATION.json
  - A_07_MEMORY/change_request_manager.py
  - A_07_MEMORY/change_request_manager.py.BAK_CONSISTENCY
  - A_07_MEMORY/change_request_manager.py.BAK_LOOP
- imports:
  - A_07_MEMORY.change_request_manager (file: 1114)
  - A_07_MEMORY.change_request_manager (file: 1117)
  - A_07_MEMORY.change_request_manager (file: 1118)
  - A_07_MEMORY.change_request_manager (file: 1144)
  - A_07_MEMORY.change_request_manager (file: 1145)
- link_targets:
  - A_07_MEMORY.change_request_manager (type: import)
  - A_07_MEMORY.change_request_manager (type: import)
  - A_07_MEMORY.change_request_manager (type: import)
  - A_07_MEMORY.change_request_manager (type: import)
  - A_07_MEMORY.change_request_manager (type: import)
- dependency_nodes:
  - node: A_07_MEMORY.change_request_manager

### Workflow
- Evidence count: 13
- file_paths:
  - A_07_CONFIG/comfy_workflow.json
  - A_07_MEMORY/PNG_WORKFLOW_MEMORY.json
  - A_07_MEMORY/png_workflow_memory.py
- classes:
  - PNGWorkflowMemory (file: 1164)
- imports:
  - A_07_MEMORY.png_workflow_memory (file: 1351)
- calls:
  - PNGWorkflowMemory (file: 1351)
  - get_workflow (file: 1351)
- link_targets:
  - A_07_MEMORY.png_workflow_memory (type: import)
  - PNGWorkflowMemory (type: call)
  - get_workflow (type: call)
- dependency_nodes:
  - node: A_07_MEMORY.png_workflow_memory
  - node: PNGWorkflowMemory
  - node: get_workflow

### Artist
- Evidence count: 12
- file_paths:
  - patch_image_dual_artist.py
- calls:
  - _select_artist (file: 499)
  - _build_artist_prompt (file: 499)
  - _ask_artist (file: 499)
  - _ask_artist (file: 499)
- link_targets:
  - _select_artist (type: call)
  - _build_artist_prompt (type: call)
  - _ask_artist (type: call)
  - _ask_artist (type: call)
- dependency_nodes:
  - node: _select_artist
  - node: _build_artist_prompt
  - node: _ask_artist

### Reference
- Evidence count: 11
- file_paths:
  - A_07_MEMORY/SESSION/reference_resolver.py
- classes:
  - ReferenceResolver (file: 1201)
- imports:
  - A_07_MEMORY.SESSION.reference_resolver (file: 507)
- calls:
  - get_preferences (file: 218)
  - ReferenceResolver (file: 507)
- link_targets:
  - A_07_MEMORY.SESSION.reference_resolver (type: import)
  - get_preferences (type: call)
  - ReferenceResolver (type: call)
- dependency_nodes:
  - node: A_07_MEMORY.SESSION.reference_resolver
  - node: get_preferences
  - node: ReferenceResolver

### Bootstrap
- Evidence count: 11
- file_paths:
  - A_00_UTILS/butler_bootstrap.ps1
  - A_01_CORE/bootstrap_guard.py
  - A_02_MANAGERS/ArchitectAgent/architect_bootstrap.py
- classes:
  - ArchitectBootstrap (file: 264)
  - BootstrapCore (file: 1495)
- calls:
  - ArchitectBootstrap (file: 264)
  - BootstrapCore (file: 1495)
- link_targets:
  - ArchitectBootstrap (type: call)
  - BootstrapCore (type: call)
- dependency_nodes:
  - node: ArchitectBootstrap
  - node: BootstrapCore

## DO NOT BUILD AGAIN
Do not rebuild any of the above capabilities.
