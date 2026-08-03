# BUTLER KNOWLEDGE SUMMARY

## DEPARTMENTS
- ArchiveDepartment
- AudioDepartment
- BaseDepartment
- CodingDepartment
- Department
- DocumentsDepartment
- ImageDepartment
- MemoryDepartment
- OpenDocumentDepartment
- ProjectDocumentationDepartment
- RuntimeDepartmentsDiscoveryAgent
- SearchDepartment
- TextDepartment
- VideoDepartment
- VisionDepartment

## MEMORY
- AttentionMemory
- ExecutionHistory
- ExecutionMemoryV2
- HistoryScanner
- MemoryAdvisor
- MemoryCore
- MemoryDepartment
- MemoryFacade
- MemoryFacadeV2
- MemoryLayer
- MemoryLoop
- MemoryManager
- MemoryOrchestrator
- MemoryOrchestratorV2
- MemoryReplay
- MemorySidecar
- PNGWorkflowMemory
- ProjectHistory
- ProjectMemoryLoader
- ReasoningPath
- SelfHealingMemory
- SemanticCompressor
- SemanticConstraintLayer
- SemanticCore
- SemanticLayer
- SemanticMatch
- SemanticMemory
- SemanticQueryParser
- SemanticReasoningEngine
- SemanticReasoningEngineV2
- SemanticRelationsEngine
- SemanticSearchEngine
- TestMemoryAdvisor

## SECURITY
- ExecutionMonitor
- RecipeQueueWatcher
- SecurityValidator
- SecurityViolation

## EXECUTION
- AgentLoopExecutor
- AutomaticVerifier
- AutonomousLoop
- BaseExecutionAdapter
- ButlerHarness
- EngineeringPipeline
- ExecutionContext
- ExecutionHistory
- ExecutionLoop
- ExecutionMemoryV2
- ExecutionMonitor
- ExecutionPolicy
- ExecutionRegistry
- ExecutionRegistryDiscoveryAgent
- ExecutionResult
- ExecutionScanner
- ExecutionState
- Executor
- ExecutorFactory
- HarnessScanner
- IntegrationTestGuard
- PDFOCRPipeline
- PNGWorkflowMemory
- PlannerPipeline
- PowerShellExecutionAdapter
- PythonExecutionAdapter
- QueueManager
- Recipe
- RecipeBuilder
- RecipeExecutor
- RecipeGenerator
- RecipeLoader
- RecipeQueueWatcher
- RecipeStep
- RecipeValidator
- RecipeWriter
- SessionQueue
- TaskContractBuilder
- TaskFeeder
- TaskPlanner
- TaskRunner
- TestMemoryAdvisor
- TestProjectAuditor

## MAIN ARCHITECTURE
- ARCHIVE: ArchiveDepartment
- AUDIO: AudioDepartment
- AUDIT: AuditScanner
- AUTOMATION: Recipe
- CODING: CodingDepartment
- CONFIG: RouterRegistry
- DEPARTMENT: Department
- DISPATCHER: dispatch
- DOCUMENTATION: ProjectDocumentationDepartment
- EXECUTION: run_self_test
- GUARDIAN: RecipeQueueWatcher
- IMAGE: ImageDepartment
- MEMORY: SemanticReasoningEngine
- MODEL: main
- OLLAMA: ask_ollama
- PASSPORT: load_profile
- PROVIDER: ask_ollama
- QUEUE: Recipe
- REASONING: SemanticReasoningEngine
- REGISTRY: RouterRegistry
- ROUTER: SmartDispatcherV2
- SEARCH: SearchDepartment
- SECURITY: RecipeQueueWatcher
- SEMANTIC: SemanticReasoningEngine
- VIDEO: VideoDepartment
- VISION: ImageDepartment
- WATCHER: RecipeQueueWatcher

---

## CAPABILITY: MEMORY
**TOTAL EVIDENCE:** 292
**STATUS:** READY
**MAIN ENTRY:** SemanticReasoningEngine

### FILES (canonical):
- A_07_CONFIG/project_memory_loader.py
- A_07_MEMORY/agent_runtime_v2.py
- A_07_MEMORY/attention_memory.py
- A_07_MEMORY/memory_advisor.py
- A_07_MEMORY/memory_facade.py
- A_07_MEMORY/memory_facade_v2.py
- A_07_MEMORY/memory_layer.py
- A_07_MEMORY/memory_orchestrator.py
- A_07_MEMORY/memory_orchestrator_v2.py
- A_07_MEMORY/memory_replay.py
- A_07_MEMORY/memory_router.py
- A_07_MEMORY/png_workflow_memory.py
- A_07_MEMORY/profile_manager.py
- A_07_MEMORY/profile_sync.py
- A_07_MEMORY/project_history.py
- A_07_MEMORY/search_engine.py
- A_07_MEMORY/self_healing_memory.py
- A_07_MEMORY/semantic_compression.py
- A_07_MEMORY/semantic_constraint_layer.py
- A_07_MEMORY/semantic_core.py
- A_07_MEMORY/semantic_memory.py
- A_07_MEMORY/semantic_query_parser.py
- A_07_MEMORY/semantic_reasoning_engine.py
- A_07_MEMORY/semantic_reasoning_engine_v2.py
- A_07_MEMORY/semantic_relations_engine.py
- A_09_TESTS/test_memory_advisor.py
- A_01_CORE/memory_core.py
- A_01_CORE/memory_guardian.py
- A_02_MANAGERS/ExecutionMonitor/execution_history.py
- A_02_MANAGERS/memory_manager.py
- A_03_ORCHESTRATION/memory_loop.py
- A_03_ORCHESTRATION/memory_sidecar.py
- A_03_ORCHESTRATION/semantic_layer.py
- A_04_AGENTS/MemoryDepartment/runner.py
- A_04_AGENTS/ProjectDocumentationDepartment/Core/Scanners/history_scanner.py
- A_04_COMPONENTS/MemoryAdvisor/memory_advisor.py

### CLASSES:
- AttentionMemory (file: A_07_MEMORY/attention_memory.py)
- ExecutionHistory (file: A_02_MANAGERS/ExecutionMonitor/execution_history.py)
- ExecutionMemoryV2 (file: A_07_MEMORY/agent_runtime_v2.py)
- HistoryScanner (file: A_04_AGENTS/ProjectDocumentationDepartment/Core/Scanners/history_scanner.py)
- MemoryAdvisor (file: A_07_MEMORY/memory_advisor.py)
- MemoryAdvisor (file: A_04_COMPONENTS/MemoryAdvisor/memory_advisor.py)
- MemoryCore (file: A_01_CORE/memory_core.py)
- MemoryDepartment (file: A_04_AGENTS/MemoryDepartment/runner.py)
- MemoryFacade (file: A_07_MEMORY/memory_facade.py)
- MemoryFacadeV2 (file: A_07_MEMORY/memory_facade_v2.py)
- MemoryLayer (file: A_07_MEMORY/memory_layer.py)
- MemoryLoop (file: A_03_ORCHESTRATION/memory_loop.py)
- MemoryManager (file: A_02_MANAGERS/memory_manager.py)
- MemoryOrchestrator (file: A_07_MEMORY/memory_orchestrator.py)
- MemoryOrchestratorV2 (file: A_07_MEMORY/memory_orchestrator_v2.py)
- MemoryReplay (file: A_07_MEMORY/memory_replay.py)
- MemorySidecar (file: A_03_ORCHESTRATION/memory_sidecar.py)
- PNGWorkflowMemory (file: A_07_MEMORY/png_workflow_memory.py)
- ProjectHistory (file: A_07_MEMORY/project_history.py)
- ProjectMemoryLoader (file: A_07_CONFIG/project_memory_loader.py)
- ReasoningPath (file: A_07_MEMORY/semantic_reasoning_engine_v2.py)
- SelfHealingMemory (file: A_07_MEMORY/self_healing_memory.py)
- SemanticCompressor (file: A_07_MEMORY/semantic_compression.py)
- SemanticConstraintLayer (file: A_07_MEMORY/semantic_constraint_layer.py)
- SemanticCore (file: A_07_MEMORY/semantic_core.py)
- SemanticLayer (file: A_03_ORCHESTRATION/semantic_layer.py)
- SemanticMatch (file: A_07_MEMORY/semantic_reasoning_engine.py)
- SemanticMemory (file: A_07_MEMORY/semantic_memory.py)
- SemanticQueryParser (file: A_07_MEMORY/semantic_query_parser.py)
- SemanticReasoningEngine (file: A_07_MEMORY/semantic_reasoning_engine.py)
- SemanticReasoningEngineV2 (file: A_07_MEMORY/semantic_reasoning_engine_v2.py)
- SemanticRelationsEngine (file: A_07_MEMORY/semantic_relations_engine.py)
- SemanticSearchEngine (file: A_07_MEMORY/search_engine.py)
- TestMemoryAdvisor (file: A_09_TESTS/test_memory_advisor.py)

### FUNCTIONS:
- get_memory_summary (file: A_07_MEMORY/profile_manager.py)
- rebuild_user_memory (file: A_07_MEMORY/profile_manager.py)
- rebuild_user_memory (file: A_07_MEMORY/profile_sync.py)
- remember (file: A_07_MEMORY/memory_router.py)
- route_memory (file: A_07_MEMORY/memory_router.py)
- run_memory_guardian (file: A_01_CORE/memory_guardian.py)

### CALLS:
- AttentionMemory (file: A_07_MEMORY/attention_memory.py)
- AttentionMemory (file: 1136)
- AttentionMemory (file: A_07_MEMORY/memory_orchestrator_v2.py)
- ExecutionMemoryV2 (file: A_07_MEMORY/agent_runtime_v2.py)
- HistoryScanner (file: 536)
- HistoryScanner (file: A_04_AGENTS/ProjectDocumentationDepartment/Core/Scanners/history_scanner.py)
- HistoryScanner (file: 591)
- HistoryScanner (file: 601)
- MemoryAdvisor (file: A_07_MEMORY/memory_advisor.py)
- MemoryAdvisor (file: A_09_TESTS/test_memory_advisor.py)
- MemoryCore (file: 208)
- MemoryCore (file: A_01_CORE/memory_core.py)
- MemoryDepartment (file: 1285)
- MemoryDepartment (file: 1287)
- MemoryDepartment (file: 1340)
- MemoryDepartment (file: 324)
- MemoryDepartment (file: 338)
- MemoryFacade (file: 1144)
- MemoryFacade (file: A_07_MEMORY/memory_facade.py)
- MemoryFacade (file: 453)
- ... and 70 more

### DEPENDENCY_NODES:
- A_04_AGENTS.MemoryDepartment.runner (file: None)
- A_04_COMPONENTS.MemoryAdvisor.memory_advisor (file: None)
- AttentionMemory (file: None)
- ExecutionMemoryV2 (file: None)
- HistoryScanner (file: None)
- MemoryAdvisor (file: None)
- MemoryCore (file: None)
- MemoryDepartment (file: None)
- MemoryFacade (file: None)
- MemoryFacadeV2 (file: None)
- MemoryLayer (file: None)
- MemoryLoop (file: None)
- MemoryManager (file: None)
- MemoryOrchestrator (file: None)
- MemoryOrchestratorV2 (file: None)
- MemoryReplay (file: None)
- MemorySidecar (file: None)
- PNGWorkflowMemory (file: None)
- ProjectHistory (file: None)
- ProjectMemoryLoader (file: None)
- ... and 18 more

### EXECUTION_FACTS:
- PHASE_1_INIT::BOOTSTRAP: DONE
- PHASE_1_MULTITASK_TEST::TEST_TASK_A: DONE
- PHASE_1_MULTITASK_TEST::TEST_TASK_B: DONE
- PHASE_1_MULTITASK_TEST::TEST_TASK_C: DONE
- PHASE_1_TEST_DIAGNOSTICS::AUDIT_VERIFY_HEALTH: DONE
- PHASE_3_CLEANUP_AND_BACKUP::RUN_CORE_BACKUP: DONE
- TEST_PHASE_1::PHASE_1_TASK_A: DONE
- TEST_PHASE_1::PHASE_1_TASK_B: DONE
- TEST_PHASE_2::PHASE_2_TASK_C: DONE
- TEST_PHASE_2::PHASE_2_TASK_D: DONE

### GOALS_FACTS:
- active_goal: BUTLER_RECIPE_LIBRARY
- current_phase: ROADMAP_6_PHASE_4_RECIPES
- subgoal: ROADMAP_6_PHASE_4_RECIPES status=COMPLETED
- task: task_run_full_audit status=COMPLETED
- task: task_verify_contour status=COMPLETED
- weight: autonomy=0.6
- weight: stability=1.0

### IMPORTS:
- A_04_AGENTS.MemoryDepartment.runner (file: 1285)
- A_04_AGENTS.MemoryDepartment.runner (file: 1287)
- A_04_AGENTS.MemoryDepartment.runner (file: 1340)
- A_04_AGENTS.MemoryDepartment.runner (file: 324)
- A_04_AGENTS.MemoryDepartment.runner (file: 338)
- A_04_COMPONENTS.MemoryAdvisor.memory_advisor (file: A_09_TESTS/test_memory_advisor.py)

### LINKS:
- {"metadata": {"alias": null, "kind": "from", "line": 2, "name": "MemoryDepartment"}, "source": 1340, "target": "A_04_AGENTS.MemoryDepartment.runner", "type": "import"} (file: None)
- {"metadata": {"alias": null, "kind": "from", "line": 3, "name": "MemoryAdvisor"}, "source": 1347, "target": "A_04_COMPONENTS.MemoryAdvisor.memory_advisor", "type": "import"} (file: None)
- {"metadata": {"alias": null, "kind": "from", "line": 4, "name": "MemoryDepartment"}, "source": 1285, "target": "A_04_AGENTS.MemoryDepartment.runner", "type": "import"} (file: None)
- {"metadata": {"alias": null, "kind": "from", "line": 4, "name": "MemoryDepartment"}, "source": 1287, "target": "A_04_AGENTS.MemoryDepartment.runner", "type": "import"} (file: None)
- {"metadata": {"alias": null, "kind": "from", "line": 4, "name": "MemoryDepartment"}, "source": 324, "target": "A_04_AGENTS.MemoryDepartment.runner", "type": "import"} (file: None)
- {"metadata": {"alias": null, "kind": "from", "line": 4, "name": "MemoryDepartment"}, "source": 338, "target": "A_04_AGENTS.MemoryDepartment.runner", "type": "import"} (file: None)
- {"metadata": {"context": "AgentLoopExecutor.__init__", "line": 10}, "source": 1114, "target": "ProjectHistory", "type": "call"} (file: None)
- {"metadata": {"context": "AttentionMemory.__init__", "line": 14}, "source": 1124, "target": "MemoryReplay", "type": "call"} (file: None)
- {"metadata": {"context": "BootstrapCore.__init__", "line": 15}, "source": 1495, "target": "SelfHealingMemory", "type": "call"} (file: None)
- {"metadata": {"context": "ButlerOSAdapter.__init__", "line": 12}, "source": 405, "target": "ProjectMemoryLoader", "type": "call"} (file: None)
- {"metadata": {"context": "ButlerOSAdapter.memory_summary", "line": 15}, "source": 405, "target": "get_memory_summary", "type": "call"} (file: None)
- {"metadata": {"context": "ButlerSystem.__init__", "line": 14}, "source": 1505, "target": "SelfHealingMemory", "type": "call"} (file: None)
- {"metadata": {"context": "ChatCoreBridge.__init__", "line": 7}, "source": 205, "target": "SemanticLayer", "type": "call"} (file: None)
- {"metadata": {"context": "ChatRouterMirror.__init__", "line": 7}, "source": 419, "target": "SemanticLayer", "type": "call"} (file: None)
- {"metadata": {"context": "ContextBudgetManager.__init__", "line": 15}, "source": 1136, "target": "AttentionMemory", "type": "call"} (file: None)
- {"metadata": {"context": "ContextBudgetManager.__init__", "line": 16}, "source": 1136, "target": "MemoryOrchestrator", "type": "call"} (file: None)
- {"metadata": {"context": "CoreKernel.__init__", "line": 9}, "source": 207, "target": "SemanticLayer", "type": "call"} (file: None)
- {"metadata": {"context": "CoreOrchestrator.__init__", "line": 7}, "source": 208, "target": "SemanticLayer", "type": "call"} (file: None)
- {"metadata": {"context": "CoreOrchestrator.__init__", "line": 8}, "source": 208, "target": "MemoryCore", "type": "call"} (file: None)
- {"metadata": {"context": "DispatcherAgent.__init__", "line": 25}, "source": 508, "target": "SemanticMemory", "type": "call"} (file: None)
- ... and 81 more

---

## CAPABILITY: ROUTER
**TOTAL EVIDENCE:** 118
**STATUS:** READY
**MAIN ENTRY:** SmartDispatcherV2

### FILES (canonical):
- A_09_GUARDIANS/BONE_CACHE/Dispatcher/Dispatcher_bone_20260626_182912.py
- A_09_GUARDIANS/BONE_CACHE/Dispatcher/Dispatcher_bone_20260626_214839.py
- A_10_BUTLER_OS/00_PRODUCTION/core/smart_router.py
- A_02_MANAGERS/dream_manager.py
- A_02_MANAGERS/smart_dispatcher.py
- A_02_MANAGERS/smart_dispatcher_v2.py
- A_02_MANAGERS/smart_dispatcher_v2.RECOVERY_TEMPLATE.py
- A_03_ORCHESTRATION/agent_router.py
- A_03_ORCHESTRATION/chat_router_mirror.py
- A_03_ORCHESTRATION/dispatcher_bridge.py
- A_03_ORCHESTRATION/dream_dispatcher_adapter.py
- A_03_ORCHESTRATION/router_integration.py
- A_03_ORCHESTRATION/router_registry.py
- A_04_AGENTS/professor.py

### CLASSES:
- AgentRouter (file: A_03_ORCHESTRATION/agent_router.py)
- ChatRouterMirror (file: A_03_ORCHESTRATION/chat_router_mirror.py)
- DispatcherAgent (file: A_04_AGENTS/professor.py)
- DispatcherBridge (file: A_03_ORCHESTRATION/dispatcher_bridge.py)
- DreamDispatcherAdapter (file: A_03_ORCHESTRATION/dream_dispatcher_adapter.py)
- FakeDispatcher (file: A_02_MANAGERS/dream_manager.py)
- RouterIntegration (file: A_03_ORCHESTRATION/router_integration.py)
- RouterRegistry (file: A_03_ORCHESTRATION/router_registry.py)
- SmartDispatcher (file: A_02_MANAGERS/smart_dispatcher.py)
- SmartDispatcherV2 (file: A_09_GUARDIANS/BONE_CACHE/Dispatcher/Dispatcher_bone_20260626_182912.py)
- SmartDispatcherV2 (file: A_09_GUARDIANS/BONE_CACHE/Dispatcher/Dispatcher_bone_20260626_214839.py)
- SmartDispatcherV2 (file: A_02_MANAGERS/smart_dispatcher_v2.py)
- SmartDispatcherV2 (file: A_02_MANAGERS/smart_dispatcher_v2.RECOVERY_TEMPLATE.py)
- SmartRouter (file: A_10_BUTLER_OS/00_PRODUCTION/core/smart_router.py)

### FUNCTIONS:

### CALLS:
- AgentRouter (file: 123)
- AgentRouter (file: 394)
- AgentRouter (file: A_03_ORCHESTRATION/agent_router.py)
- AgentRouter (file: 467)
- AgentRouter (file: A_03_ORCHESTRATION/router_integration.py)
- ChatRouterMirror (file: A_03_ORCHESTRATION/chat_router_mirror.py)
- DispatcherAgent (file: 116)
- DispatcherAgent (file: 241)
- DispatcherAgent (file: A_03_ORCHESTRATION/dream_dispatcher_adapter.py)
- DispatcherAgent (file: 465)
- DispatcherAgent (file: 480)
- DispatcherAgent (file: 615)
- DispatcherAgent (file: 631)
- FakeDispatcher (file: A_02_MANAGERS/dream_manager.py)
- RouterIntegration (file: 123)
- RouterIntegration (file: 1364)
- RouterIntegration (file: 1512)
- RouterIntegration (file: 1517)
- RouterIntegration (file: 414)
- RouterIntegration (file: 417)
- ... and 19 more

### DEPENDENCY_NODES:
- AgentRouter (file: None)
- ChatRouterMirror (file: None)
- DispatcherAgent (file: None)
- FakeDispatcher (file: None)
- RouterIntegration (file: None)
- RouterRegistry (file: None)
- SmartDispatcher (file: None)
- SmartDispatcherV2 (file: None)
- SmartRouter (file: None)

### EXECUTION_FACTS:
- PHASE_1_INIT::BOOTSTRAP: DONE
- PHASE_1_MULTITASK_TEST::TEST_TASK_A: DONE
- PHASE_1_MULTITASK_TEST::TEST_TASK_B: DONE
- PHASE_1_MULTITASK_TEST::TEST_TASK_C: DONE
- PHASE_1_TEST_DIAGNOSTICS::AUDIT_VERIFY_HEALTH: DONE
- PHASE_3_CLEANUP_AND_BACKUP::RUN_CORE_BACKUP: DONE
- TEST_PHASE_1::PHASE_1_TASK_A: DONE
- TEST_PHASE_1::PHASE_1_TASK_B: DONE
- TEST_PHASE_2::PHASE_2_TASK_C: DONE
- TEST_PHASE_2::PHASE_2_TASK_D: DONE

### GOALS_FACTS:
- active_goal: BUTLER_RECIPE_LIBRARY
- current_phase: ROADMAP_6_PHASE_4_RECIPES
- subgoal: ROADMAP_6_PHASE_4_RECIPES status=COMPLETED
- task: task_run_full_audit status=COMPLETED
- task: task_verify_contour status=COMPLETED
- weight: autonomy=0.6
- weight: stability=1.0

### LINKS:
- {"metadata": {"context": "ButlerInteractiveChat.__init__", "line": 38}, "source": 241, "target": "DispatcherAgent", "type": "call"} (file: None)
- {"metadata": {"context": "DispatcherScanner.scan", "line": 18}, "source": 549, "target": "SmartDispatcherV2", "type": "call"} (file: None)
- {"metadata": {"context": "DispatcherScanner.scan", "line": 18}, "source": 597, "target": "SmartDispatcherV2", "type": "call"} (file: None)
- {"metadata": {"context": "DreamDispatcherAdapter.__init__", "line": 9}, "source": 432, "target": "DispatcherAgent", "type": "call"} (file: None)
- {"metadata": {"context": "ProfessorAdapter.__init__", "line": 9}, "source": 465, "target": "DispatcherAgent", "type": "call"} (file: None)
- {"metadata": {"context": "RouterIntegration.__init__", "line": 21}, "source": 123, "target": "AgentRouter", "type": "call"} (file: None)
- {"metadata": {"context": "RouterIntegration.__init__", "line": 21}, "source": 467, "target": "AgentRouter", "type": "call"} (file: None)
- {"metadata": {"context": "RouterIntegration.__init__", "line": 22}, "source": 123, "target": "RouterRegistry", "type": "call"} (file: None)
- {"metadata": {"context": "RouterIntegration.__init__", "line": 22}, "source": 467, "target": "RouterRegistry", "type": "call"} (file: None)
- {"metadata": {"context": "RouterIntegration.__init__", "line": 24}, "source": 468, "target": "AgentRouter", "type": "call"} (file: None)
- {"metadata": {"context": "RouterIntegration.__init__", "line": 25}, "source": 468, "target": "RouterRegistry", "type": "call"} (file: None)
- {"metadata": {"context": "RuntimeDepartmentsDiscoveryAgent.discover", "line": 24}, "source": 534, "target": "SmartDispatcherV2", "type": "call"} (file: None)
- {"metadata": {"context": "RuntimeDepartmentsDiscoveryAgent.discover", "line": 24}, "source": 589, "target": "SmartDispatcherV2", "type": "call"} (file: None)
- {"metadata": {"context": "Worker.__init__", "line": 10}, "source": 480, "target": "DispatcherAgent", "type": "call"} (file: None)
- {"metadata": {"context": "Worker.__init__", "line": 35}, "source": 477, "target": "RouterRegistry", "type": "call"} (file: None)
- {"metadata": {"context": "main", "line": 233}, "source": 1364, "target": "RouterIntegration", "type": "call"} (file: None)
- {"metadata": {"context": "main", "line": 233}, "source": 417, "target": "RouterIntegration", "type": "call"} (file: None)
- {"metadata": {"context": "main", "line": 250}, "source": 414, "target": "RouterIntegration", "type": "call"} (file: None)
- {"metadata": {"context": null, "line": 10}, "source": 1393, "target": "SmartDispatcherV2", "type": "call"} (file: None)
- {"metadata": {"context": null, "line": 120}, "source": 338, "target": "SmartDispatcherV2", "type": "call"} (file: None)
- ... and 19 more

---

## CAPABILITY: DEPARTMENT
**TOTAL EVIDENCE:** 331
**STATUS:** READY
**MAIN ENTRY:** Department

### FILES (canonical):
- A_10_BUTLER_OS/00_PRODUCTION/core/department_contract.py
- A_99_TEST_DATA/runner_before_image_v2.py
- A_04_AGENTS/ArchiveDepartment/runner.py
- A_04_AGENTS/AudioDepartment/runner.py
- A_04_AGENTS/base_department.py
- A_04_AGENTS/CodingDepartment/runner.py
- A_04_AGENTS/DocumentsDepartment/runner.py
- A_04_AGENTS/ImageDepartment/runner.py
- A_04_AGENTS/MemoryDepartment/runner.py
- A_04_AGENTS/OpenDocumentDepartment/runner.py
- A_04_AGENTS/ProjectDocumentationDepartment/Core/Discovery/runtime_departments_discovery_agent.py
- A_04_AGENTS/ProjectDocumentationDepartment/runner.py
- A_04_AGENTS/SearchDepartment/runner.py
- A_04_AGENTS/TextDepartment/runner.py
- A_04_AGENTS/VideoDepartment/runner.py
- A_04_AGENTS/VisionDepartment/runner.py

### CLASSES:
- ArchiveDepartment (file: A_04_AGENTS/ArchiveDepartment/runner.py)
- AudioDepartment (file: A_04_AGENTS/AudioDepartment/runner.py)
- BaseDepartment (file: A_04_AGENTS/base_department.py)
- CodingDepartment (file: A_04_AGENTS/CodingDepartment/runner.py)
- Department (file: A_10_BUTLER_OS/00_PRODUCTION/core/department_contract.py)
- DocumentsDepartment (file: A_04_AGENTS/DocumentsDepartment/runner.py)
- ImageDepartment (file: A_99_TEST_DATA/runner_before_image_v2.py)
- ImageDepartment (file: A_04_AGENTS/ImageDepartment/runner.py)
- MemoryDepartment (file: A_04_AGENTS/MemoryDepartment/runner.py)
- OpenDocumentDepartment (file: A_04_AGENTS/OpenDocumentDepartment/runner.py)
- ProjectDocumentationDepartment (file: A_04_AGENTS/ProjectDocumentationDepartment/runner.py)
- RuntimeDepartmentsDiscoveryAgent (file: A_04_AGENTS/ProjectDocumentationDepartment/Core/Discovery/runtime_departments_discovery_agent.py)
- SearchDepartment (file: A_04_AGENTS/SearchDepartment/runner.py)
- TextDepartment (file: A_04_AGENTS/TextDepartment/runner.py)
- VideoDepartment (file: A_04_AGENTS/VideoDepartment/runner.py)
- VisionDepartment (file: A_04_AGENTS/VisionDepartment/runner.py)

### FUNCTIONS:

### CALLS:
- ArchiveDepartment (file: 1285)
- ArchiveDepartment (file: 1287)
- ArchiveDepartment (file: 1340)
- ArchiveDepartment (file: 324)
- ArchiveDepartment (file: 338)
- AudioDepartment (file: 1285)
- AudioDepartment (file: 1287)
- AudioDepartment (file: 1340)
- AudioDepartment (file: 324)
- AudioDepartment (file: 338)
- CodingDepartment (file: 1285)
- CodingDepartment (file: 1287)
- CodingDepartment (file: 1340)
- CodingDepartment (file: 324)
- CodingDepartment (file: 338)
- CodingDepartment (file: 490)
- DocumentsDepartment (file: 1285)
- DocumentsDepartment (file: 1287)
- DocumentsDepartment (file: 324)
- ImageDepartment (file: 1285)
- ... and 41 more

### DEPENDENCY_NODES:
- A_04_AGENTS.ArchiveDepartment.runner (file: None)
- A_04_AGENTS.AudioDepartment.runner (file: None)
- A_04_AGENTS.CodingDepartment.runner (file: None)
- A_04_AGENTS.DocumentsDepartment.runner (file: None)
- A_04_AGENTS.ImageDepartment.runner (file: None)
- A_04_AGENTS.MemoryDepartment.runner (file: None)
- A_04_AGENTS.OpenDocumentDepartment.runner (file: None)
- A_04_AGENTS.ProjectDocumentationDepartment.Core.engineering_pipeline (file: None)
- A_04_AGENTS.ProjectDocumentationDepartment.Core.evidence_doctor (file: None)
- A_04_AGENTS.ProjectDocumentationDepartment.runner (file: None)
- A_04_AGENTS.SearchDepartment.runner (file: None)
- A_04_AGENTS.TextDepartment.runner (file: None)
- A_04_AGENTS.VideoDepartment.runner (file: None)
- A_04_AGENTS.VisionDepartment.runner (file: None)
- A_04_AGENTS.base_department (file: None)
- ArchiveDepartment (file: None)
- AudioDepartment (file: None)
- CodingDepartment (file: None)
- DocumentsDepartment (file: None)
- ImageDepartment (file: None)
- ... and 8 more

### EXECUTION_FACTS:
- PHASE_1_INIT::BOOTSTRAP: DONE
- PHASE_1_MULTITASK_TEST::TEST_TASK_A: DONE
- PHASE_1_MULTITASK_TEST::TEST_TASK_B: DONE
- PHASE_1_MULTITASK_TEST::TEST_TASK_C: DONE
- PHASE_1_TEST_DIAGNOSTICS::AUDIT_VERIFY_HEALTH: DONE
- PHASE_3_CLEANUP_AND_BACKUP::RUN_CORE_BACKUP: DONE
- TEST_PHASE_1::PHASE_1_TASK_A: DONE
- TEST_PHASE_1::PHASE_1_TASK_B: DONE
- TEST_PHASE_2::PHASE_2_TASK_C: DONE
- TEST_PHASE_2::PHASE_2_TASK_D: DONE

### GOALS_FACTS:
- active_goal: BUTLER_RECIPE_LIBRARY
- current_phase: ROADMAP_6_PHASE_4_RECIPES
- subgoal: ROADMAP_6_PHASE_4_RECIPES status=COMPLETED
- task: task_run_full_audit status=COMPLETED
- task: task_verify_contour status=COMPLETED
- weight: autonomy=0.6
- weight: stability=1.0

### IMPORTS:
- A_04_AGENTS.ArchiveDepartment.runner (file: 1285)
- A_04_AGENTS.ArchiveDepartment.runner (file: 1287)
- A_04_AGENTS.ArchiveDepartment.runner (file: 1340)
- A_04_AGENTS.ArchiveDepartment.runner (file: 324)
- A_04_AGENTS.ArchiveDepartment.runner (file: 338)
- A_04_AGENTS.AudioDepartment.runner (file: 1285)
- A_04_AGENTS.AudioDepartment.runner (file: 1287)
- A_04_AGENTS.AudioDepartment.runner (file: 1340)
- A_04_AGENTS.AudioDepartment.runner (file: 324)
- A_04_AGENTS.AudioDepartment.runner (file: 338)
- A_04_AGENTS.CodingDepartment.runner (file: 1285)
- A_04_AGENTS.CodingDepartment.runner (file: 1287)
- A_04_AGENTS.CodingDepartment.runner (file: 1340)
- A_04_AGENTS.CodingDepartment.runner (file: 324)
- A_04_AGENTS.CodingDepartment.runner (file: 338)
- A_04_AGENTS.DocumentsDepartment.runner (file: 1285)
- A_04_AGENTS.DocumentsDepartment.runner (file: 1287)
- A_04_AGENTS.DocumentsDepartment.runner (file: 324)
- A_04_AGENTS.ImageDepartment.runner (file: 1285)
- A_04_AGENTS.ImageDepartment.runner (file: 1287)
- ... and 53 more

### LINKS:
- {"metadata": {"alias": "evidence_doctor", "kind": "from", "line": 5, "name": "dispatch"}, "source": 611, "target": "A_04_AGENTS.ProjectDocumentationDepartment.Core.evidence_doctor", "type": "import"} (file: None)
- {"metadata": {"alias": null, "kind": "from", "line": 1, "name": "BaseDepartment"}, "source": 486, "target": "A_04_AGENTS.base_department", "type": "import"} (file: None)
- {"metadata": {"alias": null, "kind": "from", "line": 1, "name": "BaseDepartment"}, "source": 505, "target": "A_04_AGENTS.base_department", "type": "import"} (file: None)
- {"metadata": {"alias": null, "kind": "from", "line": 1, "name": "BaseDepartment"}, "source": 623, "target": "A_04_AGENTS.base_department", "type": "import"} (file: None)
- {"metadata": {"alias": null, "kind": "from", "line": 1, "name": "CodingDepartment"}, "source": 1340, "target": "A_04_AGENTS.CodingDepartment.runner", "type": "import"} (file: None)
- {"metadata": {"alias": null, "kind": "from", "line": 1, "name": "SearchDepartment"}, "source": 1518, "target": "A_04_AGENTS.SearchDepartment.runner", "type": "import"} (file: None)
- {"metadata": {"alias": null, "kind": "from", "line": 10, "name": "ArchiveDepartment"}, "source": 1285, "target": "A_04_AGENTS.ArchiveDepartment.runner", "type": "import"} (file: None)
- {"metadata": {"alias": null, "kind": "from", "line": 10, "name": "ArchiveDepartment"}, "source": 1287, "target": "A_04_AGENTS.ArchiveDepartment.runner", "type": "import"} (file: None)
- {"metadata": {"alias": null, "kind": "from", "line": 10, "name": "ArchiveDepartment"}, "source": 324, "target": "A_04_AGENTS.ArchiveDepartment.runner", "type": "import"} (file: None)
- {"metadata": {"alias": null, "kind": "from", "line": 10, "name": "ArchiveDepartment"}, "source": 338, "target": "A_04_AGENTS.ArchiveDepartment.runner", "type": "import"} (file: None)
- {"metadata": {"alias": null, "kind": "from", "line": 11, "name": "SearchDepartment"}, "source": 1285, "target": "A_04_AGENTS.SearchDepartment.runner", "type": "import"} (file: None)
- {"metadata": {"alias": null, "kind": "from", "line": 11, "name": "SearchDepartment"}, "source": 1287, "target": "A_04_AGENTS.SearchDepartment.runner", "type": "import"} (file: None)
- {"metadata": {"alias": null, "kind": "from", "line": 11, "name": "SearchDepartment"}, "source": 324, "target": "A_04_AGENTS.SearchDepartment.runner", "type": "import"} (file: None)
- {"metadata": {"alias": null, "kind": "from", "line": 12, "name": "BaseDepartment"}, "source": 1389, "target": "A_04_AGENTS.base_department", "type": "import"} (file: None)
- {"metadata": {"alias": null, "kind": "from", "line": 12, "name": "BaseDepartment"}, "source": 499, "target": "A_04_AGENTS.base_department", "type": "import"} (file: None)
- {"metadata": {"alias": null, "kind": "from", "line": 12, "name": "DocumentsDepartment"}, "source": 1285, "target": "A_04_AGENTS.DocumentsDepartment.runner", "type": "import"} (file: None)
- {"metadata": {"alias": null, "kind": "from", "line": 12, "name": "DocumentsDepartment"}, "source": 1287, "target": "A_04_AGENTS.DocumentsDepartment.runner", "type": "import"} (file: None)
- {"metadata": {"alias": null, "kind": "from", "line": 12, "name": "DocumentsDepartment"}, "source": 324, "target": "A_04_AGENTS.DocumentsDepartment.runner", "type": "import"} (file: None)
- {"metadata": {"alias": null, "kind": "from", "line": 13, "name": "OpenDocumentDepartment"}, "source": 1285, "target": "A_04_AGENTS.OpenDocumentDepartment.runner", "type": "import"} (file: None)
- {"metadata": {"alias": null, "kind": "from", "line": 13, "name": "OpenDocumentDepartment"}, "source": 1287, "target": "A_04_AGENTS.OpenDocumentDepartment.runner", "type": "import"} (file: None)
- ... and 116 more

---

## CAPABILITY: VISION
**TOTAL EVIDENCE:** 111
**STATUS:** READY
**MAIN ENTRY:** ImageDepartment

### FILES (canonical):
- A_99_TEST_DATA/runner_before_image_v2.py
- A_03_ENGINES/Vision_Engine/GO.py
- A_03_HANDLERS/image_handler.py
- A_03_HANDLERS/ollama_vision_backend.py
- A_03_HANDLERS/vision_analyzer.py
- A_03_HANDLERS/vision_engine.py
- A_03_ORCHESTRATION/ConversationContext/ImageSession/image_session.py
- A_04_AGENTS/ImageDepartment/runner.py
- A_04_AGENTS/VisionDepartment/runner.py

### CLASSES:
- ImageDepartment (file: A_99_TEST_DATA/runner_before_image_v2.py)
- ImageDepartment (file: A_04_AGENTS/ImageDepartment/runner.py)
- ImageHandler (file: A_03_HANDLERS/image_handler.py)
- ImageSession (file: A_03_ORCHESTRATION/ConversationContext/ImageSession/image_session.py)
- OllamaVisionBackend (file: A_03_HANDLERS/ollama_vision_backend.py)
- VisionAnalyzer (file: A_03_HANDLERS/vision_analyzer.py)
- VisionDepartment (file: A_04_AGENTS/VisionDepartment/runner.py)
- VisionEngine (file: A_03_HANDLERS/vision_engine.py)

### FUNCTIONS:
- process_image (file: A_03_ENGINES/Vision_Engine/GO.py)

### CALLS:
- ImageDepartment (file: 1285)
- ImageDepartment (file: 1287)
- ImageDepartment (file: 1340)
- ImageDepartment (file: 1392)
- ImageDepartment (file: 1394)
- ImageDepartment (file: 324)
- ImageDepartment (file: 338)
- ImageDepartment (file: 414)
- ImageHandler (file: 387)
- OllamaVisionBackend (file: A_03_HANDLERS/vision_engine.py)
- VisionAnalyzer (file: 1357)
- VisionDepartment (file: 1285)
- VisionDepartment (file: 1287)
- VisionDepartment (file: 1340)
- VisionDepartment (file: 324)
- VisionDepartment (file: 338)
- VisionEngine (file: A_03_HANDLERS/image_handler.py)
- VisionEngine (file: 385)
- VisionEngine (file: 386)
- VisionEngine (file: A_03_HANDLERS/vision_analyzer.py)
- ... and 2 more

### DEPENDENCY_NODES:
- A_03_ORCHESTRATION.ConversationContext.ImageSession.image_session (file: None)
- A_04_AGENTS.ImageDepartment.runner (file: None)
- A_04_AGENTS.VisionDepartment.runner (file: None)
- ImageDepartment (file: None)
- ImageHandler (file: None)
- OllamaVisionBackend (file: None)
- VisionAnalyzer (file: None)
- VisionDepartment (file: None)
- VisionEngine (file: None)
- process_image (file: None)

### EXECUTION_FACTS:
- PHASE_1_INIT::BOOTSTRAP: DONE
- PHASE_1_MULTITASK_TEST::TEST_TASK_A: DONE
- PHASE_1_MULTITASK_TEST::TEST_TASK_B: DONE
- PHASE_1_MULTITASK_TEST::TEST_TASK_C: DONE
- PHASE_1_TEST_DIAGNOSTICS::AUDIT_VERIFY_HEALTH: DONE
- PHASE_3_CLEANUP_AND_BACKUP::RUN_CORE_BACKUP: DONE
- TEST_PHASE_1::PHASE_1_TASK_A: DONE
- TEST_PHASE_1::PHASE_1_TASK_B: DONE
- TEST_PHASE_2::PHASE_2_TASK_C: DONE
- TEST_PHASE_2::PHASE_2_TASK_D: DONE

### GOALS_FACTS:
- active_goal: BUTLER_RECIPE_LIBRARY
- current_phase: ROADMAP_6_PHASE_4_RECIPES
- subgoal: ROADMAP_6_PHASE_4_RECIPES status=COMPLETED
- task: task_run_full_audit status=COMPLETED
- task: task_verify_contour status=COMPLETED
- weight: autonomy=0.6
- weight: stability=1.0

### IMPORTS:
- A_03_ORCHESTRATION.ConversationContext.ImageSession.image_session (file: 426)
- A_03_ORCHESTRATION.ConversationContext.ImageSession.image_session (file: A_04_AGENTS/ImageDepartment/runner.py)
- A_04_AGENTS.ImageDepartment.runner (file: 1285)
- A_04_AGENTS.ImageDepartment.runner (file: 1287)
- A_04_AGENTS.ImageDepartment.runner (file: 1340)
- A_04_AGENTS.ImageDepartment.runner (file: 1392)
- A_04_AGENTS.ImageDepartment.runner (file: 1394)
- A_04_AGENTS.ImageDepartment.runner (file: 324)
- A_04_AGENTS.ImageDepartment.runner (file: 338)
- A_04_AGENTS.ImageDepartment.runner (file: 414)
- A_04_AGENTS.VisionDepartment.runner (file: 1285)
- A_04_AGENTS.VisionDepartment.runner (file: 1287)
- A_04_AGENTS.VisionDepartment.runner (file: 1340)
- A_04_AGENTS.VisionDepartment.runner (file: 324)
- A_04_AGENTS.VisionDepartment.runner (file: 338)

### LINKS:
- {"metadata": {"alias": null, "kind": "from", "line": 11, "name": "ImageSession"}, "source": 426, "target": "A_03_ORCHESTRATION.ConversationContext.ImageSession.image_session", "type": "import"} (file: None)
- {"metadata": {"alias": null, "kind": "from", "line": 13, "name": "ImageSession"}, "source": 499, "target": "A_03_ORCHESTRATION.ConversationContext.ImageSession.image_session", "type": "import"} (file: None)
- {"metadata": {"alias": null, "kind": "from", "line": 158, "name": "ImageDepartment"}, "source": 414, "target": "A_04_AGENTS.ImageDepartment.runner", "type": "import"} (file: None)
- {"metadata": {"alias": null, "kind": "from", "line": 3, "name": "VisionDepartment"}, "source": 1340, "target": "A_04_AGENTS.VisionDepartment.runner", "type": "import"} (file: None)
- {"metadata": {"alias": null, "kind": "from", "line": 4, "name": "ImageDepartment"}, "source": 1340, "target": "A_04_AGENTS.ImageDepartment.runner", "type": "import"} (file: None)
- {"metadata": {"alias": null, "kind": "from", "line": 5, "name": "VisionDepartment"}, "source": 1285, "target": "A_04_AGENTS.VisionDepartment.runner", "type": "import"} (file: None)
- {"metadata": {"alias": null, "kind": "from", "line": 5, "name": "VisionDepartment"}, "source": 1287, "target": "A_04_AGENTS.VisionDepartment.runner", "type": "import"} (file: None)
- {"metadata": {"alias": null, "kind": "from", "line": 5, "name": "VisionDepartment"}, "source": 324, "target": "A_04_AGENTS.VisionDepartment.runner", "type": "import"} (file: None)
- {"metadata": {"alias": null, "kind": "from", "line": 5, "name": "VisionDepartment"}, "source": 338, "target": "A_04_AGENTS.VisionDepartment.runner", "type": "import"} (file: None)
- {"metadata": {"alias": null, "kind": "from", "line": 6, "name": "ImageDepartment"}, "source": 1285, "target": "A_04_AGENTS.ImageDepartment.runner", "type": "import"} (file: None)
- {"metadata": {"alias": null, "kind": "from", "line": 6, "name": "ImageDepartment"}, "source": 1287, "target": "A_04_AGENTS.ImageDepartment.runner", "type": "import"} (file: None)
- {"metadata": {"alias": null, "kind": "from", "line": 6, "name": "ImageDepartment"}, "source": 324, "target": "A_04_AGENTS.ImageDepartment.runner", "type": "import"} (file: None)
- {"metadata": {"alias": null, "kind": "from", "line": 6, "name": "ImageDepartment"}, "source": 338, "target": "A_04_AGENTS.ImageDepartment.runner", "type": "import"} (file: None)
- {"metadata": {"alias": null, "kind": "from", "line": 7, "name": "ImageDepartment"}, "source": 1392, "target": "A_04_AGENTS.ImageDepartment.runner", "type": "import"} (file: None)
- {"metadata": {"alias": null, "kind": "from", "line": 9, "name": "ImageDepartment"}, "source": 1394, "target": "A_04_AGENTS.ImageDepartment.runner", "type": "import"} (file: None)
- {"metadata": {"context": "DispatcherAgent.__init__", "line": 24}, "source": 508, "target": "VisionEngine", "type": "call"} (file: None)
- {"metadata": {"context": "DispatcherAgent.__init__", "line": 35}, "source": 508, "target": "VisionEngine", "type": "call"} (file: None)
- {"metadata": {"context": "HandlerRegistry.__init__", "line": 22}, "source": 387, "target": "ImageHandler", "type": "call"} (file: None)
- {"metadata": {"context": "ImageHandler.__init__", "line": 20}, "source": 382, "target": "VisionEngine", "type": "call"} (file: None)
- {"metadata": {"context": "PDFHandler._extract_scanned_pdf_with_vision", "line": 113}, "source": 385, "target": "VisionEngine", "type": "call"} (file: None)
- ... and 18 more

---

## CAPABILITY: IMAGE
**TOTAL EVIDENCE:** 111
**STATUS:** READY
**MAIN ENTRY:** ImageDepartment

### FILES (canonical):
- A_99_TEST_DATA/runner_before_image_v2.py
- A_03_ENGINES/Vision_Engine/GO.py
- A_03_HANDLERS/image_handler.py
- A_03_HANDLERS/ollama_vision_backend.py
- A_03_HANDLERS/vision_analyzer.py
- A_03_HANDLERS/vision_engine.py
- A_03_ORCHESTRATION/ConversationContext/ImageSession/image_session.py
- A_04_AGENTS/ImageDepartment/runner.py
- A_04_AGENTS/VisionDepartment/runner.py

### CLASSES:
- ImageDepartment (file: A_99_TEST_DATA/runner_before_image_v2.py)
- ImageDepartment (file: A_04_AGENTS/ImageDepartment/runner.py)
- ImageHandler (file: A_03_HANDLERS/image_handler.py)
- ImageSession (file: A_03_ORCHESTRATION/ConversationContext/ImageSession/image_session.py)
- OllamaVisionBackend (file: A_03_HANDLERS/ollama_vision_backend.py)
- VisionAnalyzer (file: A_03_HANDLERS/vision_analyzer.py)
- VisionDepartment (file: A_04_AGENTS/VisionDepartment/runner.py)
- VisionEngine (file: A_03_HANDLERS/vision_engine.py)

### FUNCTIONS:
- process_image (file: A_03_ENGINES/Vision_Engine/GO.py)

### CALLS:
- ImageDepartment (file: 1285)
- ImageDepartment (file: 1287)
- ImageDepartment (file: 1340)
- ImageDepartment (file: 1392)
- ImageDepartment (file: 1394)
- ImageDepartment (file: 324)
- ImageDepartment (file: 338)
- ImageDepartment (file: 414)
- ImageHandler (file: 387)
- OllamaVisionBackend (file: A_03_HANDLERS/vision_engine.py)
- VisionAnalyzer (file: 1357)
- VisionDepartment (file: 1285)
- VisionDepartment (file: 1287)
- VisionDepartment (file: 1340)
- VisionDepartment (file: 324)
- VisionDepartment (file: 338)
- VisionEngine (file: A_03_HANDLERS/image_handler.py)
- VisionEngine (file: 385)
- VisionEngine (file: 386)
- VisionEngine (file: A_03_HANDLERS/vision_analyzer.py)
- ... and 2 more

### DEPENDENCY_NODES:
- A_03_ORCHESTRATION.ConversationContext.ImageSession.image_session (file: None)
- A_04_AGENTS.ImageDepartment.runner (file: None)
- A_04_AGENTS.VisionDepartment.runner (file: None)
- ImageDepartment (file: None)
- ImageHandler (file: None)
- OllamaVisionBackend (file: None)
- VisionAnalyzer (file: None)
- VisionDepartment (file: None)
- VisionEngine (file: None)
- process_image (file: None)

### EXECUTION_FACTS:
- PHASE_1_INIT::BOOTSTRAP: DONE
- PHASE_1_MULTITASK_TEST::TEST_TASK_A: DONE
- PHASE_1_MULTITASK_TEST::TEST_TASK_B: DONE
- PHASE_1_MULTITASK_TEST::TEST_TASK_C: DONE
- PHASE_1_TEST_DIAGNOSTICS::AUDIT_VERIFY_HEALTH: DONE
- PHASE_3_CLEANUP_AND_BACKUP::RUN_CORE_BACKUP: DONE
- TEST_PHASE_1::PHASE_1_TASK_A: DONE
- TEST_PHASE_1::PHASE_1_TASK_B: DONE
- TEST_PHASE_2::PHASE_2_TASK_C: DONE
- TEST_PHASE_2::PHASE_2_TASK_D: DONE

### GOALS_FACTS:
- active_goal: BUTLER_RECIPE_LIBRARY
- current_phase: ROADMAP_6_PHASE_4_RECIPES
- subgoal: ROADMAP_6_PHASE_4_RECIPES status=COMPLETED
- task: task_run_full_audit status=COMPLETED
- task: task_verify_contour status=COMPLETED
- weight: autonomy=0.6
- weight: stability=1.0

### IMPORTS:
- A_03_ORCHESTRATION.ConversationContext.ImageSession.image_session (file: 426)
- A_03_ORCHESTRATION.ConversationContext.ImageSession.image_session (file: A_04_AGENTS/ImageDepartment/runner.py)
- A_04_AGENTS.ImageDepartment.runner (file: 1285)
- A_04_AGENTS.ImageDepartment.runner (file: 1287)
- A_04_AGENTS.ImageDepartment.runner (file: 1340)
- A_04_AGENTS.ImageDepartment.runner (file: 1392)
- A_04_AGENTS.ImageDepartment.runner (file: 1394)
- A_04_AGENTS.ImageDepartment.runner (file: 324)
- A_04_AGENTS.ImageDepartment.runner (file: 338)
- A_04_AGENTS.ImageDepartment.runner (file: 414)
- A_04_AGENTS.VisionDepartment.runner (file: 1285)
- A_04_AGENTS.VisionDepartment.runner (file: 1287)
- A_04_AGENTS.VisionDepartment.runner (file: 1340)
- A_04_AGENTS.VisionDepartment.runner (file: 324)
- A_04_AGENTS.VisionDepartment.runner (file: 338)

### LINKS:
- {"metadata": {"alias": null, "kind": "from", "line": 11, "name": "ImageSession"}, "source": 426, "target": "A_03_ORCHESTRATION.ConversationContext.ImageSession.image_session", "type": "import"} (file: None)
- {"metadata": {"alias": null, "kind": "from", "line": 13, "name": "ImageSession"}, "source": 499, "target": "A_03_ORCHESTRATION.ConversationContext.ImageSession.image_session", "type": "import"} (file: None)
- {"metadata": {"alias": null, "kind": "from", "line": 158, "name": "ImageDepartment"}, "source": 414, "target": "A_04_AGENTS.ImageDepartment.runner", "type": "import"} (file: None)
- {"metadata": {"alias": null, "kind": "from", "line": 3, "name": "VisionDepartment"}, "source": 1340, "target": "A_04_AGENTS.VisionDepartment.runner", "type": "import"} (file: None)
- {"metadata": {"alias": null, "kind": "from", "line": 4, "name": "ImageDepartment"}, "source": 1340, "target": "A_04_AGENTS.ImageDepartment.runner", "type": "import"} (file: None)
- {"metadata": {"alias": null, "kind": "from", "line": 5, "name": "VisionDepartment"}, "source": 1285, "target": "A_04_AGENTS.VisionDepartment.runner", "type": "import"} (file: None)
- {"metadata": {"alias": null, "kind": "from", "line": 5, "name": "VisionDepartment"}, "source": 1287, "target": "A_04_AGENTS.VisionDepartment.runner", "type": "import"} (file: None)
- {"metadata": {"alias": null, "kind": "from", "line": 5, "name": "VisionDepartment"}, "source": 324, "target": "A_04_AGENTS.VisionDepartment.runner", "type": "import"} (file: None)
- {"metadata": {"alias": null, "kind": "from", "line": 5, "name": "VisionDepartment"}, "source": 338, "target": "A_04_AGENTS.VisionDepartment.runner", "type": "import"} (file: None)
- {"metadata": {"alias": null, "kind": "from", "line": 6, "name": "ImageDepartment"}, "source": 1285, "target": "A_04_AGENTS.ImageDepartment.runner", "type": "import"} (file: None)
- {"metadata": {"alias": null, "kind": "from", "line": 6, "name": "ImageDepartment"}, "source": 1287, "target": "A_04_AGENTS.ImageDepartment.runner", "type": "import"} (file: None)
- {"metadata": {"alias": null, "kind": "from", "line": 6, "name": "ImageDepartment"}, "source": 324, "target": "A_04_AGENTS.ImageDepartment.runner", "type": "import"} (file: None)
- {"metadata": {"alias": null, "kind": "from", "line": 6, "name": "ImageDepartment"}, "source": 338, "target": "A_04_AGENTS.ImageDepartment.runner", "type": "import"} (file: None)
- {"metadata": {"alias": null, "kind": "from", "line": 7, "name": "ImageDepartment"}, "source": 1392, "target": "A_04_AGENTS.ImageDepartment.runner", "type": "import"} (file: None)
- {"metadata": {"alias": null, "kind": "from", "line": 9, "name": "ImageDepartment"}, "source": 1394, "target": "A_04_AGENTS.ImageDepartment.runner", "type": "import"} (file: None)
- {"metadata": {"context": "DispatcherAgent.__init__", "line": 24}, "source": 508, "target": "VisionEngine", "type": "call"} (file: None)
- {"metadata": {"context": "DispatcherAgent.__init__", "line": 35}, "source": 508, "target": "VisionEngine", "type": "call"} (file: None)
- {"metadata": {"context": "HandlerRegistry.__init__", "line": 22}, "source": 387, "target": "ImageHandler", "type": "call"} (file: None)
- {"metadata": {"context": "ImageHandler.__init__", "line": 20}, "source": 382, "target": "VisionEngine", "type": "call"} (file: None)
- {"metadata": {"context": "PDFHandler._extract_scanned_pdf_with_vision", "line": 113}, "source": 385, "target": "VisionEngine", "type": "call"} (file: None)
- ... and 18 more

---

## CAPABILITY: SEARCH
**TOTAL EVIDENCE:** 58
**STATUS:** READY
**MAIN ENTRY:** SearchDepartment

### FILES (canonical):
- A_07_MEMORY/catalog_search_bridge.py
- A_07_MEMORY/search_engine.py
- A_07_MEMORY/semantic_query_parser.py
- A_04_AGENTS/SearchDepartment/runner.py

### CLASSES:
- CatalogSearchBridge (file: A_07_MEMORY/catalog_search_bridge.py)
- SearchDepartment (file: A_04_AGENTS/SearchDepartment/runner.py)
- SemanticQueryParser (file: A_07_MEMORY/semantic_query_parser.py)
- SemanticSearchEngine (file: A_07_MEMORY/search_engine.py)

### FUNCTIONS:

### CALLS:
- CatalogSearchBridge (file: A_04_AGENTS/SearchDepartment/runner.py)
- SearchDepartment (file: 1285)
- SearchDepartment (file: 1287)
- SearchDepartment (file: 1518)
- SearchDepartment (file: 1519)
- SearchDepartment (file: 324)
- SemanticQueryParser (file: 1179)
- SemanticQueryParser (file: A_07_MEMORY/semantic_query_parser.py)
- SemanticQueryParser (file: 1216)
- SemanticSearchEngine (file: 1141)
- SemanticSearchEngine (file: 1354)

### DEPENDENCY_NODES:
- A_04_AGENTS.SearchDepartment.runner (file: None)
- CatalogSearchBridge (file: None)
- SearchDepartment (file: None)
- SemanticQueryParser (file: None)
- SemanticSearchEngine (file: None)

### EXECUTION_FACTS:
- PHASE_1_INIT::BOOTSTRAP: DONE
- PHASE_1_MULTITASK_TEST::TEST_TASK_A: DONE
- PHASE_1_MULTITASK_TEST::TEST_TASK_B: DONE
- PHASE_1_MULTITASK_TEST::TEST_TASK_C: DONE
- PHASE_1_TEST_DIAGNOSTICS::AUDIT_VERIFY_HEALTH: DONE
- PHASE_3_CLEANUP_AND_BACKUP::RUN_CORE_BACKUP: DONE
- TEST_PHASE_1::PHASE_1_TASK_A: DONE
- TEST_PHASE_1::PHASE_1_TASK_B: DONE
- TEST_PHASE_2::PHASE_2_TASK_C: DONE
- TEST_PHASE_2::PHASE_2_TASK_D: DONE

### GOALS_FACTS:
- active_goal: BUTLER_RECIPE_LIBRARY
- current_phase: ROADMAP_6_PHASE_4_RECIPES
- subgoal: ROADMAP_6_PHASE_4_RECIPES status=COMPLETED
- task: task_run_full_audit status=COMPLETED
- task: task_verify_contour status=COMPLETED
- weight: autonomy=0.6
- weight: stability=1.0

### IMPORTS:
- A_04_AGENTS.SearchDepartment.runner (file: 1285)
- A_04_AGENTS.SearchDepartment.runner (file: 1287)
- A_04_AGENTS.SearchDepartment.runner (file: 1518)
- A_04_AGENTS.SearchDepartment.runner (file: 1519)
- A_04_AGENTS.SearchDepartment.runner (file: 324)

### LINKS:
- {"metadata": {"alias": null, "kind": "from", "line": 1, "name": "SearchDepartment"}, "source": 1518, "target": "A_04_AGENTS.SearchDepartment.runner", "type": "import"} (file: None)
- {"metadata": {"alias": null, "kind": "from", "line": 11, "name": "SearchDepartment"}, "source": 1285, "target": "A_04_AGENTS.SearchDepartment.runner", "type": "import"} (file: None)
- {"metadata": {"alias": null, "kind": "from", "line": 11, "name": "SearchDepartment"}, "source": 1287, "target": "A_04_AGENTS.SearchDepartment.runner", "type": "import"} (file: None)
- {"metadata": {"alias": null, "kind": "from", "line": 11, "name": "SearchDepartment"}, "source": 324, "target": "A_04_AGENTS.SearchDepartment.runner", "type": "import"} (file: None)
- {"metadata": {"alias": null, "kind": "from", "line": 3, "name": "SearchDepartment"}, "source": 1519, "target": "A_04_AGENTS.SearchDepartment.runner", "type": "import"} (file: None)
- {"metadata": {"context": "MemoryAdvisor.__init__", "line": 13}, "source": 1141, "target": "SemanticSearchEngine", "type": "call"} (file: None)
- {"metadata": {"context": "SearchDepartment.__init__", "line": 11}, "source": 616, "target": "CatalogSearchBridge", "type": "call"} (file: None)
- {"metadata": {"context": "SemanticCore.__init__", "line": 26}, "source": 1179, "target": "SemanticQueryParser", "type": "call"} (file: None)
- {"metadata": {"context": "SmartDispatcherV2.__init__", "line": 25}, "source": 1285, "target": "SearchDepartment", "type": "call"} (file: None)
- {"metadata": {"context": "SmartDispatcherV2.__init__", "line": 25}, "source": 1287, "target": "SearchDepartment", "type": "call"} (file: None)
- {"metadata": {"context": "SmartDispatcherV2.__init__", "line": 28}, "source": 324, "target": "SearchDepartment", "type": "call"} (file: None)
- {"metadata": {"context": "run_tests", "line": 62}, "source": 1354, "target": "SemanticSearchEngine", "type": "call"} (file: None)
- {"metadata": {"context": null, "line": 11}, "source": 1216, "target": "SemanticQueryParser", "type": "call"} (file: None)
- {"metadata": {"context": null, "line": 48}, "source": 1190, "target": "SemanticQueryParser", "type": "call"} (file: None)
- {"metadata": {"context": null, "line": 4}, "source": 1518, "target": "SearchDepartment", "type": "call"} (file: None)
- {"metadata": {"context": null, "line": 5}, "source": 1519, "target": "SearchDepartment", "type": "call"} (file: None)

---

## CAPABILITY: CODING
**TOTAL EVIDENCE:** 62
**STATUS:** READY
**MAIN ENTRY:** CodingDepartment

### FILES (canonical):
- A_01_CORE/memory_guardian.py
- A_03_HANDLERS/code_detector.py
- A_03_HANDLERS/code_handler.py
- A_03_ORCHESTRATION/editor_patch.py
- A_04_AGENTS/CodingDepartment/runner.py

### CLASSES:
- CodeHandler (file: A_03_HANDLERS/code_handler.py)
- CodingDepartment (file: A_04_AGENTS/CodingDepartment/runner.py)
- InlineCodeEditor (file: A_03_ORCHESTRATION/editor_patch.py)

### FUNCTIONS:
- check_code_layer (file: A_01_CORE/memory_guardian.py)
- looks_like_code (file: A_03_HANDLERS/code_detector.py)

### CALLS:
- CodeHandler (file: 387)
- CodingDepartment (file: 1285)
- CodingDepartment (file: 1287)
- CodingDepartment (file: 1340)
- CodingDepartment (file: 324)
- CodingDepartment (file: 338)
- CodingDepartment (file: 490)
- InlineCodeEditor (file: 1345)
- _looks_like_code (file: 390)
- check_code_layer (file: A_01_CORE/memory_guardian.py)
- looks_like_code (file: 385)

### DEPENDENCY_NODES:
- A_04_AGENTS.CodingDepartment.runner (file: None)
- CodeHandler (file: None)
- CodingDepartment (file: None)
- InlineCodeEditor (file: None)
- _looks_like_code (file: None)
- check_code_layer (file: None)
- looks_like_code (file: None)

### EXECUTION_FACTS:
- PHASE_1_INIT::BOOTSTRAP: DONE
- PHASE_1_MULTITASK_TEST::TEST_TASK_A: DONE
- PHASE_1_MULTITASK_TEST::TEST_TASK_B: DONE
- PHASE_1_MULTITASK_TEST::TEST_TASK_C: DONE
- PHASE_1_TEST_DIAGNOSTICS::AUDIT_VERIFY_HEALTH: DONE
- PHASE_3_CLEANUP_AND_BACKUP::RUN_CORE_BACKUP: DONE
- TEST_PHASE_1::PHASE_1_TASK_A: DONE
- TEST_PHASE_1::PHASE_1_TASK_B: DONE
- TEST_PHASE_2::PHASE_2_TASK_C: DONE
- TEST_PHASE_2::PHASE_2_TASK_D: DONE

### GOALS_FACTS:
- active_goal: BUTLER_RECIPE_LIBRARY
- current_phase: ROADMAP_6_PHASE_4_RECIPES
- subgoal: ROADMAP_6_PHASE_4_RECIPES status=COMPLETED
- task: task_run_full_audit status=COMPLETED
- task: task_verify_contour status=COMPLETED
- weight: autonomy=0.6
- weight: stability=1.0

### IMPORTS:
- A_04_AGENTS.CodingDepartment.runner (file: 1285)
- A_04_AGENTS.CodingDepartment.runner (file: 1287)
- A_04_AGENTS.CodingDepartment.runner (file: 1340)
- A_04_AGENTS.CodingDepartment.runner (file: 324)
- A_04_AGENTS.CodingDepartment.runner (file: 338)

### LINKS:
- {"metadata": {"alias": null, "kind": "from", "line": 1, "name": "CodingDepartment"}, "source": 1340, "target": "A_04_AGENTS.CodingDepartment.runner", "type": "import"} (file: None)
- {"metadata": {"alias": null, "kind": "from", "line": 3, "name": "CodingDepartment"}, "source": 1285, "target": "A_04_AGENTS.CodingDepartment.runner", "type": "import"} (file: None)
- {"metadata": {"alias": null, "kind": "from", "line": 3, "name": "CodingDepartment"}, "source": 1287, "target": "A_04_AGENTS.CodingDepartment.runner", "type": "import"} (file: None)
- {"metadata": {"alias": null, "kind": "from", "line": 3, "name": "CodingDepartment"}, "source": 324, "target": "A_04_AGENTS.CodingDepartment.runner", "type": "import"} (file: None)
- {"metadata": {"alias": null, "kind": "from", "line": 3, "name": "CodingDepartment"}, "source": 338, "target": "A_04_AGENTS.CodingDepartment.runner", "type": "import"} (file: None)
- {"metadata": {"context": "HandlerRegistry.__init__", "line": 17}, "source": 387, "target": "CodeHandler", "type": "call"} (file: None)
- {"metadata": {"context": "PDFHandler._extract_scanned_pdf_with_vision", "line": 172}, "source": 385, "target": "looks_like_code", "type": "call"} (file: None)
- {"metadata": {"context": "PDFHandler._extract_text_pdf", "line": 76}, "source": 385, "target": "looks_like_code", "type": "call"} (file: None)
- {"metadata": {"context": "SmartDispatcherV2.__init__", "line": 22}, "source": 338, "target": "CodingDepartment", "type": "call"} (file: None)
- {"metadata": {"context": "SmartDispatcherV2.__init__", "line": 27}, "source": 1285, "target": "CodingDepartment", "type": "call"} (file: None)
- {"metadata": {"context": "SmartDispatcherV2.__init__", "line": 27}, "source": 1287, "target": "CodingDepartment", "type": "call"} (file: None)
- {"metadata": {"context": "SmartDispatcherV2.__init__", "line": 32}, "source": 324, "target": "CodingDepartment", "type": "call"} (file: None)
- {"metadata": {"context": "VisionAnalyzer.analyze", "line": 53}, "source": 390, "target": "_looks_like_code", "type": "call"} (file: None)
- {"metadata": {"context": "run_memory_guardian", "line": 201}, "source": 219, "target": "check_code_layer", "type": "call"} (file: None)
- {"metadata": {"context": null, "line": 11}, "source": 1340, "target": "CodingDepartment", "type": "call"} (file: None)
- {"metadata": {"context": null, "line": 3}, "source": 1345, "target": "InlineCodeEditor", "type": "call"} (file: None)
- {"metadata": {"context": null, "line": 5}, "source": 490, "target": "CodingDepartment", "type": "call"} (file: None)

---

## CAPABILITY: SECURITY
**TOTAL EVIDENCE:** 56
**STATUS:** READY
**MAIN ENTRY:** RecipeQueueWatcher

### FILES (canonical):
- A_01_CORE/memory_guardian.py
- A_01_CORE/system_guardian.py
- A_02_MANAGERS/ExecutionMonitor/execution_monitor.py
- A_02_MANAGERS/TaskRunner/recipe_queue_watcher.py
- A_02_MANAGERS/TaskRunner/security_validator.py

### CLASSES:
- ExecutionMonitor (file: A_02_MANAGERS/ExecutionMonitor/execution_monitor.py)
- RecipeQueueWatcher (file: A_02_MANAGERS/TaskRunner/recipe_queue_watcher.py)
- SecurityValidator (file: A_02_MANAGERS/TaskRunner/security_validator.py)
- SecurityViolation (file: A_02_MANAGERS/TaskRunner/security_validator.py)

### FUNCTIONS:
- run_guardian (file: A_01_CORE/system_guardian.py)
- run_memory_guardian (file: A_01_CORE/memory_guardian.py)

### CALLS:
- ExecutionMonitor (file: A_02_MANAGERS/ExecutionMonitor/execution_monitor.py)
- RecipeQueueWatcher (file: A_02_MANAGERS/TaskRunner/recipe_queue_watcher.py)
- RecipeQueueWatcher (file: 357)
- RecipeQueueWatcher (file: 358)
- SecurityViolation (file: A_02_MANAGERS/TaskRunner/security_validator.py)
- run_guardian (file: A_01_CORE/system_guardian.py)
- run_memory_guardian (file: 1486)
- run_memory_guardian (file: A_01_CORE/memory_guardian.py)

### DEPENDENCY_NODES:
- A_02_MANAGERS.ExecutionMonitor.execution_history (file: None)
- A_02_MANAGERS.ExecutionMonitor.execution_state (file: None)
- A_02_MANAGERS.ExecutionMonitor.system_state (file: None)
- ExecutionMonitor (file: None)
- RecipeQueueWatcher (file: None)
- SecurityViolation (file: None)
- run_guardian (file: None)
- run_memory_guardian (file: None)

### EXECUTION_FACTS:
- PHASE_1_INIT::BOOTSTRAP: DONE
- PHASE_1_MULTITASK_TEST::TEST_TASK_A: DONE
- PHASE_1_MULTITASK_TEST::TEST_TASK_B: DONE
- PHASE_1_MULTITASK_TEST::TEST_TASK_C: DONE
- PHASE_1_TEST_DIAGNOSTICS::AUDIT_VERIFY_HEALTH: DONE
- PHASE_3_CLEANUP_AND_BACKUP::RUN_CORE_BACKUP: DONE
- TEST_PHASE_1::PHASE_1_TASK_A: DONE
- TEST_PHASE_1::PHASE_1_TASK_B: DONE
- TEST_PHASE_2::PHASE_2_TASK_C: DONE
- TEST_PHASE_2::PHASE_2_TASK_D: DONE

### GOALS_FACTS:
- active_goal: BUTLER_RECIPE_LIBRARY
- current_phase: ROADMAP_6_PHASE_4_RECIPES
- subgoal: ROADMAP_6_PHASE_4_RECIPES status=COMPLETED
- task: task_run_full_audit status=COMPLETED
- task: task_verify_contour status=COMPLETED
- weight: autonomy=0.6
- weight: stability=1.0

### IMPORTS:
- A_02_MANAGERS.ExecutionMonitor.execution_history (file: 294)
- A_02_MANAGERS.ExecutionMonitor.execution_state (file: 295)
- A_02_MANAGERS.ExecutionMonitor.system_state (file: 305)

### LINKS:
- {"metadata": {"alias": null, "kind": "from", "line": 11, "name": "ExecutionHistory"}, "source": 294, "target": "A_02_MANAGERS.ExecutionMonitor.execution_history", "type": "import"} (file: None)
- {"metadata": {"alias": null, "kind": "from", "line": 14, "name": "ExecutionState"}, "source": 295, "target": "A_02_MANAGERS.ExecutionMonitor.execution_state", "type": "import"} (file: None)
- {"metadata": {"alias": null, "kind": "from", "line": 9, "name": "SystemState"}, "source": 305, "target": "A_02_MANAGERS.ExecutionMonitor.system_state", "type": "import"} (file: None)
- {"metadata": {"context": "SecurityValidator.validate", "line": 41}, "source": 359, "target": "SecurityViolation", "type": "call"} (file: None)
- {"metadata": {"context": "SecurityValidator.validate", "line": 51}, "source": 359, "target": "SecurityViolation", "type": "call"} (file: None)
- {"metadata": {"context": "execute_repair", "line": 88}, "source": 1486, "target": "run_memory_guardian", "type": "call"} (file: None)
- {"metadata": {"context": "main", "line": 118}, "source": 1486, "target": "run_memory_guardian", "type": "call"} (file: None)
- {"metadata": {"context": "main", "line": 121}, "source": 1486, "target": "run_memory_guardian", "type": "call"} (file: None)
- {"metadata": {"context": "run", "line": 21}, "source": 357, "target": "RecipeQueueWatcher", "type": "call"} (file: None)
- {"metadata": {"context": "run_once", "line": 25}, "source": 358, "target": "RecipeQueueWatcher", "type": "call"} (file: None)
- {"metadata": {"context": null, "line": 144}, "source": 231, "target": "run_guardian", "type": "call"} (file: None)
- {"metadata": {"context": null, "line": 229}, "source": 219, "target": "run_memory_guardian", "type": "call"} (file: None)
- {"metadata": {"context": null, "line": 39}, "source": 293, "target": "ExecutionMonitor", "type": "call"} (file: None)
- {"metadata": {"context": null, "line": 39}, "source": 350, "target": "RecipeQueueWatcher", "type": "call"} (file: None)

---

## CAPABILITY: EXECUTION
**TOTAL EVIDENCE:** 454
**STATUS:** READY
**MAIN ENTRY:** run_self_test

### FILES (canonical):
- A_07_CONFIG/execution_context_schema.py
- A_07_CONFIG/execution_policy_schema.py
- A_07_CONFIG/recipe_schema.py
- A_07_MEMORY/agent_loop_executor.py
- A_07_MEMORY/agent_runtime_v2.py
- A_07_MEMORY/execution_registry.py
- A_07_MEMORY/png_workflow_memory.py
- A_09_TESTS/test_memory_advisor.py
- A_09_TESTS/test_pdf_ocr_pipeline.py
- A_09_TESTS/test_project_auditor.py
- A_09_TESTS/test_search_engine.py
- A_09_TESTS/test_vision_analyzer.py
- Butler_Gate.py
- INIT_OMEGA.py
- restore_full_project.py
- RUN_PIPELINE.py
- RUN_PIPELINE_V12.py
- safe_change.py
- A_01_CORE/execution_loop.py
- A_01_CORE/task_feeder.py
- A_01_CORE/test_db.py
- A_02_MANAGERS/ArchitectAgent/planner_pipeline.py
- A_02_MANAGERS/ArchitectAgent/queue_manager.py
- A_02_MANAGERS/ArchitectAgent/recipe_builder.py
- A_02_MANAGERS/ArchitectAgent/recipe_generator.py
- A_02_MANAGERS/ArchitectAgent/task_contract_builder.py
- A_02_MANAGERS/ExecutionMonitor/execution_history.py
- A_02_MANAGERS/ExecutionMonitor/execution_monitor.py
- A_02_MANAGERS/ExecutionMonitor/execution_state.py
- A_02_MANAGERS/Planner/task_planner.py
- A_02_MANAGERS/queue_manager.py
- A_02_MANAGERS/recipe_generator.py
- A_02_MANAGERS/recipe_validator.py
- A_02_MANAGERS/TaskRunner/execution_result.py
- A_02_MANAGERS/TaskRunner/ExecutionAdapters/base_adapter.py
- A_02_MANAGERS/TaskRunner/ExecutionAdapters/powershell_adapter.py
- A_02_MANAGERS/TaskRunner/ExecutionAdapters/python_adapter.py
- A_02_MANAGERS/TaskRunner/executor_factory.py
- A_02_MANAGERS/TaskRunner/recipe_builder.py
- A_02_MANAGERS/TaskRunner/recipe_executor.py
- A_02_MANAGERS/TaskRunner/recipe_loader.py
- A_02_MANAGERS/TaskRunner/recipe_queue_watcher.py
- A_02_MANAGERS/TaskRunner/recipe_writer.py
- A_02_MANAGERS/TaskRunner/runner.py
- A_03_EXECUTORS/executor.py
- A_03_HANDLERS/pdf_ocr_pipeline.py
- A_03_ORCHESTRATION/butler_harness.py
- A_03_ORCHESTRATION/chat_router.CLEAN_UTF8.py
- A_03_ORCHESTRATION/chat_router.HYBRID_WORK.after_import.py
- A_03_ORCHESTRATION/chat_router.HYBRID_WORK.after_resolver.py
- A_03_ORCHESTRATION/chat_router.HYBRID_WORK.hybrid_ok.py
- A_03_ORCHESTRATION/chat_router.HYBRID_WORK.py
- A_03_ORCHESTRATION/chat_router.py
- A_03_ORCHESTRATION/chat_router.STABLE_BEFORE_HYBRID.py
- A_03_ORCHESTRATION/chat_router.STABLE_TEST.py
- A_03_ORCHESTRATION/chat_router.WORKING_RUSSIAN_OK.py
- A_03_ORCHESTRATION/chat_router_test_restore.py
- A_03_ORCHESTRATION/guards/integration_test_guard.py
- A_03_ORCHESTRATION/session_queue.py
- A_04_AGENTS/ProjectDocumentationDepartment/Core/Discovery/execution_registry_discovery_agent.py
- A_04_AGENTS/ProjectDocumentationDepartment/Core/engineering_pipeline.py
- A_04_AGENTS/ProjectDocumentationDepartment/Core/Scanners/execution_scanner.py
- A_04_AGENTS/ProjectDocumentationDepartment/Core/Scanners/harness_scanner.py

### CLASSES:
- AgentLoopExecutor (file: A_07_MEMORY/agent_loop_executor.py)
- BaseExecutionAdapter (file: A_02_MANAGERS/TaskRunner/ExecutionAdapters/base_adapter.py)
- ButlerHarness (file: A_03_ORCHESTRATION/butler_harness.py)
- EngineeringPipeline (file: A_04_AGENTS/ProjectDocumentationDepartment/Core/engineering_pipeline.py)
- ExecutionContext (file: A_07_CONFIG/execution_context_schema.py)
- ExecutionHistory (file: A_02_MANAGERS/ExecutionMonitor/execution_history.py)
- ExecutionLoop (file: A_01_CORE/execution_loop.py)
- ExecutionMemoryV2 (file: A_07_MEMORY/agent_runtime_v2.py)
- ExecutionMonitor (file: A_02_MANAGERS/ExecutionMonitor/execution_monitor.py)
- ExecutionPolicy (file: A_07_CONFIG/execution_policy_schema.py)
- ExecutionRegistry (file: A_07_MEMORY/execution_registry.py)
- ExecutionRegistryDiscoveryAgent (file: A_04_AGENTS/ProjectDocumentationDepartment/Core/Discovery/execution_registry_discovery_agent.py)
- ExecutionResult (file: A_02_MANAGERS/TaskRunner/execution_result.py)
- ExecutionScanner (file: A_04_AGENTS/ProjectDocumentationDepartment/Core/Scanners/execution_scanner.py)
- ExecutionState (file: A_02_MANAGERS/ExecutionMonitor/execution_state.py)
- Executor (file: A_03_EXECUTORS/executor.py)
- ExecutorFactory (file: A_02_MANAGERS/TaskRunner/executor_factory.py)
- HarnessScanner (file: A_04_AGENTS/ProjectDocumentationDepartment/Core/Scanners/harness_scanner.py)
- IntegrationTestGuard (file: A_03_ORCHESTRATION/guards/integration_test_guard.py)
- PDFOCRPipeline (file: A_03_HANDLERS/pdf_ocr_pipeline.py)
- PNGWorkflowMemory (file: A_07_MEMORY/png_workflow_memory.py)
- PlannerPipeline (file: A_02_MANAGERS/ArchitectAgent/planner_pipeline.py)
- PowerShellExecutionAdapter (file: A_02_MANAGERS/TaskRunner/ExecutionAdapters/powershell_adapter.py)
- PythonExecutionAdapter (file: A_02_MANAGERS/TaskRunner/ExecutionAdapters/python_adapter.py)
- QueueManager (file: A_02_MANAGERS/ArchitectAgent/queue_manager.py)
- QueueManager (file: A_02_MANAGERS/queue_manager.py)
- Recipe (file: A_07_CONFIG/recipe_schema.py)
- RecipeBuilder (file: A_02_MANAGERS/ArchitectAgent/recipe_builder.py)
- RecipeBuilder (file: A_02_MANAGERS/TaskRunner/recipe_builder.py)
- RecipeExecutor (file: A_02_MANAGERS/TaskRunner/recipe_executor.py)
- RecipeGenerator (file: A_02_MANAGERS/ArchitectAgent/recipe_generator.py)
- RecipeGenerator (file: A_02_MANAGERS/recipe_generator.py)
- RecipeLoader (file: A_02_MANAGERS/TaskRunner/recipe_loader.py)
- RecipeQueueWatcher (file: A_02_MANAGERS/TaskRunner/recipe_queue_watcher.py)
- RecipeStep (file: A_07_CONFIG/recipe_schema.py)
- RecipeValidator (file: A_02_MANAGERS/recipe_validator.py)
- RecipeWriter (file: A_02_MANAGERS/TaskRunner/recipe_writer.py)
- SessionQueue (file: A_03_ORCHESTRATION/session_queue.py)
- TaskContractBuilder (file: A_02_MANAGERS/ArchitectAgent/task_contract_builder.py)
- TaskFeeder (file: A_01_CORE/task_feeder.py)
- TaskPlanner (file: A_02_MANAGERS/Planner/task_planner.py)
- TaskRunner (file: A_02_MANAGERS/TaskRunner/runner.py)
- TestMemoryAdvisor (file: A_09_TESTS/test_memory_advisor.py)
- TestProjectAuditor (file: A_09_TESTS/test_project_auditor.py)

### FUNCTIONS:
- latest_rollback (file: restore_full_project.py)
- latest_rollback_has_factory (file: safe_change.py)
- register_test_job (file: INIT_OMEGA.py)
- run_guarded_task (file: Butler_Gate.py)
- run_pipeline (file: RUN_PIPELINE.py)
- run_pipeline (file: RUN_PIPELINE_V12.py)
- run_self_test (file: A_03_ORCHESTRATION/chat_router.CLEAN_UTF8.py)
- run_self_test (file: A_03_ORCHESTRATION/chat_router.HYBRID_WORK.after_import.py)
- run_self_test (file: A_03_ORCHESTRATION/chat_router.HYBRID_WORK.after_resolver.py)
- run_self_test (file: A_03_ORCHESTRATION/chat_router.HYBRID_WORK.hybrid_ok.py)
- run_self_test (file: A_03_ORCHESTRATION/chat_router.HYBRID_WORK.py)
- run_self_test (file: A_03_ORCHESTRATION/chat_router.py)
- run_self_test (file: A_03_ORCHESTRATION/chat_router.STABLE_BEFORE_HYBRID.py)
- run_self_test (file: A_03_ORCHESTRATION/chat_router.STABLE_TEST.py)
- run_self_test (file: A_03_ORCHESTRATION/chat_router.WORKING_RUSSIAN_OK.py)
- run_self_test (file: A_03_ORCHESTRATION/chat_router_test_restore.py)
- run_tests (file: A_09_TESTS/test_pdf_ocr_pipeline.py)
- run_tests (file: A_09_TESTS/test_search_engine.py)
- run_tests (file: A_09_TESTS/test_vision_analyzer.py)
- sample_executor (file: A_03_ORCHESTRATION/butler_harness.py)
- test_catalog_update (file: A_01_CORE/test_db.py)

### CALLS:
- ButlerHarness (file: 1117)
- ButlerHarness (file: 1285)
- ButlerHarness (file: 1287)
- ButlerHarness (file: 1344)
- ButlerHarness (file: 324)
- ButlerHarness (file: 338)
- ButlerHarness (file: A_03_ORCHESTRATION/butler_harness.py)
- ButlerHarness (file: 477)
- ButlerHarness (file: A_04_AGENTS/ProjectDocumentationDepartment/Core/Scanners/harness_scanner.py)
- ButlerHarness (file: 600)
- EngineeringPipeline (file: 611)
- ExecutionContext (file: A_07_CONFIG/execution_context_schema.py)
- ExecutionLoop (file: 1495)
- ExecutionLoop (file: 1505)
- ExecutionLoop (file: A_01_CORE/execution_loop.py)
- ExecutionMemoryV2 (file: A_07_MEMORY/agent_runtime_v2.py)
- ExecutionMonitor (file: A_02_MANAGERS/ExecutionMonitor/execution_monitor.py)
- ExecutionPolicy (file: A_07_CONFIG/execution_policy_schema.py)
- ExecutionPolicy (file: 296)
- ExecutionRegistry (file: 1117)
- ... and 85 more

### DEPENDENCY_NODES:
- A_02_MANAGERS.ExecutionMonitor.execution_history (file: None)
- A_02_MANAGERS.ExecutionMonitor.execution_state (file: None)
- A_02_MANAGERS.ExecutionMonitor.system_state (file: None)
- A_02_MANAGERS.ExecutionPolicyEngine.policy_loader (file: None)
- A_02_MANAGERS.TaskRunner.ExecutionAdapters.base_adapter (file: None)
- A_02_MANAGERS.TaskRunner.ExecutionAdapters.powershell_adapter (file: None)
- A_02_MANAGERS.TaskRunner.ExecutionAdapters.python_adapter (file: None)
- A_02_MANAGERS.TaskRunner.automatic_verifier (file: None)
- A_02_MANAGERS.TaskRunner.execution_result (file: None)
- A_02_MANAGERS.TaskRunner.executor_factory (file: None)
- A_02_MANAGERS.TaskRunner.recipe_builder (file: None)
- A_02_MANAGERS.TaskRunner.recipe_executor (file: None)
- A_02_MANAGERS.TaskRunner.recipe_loader (file: None)
- A_02_MANAGERS.TaskRunner.recipe_queue_watcher (file: None)
- A_02_MANAGERS.TaskRunner.recipe_writer (file: None)
- A_02_MANAGERS.TaskRunner.runner_once (file: None)
- A_02_MANAGERS.recipe_generator (file: None)
- A_02_MANAGERS.recipe_validator (file: None)
- A_07_CONFIG.recipe_schema (file: None)
- ButlerHarness (file: None)
- ... and 41 more

### EXECUTION_FACTS:
- PHASE_1_INIT::BOOTSTRAP: DONE
- PHASE_1_MULTITASK_TEST::TEST_TASK_A: DONE
- PHASE_1_MULTITASK_TEST::TEST_TASK_B: DONE
- PHASE_1_MULTITASK_TEST::TEST_TASK_C: DONE
- PHASE_1_TEST_DIAGNOSTICS::AUDIT_VERIFY_HEALTH: DONE
- PHASE_3_CLEANUP_AND_BACKUP::RUN_CORE_BACKUP: DONE
- TEST_PHASE_1::PHASE_1_TASK_A: DONE
- TEST_PHASE_1::PHASE_1_TASK_B: DONE
- TEST_PHASE_2::PHASE_2_TASK_C: DONE
- TEST_PHASE_2::PHASE_2_TASK_D: DONE

### GOALS_FACTS:
- active_goal: BUTLER_RECIPE_LIBRARY
- current_phase: ROADMAP_6_PHASE_4_RECIPES
- subgoal: ROADMAP_6_PHASE_4_RECIPES status=COMPLETED
- task: task_run_full_audit status=COMPLETED
- task: task_verify_contour status=COMPLETED
- weight: autonomy=0.6
- weight: stability=1.0

### IMPORTS:
- A_02_MANAGERS.ExecutionMonitor.execution_history (file: A_02_MANAGERS/ExecutionMonitor/execution_state.py)
- A_02_MANAGERS.ExecutionMonitor.execution_state (file: 295)
- A_02_MANAGERS.ExecutionMonitor.system_state (file: 305)
- A_02_MANAGERS.ExecutionPolicyEngine.policy_loader (file: A_07_CONFIG/execution_context_schema.py)
- A_02_MANAGERS.ExecutionPolicyEngine.policy_loader (file: 297)
- A_02_MANAGERS.ExecutionPolicyEngine.policy_loader (file: 298)
- A_02_MANAGERS.TaskRunner.ExecutionAdapters.base_adapter (file: A_02_MANAGERS/TaskRunner/ExecutionAdapters/powershell_adapter.py)
- A_02_MANAGERS.TaskRunner.ExecutionAdapters.base_adapter (file: A_02_MANAGERS/TaskRunner/ExecutionAdapters/python_adapter.py)
- A_02_MANAGERS.TaskRunner.ExecutionAdapters.powershell_adapter (file: A_02_MANAGERS/TaskRunner/executor_factory.py)
- A_02_MANAGERS.TaskRunner.ExecutionAdapters.python_adapter (file: A_02_MANAGERS/TaskRunner/executor_factory.py)
- A_02_MANAGERS.TaskRunner.automatic_verifier (file: 358)
- A_02_MANAGERS.TaskRunner.execution_result (file: 339)
- A_02_MANAGERS.TaskRunner.execution_result (file: A_02_MANAGERS/TaskRunner/ExecutionAdapters/base_adapter.py)
- A_02_MANAGERS.TaskRunner.execution_result (file: A_02_MANAGERS/TaskRunner/ExecutionAdapters/powershell_adapter.py)
- A_02_MANAGERS.TaskRunner.execution_result (file: A_02_MANAGERS/TaskRunner/ExecutionAdapters/python_adapter.py)
- A_02_MANAGERS.TaskRunner.execution_result (file: A_02_MANAGERS/TaskRunner/recipe_executor.py)
- A_02_MANAGERS.TaskRunner.executor_factory (file: A_02_MANAGERS/TaskRunner/recipe_executor.py)
- A_02_MANAGERS.TaskRunner.recipe_builder (file: A_02_MANAGERS/Planner/task_planner.py)
- A_02_MANAGERS.TaskRunner.recipe_builder (file: A_02_MANAGERS/TaskRunner/recipe_writer.py)
- A_02_MANAGERS.TaskRunner.recipe_executor (file: 358)
- ... and 25 more

### LINKS:
- {"metadata": {"alias": null, "kind": "from", "line": 11, "name": "ExecutionHistory"}, "source": 294, "target": "A_02_MANAGERS.ExecutionMonitor.execution_history", "type": "import"} (file: None)
- {"metadata": {"alias": null, "kind": "from", "line": 11, "name": "ExecutionResult"}, "source": 339, "target": "A_02_MANAGERS.TaskRunner.execution_result", "type": "import"} (file: None)
- {"metadata": {"alias": null, "kind": "from", "line": 11, "name": "PolicyLoader"}, "source": 297, "target": "A_02_MANAGERS.ExecutionPolicyEngine.policy_loader", "type": "import"} (file: None)
- {"metadata": {"alias": null, "kind": "from", "line": 11, "name": "PolicyLoader"}, "source": 298, "target": "A_02_MANAGERS.ExecutionPolicyEngine.policy_loader", "type": "import"} (file: None)
- {"metadata": {"alias": null, "kind": "from", "line": 11, "name": "PythonExecutionAdapter"}, "source": 346, "target": "A_02_MANAGERS.TaskRunner.ExecutionAdapters.python_adapter", "type": "import"} (file: None)
- {"metadata": {"alias": null, "kind": "from", "line": 12, "name": "ExecutionResult"}, "source": 343, "target": "A_02_MANAGERS.TaskRunner.execution_result", "type": "import"} (file: None)
- {"metadata": {"alias": null, "kind": "from", "line": 12, "name": "ExecutionResult"}, "source": 344, "target": "A_02_MANAGERS.TaskRunner.execution_result", "type": "import"} (file: None)
- {"metadata": {"alias": null, "kind": "from", "line": 12, "name": "RecipeWriter"}, "source": 305, "target": "A_02_MANAGERS.TaskRunner.recipe_writer", "type": "import"} (file: None)
- {"metadata": {"alias": null, "kind": "from", "line": 13, "name": "BaseExecutionAdapter"}, "source": 343, "target": "A_02_MANAGERS.TaskRunner.ExecutionAdapters.base_adapter", "type": "import"} (file: None)
- {"metadata": {"alias": null, "kind": "from", "line": 13, "name": "BaseExecutionAdapter"}, "source": 344, "target": "A_02_MANAGERS.TaskRunner.ExecutionAdapters.base_adapter", "type": "import"} (file: None)
- {"metadata": {"alias": null, "kind": "from", "line": 13, "name": "Recipe"}, "source": 348, "target": "A_07_CONFIG.recipe_schema", "type": "import"} (file: None)
- {"metadata": {"alias": null, "kind": "from", "line": 13, "name": "RecipeStep"}, "source": 348, "target": "A_07_CONFIG.recipe_schema", "type": "import"} (file: None)
- {"metadata": {"alias": null, "kind": "from", "line": 13, "name": "run_once"}, "source": 305, "target": "A_02_MANAGERS.TaskRunner.runner_once", "type": "import"} (file: None)
- {"metadata": {"alias": null, "kind": "from", "line": 14, "name": "ExecutionResult"}, "source": 348, "target": "A_02_MANAGERS.TaskRunner.execution_result", "type": "import"} (file: None)
- {"metadata": {"alias": null, "kind": "from", "line": 14, "name": "ExecutionState"}, "source": 295, "target": "A_02_MANAGERS.ExecutionMonitor.execution_state", "type": "import"} (file: None)
- {"metadata": {"alias": null, "kind": "from", "line": 14, "name": "PowerShellExecutionAdapter"}, "source": 346, "target": "A_02_MANAGERS.TaskRunner.ExecutionAdapters.powershell_adapter", "type": "import"} (file: None)
- {"metadata": {"alias": null, "kind": "from", "line": 14, "name": "RecipeBuilder"}, "source": 309, "target": "A_02_MANAGERS.TaskRunner.recipe_builder", "type": "import"} (file: None)
- {"metadata": {"alias": null, "kind": "from", "line": 14, "name": "RecipeQueueWatcher"}, "source": 358, "target": "A_02_MANAGERS.TaskRunner.recipe_queue_watcher", "type": "import"} (file: None)
- {"metadata": {"alias": null, "kind": "from", "line": 15, "name": "ExecutorFactory"}, "source": 348, "target": "A_02_MANAGERS.TaskRunner.executor_factory", "type": "import"} (file: None)
- {"metadata": {"alias": null, "kind": "from", "line": 15, "name": "Recipe"}, "source": 347, "target": "A_07_CONFIG.recipe_schema", "type": "import"} (file: None)
- ... and 141 more

---

## CAPABILITY: CONFIG
**TOTAL EVIDENCE:** 85
**STATUS:** READY
**MAIN ENTRY:** RouterRegistry

### FILES (canonical):
- A_07_CONFIG/registry_loader.py
- A_07_CONFIG/registry_validator.py
- A_07_MEMORY/execution_registry.py
- FIX_QUEUE.py
- INIT_OMEGA.py
- A_02_MANAGERS/ExecutionPolicyEngine/policy_registry.py
- A_02_MANAGERS/RuntimeCapabilityRegistry/runtime_registry.py
- A_03_HANDLERS/registry.py
- A_03_ORCHESTRATION/registry_brain.py
- A_03_ORCHESTRATION/router_registry.py
- A_04_AGENTS/ProjectDocumentationDepartment/Core/Discovery/execution_registry_discovery_agent.py
- A_04_AGENTS/ProjectDocumentationDepartment/Core/Discovery/goals_registry_discovery_agent.py
- A_04_AGENTS/ProjectDocumentationDepartment/Core/Discovery/registry_discovery_agent.py
- A_04_AGENTS/ProjectDocumentationDepartment/Core/Discovery/registry_reader_agent.py
- A_04_AGENTS/ProjectDocumentationDepartment/Core/Scanners/registry_scanner.py

### CLASSES:
- ExecutionRegistry (file: A_07_MEMORY/execution_registry.py)
- ExecutionRegistryDiscoveryAgent (file: A_04_AGENTS/ProjectDocumentationDepartment/Core/Discovery/execution_registry_discovery_agent.py)
- GoalsRegistryDiscoveryAgent (file: A_04_AGENTS/ProjectDocumentationDepartment/Core/Discovery/goals_registry_discovery_agent.py)
- HandlerRegistry (file: A_03_HANDLERS/registry.py)
- PolicyRegistry (file: A_02_MANAGERS/ExecutionPolicyEngine/policy_registry.py)
- RegistryBrain (file: A_03_ORCHESTRATION/registry_brain.py)
- RegistryDiscoveryAgent (file: A_04_AGENTS/ProjectDocumentationDepartment/Core/Discovery/registry_discovery_agent.py)
- RegistryLoader (file: A_07_CONFIG/registry_loader.py)
- RegistryReaderAgent (file: A_04_AGENTS/ProjectDocumentationDepartment/Core/Discovery/registry_reader_agent.py)
- RegistryScanner (file: A_04_AGENTS/ProjectDocumentationDepartment/Core/Scanners/registry_scanner.py)
- RegistryValidator (file: A_07_CONFIG/registry_validator.py)
- RouterRegistry (file: A_03_ORCHESTRATION/router_registry.py)
- RuntimeCapabilityRegistry (file: A_02_MANAGERS/RuntimeCapabilityRegistry/runtime_registry.py)

### FUNCTIONS:
- register_test_job (file: INIT_OMEGA.py)
- reset_and_register (file: FIX_QUEUE.py)

### CALLS:
- ExecutionRegistry (file: 1117)
- HandlerRegistry (file: A_03_HANDLERS/registry.py)
- RegistryBrain (file: 1495)
- RegistryBrain (file: 1505)
- RegistryBrain (file: A_03_ORCHESTRATION/registry_brain.py)
- RegistryLoader (file: 1102)
- RegistryLoader (file: 1103)
- RegistryLoader (file: A_07_CONFIG/registry_loader.py)
- RegistryScanner (file: 536)
- RegistryScanner (file: 591)
- RegistryValidator (file: A_07_CONFIG/registry_validator.py)
- RouterRegistry (file: 123)
- RouterRegistry (file: 467)
- RouterRegistry (file: 468)
- RouterRegistry (file: 469)
- RouterRegistry (file: A_03_ORCHESTRATION/router_registry.py)
- RouterRegistry (file: 477)
- register_test_job (file: INIT_OMEGA.py)
- reset_and_register (file: FIX_QUEUE.py)

### DEPENDENCY_NODES:
- A_02_MANAGERS.RuntimeCapabilityRegistry.capability_schema (file: None)
- A_02_MANAGERS.RuntimeCapabilityRegistry.runtime_registry (file: None)
- ExecutionRegistry (file: None)
- HandlerRegistry (file: None)
- RegistryBrain (file: None)
- RegistryLoader (file: None)
- RegistryScanner (file: None)
- RegistryValidator (file: None)
- RouterRegistry (file: None)
- register_test_job (file: None)
- reset_and_register (file: None)

### EXECUTION_FACTS:
- PHASE_1_INIT::BOOTSTRAP: DONE
- PHASE_1_MULTITASK_TEST::TEST_TASK_A: DONE
- PHASE_1_MULTITASK_TEST::TEST_TASK_B: DONE
- PHASE_1_MULTITASK_TEST::TEST_TASK_C: DONE
- PHASE_1_TEST_DIAGNOSTICS::AUDIT_VERIFY_HEALTH: DONE
- PHASE_3_CLEANUP_AND_BACKUP::RUN_CORE_BACKUP: DONE
- TEST_PHASE_1::PHASE_1_TASK_A: DONE
- TEST_PHASE_1::PHASE_1_TASK_B: DONE
- TEST_PHASE_2::PHASE_2_TASK_C: DONE
- TEST_PHASE_2::PHASE_2_TASK_D: DONE

### GOALS_FACTS:
- active_goal: BUTLER_RECIPE_LIBRARY
- current_phase: ROADMAP_6_PHASE_4_RECIPES
- subgoal: ROADMAP_6_PHASE_4_RECIPES status=COMPLETED
- task: task_run_full_audit status=COMPLETED
- task: task_verify_contour status=COMPLETED
- weight: autonomy=0.6
- weight: stability=1.0

### IMPORTS:
- A_02_MANAGERS.RuntimeCapabilityRegistry.capability_schema (file: A_02_MANAGERS/RuntimeCapabilityRegistry/runtime_registry.py)
- A_02_MANAGERS.RuntimeCapabilityRegistry.runtime_registry (file: 1081)

### LINKS:
- {"metadata": {"alias": null, "kind": "from", "line": 15, "name": "RuntimeCapabilityRegistry"}, "source": 1081, "target": "A_02_MANAGERS.RuntimeCapabilityRegistry.runtime_registry", "type": "import"} (file: None)
- {"metadata": {"alias": null, "kind": "from", "line": 9, "name": "RuntimeCapability"}, "source": 320, "target": "A_02_MANAGERS.RuntimeCapabilityRegistry.capability_schema", "type": "import"} (file: None)
- {"metadata": {"context": "BootstrapCore.__init__", "line": 16}, "source": 1495, "target": "RegistryBrain", "type": "call"} (file: None)
- {"metadata": {"context": "ButlerSystem.__init__", "line": 15}, "source": 1505, "target": "RegistryBrain", "type": "call"} (file: None)
- {"metadata": {"context": "EngineeringPipeline.collect", "line": 56}, "source": 536, "target": "RegistryScanner", "type": "call"} (file: None)
- {"metadata": {"context": "EngineeringPipeline.collect", "line": 56}, "source": 591, "target": "RegistryScanner", "type": "call"} (file: None)
- {"metadata": {"context": "LoopOrchestratorV3_MASTER_TRUTH.__init__", "line": 48}, "source": 1117, "target": "ExecutionRegistry", "type": "call"} (file: None)
- {"metadata": {"context": "ProjectState.__init__", "line": 11}, "source": 1102, "target": "RegistryLoader", "type": "call"} (file: None)
- {"metadata": {"context": "ProjectState.__init__", "line": 11}, "source": 1103, "target": "RegistryLoader", "type": "call"} (file: None)
- {"metadata": {"context": "RouterIntegration.__init__", "line": 22}, "source": 123, "target": "RouterRegistry", "type": "call"} (file: None)
- {"metadata": {"context": "RouterIntegration.__init__", "line": 22}, "source": 467, "target": "RouterRegistry", "type": "call"} (file: None)
- {"metadata": {"context": "RouterIntegration.__init__", "line": 25}, "source": 468, "target": "RouterRegistry", "type": "call"} (file: None)
- {"metadata": {"context": "Worker.__init__", "line": 35}, "source": 477, "target": "RouterRegistry", "type": "call"} (file: None)
- {"metadata": {"context": null, "line": 23}, "source": 469, "target": "RouterRegistry", "type": "call"} (file: None)
- {"metadata": {"context": null, "line": 23}, "source": 470, "target": "RouterRegistry", "type": "call"} (file: None)
- {"metadata": {"context": null, "line": 26}, "source": 1454, "target": "register_test_job", "type": "call"} (file: None)
- {"metadata": {"context": null, "line": 34}, "source": 1106, "target": "RegistryLoader", "type": "call"} (file: None)
- {"metadata": {"context": null, "line": 37}, "source": 387, "target": "HandlerRegistry", "type": "call"} (file: None)
- {"metadata": {"context": null, "line": 38}, "source": 1441, "target": "reset_and_register", "type": "call"} (file: None)
- {"metadata": {"context": null, "line": 47}, "source": 1107, "target": "RegistryValidator", "type": "call"} (file: None)
- ... and 1 more

---

## CAPABILITY: DOCUMENTATION
**TOTAL EVIDENCE:** 36
**STATUS:** READY
**MAIN ENTRY:** ProjectDocumentationDepartment

### FILES (canonical):
- A_04_AGENTS/ProjectDocumentationDepartment/runner.py

### CLASSES:
- ProjectDocumentationDepartment (file: A_04_AGENTS/ProjectDocumentationDepartment/runner.py)

### FUNCTIONS:

### CALLS:
- ProjectDocumentationDepartment (file: 1516)
- ProjectDocumentationDepartment (file: 324)
- ProjectDocumentationDepartment (file: A_04_AGENTS/ProjectDocumentationDepartment/runner.py)

### DEPENDENCY_NODES:
- A_04_AGENTS.ProjectDocumentationDepartment.Core.engineering_pipeline (file: None)
- A_04_AGENTS.ProjectDocumentationDepartment.Core.evidence_doctor (file: None)
- A_04_AGENTS.ProjectDocumentationDepartment.runner (file: None)
- ProjectDocumentationDepartment (file: None)

### EXECUTION_FACTS:
- PHASE_1_INIT::BOOTSTRAP: DONE
- PHASE_1_MULTITASK_TEST::TEST_TASK_A: DONE
- PHASE_1_MULTITASK_TEST::TEST_TASK_B: DONE
- PHASE_1_MULTITASK_TEST::TEST_TASK_C: DONE
- PHASE_1_TEST_DIAGNOSTICS::AUDIT_VERIFY_HEALTH: DONE
- PHASE_3_CLEANUP_AND_BACKUP::RUN_CORE_BACKUP: DONE
- TEST_PHASE_1::PHASE_1_TASK_A: DONE
- TEST_PHASE_1::PHASE_1_TASK_B: DONE
- TEST_PHASE_2::PHASE_2_TASK_C: DONE
- TEST_PHASE_2::PHASE_2_TASK_D: DONE

### GOALS_FACTS:
- active_goal: BUTLER_RECIPE_LIBRARY
- current_phase: ROADMAP_6_PHASE_4_RECIPES
- subgoal: ROADMAP_6_PHASE_4_RECIPES status=COMPLETED
- task: task_run_full_audit status=COMPLETED
- task: task_verify_contour status=COMPLETED
- weight: autonomy=0.6
- weight: stability=1.0

### IMPORTS:
- A_04_AGENTS.ProjectDocumentationDepartment.Core.engineering_pipeline (file: A_04_AGENTS/ProjectDocumentationDepartment/runner.py)
- A_04_AGENTS.ProjectDocumentationDepartment.Core.evidence_doctor (file: A_04_AGENTS/ProjectDocumentationDepartment/runner.py)
- A_04_AGENTS.ProjectDocumentationDepartment.runner (file: 1516)
- A_04_AGENTS.ProjectDocumentationDepartment.runner (file: 324)

### LINKS:
- {"metadata": {"alias": "evidence_doctor", "kind": "from", "line": 5, "name": "dispatch"}, "source": 611, "target": "A_04_AGENTS.ProjectDocumentationDepartment.Core.evidence_doctor", "type": "import"} (file: None)
- {"metadata": {"alias": null, "kind": "from", "line": 14, "name": "ProjectDocumentationDepartment"}, "source": 324, "target": "A_04_AGENTS.ProjectDocumentationDepartment.runner", "type": "import"} (file: None)
- {"metadata": {"alias": null, "kind": "from", "line": 3, "name": "ProjectDocumentationDepartment"}, "source": 1516, "target": "A_04_AGENTS.ProjectDocumentationDepartment.runner", "type": "import"} (file: None)
- {"metadata": {"alias": null, "kind": "from", "line": 4, "name": "EngineeringPipeline"}, "source": 611, "target": "A_04_AGENTS.ProjectDocumentationDepartment.Core.engineering_pipeline", "type": "import"} (file: None)
- {"metadata": {"context": "SmartDispatcherV2.__init__", "line": 31}, "source": 324, "target": "ProjectDocumentationDepartment", "type": "call"} (file: None)
- {"metadata": {"context": null, "line": 5}, "source": 1516, "target": "ProjectDocumentationDepartment", "type": "call"} (file: None)
- {"metadata": {"context": null, "line": 96}, "source": 611, "target": "ProjectDocumentationDepartment", "type": "call"} (file: None)

---

## CAPABILITY: AUDIO
**TOTAL EVIDENCE:** 40
**STATUS:** READY
**MAIN ENTRY:** AudioDepartment

### FILES (canonical):
- A_04_AGENTS/AudioDepartment/runner.py

### CLASSES:
- AudioDepartment (file: A_04_AGENTS/AudioDepartment/runner.py)

### FUNCTIONS:

### CALLS:
- AudioDepartment (file: 1285)
- AudioDepartment (file: 1287)
- AudioDepartment (file: 1340)
- AudioDepartment (file: 324)
- AudioDepartment (file: 338)

### DEPENDENCY_NODES:
- A_04_AGENTS.AudioDepartment.runner (file: None)
- AudioDepartment (file: None)

### EXECUTION_FACTS:
- PHASE_1_INIT::BOOTSTRAP: DONE
- PHASE_1_MULTITASK_TEST::TEST_TASK_A: DONE
- PHASE_1_MULTITASK_TEST::TEST_TASK_B: DONE
- PHASE_1_MULTITASK_TEST::TEST_TASK_C: DONE
- PHASE_1_TEST_DIAGNOSTICS::AUDIT_VERIFY_HEALTH: DONE
- PHASE_3_CLEANUP_AND_BACKUP::RUN_CORE_BACKUP: DONE
- TEST_PHASE_1::PHASE_1_TASK_A: DONE
- TEST_PHASE_1::PHASE_1_TASK_B: DONE
- TEST_PHASE_2::PHASE_2_TASK_C: DONE
- TEST_PHASE_2::PHASE_2_TASK_D: DONE

### GOALS_FACTS:
- active_goal: BUTLER_RECIPE_LIBRARY
- current_phase: ROADMAP_6_PHASE_4_RECIPES
- subgoal: ROADMAP_6_PHASE_4_RECIPES status=COMPLETED
- task: task_run_full_audit status=COMPLETED
- task: task_verify_contour status=COMPLETED
- weight: autonomy=0.6
- weight: stability=1.0

### IMPORTS:
- A_04_AGENTS.AudioDepartment.runner (file: 1285)
- A_04_AGENTS.AudioDepartment.runner (file: 1287)
- A_04_AGENTS.AudioDepartment.runner (file: 1340)
- A_04_AGENTS.AudioDepartment.runner (file: 324)
- A_04_AGENTS.AudioDepartment.runner (file: 338)

### LINKS:
- {"metadata": {"alias": null, "kind": "from", "line": 5, "name": "AudioDepartment"}, "source": 1340, "target": "A_04_AGENTS.AudioDepartment.runner", "type": "import"} (file: None)
- {"metadata": {"alias": null, "kind": "from", "line": 7, "name": "AudioDepartment"}, "source": 1285, "target": "A_04_AGENTS.AudioDepartment.runner", "type": "import"} (file: None)
- {"metadata": {"alias": null, "kind": "from", "line": 7, "name": "AudioDepartment"}, "source": 1287, "target": "A_04_AGENTS.AudioDepartment.runner", "type": "import"} (file: None)
- {"metadata": {"alias": null, "kind": "from", "line": 7, "name": "AudioDepartment"}, "source": 324, "target": "A_04_AGENTS.AudioDepartment.runner", "type": "import"} (file: None)
- {"metadata": {"alias": null, "kind": "from", "line": 7, "name": "AudioDepartment"}, "source": 338, "target": "A_04_AGENTS.AudioDepartment.runner", "type": "import"} (file: None)
- {"metadata": {"context": "SmartDispatcherV2.__init__", "line": 26}, "source": 338, "target": "AudioDepartment", "type": "call"} (file: None)
- {"metadata": {"context": "SmartDispatcherV2.__init__", "line": 32}, "source": 1285, "target": "AudioDepartment", "type": "call"} (file: None)
- {"metadata": {"context": "SmartDispatcherV2.__init__", "line": 32}, "source": 1287, "target": "AudioDepartment", "type": "call"} (file: None)
- {"metadata": {"context": "SmartDispatcherV2.__init__", "line": 36}, "source": 324, "target": "AudioDepartment", "type": "call"} (file: None)
- {"metadata": {"context": null, "line": 15}, "source": 1340, "target": "AudioDepartment", "type": "call"} (file: None)

---

## CAPABILITY: VIDEO
**TOTAL EVIDENCE:** 40
**STATUS:** READY
**MAIN ENTRY:** VideoDepartment

### FILES (canonical):
- A_04_AGENTS/VideoDepartment/runner.py

### CLASSES:
- VideoDepartment (file: A_04_AGENTS/VideoDepartment/runner.py)

### FUNCTIONS:

### CALLS:
- VideoDepartment (file: 1285)
- VideoDepartment (file: 1287)
- VideoDepartment (file: 1340)
- VideoDepartment (file: 324)
- VideoDepartment (file: 338)

### DEPENDENCY_NODES:
- A_04_AGENTS.VideoDepartment.runner (file: None)
- VideoDepartment (file: None)

### EXECUTION_FACTS:
- PHASE_1_INIT::BOOTSTRAP: DONE
- PHASE_1_MULTITASK_TEST::TEST_TASK_A: DONE
- PHASE_1_MULTITASK_TEST::TEST_TASK_B: DONE
- PHASE_1_MULTITASK_TEST::TEST_TASK_C: DONE
- PHASE_1_TEST_DIAGNOSTICS::AUDIT_VERIFY_HEALTH: DONE
- PHASE_3_CLEANUP_AND_BACKUP::RUN_CORE_BACKUP: DONE
- TEST_PHASE_1::PHASE_1_TASK_A: DONE
- TEST_PHASE_1::PHASE_1_TASK_B: DONE
- TEST_PHASE_2::PHASE_2_TASK_C: DONE
- TEST_PHASE_2::PHASE_2_TASK_D: DONE

### GOALS_FACTS:
- active_goal: BUTLER_RECIPE_LIBRARY
- current_phase: ROADMAP_6_PHASE_4_RECIPES
- subgoal: ROADMAP_6_PHASE_4_RECIPES status=COMPLETED
- task: task_run_full_audit status=COMPLETED
- task: task_verify_contour status=COMPLETED
- weight: autonomy=0.6
- weight: stability=1.0

### IMPORTS:
- A_04_AGENTS.VideoDepartment.runner (file: 1285)
- A_04_AGENTS.VideoDepartment.runner (file: 1287)
- A_04_AGENTS.VideoDepartment.runner (file: 1340)
- A_04_AGENTS.VideoDepartment.runner (file: 324)
- A_04_AGENTS.VideoDepartment.runner (file: 338)

### LINKS:
- {"metadata": {"alias": null, "kind": "from", "line": 7, "name": "VideoDepartment"}, "source": 1340, "target": "A_04_AGENTS.VideoDepartment.runner", "type": "import"} (file: None)
- {"metadata": {"alias": null, "kind": "from", "line": 9, "name": "VideoDepartment"}, "source": 1285, "target": "A_04_AGENTS.VideoDepartment.runner", "type": "import"} (file: None)
- {"metadata": {"alias": null, "kind": "from", "line": 9, "name": "VideoDepartment"}, "source": 1287, "target": "A_04_AGENTS.VideoDepartment.runner", "type": "import"} (file: None)
- {"metadata": {"alias": null, "kind": "from", "line": 9, "name": "VideoDepartment"}, "source": 324, "target": "A_04_AGENTS.VideoDepartment.runner", "type": "import"} (file: None)
- {"metadata": {"alias": null, "kind": "from", "line": 9, "name": "VideoDepartment"}, "source": 338, "target": "A_04_AGENTS.VideoDepartment.runner", "type": "import"} (file: None)
- {"metadata": {"context": "SmartDispatcherV2.__init__", "line": 28}, "source": 338, "target": "VideoDepartment", "type": "call"} (file: None)
- {"metadata": {"context": "SmartDispatcherV2.__init__", "line": 34}, "source": 1285, "target": "VideoDepartment", "type": "call"} (file: None)
- {"metadata": {"context": "SmartDispatcherV2.__init__", "line": 34}, "source": 1287, "target": "VideoDepartment", "type": "call"} (file: None)
- {"metadata": {"context": "SmartDispatcherV2.__init__", "line": 38}, "source": 324, "target": "VideoDepartment", "type": "call"} (file: None)
- {"metadata": {"context": null, "line": 17}, "source": 1340, "target": "VideoDepartment", "type": "call"} (file: None)

---

## CAPABILITY: ARCHIVE
**TOTAL EVIDENCE:** 64
**STATUS:** READY
**MAIN ENTRY:** ArchiveDepartment

### FILES (canonical):
- A_01_CORE/safety_gate.py
- A_02_MANAGERS/archiver.py
- A_03_HANDLERS/archive_handler.py
- A_04_AGENTS/ArchiveDepartment/runner.py

### CLASSES:
- ArchiveDepartment (file: A_04_AGENTS/ArchiveDepartment/runner.py)
- ArchiveHandler (file: A_03_HANDLERS/archive_handler.py)
- Archiver (file: A_02_MANAGERS/archiver.py)

### FUNCTIONS:
- backup_file (file: A_01_CORE/safety_gate.py)
- restore_backup (file: A_01_CORE/safety_gate.py)

### CALLS:
- ArchiveDepartment (file: 1285)
- ArchiveDepartment (file: 1287)
- ArchiveDepartment (file: 1340)
- ArchiveDepartment (file: 324)
- ArchiveDepartment (file: 338)
- ArchiveHandler (file: 387)
- ArchiveHandler (file: A_04_AGENTS/ArchiveDepartment/runner.py)
- Archiver (file: A_02_MANAGERS/archiver.py)
- Archiver (file: 362)
- backup_file (file: A_01_CORE/safety_gate.py)
- backup_file (file: 352)
- restore_backup (file: A_01_CORE/safety_gate.py)

### DEPENDENCY_NODES:
- A_04_AGENTS.ArchiveDepartment.runner (file: None)
- ArchiveDepartment (file: None)
- ArchiveHandler (file: None)
- Archiver (file: None)
- backup_file (file: None)
- restore_backup (file: None)

### EXECUTION_FACTS:
- PHASE_1_INIT::BOOTSTRAP: DONE
- PHASE_1_MULTITASK_TEST::TEST_TASK_A: DONE
- PHASE_1_MULTITASK_TEST::TEST_TASK_B: DONE
- PHASE_1_MULTITASK_TEST::TEST_TASK_C: DONE
- PHASE_1_TEST_DIAGNOSTICS::AUDIT_VERIFY_HEALTH: DONE
- PHASE_3_CLEANUP_AND_BACKUP::RUN_CORE_BACKUP: DONE
- TEST_PHASE_1::PHASE_1_TASK_A: DONE
- TEST_PHASE_1::PHASE_1_TASK_B: DONE
- TEST_PHASE_2::PHASE_2_TASK_C: DONE
- TEST_PHASE_2::PHASE_2_TASK_D: DONE

### GOALS_FACTS:
- active_goal: BUTLER_RECIPE_LIBRARY
- current_phase: ROADMAP_6_PHASE_4_RECIPES
- subgoal: ROADMAP_6_PHASE_4_RECIPES status=COMPLETED
- task: task_run_full_audit status=COMPLETED
- task: task_verify_contour status=COMPLETED
- weight: autonomy=0.6
- weight: stability=1.0

### IMPORTS:
- A_04_AGENTS.ArchiveDepartment.runner (file: 1285)
- A_04_AGENTS.ArchiveDepartment.runner (file: 1287)
- A_04_AGENTS.ArchiveDepartment.runner (file: 1340)
- A_04_AGENTS.ArchiveDepartment.runner (file: 324)
- A_04_AGENTS.ArchiveDepartment.runner (file: 338)

### LINKS:
- {"metadata": {"alias": null, "kind": "from", "line": 10, "name": "ArchiveDepartment"}, "source": 1285, "target": "A_04_AGENTS.ArchiveDepartment.runner", "type": "import"} (file: None)
- {"metadata": {"alias": null, "kind": "from", "line": 10, "name": "ArchiveDepartment"}, "source": 1287, "target": "A_04_AGENTS.ArchiveDepartment.runner", "type": "import"} (file: None)
- {"metadata": {"alias": null, "kind": "from", "line": 10, "name": "ArchiveDepartment"}, "source": 324, "target": "A_04_AGENTS.ArchiveDepartment.runner", "type": "import"} (file: None)
- {"metadata": {"alias": null, "kind": "from", "line": 10, "name": "ArchiveDepartment"}, "source": 338, "target": "A_04_AGENTS.ArchiveDepartment.runner", "type": "import"} (file: None)
- {"metadata": {"alias": null, "kind": "from", "line": 8, "name": "ArchiveDepartment"}, "source": 1340, "target": "A_04_AGENTS.ArchiveDepartment.runner", "type": "import"} (file: None)
- {"metadata": {"context": "ArchiveDepartment.execute", "line": 63}, "source": 483, "target": "ArchiveHandler", "type": "call"} (file: None)
- {"metadata": {"context": "HandlerRegistry.__init__", "line": 23}, "source": 387, "target": "ArchiveHandler", "type": "call"} (file: None)
- {"metadata": {"context": "SmartDispatcherV2.__init__", "line": 29}, "source": 338, "target": "ArchiveDepartment", "type": "call"} (file: None)
- {"metadata": {"context": "SmartDispatcherV2.__init__", "line": 35}, "source": 1285, "target": "ArchiveDepartment", "type": "call"} (file: None)
- {"metadata": {"context": "SmartDispatcherV2.__init__", "line": 35}, "source": 1287, "target": "ArchiveDepartment", "type": "call"} (file: None)
- {"metadata": {"context": "SmartDispatcherV2.__init__", "line": 39}, "source": 324, "target": "ArchiveDepartment", "type": "call"} (file: None)
- {"metadata": {"context": "TaskRunner.patch_file", "line": 63}, "source": 352, "target": "backup_file", "type": "call"} (file: None)
- {"metadata": {"context": "guarded_write", "line": 104}, "source": 225, "target": "restore_backup", "type": "call"} (file: None)
- {"metadata": {"context": "guarded_write", "line": 94}, "source": 225, "target": "backup_file", "type": "call"} (file: None)
- {"metadata": {"context": null, "line": 131}, "source": 225, "target": "backup_file", "type": "call"} (file: None)
- {"metadata": {"context": null, "line": 133}, "source": 225, "target": "restore_backup", "type": "call"} (file: None)
- {"metadata": {"context": null, "line": 18}, "source": 1340, "target": "ArchiveDepartment", "type": "call"} (file: None)
- {"metadata": {"context": null, "line": 19}, "source": 282, "target": "Archiver", "type": "call"} (file: None)
- {"metadata": {"context": null, "line": 19}, "source": 362, "target": "Archiver", "type": "call"} (file: None)

---

## CAPABILITY: MODEL
**TOTAL EVIDENCE:** 366
**STATUS:** READY
**MAIN ENTRY:** main

### FILES (canonical):
- A_07_CONFIG/execution_policy_schema.py
- A_07_MEMORY/semantic_constraint_layer.py
- A_00_HEALER_UNIT/temp_test.py
- A_09_INTERFACE/test_ollama_connect.py
- A_09_TESTS/test_vision.py
- A_99_TEST_DATA/BUTLER_OS_before_image_render.py
- A_99_TEST_DATA/model_olympics_v2.py
- butler_capability_audit.py
- BUTLER_OS.py
- RUN_PIPELINE_V12.py
- safe_change.py
- system_doctor.py
- verify_project.py
- A_01_CORE/alarm.py
- A_01_CORE/fix_butler.py
- A_01_CORE/memory_guardian.py
- A_01_CORE/orchestrator.py
- A_01_CORE/project_indexer.py
- A_03_ENGINES/Vision_Engine/vision_tool.py
- A_03_HANDLERS/ollama_vision_backend.py
- A_03_ORCHESTRATION/chat_router.CLEAN_UTF8.py
- A_03_ORCHESTRATION/chat_router.HYBRID_WORK.after_import.py
- A_03_ORCHESTRATION/chat_router.HYBRID_WORK.after_resolver.py
- A_03_ORCHESTRATION/chat_router.HYBRID_WORK.hybrid_ok.py
- A_03_ORCHESTRATION/chat_router.HYBRID_WORK.py
- A_03_ORCHESTRATION/chat_router.py
- A_03_ORCHESTRATION/chat_router.STABLE_BEFORE_HYBRID.py
- A_03_ORCHESTRATION/chat_router.STABLE_TEST.py
- A_03_ORCHESTRATION/chat_router.WORKING_RUSSIAN_OK.py
- A_03_ORCHESTRATION/chat_router_test_restore.py
- A_03_ORCHESTRATION/Console/butler_console.py
- A_03_ORCHESTRATION/registry_brain.py
- A_04_AGENTS/find_bills.py
- A_04_AGENTS/ProjectDocumentationDepartment/Core/ast_parser.py
- A_04_AGENTS/ProjectDocumentationDepartment/Core/evidence_doctor.py

### CLASSES:
- Constraints (file: A_07_CONFIG/execution_policy_schema.py)
- MainOrchestrator (file: A_01_CORE/orchestrator.py)
- OllamaVisionBackend (file: A_03_HANDLERS/ollama_vision_backend.py)
- RegistryBrain (file: A_03_ORCHESTRATION/registry_brain.py)
- SemanticConstraintLayer (file: A_07_MEMORY/semantic_constraint_layer.py)

### FUNCTIONS:
- ask_ollama (file: A_03_ORCHESTRATION/chat_router.CLEAN_UTF8.py)
- ask_ollama (file: A_03_ORCHESTRATION/chat_router.HYBRID_WORK.after_import.py)
- ask_ollama (file: A_03_ORCHESTRATION/chat_router.HYBRID_WORK.after_resolver.py)
- ask_ollama (file: A_03_ORCHESTRATION/chat_router.HYBRID_WORK.hybrid_ok.py)
- ask_ollama (file: A_03_ORCHESTRATION/chat_router.HYBRID_WORK.py)
- ask_ollama (file: A_03_ORCHESTRATION/chat_router.py)
- ask_ollama (file: A_03_ORCHESTRATION/chat_router.STABLE_BEFORE_HYBRID.py)
- ask_ollama (file: A_03_ORCHESTRATION/chat_router.STABLE_TEST.py)
- ask_ollama (file: A_03_ORCHESTRATION/chat_router.WORKING_RUSSIAN_OK.py)
- ask_ollama (file: A_03_ORCHESTRATION/chat_router_test_restore.py)
- choose_model (file: A_03_ORCHESTRATION/chat_router.CLEAN_UTF8.py)
- choose_model (file: A_03_ORCHESTRATION/chat_router.HYBRID_WORK.after_import.py)
- choose_model (file: A_03_ORCHESTRATION/chat_router.HYBRID_WORK.after_resolver.py)
- choose_model (file: A_03_ORCHESTRATION/chat_router.HYBRID_WORK.hybrid_ok.py)
- choose_model (file: A_03_ORCHESTRATION/chat_router.HYBRID_WORK.py)
- choose_model (file: A_03_ORCHESTRATION/chat_router.py)
- choose_model (file: A_03_ORCHESTRATION/chat_router.STABLE_BEFORE_HYBRID.py)
- choose_model (file: A_03_ORCHESTRATION/chat_router.STABLE_TEST.py)
- choose_model (file: A_03_ORCHESTRATION/chat_router.WORKING_RUSSIAN_OK.py)
- choose_model (file: A_03_ORCHESTRATION/chat_router_test_restore.py)
- execute_repair (file: RUN_PIPELINE_V12.py)
- fail (file: A_01_CORE/memory_guardian.py)
- fetch_ollama_models (file: A_03_ORCHESTRATION/chat_router.CLEAN_UTF8.py)
- fetch_ollama_models (file: A_03_ORCHESTRATION/chat_router.HYBRID_WORK.after_import.py)
- fetch_ollama_models (file: A_03_ORCHESTRATION/chat_router.HYBRID_WORK.after_resolver.py)
- fetch_ollama_models (file: A_03_ORCHESTRATION/chat_router.HYBRID_WORK.hybrid_ok.py)
- fetch_ollama_models (file: A_03_ORCHESTRATION/chat_router.HYBRID_WORK.py)
- fetch_ollama_models (file: A_03_ORCHESTRATION/chat_router.py)
- fetch_ollama_models (file: A_03_ORCHESTRATION/chat_router.STABLE_BEFORE_HYBRID.py)
- fetch_ollama_models (file: A_03_ORCHESTRATION/chat_router.STABLE_TEST.py)
- fetch_ollama_models (file: A_03_ORCHESTRATION/chat_router.WORKING_RUSSIAN_OK.py)
- fetch_ollama_models (file: A_03_ORCHESTRATION/chat_router_test_restore.py)
- get_models (file: A_09_INTERFACE/test_ollama_connect.py)
- installed_models (file: A_99_TEST_DATA/model_olympics_v2.py)
- main (file: A_00_HEALER_UNIT/temp_test.py)
- main (file: A_09_INTERFACE/test_ollama_connect.py)
- main (file: A_09_TESTS/test_vision.py)
- main (file: A_99_TEST_DATA/BUTLER_OS_before_image_render.py)
- main (file: butler_capability_audit.py)
- main (file: BUTLER_OS.py)
- main (file: RUN_PIPELINE_V12.py)
- main (file: safe_change.py)
- main (file: system_doctor.py)
- main (file: verify_project.py)
- main (file: A_01_CORE/alarm.py)
- main (file: A_01_CORE/fix_butler.py)
- main (file: A_01_CORE/project_indexer.py)
- main (file: A_03_ENGINES/Vision_Engine/vision_tool.py)
- main (file: A_03_ORCHESTRATION/chat_router.CLEAN_UTF8.py)
- main (file: A_03_ORCHESTRATION/chat_router.HYBRID_WORK.after_import.py)
- main (file: A_03_ORCHESTRATION/chat_router.HYBRID_WORK.after_resolver.py)
- main (file: A_03_ORCHESTRATION/chat_router.HYBRID_WORK.hybrid_ok.py)
- main (file: A_03_ORCHESTRATION/chat_router.HYBRID_WORK.py)
- main (file: A_03_ORCHESTRATION/chat_router.py)
- main (file: A_03_ORCHESTRATION/chat_router.STABLE_BEFORE_HYBRID.py)
- main (file: A_03_ORCHESTRATION/chat_router.STABLE_TEST.py)
- main (file: A_03_ORCHESTRATION/chat_router.WORKING_RUSSIAN_OK.py)
- main (file: A_03_ORCHESTRATION/chat_router_test_restore.py)
- main (file: A_03_ORCHESTRATION/Console/butler_console.py)
- main (file: A_04_AGENTS/find_bills.py)
- main (file: A_04_AGENTS/ProjectDocumentationDepartment/Core/ast_parser.py)
- main (file: A_04_AGENTS/ProjectDocumentationDepartment/Core/evidence_doctor.py)
- pick_light_model (file: A_09_INTERFACE/test_ollama_connect.py)
- print_models (file: A_09_INTERFACE/test_ollama_connect.py)
- repair (file: system_doctor.py)

### CALLS:
- Constraints (file: A_07_CONFIG/execution_policy_schema.py)
- Constraints (file: 296)
- MainOrchestrator (file: 1485)
- MainOrchestrator (file: RUN_PIPELINE_V12.py)
- OllamaVisionBackend (file: 391)
- RegistryBrain (file: 1495)
- RegistryBrain (file: 1505)
- RegistryBrain (file: A_03_ORCHESTRATION/registry_brain.py)
- SemanticConstraintLayer (file: A_07_MEMORY/semantic_constraint_layer.py)
- SemanticConstraintLayer (file: 1216)
- _failure (file: 1201)
- ask_ollama (file: 1358)
- ask_ollama (file: 1364)
- ask_ollama (file: A_03_ORCHESTRATION/chat_router.CLEAN_UTF8.py)
- ask_ollama (file: A_03_ORCHESTRATION/chat_router.HYBRID_WORK.after_import.py)
- ask_ollama (file: A_03_ORCHESTRATION/chat_router.HYBRID_WORK.after_resolver.py)
- ask_ollama (file: A_03_ORCHESTRATION/chat_router.HYBRID_WORK.hybrid_ok.py)
- ask_ollama (file: A_03_ORCHESTRATION/chat_router.HYBRID_WORK.py)
- ask_ollama (file: A_03_ORCHESTRATION/chat_router.py)
- ask_ollama (file: A_03_ORCHESTRATION/chat_router.STABLE_BEFORE_HYBRID.py)
- ... and 76 more

### DEPENDENCY_NODES:
- Constraints (file: None)
- MainOrchestrator (file: None)
- OllamaVisionBackend (file: None)
- RegistryBrain (file: None)
- SemanticConstraintLayer (file: None)
- _failure (file: None)
- ask_ollama (file: None)
- ask_ollama_free_chat (file: None)
- auto_repair (file: None)
- choose_model (file: None)
- execute_repair (file: None)
- fail (file: None)
- failed_recipes (file: None)
- fetch_ollama_models (file: None)
- get_models (file: None)
- installed_models (file: None)
- main (file: None)
- mainloop (file: None)
- pick_light_model (file: None)
- print_models (file: None)
- ... and 1 more

### EXECUTION_FACTS:
- PHASE_1_INIT::BOOTSTRAP: DONE
- PHASE_1_MULTITASK_TEST::TEST_TASK_A: DONE
- PHASE_1_MULTITASK_TEST::TEST_TASK_B: DONE
- PHASE_1_MULTITASK_TEST::TEST_TASK_C: DONE
- PHASE_1_TEST_DIAGNOSTICS::AUDIT_VERIFY_HEALTH: DONE
- PHASE_3_CLEANUP_AND_BACKUP::RUN_CORE_BACKUP: DONE
- TEST_PHASE_1::PHASE_1_TASK_A: DONE
- TEST_PHASE_1::PHASE_1_TASK_B: DONE
- TEST_PHASE_2::PHASE_2_TASK_C: DONE
- TEST_PHASE_2::PHASE_2_TASK_D: DONE

### GOALS_FACTS:
- active_goal: BUTLER_RECIPE_LIBRARY
- current_phase: ROADMAP_6_PHASE_4_RECIPES
- subgoal: ROADMAP_6_PHASE_4_RECIPES status=COMPLETED
- task: task_run_full_audit status=COMPLETED
- task: task_verify_contour status=COMPLETED
- weight: autonomy=0.6
- weight: stability=1.0

### LINKS:
- {"metadata": {"context": "BootstrapCore.__init__", "line": 16}, "source": 1495, "target": "RegistryBrain", "type": "call"} (file: None)
- {"metadata": {"context": "BootstrapCore.init_system", "line": 45}, "source": 1495, "target": "auto_repair", "type": "call"} (file: None)
- {"metadata": {"context": "ButlerInteractiveChat.start_session", "line": 101}, "source": 241, "target": "ask_ollama_free_chat", "type": "call"} (file: None)
- {"metadata": {"context": "ButlerSystem.__init__", "line": 15}, "source": 1505, "target": "RegistryBrain", "type": "call"} (file: None)
- {"metadata": {"context": "ButlerSystem.clean_init", "line": 24}, "source": 1505, "target": "auto_repair", "type": "call"} (file: None)
- {"metadata": {"context": "PolicyLoader.default_policy", "line": 32}, "source": 296, "target": "Constraints", "type": "call"} (file: None)
- {"metadata": {"context": "ReferenceResolver.resolve", "line": 56}, "source": 1201, "target": "_failure", "type": "call"} (file: None)
- {"metadata": {"context": "ReferenceResolver.resolve", "line": 62}, "source": 1201, "target": "_failure", "type": "call"} (file: None)
- {"metadata": {"context": "ReferenceResolver.resolve", "line": 69}, "source": 1201, "target": "_failure", "type": "call"} (file: None)
- {"metadata": {"context": "ReferenceResolver.resolve", "line": 76}, "source": 1201, "target": "_failure", "type": "call"} (file: None)
- {"metadata": {"context": "ReferenceResolver.resolve", "line": 81}, "source": 1201, "target": "_failure", "type": "call"} (file: None)
- {"metadata": {"context": "ReferenceResolver.resolve", "line": 88}, "source": 1201, "target": "_failure", "type": "call"} (file: None)
- {"metadata": {"context": "ReferenceResolver.resolve", "line": 90}, "source": 1201, "target": "_failure", "type": "call"} (file: None)
- {"metadata": {"context": "VisionEngine.__init__", "line": 10}, "source": 391, "target": "OllamaVisionBackend", "type": "call"} (file: None)
- {"metadata": {"context": "dispatch", "line": 103}, "source": 539, "target": "main", "type": "call"} (file: None)
- {"metadata": {"context": "dispatch", "line": 147}, "source": 539, "target": "main", "type": "call"} (file: None)
- {"metadata": {"context": "handle_chat", "line": 169}, "source": 1364, "target": "choose_model", "type": "call"} (file: None)
- {"metadata": {"context": "handle_chat", "line": 169}, "source": 417, "target": "choose_model", "type": "call"} (file: None)
- {"metadata": {"context": "handle_chat", "line": 186}, "source": 414, "target": "choose_model", "type": "call"} (file: None)
- {"metadata": {"context": "handle_chat", "line": 190}, "source": 1364, "target": "ask_ollama", "type": "call"} (file: None)
- ... and 142 more

---

## CAPABILITY: OLLAMA
**TOTAL EVIDENCE:** 309
**STATUS:** READY
**MAIN ENTRY:** ask_ollama

### FILES (canonical):
- A_07_MEMORY/change_request_manager.py
- A_07_MEMORY/context_budget_manager.py
- A_07_MEMORY/SESSION/session_manager_poly.py
- A_09_INTERFACE/test_ollama_connect.py
- A_99_TEST_DATA/model_olympics_v2.py
- A_02_MANAGERS/ArchitectAgent/context_provider.py
- A_02_MANAGERS/ArchitectAgent/queue_manager.py
- A_02_MANAGERS/catalog_manager.py
- A_02_MANAGERS/dream_manager.py
- A_02_MANAGERS/memory_manager.py
- A_02_MANAGERS/provider_manager.py
- A_02_MANAGERS/queue_manager.py
- A_02_MANAGERS/session_manager.py
- A_03_HANDLERS/ollama_vision_backend.py
- A_03_ORCHESTRATION/chat_router.CLEAN_UTF8.py
- A_03_ORCHESTRATION/chat_router.HYBRID_WORK.after_import.py
- A_03_ORCHESTRATION/chat_router.HYBRID_WORK.after_resolver.py
- A_03_ORCHESTRATION/chat_router.HYBRID_WORK.hybrid_ok.py
- A_03_ORCHESTRATION/chat_router.HYBRID_WORK.py
- A_03_ORCHESTRATION/chat_router.py
- A_03_ORCHESTRATION/chat_router.STABLE_BEFORE_HYBRID.py
- A_03_ORCHESTRATION/chat_router.STABLE_TEST.py
- A_03_ORCHESTRATION/chat_router.WORKING_RUSSIAN_OK.py
- A_03_ORCHESTRATION/chat_router_test_restore.py

### CLASSES:
- ButlerDreamManager (file: A_02_MANAGERS/dream_manager.py)
- ButlerSessionManager (file: A_02_MANAGERS/session_manager.py)
- CatalogManager (file: A_02_MANAGERS/catalog_manager.py)
- ChangeRequestManager (file: A_07_MEMORY/change_request_manager.py)
- ContextBudgetManager (file: A_07_MEMORY/context_budget_manager.py)
- ContextProvider (file: A_02_MANAGERS/ArchitectAgent/context_provider.py)
- MemoryManager (file: A_02_MANAGERS/memory_manager.py)
- OllamaVisionBackend (file: A_03_HANDLERS/ollama_vision_backend.py)
- ProviderManager (file: A_02_MANAGERS/provider_manager.py)
- QueueManager (file: A_02_MANAGERS/ArchitectAgent/queue_manager.py)
- QueueManager (file: A_02_MANAGERS/queue_manager.py)
- SessionManagerPoly (file: A_07_MEMORY/SESSION/session_manager_poly.py)

### FUNCTIONS:
- ask_ollama (file: A_03_ORCHESTRATION/chat_router.CLEAN_UTF8.py)
- ask_ollama (file: A_03_ORCHESTRATION/chat_router.HYBRID_WORK.after_import.py)
- ask_ollama (file: A_03_ORCHESTRATION/chat_router.HYBRID_WORK.after_resolver.py)
- ask_ollama (file: A_03_ORCHESTRATION/chat_router.HYBRID_WORK.hybrid_ok.py)
- ask_ollama (file: A_03_ORCHESTRATION/chat_router.HYBRID_WORK.py)
- ask_ollama (file: A_03_ORCHESTRATION/chat_router.py)
- ask_ollama (file: A_03_ORCHESTRATION/chat_router.STABLE_BEFORE_HYBRID.py)
- ask_ollama (file: A_03_ORCHESTRATION/chat_router.STABLE_TEST.py)
- ask_ollama (file: A_03_ORCHESTRATION/chat_router.WORKING_RUSSIAN_OK.py)
- ask_ollama (file: A_03_ORCHESTRATION/chat_router_test_restore.py)
- choose_model (file: A_03_ORCHESTRATION/chat_router.CLEAN_UTF8.py)
- choose_model (file: A_03_ORCHESTRATION/chat_router.HYBRID_WORK.after_import.py)
- choose_model (file: A_03_ORCHESTRATION/chat_router.HYBRID_WORK.after_resolver.py)
- choose_model (file: A_03_ORCHESTRATION/chat_router.HYBRID_WORK.hybrid_ok.py)
- choose_model (file: A_03_ORCHESTRATION/chat_router.HYBRID_WORK.py)
- choose_model (file: A_03_ORCHESTRATION/chat_router.py)
- choose_model (file: A_03_ORCHESTRATION/chat_router.STABLE_BEFORE_HYBRID.py)
- choose_model (file: A_03_ORCHESTRATION/chat_router.STABLE_TEST.py)
- choose_model (file: A_03_ORCHESTRATION/chat_router.WORKING_RUSSIAN_OK.py)
- choose_model (file: A_03_ORCHESTRATION/chat_router_test_restore.py)
- fetch_ollama_models (file: A_03_ORCHESTRATION/chat_router.CLEAN_UTF8.py)
- fetch_ollama_models (file: A_03_ORCHESTRATION/chat_router.HYBRID_WORK.after_import.py)
- fetch_ollama_models (file: A_03_ORCHESTRATION/chat_router.HYBRID_WORK.after_resolver.py)
- fetch_ollama_models (file: A_03_ORCHESTRATION/chat_router.HYBRID_WORK.hybrid_ok.py)
- fetch_ollama_models (file: A_03_ORCHESTRATION/chat_router.HYBRID_WORK.py)
- fetch_ollama_models (file: A_03_ORCHESTRATION/chat_router.py)
- fetch_ollama_models (file: A_03_ORCHESTRATION/chat_router.STABLE_BEFORE_HYBRID.py)
- fetch_ollama_models (file: A_03_ORCHESTRATION/chat_router.STABLE_TEST.py)
- fetch_ollama_models (file: A_03_ORCHESTRATION/chat_router.WORKING_RUSSIAN_OK.py)
- fetch_ollama_models (file: A_03_ORCHESTRATION/chat_router_test_restore.py)
- get_models (file: A_09_INTERFACE/test_ollama_connect.py)
- installed_models (file: A_99_TEST_DATA/model_olympics_v2.py)
- pick_light_model (file: A_09_INTERFACE/test_ollama_connect.py)
- print_models (file: A_09_INTERFACE/test_ollama_connect.py)

### CALLS:
- ButlerDreamManager (file: A_02_MANAGERS/dream_manager.py)
- ButlerSessionManager (file: 1157)
- ButlerSessionManager (file: A_03_ORCHESTRATION/chat_router.CLEAN_UTF8.py)
- CatalogManager (file: 1125)
- CatalogManager (file: 1337)
- CatalogManager (file: 1339)
- CatalogManager (file: 1441)
- CatalogManager (file: 1454)
- CatalogManager (file: 209)
- CatalogManager (file: 217)
- CatalogManager (file: 221)
- CatalogManager (file: 231)
- CatalogManager (file: 236)
- CatalogManager (file: 241)
- CatalogManager (file: 245)
- CatalogManager (file: 251)
- CatalogManager (file: 253)
- CatalogManager (file: 255)
- CatalogManager (file: 257)
- CatalogManager (file: 508)
- ... and 69 more

### DEPENDENCY_NODES:
- ButlerDreamManager (file: None)
- ButlerSessionManager (file: None)
- CatalogManager (file: None)
- ChangeRequestManager (file: None)
- ContextBudgetManager (file: None)
- ContextProvider (file: None)
- MemoryManager (file: None)
- OllamaVisionBackend (file: None)
- ProviderManager (file: None)
- QueueManager (file: None)
- SessionManagerPoly (file: None)
- ask_ollama (file: None)
- ask_ollama_free_chat (file: None)
- choose_model (file: None)
- fetch_ollama_models (file: None)
- get_models (file: None)
- installed_models (file: None)
- pick_light_model (file: None)
- print_models (file: None)

### EXECUTION_FACTS:
- PHASE_1_INIT::BOOTSTRAP: DONE
- PHASE_1_MULTITASK_TEST::TEST_TASK_A: DONE
- PHASE_1_MULTITASK_TEST::TEST_TASK_B: DONE
- PHASE_1_MULTITASK_TEST::TEST_TASK_C: DONE
- PHASE_1_TEST_DIAGNOSTICS::AUDIT_VERIFY_HEALTH: DONE
- PHASE_3_CLEANUP_AND_BACKUP::RUN_CORE_BACKUP: DONE
- TEST_PHASE_1::PHASE_1_TASK_A: DONE
- TEST_PHASE_1::PHASE_1_TASK_B: DONE
- TEST_PHASE_2::PHASE_2_TASK_C: DONE
- TEST_PHASE_2::PHASE_2_TASK_D: DONE

### GOALS_FACTS:
- active_goal: BUTLER_RECIPE_LIBRARY
- current_phase: ROADMAP_6_PHASE_4_RECIPES
- subgoal: ROADMAP_6_PHASE_4_RECIPES status=COMPLETED
- task: task_run_full_audit status=COMPLETED
- task: task_verify_contour status=COMPLETED
- weight: autonomy=0.6
- weight: stability=1.0

### LINKS:
- {"metadata": {"context": "AgentLoopExecutor.__init__", "line": 11}, "source": 1114, "target": "ChangeRequestManager", "type": "call"} (file: None)
- {"metadata": {"context": "ArchitectAgent.__init__", "line": 29}, "source": 261, "target": "ContextProvider", "type": "call"} (file: None)
- {"metadata": {"context": "ArchitectAgent.__init__", "line": 33}, "source": 261, "target": "QueueManager", "type": "call"} (file: None)
- {"metadata": {"context": "ButlerDiagnostics.__init__", "line": 14}, "source": 209, "target": "CatalogManager", "type": "call"} (file: None)
- {"metadata": {"context": "ButlerDiagnostics.__init__", "line": 14}, "source": 245, "target": "CatalogManager", "type": "call"} (file: None)
- {"metadata": {"context": "ButlerInteractiveChat.__init__", "line": 37}, "source": 241, "target": "CatalogManager", "type": "call"} (file: None)
- {"metadata": {"context": "ButlerInteractiveChat.start_session", "line": 101}, "source": 241, "target": "ask_ollama_free_chat", "type": "call"} (file: None)
- {"metadata": {"context": "ButlerMcpServer.__init__", "line": 10}, "source": 217, "target": "CatalogManager", "type": "call"} (file: None)
- {"metadata": {"context": "ButlerMcpServer.__init__", "line": 10}, "source": 251, "target": "CatalogManager", "type": "call"} (file: None)
- {"metadata": {"context": "CatalogSearchBridge.__init__", "line": 10}, "source": 1125, "target": "SessionManagerPoly", "type": "call"} (file: None)
- {"metadata": {"context": "CatalogSearchBridge.__init__", "line": 9}, "source": 1125, "target": "CatalogManager", "type": "call"} (file: None)
- {"metadata": {"context": "DispatcherAgent.__init__", "line": 22}, "source": 630, "target": "CatalogManager", "type": "call"} (file: None)
- {"metadata": {"context": "DispatcherAgent.__init__", "line": 34}, "source": 508, "target": "CatalogManager", "type": "call"} (file: None)
- {"metadata": {"context": "LoopOrchestratorV3_EXEC_V2.__init__", "line": 39}, "source": 1118, "target": "ChangeRequestManager", "type": "call"} (file: None)
- {"metadata": {"context": "LoopOrchestratorV3_MASTER_TRUTH.__init__", "line": 47}, "source": 1117, "target": "ChangeRequestManager", "type": "call"} (file: None)
- {"metadata": {"context": "MainOrchestrator.__init__", "line": 8}, "source": 253, "target": "CatalogManager", "type": "call"} (file: None)
- {"metadata": {"context": "MainOrchestrator.__init__", "line": 9}, "source": 221, "target": "CatalogManager", "type": "call"} (file: None)
- {"metadata": {"context": "MemoryFacade.__init__", "line": 16}, "source": 1144, "target": "ChangeRequestManager", "type": "call"} (file: None)
- {"metadata": {"context": "MemoryFacade.__init__", "line": 17}, "source": 1145, "target": "ChangeRequestManager", "type": "call"} (file: None)
- {"metadata": {"context": "MemoryLayer.__init__", "line": 8}, "source": 1157, "target": "ButlerSessionManager", "type": "call"} (file: None)
- ... and 118 more

---

## CAPABILITY: PROVIDER
**TOTAL EVIDENCE:** 246
**STATUS:** READY
**MAIN ENTRY:** ask_ollama

### FILES (canonical):
- A_07_MEMORY/change_request_manager.py
- A_07_MEMORY/context_budget_manager.py
- A_07_MEMORY/SESSION/session_manager_poly.py
- A_02_MANAGERS/ArchitectAgent/context_provider.py
- A_02_MANAGERS/ArchitectAgent/queue_manager.py
- A_02_MANAGERS/catalog_manager.py
- A_02_MANAGERS/dream_manager.py
- A_02_MANAGERS/memory_manager.py
- A_02_MANAGERS/provider_manager.py
- A_02_MANAGERS/queue_manager.py
- A_02_MANAGERS/session_manager.py
- A_03_HANDLERS/ollama_vision_backend.py
- A_03_ORCHESTRATION/chat_router.CLEAN_UTF8.py
- A_03_ORCHESTRATION/chat_router.HYBRID_WORK.after_import.py
- A_03_ORCHESTRATION/chat_router.HYBRID_WORK.after_resolver.py
- A_03_ORCHESTRATION/chat_router.HYBRID_WORK.hybrid_ok.py
- A_03_ORCHESTRATION/chat_router.HYBRID_WORK.py
- A_03_ORCHESTRATION/chat_router.py
- A_03_ORCHESTRATION/chat_router.STABLE_BEFORE_HYBRID.py
- A_03_ORCHESTRATION/chat_router.STABLE_TEST.py
- A_03_ORCHESTRATION/chat_router.WORKING_RUSSIAN_OK.py
- A_03_ORCHESTRATION/chat_router_test_restore.py

### CLASSES:
- ButlerDreamManager (file: A_02_MANAGERS/dream_manager.py)
- ButlerSessionManager (file: A_02_MANAGERS/session_manager.py)
- CatalogManager (file: A_02_MANAGERS/catalog_manager.py)
- ChangeRequestManager (file: A_07_MEMORY/change_request_manager.py)
- ContextBudgetManager (file: A_07_MEMORY/context_budget_manager.py)
- ContextProvider (file: A_02_MANAGERS/ArchitectAgent/context_provider.py)
- MemoryManager (file: A_02_MANAGERS/memory_manager.py)
- OllamaVisionBackend (file: A_03_HANDLERS/ollama_vision_backend.py)
- ProviderManager (file: A_02_MANAGERS/provider_manager.py)
- QueueManager (file: A_02_MANAGERS/ArchitectAgent/queue_manager.py)
- QueueManager (file: A_02_MANAGERS/queue_manager.py)
- SessionManagerPoly (file: A_07_MEMORY/SESSION/session_manager_poly.py)

### FUNCTIONS:
- ask_ollama (file: A_03_ORCHESTRATION/chat_router.CLEAN_UTF8.py)
- ask_ollama (file: A_03_ORCHESTRATION/chat_router.HYBRID_WORK.after_import.py)
- ask_ollama (file: A_03_ORCHESTRATION/chat_router.HYBRID_WORK.after_resolver.py)
- ask_ollama (file: A_03_ORCHESTRATION/chat_router.HYBRID_WORK.hybrid_ok.py)
- ask_ollama (file: A_03_ORCHESTRATION/chat_router.HYBRID_WORK.py)
- ask_ollama (file: A_03_ORCHESTRATION/chat_router.py)
- ask_ollama (file: A_03_ORCHESTRATION/chat_router.STABLE_BEFORE_HYBRID.py)
- ask_ollama (file: A_03_ORCHESTRATION/chat_router.STABLE_TEST.py)
- ask_ollama (file: A_03_ORCHESTRATION/chat_router.WORKING_RUSSIAN_OK.py)
- ask_ollama (file: A_03_ORCHESTRATION/chat_router_test_restore.py)
- fetch_ollama_models (file: A_03_ORCHESTRATION/chat_router.CLEAN_UTF8.py)
- fetch_ollama_models (file: A_03_ORCHESTRATION/chat_router.HYBRID_WORK.after_import.py)
- fetch_ollama_models (file: A_03_ORCHESTRATION/chat_router.HYBRID_WORK.after_resolver.py)
- fetch_ollama_models (file: A_03_ORCHESTRATION/chat_router.HYBRID_WORK.hybrid_ok.py)
- fetch_ollama_models (file: A_03_ORCHESTRATION/chat_router.HYBRID_WORK.py)
- fetch_ollama_models (file: A_03_ORCHESTRATION/chat_router.py)
- fetch_ollama_models (file: A_03_ORCHESTRATION/chat_router.STABLE_BEFORE_HYBRID.py)
- fetch_ollama_models (file: A_03_ORCHESTRATION/chat_router.STABLE_TEST.py)
- fetch_ollama_models (file: A_03_ORCHESTRATION/chat_router.WORKING_RUSSIAN_OK.py)
- fetch_ollama_models (file: A_03_ORCHESTRATION/chat_router_test_restore.py)

### CALLS:
- ButlerDreamManager (file: A_02_MANAGERS/dream_manager.py)
- ButlerSessionManager (file: 1157)
- ButlerSessionManager (file: A_03_ORCHESTRATION/chat_router.CLEAN_UTF8.py)
- CatalogManager (file: 1125)
- CatalogManager (file: 1337)
- CatalogManager (file: 1339)
- CatalogManager (file: 1441)
- CatalogManager (file: 1454)
- CatalogManager (file: 209)
- CatalogManager (file: 217)
- CatalogManager (file: 221)
- CatalogManager (file: 231)
- CatalogManager (file: 236)
- CatalogManager (file: 241)
- CatalogManager (file: 245)
- CatalogManager (file: 251)
- CatalogManager (file: 253)
- CatalogManager (file: 255)
- CatalogManager (file: 257)
- CatalogManager (file: 508)
- ... and 53 more

### DEPENDENCY_NODES:
- ButlerDreamManager (file: None)
- ButlerSessionManager (file: None)
- CatalogManager (file: None)
- ChangeRequestManager (file: None)
- ContextBudgetManager (file: None)
- ContextProvider (file: None)
- MemoryManager (file: None)
- OllamaVisionBackend (file: None)
- ProviderManager (file: None)
- QueueManager (file: None)
- SessionManagerPoly (file: None)
- ask_ollama (file: None)
- ask_ollama_free_chat (file: None)
- fetch_ollama_models (file: None)

### EXECUTION_FACTS:
- PHASE_1_INIT::BOOTSTRAP: DONE
- PHASE_1_MULTITASK_TEST::TEST_TASK_A: DONE
- PHASE_1_MULTITASK_TEST::TEST_TASK_B: DONE
- PHASE_1_MULTITASK_TEST::TEST_TASK_C: DONE
- PHASE_1_TEST_DIAGNOSTICS::AUDIT_VERIFY_HEALTH: DONE
- PHASE_3_CLEANUP_AND_BACKUP::RUN_CORE_BACKUP: DONE
- TEST_PHASE_1::PHASE_1_TASK_A: DONE
- TEST_PHASE_1::PHASE_1_TASK_B: DONE
- TEST_PHASE_2::PHASE_2_TASK_C: DONE
- TEST_PHASE_2::PHASE_2_TASK_D: DONE

### GOALS_FACTS:
- active_goal: BUTLER_RECIPE_LIBRARY
- current_phase: ROADMAP_6_PHASE_4_RECIPES
- subgoal: ROADMAP_6_PHASE_4_RECIPES status=COMPLETED
- task: task_run_full_audit status=COMPLETED
- task: task_verify_contour status=COMPLETED
- weight: autonomy=0.6
- weight: stability=1.0

### LINKS:
- {"metadata": {"context": "AgentLoopExecutor.__init__", "line": 11}, "source": 1114, "target": "ChangeRequestManager", "type": "call"} (file: None)
- {"metadata": {"context": "ArchitectAgent.__init__", "line": 29}, "source": 261, "target": "ContextProvider", "type": "call"} (file: None)
- {"metadata": {"context": "ArchitectAgent.__init__", "line": 33}, "source": 261, "target": "QueueManager", "type": "call"} (file: None)
- {"metadata": {"context": "ButlerDiagnostics.__init__", "line": 14}, "source": 209, "target": "CatalogManager", "type": "call"} (file: None)
- {"metadata": {"context": "ButlerDiagnostics.__init__", "line": 14}, "source": 245, "target": "CatalogManager", "type": "call"} (file: None)
- {"metadata": {"context": "ButlerInteractiveChat.__init__", "line": 37}, "source": 241, "target": "CatalogManager", "type": "call"} (file: None)
- {"metadata": {"context": "ButlerInteractiveChat.start_session", "line": 101}, "source": 241, "target": "ask_ollama_free_chat", "type": "call"} (file: None)
- {"metadata": {"context": "ButlerMcpServer.__init__", "line": 10}, "source": 217, "target": "CatalogManager", "type": "call"} (file: None)
- {"metadata": {"context": "ButlerMcpServer.__init__", "line": 10}, "source": 251, "target": "CatalogManager", "type": "call"} (file: None)
- {"metadata": {"context": "CatalogSearchBridge.__init__", "line": 10}, "source": 1125, "target": "SessionManagerPoly", "type": "call"} (file: None)
- {"metadata": {"context": "CatalogSearchBridge.__init__", "line": 9}, "source": 1125, "target": "CatalogManager", "type": "call"} (file: None)
- {"metadata": {"context": "DispatcherAgent.__init__", "line": 22}, "source": 630, "target": "CatalogManager", "type": "call"} (file: None)
- {"metadata": {"context": "DispatcherAgent.__init__", "line": 34}, "source": 508, "target": "CatalogManager", "type": "call"} (file: None)
- {"metadata": {"context": "LoopOrchestratorV3_EXEC_V2.__init__", "line": 39}, "source": 1118, "target": "ChangeRequestManager", "type": "call"} (file: None)
- {"metadata": {"context": "LoopOrchestratorV3_MASTER_TRUTH.__init__", "line": 47}, "source": 1117, "target": "ChangeRequestManager", "type": "call"} (file: None)
- {"metadata": {"context": "MainOrchestrator.__init__", "line": 8}, "source": 253, "target": "CatalogManager", "type": "call"} (file: None)
- {"metadata": {"context": "MainOrchestrator.__init__", "line": 9}, "source": 221, "target": "CatalogManager", "type": "call"} (file: None)
- {"metadata": {"context": "MemoryFacade.__init__", "line": 16}, "source": 1144, "target": "ChangeRequestManager", "type": "call"} (file: None)
- {"metadata": {"context": "MemoryFacade.__init__", "line": 17}, "source": 1145, "target": "ChangeRequestManager", "type": "call"} (file: None)
- {"metadata": {"context": "MemoryLayer.__init__", "line": 8}, "source": 1157, "target": "ButlerSessionManager", "type": "call"} (file: None)
- ... and 90 more

---

## CAPABILITY: AUTOMATION
**TOTAL EVIDENCE:** 356
**STATUS:** READY
**MAIN ENTRY:** Recipe

### FILES (canonical):
- A_07_CONFIG/execution_context_schema.py
- A_07_CONFIG/execution_policy_schema.py
- A_07_CONFIG/recipe_schema.py
- A_07_MEMORY/agent_loop_executor.py
- A_07_MEMORY/agent_runtime_v2.py
- A_07_MEMORY/execution_registry.py
- A_07_MEMORY/png_workflow_memory.py
- Butler_Gate.py
- RUN_PIPELINE.py
- RUN_PIPELINE_V12.py
- A_01_CORE/execution_loop.py
- A_01_CORE/task_feeder.py
- A_02_MANAGERS/ArchitectAgent/planner_pipeline.py
- A_02_MANAGERS/ArchitectAgent/queue_manager.py
- A_02_MANAGERS/ArchitectAgent/recipe_builder.py
- A_02_MANAGERS/ArchitectAgent/recipe_generator.py
- A_02_MANAGERS/ArchitectAgent/task_contract_builder.py
- A_02_MANAGERS/ExecutionMonitor/execution_history.py
- A_02_MANAGERS/ExecutionMonitor/execution_monitor.py
- A_02_MANAGERS/ExecutionMonitor/execution_state.py
- A_02_MANAGERS/Planner/task_planner.py
- A_02_MANAGERS/queue_manager.py
- A_02_MANAGERS/recipe_generator.py
- A_02_MANAGERS/recipe_validator.py
- A_02_MANAGERS/TaskRunner/automatic_verifier.py
- A_02_MANAGERS/TaskRunner/execution_result.py
- A_02_MANAGERS/TaskRunner/ExecutionAdapters/base_adapter.py
- A_02_MANAGERS/TaskRunner/ExecutionAdapters/powershell_adapter.py
- A_02_MANAGERS/TaskRunner/ExecutionAdapters/python_adapter.py
- A_02_MANAGERS/TaskRunner/executor_factory.py
- A_02_MANAGERS/TaskRunner/recipe_builder.py
- A_02_MANAGERS/TaskRunner/recipe_executor.py
- A_02_MANAGERS/TaskRunner/recipe_loader.py
- A_02_MANAGERS/TaskRunner/recipe_queue_watcher.py
- A_02_MANAGERS/TaskRunner/recipe_writer.py
- A_02_MANAGERS/TaskRunner/runner.py
- A_03_EXECUTORS/executor.py
- A_03_HANDLERS/pdf_ocr_pipeline.py
- A_03_ORCHESTRATION/autonomous_loop.py
- A_03_ORCHESTRATION/butler_harness.py
- A_03_ORCHESTRATION/session_queue.py
- A_04_AGENTS/ProjectDocumentationDepartment/Core/Discovery/execution_registry_discovery_agent.py
- A_04_AGENTS/ProjectDocumentationDepartment/Core/engineering_pipeline.py
- A_04_AGENTS/ProjectDocumentationDepartment/Core/Scanners/execution_scanner.py

### CLASSES:
- AgentLoopExecutor (file: A_07_MEMORY/agent_loop_executor.py)
- AutomaticVerifier (file: A_02_MANAGERS/TaskRunner/automatic_verifier.py)
- AutonomousLoop (file: A_03_ORCHESTRATION/autonomous_loop.py)
- BaseExecutionAdapter (file: A_02_MANAGERS/TaskRunner/ExecutionAdapters/base_adapter.py)
- EngineeringPipeline (file: A_04_AGENTS/ProjectDocumentationDepartment/Core/engineering_pipeline.py)
- ExecutionContext (file: A_07_CONFIG/execution_context_schema.py)
- ExecutionHistory (file: A_02_MANAGERS/ExecutionMonitor/execution_history.py)
- ExecutionLoop (file: A_01_CORE/execution_loop.py)
- ExecutionMemoryV2 (file: A_07_MEMORY/agent_runtime_v2.py)
- ExecutionMonitor (file: A_02_MANAGERS/ExecutionMonitor/execution_monitor.py)
- ExecutionPolicy (file: A_07_CONFIG/execution_policy_schema.py)
- ExecutionRegistry (file: A_07_MEMORY/execution_registry.py)
- ExecutionRegistryDiscoveryAgent (file: A_04_AGENTS/ProjectDocumentationDepartment/Core/Discovery/execution_registry_discovery_agent.py)
- ExecutionResult (file: A_02_MANAGERS/TaskRunner/execution_result.py)
- ExecutionScanner (file: A_04_AGENTS/ProjectDocumentationDepartment/Core/Scanners/execution_scanner.py)
- ExecutionState (file: A_02_MANAGERS/ExecutionMonitor/execution_state.py)
- Executor (file: A_03_EXECUTORS/executor.py)
- ExecutorFactory (file: A_02_MANAGERS/TaskRunner/executor_factory.py)
- PDFOCRPipeline (file: A_03_HANDLERS/pdf_ocr_pipeline.py)
- PNGWorkflowMemory (file: A_07_MEMORY/png_workflow_memory.py)
- PlannerPipeline (file: A_02_MANAGERS/ArchitectAgent/planner_pipeline.py)
- PowerShellExecutionAdapter (file: A_02_MANAGERS/TaskRunner/ExecutionAdapters/powershell_adapter.py)
- PythonExecutionAdapter (file: A_02_MANAGERS/TaskRunner/ExecutionAdapters/python_adapter.py)
- QueueManager (file: A_02_MANAGERS/ArchitectAgent/queue_manager.py)
- QueueManager (file: A_02_MANAGERS/queue_manager.py)
- Recipe (file: A_07_CONFIG/recipe_schema.py)
- RecipeBuilder (file: A_02_MANAGERS/ArchitectAgent/recipe_builder.py)
- RecipeBuilder (file: A_02_MANAGERS/TaskRunner/recipe_builder.py)
- RecipeExecutor (file: A_02_MANAGERS/TaskRunner/recipe_executor.py)
- RecipeGenerator (file: A_02_MANAGERS/ArchitectAgent/recipe_generator.py)
- RecipeGenerator (file: A_02_MANAGERS/recipe_generator.py)
- RecipeLoader (file: A_02_MANAGERS/TaskRunner/recipe_loader.py)
- RecipeQueueWatcher (file: A_02_MANAGERS/TaskRunner/recipe_queue_watcher.py)
- RecipeStep (file: A_07_CONFIG/recipe_schema.py)
- RecipeValidator (file: A_02_MANAGERS/recipe_validator.py)
- RecipeWriter (file: A_02_MANAGERS/TaskRunner/recipe_writer.py)
- SessionQueue (file: A_03_ORCHESTRATION/session_queue.py)
- TaskContractBuilder (file: A_02_MANAGERS/ArchitectAgent/task_contract_builder.py)
- TaskFeeder (file: A_01_CORE/task_feeder.py)
- TaskPlanner (file: A_02_MANAGERS/Planner/task_planner.py)
- TaskRunner (file: A_02_MANAGERS/TaskRunner/runner.py)

### FUNCTIONS:
- run_guarded_task (file: Butler_Gate.py)
- run_pipeline (file: RUN_PIPELINE.py)
- run_pipeline (file: RUN_PIPELINE_V12.py)
- sample_executor (file: A_03_ORCHESTRATION/butler_harness.py)

### CALLS:
- AutonomousLoop (file: A_03_ORCHESTRATION/autonomous_loop.py)
- EngineeringPipeline (file: 611)
- ExecutionContext (file: A_07_CONFIG/execution_context_schema.py)
- ExecutionLoop (file: 1495)
- ExecutionLoop (file: 1505)
- ExecutionLoop (file: A_01_CORE/execution_loop.py)
- ExecutionMemoryV2 (file: A_07_MEMORY/agent_runtime_v2.py)
- ExecutionMonitor (file: A_02_MANAGERS/ExecutionMonitor/execution_monitor.py)
- ExecutionPolicy (file: A_07_CONFIG/execution_policy_schema.py)
- ExecutionPolicy (file: 296)
- ExecutionRegistry (file: 1117)
- ExecutionResult (file: A_02_MANAGERS/TaskRunner/automatic_verifier.py)
- ExecutionResult (file: A_02_MANAGERS/TaskRunner/execution_result.py)
- ExecutionResult (file: A_02_MANAGERS/TaskRunner/ExecutionAdapters/powershell_adapter.py)
- ExecutionResult (file: A_02_MANAGERS/TaskRunner/ExecutionAdapters/python_adapter.py)
- ExecutionResult (file: A_02_MANAGERS/TaskRunner/recipe_executor.py)
- ExecutionScanner (file: A_04_AGENTS/ProjectDocumentationDepartment/Core/engineering_pipeline.py)
- ExecutionScanner (file: 591)
- Executor (file: A_03_EXECUTORS/executor.py)
- PDFOCRPipeline (file: 1349)
- ... and 50 more

### DEPENDENCY_NODES:
- A_02_MANAGERS.ExecutionMonitor.execution_history (file: None)
- A_02_MANAGERS.ExecutionMonitor.execution_state (file: None)
- A_02_MANAGERS.ExecutionMonitor.system_state (file: None)
- A_02_MANAGERS.ExecutionPolicyEngine.policy_loader (file: None)
- A_02_MANAGERS.TaskRunner.ExecutionAdapters.base_adapter (file: None)
- A_02_MANAGERS.TaskRunner.ExecutionAdapters.powershell_adapter (file: None)
- A_02_MANAGERS.TaskRunner.ExecutionAdapters.python_adapter (file: None)
- A_02_MANAGERS.TaskRunner.automatic_verifier (file: None)
- A_02_MANAGERS.TaskRunner.execution_result (file: None)
- A_02_MANAGERS.TaskRunner.executor_factory (file: None)
- A_02_MANAGERS.TaskRunner.recipe_builder (file: None)
- A_02_MANAGERS.TaskRunner.recipe_executor (file: None)
- A_02_MANAGERS.TaskRunner.recipe_loader (file: None)
- A_02_MANAGERS.TaskRunner.recipe_queue_watcher (file: None)
- A_02_MANAGERS.TaskRunner.recipe_writer (file: None)
- A_02_MANAGERS.TaskRunner.runner_once (file: None)
- A_02_MANAGERS.recipe_generator (file: None)
- A_02_MANAGERS.recipe_validator (file: None)
- A_07_CONFIG.recipe_schema (file: None)
- AutonomousLoop (file: None)
- ... and 33 more

### EXECUTION_FACTS:
- PHASE_1_INIT::BOOTSTRAP: DONE
- PHASE_1_MULTITASK_TEST::TEST_TASK_A: DONE
- PHASE_1_MULTITASK_TEST::TEST_TASK_B: DONE
- PHASE_1_MULTITASK_TEST::TEST_TASK_C: DONE
- PHASE_1_TEST_DIAGNOSTICS::AUDIT_VERIFY_HEALTH: DONE
- PHASE_3_CLEANUP_AND_BACKUP::RUN_CORE_BACKUP: DONE
- TEST_PHASE_1::PHASE_1_TASK_A: DONE
- TEST_PHASE_1::PHASE_1_TASK_B: DONE
- TEST_PHASE_2::PHASE_2_TASK_C: DONE
- TEST_PHASE_2::PHASE_2_TASK_D: DONE

### GOALS_FACTS:
- active_goal: BUTLER_RECIPE_LIBRARY
- current_phase: ROADMAP_6_PHASE_4_RECIPES
- subgoal: ROADMAP_6_PHASE_4_RECIPES status=COMPLETED
- task: task_run_full_audit status=COMPLETED
- task: task_verify_contour status=COMPLETED
- weight: autonomy=0.6
- weight: stability=1.0

### IMPORTS:
- A_02_MANAGERS.ExecutionMonitor.execution_history (file: A_02_MANAGERS/ExecutionMonitor/execution_state.py)
- A_02_MANAGERS.ExecutionMonitor.execution_state (file: 295)
- A_02_MANAGERS.ExecutionMonitor.system_state (file: 305)
- A_02_MANAGERS.ExecutionPolicyEngine.policy_loader (file: A_07_CONFIG/execution_context_schema.py)
- A_02_MANAGERS.ExecutionPolicyEngine.policy_loader (file: 297)
- A_02_MANAGERS.ExecutionPolicyEngine.policy_loader (file: 298)
- A_02_MANAGERS.TaskRunner.ExecutionAdapters.base_adapter (file: A_02_MANAGERS/TaskRunner/ExecutionAdapters/powershell_adapter.py)
- A_02_MANAGERS.TaskRunner.ExecutionAdapters.base_adapter (file: A_02_MANAGERS/TaskRunner/ExecutionAdapters/python_adapter.py)
- A_02_MANAGERS.TaskRunner.ExecutionAdapters.powershell_adapter (file: A_02_MANAGERS/TaskRunner/executor_factory.py)
- A_02_MANAGERS.TaskRunner.ExecutionAdapters.python_adapter (file: A_02_MANAGERS/TaskRunner/executor_factory.py)
- A_02_MANAGERS.TaskRunner.automatic_verifier (file: 358)
- A_02_MANAGERS.TaskRunner.execution_result (file: A_02_MANAGERS/TaskRunner/automatic_verifier.py)
- A_02_MANAGERS.TaskRunner.execution_result (file: A_02_MANAGERS/TaskRunner/ExecutionAdapters/base_adapter.py)
- A_02_MANAGERS.TaskRunner.execution_result (file: A_02_MANAGERS/TaskRunner/ExecutionAdapters/powershell_adapter.py)
- A_02_MANAGERS.TaskRunner.execution_result (file: A_02_MANAGERS/TaskRunner/ExecutionAdapters/python_adapter.py)
- A_02_MANAGERS.TaskRunner.execution_result (file: A_02_MANAGERS/TaskRunner/recipe_executor.py)
- A_02_MANAGERS.TaskRunner.executor_factory (file: A_02_MANAGERS/TaskRunner/recipe_executor.py)
- A_02_MANAGERS.TaskRunner.recipe_builder (file: A_02_MANAGERS/Planner/task_planner.py)
- A_02_MANAGERS.TaskRunner.recipe_builder (file: A_02_MANAGERS/TaskRunner/recipe_writer.py)
- A_02_MANAGERS.TaskRunner.recipe_executor (file: 358)
- ... and 25 more

### LINKS:
- {"metadata": {"alias": null, "kind": "from", "line": 11, "name": "ExecutionHistory"}, "source": 294, "target": "A_02_MANAGERS.ExecutionMonitor.execution_history", "type": "import"} (file: None)
- {"metadata": {"alias": null, "kind": "from", "line": 11, "name": "ExecutionResult"}, "source": 339, "target": "A_02_MANAGERS.TaskRunner.execution_result", "type": "import"} (file: None)
- {"metadata": {"alias": null, "kind": "from", "line": 11, "name": "PolicyLoader"}, "source": 297, "target": "A_02_MANAGERS.ExecutionPolicyEngine.policy_loader", "type": "import"} (file: None)
- {"metadata": {"alias": null, "kind": "from", "line": 11, "name": "PolicyLoader"}, "source": 298, "target": "A_02_MANAGERS.ExecutionPolicyEngine.policy_loader", "type": "import"} (file: None)
- {"metadata": {"alias": null, "kind": "from", "line": 11, "name": "PythonExecutionAdapter"}, "source": 346, "target": "A_02_MANAGERS.TaskRunner.ExecutionAdapters.python_adapter", "type": "import"} (file: None)
- {"metadata": {"alias": null, "kind": "from", "line": 12, "name": "ExecutionResult"}, "source": 343, "target": "A_02_MANAGERS.TaskRunner.execution_result", "type": "import"} (file: None)
- {"metadata": {"alias": null, "kind": "from", "line": 12, "name": "ExecutionResult"}, "source": 344, "target": "A_02_MANAGERS.TaskRunner.execution_result", "type": "import"} (file: None)
- {"metadata": {"alias": null, "kind": "from", "line": 12, "name": "RecipeWriter"}, "source": 305, "target": "A_02_MANAGERS.TaskRunner.recipe_writer", "type": "import"} (file: None)
- {"metadata": {"alias": null, "kind": "from", "line": 13, "name": "BaseExecutionAdapter"}, "source": 343, "target": "A_02_MANAGERS.TaskRunner.ExecutionAdapters.base_adapter", "type": "import"} (file: None)
- {"metadata": {"alias": null, "kind": "from", "line": 13, "name": "BaseExecutionAdapter"}, "source": 344, "target": "A_02_MANAGERS.TaskRunner.ExecutionAdapters.base_adapter", "type": "import"} (file: None)
- {"metadata": {"alias": null, "kind": "from", "line": 13, "name": "Recipe"}, "source": 348, "target": "A_07_CONFIG.recipe_schema", "type": "import"} (file: None)
- {"metadata": {"alias": null, "kind": "from", "line": 13, "name": "RecipeStep"}, "source": 348, "target": "A_07_CONFIG.recipe_schema", "type": "import"} (file: None)
- {"metadata": {"alias": null, "kind": "from", "line": 13, "name": "run_once"}, "source": 305, "target": "A_02_MANAGERS.TaskRunner.runner_once", "type": "import"} (file: None)
- {"metadata": {"alias": null, "kind": "from", "line": 14, "name": "ExecutionResult"}, "source": 348, "target": "A_02_MANAGERS.TaskRunner.execution_result", "type": "import"} (file: None)
- {"metadata": {"alias": null, "kind": "from", "line": 14, "name": "ExecutionState"}, "source": 295, "target": "A_02_MANAGERS.ExecutionMonitor.execution_state", "type": "import"} (file: None)
- {"metadata": {"alias": null, "kind": "from", "line": 14, "name": "PowerShellExecutionAdapter"}, "source": 346, "target": "A_02_MANAGERS.TaskRunner.ExecutionAdapters.powershell_adapter", "type": "import"} (file: None)
- {"metadata": {"alias": null, "kind": "from", "line": 14, "name": "RecipeBuilder"}, "source": 309, "target": "A_02_MANAGERS.TaskRunner.recipe_builder", "type": "import"} (file: None)
- {"metadata": {"alias": null, "kind": "from", "line": 14, "name": "RecipeQueueWatcher"}, "source": 358, "target": "A_02_MANAGERS.TaskRunner.recipe_queue_watcher", "type": "import"} (file: None)
- {"metadata": {"alias": null, "kind": "from", "line": 15, "name": "ExecutorFactory"}, "source": 348, "target": "A_02_MANAGERS.TaskRunner.executor_factory", "type": "import"} (file: None)
- {"metadata": {"alias": null, "kind": "from", "line": 15, "name": "Recipe"}, "source": 347, "target": "A_07_CONFIG.recipe_schema", "type": "import"} (file: None)
- ... and 106 more

---

## CAPABILITY: QUEUE
**TOTAL EVIDENCE:** 355
**STATUS:** READY
**MAIN ENTRY:** Recipe

### FILES (canonical):
- A_07_CONFIG/execution_context_schema.py
- A_07_CONFIG/execution_policy_schema.py
- A_07_CONFIG/recipe_schema.py
- A_07_MEMORY/agent_loop_executor.py
- A_07_MEMORY/agent_runtime_v2.py
- A_07_MEMORY/execution_registry.py
- A_07_MEMORY/png_workflow_memory.py
- Butler_Gate.py
- INIT_OMEGA.py
- RUN_PIPELINE.py
- RUN_PIPELINE_V12.py
- A_01_CORE/execution_loop.py
- A_01_CORE/task_feeder.py
- A_02_MANAGERS/ArchitectAgent/planner_pipeline.py
- A_02_MANAGERS/ArchitectAgent/queue_manager.py
- A_02_MANAGERS/ArchitectAgent/recipe_builder.py
- A_02_MANAGERS/ArchitectAgent/recipe_generator.py
- A_02_MANAGERS/ArchitectAgent/task_contract_builder.py
- A_02_MANAGERS/ExecutionMonitor/execution_history.py
- A_02_MANAGERS/ExecutionMonitor/execution_monitor.py
- A_02_MANAGERS/ExecutionMonitor/execution_state.py
- A_02_MANAGERS/Planner/task_planner.py
- A_02_MANAGERS/queue_manager.py
- A_02_MANAGERS/recipe_generator.py
- A_02_MANAGERS/recipe_validator.py
- A_02_MANAGERS/TaskRunner/execution_result.py
- A_02_MANAGERS/TaskRunner/ExecutionAdapters/base_adapter.py
- A_02_MANAGERS/TaskRunner/ExecutionAdapters/powershell_adapter.py
- A_02_MANAGERS/TaskRunner/ExecutionAdapters/python_adapter.py
- A_02_MANAGERS/TaskRunner/executor_factory.py
- A_02_MANAGERS/TaskRunner/recipe_builder.py
- A_02_MANAGERS/TaskRunner/recipe_executor.py
- A_02_MANAGERS/TaskRunner/recipe_loader.py
- A_02_MANAGERS/TaskRunner/recipe_queue_watcher.py
- A_02_MANAGERS/TaskRunner/recipe_writer.py
- A_02_MANAGERS/TaskRunner/runner.py
- A_03_EXECUTORS/executor.py
- A_03_HANDLERS/pdf_ocr_pipeline.py
- A_03_ORCHESTRATION/butler_harness.py
- A_03_ORCHESTRATION/session_queue.py
- A_04_AGENTS/ProjectDocumentationDepartment/Core/Discovery/execution_registry_discovery_agent.py
- A_04_AGENTS/ProjectDocumentationDepartment/Core/engineering_pipeline.py
- A_04_AGENTS/ProjectDocumentationDepartment/Core/Scanners/execution_scanner.py

### CLASSES:
- AgentLoopExecutor (file: A_07_MEMORY/agent_loop_executor.py)
- BaseExecutionAdapter (file: A_02_MANAGERS/TaskRunner/ExecutionAdapters/base_adapter.py)
- EngineeringPipeline (file: A_04_AGENTS/ProjectDocumentationDepartment/Core/engineering_pipeline.py)
- ExecutionContext (file: A_07_CONFIG/execution_context_schema.py)
- ExecutionHistory (file: A_02_MANAGERS/ExecutionMonitor/execution_history.py)
- ExecutionLoop (file: A_01_CORE/execution_loop.py)
- ExecutionMemoryV2 (file: A_07_MEMORY/agent_runtime_v2.py)
- ExecutionMonitor (file: A_02_MANAGERS/ExecutionMonitor/execution_monitor.py)
- ExecutionPolicy (file: A_07_CONFIG/execution_policy_schema.py)
- ExecutionRegistry (file: A_07_MEMORY/execution_registry.py)
- ExecutionRegistryDiscoveryAgent (file: A_04_AGENTS/ProjectDocumentationDepartment/Core/Discovery/execution_registry_discovery_agent.py)
- ExecutionResult (file: A_02_MANAGERS/TaskRunner/execution_result.py)
- ExecutionScanner (file: A_04_AGENTS/ProjectDocumentationDepartment/Core/Scanners/execution_scanner.py)
- ExecutionState (file: A_02_MANAGERS/ExecutionMonitor/execution_state.py)
- Executor (file: A_03_EXECUTORS/executor.py)
- ExecutorFactory (file: A_02_MANAGERS/TaskRunner/executor_factory.py)
- PDFOCRPipeline (file: A_03_HANDLERS/pdf_ocr_pipeline.py)
- PNGWorkflowMemory (file: A_07_MEMORY/png_workflow_memory.py)
- PlannerPipeline (file: A_02_MANAGERS/ArchitectAgent/planner_pipeline.py)
- PowerShellExecutionAdapter (file: A_02_MANAGERS/TaskRunner/ExecutionAdapters/powershell_adapter.py)
- PythonExecutionAdapter (file: A_02_MANAGERS/TaskRunner/ExecutionAdapters/python_adapter.py)
- QueueManager (file: A_02_MANAGERS/ArchitectAgent/queue_manager.py)
- QueueManager (file: A_02_MANAGERS/queue_manager.py)
- Recipe (file: A_07_CONFIG/recipe_schema.py)
- RecipeBuilder (file: A_02_MANAGERS/ArchitectAgent/recipe_builder.py)
- RecipeBuilder (file: A_02_MANAGERS/TaskRunner/recipe_builder.py)
- RecipeExecutor (file: A_02_MANAGERS/TaskRunner/recipe_executor.py)
- RecipeGenerator (file: A_02_MANAGERS/ArchitectAgent/recipe_generator.py)
- RecipeGenerator (file: A_02_MANAGERS/recipe_generator.py)
- RecipeLoader (file: A_02_MANAGERS/TaskRunner/recipe_loader.py)
- RecipeQueueWatcher (file: A_02_MANAGERS/TaskRunner/recipe_queue_watcher.py)
- RecipeStep (file: A_07_CONFIG/recipe_schema.py)
- RecipeValidator (file: A_02_MANAGERS/recipe_validator.py)
- RecipeWriter (file: A_02_MANAGERS/TaskRunner/recipe_writer.py)
- SessionQueue (file: A_03_ORCHESTRATION/session_queue.py)
- TaskContractBuilder (file: A_02_MANAGERS/ArchitectAgent/task_contract_builder.py)
- TaskFeeder (file: A_01_CORE/task_feeder.py)
- TaskPlanner (file: A_02_MANAGERS/Planner/task_planner.py)
- TaskRunner (file: A_02_MANAGERS/TaskRunner/runner.py)

### FUNCTIONS:
- register_test_job (file: INIT_OMEGA.py)
- run_guarded_task (file: Butler_Gate.py)
- run_pipeline (file: RUN_PIPELINE.py)
- run_pipeline (file: RUN_PIPELINE_V12.py)
- sample_executor (file: A_03_ORCHESTRATION/butler_harness.py)

### CALLS:
- EngineeringPipeline (file: 611)
- ExecutionContext (file: A_07_CONFIG/execution_context_schema.py)
- ExecutionLoop (file: 1495)
- ExecutionLoop (file: 1505)
- ExecutionLoop (file: A_01_CORE/execution_loop.py)
- ExecutionMemoryV2 (file: A_07_MEMORY/agent_runtime_v2.py)
- ExecutionMonitor (file: A_02_MANAGERS/ExecutionMonitor/execution_monitor.py)
- ExecutionPolicy (file: A_07_CONFIG/execution_policy_schema.py)
- ExecutionPolicy (file: 296)
- ExecutionRegistry (file: 1117)
- ExecutionResult (file: 339)
- ExecutionResult (file: A_02_MANAGERS/TaskRunner/execution_result.py)
- ExecutionResult (file: A_02_MANAGERS/TaskRunner/ExecutionAdapters/powershell_adapter.py)
- ExecutionResult (file: A_02_MANAGERS/TaskRunner/ExecutionAdapters/python_adapter.py)
- ExecutionResult (file: A_02_MANAGERS/TaskRunner/recipe_executor.py)
- ExecutionScanner (file: A_04_AGENTS/ProjectDocumentationDepartment/Core/engineering_pipeline.py)
- ExecutionScanner (file: 591)
- Executor (file: A_03_EXECUTORS/executor.py)
- PDFOCRPipeline (file: 1349)
- PNGWorkflowMemory (file: 1351)
- ... and 50 more

### DEPENDENCY_NODES:
- A_02_MANAGERS.ExecutionMonitor.execution_history (file: None)
- A_02_MANAGERS.ExecutionMonitor.execution_state (file: None)
- A_02_MANAGERS.ExecutionMonitor.system_state (file: None)
- A_02_MANAGERS.ExecutionPolicyEngine.policy_loader (file: None)
- A_02_MANAGERS.TaskRunner.ExecutionAdapters.base_adapter (file: None)
- A_02_MANAGERS.TaskRunner.ExecutionAdapters.powershell_adapter (file: None)
- A_02_MANAGERS.TaskRunner.ExecutionAdapters.python_adapter (file: None)
- A_02_MANAGERS.TaskRunner.automatic_verifier (file: None)
- A_02_MANAGERS.TaskRunner.execution_result (file: None)
- A_02_MANAGERS.TaskRunner.executor_factory (file: None)
- A_02_MANAGERS.TaskRunner.recipe_builder (file: None)
- A_02_MANAGERS.TaskRunner.recipe_executor (file: None)
- A_02_MANAGERS.TaskRunner.recipe_loader (file: None)
- A_02_MANAGERS.TaskRunner.recipe_queue_watcher (file: None)
- A_02_MANAGERS.TaskRunner.recipe_writer (file: None)
- A_02_MANAGERS.TaskRunner.runner_once (file: None)
- A_02_MANAGERS.recipe_generator (file: None)
- A_02_MANAGERS.recipe_validator (file: None)
- A_07_CONFIG.recipe_schema (file: None)
- EngineeringPipeline (file: None)
- ... and 33 more

### EXECUTION_FACTS:
- PHASE_1_INIT::BOOTSTRAP: DONE
- PHASE_1_MULTITASK_TEST::TEST_TASK_A: DONE
- PHASE_1_MULTITASK_TEST::TEST_TASK_B: DONE
- PHASE_1_MULTITASK_TEST::TEST_TASK_C: DONE
- PHASE_1_TEST_DIAGNOSTICS::AUDIT_VERIFY_HEALTH: DONE
- PHASE_3_CLEANUP_AND_BACKUP::RUN_CORE_BACKUP: DONE
- TEST_PHASE_1::PHASE_1_TASK_A: DONE
- TEST_PHASE_1::PHASE_1_TASK_B: DONE
- TEST_PHASE_2::PHASE_2_TASK_C: DONE
- TEST_PHASE_2::PHASE_2_TASK_D: DONE

### GOALS_FACTS:
- active_goal: BUTLER_RECIPE_LIBRARY
- current_phase: ROADMAP_6_PHASE_4_RECIPES
- subgoal: ROADMAP_6_PHASE_4_RECIPES status=COMPLETED
- task: task_run_full_audit status=COMPLETED
- task: task_verify_contour status=COMPLETED
- weight: autonomy=0.6
- weight: stability=1.0

### IMPORTS:
- A_02_MANAGERS.ExecutionMonitor.execution_history (file: A_02_MANAGERS/ExecutionMonitor/execution_state.py)
- A_02_MANAGERS.ExecutionMonitor.execution_state (file: 295)
- A_02_MANAGERS.ExecutionMonitor.system_state (file: 305)
- A_02_MANAGERS.ExecutionPolicyEngine.policy_loader (file: A_07_CONFIG/execution_context_schema.py)
- A_02_MANAGERS.ExecutionPolicyEngine.policy_loader (file: 297)
- A_02_MANAGERS.ExecutionPolicyEngine.policy_loader (file: 298)
- A_02_MANAGERS.TaskRunner.ExecutionAdapters.base_adapter (file: A_02_MANAGERS/TaskRunner/ExecutionAdapters/powershell_adapter.py)
- A_02_MANAGERS.TaskRunner.ExecutionAdapters.base_adapter (file: A_02_MANAGERS/TaskRunner/ExecutionAdapters/python_adapter.py)
- A_02_MANAGERS.TaskRunner.ExecutionAdapters.powershell_adapter (file: A_02_MANAGERS/TaskRunner/executor_factory.py)
- A_02_MANAGERS.TaskRunner.ExecutionAdapters.python_adapter (file: A_02_MANAGERS/TaskRunner/executor_factory.py)
- A_02_MANAGERS.TaskRunner.automatic_verifier (file: 358)
- A_02_MANAGERS.TaskRunner.execution_result (file: 339)
- A_02_MANAGERS.TaskRunner.execution_result (file: A_02_MANAGERS/TaskRunner/ExecutionAdapters/base_adapter.py)
- A_02_MANAGERS.TaskRunner.execution_result (file: A_02_MANAGERS/TaskRunner/ExecutionAdapters/powershell_adapter.py)
- A_02_MANAGERS.TaskRunner.execution_result (file: A_02_MANAGERS/TaskRunner/ExecutionAdapters/python_adapter.py)
- A_02_MANAGERS.TaskRunner.execution_result (file: A_02_MANAGERS/TaskRunner/recipe_executor.py)
- A_02_MANAGERS.TaskRunner.executor_factory (file: A_02_MANAGERS/TaskRunner/recipe_executor.py)
- A_02_MANAGERS.TaskRunner.recipe_builder (file: A_02_MANAGERS/Planner/task_planner.py)
- A_02_MANAGERS.TaskRunner.recipe_builder (file: A_02_MANAGERS/TaskRunner/recipe_writer.py)
- A_02_MANAGERS.TaskRunner.recipe_executor (file: 358)
- ... and 25 more

### LINKS:
- {"metadata": {"alias": null, "kind": "from", "line": 11, "name": "ExecutionHistory"}, "source": 294, "target": "A_02_MANAGERS.ExecutionMonitor.execution_history", "type": "import"} (file: None)
- {"metadata": {"alias": null, "kind": "from", "line": 11, "name": "ExecutionResult"}, "source": 339, "target": "A_02_MANAGERS.TaskRunner.execution_result", "type": "import"} (file: None)
- {"metadata": {"alias": null, "kind": "from", "line": 11, "name": "PolicyLoader"}, "source": 297, "target": "A_02_MANAGERS.ExecutionPolicyEngine.policy_loader", "type": "import"} (file: None)
- {"metadata": {"alias": null, "kind": "from", "line": 11, "name": "PolicyLoader"}, "source": 298, "target": "A_02_MANAGERS.ExecutionPolicyEngine.policy_loader", "type": "import"} (file: None)
- {"metadata": {"alias": null, "kind": "from", "line": 11, "name": "PythonExecutionAdapter"}, "source": 346, "target": "A_02_MANAGERS.TaskRunner.ExecutionAdapters.python_adapter", "type": "import"} (file: None)
- {"metadata": {"alias": null, "kind": "from", "line": 12, "name": "ExecutionResult"}, "source": 343, "target": "A_02_MANAGERS.TaskRunner.execution_result", "type": "import"} (file: None)
- {"metadata": {"alias": null, "kind": "from", "line": 12, "name": "ExecutionResult"}, "source": 344, "target": "A_02_MANAGERS.TaskRunner.execution_result", "type": "import"} (file: None)
- {"metadata": {"alias": null, "kind": "from", "line": 12, "name": "RecipeWriter"}, "source": 305, "target": "A_02_MANAGERS.TaskRunner.recipe_writer", "type": "import"} (file: None)
- {"metadata": {"alias": null, "kind": "from", "line": 13, "name": "BaseExecutionAdapter"}, "source": 343, "target": "A_02_MANAGERS.TaskRunner.ExecutionAdapters.base_adapter", "type": "import"} (file: None)
- {"metadata": {"alias": null, "kind": "from", "line": 13, "name": "BaseExecutionAdapter"}, "source": 344, "target": "A_02_MANAGERS.TaskRunner.ExecutionAdapters.base_adapter", "type": "import"} (file: None)
- {"metadata": {"alias": null, "kind": "from", "line": 13, "name": "Recipe"}, "source": 348, "target": "A_07_CONFIG.recipe_schema", "type": "import"} (file: None)
- {"metadata": {"alias": null, "kind": "from", "line": 13, "name": "RecipeStep"}, "source": 348, "target": "A_07_CONFIG.recipe_schema", "type": "import"} (file: None)
- {"metadata": {"alias": null, "kind": "from", "line": 13, "name": "run_once"}, "source": 305, "target": "A_02_MANAGERS.TaskRunner.runner_once", "type": "import"} (file: None)
- {"metadata": {"alias": null, "kind": "from", "line": 14, "name": "ExecutionResult"}, "source": 348, "target": "A_02_MANAGERS.TaskRunner.execution_result", "type": "import"} (file: None)
- {"metadata": {"alias": null, "kind": "from", "line": 14, "name": "ExecutionState"}, "source": 295, "target": "A_02_MANAGERS.ExecutionMonitor.execution_state", "type": "import"} (file: None)
- {"metadata": {"alias": null, "kind": "from", "line": 14, "name": "PowerShellExecutionAdapter"}, "source": 346, "target": "A_02_MANAGERS.TaskRunner.ExecutionAdapters.powershell_adapter", "type": "import"} (file: None)
- {"metadata": {"alias": null, "kind": "from", "line": 14, "name": "RecipeBuilder"}, "source": 309, "target": "A_02_MANAGERS.TaskRunner.recipe_builder", "type": "import"} (file: None)
- {"metadata": {"alias": null, "kind": "from", "line": 14, "name": "RecipeQueueWatcher"}, "source": 358, "target": "A_02_MANAGERS.TaskRunner.recipe_queue_watcher", "type": "import"} (file: None)
- {"metadata": {"alias": null, "kind": "from", "line": 15, "name": "ExecutorFactory"}, "source": 348, "target": "A_02_MANAGERS.TaskRunner.executor_factory", "type": "import"} (file: None)
- {"metadata": {"alias": null, "kind": "from", "line": 15, "name": "Recipe"}, "source": 347, "target": "A_07_CONFIG.recipe_schema", "type": "import"} (file: None)
- ... and 106 more

---

## CAPABILITY: WATCHER
**TOTAL EVIDENCE:** 25
**STATUS:** READY
**MAIN ENTRY:** RecipeQueueWatcher

### FILES (canonical):
- A_02_MANAGERS/TaskRunner/recipe_queue_watcher.py

### CLASSES:
- RecipeQueueWatcher (file: A_02_MANAGERS/TaskRunner/recipe_queue_watcher.py)

### FUNCTIONS:

### CALLS:
- RecipeQueueWatcher (file: A_02_MANAGERS/TaskRunner/recipe_queue_watcher.py)
- RecipeQueueWatcher (file: 357)
- RecipeQueueWatcher (file: 358)

### DEPENDENCY_NODES:
- RecipeQueueWatcher (file: None)

### EXECUTION_FACTS:
- PHASE_1_INIT::BOOTSTRAP: DONE
- PHASE_1_MULTITASK_TEST::TEST_TASK_A: DONE
- PHASE_1_MULTITASK_TEST::TEST_TASK_B: DONE
- PHASE_1_MULTITASK_TEST::TEST_TASK_C: DONE
- PHASE_1_TEST_DIAGNOSTICS::AUDIT_VERIFY_HEALTH: DONE
- PHASE_3_CLEANUP_AND_BACKUP::RUN_CORE_BACKUP: DONE
- TEST_PHASE_1::PHASE_1_TASK_A: DONE
- TEST_PHASE_1::PHASE_1_TASK_B: DONE
- TEST_PHASE_2::PHASE_2_TASK_C: DONE
- TEST_PHASE_2::PHASE_2_TASK_D: DONE

### GOALS_FACTS:
- active_goal: BUTLER_RECIPE_LIBRARY
- current_phase: ROADMAP_6_PHASE_4_RECIPES
- subgoal: ROADMAP_6_PHASE_4_RECIPES status=COMPLETED
- task: task_run_full_audit status=COMPLETED
- task: task_verify_contour status=COMPLETED
- weight: autonomy=0.6
- weight: stability=1.0

### LINKS:
- {"metadata": {"context": "run", "line": 21}, "source": 357, "target": "RecipeQueueWatcher", "type": "call"} (file: None)
- {"metadata": {"context": "run_once", "line": 25}, "source": 358, "target": "RecipeQueueWatcher", "type": "call"} (file: None)
- {"metadata": {"context": null, "line": 39}, "source": 350, "target": "RecipeQueueWatcher", "type": "call"} (file: None)

---

## CAPABILITY: REGISTRY
**TOTAL EVIDENCE:** 85
**STATUS:** READY
**MAIN ENTRY:** RouterRegistry

### FILES (canonical):
- A_07_CONFIG/registry_loader.py
- A_07_CONFIG/registry_validator.py
- A_07_MEMORY/execution_registry.py
- FIX_QUEUE.py
- INIT_OMEGA.py
- A_02_MANAGERS/ExecutionPolicyEngine/policy_registry.py
- A_02_MANAGERS/RuntimeCapabilityRegistry/runtime_registry.py
- A_03_HANDLERS/registry.py
- A_03_ORCHESTRATION/registry_brain.py
- A_03_ORCHESTRATION/router_registry.py
- A_04_AGENTS/ProjectDocumentationDepartment/Core/Discovery/execution_registry_discovery_agent.py
- A_04_AGENTS/ProjectDocumentationDepartment/Core/Discovery/goals_registry_discovery_agent.py
- A_04_AGENTS/ProjectDocumentationDepartment/Core/Discovery/registry_discovery_agent.py
- A_04_AGENTS/ProjectDocumentationDepartment/Core/Discovery/registry_reader_agent.py
- A_04_AGENTS/ProjectDocumentationDepartment/Core/Scanners/registry_scanner.py

### CLASSES:
- ExecutionRegistry (file: A_07_MEMORY/execution_registry.py)
- ExecutionRegistryDiscoveryAgent (file: A_04_AGENTS/ProjectDocumentationDepartment/Core/Discovery/execution_registry_discovery_agent.py)
- GoalsRegistryDiscoveryAgent (file: A_04_AGENTS/ProjectDocumentationDepartment/Core/Discovery/goals_registry_discovery_agent.py)
- HandlerRegistry (file: A_03_HANDLERS/registry.py)
- PolicyRegistry (file: A_02_MANAGERS/ExecutionPolicyEngine/policy_registry.py)
- RegistryBrain (file: A_03_ORCHESTRATION/registry_brain.py)
- RegistryDiscoveryAgent (file: A_04_AGENTS/ProjectDocumentationDepartment/Core/Discovery/registry_discovery_agent.py)
- RegistryLoader (file: A_07_CONFIG/registry_loader.py)
- RegistryReaderAgent (file: A_04_AGENTS/ProjectDocumentationDepartment/Core/Discovery/registry_reader_agent.py)
- RegistryScanner (file: A_04_AGENTS/ProjectDocumentationDepartment/Core/Scanners/registry_scanner.py)
- RegistryValidator (file: A_07_CONFIG/registry_validator.py)
- RouterRegistry (file: A_03_ORCHESTRATION/router_registry.py)
- RuntimeCapabilityRegistry (file: A_02_MANAGERS/RuntimeCapabilityRegistry/runtime_registry.py)

### FUNCTIONS:
- register_test_job (file: INIT_OMEGA.py)
- reset_and_register (file: FIX_QUEUE.py)

### CALLS:
- ExecutionRegistry (file: 1117)
- HandlerRegistry (file: A_03_HANDLERS/registry.py)
- RegistryBrain (file: 1495)
- RegistryBrain (file: 1505)
- RegistryBrain (file: A_03_ORCHESTRATION/registry_brain.py)
- RegistryLoader (file: 1102)
- RegistryLoader (file: 1103)
- RegistryLoader (file: A_07_CONFIG/registry_loader.py)
- RegistryScanner (file: 536)
- RegistryScanner (file: 591)
- RegistryValidator (file: A_07_CONFIG/registry_validator.py)
- RouterRegistry (file: 123)
- RouterRegistry (file: 467)
- RouterRegistry (file: 468)
- RouterRegistry (file: 469)
- RouterRegistry (file: A_03_ORCHESTRATION/router_registry.py)
- RouterRegistry (file: 477)
- register_test_job (file: INIT_OMEGA.py)
- reset_and_register (file: FIX_QUEUE.py)

### DEPENDENCY_NODES:
- A_02_MANAGERS.RuntimeCapabilityRegistry.capability_schema (file: None)
- A_02_MANAGERS.RuntimeCapabilityRegistry.runtime_registry (file: None)
- ExecutionRegistry (file: None)
- HandlerRegistry (file: None)
- RegistryBrain (file: None)
- RegistryLoader (file: None)
- RegistryScanner (file: None)
- RegistryValidator (file: None)
- RouterRegistry (file: None)
- register_test_job (file: None)
- reset_and_register (file: None)

### EXECUTION_FACTS:
- PHASE_1_INIT::BOOTSTRAP: DONE
- PHASE_1_MULTITASK_TEST::TEST_TASK_A: DONE
- PHASE_1_MULTITASK_TEST::TEST_TASK_B: DONE
- PHASE_1_MULTITASK_TEST::TEST_TASK_C: DONE
- PHASE_1_TEST_DIAGNOSTICS::AUDIT_VERIFY_HEALTH: DONE
- PHASE_3_CLEANUP_AND_BACKUP::RUN_CORE_BACKUP: DONE
- TEST_PHASE_1::PHASE_1_TASK_A: DONE
- TEST_PHASE_1::PHASE_1_TASK_B: DONE
- TEST_PHASE_2::PHASE_2_TASK_C: DONE
- TEST_PHASE_2::PHASE_2_TASK_D: DONE

### GOALS_FACTS:
- active_goal: BUTLER_RECIPE_LIBRARY
- current_phase: ROADMAP_6_PHASE_4_RECIPES
- subgoal: ROADMAP_6_PHASE_4_RECIPES status=COMPLETED
- task: task_run_full_audit status=COMPLETED
- task: task_verify_contour status=COMPLETED
- weight: autonomy=0.6
- weight: stability=1.0

### IMPORTS:
- A_02_MANAGERS.RuntimeCapabilityRegistry.capability_schema (file: A_02_MANAGERS/RuntimeCapabilityRegistry/runtime_registry.py)
- A_02_MANAGERS.RuntimeCapabilityRegistry.runtime_registry (file: 1081)

### LINKS:
- {"metadata": {"alias": null, "kind": "from", "line": 15, "name": "RuntimeCapabilityRegistry"}, "source": 1081, "target": "A_02_MANAGERS.RuntimeCapabilityRegistry.runtime_registry", "type": "import"} (file: None)
- {"metadata": {"alias": null, "kind": "from", "line": 9, "name": "RuntimeCapability"}, "source": 320, "target": "A_02_MANAGERS.RuntimeCapabilityRegistry.capability_schema", "type": "import"} (file: None)
- {"metadata": {"context": "BootstrapCore.__init__", "line": 16}, "source": 1495, "target": "RegistryBrain", "type": "call"} (file: None)
- {"metadata": {"context": "ButlerSystem.__init__", "line": 15}, "source": 1505, "target": "RegistryBrain", "type": "call"} (file: None)
- {"metadata": {"context": "EngineeringPipeline.collect", "line": 56}, "source": 536, "target": "RegistryScanner", "type": "call"} (file: None)
- {"metadata": {"context": "EngineeringPipeline.collect", "line": 56}, "source": 591, "target": "RegistryScanner", "type": "call"} (file: None)
- {"metadata": {"context": "LoopOrchestratorV3_MASTER_TRUTH.__init__", "line": 48}, "source": 1117, "target": "ExecutionRegistry", "type": "call"} (file: None)
- {"metadata": {"context": "ProjectState.__init__", "line": 11}, "source": 1102, "target": "RegistryLoader", "type": "call"} (file: None)
- {"metadata": {"context": "ProjectState.__init__", "line": 11}, "source": 1103, "target": "RegistryLoader", "type": "call"} (file: None)
- {"metadata": {"context": "RouterIntegration.__init__", "line": 22}, "source": 123, "target": "RouterRegistry", "type": "call"} (file: None)
- {"metadata": {"context": "RouterIntegration.__init__", "line": 22}, "source": 467, "target": "RouterRegistry", "type": "call"} (file: None)
- {"metadata": {"context": "RouterIntegration.__init__", "line": 25}, "source": 468, "target": "RouterRegistry", "type": "call"} (file: None)
- {"metadata": {"context": "Worker.__init__", "line": 35}, "source": 477, "target": "RouterRegistry", "type": "call"} (file: None)
- {"metadata": {"context": null, "line": 23}, "source": 469, "target": "RouterRegistry", "type": "call"} (file: None)
- {"metadata": {"context": null, "line": 23}, "source": 470, "target": "RouterRegistry", "type": "call"} (file: None)
- {"metadata": {"context": null, "line": 26}, "source": 1454, "target": "register_test_job", "type": "call"} (file: None)
- {"metadata": {"context": null, "line": 34}, "source": 1106, "target": "RegistryLoader", "type": "call"} (file: None)
- {"metadata": {"context": null, "line": 37}, "source": 387, "target": "HandlerRegistry", "type": "call"} (file: None)
- {"metadata": {"context": null, "line": 38}, "source": 1441, "target": "reset_and_register", "type": "call"} (file: None)
- {"metadata": {"context": null, "line": 47}, "source": 1107, "target": "RegistryValidator", "type": "call"} (file: None)
- ... and 1 more

---

## CAPABILITY: DISPATCHER
**TOTAL EVIDENCE:** 194
**STATUS:** READY
**MAIN ENTRY:** dispatch

### FILES (canonical):
- A_09_GUARDIANS/BONE_CACHE/Dispatcher/Dispatcher_bone_20260626_182912.py
- A_09_GUARDIANS/BONE_CACHE/Dispatcher/Dispatcher_bone_20260626_214839.py
- A_10_BUTLER_OS/00_PRODUCTION/core/smart_router.py
- A_02_MANAGERS/dream_manager.py
- A_02_MANAGERS/smart_dispatcher.py
- A_02_MANAGERS/smart_dispatcher_v2.py
- A_02_MANAGERS/smart_dispatcher_v2.RECOVERY_TEMPLATE.py
- A_03_ORCHESTRATION/agent_router.py
- A_03_ORCHESTRATION/chat_router_mirror.py
- A_03_ORCHESTRATION/dispatcher_bridge.py
- A_03_ORCHESTRATION/dispatcher_bridge_v2.py
- A_03_ORCHESTRATION/dream_dispatcher_adapter.py
- A_03_ORCHESTRATION/router_integration.py
- A_03_ORCHESTRATION/router_registry.py
- A_04_AGENTS/professor.py
- A_04_AGENTS/ProjectDocumentationDepartment/Core/evidence_doctor.py

### CLASSES:
- AgentRouter (file: A_03_ORCHESTRATION/agent_router.py)
- ChatRouterMirror (file: A_03_ORCHESTRATION/chat_router_mirror.py)
- DispatcherAgent (file: A_04_AGENTS/professor.py)
- DispatcherBridge (file: A_03_ORCHESTRATION/dispatcher_bridge.py)
- DreamDispatcherAdapter (file: A_03_ORCHESTRATION/dream_dispatcher_adapter.py)
- FakeDispatcher (file: A_02_MANAGERS/dream_manager.py)
- RouterIntegration (file: A_03_ORCHESTRATION/router_integration.py)
- RouterRegistry (file: A_03_ORCHESTRATION/router_registry.py)
- SmartDispatcher (file: A_02_MANAGERS/smart_dispatcher.py)
- SmartDispatcherV2 (file: A_09_GUARDIANS/BONE_CACHE/Dispatcher/Dispatcher_bone_20260626_182912.py)
- SmartDispatcherV2 (file: A_09_GUARDIANS/BONE_CACHE/Dispatcher/Dispatcher_bone_20260626_214839.py)
- SmartDispatcherV2 (file: A_02_MANAGERS/smart_dispatcher_v2.py)
- SmartDispatcherV2 (file: A_02_MANAGERS/smart_dispatcher_v2.RECOVERY_TEMPLATE.py)
- SmartRouter (file: A_10_BUTLER_OS/00_PRODUCTION/core/smart_router.py)

### FUNCTIONS:
- dispatch (file: A_03_ORCHESTRATION/dispatcher_bridge_v2.py)
- dispatch (file: A_04_AGENTS/ProjectDocumentationDepartment/Core/evidence_doctor.py)

### CALLS:
- AgentRouter (file: 123)
- AgentRouter (file: 394)
- AgentRouter (file: A_03_ORCHESTRATION/agent_router.py)
- AgentRouter (file: 467)
- AgentRouter (file: A_03_ORCHESTRATION/router_integration.py)
- ChatRouterMirror (file: A_03_ORCHESTRATION/chat_router_mirror.py)
- Dispatcher (file: 365)
- DispatcherAgent (file: 116)
- DispatcherAgent (file: 241)
- DispatcherAgent (file: A_03_ORCHESTRATION/dream_dispatcher_adapter.py)
- DispatcherAgent (file: 465)
- DispatcherAgent (file: 480)
- DispatcherAgent (file: 615)
- DispatcherAgent (file: 631)
- DispatcherScanner (file: 549)
- DispatcherScanner (file: 597)
- FakeDispatcher (file: A_02_MANAGERS/dream_manager.py)
- RouterIntegration (file: 123)
- RouterIntegration (file: 1364)
- RouterIntegration (file: 1512)
- ... and 40 more

### DEPENDENCY_NODES:
- A_02_MANAGERS.smart_dispatcher (file: None)
- A_02_MANAGERS.smart_dispatcher_v2 (file: None)
- A_03_ORCHESTRATION.dispatcher_bridge_v2 (file: None)
- AgentRouter (file: None)
- ChatRouterMirror (file: None)
- Dispatcher (file: None)
- DispatcherAgent (file: None)
- DispatcherScanner (file: None)
- FakeDispatcher (file: None)
- RouterIntegration (file: None)
- RouterRegistry (file: None)
- SmartDispatcher (file: None)
- SmartDispatcherV2 (file: None)
- SmartRouter (file: None)
- _dispatch (file: None)
- dispatch (file: None)

### EXECUTION_FACTS:
- PHASE_1_INIT::BOOTSTRAP: DONE
- PHASE_1_MULTITASK_TEST::TEST_TASK_A: DONE
- PHASE_1_MULTITASK_TEST::TEST_TASK_B: DONE
- PHASE_1_MULTITASK_TEST::TEST_TASK_C: DONE
- PHASE_1_TEST_DIAGNOSTICS::AUDIT_VERIFY_HEALTH: DONE
- PHASE_3_CLEANUP_AND_BACKUP::RUN_CORE_BACKUP: DONE
- TEST_PHASE_1::PHASE_1_TASK_A: DONE
- TEST_PHASE_1::PHASE_1_TASK_B: DONE
- TEST_PHASE_2::PHASE_2_TASK_C: DONE
- TEST_PHASE_2::PHASE_2_TASK_D: DONE

### GOALS_FACTS:
- active_goal: BUTLER_RECIPE_LIBRARY
- current_phase: ROADMAP_6_PHASE_4_RECIPES
- subgoal: ROADMAP_6_PHASE_4_RECIPES status=COMPLETED
- task: task_run_full_audit status=COMPLETED
- task: task_verify_contour status=COMPLETED
- weight: autonomy=0.6
- weight: stability=1.0

### IMPORTS:
- A_02_MANAGERS.smart_dispatcher (file: 227)
- A_02_MANAGERS.smart_dispatcher_v2 (file: 1393)
- A_02_MANAGERS.smart_dispatcher_v2 (file: 1513)
- A_02_MANAGERS.smart_dispatcher_v2 (file: A_03_ORCHESTRATION/dispatcher_bridge_v2.py)
- A_02_MANAGERS.smart_dispatcher_v2 (file: 534)
- A_02_MANAGERS.smart_dispatcher_v2 (file: 549)
- A_02_MANAGERS.smart_dispatcher_v2 (file: 589)
- A_02_MANAGERS.smart_dispatcher_v2 (file: 597)
- A_03_ORCHESTRATION.dispatcher_bridge_v2 (file: 1363)
- A_03_ORCHESTRATION.dispatcher_bridge_v2 (file: 1394)
- A_03_ORCHESTRATION.dispatcher_bridge_v2 (file: 1423)
- A_03_ORCHESTRATION.dispatcher_bridge_v2 (file: 414)

### LINKS:
- {"metadata": {"alias": null, "kind": "from", "line": 10, "name": "SmartDispatcher"}, "source": 227, "target": "A_02_MANAGERS.smart_dispatcher", "type": "import"} (file: None)
- {"metadata": {"alias": null, "kind": "from", "line": 157, "name": "dispatch"}, "source": 414, "target": "A_03_ORCHESTRATION.dispatcher_bridge_v2", "type": "import"} (file: None)
- {"metadata": {"alias": null, "kind": "from", "line": 3, "name": "SmartDispatcherV2"}, "source": 1513, "target": "A_02_MANAGERS.smart_dispatcher_v2", "type": "import"} (file: None)
- {"metadata": {"alias": null, "kind": "from", "line": 3, "name": "SmartDispatcherV2"}, "source": 430, "target": "A_02_MANAGERS.smart_dispatcher_v2", "type": "import"} (file: None)
- {"metadata": {"alias": null, "kind": "from", "line": 3, "name": "dispatch"}, "source": 1363, "target": "A_03_ORCHESTRATION.dispatcher_bridge_v2", "type": "import"} (file: None)
- {"metadata": {"alias": null, "kind": "from", "line": 3, "name": "dispatch"}, "source": 1423, "target": "A_03_ORCHESTRATION.dispatcher_bridge_v2", "type": "import"} (file: None)
- {"metadata": {"alias": null, "kind": "from", "line": 7, "name": "SmartDispatcherV2"}, "source": 534, "target": "A_02_MANAGERS.smart_dispatcher_v2", "type": "import"} (file: None)
- {"metadata": {"alias": null, "kind": "from", "line": 7, "name": "SmartDispatcherV2"}, "source": 589, "target": "A_02_MANAGERS.smart_dispatcher_v2", "type": "import"} (file: None)
- {"metadata": {"alias": null, "kind": "from", "line": 8, "name": "SmartDispatcherV2"}, "source": 1393, "target": "A_02_MANAGERS.smart_dispatcher_v2", "type": "import"} (file: None)
- {"metadata": {"alias": null, "kind": "from", "line": 8, "name": "_dispatcher"}, "source": 1394, "target": "A_03_ORCHESTRATION.dispatcher_bridge_v2", "type": "import"} (file: None)
- {"metadata": {"alias": null, "kind": "from", "line": 9, "name": "SmartDispatcherV2"}, "source": 549, "target": "A_02_MANAGERS.smart_dispatcher_v2", "type": "import"} (file: None)
- {"metadata": {"alias": null, "kind": "from", "line": 9, "name": "SmartDispatcherV2"}, "source": 597, "target": "A_02_MANAGERS.smart_dispatcher_v2", "type": "import"} (file: None)
- {"metadata": {"args": [], "kind": "constructor", "line": 33}, "source": 365, "target": "Dispatcher", "type": "registration"} (file: None)
- {"metadata": {"context": "ButlerInteractiveChat.__init__", "line": 38}, "source": 241, "target": "DispatcherAgent", "type": "call"} (file: None)
- {"metadata": {"context": "DispatcherScanner.scan", "line": 18}, "source": 549, "target": "SmartDispatcherV2", "type": "call"} (file: None)
- {"metadata": {"context": "DispatcherScanner.scan", "line": 18}, "source": 597, "target": "SmartDispatcherV2", "type": "call"} (file: None)
- {"metadata": {"context": "DreamDispatcherAdapter.__init__", "line": 9}, "source": 432, "target": "DispatcherAgent", "type": "call"} (file: None)
- {"metadata": {"context": "FactoryCoreBridge.handle", "line": 26}, "source": 434, "target": "_dispatch", "type": "call"} (file: None)
- {"metadata": {"context": "ProfessorAdapter.__init__", "line": 9}, "source": 465, "target": "DispatcherAgent", "type": "call"} (file: None)
- {"metadata": {"context": "RouterIntegration.__init__", "line": 21}, "source": 123, "target": "AgentRouter", "type": "call"} (file: None)
- ... and 53 more

---

## CAPABILITY: GUARDIAN
**TOTAL EVIDENCE:** 56
**STATUS:** READY
**MAIN ENTRY:** RecipeQueueWatcher

### FILES (canonical):
- A_01_CORE/memory_guardian.py
- A_01_CORE/system_guardian.py
- A_02_MANAGERS/ExecutionMonitor/execution_monitor.py
- A_02_MANAGERS/TaskRunner/recipe_queue_watcher.py
- A_02_MANAGERS/TaskRunner/security_validator.py

### CLASSES:
- ExecutionMonitor (file: A_02_MANAGERS/ExecutionMonitor/execution_monitor.py)
- RecipeQueueWatcher (file: A_02_MANAGERS/TaskRunner/recipe_queue_watcher.py)
- SecurityValidator (file: A_02_MANAGERS/TaskRunner/security_validator.py)
- SecurityViolation (file: A_02_MANAGERS/TaskRunner/security_validator.py)

### FUNCTIONS:
- run_guardian (file: A_01_CORE/system_guardian.py)
- run_memory_guardian (file: A_01_CORE/memory_guardian.py)

### CALLS:
- ExecutionMonitor (file: A_02_MANAGERS/ExecutionMonitor/execution_monitor.py)
- RecipeQueueWatcher (file: A_02_MANAGERS/TaskRunner/recipe_queue_watcher.py)
- RecipeQueueWatcher (file: 357)
- RecipeQueueWatcher (file: 358)
- SecurityViolation (file: A_02_MANAGERS/TaskRunner/security_validator.py)
- run_guardian (file: A_01_CORE/system_guardian.py)
- run_memory_guardian (file: 1486)
- run_memory_guardian (file: A_01_CORE/memory_guardian.py)

### DEPENDENCY_NODES:
- A_02_MANAGERS.ExecutionMonitor.execution_history (file: None)
- A_02_MANAGERS.ExecutionMonitor.execution_state (file: None)
- A_02_MANAGERS.ExecutionMonitor.system_state (file: None)
- ExecutionMonitor (file: None)
- RecipeQueueWatcher (file: None)
- SecurityViolation (file: None)
- run_guardian (file: None)
- run_memory_guardian (file: None)

### EXECUTION_FACTS:
- PHASE_1_INIT::BOOTSTRAP: DONE
- PHASE_1_MULTITASK_TEST::TEST_TASK_A: DONE
- PHASE_1_MULTITASK_TEST::TEST_TASK_B: DONE
- PHASE_1_MULTITASK_TEST::TEST_TASK_C: DONE
- PHASE_1_TEST_DIAGNOSTICS::AUDIT_VERIFY_HEALTH: DONE
- PHASE_3_CLEANUP_AND_BACKUP::RUN_CORE_BACKUP: DONE
- TEST_PHASE_1::PHASE_1_TASK_A: DONE
- TEST_PHASE_1::PHASE_1_TASK_B: DONE
- TEST_PHASE_2::PHASE_2_TASK_C: DONE
- TEST_PHASE_2::PHASE_2_TASK_D: DONE

### GOALS_FACTS:
- active_goal: BUTLER_RECIPE_LIBRARY
- current_phase: ROADMAP_6_PHASE_4_RECIPES
- subgoal: ROADMAP_6_PHASE_4_RECIPES status=COMPLETED
- task: task_run_full_audit status=COMPLETED
- task: task_verify_contour status=COMPLETED
- weight: autonomy=0.6
- weight: stability=1.0

### IMPORTS:
- A_02_MANAGERS.ExecutionMonitor.execution_history (file: 294)
- A_02_MANAGERS.ExecutionMonitor.execution_state (file: 295)
- A_02_MANAGERS.ExecutionMonitor.system_state (file: 305)

### LINKS:
- {"metadata": {"alias": null, "kind": "from", "line": 11, "name": "ExecutionHistory"}, "source": 294, "target": "A_02_MANAGERS.ExecutionMonitor.execution_history", "type": "import"} (file: None)
- {"metadata": {"alias": null, "kind": "from", "line": 14, "name": "ExecutionState"}, "source": 295, "target": "A_02_MANAGERS.ExecutionMonitor.execution_state", "type": "import"} (file: None)
- {"metadata": {"alias": null, "kind": "from", "line": 9, "name": "SystemState"}, "source": 305, "target": "A_02_MANAGERS.ExecutionMonitor.system_state", "type": "import"} (file: None)
- {"metadata": {"context": "SecurityValidator.validate", "line": 41}, "source": 359, "target": "SecurityViolation", "type": "call"} (file: None)
- {"metadata": {"context": "SecurityValidator.validate", "line": 51}, "source": 359, "target": "SecurityViolation", "type": "call"} (file: None)
- {"metadata": {"context": "execute_repair", "line": 88}, "source": 1486, "target": "run_memory_guardian", "type": "call"} (file: None)
- {"metadata": {"context": "main", "line": 118}, "source": 1486, "target": "run_memory_guardian", "type": "call"} (file: None)
- {"metadata": {"context": "main", "line": 121}, "source": 1486, "target": "run_memory_guardian", "type": "call"} (file: None)
- {"metadata": {"context": "run", "line": 21}, "source": 357, "target": "RecipeQueueWatcher", "type": "call"} (file: None)
- {"metadata": {"context": "run_once", "line": 25}, "source": 358, "target": "RecipeQueueWatcher", "type": "call"} (file: None)
- {"metadata": {"context": null, "line": 144}, "source": 231, "target": "run_guardian", "type": "call"} (file: None)
- {"metadata": {"context": null, "line": 229}, "source": 219, "target": "run_memory_guardian", "type": "call"} (file: None)
- {"metadata": {"context": null, "line": 39}, "source": 293, "target": "ExecutionMonitor", "type": "call"} (file: None)
- {"metadata": {"context": null, "line": 39}, "source": 350, "target": "RecipeQueueWatcher", "type": "call"} (file: None)

---

## CAPABILITY: AUDIT
**TOTAL EVIDENCE:** 41
**STATUS:** READY
**MAIN ENTRY:** AuditScanner

### FILES (canonical):
- A_09_TESTS/test_project_auditor.py
- A_01_CORE/project_state_builder.py
- A_04_AGENTS/ProjectDocumentationDepartment/Core/Scanners/audit_scanner.py
- A_04_COMPONENTS/ProjectAuditor/project_auditor.py

### CLASSES:
- AuditScanner (file: A_04_AGENTS/ProjectDocumentationDepartment/Core/Scanners/audit_scanner.py)
- ProjectAuditor (file: A_04_COMPONENTS/ProjectAuditor/project_auditor.py)
- TestProjectAuditor (file: A_09_TESTS/test_project_auditor.py)

### FUNCTIONS:
- write_audit_log (file: A_01_CORE/project_state_builder.py)

### CALLS:
- AuditScanner (file: 536)
- AuditScanner (file: A_04_AGENTS/ProjectDocumentationDepartment/Core/Scanners/audit_scanner.py)
- AuditScanner (file: 591)
- AuditScanner (file: 596)
- ProjectAuditor (file: A_09_TESTS/test_project_auditor.py)
- write_audit_log (file: A_01_CORE/project_state_builder.py)

### DEPENDENCY_NODES:
- A_04_COMPONENTS.ProjectAuditor.project_auditor (file: None)
- AuditScanner (file: None)
- ProjectAuditor (file: None)
- write_audit_log (file: None)

### EXECUTION_FACTS:
- PHASE_1_INIT::BOOTSTRAP: DONE
- PHASE_1_MULTITASK_TEST::TEST_TASK_A: DONE
- PHASE_1_MULTITASK_TEST::TEST_TASK_B: DONE
- PHASE_1_MULTITASK_TEST::TEST_TASK_C: DONE
- PHASE_1_TEST_DIAGNOSTICS::AUDIT_VERIFY_HEALTH: DONE
- PHASE_3_CLEANUP_AND_BACKUP::RUN_CORE_BACKUP: DONE
- TEST_PHASE_1::PHASE_1_TASK_A: DONE
- TEST_PHASE_1::PHASE_1_TASK_B: DONE
- TEST_PHASE_2::PHASE_2_TASK_C: DONE
- TEST_PHASE_2::PHASE_2_TASK_D: DONE

### GOALS_FACTS:
- active_goal: BUTLER_RECIPE_LIBRARY
- current_phase: ROADMAP_6_PHASE_4_RECIPES
- subgoal: ROADMAP_6_PHASE_4_RECIPES status=COMPLETED
- task: task_run_full_audit status=COMPLETED
- task: task_verify_contour status=COMPLETED
- weight: autonomy=0.6
- weight: stability=1.0

### IMPORTS:
- A_04_COMPONENTS.ProjectAuditor.project_auditor (file: A_09_TESTS/test_project_auditor.py)

### LINKS:
- {"metadata": {"alias": null, "kind": "from", "line": 3, "name": "ProjectAuditor"}, "source": 1353, "target": "A_04_COMPONENTS.ProjectAuditor.project_auditor", "type": "import"} (file: None)
- {"metadata": {"context": "EngineeringPipeline.collect", "line": 62}, "source": 536, "target": "AuditScanner", "type": "call"} (file: None)
- {"metadata": {"context": "EngineeringPipeline.collect", "line": 62}, "source": 591, "target": "AuditScanner", "type": "call"} (file: None)
- {"metadata": {"context": "TestProjectAuditor.test_stub", "line": 8}, "source": 1353, "target": "ProjectAuditor", "type": "call"} (file: None)
- {"metadata": {"context": "build_state", "line": 231}, "source": 223, "target": "write_audit_log", "type": "call"} (file: None)
- {"metadata": {"context": "create_architecture_snapshot", "line": 120}, "source": 223, "target": "write_audit_log", "type": "call"} (file: None)
- {"metadata": {"context": "rebuild_lock_manifest", "line": 153}, "source": 223, "target": "write_audit_log", "type": "call"} (file: None)
- {"metadata": {"context": null, "line": 30}, "source": 548, "target": "AuditScanner", "type": "call"} (file: None)
- {"metadata": {"context": null, "line": 30}, "source": 596, "target": "AuditScanner", "type": "call"} (file: None)

---

## CAPABILITY: PASSPORT
**TOTAL EVIDENCE:** 88
**STATUS:** READY
**MAIN ENTRY:** load_profile

### FILES (canonical):
- A_07_CONFIG/passport_report.py
- A_07_CONFIG/project_passport_loader.py
- A_07_MEMORY/profile_manager.py
- A_07_MEMORY/profile_sync.py
- A_03_ORCHESTRATION/passport_commands.py
- A_04_AGENTS/ProjectDocumentationDepartment/Core/Discovery/passport_discovery_agent.py
- A_04_AGENTS/ProjectDocumentationDepartment/Core/Scanners/passport_scanner.py

### CLASSES:
- PassportCommandHandler (file: A_03_ORCHESTRATION/passport_commands.py)
- PassportDiscoveryAgent (file: A_04_AGENTS/ProjectDocumentationDepartment/Core/Discovery/passport_discovery_agent.py)
- PassportReport (file: A_07_CONFIG/passport_report.py)
- PassportScanner (file: A_04_AGENTS/ProjectDocumentationDepartment/Core/Scanners/passport_scanner.py)
- ProjectPassportLoader (file: A_07_CONFIG/project_passport_loader.py)

### FUNCTIONS:
- load_profile (file: A_07_MEMORY/profile_manager.py)
- load_profile (file: A_07_MEMORY/profile_sync.py)
- save_profile (file: A_07_MEMORY/profile_manager.py)
- save_profile (file: A_07_MEMORY/profile_sync.py)

### CALLS:
- PassportCommandHandler (file: 123)
- PassportCommandHandler (file: A_03_ORCHESTRATION/passport_commands.py)
- PassportCommandHandler (file: 467)
- PassportCommandHandler (file: 468)
- PassportReport (file: A_07_CONFIG/passport_report.py)
- PassportReport (file: 1155)
- PassportScanner (file: 536)
- PassportScanner (file: 591)
- ProjectPassportLoader (file: 1102)
- ProjectPassportLoader (file: 1103)
- ProjectPassportLoader (file: 1395)
- ProjectPassportLoader (file: 399)
- ProjectPassportLoader (file: 405)
- load_profile (file: A_07_MEMORY/profile_manager.py)
- load_profile (file: A_07_MEMORY/profile_sync.py)
- load_profile (file: 205)
- load_profile (file: 218)
- load_profile (file: 419)
- save_profile (file: A_07_MEMORY/profile_manager.py)
- save_profile (file: A_07_MEMORY/profile_sync.py)

### DEPENDENCY_NODES:
- PassportCommandHandler (file: None)
- PassportReport (file: None)
- PassportScanner (file: None)
- ProjectPassportLoader (file: None)
- load_profile (file: None)
- save_profile (file: None)

### EXECUTION_FACTS:
- PHASE_1_INIT::BOOTSTRAP: DONE
- PHASE_1_MULTITASK_TEST::TEST_TASK_A: DONE
- PHASE_1_MULTITASK_TEST::TEST_TASK_B: DONE
- PHASE_1_MULTITASK_TEST::TEST_TASK_C: DONE
- PHASE_1_TEST_DIAGNOSTICS::AUDIT_VERIFY_HEALTH: DONE
- PHASE_3_CLEANUP_AND_BACKUP::RUN_CORE_BACKUP: DONE
- TEST_PHASE_1::PHASE_1_TASK_A: DONE
- TEST_PHASE_1::PHASE_1_TASK_B: DONE
- TEST_PHASE_2::PHASE_2_TASK_C: DONE
- TEST_PHASE_2::PHASE_2_TASK_D: DONE

### GOALS_FACTS:
- active_goal: BUTLER_RECIPE_LIBRARY
- current_phase: ROADMAP_6_PHASE_4_RECIPES
- subgoal: ROADMAP_6_PHASE_4_RECIPES status=COMPLETED
- task: task_run_full_audit status=COMPLETED
- task: task_verify_contour status=COMPLETED
- weight: autonomy=0.6
- weight: stability=1.0

### LINKS:
- {"metadata": {"context": "ButlerHarness.execute", "line": 134}, "source": 399, "target": "ProjectPassportLoader", "type": "call"} (file: None)
- {"metadata": {"context": "ButlerOSAdapter.__init__", "line": 11}, "source": 405, "target": "ProjectPassportLoader", "type": "call"} (file: None)
- {"metadata": {"context": "ChatCoreBridge.process", "line": 12}, "source": 205, "target": "load_profile", "type": "call"} (file: None)
- {"metadata": {"context": "ChatRouterMirror.route", "line": 11}, "source": 419, "target": "load_profile", "type": "call"} (file: None)
- {"metadata": {"context": "EngineeringPipeline.collect", "line": 55}, "source": 536, "target": "PassportScanner", "type": "call"} (file: None)
- {"metadata": {"context": "EngineeringPipeline.collect", "line": 55}, "source": 591, "target": "PassportScanner", "type": "call"} (file: None)
- {"metadata": {"context": "MemoryCore.__init__", "line": 8}, "source": 218, "target": "load_profile", "type": "call"} (file: None)
- {"metadata": {"context": "MemoryFacadeV2.get_passport_string", "line": 16}, "source": 1155, "target": "PassportReport", "type": "call"} (file: None)
- {"metadata": {"context": "ProjectState.__init__", "line": 10}, "source": 1102, "target": "ProjectPassportLoader", "type": "call"} (file: None)
- {"metadata": {"context": "ProjectState.__init__", "line": 10}, "source": 1103, "target": "ProjectPassportLoader", "type": "call"} (file: None)
- {"metadata": {"context": "RouterIntegration.__init__", "line": 23}, "source": 123, "target": "PassportCommandHandler", "type": "call"} (file: None)
- {"metadata": {"context": "RouterIntegration.__init__", "line": 23}, "source": 467, "target": "PassportCommandHandler", "type": "call"} (file: None)
- {"metadata": {"context": "RouterIntegration.__init__", "line": 26}, "source": 468, "target": "PassportCommandHandler", "type": "call"} (file: None)
- {"metadata": {"context": "add_episode", "line": 222}, "source": 1165, "target": "load_profile", "type": "call"} (file: None)
- {"metadata": {"context": "add_episode", "line": 232}, "source": 1165, "target": "save_profile", "type": "call"} (file: None)
- {"metadata": {"context": "add_episode", "line": 233}, "source": 1165, "target": "save_profile", "type": "call"} (file: None)
- {"metadata": {"context": "add_skill", "line": 161}, "source": 1165, "target": "load_profile", "type": "call"} (file: None)
- {"metadata": {"context": "add_skill", "line": 172}, "source": 1165, "target": "save_profile", "type": "call"} (file: None)
- {"metadata": {"context": "delete_fact", "line": 56}, "source": 1165, "target": "load_profile", "type": "call"} (file: None)
- {"metadata": {"context": "delete_fact", "line": 65}, "source": 1165, "target": "save_profile", "type": "call"} (file: None)
- ... and 16 more

---

## CAPABILITY: REASONING
**TOTAL EVIDENCE:** 292
**STATUS:** READY
**MAIN ENTRY:** SemanticReasoningEngine

### FILES (canonical):
- A_07_CONFIG/project_memory_loader.py
- A_07_MEMORY/agent_runtime_v2.py
- A_07_MEMORY/attention_memory.py
- A_07_MEMORY/memory_advisor.py
- A_07_MEMORY/memory_facade.py
- A_07_MEMORY/memory_facade_v2.py
- A_07_MEMORY/memory_layer.py
- A_07_MEMORY/memory_orchestrator.py
- A_07_MEMORY/memory_orchestrator_v2.py
- A_07_MEMORY/memory_replay.py
- A_07_MEMORY/memory_router.py
- A_07_MEMORY/png_workflow_memory.py
- A_07_MEMORY/profile_manager.py
- A_07_MEMORY/profile_sync.py
- A_07_MEMORY/project_history.py
- A_07_MEMORY/search_engine.py
- A_07_MEMORY/self_healing_memory.py
- A_07_MEMORY/semantic_compression.py
- A_07_MEMORY/semantic_constraint_layer.py
- A_07_MEMORY/semantic_core.py
- A_07_MEMORY/semantic_memory.py
- A_07_MEMORY/semantic_query_parser.py
- A_07_MEMORY/semantic_reasoning_engine.py
- A_07_MEMORY/semantic_reasoning_engine_v2.py
- A_07_MEMORY/semantic_relations_engine.py
- A_09_TESTS/test_memory_advisor.py
- A_01_CORE/memory_core.py
- A_01_CORE/memory_guardian.py
- A_02_MANAGERS/ExecutionMonitor/execution_history.py
- A_02_MANAGERS/memory_manager.py
- A_03_ORCHESTRATION/memory_loop.py
- A_03_ORCHESTRATION/memory_sidecar.py
- A_03_ORCHESTRATION/semantic_layer.py
- A_04_AGENTS/MemoryDepartment/runner.py
- A_04_AGENTS/ProjectDocumentationDepartment/Core/Scanners/history_scanner.py
- A_04_COMPONENTS/MemoryAdvisor/memory_advisor.py

### CLASSES:
- AttentionMemory (file: A_07_MEMORY/attention_memory.py)
- ExecutionHistory (file: A_02_MANAGERS/ExecutionMonitor/execution_history.py)
- ExecutionMemoryV2 (file: A_07_MEMORY/agent_runtime_v2.py)
- HistoryScanner (file: A_04_AGENTS/ProjectDocumentationDepartment/Core/Scanners/history_scanner.py)
- MemoryAdvisor (file: A_07_MEMORY/memory_advisor.py)
- MemoryAdvisor (file: A_04_COMPONENTS/MemoryAdvisor/memory_advisor.py)
- MemoryCore (file: A_01_CORE/memory_core.py)
- MemoryDepartment (file: A_04_AGENTS/MemoryDepartment/runner.py)
- MemoryFacade (file: A_07_MEMORY/memory_facade.py)
- MemoryFacadeV2 (file: A_07_MEMORY/memory_facade_v2.py)
- MemoryLayer (file: A_07_MEMORY/memory_layer.py)
- MemoryLoop (file: A_03_ORCHESTRATION/memory_loop.py)
- MemoryManager (file: A_02_MANAGERS/memory_manager.py)
- MemoryOrchestrator (file: A_07_MEMORY/memory_orchestrator.py)
- MemoryOrchestratorV2 (file: A_07_MEMORY/memory_orchestrator_v2.py)
- MemoryReplay (file: A_07_MEMORY/memory_replay.py)
- MemorySidecar (file: A_03_ORCHESTRATION/memory_sidecar.py)
- PNGWorkflowMemory (file: A_07_MEMORY/png_workflow_memory.py)
- ProjectHistory (file: A_07_MEMORY/project_history.py)
- ProjectMemoryLoader (file: A_07_CONFIG/project_memory_loader.py)
- ReasoningPath (file: A_07_MEMORY/semantic_reasoning_engine_v2.py)
- SelfHealingMemory (file: A_07_MEMORY/self_healing_memory.py)
- SemanticCompressor (file: A_07_MEMORY/semantic_compression.py)
- SemanticConstraintLayer (file: A_07_MEMORY/semantic_constraint_layer.py)
- SemanticCore (file: A_07_MEMORY/semantic_core.py)
- SemanticLayer (file: A_03_ORCHESTRATION/semantic_layer.py)
- SemanticMatch (file: A_07_MEMORY/semantic_reasoning_engine.py)
- SemanticMemory (file: A_07_MEMORY/semantic_memory.py)
- SemanticQueryParser (file: A_07_MEMORY/semantic_query_parser.py)
- SemanticReasoningEngine (file: A_07_MEMORY/semantic_reasoning_engine.py)
- SemanticReasoningEngineV2 (file: A_07_MEMORY/semantic_reasoning_engine_v2.py)
- SemanticRelationsEngine (file: A_07_MEMORY/semantic_relations_engine.py)
- SemanticSearchEngine (file: A_07_MEMORY/search_engine.py)
- TestMemoryAdvisor (file: A_09_TESTS/test_memory_advisor.py)

### FUNCTIONS:
- get_memory_summary (file: A_07_MEMORY/profile_manager.py)
- rebuild_user_memory (file: A_07_MEMORY/profile_manager.py)
- rebuild_user_memory (file: A_07_MEMORY/profile_sync.py)
- remember (file: A_07_MEMORY/memory_router.py)
- route_memory (file: A_07_MEMORY/memory_router.py)
- run_memory_guardian (file: A_01_CORE/memory_guardian.py)

### CALLS:
- AttentionMemory (file: A_07_MEMORY/attention_memory.py)
- AttentionMemory (file: 1136)
- AttentionMemory (file: A_07_MEMORY/memory_orchestrator_v2.py)
- ExecutionMemoryV2 (file: A_07_MEMORY/agent_runtime_v2.py)
- HistoryScanner (file: 536)
- HistoryScanner (file: A_04_AGENTS/ProjectDocumentationDepartment/Core/Scanners/history_scanner.py)
- HistoryScanner (file: 591)
- HistoryScanner (file: 601)
- MemoryAdvisor (file: A_07_MEMORY/memory_advisor.py)
- MemoryAdvisor (file: A_09_TESTS/test_memory_advisor.py)
- MemoryCore (file: 208)
- MemoryCore (file: A_01_CORE/memory_core.py)
- MemoryDepartment (file: 1285)
- MemoryDepartment (file: 1287)
- MemoryDepartment (file: 1340)
- MemoryDepartment (file: 324)
- MemoryDepartment (file: 338)
- MemoryFacade (file: 1144)
- MemoryFacade (file: A_07_MEMORY/memory_facade.py)
- MemoryFacade (file: 453)
- ... and 70 more

### DEPENDENCY_NODES:
- A_04_AGENTS.MemoryDepartment.runner (file: None)
- A_04_COMPONENTS.MemoryAdvisor.memory_advisor (file: None)
- AttentionMemory (file: None)
- ExecutionMemoryV2 (file: None)
- HistoryScanner (file: None)
- MemoryAdvisor (file: None)
- MemoryCore (file: None)
- MemoryDepartment (file: None)
- MemoryFacade (file: None)
- MemoryFacadeV2 (file: None)
- MemoryLayer (file: None)
- MemoryLoop (file: None)
- MemoryManager (file: None)
- MemoryOrchestrator (file: None)
- MemoryOrchestratorV2 (file: None)
- MemoryReplay (file: None)
- MemorySidecar (file: None)
- PNGWorkflowMemory (file: None)
- ProjectHistory (file: None)
- ProjectMemoryLoader (file: None)
- ... and 18 more

### EXECUTION_FACTS:
- PHASE_1_INIT::BOOTSTRAP: DONE
- PHASE_1_MULTITASK_TEST::TEST_TASK_A: DONE
- PHASE_1_MULTITASK_TEST::TEST_TASK_B: DONE
- PHASE_1_MULTITASK_TEST::TEST_TASK_C: DONE
- PHASE_1_TEST_DIAGNOSTICS::AUDIT_VERIFY_HEALTH: DONE
- PHASE_3_CLEANUP_AND_BACKUP::RUN_CORE_BACKUP: DONE
- TEST_PHASE_1::PHASE_1_TASK_A: DONE
- TEST_PHASE_1::PHASE_1_TASK_B: DONE
- TEST_PHASE_2::PHASE_2_TASK_C: DONE
- TEST_PHASE_2::PHASE_2_TASK_D: DONE

### GOALS_FACTS:
- active_goal: BUTLER_RECIPE_LIBRARY
- current_phase: ROADMAP_6_PHASE_4_RECIPES
- subgoal: ROADMAP_6_PHASE_4_RECIPES status=COMPLETED
- task: task_run_full_audit status=COMPLETED
- task: task_verify_contour status=COMPLETED
- weight: autonomy=0.6
- weight: stability=1.0

### IMPORTS:
- A_04_AGENTS.MemoryDepartment.runner (file: 1285)
- A_04_AGENTS.MemoryDepartment.runner (file: 1287)
- A_04_AGENTS.MemoryDepartment.runner (file: 1340)
- A_04_AGENTS.MemoryDepartment.runner (file: 324)
- A_04_AGENTS.MemoryDepartment.runner (file: 338)
- A_04_COMPONENTS.MemoryAdvisor.memory_advisor (file: A_09_TESTS/test_memory_advisor.py)

### LINKS:
- {"metadata": {"alias": null, "kind": "from", "line": 2, "name": "MemoryDepartment"}, "source": 1340, "target": "A_04_AGENTS.MemoryDepartment.runner", "type": "import"} (file: None)
- {"metadata": {"alias": null, "kind": "from", "line": 3, "name": "MemoryAdvisor"}, "source": 1347, "target": "A_04_COMPONENTS.MemoryAdvisor.memory_advisor", "type": "import"} (file: None)
- {"metadata": {"alias": null, "kind": "from", "line": 4, "name": "MemoryDepartment"}, "source": 1285, "target": "A_04_AGENTS.MemoryDepartment.runner", "type": "import"} (file: None)
- {"metadata": {"alias": null, "kind": "from", "line": 4, "name": "MemoryDepartment"}, "source": 1287, "target": "A_04_AGENTS.MemoryDepartment.runner", "type": "import"} (file: None)
- {"metadata": {"alias": null, "kind": "from", "line": 4, "name": "MemoryDepartment"}, "source": 324, "target": "A_04_AGENTS.MemoryDepartment.runner", "type": "import"} (file: None)
- {"metadata": {"alias": null, "kind": "from", "line": 4, "name": "MemoryDepartment"}, "source": 338, "target": "A_04_AGENTS.MemoryDepartment.runner", "type": "import"} (file: None)
- {"metadata": {"context": "AgentLoopExecutor.__init__", "line": 10}, "source": 1114, "target": "ProjectHistory", "type": "call"} (file: None)
- {"metadata": {"context": "AttentionMemory.__init__", "line": 14}, "source": 1124, "target": "MemoryReplay", "type": "call"} (file: None)
- {"metadata": {"context": "BootstrapCore.__init__", "line": 15}, "source": 1495, "target": "SelfHealingMemory", "type": "call"} (file: None)
- {"metadata": {"context": "ButlerOSAdapter.__init__", "line": 12}, "source": 405, "target": "ProjectMemoryLoader", "type": "call"} (file: None)
- {"metadata": {"context": "ButlerOSAdapter.memory_summary", "line": 15}, "source": 405, "target": "get_memory_summary", "type": "call"} (file: None)
- {"metadata": {"context": "ButlerSystem.__init__", "line": 14}, "source": 1505, "target": "SelfHealingMemory", "type": "call"} (file: None)
- {"metadata": {"context": "ChatCoreBridge.__init__", "line": 7}, "source": 205, "target": "SemanticLayer", "type": "call"} (file: None)
- {"metadata": {"context": "ChatRouterMirror.__init__", "line": 7}, "source": 419, "target": "SemanticLayer", "type": "call"} (file: None)
- {"metadata": {"context": "ContextBudgetManager.__init__", "line": 15}, "source": 1136, "target": "AttentionMemory", "type": "call"} (file: None)
- {"metadata": {"context": "ContextBudgetManager.__init__", "line": 16}, "source": 1136, "target": "MemoryOrchestrator", "type": "call"} (file: None)
- {"metadata": {"context": "CoreKernel.__init__", "line": 9}, "source": 207, "target": "SemanticLayer", "type": "call"} (file: None)
- {"metadata": {"context": "CoreOrchestrator.__init__", "line": 7}, "source": 208, "target": "SemanticLayer", "type": "call"} (file: None)
- {"metadata": {"context": "CoreOrchestrator.__init__", "line": 8}, "source": 208, "target": "MemoryCore", "type": "call"} (file: None)
- {"metadata": {"context": "DispatcherAgent.__init__", "line": 25}, "source": 508, "target": "SemanticMemory", "type": "call"} (file: None)
- ... and 81 more

---

## CAPABILITY: SEMANTIC
**TOTAL EVIDENCE:** 292
**STATUS:** READY
**MAIN ENTRY:** SemanticReasoningEngine

### FILES (canonical):
- A_07_CONFIG/project_memory_loader.py
- A_07_MEMORY/agent_runtime_v2.py
- A_07_MEMORY/attention_memory.py
- A_07_MEMORY/memory_advisor.py
- A_07_MEMORY/memory_facade.py
- A_07_MEMORY/memory_facade_v2.py
- A_07_MEMORY/memory_layer.py
- A_07_MEMORY/memory_orchestrator.py
- A_07_MEMORY/memory_orchestrator_v2.py
- A_07_MEMORY/memory_replay.py
- A_07_MEMORY/memory_router.py
- A_07_MEMORY/png_workflow_memory.py
- A_07_MEMORY/profile_manager.py
- A_07_MEMORY/profile_sync.py
- A_07_MEMORY/project_history.py
- A_07_MEMORY/search_engine.py
- A_07_MEMORY/self_healing_memory.py
- A_07_MEMORY/semantic_compression.py
- A_07_MEMORY/semantic_constraint_layer.py
- A_07_MEMORY/semantic_core.py
- A_07_MEMORY/semantic_memory.py
- A_07_MEMORY/semantic_query_parser.py
- A_07_MEMORY/semantic_reasoning_engine.py
- A_07_MEMORY/semantic_reasoning_engine_v2.py
- A_07_MEMORY/semantic_relations_engine.py
- A_09_TESTS/test_memory_advisor.py
- A_01_CORE/memory_core.py
- A_01_CORE/memory_guardian.py
- A_02_MANAGERS/ExecutionMonitor/execution_history.py
- A_02_MANAGERS/memory_manager.py
- A_03_ORCHESTRATION/memory_loop.py
- A_03_ORCHESTRATION/memory_sidecar.py
- A_03_ORCHESTRATION/semantic_layer.py
- A_04_AGENTS/MemoryDepartment/runner.py
- A_04_AGENTS/ProjectDocumentationDepartment/Core/Scanners/history_scanner.py
- A_04_COMPONENTS/MemoryAdvisor/memory_advisor.py

### CLASSES:
- AttentionMemory (file: A_07_MEMORY/attention_memory.py)
- ExecutionHistory (file: A_02_MANAGERS/ExecutionMonitor/execution_history.py)
- ExecutionMemoryV2 (file: A_07_MEMORY/agent_runtime_v2.py)
- HistoryScanner (file: A_04_AGENTS/ProjectDocumentationDepartment/Core/Scanners/history_scanner.py)
- MemoryAdvisor (file: A_07_MEMORY/memory_advisor.py)
- MemoryAdvisor (file: A_04_COMPONENTS/MemoryAdvisor/memory_advisor.py)
- MemoryCore (file: A_01_CORE/memory_core.py)
- MemoryDepartment (file: A_04_AGENTS/MemoryDepartment/runner.py)
- MemoryFacade (file: A_07_MEMORY/memory_facade.py)
- MemoryFacadeV2 (file: A_07_MEMORY/memory_facade_v2.py)
- MemoryLayer (file: A_07_MEMORY/memory_layer.py)
- MemoryLoop (file: A_03_ORCHESTRATION/memory_loop.py)
- MemoryManager (file: A_02_MANAGERS/memory_manager.py)
- MemoryOrchestrator (file: A_07_MEMORY/memory_orchestrator.py)
- MemoryOrchestratorV2 (file: A_07_MEMORY/memory_orchestrator_v2.py)
- MemoryReplay (file: A_07_MEMORY/memory_replay.py)
- MemorySidecar (file: A_03_ORCHESTRATION/memory_sidecar.py)
- PNGWorkflowMemory (file: A_07_MEMORY/png_workflow_memory.py)
- ProjectHistory (file: A_07_MEMORY/project_history.py)
- ProjectMemoryLoader (file: A_07_CONFIG/project_memory_loader.py)
- ReasoningPath (file: A_07_MEMORY/semantic_reasoning_engine_v2.py)
- SelfHealingMemory (file: A_07_MEMORY/self_healing_memory.py)
- SemanticCompressor (file: A_07_MEMORY/semantic_compression.py)
- SemanticConstraintLayer (file: A_07_MEMORY/semantic_constraint_layer.py)
- SemanticCore (file: A_07_MEMORY/semantic_core.py)
- SemanticLayer (file: A_03_ORCHESTRATION/semantic_layer.py)
- SemanticMatch (file: A_07_MEMORY/semantic_reasoning_engine.py)
- SemanticMemory (file: A_07_MEMORY/semantic_memory.py)
- SemanticQueryParser (file: A_07_MEMORY/semantic_query_parser.py)
- SemanticReasoningEngine (file: A_07_MEMORY/semantic_reasoning_engine.py)
- SemanticReasoningEngineV2 (file: A_07_MEMORY/semantic_reasoning_engine_v2.py)
- SemanticRelationsEngine (file: A_07_MEMORY/semantic_relations_engine.py)
- SemanticSearchEngine (file: A_07_MEMORY/search_engine.py)
- TestMemoryAdvisor (file: A_09_TESTS/test_memory_advisor.py)

### FUNCTIONS:
- get_memory_summary (file: A_07_MEMORY/profile_manager.py)
- rebuild_user_memory (file: A_07_MEMORY/profile_manager.py)
- rebuild_user_memory (file: A_07_MEMORY/profile_sync.py)
- remember (file: A_07_MEMORY/memory_router.py)
- route_memory (file: A_07_MEMORY/memory_router.py)
- run_memory_guardian (file: A_01_CORE/memory_guardian.py)

### CALLS:
- AttentionMemory (file: A_07_MEMORY/attention_memory.py)
- AttentionMemory (file: 1136)
- AttentionMemory (file: A_07_MEMORY/memory_orchestrator_v2.py)
- ExecutionMemoryV2 (file: A_07_MEMORY/agent_runtime_v2.py)
- HistoryScanner (file: 536)
- HistoryScanner (file: A_04_AGENTS/ProjectDocumentationDepartment/Core/Scanners/history_scanner.py)
- HistoryScanner (file: 591)
- HistoryScanner (file: 601)
- MemoryAdvisor (file: A_07_MEMORY/memory_advisor.py)
- MemoryAdvisor (file: A_09_TESTS/test_memory_advisor.py)
- MemoryCore (file: 208)
- MemoryCore (file: A_01_CORE/memory_core.py)
- MemoryDepartment (file: 1285)
- MemoryDepartment (file: 1287)
- MemoryDepartment (file: 1340)
- MemoryDepartment (file: 324)
- MemoryDepartment (file: 338)
- MemoryFacade (file: 1144)
- MemoryFacade (file: A_07_MEMORY/memory_facade.py)
- MemoryFacade (file: 453)
- ... and 70 more

### DEPENDENCY_NODES:
- A_04_AGENTS.MemoryDepartment.runner (file: None)
- A_04_COMPONENTS.MemoryAdvisor.memory_advisor (file: None)
- AttentionMemory (file: None)
- ExecutionMemoryV2 (file: None)
- HistoryScanner (file: None)
- MemoryAdvisor (file: None)
- MemoryCore (file: None)
- MemoryDepartment (file: None)
- MemoryFacade (file: None)
- MemoryFacadeV2 (file: None)
- MemoryLayer (file: None)
- MemoryLoop (file: None)
- MemoryManager (file: None)
- MemoryOrchestrator (file: None)
- MemoryOrchestratorV2 (file: None)
- MemoryReplay (file: None)
- MemorySidecar (file: None)
- PNGWorkflowMemory (file: None)
- ProjectHistory (file: None)
- ProjectMemoryLoader (file: None)
- ... and 18 more

### EXECUTION_FACTS:
- PHASE_1_INIT::BOOTSTRAP: DONE
- PHASE_1_MULTITASK_TEST::TEST_TASK_A: DONE
- PHASE_1_MULTITASK_TEST::TEST_TASK_B: DONE
- PHASE_1_MULTITASK_TEST::TEST_TASK_C: DONE
- PHASE_1_TEST_DIAGNOSTICS::AUDIT_VERIFY_HEALTH: DONE
- PHASE_3_CLEANUP_AND_BACKUP::RUN_CORE_BACKUP: DONE
- TEST_PHASE_1::PHASE_1_TASK_A: DONE
- TEST_PHASE_1::PHASE_1_TASK_B: DONE
- TEST_PHASE_2::PHASE_2_TASK_C: DONE
- TEST_PHASE_2::PHASE_2_TASK_D: DONE

### GOALS_FACTS:
- active_goal: BUTLER_RECIPE_LIBRARY
- current_phase: ROADMAP_6_PHASE_4_RECIPES
- subgoal: ROADMAP_6_PHASE_4_RECIPES status=COMPLETED
- task: task_run_full_audit status=COMPLETED
- task: task_verify_contour status=COMPLETED
- weight: autonomy=0.6
- weight: stability=1.0

### IMPORTS:
- A_04_AGENTS.MemoryDepartment.runner (file: 1285)
- A_04_AGENTS.MemoryDepartment.runner (file: 1287)
- A_04_AGENTS.MemoryDepartment.runner (file: 1340)
- A_04_AGENTS.MemoryDepartment.runner (file: 324)
- A_04_AGENTS.MemoryDepartment.runner (file: 338)
- A_04_COMPONENTS.MemoryAdvisor.memory_advisor (file: A_09_TESTS/test_memory_advisor.py)

### LINKS:
- {"metadata": {"alias": null, "kind": "from", "line": 2, "name": "MemoryDepartment"}, "source": 1340, "target": "A_04_AGENTS.MemoryDepartment.runner", "type": "import"} (file: None)
- {"metadata": {"alias": null, "kind": "from", "line": 3, "name": "MemoryAdvisor"}, "source": 1347, "target": "A_04_COMPONENTS.MemoryAdvisor.memory_advisor", "type": "import"} (file: None)
- {"metadata": {"alias": null, "kind": "from", "line": 4, "name": "MemoryDepartment"}, "source": 1285, "target": "A_04_AGENTS.MemoryDepartment.runner", "type": "import"} (file: None)
- {"metadata": {"alias": null, "kind": "from", "line": 4, "name": "MemoryDepartment"}, "source": 1287, "target": "A_04_AGENTS.MemoryDepartment.runner", "type": "import"} (file: None)
- {"metadata": {"alias": null, "kind": "from", "line": 4, "name": "MemoryDepartment"}, "source": 324, "target": "A_04_AGENTS.MemoryDepartment.runner", "type": "import"} (file: None)
- {"metadata": {"alias": null, "kind": "from", "line": 4, "name": "MemoryDepartment"}, "source": 338, "target": "A_04_AGENTS.MemoryDepartment.runner", "type": "import"} (file: None)
- {"metadata": {"context": "AgentLoopExecutor.__init__", "line": 10}, "source": 1114, "target": "ProjectHistory", "type": "call"} (file: None)
- {"metadata": {"context": "AttentionMemory.__init__", "line": 14}, "source": 1124, "target": "MemoryReplay", "type": "call"} (file: None)
- {"metadata": {"context": "BootstrapCore.__init__", "line": 15}, "source": 1495, "target": "SelfHealingMemory", "type": "call"} (file: None)
- {"metadata": {"context": "ButlerOSAdapter.__init__", "line": 12}, "source": 405, "target": "ProjectMemoryLoader", "type": "call"} (file: None)
- {"metadata": {"context": "ButlerOSAdapter.memory_summary", "line": 15}, "source": 405, "target": "get_memory_summary", "type": "call"} (file: None)
- {"metadata": {"context": "ButlerSystem.__init__", "line": 14}, "source": 1505, "target": "SelfHealingMemory", "type": "call"} (file: None)
- {"metadata": {"context": "ChatCoreBridge.__init__", "line": 7}, "source": 205, "target": "SemanticLayer", "type": "call"} (file: None)
- {"metadata": {"context": "ChatRouterMirror.__init__", "line": 7}, "source": 419, "target": "SemanticLayer", "type": "call"} (file: None)
- {"metadata": {"context": "ContextBudgetManager.__init__", "line": 15}, "source": 1136, "target": "AttentionMemory", "type": "call"} (file: None)
- {"metadata": {"context": "ContextBudgetManager.__init__", "line": 16}, "source": 1136, "target": "MemoryOrchestrator", "type": "call"} (file: None)
- {"metadata": {"context": "CoreKernel.__init__", "line": 9}, "source": 207, "target": "SemanticLayer", "type": "call"} (file: None)
- {"metadata": {"context": "CoreOrchestrator.__init__", "line": 7}, "source": 208, "target": "SemanticLayer", "type": "call"} (file: None)
- {"metadata": {"context": "CoreOrchestrator.__init__", "line": 8}, "source": 208, "target": "MemoryCore", "type": "call"} (file: None)
- {"metadata": {"context": "DispatcherAgent.__init__", "line": 25}, "source": 508, "target": "SemanticMemory", "type": "call"} (file: None)
- ... and 81 more

---
