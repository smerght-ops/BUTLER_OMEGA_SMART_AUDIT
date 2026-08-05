# Butler Omega Smart Production Architecture

Этот документ и JSON-контракт с тем же именем являются главным описанием действующей системы.

## Runtime

`START_BUTLER_OS.ps1 → BUTLER_OS.py → AgentCoreCoordinator → dispatcher_bridge_v2 → SmartDispatcherV2 → ButlerHarness → DepartmentExecutionGateway → PermissionEngine → Department`

Остановка выполняется `STOP_BUTLER_OS.ps1` исключительно по session ownership.
Ollama и ComfyUI считаются внешними сервисами и не завершаются Butler.

## Components

- Каноническая таблица Department: `A_02_MANAGERS/department_registry.py`.
- `GoalManager`: Manager, не Department.
- `SmartDispatcher`: активный supporting chat/model provider, не основной Dispatcher.
- Память: `MemoryOrchestratorV2`, контракт `MEMORY_CONTRACT.json`.
- Project Knowledge: RKD через gateway; вторые production scanner запрещены.
- Engineering gate: `Run-EngineeringReview.ps1 -Full -Detailed`.

## Boundaries

Старые `chat_router*` и launcher физически изолированы в `A_00_LEGACY_ARCHIVE/production_cleanup_tz4`; `professor.py` классифицирован как legacy и не входит
в официальную цепочку. Диагностические Inspector не являются production index.
