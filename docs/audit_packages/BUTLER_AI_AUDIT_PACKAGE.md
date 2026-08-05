# BUTLER OMEGA SMART — AI ARCHITECTURE AUDIT PACKAGE

Собрано: 2026-07-13 11:59:47
Корень проекта: C:\Users\KOS\Desktop\Butler_Agent\BUTLER_OMEGA_SMART

---

# MASTER PROJECT CONTEXT

Источник: `C:\Users\KOS\Desktop\Butler_Agent\BUTLER_OMEGA_SMART\MASTER_PROJECT_CONTEXT.md`

``md

``

---

# НАЗНАЧЕНИЕ BUTLER

Источник: `C:\Users\KOS\Desktop\Butler_Agent\BUTLER_OMEGA_SMART\НАЗНАЧЕНИЕ_BUTLER.md`

``md
# НАЗНАЧЕНИЕ BUTLER OMEGA SMART

## Статус документа

Этот документ определяет главную цель существования проекта Butler Omega Smart.

Документ является основой для всех архитектурных решений, Roadmap, паспортов проекта и последующих этапов разработки.

При возникновении любых сомнений в направлении развития проекта приоритет имеет данный документ.

---

# Главная цель проекта

Butler Omega Smart создаётся как локальная персональная многоагентная интеллектуальная система, предназначенная для помощи человеку и семье в повседневной жизни, организации информации, хранении знаний, автоматизации задач и безопасном выполнении действий.

Многоагентная архитектура является способом реализации этой цели, а не целью сама по себе.

Главная задача Butler — стать единым цифровым помощником семьи.

---

# Основные функции Butler

Butler должен:

- знать членов семьи и учитывать их контекст;
- хранить семейные документы, фотографии, видео и историю;
- помнить дни рождения, платежи, сроки и важные события;
- следить за автомобилями, страховками, ремонтами и техническим обслуживанием;
- помогать со здоровьем, медицинскими документами и справками;
- учитывать покупки, чеки, домашние запасы и продукты;
- предлагать рецепты и формировать список покупок;
- работать с письмами, договорами, счетами, PDF-документами, изображениями и таблицами;
- выполнять OCR и анализ документов;
- выполнять инженерные расчёты, расчёты материалов и смет;
- создавать документы, таблицы, изображения, инструкции, скрипты и небольшие программы;
- помогать в разработке программного обеспечения;
- наводить порядок в файлах, цифровом архиве и рабочем пространстве;
- выполнять действия через специализированные отделы и инструменты;
- сохранять долговременную память и объяснять ранее принятые решения;
- работать преимущественно локально;
- обеспечивать безопасность, проверяемость, подтверждение действий человеком и возможность отката.

---

# Архитектурные принципы

При разработке Butler должны соблюдаться следующие принципы:

- локальная работа является приоритетной;
- безопасность важнее скорости разработки;
- каждое действие должно быть проверяемым;
- предпочтение отдаётся фактам, а не предположениям;
- архитектура должна быть модульной;
- память должна быть долговременной и объяснимой;
- изменения должны быть обратимыми;
- новые возможности не должны разрушать существующую архитектуру;
- человек остаётся главным принимающим решения.

---

# Что не является целью проекта

Butler не создаётся как:

- обычный чат-бот;
- генератор текста;
- отдельный AI-агент;
- только система поиска;
- только RAG;
- только средство генерации кода.

Все эти возможности являются лишь отдельными функциями единой системы.

---

# Критерий успешного развития

Любое новое изменение проекта должно отвечать на вопрос:

**Приближает ли данная возможность Butler к его главной цели — быть единым локальным цифровым помощником семьи?**

Если ответ отрицательный, необходимость такой функции должна быть дополнительно обоснована.

---

# Статус

Документ создан на основании исторических архитектурных материалов проекта, манифестов, паспортов, исследований и восстановленного замысла Butler Omega Smart.

Данный документ является отправной точкой для последующего аудита текущего состояния проекта и формирования новой Roadmap развития.


``

---

# ОПЕРАЦИОННАЯ ФИЛОСОФИЯ

Источник: `C:\Users\KOS\Desktop\Butler_Agent\BUTLER_OMEGA_SMART\BUTLER_OPERATING_PHILOSOPHY.md`

``md
# НАЗНАЧЕНИЕ BUTLER OMEGA SMART

## Статус документа

Этот документ определяет главную цель существования проекта Butler Omega Smart.

Документ является основой для всех архитектурных решений, Roadmap, паспортов проекта и последующих этапов разработки.

При возникновении любых сомнений в направлении развития проекта приоритет имеет данный документ.

---

# Главная цель проекта

Butler Omega Smart создаётся как локальная персональная многоагентная интеллектуальная система, предназначенная для помощи человеку и семье в повседневной жизни, организации информации, хранении знаний, автоматизации задач и безопасном выполнении действий.

Многоагентная архитектура является способом реализации этой цели, а не целью сама по себе.

Главная задача Butler — стать единым цифровым помощником семьи.

---

# Основные функции Butler

Butler должен:

- знать членов семьи и учитывать их контекст;
- хранить семейные документы, фотографии, видео и историю;
- помнить дни рождения, платежи, сроки и важные события;
- следить за автомобилями, страховками, ремонтами и техническим обслуживанием;
- помогать со здоровьем, медицинскими документами и справками;
- учитывать покупки, чеки, домашние запасы и продукты;
- предлагать рецепты и формировать список покупок;
- работать с письмами, договорами, счетами, PDF-документами, изображениями и таблицами;
- выполнять OCR и анализ документов;
- выполнять инженерные расчёты, расчёты материалов и смет;
- создавать документы, таблицы, изображения, инструкции, скрипты и небольшие программы;
- помогать в разработке программного обеспечения;
- наводить порядок в файлах, цифровом архиве и рабочем пространстве;
- выполнять действия через специализированные отделы и инструменты;
- сохранять долговременную память и объяснять ранее принятые решения;
- работать преимущественно локально;
- обеспечивать безопасность, проверяемость, подтверждение действий человеком и возможность отката.

---

# Архитектурные принципы

При разработке Butler должны соблюдаться следующие принципы:

- локальная работа является приоритетной;
- безопасность важнее скорости разработки;
- каждое действие должно быть проверяемым;
- предпочтение отдаётся фактам, а не предположениям;
- архитектура должна быть модульной;
- память должна быть долговременной и объяснимой;
- изменения должны быть обратимыми;
- новые возможности не должны разрушать существующую архитектуру;
- человек остаётся главным принимающим решения.

---

# Что не является целью проекта

Butler не создаётся как:

- обычный чат-бот;
- генератор текста;
- отдельный AI-агент;
- только система поиска;
- только RAG;
- только средство генерации кода.

Все эти возможности являются лишь отдельными функциями единой системы.

---

# Критерий успешного развития

Любое новое изменение проекта должно отвечать на вопрос:

**Приближает ли данная возможность Butler к его главной цели — быть единым локальным цифровым помощником семьи?**

Если ответ отрицательный, необходимость такой функции должна быть дополнительно обоснована.

---

# Статус

Документ создан на основании исторических архитектурных материалов проекта, манифестов, паспортов, исследований и восстановленного замысла Butler Omega Smart.

Данный документ является отправной точкой для последующего аудита текущего состояния проекта и формирования новой Roadmap развития.


``

---

# ROADMAP

Источник: `C:\Users\KOS\Desktop\Butler_Agent\BUTLER_OMEGA_SMART\ROADMAP_6_0_BUTLER_OMEGA_SMART_UPDATED.md`

``md
# BUTLER OMEGA SMART

# ROADMAP 6.0

## От инженерной платформы к автономному локальному дворецкому

## GLOBAL LAWS

LAW 01 --- Local First Любая задача сначала решается локально.

LAW 02 --- Human Confirmation Любые потенциально опасные действия
требуют подтверждения владельца.

LAW 03 --- Minimal Disclosure Во внешний сервис передается только
минимально необходимый объем данных.

LAW 04 --- Immutable Core Замороженные части проекта изменяются только
при критических исправлениях.

LAW 05 --- Proof Before Action Любое изменение должно подтверждаться
фактами, а не предположениями.

LAW 06 --- Semantic Consistency Семантические выводы не могут
противоречить архитектуре проекта, манифесту или уже известным фактам.

------------------------------------------------------------------------

## ЭТАП 0 --- FOUNDATION

Статус: COMPLETED / FROZEN

Входит: - Butler OS - SmartDispatcherV2 - Department Architecture -
Department Registry - Project Documentation Department - Engineering
Pipeline - Evidence Builder - EvidenceDoctor - Scope Loader - Project
Passport - Ledger - Status Center - Safe Actions - Cloud Audit - Local
First Architecture

После закрытия этапа --- только исправление ошибок.

------------------------------------------------------------------------

## ЭТАП 1 --- SEMANTIC REASONING ENGINE

Цель: научить Butler понимать смысл.

1.1 Semantic Search\
Поиск по смыслу, а не по словам.

1.2 Semantic Relations\
Понимание связей между объектами.

1.3 Knowledge Graph\
Построение графа знаний проекта.

1.4 Semantic Memory\
Хранение смысловых связей.

1.5 Semantic Constraint Layer\
Контроль логической непротиворечивости. Butler соблюдает архитектурные
ограничения, законы проекта, манифест и Local First.

1.6 Architectural Knowledge Graph\
Butler понимает собственную архитектуру и отвечает на вопросы по
реальным зависимостям графа.

Результат: Butler начинает понимать смысл, связи и собственную
архитектуру.

------------------------------------------------------------------------

## ЭТАП 2 --- MEMORY BRAIN

Цель: создать долговременную память Butler.

2.1 Project Memory\
История разработки.

2.2 User Memory\
Предпочтения пользователя.

2.3 Long-Term Memory\
Память на годы.

2.4 Memory Replay\
Восстановление любого состояния проекта.

2.5 Memory Compression\
Сжатие истории без потери смысла.

2.6 Memory Timeline\
Хронология событий.

2.7 Context Builder\
Автоматическое построение контекста перед выполнением задачи.

Результат: Butler перестает забывать.

------------------------------------------------------------------------

## ЭТАП 3 --- GOAL PLANNER

Цель: научить Butler самостоятельно управлять задачами.

3.1 Goal Manager\
Главные цели.

3.2 Planner\
Автоматическое построение плана.

3.3 Progress Tracker\
Контроль выполнения.

3.4 Priority Engine\
Приоритеты.

3.5 Reminder Engine\
Напоминания.

3.6 Dependency Engine\
Зависимости между задачами.

3.7 Auto Checklist\
Автоматическая декомпозиция больших задач.

3.8 Feedback Loop / Self-Correction\
Если задача выполнена плохо, Butler анализирует причину и перестраивает
план.

Результат: Butler становится адаптивным планировщиком.

------------------------------------------------------------------------

## ЭТАП 3.x --- AUTONOMOUS EXECUTION PLATFORM

Статус: COMPLETED / FROZEN

Назначение: Создать детерминированный протокол исполнения между
Планировщиком и Исполнителем.

Входит: - Recipe Schema v1.0 - Recipe Generator - Universal Recipe
Validator - Butler Gate - Deterministic Execution Pipeline

Архитектура:

Planner ↓ Recipe ↓ Recipe Schema ↓ Recipe Validator ↓ Butler Gate ↓
TaskRunner

После закрытия этапа изменяется только при исправлении критических
ошибок.

------------------------------------------------------------------------

## ЭТАП 3.2+ --- ARCHITECT AGENT

Назначение: Создать интеллектуальный слой, который преобразует цели в
рецепты, не вмешиваясь напрямую в исполнительный контур.

Структура:

A_02_MANAGERS/ ArchitectAgent/ **init**.py architect_agent.py
context_provider.py goal_analyzer.py dependency_analyzer.py
recipe_builder.py queue_manager.py

Ответственность модулей:

-   context_provider.py --- формирует снимок состояния проекта.
-   goal_analyzer.py --- анализирует цели и определяет необходимые
    изменения.
-   dependency_analyzer.py --- строит зависимости между изменяемыми
    объектами.
-   recipe_builder.py --- создаёт Recipe v1.0.
-   queue_manager.py --- управляет очередью рецептов.
-   architect_agent.py --- координирует работу всех компонентов.

Architect Agent не имеет права: - изменять файлы проекта; - запускать
TaskRunner; - обходить Butler Gate; - выполнять команды напрямую.

Единственный результат его работы --- корректный Recipe v1.0.

------------------------------------------------------------------------

## ЭТАП 3.y — QUALITY ASSURANCE PLATFORM

------------------------------------------------------------------------

## ЭТАП 4 --- DESKTOP AGENT

Цель: сделать Butler полноценным агентом Windows.

4.1 File Manager\
Файлы.

4.2 Folder Manager\
Папки.

4.3 Archive Manager\
Архив.

4.4 Desktop Organizer\
Рабочий стол.

4.5 Document Manager\
PDF, Word, Excel, фото, видео.

4.6 OCR Agent\
Распознавание документов.

4.7 Windows Automation\
PowerShell, Python, BAT, EXE, службы Windows.

4.8 Application Control\
ComfyUI, Ollama, Word, Excel, браузеры и локальные программы.

4.9 Workspace Manager\
Автоматическая организация рабочих проектов.

Результат: Butler становится полноценным помощником операционной
системы.

------------------------------------------------------------------------

## ЭТАП 5 --- HOME BUTLER

Главная цель проекта.

5.1 Home Manager\
Дом.

5.2 Finance Manager\
Платежи, счета, бюджет.

5.3 Calendar Manager\
Планирование.

5.4 Vehicle Manager\
Автобус, автомобиль, ТО, документы.

5.5 Purchase Manager\
Покупки.

5.6 Archive Butler\
Полный домашний архив.

5.7 Knowledge Butler\
Ответы по личной базе знаний.

5.8 Autonomous Assistant\
Самостоятельные рекомендации.

5.9 External Expert Gateway\
Единственная точка выхода во внешний мир. Gemini, OpenAI, Claude и
другие внешние модели используются только как консультанты, при
соблюдении Local First, Human Confirmation и Minimal Disclosure.

------------------------------------------------------------------------

## ИТОГОВАЯ АРХИТЕКТУРА

GLOBAL LAWS ↓ FOUNDATION ↓ SEMANTIC REASONING ENGINE ↓ MEMORY BRAIN ↓
GOAL PLANNER ↓ DESKTOP AGENT ↓ HOME BUTLER ↓ External Expert Gateway

## КЛЮЧЕВАЯ ЦЕЛЬ ROADMAP 6.0

После завершения Этапа 0 разработка смещается с инструментов
строительства Butler на самого Butler.

Система должна: 1. понимать; 2. помнить; 3. планировать; 4. действовать
в Windows; 5. стать полноценным домашним дворецким.

Облачные сервисы остаются вспомогательными внешними экспертами и не
являются обязательной частью локального ядра Butler.

``

---

# PASSPORT SUMMARY

Источник: `C:\Users\KOS\Desktop\Butler_Agent\BUTLER_OMEGA_SMART\PASSPORT_SUMMARY.md`

``md

Line
----
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
## MAIN ARCHITECTURE
- ARCHIVE: ArchiveDepartment
- AUDIO: AudioDepartment
- AUDIT: AuditScanner
- AUTOMATION: Recipe
- CODING: CodingDepartment
- CONFIG: RouterRegistry
- DEPARTMENT: Department
- DISPATCHER: SmartDispatcherV2
- DOCUMENTATION: ProjectDocumentationDepartment
- EXECUTION: Recipe
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
## CAPABILITY: MEMORY
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
- {"metadata": {"alias": null, "kind": "from", "line": 2, "name": "MemoryDepartment"}, "source": 1340, "target": "A_...
- {"metadata": {"alias": null, "kind": "from", "line": 3, "name": "MemoryAdvisor"}, "source": 1347, "target": "A_04_...
- {"metadata": {"alias": null, "kind": "from", "line": 4, "name": "MemoryDepartment"}, "source": 1285, "target": "A_...
- {"metadata": {"alias": null, "kind": "from", "line": 4, "name": "MemoryDepartment"}, "source": 1287, "target": "A_...
- {"metadata": {"alias": null, "kind": "from", "line": 4, "name": "MemoryDepartment"}, "source": 324, "target": "A_0...
- {"metadata": {"alias": null, "kind": "from", "line": 4, "name": "MemoryDepartment"}, "source": 338, "target": "A_0...
- {"metadata": {"context": "AgentLoopExecutor.__init__", "line": 10}, "source": 1114, "target": "ProjectHistory", "t...
- {"metadata": {"context": "AttentionMemory.__init__", "line": 14}, "source": 1124, "target": "MemoryReplay", "type"...
- {"metadata": {"context": "BootstrapCore.__init__", "line": 15}, "source": 1495, "target": "SelfHealingMemory", "ty...
- {"metadata": {"context": "ButlerOSAdapter.__init__", "line": 12}, "source": 405, "target": "ProjectMemoryLoader", ...
- {"metadata": {"context": "ButlerOSAdapter.memory_summary", "line": 15}, "source": 405, "target": "get_memory_summa...
- {"metadata": {"context": "ButlerSystem.__init__", "line": 14}, "source": 1505, "target": "SelfHealingMemory", "typ...
- {"metadata": {"context": "ChatCoreBridge.__init__", "line": 7}, "source": 205, "target": "SemanticLayer", "type": ...
- {"metadata": {"context": "ChatRouterMirror.__init__", "line": 7}, "source": 419, "target": "SemanticLayer", "type"...
- {"metadata": {"context": "ContextBudgetManager.__init__", "line": 15}, "source": 1136, "target": "AttentionMemory"...
- {"metadata": {"context": "ContextBudgetManager.__init__", "line": 16}, "source": 1136, "target": "MemoryOrchestrat...
- {"metadata": {"context": "CoreKernel.__init__", "line": 9}, "source": 207, "target": "SemanticLayer", "type": "cal...
- {"metadata": {"context": "CoreOrchestrator.__init__", "line": 7}, "source": 208, "target": "SemanticLayer", "type"...
- {"metadata": {"context": "CoreOrchestrator.__init__", "line": 8}, "source": 208, "target": "MemoryCore", "type": "...
- {"metadata": {"context": "DispatcherAgent.__init__", "line": 25}, "source": 508, "target": "SemanticMemory", "type...
- ... and 81 more
## CAPABILITY: ROUTER
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
- {"metadata": {"context": "ButlerInteractiveChat.__init__", "line": 38}, "source": 241, "target": "DispatcherAgent"...
- {"metadata": {"context": "DispatcherScanner.scan", "line": 18}, "source": 549, "target": "SmartDispatcherV2", "typ...
- {"metadata": {"context": "DispatcherScanner.scan", "line": 18}, "source": 597, "target": "SmartDispatcherV2", "typ...
- {"metadata": {"context": "DreamDispatcherAdapter.__init__", "line": 9}, "source": 432, "target": "DispatcherAgent"...
- {"metadata": {"context": "ProfessorAdapter.__init__", "line": 9}, "source": 465, "target": "DispatcherAgent", "typ...
- {"metadata": {"context": "RouterIntegration.__init__", "line": 21}, "source": 123, "target": "AgentRouter", "type"...
- {"metadata": {"context": "RouterIntegration.__init__", "line": 21}, "source": 467, "target": "AgentRouter", "type"...
- {"metadata": {"context": "RouterIntegration.__init__", "line": 22}, "source": 123, "target": "RouterRegistry", "ty...
- {"metadata": {"context": "RouterIntegration.__init__", "line": 22}, "source": 467, "target": "RouterRegistry", "ty...
- {"metadata": {"context": "RouterIntegration.__init__", "line": 24}, "source": 468, "target": "AgentRouter", "type"...
- {"metadata": {"context": "RouterIntegration.__init__", "line": 25}, "source": 468, "target": "RouterRegistry", "ty...
- {"metadata": {"context": "RuntimeDepartmentsDiscoveryAgent.discover", "line": 24}, "source": 534, "target": "Smart...
- {"metadata": {"context": "RuntimeDepartmentsDiscoveryAgent.discover", "line": 24}, "source": 589, "target": "Smart...
- {"metadata": {"context": "Worker.__init__", "line": 10}, "source": 480, "target": "DispatcherAgent", "type": "call...
- {"metadata": {"context": "Worker.__init__", "line": 35}, "source": 477, "target": "RouterRegistry", "type": "call"...
- {"metadata": {"context": "main", "line": 233}, "source": 1364, "target": "RouterIntegration", "type": "call"} (fil...
- {"metadata": {"context": "main", "line": 233}, "source": 417, "target": "RouterIntegration", "type": "call"} (file...
- {"metadata": {"context": "main", "line": 250}, "source": 414, "target": "RouterIntegration", "type": "call"} (file...
- {"metadata": {"context": null, "line": 10}, "source": 1393, "target": "SmartDispatcherV2", "type": "call"} (file: ...
- {"metadata": {"context": null, "line": 120}, "source": 338, "target": "SmartDispatcherV2", "type": "call"} (file: ...
- ... and 19 more
## CAPABILITY: DEPARTMENT
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
- RuntimeDepartmentsDiscoveryAgent (file: A_04_AGENTS/ProjectDocumentationDepartment/Core/Discovery/runtime_departme...
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
- {"metadata": {"alias": "evidence_doctor", "kind": "from", "line": 5, "name": "dispatch"}, "source": 611, "target":...
- {"metadata": {"alias": null, "kind": "from", "line": 1, "name": "BaseDepartment"}, "source": 486, "target": "A_04_...
- {"metadata": {"alias": null, "kind": "from", "line": 1, "name": "BaseDepartment"}, "source": 505, "target": "A_04_...
- {"metadata": {"alias": null, "kind": "from", "line": 1, "name": "BaseDepartment"}, "source": 623, "target": "A_04_...
- {"metadata": {"alias": null, "kind": "from", "line": 1, "name": "CodingDepartment"}, "source": 1340, "target": "A_...
- {"metadata": {"alias": null, "kind": "from", "line": 1, "name": "SearchDepartment"}, "source": 1518, "target": "A_...
- {"metadata": {"alias": null, "kind": "from", "line": 10, "name": "ArchiveDepartment"}, "source": 1285, "target": "...
- {"metadata": {"alias": null, "kind": "from", "line": 10, "name": "ArchiveDepartment"}, "source": 1287, "target": "...
- {"metadata": {"alias": null, "kind": "from", "line": 10, "name": "ArchiveDepartment"}, "source": 324, "target": "A...
- {"metadata": {"alias": null, "kind": "from", "line": 10, "name": "ArchiveDepartment"}, "source": 338, "target": "A...
- {"metadata": {"alias": null, "kind": "from", "line": 11, "name": "SearchDepartment"}, "source": 1285, "target": "A...
- {"metadata": {"alias": null, "kind": "from", "line": 11, "name": "SearchDepartment"}, "source": 1287, "target": "A...
- {"metadata": {"alias": null, "kind": "from", "line": 11, "name": "SearchDepartment"}, "source": 324, "target": "A_...
- {"metadata": {"alias": null, "kind": "from", "line": 12, "name": "BaseDepartment"}, "source": 1389, "target": "A_0...
- {"metadata": {"alias": null, "kind": "from", "line": 12, "name": "BaseDepartment"}, "source": 499, "target": "A_04...
- {"metadata": {"alias": null, "kind": "from", "line": 12, "name": "DocumentsDepartment"}, "source": 1285, "target":...
- {"metadata": {"alias": null, "kind": "from", "line": 12, "name": "DocumentsDepartment"}, "source": 1287, "target":...
- {"metadata": {"alias": null, "kind": "from", "line": 12, "name": "DocumentsDepartment"}, "source": 324, "target": ...
- {"metadata": {"alias": null, "kind": "from", "line": 13, "name": "OpenDocumentDepartment"}, "source": 1285, "targe...
- {"metadata": {"alias": null, "kind": "from", "line": 13, "name": "OpenDocumentDepartment"}, "source": 1287, "targe...
- ... and 116 more
## CAPABILITY: VISION
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
- {"metadata": {"alias": null, "kind": "from", "line": 11, "name": "ImageSession"}, "source": 426, "target": "A_03_O...
- {"metadata": {"alias": null, "kind": "from", "line": 13, "name": "ImageSession"}, "source": 499, "target": "A_03_O...
- {"metadata": {"alias": null, "kind": "from", "line": 158, "name": "ImageDepartment"}, "source": 414, "target": "A_...
- {"metadata": {"alias": null, "kind": "from", "line": 3, "name": "VisionDepartment"}, "source": 1340, "target": "A_...
- {"metadata": {"alias": null, "kind": "from", "line": 4, "name": "ImageDepartment"}, "source": 1340, "target": "A_0...
- {"metadata": {"alias": null, "kind": "from", "line": 5, "name": "VisionDepartment"}, "source": 1285, "target": "A_...
- {"metadata": {"alias": null, "kind": "from", "line": 5, "name": "VisionDepartment"}, "source": 1287, "target": "A_...
- {"metadata": {"alias": null, "kind": "from", "line": 5, "name": "VisionDepartment"}, "source": 324, "target": "A_0...
- {"metadata": {"alias": null, "kind": "from", "line": 5, "name": "VisionDepartment"}, "source": 338, "target": "A_0...
- {"metadata": {"alias": null, "kind": "from", "line": 6, "name": "ImageDepartment"}, "source": 1285, "target": "A_0...
- {"metadata": {"alias": null, "kind": "from", "line": 6, "name": "ImageDepartment"}, "source": 1287, "target": "A_0...
- {"metadata": {"alias": null, "kind": "from", "line": 6, "name": "ImageDepartment"}, "source": 324, "target": "A_04...
- {"metadata": {"alias": null, "kind": "from", "line": 6, "name": "ImageDepartment"}, "source": 338, "target": "A_04...
- {"metadata": {"alias": null, "kind": "from", "line": 7, "name": "ImageDepartment"}, "source": 1392, "target": "A_0...
- {"metadata": {"alias": null, "kind": "from", "line": 9, "name": "ImageDepartment"}, "source": 1394, "target": "A_0...
- {"metadata": {"context": "DispatcherAgent.__init__", "line": 24}, "source": 508, "target": "VisionEngine", "type":...
- {"metadata": {"context": "DispatcherAgent.__init__", "line": 35}, "source": 508, "target": "VisionEngine", "type":...
- {"metadata": {"context": "HandlerRegistry.__init__", "line": 22}, "source": 387, "target": "ImageHandler", "type":...
- {"metadata": {"context": "ImageHandler.__init__", "line": 20}, "source": 382, "target": "VisionEngine", "type": "c...
- {"metadata": {"context": "PDFHandler._extract_scanned_pdf_with_vision", "line": 113}, "source": 385, "target": "Vi...
- ... and 18 more
## CAPABILITY: IMAGE
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
- {"metadata": {"alias": null, "kind": "from", "line": 11, "name": "ImageSession"}, "source": 426, "target": "A_03_O...
- {"metadata": {"alias": null, "kind": "from", "line": 13, "name": "ImageSession"}, "source": 499, "target": "A_03_O...
- {"metadata": {"alias": null, "kind": "from", "line": 158, "name": "ImageDepartment"}, "source": 414, "target": "A_...
- {"metadata": {"alias": null, "kind": "from", "line": 3, "name": "VisionDepartment"}, "source": 1340, "target": "A_...
- {"metadata": {"alias": null, "kind": "from", "line": 4, "name": "ImageDepartment"}, "source": 1340, "target": "A_0...
- {"metadata": {"alias": null, "kind": "from", "line": 5, "name": "VisionDepartment"}, "source": 1285, "target": "A_...
- {"metadata": {"alias": null, "kind": "from", "line": 5, "name": "VisionDepartment"}, "source": 1287, "target": "A_...
- {"metadata": {"alias": null, "kind": "from", "line": 5, "name": "VisionDepartment"}, "source": 324, "target": "A_0...
- {"metadata": {"alias": null, "kind": "from", "line": 5, "name": "VisionDepartment"}, "source": 338, "target": "A_0...
- {"metadata": {"alias": null, "kind": "from", "line": 6, "name": "ImageDepartment"}, "source": 1285, "target": "A_0...
- {"metadata": {"alias": null, "kind": "from", "line": 6, "name": "ImageDepartment"}, "source": 1287, "target": "A_0...
- {"metadata": {"alias": null, "kind": "from", "line": 6, "name": "ImageDepartment"}, "source": 324, "target": "A_04...
- {"metadata": {"alias": null, "kind": "from", "line": 6, "name": "ImageDepartment"}, "source": 338, "target": "A_04...
- {"metadata": {"alias": null, "kind": "from", "line": 7, "name": "ImageDepartment"}, "source": 1392, "target": "A_0...
- {"metadata": {"alias": null, "kind": "from", "line": 9, "name": "ImageDepartment"}, "source": 1394, "target": "A_0...
- {"metadata": {"context": "DispatcherAgent.__init__", "line": 24}, "source": 508, "target": "VisionEngine", "type":...
- {"metadata": {"context": "DispatcherAgent.__init__", "line": 35}, "source": 508, "target": "VisionEngine", "type":...
- {"metadata": {"context": "HandlerRegistry.__init__", "line": 22}, "source": 387, "target": "ImageHandler", "type":...
- {"metadata": {"context": "ImageHandler.__init__", "line": 20}, "source": 382, "target": "VisionEngine", "type": "c...
- {"metadata": {"context": "PDFHandler._extract_scanned_pdf_with_vision", "line": 113}, "source": 385, "target": "Vi...
- ... and 18 more
## CAPABILITY: SEARCH
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
- {"metadata": {"alias": null, "kind": "from", "line": 1, "name": "SearchDepartment"}, "source": 1518, "target": "A_...
- {"metadata": {"alias": null, "kind": "from", "line": 11, "name": "SearchDepartment"}, "source": 1285, "target": "A...
- {"metadata": {"alias": null, "kind": "from", "line": 11, "name": "SearchDepartment"}, "source": 1287, "target": "A...
- {"metadata": {"alias": null, "kind": "from", "line": 11, "name": "SearchDepartment"}, "source": 324, "target": "A_...
- {"metadata": {"alias": null, "kind": "from", "line": 3, "name": "SearchDepartment"}, "source": 1519, "target": "A_...
- {"metadata": {"context": "MemoryAdvisor.__init__", "line": 13}, "source": 1141, "target": "SemanticSearchEngine", ...
- {"metadata": {"context": "SearchDepartment.__init__", "line": 11}, "source": 616, "target": "CatalogSearchBridge",...
- {"metadata": {"context": "SemanticCore.__init__", "line": 26}, "source": 1179, "target": "SemanticQueryParser", "t...
- {"metadata": {"context": "SmartDispatcherV2.__init__", "line": 25}, "source": 1285, "target": "SearchDepartment", ...
- {"metadata": {"context": "SmartDispatcherV2.__init__", "line": 25}, "source": 1287, "target": "SearchDepartment", ...
- {"metadata": {"context": "SmartDispatcherV2.__init__", "line": 28}, "source": 324, "target": "SearchDepartment", "...
- {"metadata": {"context": "run_tests", "line": 62}, "source": 1354, "target": "SemanticSearchEngine", "type": "call...
- {"metadata": {"context": null, "line": 11}, "source": 1216, "target": "SemanticQueryParser", "type": "call"} (file...
- {"metadata": {"context": null, "line": 48}, "source": 1190, "target": "SemanticQueryParser", "type": "call"} (file...
- {"metadata": {"context": null, "line": 4}, "source": 1518, "target": "SearchDepartment", "type": "call"} (file: None)
- {"metadata": {"context": null, "line": 5}, "source": 1519, "target": "SearchDepartment", "type": "call"} (file: None)
## CAPABILITY: CODING
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
- {"metadata": {"alias": null, "kind": "from", "line": 1, "name": "CodingDepartment"}, "source": 1340, "target": "A_...
- {"metadata": {"alias": null, "kind": "from", "line": 3, "name": "CodingDepartment"}, "source": 1285, "target": "A_...
- {"metadata": {"alias": null, "kind": "from", "line": 3, "name": "CodingDepartment"}, "source": 1287, "target": "A_...
- {"metadata": {"alias": null, "kind": "from", "line": 3, "name": "CodingDepartment"}, "source": 324, "target": "A_0...
- {"metadata": {"alias": null, "kind": "from", "line": 3, "name": "CodingDepartment"}, "source": 338, "target": "A_0...
- {"metadata": {"context": "HandlerRegistry.__init__", "line": 17}, "source": 387, "target": "CodeHandler", "type": ...
- {"metadata": {"context": "PDFHandler._extract_scanned_pdf_with_vision", "line": 172}, "source": 385, "target": "lo...
- {"metadata": {"context": "PDFHandler._extract_text_pdf", "line": 76}, "source": 385, "target": "looks_like_code", ...
- {"metadata": {"context": "SmartDispatcherV2.__init__", "line": 22}, "source": 338, "target": "CodingDepartment", "...
- {"metadata": {"context": "SmartDispatcherV2.__init__", "line": 27}, "source": 1285, "target": "CodingDepartment", ...
- {"metadata": {"context": "SmartDispatcherV2.__init__", "line": 27}, "source": 1287, "target": "CodingDepartment", ...
- {"metadata": {"context": "SmartDispatcherV2.__init__", "line": 32}, "source": 324, "target": "CodingDepartment", "...
- {"metadata": {"context": "VisionAnalyzer.analyze", "line": 53}, "source": 390, "target": "_looks_like_code", "type...
- {"metadata": {"context": "run_memory_guardian", "line": 201}, "source": 219, "target": "check_code_layer", "type":...
- {"metadata": {"context": null, "line": 11}, "source": 1340, "target": "CodingDepartment", "type": "call"} (file: N...
- {"metadata": {"context": null, "line": 3}, "source": 1345, "target": "InlineCodeEditor", "type": "call"} (file: None)
- {"metadata": {"context": null, "line": 5}, "source": 490, "target": "CodingDepartment", "type": "call"} (file: None)
## CAPABILITY: SECURITY
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
- {"metadata": {"alias": null, "kind": "from", "line": 11, "name": "ExecutionHistory"}, "source": 294, "target": "A_...
- {"metadata": {"alias": null, "kind": "from", "line": 14, "name": "ExecutionState"}, "source": 295, "target": "A_02...
- {"metadata": {"alias": null, "kind": "from", "line": 9, "name": "SystemState"}, "source": 305, "target": "A_02_MAN...
- {"metadata": {"context": "SecurityValidator.validate", "line": 41}, "source": 359, "target": "SecurityViolation", ...
- {"metadata": {"context": "SecurityValidator.validate", "line": 51}, "source": 359, "target": "SecurityViolation", ...
- {"metadata": {"context": "execute_repair", "line": 88}, "source": 1486, "target": "run_memory_guardian", "type": "...
- {"metadata": {"context": "main", "line": 118}, "source": 1486, "target": "run_memory_guardian", "type": "call"} (f...
- {"metadata": {"context": "main", "line": 121}, "source": 1486, "target": "run_memory_guardian", "type": "call"} (f...
- {"metadata": {"context": "run", "line": 21}, "source": 357, "target": "RecipeQueueWatcher", "type": "call"} (file:...
- {"metadata": {"context": "run_once", "line": 25}, "source": 358, "target": "RecipeQueueWatcher", "type": "call"} (...
- {"metadata": {"context": null, "line": 144}, "source": 231, "target": "run_guardian", "type": "call"} (file: None)
- {"metadata": {"context": null, "line": 229}, "source": 219, "target": "run_memory_guardian", "type": "call"} (file...
- {"metadata": {"context": null, "line": 39}, "source": 293, "target": "ExecutionMonitor", "type": "call"} (file: None)
- {"metadata": {"context": null, "line": 39}, "source": 350, "target": "RecipeQueueWatcher", "type": "call"} (file: ...
## CAPABILITY: EXECUTION
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
- ExecutionRegistryDiscoveryAgent (file: A_04_AGENTS/ProjectDocumentationDepartment/Core/Discovery/execution_registr...
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
- ... and 49 more
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
- ... and 32 more
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
- A_02_MANAGERS.TaskRunner.ExecutionAdapters.base_adapter (file: A_02_MANAGERS/TaskRunner/ExecutionAdapters/powershe...
- A_02_MANAGERS.TaskRunner.ExecutionAdapters.base_adapter (file: A_02_MANAGERS/TaskRunner/ExecutionAdapters/python_a...
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
- {"metadata": {"alias": null, "kind": "from", "line": 11, "name": "ExecutionHistory"}, "source": 294, "target": "A_...
- {"metadata": {"alias": null, "kind": "from", "line": 11, "name": "ExecutionResult"}, "source": 339, "target": "A_0...
- {"metadata": {"alias": null, "kind": "from", "line": 11, "name": "PolicyLoader"}, "source": 297, "target": "A_02_M...
- {"metadata": {"alias": null, "kind": "from", "line": 11, "name": "PolicyLoader"}, "source": 298, "target": "A_02_M...
- {"metadata": {"alias": null, "kind": "from", "line": 11, "name": "PythonExecutionAdapter"}, "source": 346, "target...
- {"metadata": {"alias": null, "kind": "from", "line": 12, "name": "ExecutionResult"}, "source": 343, "target": "A_0...
- {"metadata": {"alias": null, "kind": "from", "line": 12, "name": "ExecutionResult"}, "source": 344, "target": "A_0...
- {"metadata": {"alias": null, "kind": "from", "line": 12, "name": "RecipeWriter"}, "source": 305, "target": "A_02_M...
- {"metadata": {"alias": null, "kind": "from", "line": 13, "name": "BaseExecutionAdapter"}, "source": 343, "target":...
- {"metadata": {"alias": null, "kind": "from", "line": 13, "name": "BaseExecutionAdapter"}, "source": 344, "target":...
- {"metadata": {"alias": null, "kind": "from", "line": 13, "name": "Recipe"}, "source": 348, "target": "A_07_CONFIG....
- {"metadata": {"alias": null, "kind": "from", "line": 13, "name": "RecipeStep"}, "source": 348, "target": "A_07_CON...
- {"metadata": {"alias": null, "kind": "from", "line": 13, "name": "run_once"}, "source": 305, "target": "A_02_MANAG...
- {"metadata": {"alias": null, "kind": "from", "line": 14, "name": "ExecutionResult"}, "source": 348, "target": "A_0...
- {"metadata": {"alias": null, "kind": "from", "line": 14, "name": "ExecutionState"}, "source": 295, "target": "A_02...
- {"metadata": {"alias": null, "kind": "from", "line": 14, "name": "PowerShellExecutionAdapter"}, "source": 346, "ta...
- {"metadata": {"alias": null, "kind": "from", "line": 14, "name": "RecipeBuilder"}, "source": 309, "target": "A_02_...
- {"metadata": {"alias": null, "kind": "from", "line": 14, "name": "RecipeQueueWatcher"}, "source": 358, "target": "...
- {"metadata": {"alias": null, "kind": "from", "line": 15, "name": "ExecutorFactory"}, "source": 348, "target": "A_0...
- {"metadata": {"alias": null, "kind": "from", "line": 15, "name": "Recipe"}, "source": 347, "target": "A_07_CONFIG....
- ... and 105 more
## CAPABILITY: CONFIG
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
- ExecutionRegistryDiscoveryAgent (file: A_04_AGENTS/ProjectDocumentationDepartment/Core/Discovery/execution_registr...
- GoalsRegistryDiscoveryAgent (file: A_04_AGENTS/ProjectDocumentationDepartment/Core/Discovery/goals_registry_discov...
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
- A_02_MANAGERS.RuntimeCapabilityRegistry.capability_schema (file: A_02_MANAGERS/RuntimeCapabilityRegistry/runtime_r...
- A_02_MANAGERS.RuntimeCapabilityRegistry.runtime_registry (file: 1081)
### LINKS:
- {"metadata": {"alias": null, "kind": "from", "line": 15, "name": "RuntimeCapabilityRegistry"}, "source": 1081, "ta...
- {"metadata": {"alias": null, "kind": "from", "line": 9, "name": "RuntimeCapability"}, "source": 320, "target": "A_...
- {"metadata": {"context": "BootstrapCore.__init__", "line": 16}, "source": 1495, "target": "RegistryBrain", "type":...
- {"metadata": {"context": "ButlerSystem.__init__", "line": 15}, "source": 1505, "target": "RegistryBrain", "type": ...
- {"metadata": {"context": "EngineeringPipeline.collect", "line": 56}, "source": 536, "target": "RegistryScanner", "...
- {"metadata": {"context": "EngineeringPipeline.collect", "line": 56}, "source": 591, "target": "RegistryScanner", "...
- {"metadata": {"context": "LoopOrchestratorV3_MASTER_TRUTH.__init__", "line": 48}, "source": 1117, "target": "Execu...
- {"metadata": {"context": "ProjectState.__init__", "line": 11}, "source": 1102, "target": "RegistryLoader", "type":...
- {"metadata": {"context": "ProjectState.__init__", "line": 11}, "source": 1103, "target": "RegistryLoader", "type":...
- {"metadata": {"context": "RouterIntegration.__init__", "line": 22}, "source": 123, "target": "RouterRegistry", "ty...
- {"metadata": {"context": "RouterIntegration.__init__", "line": 22}, "source": 467, "target": "RouterRegistry", "ty...
- {"metadata": {"context": "RouterIntegration.__init__", "line": 25}, "source": 468, "target": "RouterRegistry", "ty...
- {"metadata": {"context": "Worker.__init__", "line": 35}, "source": 477, "target": "RouterRegistry", "type": "call"...
- {"metadata": {"context": null, "line": 23}, "source": 469, "target": "RouterRegistry", "type": "call"} (file: None)
- {"metadata": {"context": null, "line": 23}, "source": 470, "target": "RouterRegistry", "type": "call"} (file: None)
- {"metadata": {"context": null, "line": 26}, "source": 1454, "target": "register_test_job", "type": "call"} (file: ...
- {"metadata": {"context": null, "line": 34}, "source": 1106, "target": "RegistryLoader", "type": "call"} (file: None)
- {"metadata": {"context": null, "line": 37}, "source": 387, "target": "HandlerRegistry", "type": "call"} (file: None)
- {"metadata": {"context": null, "line": 38}, "source": 1441, "target": "reset_and_register", "type": "call"} (file:...
- {"metadata": {"context": null, "line": 47}, "source": 1107, "target": "RegistryValidator", "type": "call"} (file: ...
- ... and 1 more
## CAPABILITY: DOCUMENTATION
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
- A_04_AGENTS.ProjectDocumentationDepartment.Core.engineering_pipeline (file: A_04_AGENTS/ProjectDocumentationDepart...
- A_04_AGENTS.ProjectDocumentationDepartment.Core.evidence_doctor (file: A_04_AGENTS/ProjectDocumentationDepartment/...
- A_04_AGENTS.ProjectDocumentationDepartment.runner (file: 1516)
- A_04_AGENTS.ProjectDocumentationDepartment.runner (file: 324)
### LINKS:
- {"metadata": {"alias": "evidence_doctor", "kind": "from", "line": 5, "name": "dispatch"}, "source": 611, "target":...
- {"metadata": {"alias": null, "kind": "from", "line": 14, "name": "ProjectDocumentationDepartment"}, "source": 324,...
- {"metadata": {"alias": null, "kind": "from", "line": 3, "name": "ProjectDocumentationDepartment"}, "source": 1516,...
- {"metadata": {"alias": null, "kind": "from", "line": 4, "name": "EngineeringPipeline"}, "source": 611, "target": "...
- {"metadata": {"context": "SmartDispatcherV2.__init__", "line": 31}, "source": 324, "target": "ProjectDocumentation...
- {"metadata": {"context": null, "line": 5}, "source": 1516, "target": "ProjectDocumentationDepartment", "type": "ca...
- {"metadata": {"context": null, "line": 96}, "source": 611, "target": "ProjectDocumentationDepartment", "type": "ca...
## CAPABILITY: AUDIO
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
- {"metadata": {"alias": null, "kind": "from", "line": 5, "name": "AudioDepartment"}, "source": 1340, "target": "A_0...
- {"metadata": {"alias": null, "kind": "from", "line": 7, "name": "AudioDepartment"}, "source": 1285, "target": "A_0...
- {"metadata": {"alias": null, "kind": "from", "line": 7, "name": "AudioDepartment"}, "source": 1287, "target": "A_0...
- {"metadata": {"alias": null, "kind": "from", "line": 7, "name": "AudioDepartment"}, "source": 324, "target": "A_04...
- {"metadata": {"alias": null, "kind": "from", "line": 7, "name": "AudioDepartment"}, "source": 338, "target": "A_04...
- {"metadata": {"context": "SmartDispatcherV2.__init__", "line": 26}, "source": 338, "target": "AudioDepartment", "t...
- {"metadata": {"context": "SmartDispatcherV2.__init__", "line": 32}, "source": 1285, "target": "AudioDepartment", "...
- {"metadata": {"context": "SmartDispatcherV2.__init__", "line": 32}, "source": 1287, "target": "AudioDepartment", "...
- {"metadata": {"context": "SmartDispatcherV2.__init__", "line": 36}, "source": 324, "target": "AudioDepartment", "t...
- {"metadata": {"context": null, "line": 15}, "source": 1340, "target": "AudioDepartment", "type": "call"} (file: None)
## CAPABILITY: VIDEO
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
- {"metadata": {"alias": null, "kind": "from", "line": 7, "name": "VideoDepartment"}, "source": 1340, "target": "A_0...
- {"metadata": {"alias": null, "kind": "from", "line": 9, "name": "VideoDepartment"}, "source": 1285, "target": "A_0...
- {"metadata": {"alias": null, "kind": "from", "line": 9, "name": "VideoDepartment"}, "source": 1287, "target": "A_0...
- {"metadata": {"alias": null, "kind": "from", "line": 9, "name": "VideoDepartment"}, "source": 324, "target": "A_04...
- {"metadata": {"alias": null, "kind": "from", "line": 9, "name": "VideoDepartment"}, "source": 338, "target": "A_04...
- {"metadata": {"context": "SmartDispatcherV2.__init__", "line": 28}, "source": 338, "target": "VideoDepartment", "t...
- {"metadata": {"context": "SmartDispatcherV2.__init__", "line": 34}, "source": 1285, "target": "VideoDepartment", "...
- {"metadata": {"context": "SmartDispatcherV2.__init__", "line": 34}, "source": 1287, "target": "VideoDepartment", "...
- {"metadata": {"context": "SmartDispatcherV2.__init__", "line": 38}, "source": 324, "target": "VideoDepartment", "t...
- {"metadata": {"context": null, "line": 17}, "source": 1340, "target": "VideoDepartment", "type": "call"} (file: None)
## CAPABILITY: ARCHIVE
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
- {"metadata": {"alias": null, "kind": "from", "line": 10, "name": "ArchiveDepartment"}, "source": 1285, "target": "...
- {"metadata": {"alias": null, "kind": "from", "line": 10, "name": "ArchiveDepartment"}, "source": 1287, "target": "...
- {"metadata": {"alias": null, "kind": "from", "line": 10, "name": "ArchiveDepartment"}, "source": 324, "target": "A...
- {"metadata": {"alias": null, "kind": "from", "line": 10, "name": "ArchiveDepartment"}, "source": 338, "target": "A...
- {"metadata": {"alias": null, "kind": "from", "line": 8, "name": "ArchiveDepartment"}, "source": 1340, "target": "A...
- {"metadata": {"context": "ArchiveDepartment.execute", "line": 63}, "source": 483, "target": "ArchiveHandler", "typ...
- {"metadata": {"context": "HandlerRegistry.__init__", "line": 23}, "source": 387, "target": "ArchiveHandler", "type...
- {"metadata": {"context": "SmartDispatcherV2.__init__", "line": 29}, "source": 338, "target": "ArchiveDepartment", ...
- {"metadata": {"context": "SmartDispatcherV2.__init__", "line": 35}, "source": 1285, "target": "ArchiveDepartment",...
- {"metadata": {"context": "SmartDispatcherV2.__init__", "line": 35}, "source": 1287, "target": "ArchiveDepartment",...
- {"metadata": {"context": "SmartDispatcherV2.__init__", "line": 39}, "source": 324, "target": "ArchiveDepartment", ...
- {"metadata": {"context": "TaskRunner.patch_file", "line": 63}, "source": 352, "target": "backup_file", "type": "ca...
- {"metadata": {"context": "guarded_write", "line": 104}, "source": 225, "target": "restore_backup", "type": "call"}...
- {"metadata": {"context": "guarded_write", "line": 94}, "source": 225, "target": "backup_file", "type": "call"} (fi...
- {"metadata": {"context": null, "line": 131}, "source": 225, "target": "backup_file", "type": "call"} (file: None)
- {"metadata": {"context": null, "line": 133}, "source": 225, "target": "restore_backup", "type": "call"} (file: None)
- {"metadata": {"context": null, "line": 18}, "source": 1340, "target": "ArchiveDepartment", "type": "call"} (file: ...
- {"metadata": {"context": null, "line": 19}, "source": 282, "target": "Archiver", "type": "call"} (file: None)
- {"metadata": {"context": null, "line": 19}, "source": 362, "target": "Archiver", "type": "call"} (file: None)
## CAPABILITY: MODEL
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
- {"metadata": {"context": "BootstrapCore.__init__", "line": 16}, "source": 1495, "target": "RegistryBrain", "type":...
- {"metadata": {"context": "BootstrapCore.init_system", "line": 45}, "source": 1495, "target": "auto_repair", "type"...
- {"metadata": {"context": "ButlerInteractiveChat.start_session", "line": 101}, "source": 241, "target": "ask_ollama...
- {"metadata": {"context": "ButlerSystem.__init__", "line": 15}, "source": 1505, "target": "RegistryBrain", "type": ...
- {"metadata": {"context": "ButlerSystem.clean_init", "line": 24}, "source": 1505, "target": "auto_repair", "type": ...
- {"metadata": {"context": "PolicyLoader.default_policy", "line": 32}, "source": 296, "target": "Constraints", "type...
- {"metadata": {"context": "ReferenceResolver.resolve", "line": 56}, "source": 1201, "target": "_failure", "type": "...
- {"metadata": {"context": "ReferenceResolver.resolve", "line": 62}, "source": 1201, "target": "_failure", "type": "...
- {"metadata": {"context": "ReferenceResolver.resolve", "line": 69}, "source": 1201, "target": "_failure", "type": "...
- {"metadata": {"context": "ReferenceResolver.resolve", "line": 76}, "source": 1201, "target": "_failure", "type": "...
- {"metadata": {"context": "ReferenceResolver.resolve", "line": 81}, "source": 1201, "target": "_failure", "type": "...
- {"metadata": {"context": "ReferenceResolver.resolve", "line": 88}, "source": 1201, "target": "_failure", "type": "...
- {"metadata": {"context": "ReferenceResolver.resolve", "line": 90}, "source": 1201, "target": "_failure", "type": "...
- {"metadata": {"context": "VisionEngine.__init__", "line": 10}, "source": 391, "target": "OllamaVisionBackend", "ty...
- {"metadata": {"context": "dispatch", "line": 103}, "source": 539, "target": "main", "type": "call"} (file: None)
- {"metadata": {"context": "dispatch", "line": 147}, "source": 539, "target": "main", "type": "call"} (file: None)
- {"metadata": {"context": "handle_chat", "line": 169}, "source": 1364, "target": "choose_model", "type": "call"} (f...
- {"metadata": {"context": "handle_chat", "line": 169}, "source": 417, "target": "choose_model", "type": "call"} (fi...
- {"metadata": {"context": "handle_chat", "line": 186}, "source": 414, "target": "choose_model", "type": "call"} (fi...
- {"metadata": {"context": "handle_chat", "line": 190}, "source": 1364, "target": "ask_ollama", "type": "call"} (fil...
- ... and 142 more
## CAPABILITY: OLLAMA
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
- {"metadata": {"context": "AgentLoopExecutor.__init__", "line": 11}, "source": 1114, "target": "ChangeRequestManage...
- {"metadata": {"context": "ArchitectAgent.__init__", "line": 29}, "source": 261, "target": "ContextProvider", "type...
- {"metadata": {"context": "ArchitectAgent.__init__", "line": 33}, "source": 261, "target": "QueueManager", "type": ...
- {"metadata": {"context": "ButlerDiagnostics.__init__", "line": 14}, "source": 209, "target": "CatalogManager", "ty...
- {"metadata": {"context": "ButlerDiagnostics.__init__", "line": 14}, "source": 245, "target": "CatalogManager", "ty...
- {"metadata": {"context": "ButlerInteractiveChat.__init__", "line": 37}, "source": 241, "target": "CatalogManager",...
- {"metadata": {"context": "ButlerInteractiveChat.start_session", "line": 101}, "source": 241, "target": "ask_ollama...
- {"metadata": {"context": "ButlerMcpServer.__init__", "line": 10}, "source": 217, "target": "CatalogManager", "type...
- {"metadata": {"context": "ButlerMcpServer.__init__", "line": 10}, "source": 251, "target": "CatalogManager", "type...
- {"metadata": {"context": "CatalogSearchBridge.__init__", "line": 10}, "source": 1125, "target": "SessionManagerPol...
- {"metadata": {"context": "CatalogSearchBridge.__init__", "line": 9}, "source": 1125, "target": "CatalogManager", "...
- {"metadata": {"context": "DispatcherAgent.__init__", "line": 22}, "source": 630, "target": "CatalogManager", "type...
- {"metadata": {"context": "DispatcherAgent.__init__", "line": 34}, "source": 508, "target": "CatalogManager", "type...
- {"metadata": {"context": "LoopOrchestratorV3_EXEC_V2.__init__", "line": 39}, "source": 1118, "target": "ChangeRequ...
- {"metadata": {"context": "LoopOrchestratorV3_MASTER_TRUTH.__init__", "line": 47}, "source": 1117, "target": "Chang...
- {"metadata": {"context": "MainOrchestrator.__init__", "line": 8}, "source": 253, "target": "CatalogManager", "type...
- {"metadata": {"context": "MainOrchestrator.__init__", "line": 9}, "source": 221, "target": "CatalogManager", "type...
- {"metadata": {"context": "MemoryFacade.__init__", "line": 16}, "source": 1144, "target": "ChangeRequestManager", "...
- {"metadata": {"context": "MemoryFacade.__init__", "line": 17}, "source": 1145, "target": "ChangeRequestManager", "...
- {"metadata": {"context": "MemoryLayer.__init__", "line": 8}, "source": 1157, "target": "ButlerSessionManager", "ty...
- ... and 118 more
## CAPABILITY: PROVIDER
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
- {"metadata": {"context": "AgentLoopExecutor.__init__", "line": 11}, "source": 1114, "target": "ChangeRequestManage...
- {"metadata": {"context": "ArchitectAgent.__init__", "line": 29}, "source": 261, "target": "ContextProvider", "type...
- {"metadata": {"context": "ArchitectAgent.__init__", "line": 33}, "source": 261, "target": "QueueManager", "type": ...
- {"metadata": {"context": "ButlerDiagnostics.__init__", "line": 14}, "source": 209, "target": "CatalogManager", "ty...
- {"metadata": {"context": "ButlerDiagnostics.__init__", "line": 14}, "source": 245, "target": "CatalogManager", "ty...
- {"metadata": {"context": "ButlerInteractiveChat.__init__", "line": 37}, "source": 241, "target": "CatalogManager",...
- {"metadata": {"context": "ButlerInteractiveChat.start_session", "line": 101}, "source": 241, "target": "ask_ollama...
- {"metadata": {"context": "ButlerMcpServer.__init__", "line": 10}, "source": 217, "target": "CatalogManager", "type...
- {"metadata": {"context": "ButlerMcpServer.__init__", "line": 10}, "source": 251, "target": "CatalogManager", "type...
- {"metadata": {"context": "CatalogSearchBridge.__init__", "line": 10}, "source": 1125, "target": "SessionManagerPol...
- {"metadata": {"context": "CatalogSearchBridge.__init__", "line": 9}, "source": 1125, "target": "CatalogManager", "...
- {"metadata": {"context": "DispatcherAgent.__init__", "line": 22}, "source": 630, "target": "CatalogManager", "type...
- {"metadata": {"context": "DispatcherAgent.__init__", "line": 34}, "source": 508, "target": "CatalogManager", "type...
- {"metadata": {"context": "LoopOrchestratorV3_EXEC_V2.__init__", "line": 39}, "source": 1118, "target": "ChangeRequ...
- {"metadata": {"context": "LoopOrchestratorV3_MASTER_TRUTH.__init__", "line": 47}, "source": 1117, "target": "Chang...
- {"metadata": {"context": "MainOrchestrator.__init__", "line": 8}, "source": 253, "target": "CatalogManager", "type...
- {"metadata": {"context": "MainOrchestrator.__init__", "line": 9}, "source": 221, "target": "CatalogManager", "type...
- {"metadata": {"context": "MemoryFacade.__init__", "line": 16}, "source": 1144, "target": "ChangeRequestManager", "...
- {"metadata": {"context": "MemoryFacade.__init__", "line": 17}, "source": 1145, "target": "ChangeRequestManager", "...
- {"metadata": {"context": "MemoryLayer.__init__", "line": 8}, "source": 1157, "target": "ButlerSessionManager", "ty...
- ... and 90 more
## CAPABILITY: AUTOMATION
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
- ExecutionRegistryDiscoveryAgent (file: A_04_AGENTS/ProjectDocumentationDepartment/Core/Discovery/execution_registr...
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
- A_02_MANAGERS.TaskRunner.ExecutionAdapters.base_adapter (file: A_02_MANAGERS/TaskRunner/ExecutionAdapters/powershe...
- A_02_MANAGERS.TaskRunner.ExecutionAdapters.base_adapter (file: A_02_MANAGERS/TaskRunner/ExecutionAdapters/python_a...
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
- {"metadata": {"alias": null, "kind": "from", "line": 11, "name": "ExecutionHistory"}, "source": 294, "target": "A_...
- {"metadata": {"alias": null, "kind": "from", "line": 11, "name": "ExecutionResult"}, "source": 339, "target": "A_0...
- {"metadata": {"alias": null, "kind": "from", "line": 11, "name": "PolicyLoader"}, "source": 297, "target": "A_02_M...
- {"metadata": {"alias": null, "kind": "from", "line": 11, "name": "PolicyLoader"}, "source": 298, "target": "A_02_M...
- {"metadata": {"alias": null, "kind": "from", "line": 11, "name": "PythonExecutionAdapter"}, "source": 346, "target...
- {"metadata": {"alias": null, "kind": "from", "line": 12, "name": "ExecutionResult"}, "source": 343, "target": "A_0...
- {"metadata": {"alias": null, "kind": "from", "line": 12, "name": "ExecutionResult"}, "source": 344, "target": "A_0...
- {"metadata": {"alias": null, "kind": "from", "line": 12, "name": "RecipeWriter"}, "source": 305, "target": "A_02_M...
- {"metadata": {"alias": null, "kind": "from", "line": 13, "name": "BaseExecutionAdapter"}, "source": 343, "target":...
- {"metadata": {"alias": null, "kind": "from", "line": 13, "name": "BaseExecutionAdapter"}, "source": 344, "target":...
- {"metadata": {"alias": null, "kind": "from", "line": 13, "name": "Recipe"}, "source": 348, "target": "A_07_CONFIG....
- {"metadata": {"alias": null, "kind": "from", "line": 13, "name": "RecipeStep"}, "source": 348, "target": "A_07_CON...
- {"metadata": {"alias": null, "kind": "from", "line": 13, "name": "run_once"}, "source": 305, "target": "A_02_MANAG...
- {"metadata": {"alias": null, "kind": "from", "line": 14, "name": "ExecutionResult"}, "source": 348, "target": "A_0...
- {"metadata": {"alias": null, "kind": "from", "line": 14, "name": "ExecutionState"}, "source": 295, "target": "A_02...
- {"metadata": {"alias": null, "kind": "from", "line": 14, "name": "PowerShellExecutionAdapter"}, "source": 346, "ta...
- {"metadata": {"alias": null, "kind": "from", "line": 14, "name": "RecipeBuilder"}, "source": 309, "target": "A_02_...
- {"metadata": {"alias": null, "kind": "from", "line": 14, "name": "RecipeQueueWatcher"}, "source": 358, "target": "...
- {"metadata": {"alias": null, "kind": "from", "line": 15, "name": "ExecutorFactory"}, "source": 348, "target": "A_0...
- {"metadata": {"alias": null, "kind": "from", "line": 15, "name": "Recipe"}, "source": 347, "target": "A_07_CONFIG....
- ... and 106 more
## CAPABILITY: QUEUE
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
- ExecutionRegistryDiscoveryAgent (file: A_04_AGENTS/ProjectDocumentationDepartment/Core/Discovery/execution_registr...
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
- A_02_MANAGERS.TaskRunner.ExecutionAdapters.base_adapter (file: A_02_MANAGERS/TaskRunner/ExecutionAdapters/powershe...
- A_02_MANAGERS.TaskRunner.ExecutionAdapters.base_adapter (file: A_02_MANAGERS/TaskRunner/ExecutionAdapters/python_a...
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
- {"metadata": {"alias": null, "kind": "from", "line": 11, "name": "ExecutionHistory"}, "source": 294, "target": "A_...
- {"metadata": {"alias": null, "kind": "from", "line": 11, "name": "ExecutionResult"}, "source": 339, "target": "A_0...
- {"metadata": {"alias": null, "kind": "from", "line": 11, "name": "PolicyLoader"}, "source": 297, "target": "A_02_M...
- {"metadata": {"alias": null, "kind": "from", "line": 11, "name": "PolicyLoader"}, "source": 298, "target": "A_02_M...
- {"metadata": {"alias": null, "kind": "from", "line": 11, "name": "PythonExecutionAdapter"}, "source": 346, "target...
- {"metadata": {"alias": null, "kind": "from", "line": 12, "name": "ExecutionResult"}, "source": 343, "target": "A_0...
- {"metadata": {"alias": null, "kind": "from", "line": 12, "name": "ExecutionResult"}, "source": 344, "target": "A_0...
- {"metadata": {"alias": null, "kind": "from", "line": 12, "name": "RecipeWriter"}, "source": 305, "target": "A_02_M...
- {"metadata": {"alias": null, "kind": "from", "line": 13, "name": "BaseExecutionAdapter"}, "source": 343, "target":...
- {"metadata": {"alias": null, "kind": "from", "line": 13, "name": "BaseExecutionAdapter"}, "source": 344, "target":...
- {"metadata": {"alias": null, "kind": "from", "line": 13, "name": "Recipe"}, "source": 348, "target": "A_07_CONFIG....
- {"metadata": {"alias": null, "kind": "from", "line": 13, "name": "RecipeStep"}, "source": 348, "target": "A_07_CON...
- {"metadata": {"alias": null, "kind": "from", "line": 13, "name": "run_once"}, "source": 305, "target": "A_02_MANAG...
- {"metadata": {"alias": null, "kind": "from", "line": 14, "name": "ExecutionResult"}, "source": 348, "target": "A_0...
- {"metadata": {"alias": null, "kind": "from", "line": 14, "name": "ExecutionState"}, "source": 295, "target": "A_02...
- {"metadata": {"alias": null, "kind": "from", "line": 14, "name": "PowerShellExecutionAdapter"}, "source": 346, "ta...
- {"metadata": {"alias": null, "kind": "from", "line": 14, "name": "RecipeBuilder"}, "source": 309, "target": "A_02_...
- {"metadata": {"alias": null, "kind": "from", "line": 14, "name": "RecipeQueueWatcher"}, "source": 358, "target": "...
- {"metadata": {"alias": null, "kind": "from", "line": 15, "name": "ExecutorFactory"}, "source": 348, "target": "A_0...
- {"metadata": {"alias": null, "kind": "from", "line": 15, "name": "Recipe"}, "source": 347, "target": "A_07_CONFIG....
- ... and 106 more
## CAPABILITY: WATCHER
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
- {"metadata": {"context": "run", "line": 21}, "source": 357, "target": "RecipeQueueWatcher", "type": "call"} (file:...
- {"metadata": {"context": "run_once", "line": 25}, "source": 358, "target": "RecipeQueueWatcher", "type": "call"} (...
- {"metadata": {"context": null, "line": 39}, "source": 350, "target": "RecipeQueueWatcher", "type": "call"} (file: ...
## CAPABILITY: REGISTRY
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
- ExecutionRegistryDiscoveryAgent (file: A_04_AGENTS/ProjectDocumentationDepartment/Core/Discovery/execution_registr...
- GoalsRegistryDiscoveryAgent (file: A_04_AGENTS/ProjectDocumentationDepartment/Core/Discovery/goals_registry_discov...
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
- A_02_MANAGERS.RuntimeCapabilityRegistry.capability_schema (file: A_02_MANAGERS/RuntimeCapabilityRegistry/runtime_r...
- A_02_MANAGERS.RuntimeCapabilityRegistry.runtime_registry (file: 1081)
### LINKS:
- {"metadata": {"alias": null, "kind": "from", "line": 15, "name": "RuntimeCapabilityRegistry"}, "source": 1081, "ta...
- {"metadata": {"alias": null, "kind": "from", "line": 9, "name": "RuntimeCapability"}, "source": 320, "target": "A_...
- {"metadata": {"context": "BootstrapCore.__init__", "line": 16}, "source": 1495, "target": "RegistryBrain", "type":...
- {"metadata": {"context": "ButlerSystem.__init__", "line": 15}, "source": 1505, "target": "RegistryBrain", "type": ...
- {"metadata": {"context": "EngineeringPipeline.collect", "line": 56}, "source": 536, "target": "RegistryScanner", "...
- {"metadata": {"context": "EngineeringPipeline.collect", "line": 56}, "source": 591, "target": "RegistryScanner", "...
- {"metadata": {"context": "LoopOrchestratorV3_MASTER_TRUTH.__init__", "line": 48}, "source": 1117, "target": "Execu...
- {"metadata": {"context": "ProjectState.__init__", "line": 11}, "source": 1102, "target": "RegistryLoader", "type":...
- {"metadata": {"context": "ProjectState.__init__", "line": 11}, "source": 1103, "target": "RegistryLoader", "type":...
- {"metadata": {"context": "RouterIntegration.__init__", "line": 22}, "source": 123, "target": "RouterRegistry", "ty...
- {"metadata": {"context": "RouterIntegration.__init__", "line": 22}, "source": 467, "target": "RouterRegistry", "ty...
- {"metadata": {"context": "RouterIntegration.__init__", "line": 25}, "source": 468, "target": "RouterRegistry", "ty...
- {"metadata": {"context": "Worker.__init__", "line": 35}, "source": 477, "target": "RouterRegistry", "type": "call"...
- {"metadata": {"context": null, "line": 23}, "source": 469, "target": "RouterRegistry", "type": "call"} (file: None)
- {"metadata": {"context": null, "line": 23}, "source": 470, "target": "RouterRegistry", "type": "call"} (file: None)
- {"metadata": {"context": null, "line": 26}, "source": 1454, "target": "register_test_job", "type": "call"} (file: ...
- {"metadata": {"context": null, "line": 34}, "source": 1106, "target": "RegistryLoader", "type": "call"} (file: None)
- {"metadata": {"context": null, "line": 37}, "source": 387, "target": "HandlerRegistry", "type": "call"} (file: None)
- {"metadata": {"context": null, "line": 38}, "source": 1441, "target": "reset_and_register", "type": "call"} (file:...
- {"metadata": {"context": null, "line": 47}, "source": 1107, "target": "RegistryValidator", "type": "call"} (file: ...
- ... and 1 more
## CAPABILITY: DISPATCHER
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
- {"metadata": {"alias": null, "kind": "from", "line": 10, "name": "SmartDispatcher"}, "source": 227, "target": "A_0...
- {"metadata": {"alias": null, "kind": "from", "line": 157, "name": "dispatch"}, "source": 414, "target": "A_03_ORCH...
- {"metadata": {"alias": null, "kind": "from", "line": 3, "name": "SmartDispatcherV2"}, "source": 1513, "target": "A...
- {"metadata": {"alias": null, "kind": "from", "line": 3, "name": "SmartDispatcherV2"}, "source": 430, "target": "A_...
- {"metadata": {"alias": null, "kind": "from", "line": 3, "name": "dispatch"}, "source": 1363, "target": "A_03_ORCHE...
- {"metadata": {"alias": null, "kind": "from", "line": 3, "name": "dispatch"}, "source": 1423, "target": "A_03_ORCHE...
- {"metadata": {"alias": null, "kind": "from", "line": 7, "name": "SmartDispatcherV2"}, "source": 534, "target": "A_...
- {"metadata": {"alias": null, "kind": "from", "line": 7, "name": "SmartDispatcherV2"}, "source": 589, "target": "A_...
- {"metadata": {"alias": null, "kind": "from", "line": 8, "name": "SmartDispatcherV2"}, "source": 1393, "target": "A...
- {"metadata": {"alias": null, "kind": "from", "line": 8, "name": "_dispatcher"}, "source": 1394, "target": "A_03_OR...
- {"metadata": {"alias": null, "kind": "from", "line": 9, "name": "SmartDispatcherV2"}, "source": 549, "target": "A_...
- {"metadata": {"alias": null, "kind": "from", "line": 9, "name": "SmartDispatcherV2"}, "source": 597, "target": "A_...
- {"metadata": {"args": [], "kind": "constructor", "line": 33}, "source": 365, "target": "Dispatcher", "type": "regi...
- {"metadata": {"context": "ButlerInteractiveChat.__init__", "line": 38}, "source": 241, "target": "DispatcherAgent"...
- {"metadata": {"context": "DispatcherScanner.scan", "line": 18}, "source": 549, "target": "SmartDispatcherV2", "typ...
- {"metadata": {"context": "DispatcherScanner.scan", "line": 18}, "source": 597, "target": "SmartDispatcherV2", "typ...
- {"metadata": {"context": "DreamDispatcherAdapter.__init__", "line": 9}, "source": 432, "target": "DispatcherAgent"...
- {"metadata": {"context": "FactoryCoreBridge.handle", "line": 26}, "source": 434, "target": "_dispatch", "type": "c...
- {"metadata": {"context": "ProfessorAdapter.__init__", "line": 9}, "source": 465, "target": "DispatcherAgent", "typ...
- {"metadata": {"context": "RouterIntegration.__init__", "line": 21}, "source": 123, "target": "AgentRouter", "type"...
- ... and 53 more
## CAPABILITY: GUARDIAN
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
- {"metadata": {"alias": null, "kind": "from", "line": 11, "name": "ExecutionHistory"}, "source": 294, "target": "A_...
- {"metadata": {"alias": null, "kind": "from", "line": 14, "name": "ExecutionState"}, "source": 295, "target": "A_02...
- {"metadata": {"alias": null, "kind": "from", "line": 9, "name": "SystemState"}, "source": 305, "target": "A_02_MAN...
- {"metadata": {"context": "SecurityValidator.validate", "line": 41}, "source": 359, "target": "SecurityViolation", ...
- {"metadata": {"context": "SecurityValidator.validate", "line": 51}, "source": 359, "target": "SecurityViolation", ...
- {"metadata": {"context": "execute_repair", "line": 88}, "source": 1486, "target": "run_memory_guardian", "type": "...
- {"metadata": {"context": "main", "line": 118}, "source": 1486, "target": "run_memory_guardian", "type": "call"} (f...
- {"metadata": {"context": "main", "line": 121}, "source": 1486, "target": "run_memory_guardian", "type": "call"} (f...
- {"metadata": {"context": "run", "line": 21}, "source": 357, "target": "RecipeQueueWatcher", "type": "call"} (file:...
- {"metadata": {"context": "run_once", "line": 25}, "source": 358, "target": "RecipeQueueWatcher", "type": "call"} (...
- {"metadata": {"context": null, "line": 144}, "source": 231, "target": "run_guardian", "type": "call"} (file: None)
- {"metadata": {"context": null, "line": 229}, "source": 219, "target": "run_memory_guardian", "type": "call"} (file...
- {"metadata": {"context": null, "line": 39}, "source": 293, "target": "ExecutionMonitor", "type": "call"} (file: None)
- {"metadata": {"context": null, "line": 39}, "source": 350, "target": "RecipeQueueWatcher", "type": "call"} (file: ...
## CAPABILITY: AUDIT
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
- {"metadata": {"alias": null, "kind": "from", "line": 3, "name": "ProjectAuditor"}, "source": 1353, "target": "A_04...
- {"metadata": {"context": "EngineeringPipeline.collect", "line": 62}, "source": 536, "target": "AuditScanner", "typ...
- {"metadata": {"context": "EngineeringPipeline.collect", "line": 62}, "source": 591, "target": "AuditScanner", "typ...
- {"metadata": {"context": "TestProjectAuditor.test_stub", "line": 8}, "source": 1353, "target": "ProjectAuditor", "...
- {"metadata": {"context": "build_state", "line": 231}, "source": 223, "target": "write_audit_log", "type": "call"} ...
- {"metadata": {"context": "create_architecture_snapshot", "line": 120}, "source": 223, "target": "write_audit_log",...
- {"metadata": {"context": "rebuild_lock_manifest", "line": 153}, "source": 223, "target": "write_audit_log", "type"...
- {"metadata": {"context": null, "line": 30}, "source": 548, "target": "AuditScanner", "type": "call"} (file: None)
- {"metadata": {"context": null, "line": 30}, "source": 596, "target": "AuditScanner", "type": "call"} (file: None)
## CAPABILITY: PASSPORT
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
- {"metadata": {"context": "ButlerHarness.execute", "line": 134}, "source": 399, "target": "ProjectPassportLoader", ...
- {"metadata": {"context": "ButlerOSAdapter.__init__", "line": 11}, "source": 405, "target": "ProjectPassportLoader"...
- {"metadata": {"context": "ChatCoreBridge.process", "line": 12}, "source": 205, "target": "load_profile", "type": "...
- {"metadata": {"context": "ChatRouterMirror.route", "line": 11}, "source": 419, "target": "load_profile", "type": "...
- {"metadata": {"context": "EngineeringPipeline.collect", "line": 55}, "source": 536, "target": "PassportScanner", "...
- {"metadata": {"context": "EngineeringPipeline.collect", "line": 55}, "source": 591, "target": "PassportScanner", "...
- {"metadata": {"context": "MemoryCore.__init__", "line": 8}, "source": 218, "target": "load_profile", "type": "call...
- {"metadata": {"context": "MemoryFacadeV2.get_passport_string", "line": 16}, "source": 1155, "target": "PassportRep...
- {"metadata": {"context": "ProjectState.__init__", "line": 10}, "source": 1102, "target": "ProjectPassportLoader", ...
- {"metadata": {"context": "ProjectState.__init__", "line": 10}, "source": 1103, "target": "ProjectPassportLoader", ...
- {"metadata": {"context": "RouterIntegration.__init__", "line": 23}, "source": 123, "target": "PassportCommandHandl...
- {"metadata": {"context": "RouterIntegration.__init__", "line": 23}, "source": 467, "target": "PassportCommandHandl...
- {"metadata": {"context": "RouterIntegration.__init__", "line": 26}, "source": 468, "target": "PassportCommandHandl...
- {"metadata": {"context": "add_episode", "line": 222}, "source": 1165, "target": "load_profile", "type": "call"} (f...
- {"metadata": {"context": "add_episode", "line": 232}, "source": 1165, "target": "save_profile", "type": "call"} (f...
- {"metadata": {"context": "add_episode", "line": 233}, "source": 1165, "target": "save_profile", "type": "call"} (f...
- {"metadata": {"context": "add_skill", "line": 161}, "source": 1165, "target": "load_profile", "type": "call"} (fil...
- {"metadata": {"context": "add_skill", "line": 172}, "source": 1165, "target": "save_profile", "type": "call"} (fil...
- {"metadata": {"context": "delete_fact", "line": 56}, "source": 1165, "target": "load_profile", "type": "call"} (fi...
- {"metadata": {"context": "delete_fact", "line": 65}, "source": 1165, "target": "save_profile", "type": "call"} (fi...
- ... and 16 more
## CAPABILITY: REASONING
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
- {"metadata": {"alias": null, "kind": "from", "line": 2, "name": "MemoryDepartment"}, "source": 1340, "target": "A_...
- {"metadata": {"alias": null, "kind": "from", "line": 3, "name": "MemoryAdvisor"}, "source": 1347, "target": "A_04_...
- {"metadata": {"alias": null, "kind": "from", "line": 4, "name": "MemoryDepartment"}, "source": 1285, "target": "A_...
- {"metadata": {"alias": null, "kind": "from", "line": 4, "name": "MemoryDepartment"}, "source": 1287, "target": "A_...
- {"metadata": {"alias": null, "kind": "from", "line": 4, "name": "MemoryDepartment"}, "source": 324, "target": "A_0...
- {"metadata": {"alias": null, "kind": "from", "line": 4, "name": "MemoryDepartment"}, "source": 338, "target": "A_0...
- {"metadata": {"context": "AgentLoopExecutor.__init__", "line": 10}, "source": 1114, "target": "ProjectHistory", "t...
- {"metadata": {"context": "AttentionMemory.__init__", "line": 14}, "source": 1124, "target": "MemoryReplay", "type"...
- {"metadata": {"context": "BootstrapCore.__init__", "line": 15}, "source": 1495, "target": "SelfHealingMemory", "ty...
- {"metadata": {"context": "ButlerOSAdapter.__init__", "line": 12}, "source": 405, "target": "ProjectMemoryLoader", ...
- {"metadata": {"context": "ButlerOSAdapter.memory_summary", "line": 15}, "source": 405, "target": "get_memory_summa...
- {"metadata": {"context": "ButlerSystem.__init__", "line": 14}, "source": 1505, "target": "SelfHealingMemory", "typ...
- {"metadata": {"context": "ChatCoreBridge.__init__", "line": 7}, "source": 205, "target": "SemanticLayer", "type": ...
- {"metadata": {"context": "ChatRouterMirror.__init__", "line": 7}, "source": 419, "target": "SemanticLayer", "type"...
- {"metadata": {"context": "ContextBudgetManager.__init__", "line": 15}, "source": 1136, "target": "AttentionMemory"...
- {"metadata": {"context": "ContextBudgetManager.__init__", "line": 16}, "source": 1136, "target": "MemoryOrchestrat...
- {"metadata": {"context": "CoreKernel.__init__", "line": 9}, "source": 207, "target": "SemanticLayer", "type": "cal...
- {"metadata": {"context": "CoreOrchestrator.__init__", "line": 7}, "source": 208, "target": "SemanticLayer", "type"...
- {"metadata": {"context": "CoreOrchestrator.__init__", "line": 8}, "source": 208, "target": "MemoryCore", "type": "...
- {"metadata": {"context": "DispatcherAgent.__init__", "line": 25}, "source": 508, "target": "SemanticMemory", "type...
- ... and 81 more
## CAPABILITY: SEMANTIC
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
- {"metadata": {"alias": null, "kind": "from", "line": 2, "name": "MemoryDepartment"}, "source": 1340, "target": "A_...
- {"metadata": {"alias": null, "kind": "from", "line": 3, "name": "MemoryAdvisor"}, "source": 1347, "target": "A_04_...
- {"metadata": {"alias": null, "kind": "from", "line": 4, "name": "MemoryDepartment"}, "source": 1285, "target": "A_...
- {"metadata": {"alias": null, "kind": "from", "line": 4, "name": "MemoryDepartment"}, "source": 1287, "target": "A_...
- {"metadata": {"alias": null, "kind": "from", "line": 4, "name": "MemoryDepartment"}, "source": 324, "target": "A_0...
- {"metadata": {"alias": null, "kind": "from", "line": 4, "name": "MemoryDepartment"}, "source": 338, "target": "A_0...
- {"metadata": {"context": "AgentLoopExecutor.__init__", "line": 10}, "source": 1114, "target": "ProjectHistory", "t...
- {"metadata": {"context": "AttentionMemory.__init__", "line": 14}, "source": 1124, "target": "MemoryReplay", "type"...
- {"metadata": {"context": "BootstrapCore.__init__", "line": 15}, "source": 1495, "target": "SelfHealingMemory", "ty...
- {"metadata": {"context": "ButlerOSAdapter.__init__", "line": 12}, "source": 405, "target": "ProjectMemoryLoader", ...
- {"metadata": {"context": "ButlerOSAdapter.memory_summary", "line": 15}, "source": 405, "target": "get_memory_summa...
- {"metadata": {"context": "ButlerSystem.__init__", "line": 14}, "source": 1505, "target": "SelfHealingMemory", "typ...
- {"metadata": {"context": "ChatCoreBridge.__init__", "line": 7}, "source": 205, "target": "SemanticLayer", "type": ...
- {"metadata": {"context": "ChatRouterMirror.__init__", "line": 7}, "source": 419, "target": "SemanticLayer", "type"...
- {"metadata": {"context": "ContextBudgetManager.__init__", "line": 15}, "source": 1136, "target": "AttentionMemory"...
- {"metadata": {"context": "ContextBudgetManager.__init__", "line": 16}, "source": 1136, "target": "MemoryOrchestrat...
- {"metadata": {"context": "CoreKernel.__init__", "line": 9}, "source": 207, "target": "SemanticLayer", "type": "cal...
- {"metadata": {"context": "CoreOrchestrator.__init__", "line": 7}, "source": 208, "target": "SemanticLayer", "type"...
- {"metadata": {"context": "CoreOrchestrator.__init__", "line": 8}, "source": 208, "target": "MemoryCore", "type": "...
- {"metadata": {"context": "DispatcherAgent.__init__", "line": 25}, "source": 508, "target": "SemanticMemory", "type...
- ... and 81 more



``

---

# CONSTITUTION

Источник: `C:\Users\KOS\Desktop\Butler_Agent\BUTLER_OMEGA_SMART\A_00_ARCHITECTURE\CONSTITUTION.md`

``md
# КОНСТИТУЦИЯ BUTLER OMEGA v1.2.0

1. Запрещено терять или повреждать пользовательские данные.
2. `file_hash` является главным идентификатором содержимого.
3. Повторная обработка одинакового содержимого запрещена.
4. `RUN_PIPELINE.py` не имеет права запускаться без Memory Guardian.
5. Автоматический ремонт обязан создавать резервную копию базы данных.
6. Любое изменение критического кода должно фиксироваться в PROJECT_STATE.json и CHANGELOG.md.
7. При сомнении система должна переходить в SAFE MODE, а не продолжать работу вслепую.
8. Критическое нарушение схемы БД блокирует запуск.
9. Дубликаты непустых `file_hash` блокируют запуск.
10. Автоматическое изменение кода без проверки компиляции запрещено.
---

# ПОПРАВКИ ПЕРИОДА СТРОИТЕЛЬСТВА v2.0

## ТРИ СВЯЩЕННЫХ СЛОВА

**КОНСТИТУЦИЯ. БЕЗОПАСНОСТЬ. ЯДРО.**

## 11. Безопасность прежде всего

Ни одно изменение кода не выполняется без возможности отката.

## 12. Ядро святое

Ядро проекта не используется как полигон для экспериментов.

## 13. Путь Калашникова

Любая новая функция проходит путь:

ИДЕЯ -> ЛАБОРАТОРИЯ -> ПРОВЕРКА -> ИСПЫТАНИЯ -> ВЖИВЛЕНИЕ В СИСТЕМУ

## 14. Никаких фальшивых заглушек

Модуль должен либо работать, либо честно сообщать, что функция не реализована.

## 15. Проверка после изменения

После изменения Python-файла обязательна проверка:

python -m py_compile <file>

## 16. Зелёная кнопка запуска

Главная кнопка запуска должна лежать в корне проекта и поднимать необходимые сервисы.

## 17. Начало рабочего дня

Перед работой: Конституция -> Безопасность -> Ядро -> План работ.

## 18. Точки восстановления

На этапе строительства хранить 100-200 точек восстановления.

## 19. SAFE MODE

При сомнении система останавливается и сигнализирует, а не продолжает вслепую.

## 20. Правило должно быть записано

Принятое правило считается действующим только после записи в Конституцию.

## 21. Граница проекта

Все файлы, отчёты, логи, результаты тестов, временные данные и рабочие артефакты Butler Omega должны сохраняться внутри папки проекта:

C:\Users\KOS\Desktop\Butler_Agent\BUTLER_OMEGA

Выход за пределы папки Butler Omega запрещён без отдельного согласованного решения.

Допустимая внешняя зона только по специальному решению:
C:\Users\KOS\Desktop\Butler_Agent

Запрещено самовольно сохранять рабочие данные в:
- C:\Users\KOS
- C:\Users\KOS\REPORTS
- случайные папки PowerShell
- системные каталоги Windows

Если модуль не знает, куда сохранять результат, он обязан остановиться и сообщить ошибку, а не писать куда попало.


## 22. КОДИРОВКА И POWERSHELL

1. Все текстовые файлы проекта сохраняются в UTF-8 БЕЗ BOM.
2. user_profile.json — единственный источник истины для пользовательских фактов.
3. USER_MEMORY.md генерируется автоматически из user_profile.json.
4. MEMORY.md содержит только конституцию, архитектурные правила и неизменяемые принципы.
5. В JSON запрещено записывать Markdown или произвольный текст.
6. Все PowerShell-блоки должны быть самодостаточными и готовыми к вставке целиком.
7. Запрещается публиковать незавершённые конструкции, которые ломаются при копировании.
8. После изменения Python-файлов выполнять:
   python -m py_compile <имя_файла>
9. Перед массовыми изменениями создавать резервную копию.
10. При малейшем сомнении сначала выполнить проверку, затем модификацию.


## ПРАВИЛО. ЛОКАЛЬНАЯ РАБОТА И СЕТЕВАЯ БЕЗОПАСНОСТЬ

1. Butler Omega имеет право работать с любыми локальными файлами и папками компьютера, если это необходимо для выполнения задачи пользователя.

2. Разрешается:
   - создание, чтение, изменение и перемещение локальных файлов;
   - создание папок и резервных копий;
   - анализ документов, изображений и других локальных данных;
   - использование локальных Git-команд, не требующих доступа в Интернет (например: git status).

3. Категорически запрещается без явного разрешения пользователя:
   - любые обращения в Интернет;
   - git pull;
   - git push;
   - git fetch;
   - git clone;
   - ollama pull;
   - автоматическая загрузка моделей;
   - автоматическое скачивание файлов;
   - обращения к внешним API и облачным сервисам;
   - любые иные сетевые операции.

4. При малейшем сомнении Butler обязан остановиться и запросить подтверждение пользователя до выполнения сетевого действия.

``

---

# SMART DISPATCHER V2

Источник: `C:\Users\KOS\Desktop\Butler_Agent\BUTLER_OMEGA_SMART\A_02_MANAGERS\smart_dispatcher_v2.py`

``py
# -*- coding: utf-8 -*-

from A_04_AGENTS.CodingDepartment.runner import CodingDepartment
from A_04_AGENTS.MemoryDepartment.runner import MemoryDepartment
from A_04_AGENTS.VisionDepartment.runner import VisionDepartment
from A_04_AGENTS.ImageDepartment.runner import ImageDepartment
from A_04_AGENTS.AudioDepartment.runner import AudioDepartment
from A_04_AGENTS.TextDepartment.runner import TextDepartment
from A_04_AGENTS.VideoDepartment.runner import VideoDepartment
from A_04_AGENTS.ArchiveDepartment.runner import ArchiveDepartment
from A_04_AGENTS.SearchDepartment.runner import SearchDepartment
from A_04_AGENTS.DocumentsDepartment.runner import DocumentsDepartment
from A_04_AGENTS.OpenDocumentDepartment.runner import OpenDocumentDepartment
from A_04_AGENTS.ProjectDocumentationDepartment.runner import ProjectDocumentationDepartment
from A_04_AGENTS.HomeDepartment.runner import HomeDepartment
from A_07_MEMORY.semantic_memory import SemanticMemory
from A_07_MEMORY.semantic_reasoning_engine import SemanticReasoningEngine
from A_03_ORCHESTRATION.butler_harness import ButlerHarness
from A_02_MANAGERS.smart_dispatcher import SmartDispatcher
from A_02_MANAGERS.goal_manager import GoalManager


class SmartDispatcherV2:

    def __init__(self):
        self.semantic_memory = SemanticMemory()
        self.reasoning_engine = SemanticReasoningEngine()
        self.harness = ButlerHarness()
        self.chat_provider = SmartDispatcher()

        self.departments = [
            GoalManager(),
            HomeDepartment(),
            SearchDepartment(),
            OpenDocumentDepartment(),
            DocumentsDepartment(),
            ProjectDocumentationDepartment(),
            CodingDepartment(),
            MemoryDepartment(),
            VisionDepartment(),
            ImageDepartment(),
            AudioDepartment(),
            TextDepartment(),
            VideoDepartment(),
            ArchiveDepartment(),
        ]

    def _dept_name(self, dept):
        return str(
            getattr(
                dept,
                "NAME",
                getattr(dept, "name", type(dept).__name__)
            )
        ).upper()

    def _execute_department(self, dept, query, context=None):

        def executor():

            try:
                return dept.execute(query, context=context)
            except TypeError:
                return dept.execute(query)

        harness_result = self.harness.execute(
            department_name=self._dept_name(dept),
            task=query,
            executor=executor
        )

        if harness_result.get("committed"):
            return harness_result.get("commit_result")

        return harness_result

    def _execute_chat(self, query):

        def executor():

            provider_result = self.chat_provider.execute_employee(
                employee="chat",
                system_prompt=(
                    "Ты Butler Omega Smart. Отвечай пользователю по-русски, "
                    "содержательно и по существу. Верни только готовый ответ."
                ),
                user_content=query,
            )

            text = str(provider_result.get("text") or "").strip()
            if provider_result.get("status") != "ok" or not text:
                return {
                    "ok": False,
                    "department": "CHAT",
                    "model": provider_result.get("model"),
                    "latency_ms": provider_result.get("latency_ms", 0),
                    "text": "Не удалось получить ответ CHAT-модели.",
                    "error": "CHAT_PROVIDER_ERROR",
                    "metadata": {
                        "provider": "SmartDispatcher.execute_employee",
                        "reason": provider_result.get("fallback_reason"),
                    },
                }

            return {
                "ok": True,
                "department": "CHAT",
                "model": provider_result.get("model"),
                "latency_ms": provider_result.get("latency_ms", 0),
                "text": text,
                "error": None,
                "metadata": {
                    "provider": "SmartDispatcher.execute_employee",
                    "request_id": provider_result.get("request_id"),
                },
            }

        harness_result = self.harness.execute(
            department_name="CHAT",
            task=query,
            executor=executor,
        )

        if harness_result.get("committed"):
            return harness_result.get("commit_result")

        return harness_result

    def dispatch(self, query: str, context: dict = None):

        context = dict(context or {})

        try:
            context["semantic"] = self.reasoning_engine.reason(
                query=query,
                candidates=[
                    self._dept_name(d)
                    for d in self.departments
                ]
            )
        except Exception:
            context["semantic"] = {
                "query": query,
                "tokens": [],
                "matches": []
            }


        for dept in self.departments:

            try:
                try:
                    handled = dept.can_handle(query, context=context)
                except TypeError:
                    handled = dept.can_handle(query)

                if not handled:
                    continue

                try:
                    return self._execute_department(dept, query, context=context)

                except Exception as ex:
                    return {
                        "ok": False,
                        "department": self._dept_name(dept),
                        "error": str(ex)
                    }

            except Exception:
                continue

        try:
            reasoning = context.get("semantic", {})

            if reasoning.get("matches"):
                matches = reasoning["matches"]
            else:
                matches = self.semantic_memory.search_by_text(query)


            if matches:
                target = str(matches[0].get("handler", "")).upper()

                for dept in self.departments:
                    if self._dept_name(dept) == target:
                        try:
                            return self._execute_department(dept, query, context=context)
                        except Exception as ex:
                            return {
                                "ok": False,
                                "department": self._dept_name(dept),
                                "skill_router": True,
                                "error": str(ex)
                            }

        except Exception as ex:
            return {
                "ok": False,
                "department": "SKILL_ROUTER",
                "error": str(ex)
            }

        return self._execute_chat(query)


if __name__ == "__main__":
    d = SmartDispatcherV2()

    for q in [
        "привет",
        "напиши функцию на python",
        "создай картинку дракона",
        "что изображено файл: C:\\test.jpg"
    ]:
        print(q, "=>", d.dispatch(q).get("department"))










``

---

# BUTLER HARNESS

Источник: `C:\Users\KOS\Desktop\Butler_Agent\BUTLER_OMEGA_SMART\A_03_ORCHESTRATION\butler_harness.py`

``py
# -*- coding: utf-8 -*-

from datetime import datetime
from pathlib import Path
import traceback

# Импортируем созданный и проверенный контур гвардов
from A_03_ORCHESTRATION.guards.frozen_core_guard import FrozenCoreGuard
from A_03_ORCHESTRATION.guards.rollback_guard import RollbackGuard
from A_03_ORCHESTRATION.guards.compile_guard import CompileGuard
from A_03_ORCHESTRATION.guards.integration_test_guard import IntegrationTestGuard
from A_03_ORCHESTRATION.observation_layer import ObservationLayer
from A_03_ORCHESTRATION.department_result import (
    RESULT_CONTROLLED_FAILURE,
    RESULT_INVALID,
    RESULT_NO_RESULT,
    RESULT_SUCCESS,
    validate_department_result,
)


class ButlerHarness:

    def __init__(self):
        self.version = "3.0_STABLE"
        self.observation = ObservationLayer()
        self.project_root = Path(__file__).resolve().parents[1]

        # Инициализируем обойму гвардов
        self.guards = [
            ("FrozenCore", FrozenCoreGuard()),
            ("Rollback", RollbackGuard()),
            ("Compile", CompileGuard()),
            ("IntegrationTest", IntegrationTestGuard())
        ]

    def validate(self, draft):
        """Обратная совместимость: базовая проверка артефакта постфактум."""
        return validate_department_result(draft, "UNKNOWN")["valid"]

    def commit(self, draft):
        return draft

    def execute(
        self,
        department_name,
        task,
        executor,
        auto_commit=True,
        cr_name="CR_000_TEST.json" # По умолчанию используем наш верифицированный CR
    ):
        result = {
            "ok": False,
            "department": department_name,
            "model": None,
            "latency_ms": 0,
            "text": "",
            "error": None,
            "metadata": {},
            "draft": None,
            "validated": False,
            "committed": False,
            "timestamp": datetime.now().isoformat(),
            "pipeline_status": "PENDING",
            "result_outcome": "PENDING",
        }

        # 1. Логируем старт пайплайна безопасности
        self.observation.record(
            source=department_name,
            event="HARNESS_V3_START",
            payload={"task": str(task), "cr_target": cr_name}
        )

        # Вычисляем путь к Change Request заявке от корня проекта
        cr_path = Path("A_00_ARCHITECTURE") / "CHANGE_REQUESTS" / cr_name

        # 2. ФАЗА ПРЕ-ФЛАЙТ КОНТРОЛЯ: ПОСЛЕДОВАТЕЛЬНЫЙ ПРОГОН ЦЕПОЧКИ ГВАРДОВ
        for guard_name, guard_instance in self.guards:
            try:
                guard_result = guard_instance.validate(cr_path)

                # Логируем атомарный проход каждого защитника в общую jsonl ленту
                self.observation.record(
                    source=f"Harness_Guard_{guard_name}",
                    event="GUARD_CHECK",
                    payload={"cr": cr_name, "result": guard_result}
                )

                if guard_result.get("status") == "REJECTED":
                    error_msg = f"Пайплайн заблокирован гвардом {guard_name}. Код: {guard_result.get('code')}. Причина: {guard_result.get('reason', 'Нет описания')}"

                    self.observation.record(
                        source=department_name,
                        event="HARNESS_V3_REJECTED",
                        payload={"guard": guard_name, "code": guard_result.get("code")}
                    )

                    result["pipeline_status"] = f"REJECTED_BY_{guard_name.upper()}"
                    result["error"] = error_msg
                    result["guard_code"] = guard_result.get("code")
                    result["result_outcome"] = "GUARD_REJECTED"
                    return result

            except Exception as ex:
                critical_error = f"Системный сбой внутри гварда {guard_name}: {str(ex)}"
                self.observation.record(
                    source=department_name,
                    event="HARNESS_GUARD_EXCEPTION",
                    payload={"guard": guard_name, "error": str(ex)}
                )
                result["pipeline_status"] = "SYSTEM_EXCEPTION"
                result["error"] = critical_error
                result["result_outcome"] = "EXCEPTION"
                result["metadata"]["diagnostics"] = {
                    "failure_source": f"Harness_Guard_{guard_name}",
                    "failure_stage": "pre_flight_guard",
                    "exception_type": type(ex).__name__,
                    "exception_message": str(ex),
                    "traceback": "\n".join(traceback.format_exc().strip().splitlines()[-10:]),
                }
                return result

        # 3. ФАЗА ИСПОЛНЕНИЯ (Допускается только при APPROVED от всех защитников)
        result["pipeline_status"] = "APPROVED_PRE_FLIGHT"

        try:
            draft = executor()
            result["draft"] = draft

            validation = validate_department_result(draft, department_name)
            result["result_outcome"] = validation["outcome"]
            result["metadata"]["result_validation"] = {
                "valid": validation["valid"],
                "outcome": validation["outcome"],
            }

            if validation["outcome"] == RESULT_NO_RESULT:
                self.observation.record(
                    source=department_name,
                    event="DEPARTMENT_NO_RESULT"
                )
                result["pipeline_status"] = RESULT_NO_RESULT
                result["error"] = validation["error"]
                return result

            if validation["outcome"] == RESULT_INVALID:
                self.observation.record(
                    source=department_name,
                    event="DEPARTMENT_INVALID_RESULT",
                    payload={"error": validation["error"]},
                )
                result["pipeline_status"] = RESULT_INVALID
                result["error"] = validation["error"]
                return result

            result["validated"] = True
            normalized = validation["normalized"]
            for key in (
                "ok", "department", "model", "latency_ms",
                "text", "error", "metadata"
            ):
                result[key] = normalized[key]

            if validation["outcome"] == RESULT_CONTROLLED_FAILURE:
                result["pipeline_status"] = RESULT_CONTROLLED_FAILURE
                if auto_commit:
                    result["commit_result"] = self.commit(normalized)
                    result["committed"] = True
                self.observation.record(
                    source=department_name,
                    event="DEPARTMENT_CONTROLLED_FAILURE",
                    payload={"error": normalized["error"]},
                )
                return result

            if auto_commit:
                result["commit_result"] = self.commit(normalized)
                result["committed"] = True
                result["pipeline_status"] = RESULT_SUCCESS

            self.observation.record(
                source=department_name,
                event="HARNESS_V3_SUCCESS",
                payload={"task": str(task)}
            )

            # [PASSPORT_ACTIVE_SYNC] Автоматическая фиксация живой системы
            if department_name == "SEARCH":
                try:
                    from A_07_CONFIG.project_passport_loader import ProjectPassportLoader
                    loader = ProjectPassportLoader()
                    loader.commit_proof("search_department_routing", "PROVEN")
                    loader.commit_proof("catalog_search_bridge", "PROVEN")
                    loader.commit_proof("4.24_active_sync_proof", "RUNNING_AUTOMATICALLY")
                    loader.evaluate_stage_transitions()
                except Exception as e:
                    print(f"[PASSPORT SYNC ERROR] {str(e)}")

            return result

        except Exception as ex:
            self.observation.record(
                source=department_name,
                event="EXECUTION_ERROR",
                payload={"error": str(ex)}
            )
            result["error"] = str(ex)
            result["pipeline_status"] = "EXECUTION_FAILED"
            result["result_outcome"] = "EXCEPTION"
            result["metadata"]["diagnostics"] = {
                "failure_source": department_name,
                "failure_stage": "department_execution",
                "exception_type": type(ex).__name__,
                "exception_message": str(ex),
                "traceback": "\n".join(traceback.format_exc().strip().splitlines()[-10:]),
            }
            return result


if __name__ == "__main__":
    import json
    harness = ButlerHarness()
    print("=== RUNTIME INTEGRATION TEST: BUTLER_HARNESS V3 ===")

    # Эмулируем работу абстрактного executor-а департамента
    def sample_executor():
        print(" -> [RUNNING] Executor транзакции запущен!")
        return {"status": "success", "payload": "data modified"}

    # Пробуем выполнить задачу. Так как бэкап router_integration.py сейчас старше 300с,
    # RollbackGuard обязан развернуть пайплайн до запуска sample_executor.
    print("\n[Пайплайн-Тест 1] Запуск execute() с существующим CR_000_TEST.json:")
    exec_result = harness.execute(
        department_name="ORCHESTRATION_TEST",
        task="Refactoring router integration layer",
        executor=sample_executor,
        cr_name="CR_000_TEST.json"
    )

    print("\nРезультат выполнения Harness Pipeline:")
    print(json.dumps(exec_result, indent=2, ensure_ascii=False))


``

---

# GOAL MANAGER

Источник: `C:\Users\KOS\Desktop\Butler_Agent\BUTLER_OMEGA_SMART\A_02_MANAGERS\goal_manager.py`

``py
# -*- coding: utf-8 -*-

import json
import threading
import uuid
from datetime import datetime, timezone
from pathlib import Path
from time import perf_counter


class GoalManager:
    """CRUD manager for user goals stored in the existing memory subsystem."""

    NAME = "GOAL_MANAGER"
    name = "GOAL_MANAGER"

    def __init__(self, storage_path=None):
        project_root = Path(__file__).resolve().parents[1]
        self.storage_path = Path(storage_path) if storage_path else project_root / "A_07_MEMORY" / "goals_registry.json"
        self._lock = threading.RLock()
        self._ensure_storage()

    def _now(self):
        return datetime.now(timezone.utc).isoformat()

    def _result(self, ok, text, error=None, **metadata):
        return {"ok": bool(ok), "text": str(text), "error": error, "metadata": metadata}

    def _ensure_storage(self):
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.storage_path.exists():
            self._save({"version": "1.0", "goals": []})

    def _load(self):
        try:
            data = json.loads(self.storage_path.read_text(encoding="utf-8-sig"))
            if not isinstance(data, dict) or not isinstance(data.get("goals"), list):
                raise ValueError("invalid goals registry")
            return data
        except Exception as exc:
            raise RuntimeError("GOALS_STORAGE_READ_ERROR") from exc

    def _save(self, data):
        temporary = self.storage_path.with_suffix(self.storage_path.suffix + ".tmp")
        try:
            temporary.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
            temporary.replace(self.storage_path)
        except Exception as exc:
            if temporary.exists():
                temporary.unlink()
            raise RuntimeError("GOALS_STORAGE_WRITE_ERROR") from exc

    def _find(self, data, goal_id):
        return next((goal for goal in data["goals"] if goal.get("id") == goal_id), None)

    def _resolve_goal_id(self, reference):
        reference = str(reference or "").strip()
        data = self._load()
        direct = self._find(data, reference)
        if direct:
            return direct["id"]
        lowered = reference.casefold()
        match = next(
            (goal for goal in data["goals"] if str(goal.get("title", "")).casefold() == lowered),
            None,
        )
        return match.get("id") if match else reference

    def can_handle(self, query, context=None):
        command = str(query or "").strip().casefold()
        return any(command.startswith(prefix) for prefix in ("goal ", "plan ", "progress ", "priority ", "reminder "))

    def execute(self, query, context=None, **kwargs):
        started = perf_counter()
        command = str(query or "").strip()
        lowered = command.casefold()

        try:
            if lowered.startswith("reminder "):
                result = self._execute_reminder_command(command, lowered)
            elif lowered.startswith("priority "):
                result = self._execute_priority_command(command, lowered)
            elif lowered.startswith("progress "):
                result = self._execute_progress_command(command, lowered)
            elif lowered.startswith("plan "):
                result = self._execute_plan_command(command, lowered)
            elif lowered.startswith("goal create "):
                result = self.create_goal(command[len("goal create "):])
            elif lowered == "goal list":
                result = self.list_goals()
            elif lowered.startswith("goal get "):
                reference = command[len("goal get "):]
                result = self.get_goal(self._resolve_goal_id(reference))
            elif lowered.startswith("goal update "):
                reference = command[len("goal update "):]
                result = self.update_goal(self._resolve_goal_id(reference), {"status": "active"})
            elif lowered.startswith("goal add task "):
                task_title = command[len("goal add task "):]
                active = self.list_goals({"status": "active"})
                goals = active.get("metadata", {}).get("goals", [])
                if not goals:
                    result = self._result(False, "Активная цель не найдена.", "GOAL_NOT_FOUND")
                else:
                    result = self.add_task_to_goal(goals[-1]["id"], task_title)
            elif lowered.startswith("goal progress "):
                reference = command[len("goal progress "):]
                result = self.get_goal_progress(self._resolve_goal_id(reference))
            elif lowered.startswith("goal delete "):
                reference = command[len("goal delete "):]
                result = self.delete_goal(self._resolve_goal_id(reference))
            else:
                result = self._result(False, "Неизвестная команда цели.", "INVALID_GOAL_COMMAND")
        except RuntimeError as exc:
            result = self._result(False, "Не удалось обработать команду цели.", str(exc))

        return {
            "ok": bool(result.get("ok")),
            "department": self.NAME,
            "model": "GoalManager",
            "latency_ms": max(0, int((perf_counter() - started) * 1000)),
            "text": str(result.get("text") or ""),
            "error": result.get("error"),
            "metadata": dict(result.get("metadata") or {}),
        }

    def _execute_priority_command(self, command, lowered):
        from A_02_MANAGERS.priority_engine import PriorityEngine

        engine = PriorityEngine(goal_manager=self)
        if lowered.startswith("priority calculate "):
            reference = command[len("priority calculate "):].strip()
            if reference.casefold() == "latest":
                tasks = [task for goal in self._load()["goals"] for task in goal.get("tasks", [])]
                reference = tasks[-1]["id"] if tasks else ""
            return engine.calculate_priority(reference)
        if lowered.startswith("priority list "):
            reference = command[len("priority list "):].strip()
            return engine.get_prioritized_tasks(self._resolve_goal_id(reference))
        if lowered.startswith("priority next "):
            reference = command[len("priority next "):].strip()
            return engine.next_task(self._resolve_goal_id(reference))
        return self._result(False, "Неизвестная команда приоритета.", "INVALID_PRIORITY_COMMAND")

    def _execute_reminder_command(self, command, lowered):
        from A_02_MANAGERS.reminder_engine import ReminderEngine

        engine = ReminderEngine(goal_manager=self)
        if lowered.startswith("reminder set "):
            arguments = command[len("reminder set "):].split(maxsplit=2)
            if len(arguments) < 2:
                return self._result(False, "Не указаны target и due_at.", "INVALID_REMINDER_COMMAND")
            target, due_at = arguments[:2]
            message = arguments[2] if len(arguments) > 2 else ""
            tasks = [task for goal in self._load()["goals"] for task in goal.get("tasks", [])]
            task_id = tasks[-1]["id"] if target.casefold() == "latest" and tasks else target
            goal = next((goal for goal in self._load()["goals"] if any(task.get("id") == task_id for task in goal.get("tasks", []))), None)
            if goal is None:
                return self._result(False, "Задача не найдена.", "TASK_NOT_FOUND", task_id=task_id)
            return engine.set_reminder(goal["id"], due_at, task_id=task_id, message=message)
        if lowered == "reminder list":
            return engine.list_reminders()
        if lowered == "reminder check":
            return engine.check_reminders()
        if lowered.startswith("reminder acknowledge "):
            reference = command[len("reminder acknowledge "):].strip()
            reminder_id = engine.latest_reminder_id() if reference.casefold() == "latest" else reference
            return engine.acknowledge_reminder(reminder_id or "")
        return self._result(False, "Неизвестная команда напоминания.", "INVALID_REMINDER_COMMAND")

    def _execute_plan_command(self, command, lowered):
        from A_02_MANAGERS.Planner.planner_manager import PlannerManager

        planner = PlannerManager(goal_manager=self)
        if lowered.startswith("plan generate "):
            reference = command[len("plan generate "):]
            return planner.generate_plan(self._resolve_goal_id(reference))
        if lowered.startswith("plan get "):
            reference = command[len("plan get "):].strip()
            plan_id = planner.latest_plan_id() if reference.casefold() == "latest" else reference
            return planner.get_plan(plan_id or "")
        if lowered.startswith("plan optimize "):
            reference = command[len("plan optimize "):].strip()
            plan_id = planner.latest_plan_id() if reference.casefold() == "latest" else reference
            return planner.optimize_plan(plan_id or "")
        return self._result(False, "Неизвестная команда планирования.", "INVALID_PLAN_COMMAND")

    def _execute_progress_command(self, command, lowered):
        from A_02_MANAGERS.progress_tracker import ProgressTracker

        tracker = ProgressTracker(goal_manager=self)
        if lowered.startswith("progress update "):
            arguments = command[len("progress update "):].rsplit(maxsplit=1)
            if len(arguments) != 2:
                return self._result(False, "Не указаны task_id и status.", "INVALID_PROGRESS_COMMAND")
            task_id, status = arguments
            if task_id.casefold() == "latest":
                goals = self._load()["goals"]
                tasks = [task for goal in goals for task in goal.get("tasks", [])]
                task_id = tasks[-1]["id"] if tasks else ""
            return tracker.update_task_status(task_id, status)
        if lowered.startswith("progress get "):
            reference = command[len("progress get "):]
            return tracker.get_goal_progress(self._resolve_goal_id(reference))
        if lowered.startswith("progress timeline "):
            reference = command[len("progress timeline "):]
            return tracker.get_timeline(self._resolve_goal_id(reference))
        return self._result(False, "Неизвестная команда прогресса.", "INVALID_PROGRESS_COMMAND")

    def create_goal(self, title, description="", priority="normal"):
        title = str(title or "").strip()
        if not title:
            return self._result(False, "Название цели не указано.", "INVALID_GOAL_TITLE")
        with self._lock:
            try:
                data = self._load()
                goal_id = "goal_" + uuid.uuid4().hex[:12]
                now = self._now()
                goal = {"id": goal_id, "title": title, "description": str(description or "").strip(),
                        "priority": str(priority or "normal"), "status": "active", "tasks": [],
                        "created_at": now, "updated_at": now}
                data["goals"].append(goal)
                self._save(data)
                return self._result(True, f"Цель создана: {title}", goal_id=goal_id, goal=goal)
            except RuntimeError as exc:
                return self._result(False, "Не удалось создать цель.", str(exc))

    def get_goal(self, goal_id):
        with self._lock:
            try:
                goal = self._find(self._load(), goal_id)
                if goal is None:
                    return self._result(False, "Цель не найдена.", "GOAL_NOT_FOUND", goal_id=goal_id)
                return self._result(True, f"Цель найдена: {goal['title']}", goal=goal, goal_id=goal_id)
            except RuntimeError as exc:
                return self._result(False, "Не удалось прочитать цель.", str(exc), goal_id=goal_id)

    def update_goal(self, goal_id, updates):
        allowed = {"title", "description", "priority", "status"}
        if not isinstance(updates, dict) or not updates:
            return self._result(False, "Изменения цели не указаны.", "INVALID_GOAL_UPDATES", goal_id=goal_id)
        changes = {key: value for key, value in updates.items() if key in allowed}
        if not changes or ("title" in changes and not str(changes["title"] or "").strip()):
            return self._result(False, "Допустимые изменения цели не указаны.", "INVALID_GOAL_UPDATES", goal_id=goal_id)
        with self._lock:
            try:
                data = self._load(); goal = self._find(data, goal_id)
                if goal is None:
                    return self._result(False, "Цель не найдена.", "GOAL_NOT_FOUND", goal_id=goal_id)
                goal.update(changes); goal["updated_at"] = self._now(); self._save(data)
                return self._result(True, "Цель обновлена.", goal=goal, goal_id=goal_id)
            except RuntimeError as exc:
                return self._result(False, "Не удалось обновить цель.", str(exc), goal_id=goal_id)

    def delete_goal(self, goal_id):
        with self._lock:
            try:
                data = self._load(); goal = self._find(data, goal_id)
                if goal is None:
                    return self._result(False, "Цель не найдена.", "GOAL_NOT_FOUND", goal_id=goal_id)
                data["goals"].remove(goal); self._save(data)
                return self._result(True, "Цель удалена.", goal_id=goal_id)
            except RuntimeError as exc:
                return self._result(False, "Не удалось удалить цель.", str(exc), goal_id=goal_id)

    def list_goals(self, filter=None):
        with self._lock:
            try:
                goals = list(self._load()["goals"])
                filters = filter if isinstance(filter, dict) else ({"status": filter} if filter else {})
                for key, value in filters.items():
                    goals = [goal for goal in goals if goal.get(key) == value]
                return self._result(True, f"Найдено целей: {len(goals)}", goals=goals, count=len(goals), filter=filters)
            except RuntimeError as exc:
                return self._result(False, "Не удалось получить список целей.", str(exc), goals=[], count=0)

    def add_task_to_goal(self, goal_id, task):
        title = task.get("title") if isinstance(task, dict) else task
        title = str(title or "").strip()
        if not title:
            return self._result(False, "Название задачи не указано.", "INVALID_TASK", goal_id=goal_id)
        with self._lock:
            try:
                data = self._load(); goal = self._find(data, goal_id)
                if goal is None:
                    return self._result(False, "Цель не найдена.", "GOAL_NOT_FOUND", goal_id=goal_id)
                task_id = "task_" + uuid.uuid4().hex[:12]
                item = dict(task) if isinstance(task, dict) else {"title": title}
                item.update({"id": task_id, "title": title, "status": item.get("status", "pending"), "created_at": self._now()})
                goal["tasks"].append(item); goal["updated_at"] = self._now(); self._save(data)
                return self._result(True, f"Задача добавлена: {title}", goal_id=goal_id, task_id=task_id, task=item)
            except RuntimeError as exc:
                return self._result(False, "Не удалось добавить задачу.", str(exc), goal_id=goal_id)

    def update_task_status(self, task_id, status):
        normalized = str(status or "").strip().lower()
        if normalized not in {"pending", "in_progress", "completed", "cancelled"}:
            return self._result(False, "Недопустимый статус задачи.", "INVALID_TASK_STATUS", task_id=task_id)
        with self._lock:
            try:
                data = self._load()
                for goal in data["goals"]:
                    task = next((item for item in goal.get("tasks", []) if item.get("id") == task_id), None)
                    if task is None:
                        continue
                    now = self._now()
                    task["status"] = normalized
                    task["updated_at"] = now
                    if normalized == "completed":
                        task["completed_at"] = now
                    else:
                        task.pop("completed_at", None)
                    goal["updated_at"] = now
                    self._save(data)
                    return self._result(True, f"Статус задачи обновлён: {normalized}", goal_id=goal.get("id"), task_id=task_id, task=task)
                return self._result(False, "Задача не найдена.", "TASK_NOT_FOUND", task_id=task_id)
            except RuntimeError as exc:
                return self._result(False, "Не удалось обновить статус задачи.", str(exc), task_id=task_id)

    def get_goal_progress(self, goal_id):
        result = self.get_goal(goal_id)
        if not result["ok"]:
            return result
        tasks = result["metadata"]["goal"].get("tasks", [])
        total = len(tasks); completed = sum(1 for task in tasks if task.get("status") == "completed")
        percent = round(completed * 100 / total, 2) if total else 0.0
        return self._result(True, f"Прогресс цели: {percent}%", goal_id=goal_id,
                            progress={"total": total, "completed": completed, "percent": percent})

``

---

# ACCEPTANCE CONFIG

Источник: `C:\Users\KOS\Desktop\Butler_Agent\BUTLER_OMEGA_SMART\A_99_TESTS\acceptance_config.json`

``json
{
    "version":  "1.0",
    "official_entry":  "A_03_ORCHESTRATION.dispatcher_bridge_v2.dispatch",
    "storage":  [
                    "A_05_STORAGE/user_profile.json",
                    "A_05_STORAGE/USER_MEMORY.md",
                    "A_05_STORAGE/checkpoint.md",
                    "A_05_STORAGE/session_history.jsonl",
                    "A_07_MEMORY/MEMORY_INDEX.jsonl",
                    "A_07_CONFIG/execution_registry.json",
                    "A_07_MEMORY/goals_registry.json",
                    "A_07_MEMORY/plans_registry.json",
                    "A_07_MEMORY/reminders_registry.json",
                    "A_07_MEMORY/SESSION/test_sessions"
                ],
    "scenarios":  [
                      {
                          "name":  "GOAL_CREATE",
                          "kind":  "goal_manager",
                          "operation":  "create_goal",
                          "modes":  [
                                        "fast",
                                        "full"
                                    ],
                          "enabled":  true,
                          "expected_department":  "GOAL_MANAGER",
                          "timeout":  30,
                          "critical":  true,
                          "requires_provider":  false,
                          "cleanup":  "restore_storage",
                          "command":  "goal create acceptance goal"
                      },
                      {
                          "name":  "GOAL_GET",
                          "kind":  "goal_manager",
                          "operation":  "get_goal",
                          "modes":  [
                                        "fast",
                                        "full"
                                    ],
                          "enabled":  true,
                          "expected_department":  "GOAL_MANAGER",
                          "timeout":  30,
                          "critical":  true,
                          "requires_provider":  false,
                          "cleanup":  "restore_storage",
                          "command":  "goal get acceptance goal"
                      },
                      {
                          "name":  "GOAL_LIST",
                          "kind":  "goal_manager",
                          "operation":  "list_goals",
                          "modes":  [
                                        "fast",
                                        "full"
                                    ],
                          "enabled":  true,
                          "expected_department":  "GOAL_MANAGER",
                          "timeout":  30,
                          "critical":  true,
                          "requires_provider":  false,
                          "cleanup":  "restore_storage",
                          "command":  "goal list"
                      },
                      {
                          "name":  "GOAL_UPDATE",
                          "kind":  "goal_manager",
                          "operation":  "update_goal",
                          "modes":  [
                                        "fast",
                                        "full"
                                    ],
                          "enabled":  true,
                          "expected_department":  "GOAL_MANAGER",
                          "timeout":  30,
                          "critical":  true,
                          "requires_provider":  false,
                          "cleanup":  "restore_storage",
                          "command":  "goal update acceptance goal"
                      },
                      {
                          "name":  "GOAL_ADD_TASK",
                          "kind":  "goal_manager",
                          "operation":  "add_task_to_goal",
                          "modes":  [
                                        "fast",
                                        "full"
                                    ],
                          "enabled":  true,
                          "expected_department":  "GOAL_MANAGER",
                          "timeout":  30,
                          "critical":  true,
                          "requires_provider":  false,
                          "cleanup":  "restore_storage",
                          "command":  "goal add task acceptance task"
                      },
                      {
                          "name":  "PRIORITY_CALCULATE",
                          "modes":  ["fast", "full"],
                          "enabled":  true,
                          "expected_department":  "GOAL_MANAGER",
                          "contains":  ["Приоритет задачи"],
                          "timeout":  30,
                          "critical":  true,
                          "requires_provider":  false,
                          "cleanup":  "restore_storage",
                          "command":  "priority calculate latest"
                      },
                      {
                          "name":  "PRIORITY_LIST",
                          "modes":  ["fast", "full"],
                          "enabled":  true,
                          "expected_department":  "GOAL_MANAGER",
                          "contains":  ["Приоритетный список задач"],
                          "timeout":  30,
                          "critical":  true,
                          "requires_provider":  false,
                          "cleanup":  "restore_storage",
                          "command":  "priority list acceptance goal"
                      },
                      {
                          "name":  "PRIORITY_NEXT",
                          "modes":  ["fast", "full"],
                          "enabled":  true,
                          "expected_department":  "GOAL_MANAGER",
                          "contains":  ["Следующая задача"],
                          "timeout":  30,
                          "critical":  true,
                          "requires_provider":  false,
                          "cleanup":  "restore_storage",
                          "command":  "priority next acceptance goal"
                      },
                      {
                          "name":  "REMINDER_SET",
                          "modes":  ["fast", "full"],
                          "enabled":  true,
                          "expected_department":  "GOAL_MANAGER",
                          "contains":  ["Напоминание создано"],
                          "timeout":  30,
                          "critical":  true,
                          "requires_provider":  false,
                          "cleanup":  "restore_storage",
                          "command":  "reminder set latest now acceptance reminder"
                      },
                      {
                          "name":  "REMINDER_LIST",
                          "modes":  ["fast", "full"],
                          "enabled":  true,
                          "expected_department":  "GOAL_MANAGER",
                          "contains":  ["Напоминаний: 1"],
                          "timeout":  30,
                          "critical":  true,
                          "requires_provider":  false,
                          "cleanup":  "restore_storage",
                          "command":  "reminder list"
                      },
                      {
                          "name":  "REMINDER_CHECK",
                          "modes":  ["fast", "full"],
                          "enabled":  true,
                          "expected_department":  "GOAL_MANAGER",
                          "contains":  ["Активных напоминаний: 1"],
                          "timeout":  30,
                          "critical":  true,
                          "requires_provider":  false,
                          "cleanup":  "restore_storage",
                          "command":  "reminder check"
                      },
                      {
                          "name":  "REMINDER_ACKNOWLEDGE",
                          "modes":  ["fast", "full"],
                          "enabled":  true,
                          "expected_department":  "GOAL_MANAGER",
                          "contains":  ["Напоминание подтверждено"],
                          "timeout":  30,
                          "critical":  true,
                          "requires_provider":  false,
                          "cleanup":  "restore_storage",
                          "command":  "reminder acknowledge latest"
                      },
                      {
                          "name":  "PROGRESS_UPDATE",
                          "modes":  [
                                        "fast",
                                        "full"
                                    ],
                          "enabled":  true,
                          "expected_department":  "GOAL_MANAGER",
                          "timeout":  30,
                          "critical":  true,
                          "requires_provider":  false,
                          "cleanup":  "restore_storage",
                          "command":  "progress update latest completed"
                      },
                      {
                          "name":  "PROGRESS_GET",
                          "modes":  [
                                        "fast",
                                        "full"
                                    ],
                          "enabled":  true,
                          "expected_department":  "GOAL_MANAGER",
                          "timeout":  30,
                          "critical":  true,
                          "requires_provider":  false,
                          "cleanup":  "restore_storage",
                          "command":  "progress get acceptance goal"
                      },
                      {
                          "name":  "PROGRESS_TIMELINE",
                          "modes":  [
                                        "fast",
                                        "full"
                                    ],
                          "enabled":  true,
                          "expected_department":  "GOAL_MANAGER",
                          "timeout":  30,
                          "critical":  true,
                          "requires_provider":  false,
                          "cleanup":  "restore_storage",
                          "command":  "progress timeline acceptance goal"
                      },
                      {
                          "name":  "GOAL_PROGRESS",
                          "kind":  "goal_manager",
                          "operation":  "get_goal_progress",
                          "modes":  [
                                        "fast",
                                        "full"
                                    ],
                          "enabled":  true,
                          "expected_department":  "GOAL_MANAGER",
                          "timeout":  30,
                          "critical":  true,
                          "requires_provider":  false,
                          "cleanup":  "restore_storage",
                          "command":  "goal progress acceptance goal"
                      },
                      {
                          "name":  "PLANNER_GENERATE",
                          "modes":  [
                                        "fast",
                                        "full"
                                    ],
                          "enabled":  true,
                          "expected_department":  "GOAL_MANAGER",
                          "timeout":  30,
                          "critical":  true,
                          "requires_provider":  false,
                          "cleanup":  "restore_storage",
                          "command":  "plan generate acceptance goal"
                      },
                      {
                          "name":  "PLANNER_GET",
                          "modes":  [
                                        "fast",
                                        "full"
                                    ],
                          "enabled":  true,
                          "expected_department":  "GOAL_MANAGER",
                          "timeout":  30,
                          "critical":  true,
                          "requires_provider":  false,
                          "cleanup":  "restore_storage",
                          "command":  "plan get latest"
                      },
                      {
                          "name":  "PLANNER_OPTIMIZE",
                          "modes":  [
                                        "fast",
                                        "full"
                                    ],
                          "enabled":  true,
                          "expected_department":  "GOAL_MANAGER",
                          "timeout":  30,
                          "critical":  true,
                          "requires_provider":  false,
                          "cleanup":  "restore_storage",
                          "command":  "plan optimize latest"
                      },
                      {
                          "name":  "GOAL_DELETE",
                          "kind":  "goal_manager",
                          "operation":  "delete_goal",
                          "modes":  [
                                        "fast",
                                        "full"
                                    ],
                          "enabled":  true,
                          "expected_department":  "GOAL_MANAGER",
                          "timeout":  30,
                          "critical":  true,
                          "requires_provider":  false,
                          "cleanup":  "restore_storage",
                          "command":  "goal delete acceptance goal"
                      },
                      {
                          "name":  "MEMORY_PROFILE",
                          "modes":  [
                                        "fast",
                                        "full"
                                    ],
                          "enabled":  true,
                          "command":  "Как меня зовут?",
                          "expected_department":  "MEMORY",
                          "contains":  [
                                           "Виктор"
                                       ],
                          "timeout":  30,
                          "critical":  true,
                          "requires_provider":  false,
                          "cleanup":  "restore_storage"
                      },
                      {
                          "name":  "MEMORY_COLOR",
                          "modes":  [
                                        "fast",
                                        "full"
                                    ],
                          "enabled":  true,
                          "command":  "Какой мой любимый цвет?",
                          "expected_department":  "MEMORY",
                          "contains":  [
                                           "зелёный"
                                       ],
                          "timeout":  30,
                          "critical":  true,
                          "requires_provider":  false,
                          "cleanup":  "restore_storage"
                      },
                      {
                          "name":  "MEMORY_GENERAL",
                          "modes":  [
                                        "full"
                                    ],
                          "enabled":  true,
                          "command":  "Что ты помнишь обо мне?",
                          "expected_department":  "MEMORY",
                          "contains":  [
                                           "Виктор"
                                       ],
                          "timeout":  30,
                          "critical":  true,
                          "requires_provider":  false,
                          "cleanup":  "restore_storage"
                      },
                      {
                          "name":  "CHAT_POEM",
                          "modes":  [
                                        "full"
                                    ],
                          "enabled":  true,
                          "command":  "напиши стих",
                          "expected_department":  "CHAT",
                          "contains":  [

                                       ],
                          "timeout":  180,
                          "critical":  true,
                          "requires_provider":  true,
                          "cleanup":  "none"
                      },
                      {
                          "name":  "CHAT_SELF_INFO",
                          "modes":  [
                                        "full"
                                    ],
                          "enabled":  true,
                          "command":  "что ты знаешь о себе?",
                          "expected_department":  "CHAT",
                          "contains":  [

                                       ],
                          "timeout":  180,
                          "critical":  true,
                          "requires_provider":  true,
                          "cleanup":  "none"
                      },
                      {
                          "name":  "CODING_HELLO_WORLD",
                          "modes":  [
                                        "full"
                                    ],
                          "enabled":  true,
                          "command":  "напиши Python-программу hello world",
                          "expected_department":  "CODING",
                          "contains":  [
                                           "print"
                                       ],
                          "timeout":  180,
                          "critical":  true,
                          "requires_provider":  true,
                          "cleanup":  "none"
                      },
                      {
                          "name":  "SEARCH_PASSPORT",
                          "modes":  [
                                        "fast",
                                        "full"
                                    ],
                          "enabled":  true,
                          "command":  "найди паспорт",
                          "expected_department":  "SEARCH",
                          "contains":  [

                                       ],
                          "timeout":  30,
                          "critical":  true,
                          "requires_provider":  false,
                          "cleanup":  "restore_storage"
                      },
                      {
                          "name":  "OPEN_FIRST",
                          "modes":  [
                                        "full"
                                    ],
                          "enabled":  true,
                          "command":  "открой первый",
                          "expected_department":  "OPEN_DOCUMENT",
                          "contains":  [

                                       ],
                          "allowed_errors":  [
                                                 "FILE_NOT_FOUND"
                                             ],
                          "timeout":  30,
                          "critical":  true,
                          "requires_provider":  false,
                          "cleanup":  "restore_storage"
                      },
                      {
                          "name":  "VISION_EXISTING",
                          "modes":  [
                                        "full"
                                    ],
                          "enabled":  true,
                          "command":  "что на фото",
                          "expected_department":  "VISION",
                          "contains":  [

                                       ],
                          "timeout":  180,
                          "critical":  true,
                          "requires_provider":  true,
                          "fixture":  "A_99_TESTS/fixtures/vision_test_image.png",
                          "cleanup":  "none"
                      },
                      {
                          "name":  "DOCUMENTS_EXISTING",
                          "modes":  [
                                        "full"
                                    ],
                          "enabled":  true,
                          "command":  "прочитай документ",
                          "expected_department":  "DOCUMENTS",
                          "contains":  [
                                           "BUTLER_ACCEPTANCE_DOCUMENT"
                                       ],
                          "timeout":  180,
                          "critical":  true,
                          "requires_provider":  false,
                          "fixture":  "A_99_TESTS/fixtures/document_test.txt",
                          "cleanup":  "none"
                      },
                      {
                          "name":  "ARCHIVE_EXISTING",
                          "modes":  [
                                        "full"
                                    ],
                          "enabled":  true,
                          "command":  "открой этот ZIP",
                          "expected_department":  "ARCHIVE",
                          "contains":  [

                                       ],
                          "timeout":  60,
                          "critical":  false,
                          "requires_provider":  false,
                          "fixture":  "A_99_TESTS/fixtures/archive_test.zip",
                          "cleanup":  "none"
                      },
                      {
                          "name":  "AUDIO",
                          "modes":  [
                                        "full"
                                    ],
                          "enabled":  true,
                          "command":  "создай аудио",
                          "expected_department":  "AUDIO",
                          "contains":  [

                                       ],
                          "timeout":  30,
                          "critical":  false,
                          "requires_provider":  true,
                          "cleanup":  "none"
                      },
                      {
                          "name":  "VIDEO",
                          "modes":  [
                                        "full"
                                    ],
                          "enabled":  true,
                          "command":  "создай видео",
                          "expected_department":  "VIDEO",
                          "contains":  [

                                       ],
                          "timeout":  30,
                          "critical":  false,
                          "requires_provider":  true,
                          "cleanup":  "none"
                      }
                  ]
}

``

---

# FULL ACCEPTANCE RUNNER

Источник: `C:\Users\KOS\Desktop\Butler_Agent\BUTLER_OMEGA_SMART\A_99_TESTS\full_acceptance.py`

``py
# -*- coding: utf-8 -*-
"""Permanent FAST/FULL acceptance runner for Butler Omega Smart."""

import argparse
import importlib
import json
import py_compile
import shutil
import struct
import sys
import time
import traceback
import zipfile
import zlib
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEST_ROOT = ROOT / "A_99_TESTS"
CONFIG_PATH = TEST_ROOT / "acceptance_config.json"
REPORTS = TEST_ROOT / "reports"
FIXTURES = TEST_ROOT / "fixtures"

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def ensure_fixtures():
    FIXTURES.mkdir(parents=True, exist_ok=True)
    png = FIXTURES / "vision_test_image.png"
    width = height = 64
    rows = []
    for y in range(height):
        row = bytearray([0])
        for x in range(width):
            row.extend((220, 40, 40) if (x // 16 + y // 16) % 2 == 0 else (40, 170, 70))
        rows.append(bytes(row))
    def chunk(kind, data):
        return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", zlib.crc32(kind + data) & 0xffffffff)
    png.write_bytes(
        b"\x89PNG\r\n\x1a\n"
        + chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0))
        + chunk(b"IDAT", zlib.compress(b"".join(rows), 9))
        + chunk(b"IEND", b"")
    )
    doc = FIXTURES / "document_test.txt"
    if not doc.exists():
        doc.write_text("BUTLER_ACCEPTANCE_DOCUMENT\nSafe project acceptance fixture.\n", encoding="utf-8")
    unsupported = FIXTURES / "unsupported.bin"
    if not unsupported.exists():
        unsupported.write_bytes(b"BUTLER_ACCEPTANCE_UNSUPPORTED")
    archive = FIXTURES / "archive_test.zip"
    if not archive.exists():
        with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as zf:
            zf.write(doc, arcname="document_test.txt")


class StorageGuard:
    def __init__(self, paths, stamp):
        self.paths = [ROOT / p for p in paths]
        self.backup = REPORTS / (".acceptance_backup_" + stamp)
        self.manifest = []
        self.errors = []

    def capture(self):
        self.backup.mkdir(parents=True, exist_ok=False)
        for source in self.paths:
            relative = source.relative_to(ROOT)
            target = self.backup / relative
            existed = source.exists()
            self.manifest.append((source, target, existed, source.is_dir() if existed else False))
            if not existed:
                continue
            target.parent.mkdir(parents=True, exist_ok=True)
            if source.is_dir():
                shutil.copytree(source, target)
            else:
                shutil.copy2(source, target)

    def restore(self):
        for source, target, existed, was_dir in reversed(self.manifest):
            try:
                if source.exists():
                    if source.is_dir():
                        shutil.rmtree(source)
                    else:
                        source.unlink()
                if existed:
                    source.parent.mkdir(parents=True, exist_ok=True)
                    if was_dir:
                        shutil.copytree(target, source)
                    else:
                        shutil.copy2(target, source)
            except Exception as exc:
                self.errors.append(f"{source}: {type(exc).__name__}: {exc}")
        if not self.errors:
            shutil.rmtree(self.backup, ignore_errors=True)
        return not self.errors


def result_contract(result, require_text=True):
    problems = []
    if not isinstance(result, dict):
        return ["result is not a dictionary"]
    for field in ("ok", "department", "text", "error", "metadata"):
        if field not in result:
            problems.append("missing field: " + field)
    if not isinstance(result.get("ok"), bool):
        problems.append("ok is not boolean")
    if not str(result.get("department") or "").strip():
        problems.append("department is empty")
    if not isinstance(result.get("metadata"), dict):
        problems.append("metadata is not a dictionary")
    if result.get("ok") is True and result.get("error") not in (None, ""):
        problems.append("successful result contains error")
    if require_text and not str(result.get("text") or "").strip():
        problems.append("text is empty")
    return problems


def metadata_summary(metadata):
    if not isinstance(metadata, dict):
        return {}
    safe = {}
    allowed = {"path", "filepath", "format", "engine", "result_count", "mode", "action", "prompt_id", "image_path"}
    for key, value in metadata.items():
        if key not in allowed:
            continue
        if isinstance(value, (str, int, float, bool)) or value is None:
            safe[key] = value
    return safe


def _none(value):
    return value if value not in (None, "") else None


def failure_diagnostics(name, expected, result, breakpoint, exception, duration_ms, command):
    metadata = result.get("metadata") if isinstance(result.get("metadata"), dict) else {}
    nested = metadata.get("diagnostics") if isinstance(metadata.get("diagnostics"), dict) else {}
    exception_lines = str(exception or metadata.get("traceback") or nested.get("traceback") or "").strip().splitlines()
    timed_out = "timeout" in str(breakpoint or "").lower()
    actual = result.get("department")
    stage = (nested.get("failure_stage") or metadata.get("last_pipeline_step")
             or metadata.get("last_executed_step") or breakpoint)
    exception_type = nested.get("exception_type") or metadata.get("exception_type")
    exception_message = nested.get("exception_message") or metadata.get("exception_message")
    if timed_out:
        exception_type = exception_type or "TimeoutError"
        exception_message = exception_message or breakpoint
    diagnostics = {
        "failure_source": _none(nested.get("failure_source") or actual or expected),
        "failure_stage": _none(stage),
        "exception_type": _none(exception_type),
        "exception_message": _none(exception_message or result.get("error") or breakpoint),
        "elapsed_time_ms": duration_ms,
        "traceback": _none("\n".join(exception_lines[-10:])),
    }
    if str(expected or "").upper() == "IMAGE" or name.startswith("IMAGE_"):
        diagnostics.update({
            "prompt": _none(metadata.get("prompt") or command),
            "workflow": _none(metadata.get("workflow")),
            "checkpoint": _none(metadata.get("checkpoint")),
            "output_directory": _none(metadata.get("output_directory")),
            "http_status": _none(metadata.get("http_status") or metadata.get("status_code")),
            "http_response": _none(metadata.get("http_response")),
            "last_pipeline_step": _none(metadata.get("last_pipeline_step") or stage),
        })
    if str(expected or "").upper() == "OPEN_DOCUMENT" or name.startswith("OPEN_"):
        diagnostics.update({
            "file_path": _none(metadata.get("filepath") or metadata.get("path")),
            "last_executed_step": _none(metadata.get("last_executed_step") or "official dispatch returned"),
            "timeout_location": _none(metadata.get("timeout_location") or ("WindowsShell.os.startfile / dispatch" if timed_out else None)),
            "current_state": _none(metadata.get("current_state") or ("returned after timeout threshold" if timed_out else None)),
        })
    return diagnostics


def route_only(dispatcher, query):
    from A_03_ORCHESTRATION.ConversationContext.context_engine import ConversationContextEngine
    resolved = ConversationContextEngine.resolve(query)
    context = {"image_followup": ConversationContextEngine.last_was_image_followup}
    for department in dispatcher.departments:
        try:
            handled = department.can_handle(resolved, context=context)
        except TypeError:
            handled = department.can_handle(resolved)
        if handled:
            actual = dispatcher._dept_name(department)
            ConversationContextEngine.update(query, {"department": actual})
            return actual, resolved
    return None, resolved


def record(name, mode, command, expected, status, started, result=None, breakpoint=None,
           exception=None, artifacts=None, cleanup="pending"):
    result = result if isinstance(result, dict) else {}
    preview = str(result.get("text") or "")[:300]
    if str(result.get("department") or "").upper() == "MEMORY":
        preview = "[memory response redacted; non-empty=%s]" % bool(str(result.get("text") or "").strip())
    duration_ms = int((time.perf_counter() - started) * 1000)
    item = {
        "name": name, "mode": mode, "command": command,
        "expected_department": expected,
        "actual_department": result.get("department"),
        "status": status,
        "duration_ms": duration_ms,
        "ok": result.get("ok"),
        "text_preview": preview,
        "error": result.get("error"),
        "metadata_summary": metadata_summary(result.get("metadata")),
        "artifact_paths": list(artifacts or []),
        "cleanup_result": cleanup,
        "breakpoint": breakpoint,
        "exception": exception,
    }
    if status == "FAIL":
        item["diagnostics"] = failure_diagnostics(
            name, expected, result, breakpoint, exception, duration_ms, command
        )
    return item


def execute_case(dispatch, case, mode, context=None):
    started = time.perf_counter()
    command = case["command"]
    expected = case["expected_department"]
    try:
        result = dispatch(command, dict(context or {}))
        problems = result_contract(result, require_text=True)
        controlled_error = result.get("error") in case.get("allowed_errors", []) and result.get("ok") is False
        if str(result.get("department") or "").upper() != expected.upper():
            problems.append(f"department expected {expected}, got {result.get('department')}")
        if not result.get("ok") and not controlled_error:
            problems.append("ok is not true")
        lowered = str(result.get("text") or "").lower()
        for required in case.get("contains", []):
            if required.lower() not in lowered:
                problems.append("missing text: " + required)
        if lowered.strip() == "использовать qwen35-ru" or "использовать qwen35-ru" == lowered.strip(" ."):
            problems.append("model result not executed")
        if (time.perf_counter() - started) > case.get("timeout", 30):
            problems.append("scenario timeout exceeded")
        status = "PASS" if not problems else "FAIL"
        if controlled_error and not problems:
            status = "CONTROLLED_ERROR"
        return record(case["name"], mode, command, expected, status, started, result,
                      "; ".join(problems) or None)
    except Exception as exc:
        return record(case["name"], mode, command, expected, "FAIL", started,
                      breakpoint="UNHANDLED_EXCEPTION", exception=traceback.format_exc())


def negative_case(dispatch, name, command, expected, context):
    started = time.perf_counter()
    try:
        result = dispatch(command, context)
        problems = result_contract(result, require_text=True)
        if str(result.get("department") or "").upper() != expected:
            problems.append("wrong department")
        if result.get("ok") is not False or not result.get("error"):
            problems.append("controlled failure not returned")
        return record(name, "full", command, expected, "PASS" if not problems else "FAIL",
                      started, result, "; ".join(problems) or None)
    except Exception:
        return record(name, "full", command, expected, "FAIL", started,
                      breakpoint="UNHANDLED_EXCEPTION", exception=traceback.format_exc())


def run_fast(config):
    results = []
    started = time.perf_counter()
    key_files = [
        ROOT / "BUTLER_OS.py", ROOT / "A_03_ORCHESTRATION/dispatcher_bridge_v2.py",
        ROOT / "A_02_MANAGERS/smart_dispatcher_v2.py", ROOT / "A_03_ORCHESTRATION/butler_harness.py",
        ROOT / "A_04_AGENTS/MemoryDepartment/runner.py", Path(__file__),
    ]
    errors = []
    for path in key_files:
        try:
            py_compile.compile(str(path), doraise=True)
        except Exception as exc:
            errors.append(f"{path}: {exc}")
    results.append(record("PY_COMPILE", "fast", "py_compile key components", "INFRASTRUCTURE",
                          "PASS" if not errors else "FAIL", started,
                          {"ok": not errors, "department": "INFRASTRUCTURE", "text": "compiled", "error": errors or None, "metadata": {}},
                          "; ".join(errors) or None))
    started = time.perf_counter()
    try:
        importlib.import_module("BUTLER_OS")
        bridge = importlib.import_module("A_03_ORCHESTRATION.dispatcher_bridge_v2")
        dispatcher = bridge._dispatcher
        names = [dispatcher._dept_name(d) for d in dispatcher.departments]
        expected = {"MEMORY","SEARCH","OPEN_DOCUMENT","DOCUMENTS","VISION","IMAGE","TEXT","CODING","HOME","ARCHIVE","AUDIO","VIDEO"}
        missing = sorted(expected - set(names))
        results.append(record("RUNTIME_IMPORT_AND_REGISTRATION", "fast", "import official runtime", "INFRASTRUCTURE",
                              "PASS" if not missing else "FAIL", started,
                              {"ok": not missing, "department": "INFRASTRUCTURE", "text": ",".join(names), "error": missing or None, "metadata": {"departments": names}},
                              ("missing: " + ",".join(missing)) if missing else None))
    except Exception:
        results.append(record("RUNTIME_IMPORT_AND_REGISTRATION", "fast", "import official runtime", "INFRASTRUCTURE", "FAIL", started,
                              breakpoint="RUNTIME_INITIALIZATION", exception=traceback.format_exc()))
        return results, 2
    for case in config["scenarios"]:
        if case.get("enabled") and "fast" in case.get("modes", []):
            results.append(execute_case(bridge.dispatch, case, "fast"))
    routing = [
        ("ROUTE_IMAGE", "Нарисуй дракона", "IMAGE"), ("ROUTE_TEXT", "Напиши стихотворение", "TEXT"),
        ("ROUTE_CODING", "Напиши функцию Python", "CODING"), ("ROUTE_SEARCH", "Найди договор", "SEARCH"),
    ]
    for name, query, expected in routing:
        started = time.perf_counter(); actual, resolved = route_only(dispatcher, query)
        fake = {"ok": actual == expected, "department": actual or "NONE", "text": resolved, "error": None if actual == expected else "ROUTE_MISMATCH", "metadata": {"resolved": resolved}}
        results.append(record(name, "fast", query, expected, "PASS" if actual == expected else "FAIL", started, fake,
                              None if actual == expected else "ROUTING_MISMATCH"))
    return results, None


def run_full(config):
    bridge = importlib.import_module("A_03_ORCHESTRATION.dispatcher_bridge_v2")
    dispatch = bridge.dispatch
    results = []
    by_name = {c["name"]: c for c in config["scenarios"] if c.get("enabled") and "full" in c.get("modes", [])}
    for name in (
        "GOAL_CREATE", "GOAL_GET", "GOAL_LIST", "GOAL_UPDATE",
        "GOAL_ADD_TASK", "PRIORITY_CALCULATE", "PRIORITY_LIST", "PRIORITY_NEXT",
        "REMINDER_SET", "REMINDER_LIST", "REMINDER_CHECK", "REMINDER_ACKNOWLEDGE",
        "PROGRESS_UPDATE", "PROGRESS_GET",
        "PROGRESS_TIMELINE", "GOAL_PROGRESS", "PLANNER_GENERATE",
        "PLANNER_GET", "PLANNER_OPTIMIZE", "GOAL_DELETE",
    ):
        results.append(execute_case(dispatch, by_name[name], "full"))
    for name in ("MEMORY_PROFILE", "MEMORY_COLOR", "MEMORY_GENERAL"):
        results.append(execute_case(dispatch, by_name[name], "full"))
    marker = "ACCEPTANCE_MEMORY_" + datetime.now().strftime("%Y%m%d%H%M%S")
    write = dict(by_name["MEMORY_PROFILE"], name="MEMORY_WRITE", command=f"Запомни: acceptance_marker = {marker}", contains=[marker])
    read = dict(by_name["MEMORY_PROFILE"], name="MEMORY_PERSISTENCE", command="какой мой acceptance_marker", contains=[marker])
    results.append(execute_case(dispatch, write, "full")); results.append(execute_case(dispatch, read, "full"))
    for name in ("CHAT_POEM", "CHAT_SELF_INFO", "CODING_HELLO_WORLD", "SEARCH_PASSPORT", "OPEN_FIRST"):
        results.append(execute_case(dispatch, by_name[name], "full"))
    vision = by_name["VISION_EXISTING"]
    results.append(execute_case(dispatch, vision, "full", {"attachments": [str(ROOT / vision["fixture"])]}))
    results.append(negative_case(dispatch, "VISION_MISSING", "что на фото", "VISION", {"attachments": [str(FIXTURES / "missing.png")]}))
    results.append(negative_case(dispatch, "VISION_UNSUPPORTED", "что на фото", "VISION", {"attachments": [str(FIXTURES / "unsupported.bin")]}))
    documents = by_name["DOCUMENTS_EXISTING"]
    results.append(execute_case(dispatch, documents, "full", {"attachments": [str(ROOT / documents["fixture"])]}))
    results.append(negative_case(dispatch, "DOCUMENTS_MISSING", "прочитай документ", "DOCUMENTS", {"attachments": [str(FIXTURES / "missing.txt")]}))
    archive = by_name["ARCHIVE_EXISTING"]
    results.append(execute_case(dispatch, archive, "full", {"attachments": [str(ROOT / archive["fixture"])]}))
    for name in ("AUDIO", "VIDEO"):
        case = by_name[name]
        started = time.perf_counter()
        results.append(record(name, "full", case["command"], case["expected_department"], "SKIP", started,
                              breakpoint="NO_REAL_PROVIDER: registered minimal acknowledgement only"))
    from A_03_ORCHESTRATION.ConversationContext.context_engine import ConversationContextEngine
    from A_03_ORCHESTRATION.ConversationContext.ImageSession.image_session import ImageSession
    ConversationContextEngine.last_department = None; ConversationContextEngine.last_user_query = ""; ImageSession.clear()
    image_steps = [("IMAGE_INITIAL", "нарисуй девушку"), ("IMAGE_CONTINUATION_1", "не лицо"),
                   ("IMAGE_CONTINUATION_2", "в полный рост"), ("IMAGE_WATERFALL", "под водопадом")]
    for name, command in image_steps:
        case = {"name":name,"command":command,"expected_department":"IMAGE","contains":[],"timeout":300}
        item = execute_case(dispatch, case, "full")
        if name == "IMAGE_WATERFALL" and item["actual_department"] == "HOME":
            item["breakpoint"] = 'IMAGE_CONTEXT_LOST; Expected IMAGE; Actual HOME; Input: "под водопадом"'
        results.append(item)
    return results, None


def write_reports(mode, stamp, results, cleanup_ok, cleanup_errors, initial_code=None):
    REPORTS.mkdir(parents=True, exist_ok=True)
    counts = {s: sum(1 for r in results if r["status"] == s) for s in ("PASS","FAIL","CONTROLLED_ERROR","SKIP")}
    mandatory_fail = any(r["status"] == "FAIL" for r in results)
    exit_code = 3 if not cleanup_ok else (initial_code if initial_code is not None else (1 if mandatory_fail else 0))
    payload = {"timestamp": stamp, "mode": mode, "official_entry": "A_03_ORCHESTRATION.dispatcher_bridge_v2.dispatch",
               "results": results, "counts": counts, "cleanup_ok": cleanup_ok, "cleanup_errors": cleanup_errors,
               "all_scenarios_passed": not mandatory_fail, "exit_code": exit_code}
    json_path = REPORTS / f"acceptance_report_{stamp}.json"; md_path = REPORTS / f"acceptance_report_{stamp}.md"
    json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    lines = [f"# Butler Omega Smart — {mode.upper()} Acceptance", "", f"Timestamp: {stamp}", "",
             "| Scenario | Status | Expected | Actual | Duration ms |", "|---|---:|---|---|---:|"]
    for r in results:
        lines.append(f"| {r['name']} | {r['status']} | {r.get('expected_department') or ''} | {r.get('actual_department') or ''} | {r['duration_ms']} |")
    lines += ["", f"PASS: {counts['PASS']}", f"FAIL: {counts['FAIL']}", f"SKIP: {counts['SKIP']}",
              f"CONTROLLED_ERROR: {counts['CONTROLLED_ERROR']}",
              f"Cleanup: {'PASS' if cleanup_ok else 'FAIL'}", f"Exit code: {exit_code}", "", "## Failures", ""]
    for r in results:
        if r["status"] == "FAIL":
            diagnostics = r.get("diagnostics") or failure_diagnostics(
                r["name"], r.get("expected_department"), {}, r.get("breakpoint"),
                r.get("exception"), r["duration_ms"], r.get("command")
            )
            lines += [f"### {r['name']}", "", f"- Input: `{r['command']}`", f"- Expected: `{r['expected_department']}`",
                      f"- Actual: `{r.get('actual_department')}`", f"- Error: `{r.get('error')}`",
                      f"- Breakpoint: {r.get('breakpoint') or 'None'}"]
            labels = {
                "failure_source": "Failure Source", "failure_stage": "Failure Stage",
                "exception_type": "Exception Type", "exception_message": "Exception Message",
                "elapsed_time_ms": "Elapsed Time", "traceback": "Traceback",
                "prompt": "Prompt", "workflow": "Workflow", "checkpoint": "Checkpoint",
                "output_directory": "Output Directory", "http_status": "HTTP Status",
                "http_response": "HTTP Response", "last_pipeline_step": "Last Pipeline Step",
                "file_path": "File Path", "last_executed_step": "Last Executed Step",
                "timeout_location": "Timeout Location", "current_state": "Current State",
            }
            for key, label in labels.items():
                if key in diagnostics:
                    value = diagnostics.get(key)
                    lines.append(f"- {label}: `{value if value not in (None, '') else 'None'}`")
            lines.append("")
    if cleanup_errors: lines += ["## Cleanup errors", ""] + [f"- {e}" for e in cleanup_errors]
    md_path.write_text("\n".join(lines), encoding="utf-8")
    shutil.copy2(json_path, REPORTS / "latest_acceptance_report.json"); shutil.copy2(md_path, REPORTS / "latest_acceptance_report.md")
    return payload, json_path, md_path


def print_console(mode, payload):
    print("=" * 70); print(f" BUTLER OMEGA SMART — {mode.upper()} ACCEPTANCE"); print("=" * 70)
    for r in payload["results"]: print(f"[ {r['name']:<28} ] {r['status']}")
    print("-" * 70)
    for key in ("PASS","FAIL","CONTROLLED_ERROR","SKIP"): print(f"{key}: {payload['counts'][key]}")
    print(f"TOTAL: {len(payload['results'])}"); print("-" * 70)
    print("ALL SCENARIOS PASSED:", "YES" if payload["all_scenarios_passed"] else "NO")
    print("EXIT CODE:", payload["exit_code"]); print("=" * 70)


def main():
    parser = argparse.ArgumentParser(); parser.add_argument("--mode", choices=("fast","full"), required=True); args = parser.parse_args()
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    try:
        config = json.loads(CONFIG_PATH.read_text(encoding="utf-8")); ensure_fixtures(); REPORTS.mkdir(parents=True, exist_ok=True)
    except Exception:
        traceback.print_exc(); return 2
    guard = StorageGuard(config.get("storage", []), stamp); results = []; initial_code = None
    try:
        guard.capture()
        results, initial_code = run_fast(config) if args.mode == "fast" else run_full(config)
    except Exception:
        results.append(record("RUNNER_INTERNAL", args.mode, "runner", "INFRASTRUCTURE", "FAIL", time.perf_counter(), breakpoint="RUNNER_INTERNAL", exception=traceback.format_exc()))
        initial_code = 2
    finally:
        cleanup_ok = guard.restore()
    for item in results: item["cleanup_result"] = "PASS" if cleanup_ok else "FAIL"
    payload, _, _ = write_reports(args.mode, stamp, results, cleanup_ok, guard.errors, initial_code)
    print_console(args.mode, payload)
    return payload["exit_code"]


if __name__ == "__main__":
    raise SystemExit(main())

``

---

# LATEST ACCEPTANCE REPORT

Источник: `C:\Users\KOS\Desktop\Butler_Agent\BUTLER_OMEGA_SMART\A_99_TESTS\reports\latest_acceptance_report.md`

``md
# Butler Omega Smart — FULL Acceptance

Timestamp: 20260713_100727

| Scenario | Status | Expected | Actual | Duration ms |
|---|---:|---|---|---:|
| GOAL_CREATE | PASS | GOAL_MANAGER | GOAL_MANAGER | 9 |
| GOAL_GET | PASS | GOAL_MANAGER | GOAL_MANAGER | 8 |
| GOAL_LIST | PASS | GOAL_MANAGER | GOAL_MANAGER | 8 |
| GOAL_UPDATE | PASS | GOAL_MANAGER | GOAL_MANAGER | 9 |
| GOAL_ADD_TASK | PASS | GOAL_MANAGER | GOAL_MANAGER | 9 |
| PRIORITY_CALCULATE | PASS | GOAL_MANAGER | GOAL_MANAGER | 123 |
| PRIORITY_LIST | PASS | GOAL_MANAGER | GOAL_MANAGER | 110 |
| PRIORITY_NEXT | PASS | GOAL_MANAGER | GOAL_MANAGER | 110 |
| REMINDER_SET | PASS | GOAL_MANAGER | GOAL_MANAGER | 119 |
| REMINDER_LIST | PASS | GOAL_MANAGER | GOAL_MANAGER | 113 |
| REMINDER_CHECK | PASS | GOAL_MANAGER | GOAL_MANAGER | 116 |
| REMINDER_ACKNOWLEDGE | PASS | GOAL_MANAGER | GOAL_MANAGER | 109 |
| PROGRESS_UPDATE | PASS | GOAL_MANAGER | GOAL_MANAGER | 111 |
| PROGRESS_GET | PASS | GOAL_MANAGER | GOAL_MANAGER | 124 |
| PROGRESS_TIMELINE | PASS | GOAL_MANAGER | GOAL_MANAGER | 113 |
| GOAL_PROGRESS | PASS | GOAL_MANAGER | GOAL_MANAGER | 8 |
| PLANNER_GENERATE | PASS | GOAL_MANAGER | GOAL_MANAGER | 116 |
| PLANNER_GET | PASS | GOAL_MANAGER | GOAL_MANAGER | 114 |
| PLANNER_OPTIMIZE | PASS | GOAL_MANAGER | GOAL_MANAGER | 117 |
| GOAL_DELETE | PASS | GOAL_MANAGER | GOAL_MANAGER | 9 |
| MEMORY_PROFILE | PASS | MEMORY | MEMORY | 10 |
| MEMORY_COLOR | PASS | MEMORY | MEMORY | 10 |
| MEMORY_GENERAL | PASS | MEMORY | MEMORY | 13 |
| MEMORY_WRITE | PASS | MEMORY | MEMORY | 10 |
| MEMORY_PERSISTENCE | PASS | MEMORY | MEMORY | 10 |
| CHAT_POEM | PASS | CHAT | CHAT | 14865 |
| CHAT_SELF_INFO | PASS | CHAT | CHAT | 4937 |
| CODING_HELLO_WORLD | PASS | CODING | CODING | 6736 |
| SEARCH_PASSPORT | PASS | SEARCH | SEARCH | 17 |
| OPEN_FIRST | PASS | OPEN_DOCUMENT | OPEN_DOCUMENT | 98 |
| VISION_EXISTING | PASS | VISION | VISION | 43431 |
| VISION_MISSING | PASS | VISION | VISION | 10 |
| VISION_UNSUPPORTED | PASS | VISION | VISION | 9 |
| DOCUMENTS_EXISTING | PASS | DOCUMENTS | DOCUMENTS | 9 |
| DOCUMENTS_MISSING | PASS | DOCUMENTS | DOCUMENTS | 9 |
| ARCHIVE_EXISTING | PASS | ARCHIVE | ARCHIVE | 12 |
| AUDIO | SKIP | AUDIO |  | 0 |
| VIDEO | SKIP | VIDEO |  | 0 |
| IMAGE_INITIAL | PASS | IMAGE | IMAGE | 31446 |
| IMAGE_CONTINUATION_1 | PASS | IMAGE | IMAGE | 26056 |
| IMAGE_CONTINUATION_2 | PASS | IMAGE | IMAGE | 26865 |
| IMAGE_WATERFALL | PASS | IMAGE | IMAGE | 26417 |

PASS: 40
FAIL: 0
SKIP: 2
CONTROLLED_ERROR: 0
Cleanup: PASS
Exit code: 0

## Failures

``

---
