# INTEGRATION DESIGN — READ ONLY AUDIT REPORT
## Bionic General Agent Worker / Builder Integration into BUTLER_OMEGA_SMART

**Status:** BLOCKED — awaiting resolution of PROGRAMMATIC_BIONIC_INTERFACE
**Phase:** Этапы 1-2 (READ ONLY reconstruction + Integration Design)

---

## ЗАДАЧА A: Реальный интерфейс Bionic 1.0.2

### FINDING: PROGRAMMATIC_BIONIC_INTERFACE = NOT FOUND

После полного исследования локальной установки LM Studio / Bionic 1.0.2:

#### 1. LM Studio SDK (lmstudio Python package, v1.5.0)
**Доказательство:** `C:/Users/KOS/AppData/Local/Python/pythoncore-3.12-64/Lib/site-packages/lmstudio/`

```python
Client()                    # подключается к LM Studio API server на порту 41343
client.llm().predict(...)   # только LLM inference (chat completions)
client.embedding()          # только embedding модели
client.files                # namespace "files" - файловые операции API
client.system               # namespace "system" - системные операции API
```

**НЕ НАЙДЕНО:**
- Нет методов управления проектами (createProject, openProject, listProjects)
- Нет методов управления сессиями (startSession, stopSession, cancelSession)
- Нет контроля над ngModules/tools из внешнего клиента
- Нет API для отправки промптов в активную Bionic сессию

#### 2. LM Studio CLI (`lms.exe`)
**Доказательство:** `C:/Users/KOS/.lmstudio/bin/lms.exe`

```bash
lms chat --prompt "..."     # неинтерактивный чат с моделью (только inference)
lms server start/stop       # управление локальным сервером inference
lms load/unload/ls/ps       # управление моделями
```

**НЕ НАЙДЕНО:**
- Нет команд управления проектами Bionic
- Нет команд управления сессиями Bionic
- Нет команд для отправки заданий в активную сессию

#### 3. LM Studio HTTP API Server (порт 41343)
**Доказательство:** `GET http://127.0.0.1:41343/lmstudio-greeting` -> `{"lmstudio": true}`
Все другие HTTP endpoints возвращают 404.

**НЕ НАЙДЕНО:**
- Нет REST API для управления проектами/сессиями Bionic
- Нет WebSocket endpoint для мониторинга tool calls
- Нет публичного HTTP API, документированного или обнаруженного

#### 4. Electron App IPC (main_window_preload.js)
**Доказательство:** `C:/Program Files/LM Studio/resources/app/.webpack/main/main_window_preload.js`
Содержит только стандартный `exposeInMainWorld` - без специфичных Bionic session management channels.

#### 5. SQLite базы сессий (read-only анализ)
**Доказательство:** `C:/Users/KOS/.lmstudio/apps/bionic/projects/*/ng-sessions.sqlite`

Структура подтверждает, что сессии управляются исключительно внутри LM Studio:
- `sessions` таблица: session_id, session_json (включая baseSystemPrompt, parentSessionId)
- `chat_entries` таблица: entry_json (включая source.ngModule, message.parts)
- Tool calls логируются как: `source.ngModule = "lmstudio/shell-v1"`, `handler = "toolCall"`

**Вывод:** Bionic session lifecycle управляется ТОЛЬКО через UI LM Studio desktop app.
Программного интерфейса для внешнего управления сессиями НЕ СУЩЕСТВУЕТ.

---

## ЗАДАЧА B: Reconstruction BUTLER_OMEGA_SMART - полный маршрут

### Фактический маршрут OWNER -> RESULT

```
OWNER REQUEST
  |
SmartDispatcherV2.dispatch(query, context)          [A_02_MANAGERS/smart_dispatcher_v2.py:282]
  |-- memory_orchestrator.build_memory_packet(query)
  |-- reasoning_engine.detect_intent(query)           -> PROJECT_SELF_KNOWLEDGE?
  |   +-> YES -> ProjectDocumentationDepartment
  |-- task_executor.plan(query)                       [A_01_CORE/TaskExecutor/task_executor.py:23]
  |   +-> valid plan with steps?
  |       +-> YES -> _execute_task_plan() -> iterates steps -> _execute_department()
  |       +-> NO -> fallback department routing
  |-- for dept in self.departments:                   [line ~340]
  |   |-- dept.can_handle(query, context)             [A_04_AGENTS/base_department.py:7]
  |   +-> if True: _execute_department(dept, query, context)
  |-- semantic memory search fallback routing
  +-> TaskExecutor plan execution (if valid)

_execute_department(dept, query, context)             [smart_dispatcher_v2.py:248]
  |-- harness.execute(department_name, task, executor) [A_03_ORCHESTRATION/butler_harness.py:61]
  |   |-- PRE-FLIGHT: guards.validate(cr_path) sequentially
  |   |   |-- FrozenCoreGuard                         [guards/frozen_core_guard.py]
  |   |   |-- RollbackGuard                           [guards/rollback_guard.py]
  |   |   |-- CompileGuard                            [guards/compile_guard.py]
  |   |   +-> IntegrationTestGuard                    [guards/integration_test_guard.py]
  |   |-- EXECUTION: executor() = dept.execute(query, context)
  |   +-> POST-FLIGHT: validate_department_result(draft) [department_result.py:28]
  |       +-> commit(normalized) if auto_commit=True
  +-> result returned

CR (Change Request) mechanism:
  - CR_000_TEST.json in A_00_ARCHITECTURE/CHANGE_REQUESTS/
  - Read by guards during pre-flight validation
  - Contains: target_files, rollback_required, compile_required, test_required
  - MANUALLY CREATED - no automated CR generation found in codebase
```

### Назначение каждого ключевого файла

| Файл | Назначение | Подтверждено в коде |
|------|-----------|-------------------|
| `smart_dispatcher_v2.py` | Главный маршрутизатор: intent detection -> TaskExecutor -> department iteration | line 282-431 |
| `butler_harness.py` | Execution wrapper с pre-flight guards + post-flight validation | line 61-150+ |
| `base_department.py` | ABC contract: NAME, can_handle(), execute() | full file |
| `department_result.py` | Result validation: ok/status/error normalization | validate_department_result() |
| `router_registry.py` | Lightweight route name -> target module mapping (НЕ подключен к dispatch) | isolated class |
| `agent_router.py` | Keyword-based intent routing (НЕ подключён к dispatch) | isolated class |
| `anti_loop_budget.py` | Counter-based loop breaker (НЕ подключён к production) | defined, NOT USED |
| `frozen_core_guard.py` | Blocks A_01_CORE/ and chat_router.py modifications via CR validation | validate(cr_path) |
| `compile_guard.py` | py_compile for .py files; SKIPS non-existent files | validate(cr_path) |
| `rollback_guard.py` | Requires backup markers for modified files (if rollback_required=True) | validate(cr_path) |
| `integration_test_guard.py` | Runs test files if test_required=True in CR | validate(cr_path) |
| `observation_layer.py` | JSONL logger to A_08_LOGS/OBSERVATIONS.jsonl | record(source, event, payload) |

### Существующие extension points

1. **SmartDispatcherV2.departments list** - можно добавить новый Department в список
2. **TaskExecutor.plan()** - может возвращать steps с department=NEW_DEPT
3. **ButlerHarness.guards** - цепочка pre-flight guards (но CR нужен для активации)
4. **validate_department_result()** - базовая валидация результата

---

## ЗАДАЧА C: Тип интеграции Bionic

### Сравнение четырёх вариантов

#### Вариант 1: Department (наиболее подходит по контракту, но не по invocation)
```
OWNER -> SmartDispatcherV2.dispatch()
  |
for dept in departments:
  |-- CodingDepartment.can_handle("создай агента") -> False
  +-> BionicDepartment.can_handle("создай агента") -> True
    |
_execute_department(BionicDept, query)
  |-- harness.execute(...) with guards
  |-- executor() = BionicDept.execute(query)
  |   +-> ??? КАК ВЫЗВАТЬ BIONIC? NO PROGRAMMATIC API!
  +-> result returned
```

**Проблема:** Нет способа вызвать `BionicDept.execute()` программно.
Без programmatic interface, Department pattern не работает для автоматического вызова.

#### Вариант 2: Worker capability (НЕ ПОДХОДИТ)
Worker capability подразумевает что Butler может вызвать worker через API.
Нет API -> нет вызова.

#### Вариант 3: Tool (НЕ ПОДХОДИТ)
Tool - это функция/метод, который Butler вызывает напрямую.
Bionic не является функцией - это отдельное desktop приложение.

#### Вариант 4: External execution backend (теоретически возможен но не реализован)
Подразумевает внешний процесс с known interface.
Но Bionic НЕ предоставляет никакого external interface.

### Вывод по типу интеграции

**Bionic не может быть вызван программно из Butler.**
Единственный viable path - это **file-based handoff pattern**:
1. Butler создаёт structured task spec (TZ) в staging area
2. Человек или отдельный процесс передаёт spec в Bionic UI вручную
3. Bionic работает в своём Code Project с working_directory = Butler workspace
4. Butler проверяет артефакты на host filesystem

---

## ЗАДАЧА D: Delivery boundary - доказательство

### Bionic Code Project working directory <-> Windows Host

**Доказано через SQLite анализ:**

BUTLER_OMEGA_SMART coding project (`f960037a-...`):
- `projectType: "coding"`
- `working_directory`: установлен в Butler workspace (из project.json и session_json)

**Инструменты Bionic пишут НАПРЯМУЮ на Windows:**
- `lmstudio/sample-file-system/*` - createFolder, replaceFile, readFileLines -> прямой доступ к Windows filesystem
- `lmstudio/shell-v1` - shell_command -> выполнение команд в host shell
- `lmstudio/python-v1/runPython` - запуск Python кода на host

**Доказательство из TEST №2 (из BIONIC_LAB):**
Файлы, созданные Bionic через sample-file-system, были обнаружены на Windows host.

**Проблема TEST №9:**
Когда working_directory был misconfigured или указывал на internal workspace -> файлы шли в sandbox.

### Delivery boundary правило:
```
BIONIC PRODUCED  !=  DELIVERED
DELIVERED        !=  VERIFIED
VERIFIED         =  SYSTEM_ACCEPTANCE
```

**DELIVERED** только когда Butler independently проверяет:
- Файл существует по Windows path (Path.exists())
- Размер > 0
- UTF-8 encoding (decode succeeds)
- py_compile для .py файлов

---

## ЗАДАЧА E: Watchdog - observability

### EXTERNAL_TOOL_LOOP_OBSERVABILITY = NO

**Доказательство:**
1. Нет HTTP/WebSocket endpoint для мониторинга tool calls в реальном времени
2. Нет API для получения текущего состояния сессии (running/completed/failed)
3. SQLite базы доступны только read-only и обновляются внутри LM Studio process
4. AntiLoopBudget определён но НЕ подключён к production коду нигде

**Единственный watchdog:** HTTP-level timeout на LM Studio API call
(но это не применимо, так как нет programmatic Bionic invocation)

---

## ЗАДАЧА F: Lifecycle - состыковка с Harness

### Существующий Harness lifecycle:
```
1. Pre-flight guards (FrozenCore -> Rollback -> Compile -> IntegrationTest)
2. executor() = dept.execute(query, context)
3. validate_department_result(draft)
4. commit(normalized) if auto_commit=True
```

### Проблема с Bionic artifacts:
- **CompileGuard** пропускает несуществующие файлы (`if not target_file.exists(): continue`)
  -> Это хорошо для staging area (файлы ещё не созданы при pre-flight)
- **RollbackGuard** требует backup markers только если `rollback_required=True`
  -> Для new-file-only operations можно установить `rollback_required=False`
- **FrozenCoreGuard** блокирует A_01_CORE/ и chat_router.py
  -> Bionic staging area НЕ должна быть в A_01_CORE/

### Как Harness может работать с Bionic:
```
ButlerHarness.execute(
    department_name="BIONIC",
    task=task_spec,
    executor=lambda: bionic_dept.execute(task_spec),  # <-- НЕТ API!
    auto_commit=True,
    cr_name="CR_BIONIC_STAGING.json"
)
```

**Критическая проблема:** `executor()` не может вызвать Bionic без programmatic interface.

---

## ЗАДАЧА G: Shell discrepancy explanation

### Почему shell-v1 заявлен в project config но отсутствовал в TEST №1B?

**Доказательство из SQLite:**
- BUTLER_OMEGA_SMART coding project имеет `lmstudio/shell-v1` с `yolo:true` params
- BIONIC_LAB coding project также имеет `lmstudio/shell-v1` с `yolo:true` params
- Regular projects (Default, RTX 3090 Research) НЕ имеют shell module

**Причины discrepancy:**
1. **Тип проекта:** Только `projectType: "coding"` получает shell-v1
2. **Session configuration:** Shell доступен только если session создан в coding project
3. **TEST №1B сессия:** Вероятно, была создана в regular project или без shell-ngModule активированным

**Ключевой вывод:** Для Bionic Worker integration нужно использовать coding project
с working_directory = Butler workspace и shell-v1 enabled.

---

## РЕКОМЕНДУЕМЫЙ ТИП ИНТЕГРАЦИИ

### File-Based Handoff Pattern (единственный viable path)

```
OWNER REQUEST -> Butler
  |
Butler решает: использовать Bionic?
  |
Butler создаёт structured task spec в staging area
  |
[HANDOFF POINT - human or automated trigger]
  |
Bionic читает spec из working_directory (Code Project)
  |
Bionic работает в своём session, создаёт артефакты
  |
Butler проверяет артефакты на host filesystem:
  |-- exists?
  |-- size > 0?
  |-- UTF-8 valid?
  |-- py_compile для .py?
  +-> content/schema validation?
  |
VERIFIED -> SYSTEM_ACCEPTANCE=PASS
NOT VERIFIED -> SYSTEM_ACCEPTANCE=FAIL
```

### Почему не pure Department pattern:
1. Нет programmatic Bionic API для вызова `dept.execute()`
2. Нет telemetry для watchdog во время выполнения
3. Нет способа остановить зависшую сессию извне
4. Нет способа получить список tool calls в реальном времени

---

## МИНИМАЛЬНЫЕ ФАЙЛЫ ДЛЯ ИЗМЕНЕНИЯ

### Существующие файлы (изменить):

| Файл | Изменение | Обоснование |
|------|-----------|-------------|
| `A_02_MANAGERS/smart_dispatcher_v2.py` | Добавить BionicDepartment в departments list | Точка маршрутизации |
| `A_03_ORCHESTRATION/butler_harness.py` | Добавить post-execution artifact validation hook | Evidence gate integration |

### Новые файлы (создать):

| Файл | Необходимость | Доказательство |
|------|--------------|---------------|
| `A_04_AGENTS/BionicDepartment/runner.py` | ОБЯЗАТЕЛЬНО | Реализация can_handle() + execute() для BionicDept |
| `A_03_ORCHESTRATION/evidence_gate.py` | ОБЯЗАТЕЛЬНО | File-level validation (exists, py_compile, utf8) |
| `A_06_WORKSPACE/BIONIC_STAGING/` | ОБЯЗАТЕЛЬНО | Bounded staging workspace для артефактов |
| `A_03_ORCHESTRATION/bionic_task_logger.py` | ЖЕЛАТЕЛЬНО | Structured logging per TZ 25 |

### Файлы которые больше НЕ нужны:
- ~~`bionic_bridge.py`~~ - не нужен, нет programmatic API для bridge
- ~~`watchdog.py`~~ - не нужен, EXTERNAL_TOOL_LOOP_OBSERVABILITY = NO
- ~~`session_manager.py`~~ - не нужен, Bionic sessions управляются LM Studio UI

---

## E2E СЦЕНАРИИ (без выполнения)

### Positive E2E:
```
1. OWNER: "Создай небольшого локального агента для заметок со сводкой"
2. Butler -> SmartDispatcherV2.dispatch() -> BionicDepartment.can_handle() = True
3. Butler создаёт task spec в A_06_WORKSPACE/BIONIC_STAGING/
4. [Human trigger: Bionic читает spec и работает]
5. Bionic создаёт agent.py, main.py в staging area
6. Butler EvidenceGate.validate():
   |-- Path("agent.py").exists() -> True
   |-- py_compile("agent.py") -> Success
   |-- UTF-8 decode -> Success
   +-> Content check: has note-taking + summary logic
7. SYSTEM_ACCEPTANCE = PASS
```

### Negative E2E - TEST 8 (Tool Loop):
```
1. Bionic повторяет одинаковый tool call N раз без прогресса
2. EXTERNAL_TOOL_LOOP_OBSERVABILITY = NO -> watchdog невозможен externally
3. Единственный fallback: HTTP timeout на API call
4. Ожидание: ABORTED_NO_PROGRESS после timeout
```

### Negative E2E - TEST 9 (Delivery Failure):
```
1. Bionic claims: "File agent.py created"
2. Butler EvidenceGate.validate():
   |-- Path("agent.py").exists() -> False
3. SYSTEM_ACCEPTANCE = FAIL
4. BIONIC_CLAIM=PASS != SYSTEM_ACCEPTANCE=FAIL (разделены!)
```

### Retry E2E:
```
1. Attempt 1: Bionic session fails/timeout -> FAIL logged
2. Clean session / new task spec
3. Attempt 2: Bionic succeeds -> PASS logged
4. Final status: PASS_AFTER_RETRY
5. Журнал отражает обе попытки
```

### Regression Departments:
```
1. "Напиши fibonacci на Python" -> CodingDepartment.can_handle() = True OK
2. "Создай картинку дракона" -> ImageDepartment.can_handle() = True OK
3. "Найди документ про станок" -> SearchDepartment.can_handle() = True OK
4. "Привет, как дела?" -> HomeDepartment.can_handle() = True OK
5. BionicDepartment должен быть ПОСЛЕ CodingDepartment и ПЕРЕД HomeDepartment
```

---

## КРИТЕРИИ ФИНАЛЬНОГО PASS ИНТЕГРАЦИИ (TZ 30)

| Требование | Статус | Комментарий |
|-----------|--------|-------------|
| Существующие Departments не сломаны | OK Гарантировано | Bionic добавляется в конец списка, HomeDepartment - fallback |
| Bionic вызывается как подчиненный Worker | PARTIAL | Нет programmatic API -> file-based handoff |
| Bounded scope соблюдается | OK Реализуемо | Staging area + authorized_paths in task spec |
| Self-report != evidence | OK Реализуемо | EvidenceGate independent validation |
| Host delivery проверяется | OK Реализуемо | Path.exists() + py_compile + UTF-8 check |
| Watchdog работает | NO НЕВОЗМОЖНО externally | EXTERNAL_TOOL_LOOP_OBSERVABILITY = NO |
| Real Windows E2E выполняется | OK Реализуемо | Butler запускает созданные .py файлы |
| FAIL блокирует acceptance | OK Реализуемо | EvidenceGate returns validated=False -> SYSTEM_ACCEPTANCE=FAIL |
| UTF-8 сохранён | OK Реализуемо | Все file operations с encoding="utf-8" |
| Нет архитектурного хардкода | OK Реализуемо | Generic evidence gate, not prompt-specific |

---

## ИТОГОВЫЙ СТАТУС

**BLOCKED: EXTERNAL_TOOL_LOOP_OBSERVABILITY = NO**
**BLOCKED: PROGRAMMATIC_BIONIC_INTERFACE = NOT FOUND**

Без programmatic Bionic API интеграция возможна ТОЛЬКО через file-based handoff pattern,
что требует human-in-the-loop или отдельного trigger mechanism.

Для fully autonomous integration требуется:
1. LM Studio должен предоставить external API для управления Bionic сессиями
2. ИЛИ Bionic должен поддерживать headless/CLI mode с known interface
3. ИЛИ Butler должен интегрироваться через MCP (Model Context Protocol) если LM Studio его поддерживает

**До получения одного из вышеперечисленных условий:**
ЭТАП 3 НЕ НАЧИНАТЬ.

---

## ИЗМЕНЁННЫЙ ФАЙЛ: A_04_AGENTS/BionicDepartment/__init__.py

- **Размер:** ~500 bytes
- **Содержимое:** Docstring-only, определяет принципы Bionic как untrusted Worker/Builder
- **Статус:** Не развивать до approval Этап 3
