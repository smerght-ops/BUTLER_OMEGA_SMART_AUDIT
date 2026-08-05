# Шаг 3 — создание CSV из табличных данных

Дата: 2026-07-16
Статус: **PASS**
Capability Status: **PROVEN**

## Изменения

- `A_03_HANDLERS\spreadsheet_handler.py`: атомарное создание CSV стандартным модулем `csv`, UTF-8 BOM, верификация.
- `A_04_AGENTS\DocumentsDepartment\runner.py`: разбор CSV-команды и существующий Result Contract.

Откат: `A_00_RESTORE\DOCUMENT_CREATE_STEP3_20260716_100318`.

## Observation

Все пользовательские проверки выполнены исключительно через:

`START_BUTLER_OS.bat -> START_BUTLER_OS.ps1 -> BUTLER_OS.py`

Команда:

`Создай CSV "C:\Test\data.csv" с данными: Имя,Возраст; Анна,25; Борис,30`

Результат: `DOCUMENTS | model=SpreadsheetHandler | CSV успешно создан.`

Чтение `Прочитай документ "C:\Test\data.csv"` вернуло колонки `Имя`, `Возраст` и строки `Анна 25`, `Борис 30`
в исходном порядке.

Повторное создание вернуло `CSV_TARGET_EXISTS`. Команда без данных вернула `CREATE_FAILED` и понятный текст
`Не указаны данные для CSV.`

Регрессии:

- XLSX: `C:\Test\data.xlsx` прочитан через `DOCUMENTS/SpreadsheetHandler`, данные совпали;
- DOCX: `C:\Test\report.docx` прочитан через `DOCUMENTS/DocxHandler`, ответ `Отчёт Butler`.

## Evidence

`C:\Test\data.csv`:

- size_bytes: 54;
- SHA-256: `fe3d88a17028007f748f624cff220872eefe9166414282e8417eb1236fdf5c41`;
- первые байты: `EF BB BF` (UTF-8 BOM);
- delimiter: `,`;
- строки: `[["Имя","Возраст"],["Анна","25"],["Борис","30"]]`;
- row_count: 3;
- column_count: 2.

Глубокая папка создана автоматически официальным Butler:

`C:\Test\ButlerCsvDeep\Level1\Level2\deep.csv`

- size_bytes: 41;
- SHA-256: `8e49c697cff1e87d0522240385d410ffbad27f61fd63db47a4099876fd76af13`;
- UTF-8 BOM присутствует;
- строки: `[["Имя","Значение"],["Анна","42"]]`.

Harness evidence в `A_08_LOGS\OBSERVATIONS.jsonl`: `HARNESS_V3_START/HARNESS_V3_SUCCESS` для создания и чтения
обоих CSV; `DEPARTMENT_CONTROLLED_FAILURE` с `CSV_TARGET_EXISTS` для повтора.

Result Contract успешной операции:

- `ok=true`, `department=DOCUMENTS`, `model=SpreadsheetHandler`, `error=null`;
- metadata: `operation=create_csv`, `target_path`, `size_bytes`, `row_count`, `column_count`,
  `encoding=utf-8-sig`, `delimiter=,`.

## py_compile

PASS, exit code 0:

- `A_03_HANDLERS\spreadsheet_handler.py`;
- `A_04_AGENTS\DocumentsDepartment\runner.py`;
- регрессионно `A_03_HANDLERS\docx_handler.py`.

## Proven Statement

Через обязательный официальный launcher доказано, что Butler создаёт CSV из прямоугольных текстовых данных с
кириллицей, корректным UTF-8 BOM и запятой, автоматически создаёт целевые папки, запрещает перезапись, контролируемо
отклоняет отсутствие данных и читает созданный файл существующим `SpreadsheetHandler`. Регрессии DOCX/XLSX не обнаружены.

## Conclusion

**PASS**. Пользовательская возможность «Создание CSV» имеет статус **PROVEN**.
