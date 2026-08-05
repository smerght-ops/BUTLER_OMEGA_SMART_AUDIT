# Butler Omega Smart — Active Production System

Главный источник истины: `A_00_ARCHITECTURE/PRODUCTION_ARCHITECTURE.json`.

## Runtime

`START_BUTLER_OS.ps1 → BUTLER_OS.py → AgentCoreCoordinator → dispatcher_bridge_v2 → SmartDispatcherV2 → ButlerHarness → DepartmentExecutionGateway → PermissionEngine → Department`

Остановка: `STOP_BUTLER_OS.ps1`, только по session-owned PID из
`A_08_LOGS/runtime/active_session.json`.

## Production ownership

- Dispatcher: `SmartDispatcherV2`.
- Chat/model provider lifecycle: `A_02_MANAGERS.smart_dispatcher.get_chat_provider` (`ACTIVE_SUPPORT`).
- Department table: `A_02_MANAGERS/department_registry.py`.
- Memory coordinator lifecycle: `A_07_MEMORY.memory_orchestrator_v2.get_memory_orchestrator`.
- Project Knowledge: `RepositoryKnowledgeDepartment` через `repository_knowledge_gateway`.
- Engineering gate: `Run-EngineeringReview.ps1 -Full -Detailed`.
- Runtime contract: `RUNTIME_CONTRACT.json`.
- Memory contract: `MEMORY_CONTRACT.json`.

Старые launcher и `chat_router*` физически изолированы в `A_00_LEGACY_ARCHIVE/production_cleanup_tz4`.

Единая production-команда тестирования: `python -m pytest -c pytest.ini`.
`A_10_BUTLER_OS` имеет статус `ACTIVE_SUPPORT`, а не отдельного runtime.
