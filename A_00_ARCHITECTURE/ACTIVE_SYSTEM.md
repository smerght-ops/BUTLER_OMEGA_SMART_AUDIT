# Butler Omega Smart — Active Production System

Главный источник истины: `A_00_ARCHITECTURE/PRODUCTION_ARCHITECTURE.json`.

## Runtime

`START_BUTLER_OS.ps1 → BUTLER_OS.py → AgentCoreCoordinator → dispatcher_bridge_v2 → SmartDispatcherV2 → ButlerHarness → DepartmentExecutionGateway → PermissionEngine → Department`

Остановка: `STOP_BUTLER_OS.ps1`, только по session-owned PID из
`A_08_LOGS/runtime/active_session.json`.

## Production ownership

- Dispatcher: `SmartDispatcherV2`.
- Chat/model provider: `A_02_MANAGERS.smart_dispatcher.SmartDispatcher` (`ACTIVE_SUPPORT`).
- Department table: `A_02_MANAGERS/department_registry.py`.
- Memory coordinator: `MemoryOrchestratorV2`.
- Project Knowledge: `RepositoryKnowledgeDepartment` через `repository_knowledge_gateway`.
- Engineering gate: `Run-EngineeringReview.ps1 -Full -Detailed`.
- Runtime contract: `RUNTIME_CONTRACT.json`.
- Memory contract: `MEMORY_CONTRACT.json`.

`chat_router.py` имеет статус `LEGACY` и не является production entry point.
`A_10_BUTLER_OS` имеет статус `ACTIVE_SUPPORT`, а не отдельного runtime.
