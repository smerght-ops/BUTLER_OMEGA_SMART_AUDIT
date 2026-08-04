# Runtime Contract Report

Статус: `ACTIVE_PRODUCTION`
Контракт: `A_00_ARCHITECTURE/RUNTIME_CONTRACT.json`

Официальный запуск выполняет `START_BUTLER_OS.ps1`. Он разрешает канонический Python,
создаёт уникальный session state, регистрирует только действительно созданные им процессы
`RunnerLoop` и `BUTLER_OS.py`, а затем ожидает завершения Butler OS.

Официальная остановка выполняется `STOP_BUTLER_OS.ps1`. Она читает только state текущей
сессии, проверяет PID, command token и признак ownership. Внешние Ollama и ComfyUI
классифицируются как `EXTERNAL_PREEXISTING` либо `UNAVAILABLE`; Butler их не запускает
и не завершает.

Подтверждённая цепочка:

`START_BUTLER_OS.ps1 → BUTLER_OS.py → AgentCoreCoordinator → dispatcher_bridge_v2 → SmartDispatcherV2 → ButlerHarness → DepartmentExecutionGateway → PermissionEngine → Department`

Альтернативные launcher имеют явные статусы в JSON-контракте и не являются production entry point.
