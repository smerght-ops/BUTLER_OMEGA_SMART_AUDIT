# BUTLER OMEGA SMART — CODEX HANDOFF PACKAGE
## STAGE 6 — INTEGRATION RECONNAISSANCE (Bionic → Codex)

---

## 1. EXECUTIVE VERDICT

**Да, Agent Core можно интегрировать минимально без перестройки Butler.**

Существующий Butler уже предоставляет все необходимые исполнительные компоненты:
- Departments с контрактом `can_handle(query, context)` / `execute(query, context) -> dict`
- CapabilityRegistry.json — машинно-читаемое описание всех возможностей
- SmartDispatcherV2.dispatch() — маршрутизатор, который можно использовать как fallback

Agent Core не должен заменять Dispatcher. Он должен стоять **перед** ним: принимать естественный язык пользователя → планировать через LLM tool-calling → вызывать существующие Departments напрямую или через dispatch().

---

## 2. CURRENT OFFICIAL ROUTE

```
User (BUTLER_OS.py:main)
  -> BUTLER_OS._execute_query(query)          [BUTLER_OS.py:53]
    -> TaskExecutor.plan(query)                [A_01_CORE/TaskExecutor/task_executor.py:42]
      -> TaskDecomposer.decompose(goal)        [A_01_CORE/TaskExecutor/task_decomposer.py]
      -> CapabilityRegistry.all()               [CapabilityRegistry.py:36]
    -> dispatch(query, context)                [A_03_ORCHESTRATION/dispatcher_bridge_v2.py:14]
      -> PlannerEngine.can_handle / execute   [A_02_MANAGERS/Planner/planner_engine.py]  (если goal)
      -> SmartDispatcherV2.dispatch(query)     [A_02_MANAGERS/smart_dispatcher_v2.py:235]
        -> SemanticReasoningEngine.detect_intent [A_07_MEMORY/semantic_reasoning_engine.py]
        -> TaskExecutor.plan(query)            (повторно, внутри dispatcher)
        -> dept.can_handle(query, context)     [BaseDepartment.can_handle]
        -> SmartDispatcherV2._execute_department(dept, query, context)  [smart_dispatcher_v2.py:108]
          -> ButlerHarness.execute(...)         [A_03_ORCHESTRATION/butler_harness.py:45]
            -> dept.execute(query, context)     [BaseDepartment.execute]
              -> Department-specific logic      (e.g. FilesystemDepartment.execute)
```

**Ключевой факт:** `TaskExecutor.plan()` вызывается ДВАЖДЫ — один раз в BUTLER_OS._execute_query и второй раз внутри SmartDispatcherV2.dispatch(). Это дублирование, но не блокиратор интеграции.

---

## 3. CURRENT EXPERIMENTAL AGENT ROUTE

```
User query (в _AGENT_CORE_LAB probe)
  -> lmstudio.Client(api_host="127.0.0.1:41343")     [agent_core_probe.py:56]
  -> llm_model.act(chat=chat, tools=[ToolFunctionDef], ...)  [lmstudio API]
    -> LLM решает вызвать tool                       (внутренне в LM Studio)
      -> Python tool function (e.g. rename_files)     [agent_core_filesystem_probe.py:38]
        -> import FilesystemDepartment                 (динамический импорт)
        -> fs_dept.execute(query, context=context)    -> Butler Department execute
          -> result dict from Department               (ok, text, error, etc.)
        -> return formatted string to LLM              ("RENAME_OK:..." / "RENAME_FAILED:...")
      -> LLM получает observation                      (результат tool)
      -> LLM решает следующий шаг или финальный ответ  (внутренне в LM Studio)
```

**Ключевой факт:** Прототип уже работает. `agent_core_filesystem_probe.py` — доказательство, что:
1. Python tools могут вызывать Departments напрямую
2. Результат возвращается LLM как observation
3. LLM продолжает цикл tool-calling с новым контекстом

---

## 4. RECOMMENDED INTEGRATION POINT

**Файл:** `BUTLER_OS.py`
**Место:** Функция `main(once_query=None)` или итерация `while True:` внутри неё
**Конкретная точка:** Добавить опциональный Agent Core loop **перед** вызовом `_execute_query(query)`, но **внутри** того же процесса.

### Почему именно здесь:

1. `BUTLER_OS.py` — единственный entry point, который уже знает о всех импортах (TaskExecutor, CapabilityRegistry, Departments, SmartDispatcherV2).
2. Agent Core получает пользовательский запрос первым → может распланировать через LLM tool-calling.
3. Если Agent Core не справляется с простым запросом (1 step) — fallback на существующий `_execute_query(query)` сохраняет всю цепочку Butler.
4. Не нужно менять dispatcher_bridge_v2, SmartDispatcherV2, TaskDecomposer.

### Что остаётся неизменным:
- Все Departments
- SmartDispatcherV2 и его маршрутизация
- TaskExecutor / TaskDecomposer / CapabilityRegistry
- ButlerHarness и Result Contract
- ConversationContextEngine
- SemanticReasoningEngine
- MemoryOrchestratorV2

---

## 5. ALTERNATIVES REJECTED

### A. Agent Core как замена SmartDispatcherV2.dispatch()
**Почему хуже:** Agent Core не должен дублировать маршрутизацию Butler. SmartDispatcherV2 уже умеет: семантический анализ, memory-пакеты, intent detection, multi-step planning через TaskExecutor. Замена = потеря этих возможностей и необходимость их повторной реализации.

### B. Agent Core после SmartDispatcherV2 (как надстройка над результатом)
**Почему хуже:** Если Agent Core стоит после Dispatcher, он получает уже маршрутизированный результат одного Department и не может планировать multi-step задачи из естественного языка. Пользовательский сценарий "возьми фото → выбери → создай документ → сохрани" потребовал бы ручного указания шагов.

---

## 6. EXISTING TOOL/CAPABILITY SOURCE

**Источник:** `CapabilityRegistry.json` (корень проекта)
**API чтения:** `CapabilityRegistry` класс из `CapabilityRegistry.py`

```python
from CapabilityRegistry import CapabilityRegistry
registry = CapabilityRegistry()
all_caps = registry.all()           # list[dict] — все возможности
by_dept = registry.by_department("FILESYSTEM")  # по department
actions = registry.actions_by_department("BROWSER")  # список actions
found = registry.find(alias="скачай документ")  # поиск по alias
```

Каждая capability содержит: `id`, `department`, `action`, `object`, `input`, `output`, `confidence`, `aliases`.

**GAP:** CapabilityRegistry.json описывает capabilities Butler, но не формирует LM Studio ToolFunctionDef автоматически. Codex должен написать адаптер, который преобразует записи CapabilityRegistry в список tools для LLM.act().

---

## 7. EXACT CHANGE SURFACE

| FILE | SYMBOL | WHY CHANGE MAY BE NEEDED |
|------|--------|--------------------------|
| BUTLER_OS.py | main() / _execute_query() | Добавить опциональный Agent Core loop перед существующим маршрутом; или создать обёртку, которая сначала пробует Agent Core, затем fallback на dispatch() |
| CapabilityRegistry.py | (новый метод) | Опционально: добавить `.to_lmstudio_tools()` для генерации ToolFunctionDef из capability records. Если не добавлять — Codex напишет отдельный адаптер. |

**Итого: 1-2 файла максимум.**

---

## 8. DO NOT TOUCH

- `A_02_MANAGERS/smart_dispatcher_v2.py` (SmartDispatcherV2)
- `A_03_ORCHESTRATION/dispatcher_bridge_v2.py` (dispatch)
- `A_01_CORE/TaskExecutor/task_executor.py` (TaskExecutor)
- `A_01_CORE/TaskExecutor/task_decomposer.py` (TaskDecomposer)
- `A_01_CORE/TaskExecutor/capability_executor.py` (CapabilityExecutor)
- `A_03_ORCHESTRATION/butler_harness.py` (ButlerHarness)
- `A_02_MANAGERS/RuntimeCapabilityRegistry/*` (RuntimeCapabilityRegistry)
- `A_04_AGENTS/*/runner.py` (все Departments — 16 файлов)
- `A_07_MEMORY/semantic_memory.py`, `semantic_reasoning_engine.py`
- `A_03_ORCHESTRATION/ConversationContext/context_engine.py`
- `A_02_MANAGERS/smart_dispatcher.py` (SmartDispatcher / chat_provider)
- `A_02_MANAGERS/Planner/planner_engine.py`
- `MODEL_REGISTRY` или любые конфиги моделей
- `_AGENT_CORE_LAB/*` — это probe-код, не production. Codex создаст новый файл интеграции в рабочем каталоге.

---

## 9. RESOURCE AUDIT DEPENDENCIES

DEPENDENCY_ON_RESOURCE_AUDIT=Agent Core использует ту же LLM через lmstudio.Client("127.0.0.1:41343"), что и Butler (через SmartDispatcher/ProviderManager). Resource Lifecycle Audit определит, какая модель загружена в LM Studio — Agent Core должен использовать ту же или отдельную? Это влияет на GPU/RAM нагрузку, но не на архитектурный integration point.

---

## 10. ACCEPTANCE TEST

**Сценарий:** Пользователь вводит в Butler:
> "Переименуй все файлы в C:\Test\ButlerAgentCoreE2E\rename в формат Test_{n:03d}"

**Ожидаемый маршрут:**
1. User input → Agent Core loop (в BUTLER_OS.py)
2. Agent Core получает CapabilityRegistry, формирует tools для LLM
3. LLM.act() вызывает tool `rename_files(folder_path="C:\Test\ButlerAgentCoreE2E\rename", pattern="Test_{n:03d}")`
4. Tool импортирует FilesystemDepartment и вызывает `fs_dept.execute(query, context={"capability_action": "rename", ...})`
5. FilesystemDepartment.rename_files() выполняет операцию на диске
6. Результат возвращается через tool → LLM → Agent Core → пользователь

**Критерий успеха:** Файлы в папке C:\Test\ButlerAgentCoreE2E\rename переименованы, пользователь видит подтверждение. Существующий Butler продолжает работать для запросов без Agent Core.

---

## 11. OPEN QUESTIONS FOR CODEX

1. **Какая модель LM Studio используется Agent Core?** Resource Lifecycle Audit должен определить, какая LLM загружена и доступна через `client.list_loaded_models()`. Agent Core может использовать ту же модель или потребует отдельную.
2. **Нужен ли Agent Core в interactive mode (while True) или только для once_query?** Если только для once_query — проще; если нужен persistent loop — требуется управление состоянием Chat и историей.
3. **Как обрабатывать multi-step задачи, где один step зависит от результата другого?** Прототип filesystem_probe показывает pattern с depends_on через substitution в query. Нужно ли это обобщить?
4. **CapabilityRegistry.to_lmstudio_tools() — писать в CapabilityRegistry.py или отдельный модуль?** Если в CapabilityRegistry.py — добавить метод; иначе создать `A_02_MANAGERS/agent_core_tool_adapter.py`.

---

## 12. FINAL HANDOFF

READY_FOR_CODEX=YES
