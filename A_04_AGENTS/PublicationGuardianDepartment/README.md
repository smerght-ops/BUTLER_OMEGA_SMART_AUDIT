# PublicationGuardianDepartment

Обязательный fail-closed контур проверки публикаций, реализующий Publication Guardian API v1.

Публичная точка входа — `PublicationGuardianDepartment.execute()`. Формальный запрос передаётся
в `context["publication_request"]`; полный `PublicationResult` возвращается в
`metadata["publication_result"]`, а `metadata["publication_allowed"]` разрешает продолжение только
для `PASS` и `PASS_WITH_WARNINGS`.

Для Git-режима состав всегда извлекается из индекса через `git diff --cached`; переданный
`staged_files` сверяется с фактическим индексом. Для файлового экспорта поддерживаются отдельные
файлы, ZIP и TAR. Инспекторы регистрируются списком классов и не требуют изменения Core.

Политика хранится в `Policies/default_v1.json` и защищена SHA-256 checksum. Отчёты создаются
эксклюзивно и переводятся в read-only; журналы не содержат содержимого файлов или секретов.

Запуск тестов:

```powershell
& $env:BUTLER_PYTHON -m unittest discover -s A_04_AGENTS/PublicationGuardianDepartment/Tests -t . -v
```
