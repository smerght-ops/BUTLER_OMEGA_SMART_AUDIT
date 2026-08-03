# BUTLER CAPABILITY REGISTRY V2

## Что уже есть и что нельзя строить повторно

## ✅ Память проекта
- id: `PROJECT_MEMORY`
- status: `LOCKED`
- evidence: `7` / `7`
- do_not_build_again: `True`
- доказательства:
  - `MemoryFacadeV2`
  - `MemoryOrchestrator`
  - `SemanticMemory`
  - `MemoryReplay`
  - `ProjectHistory`
  - `USER_MEMORY.md`
  - `session_history.jsonl`

## ✅ Маршрутизация запросов
- id: `SMART_ROUTING`
- status: `LOCKED`
- evidence: `6` / `6`
- do_not_build_again: `True`
- доказательства:
  - `SmartDispatcherV2`
  - `DispatcherBridge`
  - `dispatcher_bridge_v2.py`
  - `RouterIntegration`
  - `ProviderManager`
  - `DepartmentRegistry`

## ✅ Генерация изображений
- id: `IMAGE_GENERATION`
- status: `LOCKED`
- evidence: `6` / `6`
- do_not_build_again: `True`
- доказательства:
  - `ImageDepartment`
  - `VisionDepartment`
  - `VisionEngine`
  - `ComfyUIBridge`
  - `generate_image`
  - `check_comfyui`

## ✅ Текстовый и кодовый департаменты
- id: `TEXT_AND_CODING`
- status: `LOCKED`
- evidence: `5` / `5`
- do_not_build_again: `True`
- доказательства:
  - `TextDepartment`
  - `CodingDepartment`
  - `CodeHandler`
  - `DeepSeek`
  - `Codestral`

## ✅ Поиск, каталог и resolver
- id: `SEARCH_AND_REFERENCE`
- status: `LOCKED`
- evidence: `6` / `6`
- do_not_build_again: `True`
- доказательства:
  - `CatalogManager`
  - `ReferenceResolver`
  - `HybridResolver`
  - `SearchDepartment`
  - `SemanticSearchEngine`
  - `rebuild_search_index`

## ✅ Исполнение задач и рецептов
- id: `EXECUTION_ENGINE`
- status: `LOCKED`
- evidence: `7` / `7`
- do_not_build_again: `True`
- доказательства:
  - `TaskRunner`
  - `RecipeExecutor`
  - `RecipeBuilder`
  - `RecipeValidator`
  - `ExecutionPolicy`
  - `ExecutorFactory`
  - `ExecutionRegistry`

## ✅ Паспорт и состояние проекта
- id: `PROJECT_PASSPORT`
- status: `LOCKED`
- evidence: `5` / `5`
- do_not_build_again: `True`
- доказательства:
  - `project_passport.json`
  - `ProjectPassportLoader`
  - `PassportCommandHandler`
  - `passport_summary`
  - `get_passport_string`

## ✅ Стражи и защитные контуры
- id: `GUARDIANS`
- status: `LOCKED`
- evidence: `6` / `6`
- do_not_build_again: `True`
- доказательства:
  - `A_09_GUARDIANS`
  - `genie_guardian.ps1`
  - `FrozenCoreGuard`
  - `IntegrationTestGuard`
  - `memory_guardian`
  - `run_guardian`

## ✅ Инспекторский аудит проекта
- id: `AUDIT_PIPELINE`
- status: `LOCKED`
- evidence: `7` / `7`
- do_not_build_again: `True`
- доказательства:
  - `Inspector0_PhysicalMap.json`
  - `Inspector1_EntityMap.json`
  - `Inspector2_ImportMap.json`
  - `Inspector3_RegistrationAST.json`
  - `Inspector4_CallGraph.json`
  - `LinkMap.json`
  - `DependencyModel.json`

## ✅ Butler OS / рабочий контур
- id: `BUTLER_OS`
- status: `LOCKED`
- evidence: `4` / `4`
- do_not_build_again: `True`
- доказательства:
  - `A_10_BUTLER_OS`
  - `ButlerOSAdapter`
  - `ButlerInteractiveChat`
  - `ButlerSystem`

## ✅ Агентные департаменты
- id: `AGENT_DEPARTMENTS`
- status: `LOCKED`
- evidence: `7` / `7`
- do_not_build_again: `True`
- доказательства:
  - `BaseDepartment`
  - `ArchiveDepartment`
  - `AudioDepartment`
  - `DocumentsDepartment`
  - `MemoryDepartment`
  - `VideoDepartment`
  - `ProjectDocumentationDepartment`

## ✅ Архитектурное управление
- id: `ARCHITECTURE_GOVERNANCE`
- status: `LOCKED`
- evidence: `6` / `6`
- do_not_build_again: `True`
- доказательства:
  - `ARCHITECTURE_LOCK.json`
  - `architecture_manifest.json`
  - `RuntimeCapabilityRegistry`
  - `GoalsRegistryDiscoveryAgent`
  - `RegistryValidator`
  - `ManifestLoader`

## DO NOT BUILD AGAIN

- Память проекта / `PROJECT_MEMORY`
- Маршрутизация запросов / `SMART_ROUTING`
- Генерация изображений / `IMAGE_GENERATION`
- Текстовый и кодовый департаменты / `TEXT_AND_CODING`
- Поиск, каталог и resolver / `SEARCH_AND_REFERENCE`
- Исполнение задач и рецептов / `EXECUTION_ENGINE`
- Паспорт и состояние проекта / `PROJECT_PASSPORT`
- Стражи и защитные контуры / `GUARDIANS`
- Инспекторский аудит проекта / `AUDIT_PIPELINE`
- Butler OS / рабочий контур / `BUTLER_OS`
- Агентные департаменты / `AGENT_DEPARTMENTS`
- Архитектурное управление / `ARCHITECTURE_GOVERNANCE`