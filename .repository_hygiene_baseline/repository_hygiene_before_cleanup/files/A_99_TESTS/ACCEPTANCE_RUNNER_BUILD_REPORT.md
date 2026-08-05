# Acceptance Runner Build Report

Date: 2026-07-12  
Final status: **ACCEPTANCE RUNNER CREATED**

## 1. Created Files

- `A_99_TESTS/full_acceptance.py`
- `A_99_TESTS/acceptance_config.json`
- `A_99_TESTS/fixtures/README.md`
- `A_99_TESTS/fixtures/vision_test_image.png`
- `A_99_TESTS/fixtures/document_test.txt`
- `A_99_TESTS/fixtures/unsupported.bin`
- `A_99_TESTS/fixtures/archive_test.zip`
- `A_99_TESTS/reports/acceptance_report_*.json`
- `A_99_TESTS/reports/acceptance_report_*.md`
- `A_99_TESTS/reports/latest_acceptance_report.json`
- `A_99_TESTS/reports/latest_acceptance_report.md`
- `A_99_TESTS/README.md`
- `START_FAST_ACCEPTANCE.bat`
- `START_FULL_ACCEPTANCE.bat`

## 2. Modified Existing Files

None. Runtime, Dispatcher, ButlerHarness, Result Contract, Memory and all Department files were not changed.

## 3. Official Runtime Entry Used

`A_03_ORCHESTRATION.dispatcher_bridge_v2.dispatch -> SmartDispatcherV2 -> ButlerHarness -> Department -> Result Contract`.

The BAT launchers resolve the same `python` command used by `START_BUTLER_OS.ps1`; the observed executable was `C:\Users\KOS\AppData\Local\Python\bin\python.exe`.

## 4. FAST Scenario Results

Final FAST baseline (`20260712_104222`):

- PASS: 10
- FAIL: 1
- SKIP: 0
- Exit code: 1
- Cleanup: PASS

## 5. FULL Scenario Results

Final FULL baseline (`20260712_104559`):

- PASS: 17
- FAIL: 3
- SKIP: 2
- Exit code: 1
- Cleanup: PASS

## 6. Baseline PASS

FAST confirmed compile, Runtime import, Department registration, Memory profile/preference, Search and route checks for IMAGE, TEXT, CODING, SEARCH and VISION.

FULL confirmed Memory read/write/persistence, Coding, Search, Vision positive and negative cases, Documents positive and negative cases, Archive, all four IMAGE context steps, including `под водопадом` remaining in IMAGE.

## 7. Baseline FAIL

- FAST `ROUTE_HOME`: the standalone command `включи свет` did not select HOME.
- FULL `CHAT_POEM`: official CHAT fallback returned an incomplete Result Contract without model text.
- FULL `CHAT_SELF_INFO`: official CHAT fallback returned an incomplete Result Contract without model text.
- FULL `OPEN_FIRST`: Search returned a catalog path that does not exist on disk; OpenDocument correctly returned `FILE_NOT_FOUND`.

## 8. Baseline SKIP

- AUDIO: registered minimal acknowledgement, no real provider.
- VIDEO: registered minimal acknowledgement, no real provider.

## 9. Storage Backup And Restore

Before every run the Runner snapshots configured profile, memory, session, semantic index, execution registry and search-session state. Restoration runs in `finally`. Final FAST and FULL cleanup both passed. No `ACCEPTANCE_MEMORY_*` marker and no temporary backup directory remained.

## 10. Exit Code Verification

Both BAT files preserve the Python process exit code using delayed expansion. FAST and FULL each returned `1` for their factual baseline FAIL results. Exit code `3` is reserved for failed storage restoration and `2` for Runner/Runtime initialization failure.

## 11. Report Files

- FAST: `A_99_TESTS/reports/acceptance_report_20260712_104222.json` and `.md`.
- FULL: `A_99_TESTS/reports/acceptance_report_20260712_104559.json` and `.md`.
- Latest FULL: `A_99_TESTS/reports/latest_acceptance_report.json` and `.md`.

Reports contain bounded previews and sanitized metadata; full personal session/profile content is not stored.

## 12. Known Current Regressions

`HOME_STANDALONE_ROUTE_MISMATCH`, `CHAT_EXECUTION_MISSING` for two CHAT scenarios, and stale Search catalog path causing `OPEN_FIRST -> FILE_NOT_FOUND`.

The expected IMAGE context defect was not reproduced: all four IMAGE steps passed, including waterfall continuation.

## 13. Project Operational Status

Operational. Official bridge, Dispatcher, ButlerHarness, providers and tested Department remained available. Functional regressions were recorded and not repaired, as required.

## 14. Final Status

**ACCEPTANCE RUNNER CREATED**

The Runner launches from one-click BAT files, classifies PASS/FAIL/SKIP, writes JSON and Markdown reports, returns the required nonzero baseline exit code and restores test-modified storage.
