# Диагностика официального запуска Butler

Дата исследования: 2026-07-16 13:16–13:23 (UTC+03:00)
Режим: READ ONLY
Рабочий каталог: `C:\Users\KOS\Desktop\Butler_Agent\BUTLER_OMEGA_SMART`

## 1. Environment

- PowerShell: `C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe`
- pwsh: не найден
- cmd.exe: `C:\Windows\system32\cmd.exe`
- `Get-Command python`: `NOT FOUND`
- `python -c "import sys; print(sys.executable)"`: не выполнялся, поскольку команда `python` не разрешилась в исходной среде Codex
- Python, фактически найденный дочерним PowerShell официального запуска: `C:\Users\KOS\AppData\Local\Python\bin\python.exe`

Исходный PATH:

```text
C:\Users\KOS\.codex\tmp\arg0\codex-arg0qHesnJ;C:\Users\KOS\.cache\codex-runtimes\codex-primary-runtime\dependencies\bin\override;C:\Windows\system32;C:\Windows;C:\Windows\System32\Wbem;C:\Windows\System32\WindowsPowerShell\v1.0\;C:\Windows\System32\OpenSSH\;C:\Program Files\NVIDIA Corporation\NVIDIA App\NvDLISR;C:\Program Files (x86)\NVIDIA Corporation\PhysX\Common;C:\Program Files\Git\cmd;C:\Program Files (x86)\Microsoft SQL Server\160\Tools\Binn\;C:\Program Files\Microsoft SQL Server\160\Tools\Binn\;C:\Program Files\Microsoft SQL Server\Client SDK\ODBC\170\Tools\Binn\;C:\Program Files\Microsoft SQL Server\160\DTS\Binn\;C:\Program Files (x86)\Windows Kits\8.1\Windows Performance Toolkit\;C:\Users\KOS\AppData\Local\Python\bin;C:\Users\KOS\AppData\Local\Programs\Microsoft VS Code\bin;C:\Users\KOS\AppData\Local\Programs\Ollama;C:\Users\KOS\.lmstudio\bin;C:\Users\KOS\AppData\Local\Programs\cursor\resources\app\bin;D:\Python312;C:\Users\KOS\.cache\codex-runtimes\codex-primary-runtime\dependencies\bin\fallback;C:\Users\KOS\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\git\cmd;C:\Users\KOS\AppData\Local\OpenAI\Codex\bin\ada252862d154cdd;C:\Program Files\WindowsApps\OpenAI.Codex_26.707.12708.0_x64__2p2nqsd0c76g0\app\resources
```

Стартовые файлы и исходные SHA-256:

| Файл | Наличие | SHA-256 |
|---|---:|---|
| `START_BUTLER_OS.bat` | да | `B7BFA9E6E12CD183F1BCABA47E15F3B2EF62119E3E5E4FE633242E3DC7DE763B` |
| `START_BUTLER_OS.ps1` | да | `19830434057098141BBDF1DAF4290244E56BF96A0F2E1A10E2663B4E932C774D` |
| `BUTLER_OS.py` | да | `BFD856CF69C97999D1519AF0DAE8198B555E16142FB60771256EADA6043CC113` |

Процессы до запуска (только запрошенные имена):

```text
ollama: 30532
powershell: 27576, 28148, 30420, 32476
python: 3096, 15536, 27900, 29924, 30432
pythonw: отсутствует
pwsh: отсутствует
```

## 2. Exact official command

```text
C:\Windows\System32\cmd.exe /d /c "C:\Users\KOS\Desktop\Butler_Agent\BUTLER_OMEGA_SMART\START_BUTLER_OS.bat"
```

- Рабочий каталог: `C:\Users\KOS\Desktop\Butler_Agent\BUTLER_OMEGA_SMART`
- PID cmd.exe: `30328`
- Начало: `2026-07-16T13:22:18.6949854+03:00`
- Окончание: `2026-07-16T13:22:23.6833557+03:00`
- Тайм-аут: нет
- Код завершения cmd.exe: `0`
- stdin одного экземпляра: `кто ты`, `exit`, пустая строка

## 3. Full official log

stdout и stderr были полностью перенаправлены в отдельные потоки. Ниже приведено их полное содержимое без пересказа.

### stdout

```text
=====================================================
      BUTLER OMEGA SMART - GREEN START BUTTON
=====================================================
[ROOT] C:\Users\KOS\Desktop\Butler_Agent\BUTLER_OMEGA_SMART

[..] 1/6 STATUS CENTER
==================================================
BUTLER STATUS CENTER READONLY V2.5 [FINAL]
==================================================

Current Path:
C:\Users\KOS\Desktop\Butler_Agent\BUTLER_OMEGA_SMART

[OK] SMART contour detected.

------------- PASSPORT -------------
Name           : BUTLER_OMEGA_SMART
Version        : 1.2_DK01
Passport Stage : 4.26_SEMANTIC_SEARCH_ENGINE_V1
Roadmap Next   : SEMANTIC_REASONING_ENGINE

---------------- LEDGER ----------------
Runtime Stage  : 4.26_SEMANTIC_SEARCH_ENGINE_V1
Last Stable    : STABLE_BUTLER_V3_1_MEMORY_READY

----------- RECENT CHANGE REQUESTS -----------
  • PENDING ↳ AUTOLOOP_PHASE_2_TASK_D_EXEC [LOCK_ID=d286b5242e6d]
  • PENDING ↳ TEST_RUNTIME_CR [LOCK_ID=db17103a16c5]
  • PENDING ↳ AUTOLOOP_INTEGRATION_FINAL_PROOF [LOCK_ID=26876559e4a0]

----------- FREEZE STATUS -----------
Frozen Modules:
  ↳ A_03_ORCHESTRATION\chat_router.py
  ↳ A_01_CORE
Active Modules:
  ↳ A_03_ORCHESTRATION\butler_os_adapter.py
  ↳ A_07_MEMORY\profile_manager.py
  ↳ A_07_CONFIG\project_passport.json

------------- GOALS REGISTRY ------------
Active Goal    : BUTLER_RECIPE_LIBRARY
Current Phase  : ROADMAP_6_PHASE_4_RECIPES

----------- EXECUTION REGISTRY ----------
Verified Tasks : 10
Last Update    : 2026-06-22T12:15:16.662340

-------------- OBSERVATIONS -------------
Last Harness Event: HARNESS_V3_SUCCESS
Event Time        : 2026-07-16T11:40:39.380637

--------------- MEMORY MAP ---------------
MemoryFacadeV2 (Project State Core):
  • L1 Passport  : IMPLEMENTED
  • L2 Session   : IMPLEMENTED
  • L3 Tasks     : IMPLEMENTED
  • L4 History   : IMPLEMENTED
  • L5 Semantic  : IMPLEMENTED
  • L6 Strategy  : IMPLEMENTED
MemoryOrchestratorV2 (LLM Prompt Layer):
  • Semantic Layer  : PRESENT
  • Attention Layer : PRESENT
  • Replay Layer    : PRESENT
  • Budget Layer    : PRESENT

------------- FILE HEALTH ----------------
  • PROJECT_LEDGER.txt....... OK (3875 B)
  • OBSERVATIONS.jsonl....... OK (21624588 B)
  • goals_registry.json...... OK (488 B)
  • project_passport.json.... OK (2649 B)
  • execution_registry.json.. OK (1380 B)

----------- REAL WORKING CONTOURS -----------
Worker Pipeline      : PROVEN (QueueManager -> Worker -> ButlerHarness)
Dispatcher Pipeline  : PROVEN (SmartDispatcherV2 -> 8 Departments -> ButlerHarness)
Runtime Planner      : PROVEN (agent_runtime -> Planner -> CR -> Registry)
Runtime <-> Harness  : PROVEN (via CR_RUNTIME_AUTOMATION)

------------- EXECUTION PROOF MAP -------------
  • single_task_execution          : PROVEN
  • multi_task_execution           : PROVEN
  • phase_transition_evolution     : PROVEN
  • change_request_ledger          : PROVEN
  • execution_registry_tracking    : PROVEN
  • image_pipeline_routing         : PROVEN
  • text_roles_dispatch            : PROVEN
  • runtime_harness_harness_commit : PROVEN
  • runtime_harness_integration    : PROVEN_VIA_SERVICE_CONTRACT
  • l2_session_memory              : PROVEN_IMPLEMENTED
  • l5_semantic_memory             : PROVEN_IMPLEMENTED
  • draft_commit_engine            : ARCHITECTURALLY_REJECTED_CR_MODEL_SUFFICIENT
  • anti_loop_budget               : PROVEN_VIA_EXECUTION_MEMORY_V2
  • fallback_controller            : PROVEN_DYNAMIC_FAILOVER_ROUTER
  • search_department_routing      : PROVEN
  • catalog_search_bridge          : PROVEN
  • catalog_db_retrieval           : PROVEN_ID_171_BLUE_WHALE
  • 4.24_write_api                 : OK
  • 4.24_active_sync_proof         : RUNNING_AUTOMATICALLY
  • search_case_normalization      : PROVEN
==================================================
READONLY STATUS CENTER COMPLETE
==================================================
[..] 2/6 PASSPORT + MEMORY GUARDIAN
[OK] Passport detected

==============================================
  BUTLER OMEGA HARDCORE GUARDIAN v1.2.0
==============================================

=== SAFE REASONS ===
 - SHA256 A_02_MANAGERS/catalog_manager.py отличается от PROJECT_STATE.
====================

=== SELF-TEST COMPLETED: SAFE ===

[OK] Memory Guardian passed
[..] 3/6 OLLAMA
[OK] Ollama ONLINE on port 11434
[..] 4/6 COMFYUI
[OK] ComfyUI ONLINE on port 8188
[..] 5/6 SYSTEM GUARDIAN
==================================
   BUTLER OMEGA SYSTEM GUARDIAN
              v1.0
==================================

[CORE FILES]
  ✓ A_01_CORE/orchestrator.py (На месте)
  ✓ A_03_ORCHESTRATION/worker.py (На месте)
  ✓ A_02_MANAGERS/queue_manager.py (На месте)
  ✓ A_04_AGENTS/professor.py (На месте)
  ✓ system_manifest.json загружен

[FILESYSTEM]
  ✓ Workspace каталог подтвержден
  ✓ Storage каталог подтвержден
  ✓ Logs каталог подтвержден

[DATABASE INTERNALS]
  ✓ catalog.db active (Файлов в индексе: 26)

[OLLAMA & COGNITIVE MODELS]
  ✓ Локальный server Ollama доступен
  ✓ [Анализ] Модель готова: qwen35-ru:latest
  ✓ [Зрение] Модель готова: qwen2.5-vl:latest

==================================
QUEUE HEALTH
----------------------------------
  queued       : 1
  processing   : 0
  completed    : 21
  failed       : 4

==================================
HEALTH SCORE :  100 / 100
STATUS       :  GREEN
==================================
[..] 6/6 START BUTLER OS
=====================================================
              STARTING BUTLER OS
=====================================================
[..] Starting RunnerLoop

======================================================================
 BUTLER OMEGA OS v1.1 — WORK TERMINAL
======================================================================
[OK] Ядро загружено.
[OK] SmartDispatcherV2 подключен.
[OK] Департаменты доступны.
Введите exit / q / выход для завершения.
======================================================================

[KOS] >
[OK] Butler session closed
Press any key to continue . . .
```

### stderr

```text
Traceback (most recent call last):
  File "C:\Users\KOS\Desktop\Butler_Agent\BUTLER_OMEGA_SMART\BUTLER_OS.py", line 97, in <module>
    main()
  File "C:\Users\KOS\Desktop\Butler_Agent\BUTLER_OMEGA_SMART\BUTLER_OS.py", line 26, in main
    query = input("\n[KOS] > ").strip()
            ^^^^^^^^^^^^^^^^^^^
  File "<frozen codecs>", line 322, in decode
UnicodeDecodeError: 'utf-8' codec can't decode byte 0xaa in position 0: invalid start byte
```

## 4. Process result

Доказанно наблюдавшиеся потомки официального PID 30328:

| PID | Parent PID | Процесс | Командная строка |
|---:|---:|---|---|
| 32236 | 30328 | powershell.exe | `powershell -NoProfile -ExecutionPolicy Bypass -File ".\START_BUTLER_OS.ps1"` |
| 32796 | 32236 | powershell.exe | `powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\STATUS_CENTER_READONLY.ps1` |
| 4760 | 32236 | python.exe | `python.exe -m A_01_CORE.memory_guardian --self-test` |
| 31512 | 32236 | python.exe | `python.exe .\A_01_CORE\system_guardian.py` |
| 33224 | 32236 | python.exe | `python.exe -m A_02_MANAGERS.TaskRunner.runner_loop` |
| 30168 | 32236 | python.exe | `python.exe .\BUTLER_OS.py` |
| 17596 | 30168 | cmd.exe | командная строка недоступна |
| 32500 | 33224 | conhost.exe | `conhost.exe 0x4` |

После окончания cmd.exe оставался RunnerLoop PID 33224 и его conhost PID 32500. PID 33224 был завершён принудительно как доказанно созданный данным запуском; conhost завершился вместе с родителем. Повторная проверка не обнаружила ни одного процесса из диагностического дерева.

## 5. Control command

Приглашение `[KOS] >` появилось, однако команда `кто ты` не была обработана. В stdout отсутствует строка `[BUTLER | ...]`; stderr фиксирует исключение непосредственно в `input()` при декодировании первого байта stdin.

Таким образом, критерий `OFFICIAL START CONFIRMED` не выполнен.

## 6. Comparison

После завершения официальной попытки выполнен разрешённый сравнительный запуск:

```text
C:\Users\KOS\AppData\Local\Python\bin\python.exe BUTLER_OS.py
```

- Рабочий каталог: `C:\Users\KOS\Desktop\Butler_Agent\BUTLER_OMEGA_SMART`
- Python: `C:\Users\KOS\AppData\Local\Python\bin\python.exe`
- PID: `8740`
- Начало: `2026-07-16T13:23:11.4063014+03:00`
- Окончание: `2026-07-16T13:23:16.3327922+03:00`
- Код завершения: `0`
- Тайм-аут: нет
- stderr: пуст
- `кто ты`: обработано тем же экземпляром (`[BUTLER | CHAT | model=qwen35-ru:latest | 4712ms]`)
- `exit`: обработано, Butler завершился штатно

Полный сравнительный stdout (символы кириллицы отображены заменителями из-за несовпадения кодировки захвата, структура строк сохранена):

```text
======================================================================
 BUTLER OMEGA OS v1.1 � WORK TERMINAL
======================================================================
[OK] ���� ���������.
[OK] SmartDispatcherV2 ���������.
[OK] ������������ ��������.
������� exit / q / ����� ��� ����������.
======================================================================

[KOS] >
[BUTLER | CHAT | model=qwen35-ru:latest | 4712ms]

� ��� �� �������. ����������, �������� ��� ������ �� ������� �����.

[KOS] >
[OK] Butler OS ����������.
```

Сравнительный результат отличается тем, что прямой процесс обработал обе строки stdin, а официальный процесс завершил `BUTLER_OS.py` с приведённым выше `UnicodeDecodeError` при чтении первой строки.

## 7. Integrity

SHA-256 после исследования:

| Файл | SHA-256 после | Совпадает с исходным |
|---|---|---:|
| `START_BUTLER_OS.bat` | `B7BFA9E6E12CD183F1BCABA47E15F3B2EF62119E3E5E4FE633242E3DC7DE763B` | да |
| `START_BUTLER_OS.ps1` | `19830434057098141BBDF1DAF4290244E56BF96A0F2E1A10E2663B4E932C774D` | да |
| `BUTLER_OS.py` | `BFD856CF69C97999D1519AF0DAE8198B555E16142FB60771256EADA6043CC113` | да |

`git status` показывает перечисленные production-файлы как уже существующие untracked-файлы и не предоставляет исторической базы для сравнения их содержимого. Диагностика не выполняла патчей или команд записи production-кода. Контрольные SHA-256 трёх стартовых файлов идентичны до и после.

```text
PRODUCTION FILE CHANGES: 0
```

Единственный созданный файл — настоящий диагностический отчёт в `A_09_TESTS`, разрешённый ТЗ.

## 8. Conclusion

**OFFICIAL START FAILED**

Фактическая точка ошибки подтверждена полным stderr:

```text
UnicodeDecodeError: 'utf-8' codec can't decode byte 0xaa in position 0: invalid start byte
```

Рабочий экран был загружен официальной цепочкой BAT → PowerShell → `BUTLER_OS.py`, но обязательная контрольная команда не была обработана этим экземпляром.
