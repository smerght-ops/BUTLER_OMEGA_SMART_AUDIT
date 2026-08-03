# Butler Capability Audit v2

Generated UTC: `2026-07-07T22:49:53.432108Z`

## 1. Existing audit artifacts

- ✅ `Inspector0_PhysicalMap.json` — schema `physical_map`, generator `Inspector0_PhysicalMap`
- ✅ `Inspector1_EntityMap.json` — schema `entity_map`, generator `Inspector1_EntityMap`
- ✅ `Inspector2_ImportMap.json` — schema `import_map`, generator `Inspector2_ImportMap`
- ✅ `Inspector3_RegistrationAST.json` — schema `registration_ast`, generator `Inspector3_RegistrationAST`
- ✅ `Inspector4_CallGraph.json` — schema `call_graph`, generator `Inspector4_CallGraph`
- ✅ `LinkMap.json` — schema `link_map`, generator `LinkMapBuilder`
- ✅ `DependencyModel.json` — schema `dependency_model`, generator `DependencyModelBuilder`

## 2. Implemented capabilities / do not rebuild

- ✅ **Создание физической карты проекта** — `LOCKED`
  - evidence: `Inspector0_PhysicalMap.json` / `physical_map` / `Inspector0_PhysicalMap`
  - evidence: `Inspector1_EntityMap.json` / `entity_map` / `Inspector1_EntityMap`
  - evidence: `Inspector2_ImportMap.json` / `import_map` / `Inspector2_ImportMap`
  - evidence: `Inspector3_RegistrationAST.json` / `registration_ast` / `Inspector3_RegistrationAST`
  - evidence: `Inspector4_CallGraph.json` / `call_graph` / `Inspector4_CallGraph`
  - evidence: `LinkMap.json` / `link_map` / `LinkMapBuilder`
- ✅ **Извлечение сущностей Python-кода** — `LOCKED`
  - evidence: `Inspector1_EntityMap.json` / `entity_map` / `Inspector1_EntityMap`
  - evidence: `LinkMap.json` / `link_map` / `LinkMapBuilder`
- ✅ **Построение карты импортов** — `LOCKED`
  - evidence: `Inspector2_ImportMap.json` / `import_map` / `Inspector2_ImportMap`
  - evidence: `LinkMap.json` / `link_map` / `LinkMapBuilder`
- ✅ **Поиск регистраций компонентов через AST** — `LOCKED`
  - evidence: `Inspector3_RegistrationAST.json` / `registration_ast` / `Inspector3_RegistrationAST`
  - evidence: `LinkMap.json` / `link_map` / `LinkMapBuilder`
- ✅ **Сбор сырого графа вызовов** — `LOCKED`
  - evidence: `Inspector4_CallGraph.json` / `call_graph` / `Inspector4_CallGraph`
  - evidence: `LinkMap.json` / `link_map` / `LinkMapBuilder`
- ✅ **Нормализация связей между артефактами** — `LOCKED`
  - evidence: `LinkMap.json` / `link_map` / `LinkMapBuilder`
- ✅ **Построение независимой модели зависимостей** — `LOCKED`
  - evidence: `DependencyModel.json` / `dependency_model` / `DependencyModelBuilder`

## 3. Component roles

- **agent**: `24`
- **auditor**: `14`
- **builder**: `6`
- **department**: `18`
- **dispatcher**: `28`
- **guardian**: `11`
- **manager**: `23`
- **memory**: `41`
- **registry**: `21`
- **unknown**: `441`

## 4. Registrations

- total registrations: `20`
- file `297`: `register` line `41` args `['<expr>']`
- file `320`: `register` line `53` args `['<expr>']`
- file `346`: `register` line `53` args `['PythonExecutionAdapter']`
- file `346`: `register` line `54` args `['PowerShellExecutionAdapter']`
- file `365`: `Dispatcher` line `33` args `[]`
- file `517`: `register` line `22` args `['obj']`
- file `517`: `register` line `41` args `['obj1']`
- file `517`: `register` line `42` args `['obj2']`
- file `522`: `register` line `43` args `['obj']`
- file `526`: `register` line `50` args `['obj']`
- file `529`: `register` line `38` args `['obj']`
- file `572`: `register` line `22` args `['obj']`
- file `572`: `register` line `41` args `['obj1']`
- file `572`: `register` line `42` args `['obj2']`
- file `577`: `register` line `43` args `['obj']`
- file `581`: `register` line `50` args `['obj']`
- file `584`: `register` line `38` args `['obj']`
- file `1118`: `register` line `102` args `['task_id', 'phase']`
- file `1342`: `register` line `5` args `["'IMAGE'", '<expr>']`
- file `1351`: `register` line `5` args `["'dragon.png'", "'fantasy_workflow.json'"]`

## 5. Duplicates

- duplicate class names: `62`
- duplicate function names: `36`

## 6. Dependency summary

- nodes: `1499`
- edges: `11976`
- relations: `{'import': 1528, 'call': 10428, 'registration': 20}`
- root nodes: `457`
- leaf nodes: `1042`
- orphan nodes: `0`

## 7. Final lock statement

✅ Measurement pipeline exists and must not be rebuilt without intentional schema/version change.