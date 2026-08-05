# Butler LOCKED Capabilities

## НЕ СТРОИТЬ ПОВТОРНО

- ✅ **Создание физической карты проекта**
  - artifact: `Inspector0_PhysicalMap.json`
  - schema: `physical_map`
  - generator: `Inspector0_PhysicalMap`
  - status: `LOCKED`
- ✅ **Извлечение сущностей Python-кода**
  - artifact: `Inspector1_EntityMap.json`
  - schema: `entity_map`
  - generator: `Inspector1_EntityMap`
  - status: `LOCKED`
- ✅ **Построение карты импортов**
  - artifact: `Inspector2_ImportMap.json`
  - schema: `import_map`
  - generator: `Inspector2_ImportMap`
  - status: `LOCKED`
- ✅ **Поиск регистраций компонентов через AST**
  - artifact: `Inspector3_RegistrationAST.json`
  - schema: `registration_ast`
  - generator: `Inspector3_RegistrationAST`
  - status: `LOCKED`
- ✅ **Сбор сырого графа вызовов**
  - artifact: `Inspector4_CallGraph.json`
  - schema: `call_graph`
  - generator: `Inspector4_CallGraph`
  - status: `LOCKED`
- ✅ **Нормализация связей между артефактами**
  - artifact: `LinkMap.json`
  - schema: `link_map`
  - generator: `LinkMapBuilder`
  - status: `LOCKED`
- ✅ **Построение независимой модели зависимостей**
  - artifact: `DependencyModel.json`
  - schema: `dependency_model`
  - generator: `DependencyModelBuilder`
  - status: `LOCKED`

## Итог

- LOCKED capabilities: `7` / `7`
- Правило: если capability LOCKED — новый ИИ не имеет права предлагать строить её повторно без смены schema/version.