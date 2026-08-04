# Butler Runtime Contract Report

Generated: 2026-08-04 (Europe/Moscow)

Contract: `butler.runtime-contract.v1`

## ENTRY POINT

Status: **AMBIGUOUS_RUNTIME**.

The requested `START_BUTLER_OS.ps1` route is executable: launcher line 123 starts `A_02_MANAGERS.TaskRunner.runner_loop`, and line 132 invokes `BUTLER_OS.py`. This proves that route exists; it does not prove exclusivity.

Competing executable launchers were also found:

- `START_BUTLER.ps1:33` invokes `A_03_ORCHESTRATION/chat_router.py`.
- `START_BUTLER_FULL.ps1:45` invokes `A_03_ORCHESTRATION/chat_router.py`.
- `START_BUTLER_RUNTIME_DIAGNOSTIC.bat:131` invokes `BUTLER_OS.py` without the canonical PowerShell launcher.
- `START_SAFE_LAUNCH.py:15-27` starts `task_feeder.py`, `execution_loop.py`, and `flow_monitor.py` as a separate implementation.
- `START_BUTLER_CORE.py:81-82` constructs and runs `BootstrapCore`/`ExecutionLoop`.
- `START_BUTLER_SYSTEM.py:66-67` constructs and runs `ButlerSystem`/`ExecutionLoop`.

No runtime trace, process provenance record, or enforced launcher selection in the repository proves that only one of these is the production entry point. None was automatically selected.

## RUNTIME TRACE — BUTLER_OS CANDIDATE

`START_BUTLER_OS.ps1:132` → `BUTLER_OS.py:29` (`_agent_core = AgentCoreCoordinator(...)`) → `AgentCoreCoordinator._dispatch_tool_call`, line 433 (`self.department_dispatch(...)`) → `dispatcher_bridge_v2.dispatch`, line 34 (`_dispatcher.dispatch(...)`) → `SmartDispatcherV2._execute_department`, lines 175-188 → `ButlerHarness.execute`, line 44 → `DepartmentExecutionGateway.execute`, line 64 → selected `Department.execute`.

Evidence source: launcher commands, Python AST imports/assignments/calls, and the static import graph. `BUTLER_OS.py:6` imports the bridge callback; lines 29-33 pass it to `AgentCoreCoordinator`; line 98 calls `_agent_core.execute`; line 102 calls the same bridge in the `AgentCoreUnavailable` branch. This proves convergence inside the BUTLER_OS implementation only.

## COMPETING RUNTIME TRACE — CHAT ROUTER

`START_BUTLER.ps1:33` or `START_BUTLER_FULL.ps1:45` → `A_03_ORCHESTRATION/chat_router.py:241` (`main`) → line 274 (`router_bus.dispatch`). A separate conditional image branch imports `dispatcher_bridge_v2`, `DepartmentExecutionGateway`, and `ImageDepartment` at lines 157-164 and invokes the gateway directly.

Evidence source: launcher commands and Python AST calls. This chain is structurally different from the BUTLER_OS coordinator/dispatcher chain and is therefore marked **MULTIPLE_IMPLEMENTATIONS**.

## DISPATCHER

Class `SmartDispatcherV2` is defined at `A_02_MANAGERS/smart_dispatcher_v2.py:35`, imported by `A_03_ORCHESTRATION/dispatcher_bridge_v2.py:3`, instantiated at line 7, and called at line 34. Status for the BUTLER_OS candidate: **PASS**. This is not evidence that every competing launcher uses it.

Dispatcher registration is its actual runtime list. `GoalManager` is also in that routable list but is a Manager, not a Department, and is therefore not represented as a Department row.

## GATEWAY

Class `DepartmentExecutionGateway` is defined at `A_03_ORCHESTRATION/permission/gateway.py:38`; method `execute` is at line 64. `SmartDispatcherV2._execute_department` calls it at lines 184 and 186 from the executor passed to `ButlerHarness.execute` at line 188. Status for this call path: **PASS**.

## PERMISSION

Class `PermissionEngine` is defined at `A_03_ORCHESTRATION/permission/engine.py:6`. `DepartmentExecutionGateway.__init__` constructs it at `permission/gateway.py:42`. Evidence source: Python AST class, import, and constructor call. Status: **PASS**.

## COORDINATOR

Class `AgentCoreCoordinator` is defined at `A_03_ORCHESTRATION/agent_core_coordinator.py:199`. `BUTLER_OS.py:29-33` constructs it and passes the imported `dispatch` callback; coordinator line 208 stores that callback and line 433 invokes it. Evidence source: Python AST assignment and call graph. Status for the BUTLER_OS candidate: **PASS**.

## RUNTIME SERVICES

- `MemoryOrchestratorV2`: active in the coordinator and dispatcher context paths.
- Voice Interface: conditional active input path from `BUTLER_OS.py`.
- `RunnerLoop`: launcher-managed companion process.
- `CapabilityExecutor` and the top-level `TaskExecutor` are imported and instantiated in `BUTLER_OS.py`, but no call from that module was found. They are loaded, not proven active services on the canonical chain. The dispatcher has its own active `TaskExecutor`.

## DEPARTMENTS

| Department | runner | registered | dispatcher | status |
|---|---|---:|---:|---|
| Archive | runner.py | yes | yes | ACTIVE |
| Audio | runner.py | yes | yes | ACTIVE |
| Bionic | missing | no | no | INCOMPLETE |
| Browser | runner.py | no | yes | ACTIVE_REGISTRY_MISMATCH |
| Chat | missing | no | no | INCOMPLETE |
| Coding | runner.py | yes | yes | ACTIVE |
| Documents | runner.py | no | yes | ACTIVE_REGISTRY_MISMATCH |
| EngineeringReview | runner.py | yes | yes | ACTIVE |
| External | missing | no | no | INCOMPLETE |
| Filesystem | runner.py | no | yes | ACTIVE_REGISTRY_MISMATCH |
| GitPublishGuardian | missing | no | no | INCOMPLETE |
| Home | runner.py | no | yes | ACTIVE_REGISTRY_MISMATCH |
| Image | runner.py | yes | yes | ACTIVE |
| Memory | runner.py | yes | yes | ACTIVE |
| OCR | missing | no | no | INCOMPLETE |
| OpenDocument | runner.py | no | yes | ACTIVE_REGISTRY_MISMATCH |
| ProjectDocumentation | runner.py | no | yes | ACTIVE_REGISTRY_MISMATCH |
| PublicationGuardian | runner.py | no | yes | ACTIVE_REGISTRY_MISMATCH |
| RepositoryKnowledge | runner.py | yes | yes | ACTIVE |
| Search | runner.py | no | yes | ACTIVE_REGISTRY_MISMATCH |
| Text | runner.py | yes | yes | ACTIVE |
| Video | runner.py | yes | yes | ACTIVE |
| Vision | runner.py | yes | yes | ACTIVE |
| Voice | missing | no | no | INCOMPLETE |

Evidence sources for the table:

- runner existence: exact `A_04_AGENTS/<Department>/runner.py` path checks;
- dispatcher import graph: `smart_dispatcher_v2.py:6-24`;
- dispatcher instances: `SmartDispatcherV2.__init__`, lines 49-70;
- registry entries: `department_registry.py:5-14`;
- missing runner/registration status: absence from those exact path/import/registry sets, not an inference from the component name.

Missing runners and registrations were only reported, not repaired.

## RKD INTEGRATION EVIDENCE

The approved boundary is implemented by `A_03_ORCHESTRATION/repository_knowledge_gateway.py`: line 5 imports `DepartmentExecutionGateway`, line 6 imports the public `RepositoryKnowledgeDepartment`, function `query_repository` begins at line 13, constructs the Department at line 15, and invokes the gateway at line 16. Lines 28 and 31 raise the diagnostic `RKD_UNAVAILABLE` contract; there is no fallback scan in this function.

Consumer evidence:

- `ast_parser.py:11,60` — imports and calls `list_repository_files`.
- `config_scanner.py:11,38` — imports and calls `list_repository_files`.
- `structural_extractor.py:12,91` — imports and calls `list_repository_files`.
- `ast_call_parser.py:12,88` — imports and calls `list_repository_files`.
- `ast_path_resolver.py:12,55` — imports and calls `list_repository_files`.
- `project_indexer.py:5,75` — imports `query_repository` and requests `get_index`.

AST verification found no `RepositoryKnowledgeService`/`QueryEngine` import, `os.walk` call, or `Path.rglob` call in those six files. The dependency direction is proven by imports: `project_indexer.py:5 → repository_knowledge_gateway.py:5-6 → RepositoryKnowledgeDepartment`; recursive search of RKD Python sources found no import or reference to `project_indexer`.

## DOCUMENT STATUS

**DOCUMENT_OUTDATED.** `A_00_ARCHITECTURE/ACTIVE_SYSTEM.md` names `chat_router.py` as the entry point and omits the launcher, `BUTLER_OS.py`, coordinator, bridge, harness, gateway, and permission stage. It also lists only eight active Departments. The file was not changed.

## REGISTRY STATUS

**REGISTRY_OUTDATED.** `department_registry.py` omits active dispatcher Departments: Browser, Documents, Filesystem, Home, OpenDocument, ProjectDocumentation, PublicationGuardian, and Search. It also contains `CHAT` and `ROUTER` placeholders not represented by Department runners. The file was not changed.

## DISPATCHER VALIDATION

**FAIL (metadata consistency only).** The dispatcher uses instantiated/imported runtime components, but eight active Departments are absent from `department_registry.py`; therefore “dispatcher uses only registry-listed Departments” is false. No runtime registration was changed.

## RUNTIME STATUS

**AMBIGUOUS_RUNTIME / MULTIPLE_IMPLEMENTATIONS.** The BUTLER_OS chain is proven to exist and is structurally traceable, but exclusivity as the single production chain is not proven. Competing executable launcher implementations are listed above. A later architectural decision or runtime provenance trace is required before `START_BUTLER_OS.ps1` can be declared the exclusive canonical entry point.
