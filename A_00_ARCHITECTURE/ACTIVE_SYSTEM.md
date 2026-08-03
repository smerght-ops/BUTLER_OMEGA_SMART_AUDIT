# BUTLER OMEGA SMART - ACTIVE SYSTEM

ENTRY POINT
A_03_ORCHESTRATION/chat_router.py

MAIN DISPATCHER
A_02_MANAGERS/smart_dispatcher_v2.py

ACTIVE DEPARTMENTS
- CodingDepartment
- ImageDepartment
- VisionDepartment
- TextDepartment
- MemoryDepartment
- VideoDepartment
- AudioDepartment
- ArchiveDepartment

ACTIVE MEMORY
A_07_MEMORY

ACTIVE PROVIDER
A_02_MANAGERS/provider_manager.py

ACTIVE ORCHESTRATION
A_03_ORCHESTRATION

LEGACY COMPONENTS
- A_04_AGENTS/professor.py
- A_04_AGENTS/run_professor_daemon.py
- A_02_MANAGERS/smart_dispatcher.py
- A_02_MANAGERS/dream_manager.py

RULE
Все новые изменения вносятся только через:
chat_router.py
→ smart_dispatcher_v2.py
→ Department
→ provider_manager.py
