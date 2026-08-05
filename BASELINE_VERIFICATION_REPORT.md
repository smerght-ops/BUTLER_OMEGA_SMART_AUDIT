# BASELINE VERIFICATION REPORT

Date: 2026-08-05
Baseline commit: `d77b49c126fb7753c458b0d833697e4f02bff3ad`
Baseline status: Architecture Baseline Stabilization v1.0, Repository Hygiene PASS

## Production components

- Official launcher: `START_BUTLER_OS.ps1`
- Main runtime: `BUTLER_OS.py`
- Core coordinator: `AgentCoreCoordinator`
- Dispatcher: `SmartDispatcherV2`
- Harness: `ButlerHarness`
- Permission boundary: `DepartmentExecutionGateway` and `PermissionEngine`
- Memory owner: `MemoryOrchestratorV2`
- Capability registry: `CapabilityRegistry`
- Department registry: `A_02_MANAGERS/department_registry.py`
- Production Departments: the 18 entries declared by the canonical Department registry

Canonical chain:

`START_BUTLER_OS.ps1 -> BUTLER_OS.py -> AgentCoreCoordinator -> dispatcher_bridge_v2 -> SmartDispatcherV2 -> ButlerHarness -> DepartmentExecutionGateway -> PermissionEngine -> Department`

## Engineering components

The engineering boundary is defined by `PROJECT_SCOPE.yaml` and includes
`A_00_ARCHITECTURE`, `A_00_UTILS`, `A_09_TESTS`, `A_99_TESTS`,
`A_99_TEST_DATA`, `tools`, `docs`, `AUDIT`, `AUDIT_PACKS`, and
`A_10_BUTLER_OS`. The generated registry contains the file-level inventory,
Python top-level symbols, owners, and import dependencies.

## Duplicates found

None confirmed in the active production chain. Similar or superseded
implementations are already isolated and classified as LEGACY, DEVELOPMENT,
DIAGNOSTIC, UNUSED, or ACTIVE_SUPPORT by the existing architecture sources.

## Legacy components

- `A_00_LEGACY_ARCHIVE/production_cleanup_tz4/launchers/*`
- `A_00_LEGACY_ARCHIVE/production_cleanup_tz4/orchestration/*`
- `A_07_MEMORY/memory_orchestrator.py`
- `A_07_MEMORY/memory_facade.py`
- `A_04_AGENTS/professor.py`
- `A_99_TESTS`

The complete file-level list is recorded in `registry_baseline.json`. No legacy
component was removed or modified during Phase 0.

## Decisions

- `AgentCoreCoordinator` -> KEEP: sole active production core coordinator.
- `SmartDispatcherV2` -> KEEP: sole active production dispatcher.
- `MemoryOrchestratorV2` -> KEEP: sole production memory coordinator.
- `DepartmentExecutionGateway` -> KEEP: canonical execution and permission boundary.
- `CapabilityRegistry` -> KEEP: canonical capability registry used by the coordinator.
- `SmartDispatcher` -> KEEP as ACTIVE_SUPPORT: canonical chat-provider lifecycle.
- Isolated launchers and superseded memory/orchestration modules -> RETIRE CANDIDATE: deletion deferred to a separate approved task.

Registry saved: `registry_baseline.json`

## Automated verification

- Registry JSON validation: PASS.
- Canonical pytest profile: PASS (`56 passed`).
- Engineering Review Full: PASS.
- Passing Engineering Review sections: Python, Imports, Encoding, Scope,
  Manifest, Registration, Gateway, Permission, Dispatcher, Runtime,
  Architecture, RKD Boundary, RKD Lifecycle, Duplicates, Tests.
- Repository baseline whitespace scope: active paths and official root entry
  files declared by `system_manifest.json`. Historical backup, rollback,
  snapshot, and hygiene-manifest stores are excluded from blocking the active
  baseline result; their files remain intact.
- Canonical pytest profile after scope correction: PASS (`57 passed`).
- Ordinary working-tree `git diff --check`: PASS.

Verification PASS/FAIL: **PASS**

Phase 0 is complete. The repository is cleared to continue from Phase 1 under
the Master Engineering Specification and its phase-specific engineering task.

