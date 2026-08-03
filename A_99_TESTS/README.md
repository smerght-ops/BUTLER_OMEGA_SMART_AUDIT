# Butler Omega Smart Acceptance Runner

Постоянный приёмочный и регрессионный Runner проверяет официальный программный маршрут `dispatcher_bridge_v2 → SmartDispatcherV2 → ButlerHarness → Department → Result Contract`.

## Запуск

- Быстрая проверка: `START_FAST_ACCEPTANCE.bat`.
- Полная production-проверка: `START_FULL_ACCEPTANCE.bat`.

FAST проверяет синтаксис, импорт Runtime, регистрацию, маршрутизацию и недорогие официальные сценарии. FULL дополнительно выполняет реальные provider-вызовы, memory persistence, Search/OpenDocument, Vision, Documents, Archive и IMAGE-контекст.

## Статусы и exit codes

- `PASS` — ожидания подтверждены поведением.
- `FAIL` — обязательное ожидание нарушено.
- `SKIP` — реальный provider или официальный fixture отсутствует; PASS не имитируется.
- `0` — обязательные сценарии прошли; `1` — есть FAIL; `2` — Runner/Runtime не инициализирован; `3` — storage cleanup завершился ошибкой.

Отчёты находятся в `A_99_TESTS/reports`. Файлы `latest_acceptance_report.json` и `.md` всегда указывают на последний запуск соответствующего режима.

## Storage safety

До изменяющих сценариев Runner копирует перечисленные в конфигурации storage-файлы. В `finally` исходное состояние восстанавливается. Ошибка восстановления даёт exit code 3.

## Добавление сценария

Добавьте декларацию в `acceptance_config.json`: имя, режимы, команду, ожидаемый Department, обязательные подстроки, timeout, critical/provider flags, fixture и cleanup policy. Python-код в JSON не хранится.

## Норматив после изменений Codex

После любого изменения Runtime, Dispatcher, Department, Memory, Session, Router, Result Contract или Storage исполнитель обязан:

1. выполнить py_compile изменённых файлов;
2. выполнить START_FAST_ACCEPTANCE.bat;
3. выполнить START_FULL_ACCEPTANCE.bat для крупных изменений;
4. приложить latest_acceptance_report.md;
5. не объявлять STATUS: COMPLETED, если обязательные ранее проходившие сценарии стали FAIL.

Если baseline уже содержит известные FAIL, новые изменения не должны увеличивать их количество; исправленный сценарий должен стать PASS, существующий PASS не должен стать FAIL, а baseline FAIL перечисляются отдельно.
