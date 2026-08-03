============================================================
BUTLER SEMANTIC AUDIT
============================================================

Total categorized components: 857

## ADAPTER (7 components)
- **ButlerOSAdapter** (class) — 405
  - Methods: __init__, memory_summary, skills_summary, episodes_summary, passport_summary...
- **ProfessorAdapter** (class) — 465
  - Methods: __init__, process_agent_task
- **adapter_class** (call) — 346
  - Context: ExecutorFactory.register

## AGENT (46 components)
- **AgentLoopExecutor** (class) — 1114
  - Methods: __init__, get_last_state, decide_next_action, run_cycle
- **AgentPlanner** (class) — 393
  - Methods: __init__, create_plan, save_checkpoint, load_unfinished_plan
- **AgentPlannerV2** (class) — 1115
  - Methods: __init__, load_registry, _save_registry, get_current_action_plan, complete_task
- **AgentRouter** (class) — 394
  - Methods: route
- **ArchitectAgent** (class) — 261
  - Methods: __init__, execute_goal, plan
- **DispatcherAgent** (class) — 508
  - Methods: __init__, execute_employee, resolve_file_path, normalize_tags, parse_model_response...
- **EngineeringAgent** (class) — 518
  - Methods: __init__, discover, collect_evidence, verify, report
- **ExecutionRegistryDiscoveryAgent** (class) — 527
  - Methods: discover, collect_evidence, verify, report
- **GoalsRegistryDiscoveryAgent** (class) — 528
  - Methods: discover, collect_evidence, verify, report
- **PassportDiscoveryAgent** (class) — 530
  - Methods: discover, collect_evidence, verify, report
- **ProjectStateDiscoveryAgent** (class) — 531
  - Methods: discover, collect_evidence, verify, report
- **RegistryDiscoveryAgent** (class) — 532
  - Methods: discover, collect_evidence, verify, report
- **RegistryReaderAgent** (class) — 533
  - Methods: discover, collect_evidence, verify, report
- **process_agent_task** (call) — 465
  - Context: ProfessorAdapter.process_agent_task

## ANALYZER (19 components)
- **DependencyAnalyzer** (class) — 271
  - Methods: __init__, analyze
- **GoalAnalyzer** (class) — 274
  - Methods: analyze
- **VisionAnalyzer** (class) — 390
  - Methods: __init__, analyze, analyze_document, analyze_code_screenshot, analyze_schematic...

## AUDITOR (3 components)
- **ProjectAuditor** (class) — 633
  - Methods: __init__, run
- **TestProjectAuditor** (class) — 1353
  - Methods: test_stub

## BRIDGE (9 components)
- **ChatCoreBridge** (class) — 205
  - Methods: __init__, process
- **ComfyUIBridge** (class) — 371
  - Methods: __init__, check_comfy_status, generate_image
- **FactoryCoreBridge** (class) — 434
  - Methods: __init__, handle, _archive, _quarantine, _dispatch...
- **ToolBridge** (class) — 360
  - Methods: __init__, extract_tags, find_documents, get_file_paths

## BUILDER (21 components)
- **ButlerContextBuilder** (class) — 422
  - Methods: __init__, _read_layer_safe, assemble_context
- **ProjectContextBuilder** (class) — 619
  - Methods: __init__, get_execution_context, get_goals_context, get_ledger_context, build_full_context
- **RecipeBuilder** (class) — 279
  - Methods: build_planning_recipe
- **TaskContractBuilder** (class) — 281
  - Methods: build

## CAPABILITY (3 components)
- **RuntimeCapability** (class) — 319

## CATALOG (18 components)
- **EngineeringObjectCatalog** (class) — 522
  - Methods: __init__, register, exists, get, all...
- **show_catalog** (function) — 1455
- **test_catalog_update** (function) — 236

## CONTEXT (31 components)
- **_check_patch_context** (call) — 318
  - Context: RecipeValidator.validate
- **assemble_context** (call) — 422
- **build_attention_context** (call) — 1124
- **build_context** (call) — 261
  - Context: ArchitectAgent.plan
- **build_full_context** (call) — 619
- **build_minimal_context** (function) — 289
- **get_goals_context** (call) — 619
  - Context: ProjectContextBuilder.build_full_context
- **get_ledger_context** (call) — 619
  - Context: ProjectContextBuilder.build_full_context
- **get_unified_context** (call) — 1144
  - Context: MemoryFacade.get_passport_string
- **load_latest_context** (call) — 1202
  - Context: SessionReader.get_last_query
- **reconstruct_context** (call) — 1158
  - Context: MemoryOrchestrator.build_context

## DEPARTMENT (81 components)
- **ArchiveDepartment** (class) — 483
  - Methods: can_handle, _extract_archive_path, execute
- **AudioDepartment** (class) — 486
  - Methods: can_handle, execute
- **BaseDepartment** (class) — 487
  - Methods: can_handle, execute, __repr__
- **CodingDepartment** (class) — 491
  - Methods: __init__, can_handle, _ask, execute
- **Department** (class) — 1359
  - Methods: can_handle, execute, fallback
- **DocumentsDepartment** (class) — 493
  - Methods: __init__, can_handle, _extract_file_path, _call_local_llm, execute
- **ImageDepartment** (class) — 499
  - Methods: __init__, can_handle, _clean_prompt, _list_first, _get_object_info...
- **MemoryDepartment** (class) — 505
  - Methods: __init__, can_handle, execute
- **OpenDocumentDepartment** (class) — 507
  - Methods: __init__, can_handle, execute
- **ProjectDocumentationDepartment** (class) — 611
  - Methods: can_handle, execute
- **RuntimeDepartmentsDiscoveryAgent** (class) — 534
  - Methods: discover, collect_evidence, verify, report
- **SearchDepartment** (class) — 616
  - Methods: __init__, can_handle, _clean_query, execute
- **TextDepartment** (class) — 620
  - Methods: __init__, can_handle, clean_text, available_models, execute
- **VideoDepartment** (class) — 623
  - Methods: can_handle, execute
- **VisionDepartment** (class) — 625
  - Methods: __init__, can_handle, _encode_image, _extract_image_path, execute
- **_execute_department** (call) — 324
  - Context: SmartDispatcherV2.dispatch

## DEPENDENCY (3 components)
- **DependencyClosure** (class) — 272
  - Methods: __init__, closure

## DISPATCHER (26 components)
- **Dispatcher** (class) — 365
  - Methods: __init__, dispatch
- **DispatcherBridge** (class) — 429
  - Methods: __init__, log, fetch_task
- **DispatcherScanner** (class) — 549
  - Methods: scan
- **DreamDispatcherAdapter** (class) — 432
  - Methods: __init__, execute_employee
- **FakeDispatcher** (class) — 291
  - Methods: execute_employee
- **SmartDispatcher** (class) — 322
  - Methods: __init__, determine_role, _model_for_role, execute_employee
- **SmartDispatcherV2** (class) — 324
  - Methods: __init__, _dept_name, _execute_department, dispatch

## ENGINE (96 components)
- **ConversationContextEngine** (class) — 426
  - Methods: resolve, update
- **EngineeringEvidence** (class) — 519
- **EngineeringEvidenceCollection** (class) — 520
  - Methods: __init__, add, all, count, by_source...
- **EngineeringObject** (class) — 521
  - Methods: __init__
- **EngineeringObjectIdentifier** (class) — 523
  - Methods: __init__, next_id
- **EngineeringObjectRelationship** (class) — 524
  - Methods: __init__, add, get_parent, get_children
- **EngineeringPipeline** (class) — 536
  - Methods: __init__, _add_dict_object, collect, execute
- **GoalLoopEngine** (class) — 1139
  - Methods: __init__, load, save, run
- **PlannerDecisionEngine** (class) — 275
  - Methods: __init__, decide
- **PlannerEngine** (class) — 305
  - Methods: can_handle, execute, execute_decision
- **VisionEngine** (class) — 391
  - Methods: __init__, analyze

## EXECUTION (28 components)
- **BaseExecutionAdapter** (class) — 342
  - Methods: execute_step
- **ExecutionContext** (class) — 1081
- **ExecutionHistory** (class) — 292
  - Methods: load
- **ExecutionLoop** (class) — 211
  - Methods: __init__, fetch_task, execute, run
- **ExecutionMonitor** (class) — 293
  - Methods: __init__, completed_recipes, failed_recipes
- **ExecutionPolicy** (class) — 1082
- **ExecutionResult** (class) — 340
- **ExecutionScanner** (class) — 550
  - Methods: scan
- **ExecutionState** (class) — 294
  - Methods: last
- **PowerShellExecutionAdapter** (class) — 343
  - Methods: execute_step
- **PythonExecutionAdapter** (class) — 344
  - Methods: execute_step
- **get_execution_context** (call) — 619
  - Context: ProjectContextBuilder.build_full_context

## GRAPH (6 components)
- **DependencyGraph** (class) — 273
  - Methods: __init__, _files, build
- **_build_checkpoint_graph** (call) — 499
  - Context: ImageDepartment.execute

## GUARDIAN (2 components)
- **run_guardian** (function) — 231

## HISTORY (22 components)
- **HistoryScanner** (class) — 553
  - Methods: __init__, scan
- **ProjectHistory** (class) — 1169
  - Methods: __init__, get_closed_milestones, get_lesson_summary
- **get_full_history** (call) — 1124
  - Context: AttentionMemory.get_weighted_memory
- **get_history** (call) — 1160
  - Context: MemoryReplay.get_full_history

## MANAGER (53 components)
- **ButlerDreamManager** (class) — 291
  - Methods: __init__, consolidate_completed_task, _update_global_checkpoint
- **ButlerSessionManager** (class) — 321
  - Methods: __init__, append, get_recent, clear
- **CatalogManager** (class) — 285
  - Methods: __init__, register_document, full_text_search
- **ChangeRequestManager** (class) — 1133
  - Methods: __init__, _normalize, _hash, is_already_proposed, propose_change
- **ContextBudgetManager** (class) — 1136
  - Methods: __init__, estimate_tokens, build_context, build_payload
- **MemoryManager** (class) — 300
  - Methods: __init__, save_to_memory
- **ProviderManager** (class) — 315
  - Methods: __init__, check_ollama_status, get_local_models, inspect_manifest_models
- **QueueManager** (class) — 278
  - Methods: __init__, enqueue
- **SessionManagerPoly** (class) — 1202
  - Methods: __init__, create_session, get_active_session, update_search_context, _save_state_unlocked

## MANIFEST (13 components)
- **ManifestLoader** (class) — 216
  - Methods: load
- **inspect_manifest_models** (call) — 315
- **load_manifest** (function) — 206
- **rebuild_lock_manifest** (function) — 223
- **verify_lock_manifest** (function) — 219

## MEMORY (74 components)
- **AttentionMemory** (class) — 1124
  - Methods: __init__, score_event, get_weighted_memory, build_attention_context
- **ExecutionMemoryV2** (class) — 1118
  - Methods: __init__, register, is_stuck
- **MemoryAdvisor** (class) — 632
  - Methods: __init__, extract_facts
- **MemoryCore** (class) — 218
  - Methods: __init__, get_user_name, get_preferences, build_memory_packet, inject_into_prompt
- **MemoryFacade** (class) — 1144
  - Methods: __init__, _load_raw_passport, get_unified_context, get_passport_string
- **MemoryFacadeV2** (class) — 1155
  - Methods: get_passport_string
- **MemoryLayer** (class) — 1157
  - Methods: __init__, build_prompt
- **MemoryLoop** (class) — 447
  - Methods: __init__, remember, recall
- **MemoryReplay** (class) — 1160
  - Methods: __init__, get_full_history, replay_last_n, reconstruct_context, search_event
- **MemorySidecar** (class) — 448
  - Methods: __init__, parse_line, run_loop
- **PNGWorkflowMemory** (class) — 1164
  - Methods: __init__, _load, _save, register, get_workflow
- **ProjectMemoryLoader** (class) — 1090
  - Methods: __init__, load_memory_index, get_built_features, get_current_work, get_next_work
- **SelfHealingMemory** (class) — 1175
  - Methods: __init__, validate_profile, backup_profile, heal_profile, auto_repair
- **TestMemoryAdvisor** (class) — 1347
  - Methods: test_empty
- **append_memory** (call) — 508
  - Context: DispatcherAgent.process_agent_task
- **build_memory_packet** (call) — 208
  - Context: CoreOrchestrator.process
- **get_memory_summary** (function) — 1165
- **get_weighted_memory** (call) — 1124
  - Context: AttentionMemory.build_attention_context
- **load_memory_index** (call) — 1090
  - Context: ProjectMemoryLoader.get_built_features
- **memory_stats** (call) — 1141
  - Context: MemoryAdvisor.analyze
- **memory_summary** (call) — 405
  - Context: ButlerOSAdapter.full_summary
- **project_memory_summary_text** (call) — 1277
- **rebuild_user_memory** (function) — 1165
- **route_memory** (function) — 1161
- **run_memory_guardian** (function) — 219
- **save_to_memory** (call) — 1346

## MODULE (18 components)
- **_convert_to_module_notation** (call) — 440
  - Context: IntegrationTestGuard.validate
- **frozen_modules** (call) — 474
- **get_frozen_modules** (call) — 405
  - Context: ButlerOSAdapter.frozen_modules
- **get_modules** (call) — 1102
  - Context: ProjectState.modules
- **import_module** (call) — 219
  - Context: check_code_layer
- **module_to_path** (function) — 289
- **modules** (call) — 1088
  - Context: PassportReport.print_components
- **normalize_to_module** (function) — 299

## ORCHESTRATOR (21 components)
- **CoreOrchestrator** (class) — 208
  - Methods: __init__, process, _route
- **LoopOrchestratorV3_EXEC_V2** (class) — 1118
  - Methods: __init__, fingerprint, detect_deadlock, start
- **LoopOrchestratorV3_MASTER_TRUTH** (class) — 1117
  - Methods: __init__, fingerprint, load_state, check_system_integrity, start
- **MainOrchestrator** (class) — 221
  - Methods: __init__, run
- **MemoryOrchestrator** (class) — 1158
  - Methods: __init__, build_context, build_ollama_payload, log_event, debug_dump
- **MemoryOrchestratorV2** (class) — 1159
  - Methods: __init__, build_memory_packet, build_llm_prompt
- **Orchestrator** (class) — 452
  - Methods: __init__, run

## PASSPORT (36 components)
- **PassportCommandHandler** (class) — 453
  - Methods: __init__, handle_command
- **PassportReport** (class) — 1088
  - Methods: __init__, print_header, print_components, print_footer, print_report
- **PassportScanner** (class) — 556
  - Methods: scan
- **ProjectPassportLoader** (class) — 1098
  - Methods: __init__, load_passport, get_identity, get_frozen_modules, get_current_stage...
- **_load_raw_passport** (call) — 1144
  - Context: MemoryFacade.get_unified_context
- **_save_passport** (call) — 1098
  - Context: ProjectPassportLoader.commit_proof
- **get_passport_string** (call) — 453
  - Context: PassportCommandHandler.handle_command
- **load_passport** (call) — 405
  - Context: ButlerOSAdapter.passport_summary
- **passport_summary** (call) — 405
  - Context: ButlerOSAdapter.passport_summary_text

## PIPELINE (9 components)
- **PDFOCRPipeline** (class) — 386
  - Methods: __init__, _sha256, _progress_path, _load_progress, _save_progress...
- **PlannerPipeline** (class) — 276
  - Methods: __init__, run
- **run_pipeline** (function) — 1485

## POLICY (8 components)
- **PolicyLoader** (class) — 296
  - Methods: default_policy
- **PolicyValidator** (class) — 298
  - Methods: validate
- **ScopePolicy** (class) — 562
  - Methods: __init__, _load_scope, is_allowed
- **default_policy** (call) — 296

## PROVIDER (10 components)
- **ContextProvider** (class) — 270
  - Methods: __init__, build_context, _read_json, _read_text

## RECIPE (40 components)
- **Recipe** (class) — 1105
- **RecipeExecutor** (class) — 348
  - Methods: execute
- **RecipeGenerator** (class) — 280
  - Methods: generate
- **RecipeLoader** (class) — 349
  - Methods: load
- **RecipeQueueWatcher** (class) — 350
  - Methods: __init__, pending_recipes, has_work
- **RecipeStep** (class) — 1105
- **RecipeValidator** (class) — 318
  - Methods: __init__, validate, _check_contract, _check_one_of, _resolve_inside_project...
- **RecipeWriter** (class) — 351
  - Methods: write
- **build_planning_recipe** (call) — 261
  - Context: ArchitectAgent.plan
- **completed_recipes** (call) — 293
- **failed_recipes** (call) — 293
- **pending_recipes** (call) — 350
  - Context: RecipeQueueWatcher.has_work

## REFERENCE (3 components)
- **ReferenceResolver** (class) — 1201
  - Methods: __init__, _success, _failure, resolve
- **get_preferences** (call) — 218
  - Context: MemoryCore.build_memory_packet

## REGISTRY (38 components)
- **ExecutionRegistry** (class) — 1138
  - Methods: __init__, load, save, mark_done, is_done
- **HandlerRegistry** (class) — 387
  - Methods: __init__, get_handler
- **PolicyRegistry** (class) — 297
  - Methods: register, get, exists, names
- **RegistryBrain** (class) — 466
  - Methods: __init__, load, save, route, update_department...
- **RegistryLoader** (class) — 1106
  - Methods: __init__, load_registry, get_modules, get_departments, get_services
- **RegistryScanner** (class) — 558
  - Methods: scan
- **RegistryValidator** (class) — 1107
  - Methods: __init__, load_registry, validate
- **RouterRegistry** (class) — 469
  - Methods: __init__, get_target
- **RuntimeCapabilityRegistry** (class) — 320
  - Methods: register, get, exists, names, all...
- **_save_registry** (call) — 1115
  - Context: AgentPlannerV2.complete_task
- **load_execution_registry** (call) — 1168
  - Context: ProjectContextBuilder.build_context
- **load_goals_registry** (call) — 1168
  - Context: ProjectContextBuilder.build_context
- **load_registry** (call) — 1106
  - Context: RegistryLoader.get_modules
- **registry_info** (call) — 1103
  - Context: ProjectState.summary

## RESOLVER (13 components)
- **HybridResolver** (class) — 446
  - Methods: resolve
- **Resolver** (class) — 514
  - Methods: __init__, visit_Call, visit_BinOp

## ROUTER (15 components)
- **ChatRouterMirror** (class) — 419
  - Methods: __init__, route
- **RouterIntegration** (class) — 123
  - Methods: __init__, dispatch
- **SmartRouter** (class) — 1360
  - Methods: detect

## RUNNER (2 components)
- **TaskRunner** (class) — 352
  - Methods: __init__, backup_file, patch_file, rollback_all, execute_step...

## SEARCH (29 components)
- **CatalogSearchBridge** (class) — 1125
  - Methods: __init__, search
- **full_text_search** (call) — 209
  - Context: ButlerDiagnostics.test_fts5_search
- **rebuild_search_index** (call) — 217
  - Context: ButlerMcpServer.handle_request
- **search** (call) — 322
  - Context: SmartDispatcher.determine_role
- **search_by_entity** (call) — 1354
  - Context: run_tests
- **search_by_tag** (call) — 1354
  - Context: run_tests
- **search_by_text** (call) — 324
  - Context: SmartDispatcherV2.dispatch
- **search_event** (call) — 1158
  - Context: MemoryOrchestrator.build_context
- **test_fts5_search** (call) — 209
  - Context: ButlerDiagnostics.run_all
- **update_search_context** (call) — 1125
  - Context: CatalogSearchBridge.search

## SEMANTIC (43 components)
- **SemanticCompressor** (class) — 1176
  - Methods: __init__, compress, compress_for_llm
- **SemanticConstraintLayer** (class) — 1177
  - Methods: __init__, validate
- **SemanticCore** (class) — 1179
  - Methods: __init__, analyze
- **SemanticLayer** (class) — 471
  - Methods: classify
- **SemanticMatch** (class) — 1192
- **SemanticMemory** (class) — 1188
  - Methods: __init__, append, search_by_tags, search_by_text
- **SemanticQueryParser** (class) — 1190
  - Methods: parse
- **SemanticReasoningEngine** (class) — 1192
  - Methods: __init__, normalize, tokens, expand, score...
- **SemanticReasoningEngineV2** (class) — 1197
  - Methods: __init__, load, _neighbors, explain_paths, related...
- **SemanticRelationsEngine** (class) — 1199
  - Methods: __init__, add, outgoing, incoming, neighbours...
- **SemanticSearchEngine** (class) — 1173
  - Methods: __init__, _cache_key, _cache_get, _cache_put, _load_synonyms...

## SERVICE (6 components)
- **ServicesScanner** (class) — 560
  - Methods: __init__, scan

## VALIDATOR (4 components)
- **FeedbackValidatorV2** (class) — 1115
  - Methods: __init__, validate_file_syntax
- **LocalFeedbackValidatorV2** (class) — 1117
  - Methods: __init__, validate_file_syntax
- **SecurityValidator** (class) — 359
  - Methods: validate

## WORKFLOW (1 components)
- **get_workflow** (call) — 1351

## ALREADY IMPLEMENTED
The following semantic categories are already present in the project:
- adapter
- agent
- analyzer
- auditor
- bridge
- builder
- capability
- catalog
- context
- department
- dependency
- dispatcher
- engine
- execution
- graph
- guardian
- history
- manager
- manifest
- memory
- module
- orchestrator
- passport
- pipeline
- policy
- provider
- recipe
- reference
- registry
- resolver
- router
- runner
- search
- semantic
- service
- validator
- workflow

## DO NOT BUILD AGAIN
Do not rebuild any of the following categories or their components:
- adapter (components: ButlerOSAdapter, ProfessorAdapter, adapter_class, ButlerOSAdapter, ButlerOSAdapter, ProfessorAdapter, ButlerOSAdapter)
- agent (components: ArchitectAgent, AgentPlanner, AgentRouter, AgentRouter, DispatcherAgent, EngineeringAgent, ExecutionRegistryDiscoveryAgent, GoalsRegistryDiscoveryAgent, PassportDiscoveryAgent, ProjectStateDiscoveryAgent...)
- analyzer (components: DependencyAnalyzer, GoalAnalyzer, VisionAnalyzer, GoalAnalyzer, DependencyAnalyzer, GoalAnalyzer, DependencyAnalyzer, DependencyAnalyzer, GoalAnalyzer, DependencyAnalyzer...)
- auditor (components: ProjectAuditor, TestProjectAuditor, ProjectAuditor)
- bridge (components: ChatCoreBridge, ToolBridge, ToolBridge, ComfyUIBridge, FactoryCoreBridge, ToolBridge, ComfyUIBridge, ComfyUIBridge, FactoryCoreBridge)
- builder (components: RecipeBuilder, TaskContractBuilder, RecipeBuilder, ButlerContextBuilder, ProjectContextBuilder, ProjectContextBuilder, RecipeBuilder, TaskContractBuilder, TaskContractBuilder, TaskContractBuilder...)
- capability (components: RuntimeCapability, RuntimeCapability, RuntimeCapability)
- catalog (components: test_catalog_update, test_catalog_update, EngineeringObjectCatalog, EngineeringObjectCatalog, show_catalog, test_catalog_update, test_catalog_update, EngineeringObjectCatalog, EngineeringObjectCatalog, EngineeringObjectCatalog...)
- context (components: build_minimal_context, build_context, build_context, build_context, build_context, build_context, build_context, build_context, build_context, build_context...)
- department (components: ArchiveDepartment, AudioDepartment, BaseDepartment, CodingDepartment, DocumentsDepartment, DocumentsDepartment, ImageDepartment, MemoryDepartment, OpenDocumentDepartment, RuntimeDepartmentsDiscoveryAgent...)
- dependency (components: DependencyClosure, DependencyClosure, DependencyClosure)
- dispatcher (components: FakeDispatcher, SmartDispatcher, SmartDispatcherV2, SmartDispatcherV2, Dispatcher, DispatcherBridge, DreamDispatcherAdapter, DispatcherScanner, DispatcherScanner, SmartDispatcherV2...)
- engine (components: PlannerDecisionEngine, PlannerEngine, VisionEngine, ConversationContextEngine, EngineeringEvidence, EngineeringEvidenceCollection, EngineeringObject, EngineeringObjectIdentifier, EngineeringObjectRelationship, EngineeringPipeline...)
- execution (components: ExecutionLoop, ExecutionHistory, ExecutionMonitor, ExecutionState, ExecutionResult, BaseExecutionAdapter, PowerShellExecutionAdapter, PythonExecutionAdapter, ExecutionScanner, ExecutionScanner...)
- graph (components: DependencyGraph, DependencyGraph, DependencyGraph, DependencyGraph, _build_checkpoint_graph, _build_checkpoint_graph)
- guardian (components: run_guardian, run_guardian)
- history (components: HistoryScanner, HistoryScanner, ProjectHistory, ProjectHistory, HistoryScanner, ProjectHistory, HistoryScanner, HistoryScanner, ProjectHistory, HistoryScanner...)
- manager (components: QueueManager, CatalogManager, ButlerDreamManager, MemoryManager, ProviderManager, QueueManager, ButlerSessionManager, CatalogManager, MemoryManager, ProviderManager...)
- manifest (components: load_manifest, ManifestLoader, verify_lock_manifest, rebuild_lock_manifest, load_manifest, ManifestLoader, load_manifest, verify_lock_manifest, rebuild_lock_manifest, rebuild_lock_manifest...)
- memory (components: MemoryCore, run_memory_guardian, MemoryLoop, MemorySidecar, MemoryAdvisor, ProjectMemoryLoader, ExecutionMemoryV2, AttentionMemory, MemoryAdvisor, MemoryFacade...)
- module (components: module_to_path, normalize_to_module, import_module, import_module, module_to_path, normalize_to_module, get_frozen_modules, _convert_to_module_notation, frozen_modules, modules...)
- orchestrator (components: CoreOrchestrator, MainOrchestrator, MainOrchestrator, Orchestrator, LoopOrchestratorV3_MASTER_TRUTH, LoopOrchestratorV3_EXEC_V2, MemoryOrchestrator, MemoryOrchestratorV2, CoreOrchestrator, Orchestrator...)
- passport (components: PassportCommandHandler, PassportScanner, PassportScanner, PassportReport, ProjectPassportLoader, PassportCommandHandler, ProjectPassportLoader, ProjectPassportLoader, load_passport, passport_summary...)
- pipeline (components: PlannerPipeline, PDFOCRPipeline, run_pipeline, run_pipeline, PlannerPipeline, PlannerPipeline, PDFOCRPipeline, run_pipeline, run_pipeline)
- policy (components: PolicyLoader, PolicyValidator, ScopePolicy, default_policy, default_policy, default_policy, ScopePolicy, default_policy)
- provider (components: ContextProvider, ContextProvider, ContextProvider, ContextProvider, ContextProvider, ContextProvider, ContextProvider, ContextProvider, ContextProvider, ContextProvider)
- recipe (components: RecipeGenerator, RecipeGenerator, RecipeValidator, RecipeExecutor, RecipeLoader, RecipeQueueWatcher, RecipeWriter, RecipeStep, Recipe, build_planning_recipe...)
- reference (components: ReferenceResolver, get_preferences, ReferenceResolver)
- registry (components: PolicyRegistry, RuntimeCapabilityRegistry, HandlerRegistry, RegistryBrain, RouterRegistry, RouterRegistry, RegistryScanner, RegistryScanner, RegistryLoader, RegistryValidator...)
- resolver (components: HybridResolver, Resolver, Resolver, Resolver, Resolver, HybridResolver, HybridResolver, HybridResolver, HybridResolver, Resolver...)
- router (components: RouterIntegration, ChatRouterMirror, RouterIntegration, RouterIntegration, SmartRouter, RouterIntegration, RouterIntegration, RouterIntegration, ChatRouterMirror, RouterIntegration...)
- runner (components: TaskRunner, TaskRunner)
- search (components: CatalogSearchBridge, full_text_search, test_fts5_search, full_text_search, rebuild_search_index, full_text_search, full_text_search, test_fts5_search, full_text_search, rebuild_search_index...)
- semantic (components: SemanticLayer, SemanticSearchEngine, SemanticCompressor, SemanticConstraintLayer, SemanticCore, SemanticMemory, SemanticQueryParser, SemanticMatch, SemanticReasoningEngine, SemanticReasoningEngineV2...)
- service (components: ServicesScanner, ServicesScanner, ServicesScanner, ServicesScanner, ServicesScanner, ServicesScanner)
- validator (components: SecurityValidator, FeedbackValidatorV2, LocalFeedbackValidatorV2, LocalFeedbackValidatorV2)
- workflow (components: get_workflow)
