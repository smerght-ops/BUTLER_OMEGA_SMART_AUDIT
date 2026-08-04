# Memory Contract Report

`MemoryOrchestratorV2` является единственным production-координатором памяти.
`MemoryDepartment` предоставляет пользовательский Department API и выполняет операции через
orchestrator. `MemoryFacadeV2` остаётся владельцем storage primitives внутри orchestrator,
но не маршрутизируется самостоятельно.

DKI использует утверждённый model-provider `SmartDispatcher.execute_employee` и больше не
импортирует legacy `chat_router`. Архитектурный граф является специализированным RKD consumer
и не сканирует дерево проекта самостоятельно.

Формальная таблица ownership находится в `MEMORY_CONTRACT.json`.
