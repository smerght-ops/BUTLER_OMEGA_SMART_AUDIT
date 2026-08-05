# Шаг 2 — создание XLSX из табличных данных

Дата: 2026-07-16
Статус: **PASS**
Capability Status: **PROVEN**

## Изменения

- `A_03_HANDLERS\spreadsheet_handler.py`: атомарное создание XLSX через `openpyxl`, проверка пути, запрет перезаписи, верификация содержимого.
- `A_04_AGENTS\DocumentsDepartment\runner.py`: разбор команды создания XLSX и штатный Result Contract.

Новые Handler, Department, Router, API и контракты не создавались. Откат:
`A_00_RESTORE\DOCUMENT_CREATE_STEP2_20260716_093941`.

## Observation

Официальный запуск выполнен исключительно цепочкой:

`START_BUTLER_OS.bat -> START_BUTLER_OS.ps1 -> BUTLER_OS.py`

Launcher успешно прошёл Status Center, Memory Guardian, Ollama, ComfyUI и System Guardian.

Команда:

`Создай таблицу "C:\Test\data.xlsx" с данными: Имя,Возраст; Анна,25; Борис,30`

Результат Butler:

`DOCUMENTS | model=SpreadsheetHandler | XLSX успешно создан.`

Чтение:

`Прочитай документ "C:\Test\data.xlsx"`

вернуло лист `Sheet` и данные в порядке `Имя, Возраст / Анна, 25 / Борис, 30`.

Повторное создание вернуло контролируемую ошибку `XLSX_TARGET_EXISTS`.

Регрессия шага 1:

`Прочитай документ "C:\Test\report.docx"` -> `DOCUMENTS / DocxHandler` -> `Отчёт Butler`.

## Evidence

Основной XLSX:

- путь: `C:\Test\data.xlsx`;
- размер: 4912 bytes;
- SHA-256: `258d65b77289b14bffb5dc2331d9a1b7a80b6e63f6c6bc097adc499fe0b41932`;
- содержимое через `openpyxl`: `[["Имя","Возраст"],["Анна","25"],["Борис","30"]]`;
- row_count: 3;
- column_count: 2.

Глубокая несуществовавшая папка:

`Создай таблицу "C:\Test\ButlerXlsxDeep\Level1\Level2\deep.xlsx" с данными: Имя,Значение; Анна,42`

Результат: `DOCUMENTS / SpreadsheetHandler`, файл создан и прочитан официальным Butler.

- размер: 4882 bytes;
- SHA-256: `990edce76636bbd33c00409cfc24be2f7544852dd08fede264544129918d6f25`;
- содержимое: `[["Имя","Значение"],["Анна","42"]]`;
- row_count: 2;
- column_count: 2.

Harness evidence в `A_08_LOGS\OBSERVATIONS.jsonl`:

- `HARNESS_V3_START` и `HARNESS_V3_SUCCESS` для создания XLSX;
- `HARNESS_V3_SUCCESS` для чтения XLSX;
- `DEPARTMENT_CONTROLLED_FAILURE` с `XLSX_TARGET_EXISTS` для повтора;
- compile guard: `200_GUARD_OK`.

Result Contract реализации содержит:

- `ok=true`;
- `department=DOCUMENTS`;
- `model=SpreadsheetHandler`;
- `error=null`;
- metadata: `operation=create_xlsx`, `target_path`, `size_bytes`, `row_count`, `column_count`.

## py_compile

PASS, exit code 0:

- `A_03_HANDLERS\spreadsheet_handler.py`;
- `A_04_AGENTS\DocumentsDepartment\runner.py`;
- регрессионно `A_03_HANDLERS\docx_handler.py`.

## Маршрутизационное наблюдение

Команда глубокой проверки с заголовком `Код,Значение` была перехвачена `CODING` из-за слова «Код» и не создала файл.
С нейтральными табличными данными тот же путь и операция прошли через `DOCUMENTS`. Маршрутизация не изменялась;
наблюдение не скрывается и ограничено исследованной формулировкой.

## Proven Statement

Через обязательный официальный `START_BUTLER_OS.bat` доказано, что Butler создаёт XLSX из прямоугольных текстовых
данных с кириллицей, сохраняет порядок строк и столбцов, автоматически создаёт глубокую целевую папку, запрещает
перезапись и затем читает созданный файл через `DocumentsDepartment/SpreadsheetHandler`. Чтение DOCX не нарушено.

## Conclusion

**PASS**. Пользовательская возможность «Создание XLSX» имеет статус **PROVEN**.
