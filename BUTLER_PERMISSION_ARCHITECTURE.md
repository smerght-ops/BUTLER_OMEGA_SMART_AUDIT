# BUTLER OMEGA SMART — критическая ревизия архитектуры Permission Engine

## 1. Исходная проблема

Штатный путь Department проходит через
`SmartDispatcherV2._execute_department()` и `ButlerHarness.execute()`, однако в Butler
есть прямые и вложенные вызовы:

- `voice_input._recognize_audio()` → `AudioDepartment.execute()`;
- `chat_router.handle_draw()` → `ImageDepartment.execute()`;
- `SearchDepartment._resolve_web_confirmation()` → `BrowserDepartment.execute()`;
- `CodingDepartment/DISPATCHER.execute()` → `CodingDepartment.execute()`.

Кроме основного `A_04_AGENTS.base_department.BaseDepartment`, проект содержит второй
контракт `A_10_BUTLER_OS/00_PRODUCTION/core/department_contract.py::Department`.
Следовательно, утверждение, что один `BaseDepartment` уже является доказанной общей
границей любого Department во всём проекте, неверно.

Цель архитектуры — один явный механизм принятия permission-решения для каждого
фактического запуска Department, без изменения публичного `Department.execute()` и
без переноса ответственности в Provider, Planner или произвольный Harness callback.

## 2. Критическая ревизия DepartmentExecutionProxy

Ранее был выбран автоматический proxy, устанавливаемый из
`BaseDepartment.__init_subclass__()`. Ниже решение рассматривается как потенциально
ошибочное.

Шкала вероятности: низкая — маловероятно при обычной эксплуатации; средняя — реалистично
при развитии проекта; высокая — уже следует из текущего кода или неизбежна при обычной
поддержке.

| Недостаток | Серьёзность | Последствия | Вероятность |
|---|---|---|---|
| Охватывается только наследование от `A_04_AGENTS.BaseDepartment` | Критическая | Второй контракт Department и будущие несовместимые реализации смогут полностью обойти Permission Engine | Высокая: второй контракт уже существует |
| Скрытая подмена `execute()` во время создания класса | Высокая | Runtime-поведение отличается от видимого исходного метода; сложнее отладка, профилирование и анализ stack trace | Высокая |
| Зависимость слоя `A_04_AGENTS` от orchestration permission-пакета | Высокая | Инверсия существующих зависимостей и риск циклического импорта при расширении middleware/logger | Средняя |
| Хрупкое извлечение `query` и `context` из произвольных сигнатур | Высокая | Неверный PermissionRequest для `text`, positional context, специальных kwargs и будущих сигнатур | Средняя |
| Нельзя надёжно запретить замену метода после создания класса | Высокая | Monkey patch, instance attribute или decorator более позднего этапа может обойти proxy | Низкая сейчас, средняя при развитии |
| Наследник, не объявляющий собственный `execute()`, зависит от неочевидного поведения wrapper inheritance | Средняя | Повторная проверка или отсутствие ожидаемой metadata при сложной иерархии | Средняя |
| Риск двойного оборачивания при reload/import tooling | Средняя | Два permission-решения и два события логирования на одно исполнение | Средняя в тестах и интерактивной разработке |
| `functools.wraps` сохраняет метаданные, но не фактическую Python-сигнатуру wrapper | Средняя | Framework или код, анализирующий callable нестандартным способом, может увидеть `*args/**kwargs` | Низкая |
| Permission check происходит после выбора Department | Средняя | Для будущего запрета самого факта маршрутизации или раскрытия capability точка слишком поздняя | Средняя на будущих этапах |
| Глобальная автоматическая активация при импорте | Высокая | Нельзя безопасно создать Department для discovery/inspection без побочных permission-событий | Высокая для существующих scanners |
| Неявная политика отказа при внутренней ошибке proxy | Критическая | Ошибка Permission Engine может неожиданно заблокировать весь Butler либо небезопасно пропустить действие | Средняя до явного fail-open/fail-closed контракта |
| Сложнее локально отключить интеграцию для теста | Средняя | Тесты Department становятся связанными с глобальным middleware и logger state | Высокая |
| Наблюдаемость не показывает явного caller boundary | Средняя | По коду call site невозможно увидеть, что выполняется security-sensitive операция | Высокая |
| Обход через вызов сохранённой ссылки на исходный callable | Высокая | Код, получивший `__wrapped__` или исходную функцию до установки proxy, может выполнить её напрямую | Низкая |
| Автоматическая магия усложняет Stage 2 с `READ/WRITE/EXECUTE/EXTERNAL` | Высокая | Wrapper видит общий query, но может не знать фактическое действие, ресурс и момент побочного эффекта | Высокая |

### Итог ревизии proxy

Автоматический `__init_subclass__`-proxy минимален по числу изменяемых файлов, но эта
минимальность достигнута ценой скрытого runtime-поведения и неполной доказуемости
охвата. Он не должен оставаться выбранной архитектурой.

## 3. Альтернативные архитектуры

### Вариант A. Permission в `SmartDispatcherV2._execute_department()` плюс исправление обходов

Схема:

```text
caller → dispatcher/bridge → SmartDispatcherV2._execute_department()
       → PermissionMiddleware → ButlerHarness → Department.execute()
```

Все прямые маршруты переносятся в Dispatcher или получают специальный вызов его
внутреннего execution boundary.

- Сложность внедрения: средняя.
- Изменяемые existing-файлы: ориентировочно 5–7.
- Совместимость с Butler: средняя; voice, image и nested Browser придётся подчинить
  диспетчеризации, которая раньше могла не выполнять повторный выбор Department.
- Совместимость с будущими этапами: хорошая для маршрутизируемых задач.
- Риски: рекурсивная диспетчеризация, повторная классификация query, изменение context,
  случайный выбор другого Department.
- Откат: простой по отдельным call sites, но несколько backups.

Вердикт: лучше автоматического proxy по явности, но смешивает выбор маршрута и контроль
уже выбранного Department.

### Вариант B. Permission внутри `ButlerHarness.execute()` и обязательный Harness

Схема:

```text
caller → ButlerHarness.execute(department metadata, executor)
       → PermissionMiddleware → executor → validation/commit
```

Прямые вызовы voice/image/search/coding оборачиваются Harness. Для Department вводится
обязательный признак или отдельный метод Harness.

- Сложность внедрения: средняя.
- Изменяемые existing-файлы: ориентировочно 5–6.
- Совместимость с Butler: средняя; Harness уже существует, но используется также для
  worker callback и несёт guards, не относящиеся к каждому runtime-действию.
- Совместимость с будущими этапами: средняя.
- Риски: смешение permission и Change Request guards; ложные проверки non-Department
  callback; изменение поведения прямых быстрых путей из-за pre-flight guards.
- Откат: средний, поскольку меняется центральный Harness и обходные маршруты.

Вердикт: повторно использует готовый pipeline, но перегружает его новой ответственностью.

### Вариант C. Явный DepartmentExecutionGateway — выбран

Вводится один небольшой gateway, который не выбирает Department и не выполняет guards.
Он только принимает уже выбранный объект, строит PermissionRequest, получает решение и
вызывает исходный `execute()`.

```text
caller
→ DepartmentExecutionGateway.execute(department, query, context, **kwargs)
→ PermissionMiddleware.evaluate(...)
→ PermissionEngine.decide(...)
→ PermissionLogger.record(...)
→ department.execute(query, context, **kwargs)
→ Result
```

Текущие production call sites явно переводятся на gateway:

| Маршрут | Изменение |
|---|---|
| `SmartDispatcherV2._execute_department()` | Внутри существующего Harness executor вызывать gateway вместо `dept.execute()` |
| `voice_input._recognize_audio()` | Перенаправить прямой Audio-вызов в gateway |
| `chat_router.handle_draw()` | Перенаправить прямой Image-вызов в gateway без повторной маршрутизации |
| `SearchDepartment._resolve_web_confirmation()` | Перенаправить Browser-вызов в gateway; это отдельное вложенное permission-решение |
| `CodingDepartment/DISPATCHER.execute()` | Перенаправить compatibility adapter в gateway |
| `Worker → ButlerHarness` | Оставить как есть: callback не является Department |

- Сложность внедрения: средняя, изменения механические и локальные.
- Изменяемые existing-файлы: 5; новых production-файлов ориентировочно 5–6 плюс тест.
- Совместимость с Butler: высокая; маршрутизация, Harness, Department API и результаты
  сохраняются.
- Совместимость с будущими этапами: высокая; gateway получает явный Department,
  query/context и позже сможет принимать нормализованные action/resource metadata.
- Риски: новый или забытый call site может вызвать `department.execute()` напрямую.
  Риск закрывается обязательным AST-тестом архитектурной границы и allowlist для самого
  gateway и реализаций методов.
- Откат: высокий уровень управляемости; восстановить пять маленьких call-site patches,
  после чего новые модули становятся недостижимыми.

### Вариант D. Template Method в `BaseDepartment`

`BaseDepartment.execute()` становится единственной concrete/final реализацией, внутри
вызывает Permission Engine, а каждый Department переименовывает текущий `execute()` в
`_execute_impl()`.

- Сложность внедрения: высокая.
- Изменяемые existing-файлы: не менее 16 — базовый класс и все активные Department.
- Совместимость с Butler: средняя; публичный вызов сохраняется, но внутренний контракт
  каждого Department меняется.
- Совместимость с будущими этапами: высокая после миграции.
- Риски: массовый patch, пропущенный Department, несовместимость со вторым контрактом,
  большие regression/rollback затраты.
- Откат: сложный из-за количества файлов.

Вердикт: строгая объектная граница, но непропорциональна Stage 1.

### Вариант E. Decorator на каждом Department.execute()

Каждая реализация явно получает `@permission_checked`.

- Сложность внедрения: средне-высокая.
- Изменяемые existing-файлы: не менее 15.
- Совместимость с Butler: высокая на уровне API.
- Совместимость с будущими этапами: средняя; metadata можно задавать явно.
- Риски: забытый decorator, неравномерная конфигурация, массовый import dependency.
- Откат: сложный из-за числа файлов.

Вердикт: явнее автоматического proxy, но уступает gateway по числу изменений и
централизованности.

## 4. Сводное сравнение

| Архитектура | Сложность | Existing-файлы | Совместимость сейчас | Будущие этапы | Главный риск | Откат |
|---|---:|---:|---|---|---|---|
| A. Dispatcher boundary | Средняя | 5–7 | Средняя | Хорошая | Повторная маршрутизация | Простой/средний |
| B. Harness middleware | Средняя | 5–6 | Средняя | Средняя | Смешение guards и permissions | Средний |
| C. Явный Gateway | Средняя | 5 | Высокая | Высокая | Забытый direct call | Простой |
| D. Template Method | Высокая | ≥16 | Средняя | Высокая | Массовая миграция | Сложный |
| E. Decorators | Средне-высокая | ≥15 | Высокая | Средняя | Пропущенный decorator | Сложный |
| Старый automatic proxy | Низкая | 1 | Внешне высокая | Низкая/средняя | Скрытый и неполный охват | Простой |

## 5. Выбранная архитектура

Выбран **вариант C: явный `DepartmentExecutionGateway` плюс архитектурный AST-тест**.

Он превосходит остальные варианты по совокупности причин:

1. Не изменяет алгоритм выбора Department и не заставляет прямой вызов проходить
   повторную маршрутизацию.
2. Не смешивает Permission Engine с guards, commit и произвольными callback Harness.
3. Делает security boundary видимой в каждом production call site и stack trace.
4. Сохраняет существующий `Department.execute()` и Result Contract.
5. Позволяет вложенному `SearchDepartment → BrowserDepartment` получить отдельное
   решение, что важно для будущего `EXTERNAL`.
6. Изменяет ограниченное число файлов простыми однотипными patches.
7. Допускает dependency injection PermissionEngine/Logger в тестах без глобальной
   подмены классов.
8. Расширяется до `READ`, `WRITE`, `EXECUTE`, `EXTERNAL` через явные metadata, не
   заставляя wrapper угадывать действие только по query.
9. Архитектурный AST-тест превращает правило «не вызывать Department напрямую» из
   соглашения в автоматически проверяемый инвариант.

AST-тест должен сканировать актуальный production-код и запрещать вызовы `.execute()`
на объектах Department вне:

- реализаций самих Department;
- `DepartmentExecutionGateway`;
- явно документированного тестового allowlist.

Первоначально тест фиксирует пять известных call sites и должен стать зелёным только
после их перенаправления. Любой новый обход ломает CI/acceptance.

## 6. План файлов будущей реализации

### Изменяемые existing-файлы

1. `A_02_MANAGERS/smart_dispatcher_v2.py`;
2. `A_09_INTERFACE/voice_input.py`;
3. `A_03_ORCHESTRATION/chat_router.py`;
4. `A_04_AGENTS/SearchDepartment/runner.py`;
5. `A_04_AGENTS/CodingDepartment/DISPATCHER.py`.

Перед изменением каждого файла требуется отдельный timestamped backup. Frozen Core не
затрагивается. `BaseDepartment`, `AgentCoreCoordinator`, Department implementations и
публичные сигнатуры не меняются.

### Новые файлы

```text
A_03_ORCHESTRATION/permission/
├── __init__.py
├── models.py
├── engine.py
├── middleware.py
├── gateway.py
└── logger.py

A_09_TESTS/
└── test_permission_engine_stage1.py
```

`test_permission_engine_stage1.py` должен проверить:

- allow-only решение и неизменность результата;
- ровно одно решение на один gateway execution;
- отдельные решения для вложенных Department;
- проброс исключений/контролируемых ошибок без искажения;
- сохранение positional и keyword context;
- отсутствие запрещённых production-вызовов по AST;
- независимость discovery/создания экземпляра Department от Permission Engine.

## 7. Почему DepartmentExecutionProxy больше не выбран

После критического анализа `DepartmentExecutionProxy` **не остался лучшим вариантом**.
Его преимущество — один изменяемый файл — не компенсирует скрытую подмену методов,
неполный охват альтернативного контракта, слабую action/resource семантику и сложность
диагностики. Явный gateway требует на четыре существующих файла больше, но создаёт
проверяемую, прозрачную и расширяемую архитектурную границу.

## 8. Ограничения Stage 1

На следующем этапе Permission Engine по-прежнему должен всегда возвращать `ALLOW`.
Запрещены реальные deny-правила, классификация намерений, запросы пользователю и
изменение пользовательского поведения. После реализации обязательны backup,
`py_compile`, UTF-8 без BOM, unit/integration tests и команды ручного rollback.
