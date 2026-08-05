# Research Before Change — документный блок Butler

Дата: 2026-07-16
Рабочий корень: `C:\Users\KOS\Desktop\Butler_Agent\BUTLER_OMEGA_SMART`
Режим: READ ONLY для production-кода
Research Status: **INCONCLUSIVE**
Итог: исследование не завершено из-за невозможности запустить свежий официальный Butler в закреплённом runtime без изменения окружения.

## Блокирующее доказательство

Точная команда запуска исследовательского процесса из основного корня:

`C:\Users\KOS\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe A_09_TESTS\documents_research_v3.py`

Процесс завершился до создания тестовых данных и до первого пользовательского сценария. Импорт официального маршрута
`dispatcher_bridge_v2.dispatch -> SmartDispatcherV2` импортирует все Department; импорт
`A_04_AGENTS\ImageDepartment\runner.py` завершился исключением:

`ModuleNotFoundError: No module named 'requests'`

Дополнительный probe закреплённого Python:

`{'requests': False, 'docx': True, 'pandas': True, 'openpyxl': True, 'pypdf': True}`

Установка `requests`, изменение production-импортов или runtime-подмена запрещены заданием. Поэтому официальные пользовательские проверки не могут быть достоверно выполнены.

Research Status блокера: **REPRODUCED**.
Assertion Status: **PROVEN**.
Proven Statement: в исследованном закреплённом runtime свежий официальный dispatch не импортируется при неизменённом production-коде из-за отсутствующего обязательного для импорта `requests`.

## Статическая карта Department

Фактический порядок релевантных Department в `SmartDispatcherV2.departments`:

1. `OPEN_DOCUMENT` — `A_04_AGENTS\OpenDocumentDepartment\runner.py`;
2. `DOCUMENTS` — `A_04_AGENTS\DocumentsDepartment\runner.py`;
3. `PROJECT_DOCUMENTATION` — `A_04_AGENTS\ProjectDocumentationDepartment\runner.py`.

`OPEN_DOCUMENT` распознаёт намерения открыть/запустить/показать физический файл. `DOCUMENTS` распознаёт чтение,
извлечение и анализ документов и содержит карту Handler по расширениям. `PROJECT_DOCUMENTATION` обслуживает
документацию, статус и архитектуру самого проекта.

## Зарегистрированные форматы и Handler

| Расширение | Department | Handler | Статически найденный режим | Статус без официальной проверки |
|---|---|---|---|---|
| `.txt` | DOCUMENTS | TextHandler | чтение UTF-8/UTF-8-SIG/CP1251/Latin-1 | IMPLEMENTED_NOT_PROVEN |
| `.md` | DOCUMENTS | TextHandler | чтение как обычного текста | IMPLEMENTED_NOT_PROVEN |
| `.log` | DOCUMENTS | TextHandler | чтение как обычного текста | IMPLEMENTED_NOT_PROVEN |
| `.docx` | DOCUMENTS | DocxHandler | извлечение непустых абзацев через python-docx | IMPLEMENTED_NOT_PROVEN |
| `.csv` | DOCUMENTS | SpreadsheetHandler | `pandas.read_csv`, табличный текст | IMPLEMENTED_NOT_PROVEN |
| `.xlsx` | DOCUMENTS | SpreadsheetHandler | `pandas.read_excel`, все листы | IMPLEMENTED_NOT_PROVEN |
| `.pdf` | DOCUMENTS | PDFHandler | текст; OCR fallback; пользовательские PDF-операции | ранее подтверждённый контроль, в этом запуске INCONCLUSIVE |

Отдельный `A_03_HANDLERS\registry.py` также регистрирует `CodeHandler`, `ImageHandler` и `ArchiveHandler`, но они не
включены в карту `DocumentsDepartment.handlers` и потому не доказаны как часть официального DOCUMENTS-маршрута.

## Публичные внутренние структуры

`TextHandler.extract`, `DocxHandler.extract`, `SpreadsheetHandler.extract` и `PDFHandler.extract` возвращают внутренний
словарь `success`, `text`, `metadata`. Официальный `DocumentsDepartment` преобразует его в Result Contract с полями
`ok`, `department`, `model`, `latency_ms`, `text`, `error`, `metadata`.

## Зависимости

| Библиотека | Назначение | Доступность | Поведение/ограничение |
|---|---|---:|---|
| python-docx (`docx`) | DOCX | установлена | импортируется обязательно в DocxHandler |
| pandas | CSV/XLSX | установлена | импортируется внутри операции |
| openpyxl | XLSX engine/создание fixture | установлена | доступна |
| pypdf | PDF | установлена | доступна как fallback вместо PyPDF2 |
| PyPDF2 | PDF | отсутствует | PDFHandler использует pypdf fallback |
| PyMuPDF (`fitz`) | PDF render/OCR/export | отсутствует | контролируемые ограничения PDF |
| Pillow | изображения/PDF | установлена | доступна |
| reportlab | PDF из текста | установлена | доступна |
| requests | импорт ImageDepartment при старте dispatcher | **отсутствует** | блокирует импорт свежего официального Butler |

## Матрица возможностей (граница статического исследования)

| Формат | Открыть | Читать | Извлечь текст | Данные/таблицы | Анализ | Информация | Создать | Изменить | Сохранить | Экспорт |
|---|---|---|---|---|---|---|---|---|---|---|
| TXT/MD/LOG | INCONCLUSIVE | IMPLEMENTED_NOT_PROVEN | IMPLEMENTED_NOT_PROVEN | NOT_APPLICABLE | IMPLEMENTED_NOT_PROVEN | NOT_IMPLEMENTED | NOT_IMPLEMENTED | NOT_IMPLEMENTED | NOT_IMPLEMENTED | NOT_IMPLEMENTED |
| DOCX | INCONCLUSIVE | IMPLEMENTED_NOT_PROVEN | IMPLEMENTED_NOT_PROVEN | PARTIAL | IMPLEMENTED_NOT_PROVEN | NOT_IMPLEMENTED | NOT_IMPLEMENTED | NOT_IMPLEMENTED | NOT_IMPLEMENTED | NOT_IMPLEMENTED |
| CSV | INCONCLUSIVE | IMPLEMENTED_NOT_PROVEN | IMPLEMENTED_NOT_PROVEN | IMPLEMENTED_NOT_PROVEN | IMPLEMENTED_NOT_PROVEN | NOT_IMPLEMENTED | NOT_IMPLEMENTED | NOT_IMPLEMENTED | NOT_IMPLEMENTED | NOT_IMPLEMENTED |
| XLSX | INCONCLUSIVE | IMPLEMENTED_NOT_PROVEN | IMPLEMENTED_NOT_PROVEN | IMPLEMENTED_NOT_PROVEN | IMPLEMENTED_NOT_PROVEN | NOT_IMPLEMENTED | NOT_IMPLEMENTED | NOT_IMPLEMENTED | NOT_IMPLEMENTED | NOT_IMPLEMENTED |
| PDF | ранее доказано | ранее доказано | ранее доказано | NOT_APPLICABLE | PARTIAL | ранее доказано | ранее доказано | ранее доказано | ранее доказано | DEPENDENCY_MISSING для fitz-функций |

DOCX `PARTIAL` для таблиц означает: таблица может существовать в документе, но статический код извлекает только
`doc.paragraphs`; официальное поведение в этом исследовании не воспроизведено.

## Матрица пользовательских команд

Официально выполненных пользовательских команд: **0**. Импорт завершился до первого dispatch. Прямые вызовы Handler
не выполнялись и не использовались вместо официальной приёмки.

## READ ONLY и временные данные

- Production-код в ходе этого исследования не изменялся.
- Созданы только исследовательские файлы в `A_09_TESTS`.
- Каталог `C:\Test\ButlerDocumentsResearch_<TIMESTAMP>` не был создан: сбой произошёл на импорте до `fixtures()`.
- Остаточных каталогов `C:\Test\ButlerDocumentsResearch_*` не обнаружено.
- Установка и удаление библиотек не выполнялись.

## Функциональные пробелы для будущих отдельных ТЗ

- DOCX: таблицы и прочие структурные элементы не представлены в извлекаемом тексте; создание/изменение отсутствуют на найденном уровне кода.
- XLSX: найдено только чтение листов; создание/изменение/сохранение/экспорт не найдены в документной вертикали.
- CSV: найдено только чтение; изменение/сохранение/экспорт не найдены.
- TXT/MD/LOG: найдено только чтение текста; изменение и сохранение не найдены.

Это перечень статически найденных пробелов, не ТЗ и не проект архитектуры.

## Созданные исследовательские файлы

- `A_09_TESTS\documents_research_v3.py` — runner, остановившийся на импорте официального маршрута;
- `A_09_TESTS\DOCUMENTS_RESEARCH_V3_INCONCLUSIVE_20260716.md` — настоящий отчёт.

Итоговый Research Status: **INCONCLUSIVE**.
Итоговый вывод: **исследование не завершено**; обязательная официальная пользовательская проверка невозможна в текущем закреплённом runtime без запрещённого изменения окружения.
