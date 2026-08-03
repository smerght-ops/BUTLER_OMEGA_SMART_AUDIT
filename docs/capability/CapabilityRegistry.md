============================================================
BUTLER CAPABILITY REGISTRY
============================================================

## Project Memory
**Status**: LOCKED

**Components**:
- MemoryFacadeV2
- MemoryOrchestrator
- SemanticMemory
- MemoryReplay
- ProjectHistory

**Evidence files**:
- 1169
- 1155
- 1188
- 1158
- 1160

**Artifacts**:
- A_07_MEMORY

**Dependencies**:
- ExecutionRegistry


## Smart Routing
**Status**: LOCKED

**Components**:
- SmartDispatcherV2
- DispatcherBridge
- RouterIntegration
- ProviderManager

**Evidence files**:
- 324
- 1285
- 1287
- 429
- 367
- 315
- 338
- 467
- 468
- 123

**Artifacts**:
- A_02_MANAGERS
- A_03_ORCHESTRATION

**Dependencies**:
- ExecutionRegistry


## Image Generation
**Status**: LOCKED

**Components**:
- ImageDepartment
- VisionDepartment
- VisionEngine
- ComfyUIBridge

**Evidence files**:
- 625
- 499
- 371
- 391
- 1389

**Artifacts**:
- A_04_AGENTS/ImageDepartment
- A_04_AGENTS/VisionDepartment



## Task Execution
**Status**: LOCKED

**Components**:
- TaskRunner
- ExecutionPolicy
- RecipeExecutor
- ExecutorFactory

**Evidence files**:
- 352
- 1082
- 348
- 346

**Artifacts**:
- A_02_MANAGERS/TaskRunner



## Semantic Search
**Status**: PARTIAL

**Components**:
- CatalogManager
- ReferenceResolver
- SemanticReasoningEngine

**Evidence files**:
- 1192
- 1201
- 364
- 285

**Artifacts**:
- A_07_MEMORY/semantic_memory.py


**Missing components**:
- SearchEngine

## DO NOT BUILD AGAIN
The following capabilities are LOCKED and should not be rebuilt:
- Project Memory
- Smart Routing
- Image Generation
- Task Execution
