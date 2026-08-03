# HARNESS_SPEC.md — Спецификация контура безопасности V3

## 1. Архитектурный принцип: Декларативное намерение
- **Главный инвариант:** `Harness never validates executable code first. Harness validates change requests first.`
- Любая модификация системы начинается строго с генерации структурированного JSON-файла заявки в каталоге `A_00_ARCHITECTURE\CHANGE_REQUESTS\`.

## 2. Разделение обязанностей (Separation of Responsibilities)
- **Инвариант роли:** `Harness validates. Patch Executor modifies.`
- **Жесткий запрет:** `Harness must never rewrite source files during validation.`
- Валидатор является контролирующим органом, а не редактором.

## 3. Спецификация Change Request (Входной контракт)

## 4. Модульная структура BUTLER_HARNESS_V3

## 5. Спецификация выходов и журналирования
