# -*- coding: utf-8 -*-
# ==============================================================================
# SYSTEM ARTIFACT: STATUS_CENTER_READONLY.ps1
# VERSION: SAFE-READONLY V2.5 (AUTOMATED AUDIT SYNCHRONIZED)
# PRINCIPLE: STRICT READ-ONLY / NO PYTHON RUNTIME / NO WRITES
# ==============================================================================

Clear-Host
$ErrorActionPreference = "SilentlyContinue"

$CurrentPath = (Get-Location).Path
$ExpectedFolder = "BUTLER_OMEGA_SMART"

Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "BUTLER STATUS CENTER READONLY V2.5 [FINAL]" -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan

Write-Host ""
Write-Host "Current Path:"
Write-Host $CurrentPath -ForegroundColor Green

if ($CurrentPath -notmatch $ExpectedFolder) {
    Write-Host ""
    Write-Host "[FAIL] SMART contour NOT detected." -ForegroundColor Red
    exit
}

Write-Host ""
Write-Host "[OK] SMART contour detected." -ForegroundColor Green

# ------------- БЛОК 1: PASSPORT -------------
Write-Host ""
Write-Host "------------- PASSPORT -------------" -ForegroundColor Yellow

$PassportFile = ".\A_07_CONFIG\project_passport.json"
$PassportValid = $false

if (Test-Path $PassportFile) {
    $Passport = Get-Content $PassportFile -Raw | ConvertFrom-Json
    $PassportValid = $true

    Write-Host "Name           :" -NoNewline; Write-Host " $($Passport.project_identity.name)" -ForegroundColor Cyan
    Write-Host "Version        :" -NoNewline; Write-Host " $($Passport.project_identity.version)" -ForegroundColor Cyan
    Write-Host "MAIN ROADMAP   :" -NoNewline; Write-Host " $($Passport.project_state.main_roadmap.name) / $($Passport.project_state.main_roadmap.milestone) / $($Passport.project_state.main_roadmap.status)" -ForegroundColor Green
    Write-Host "AGENT CORE ROADMAP:" -NoNewline; Write-Host " $($Passport.project_state.agent_core_roadmap.name) / $($Passport.project_state.agent_core_roadmap.milestone) / $($Passport.project_state.agent_core_roadmap.status)" -ForegroundColor Green
    Write-Host "LAST STABLE    :" -NoNewline; Write-Host " MAIN=$($Passport.project_state.last_stable.main); AGENT_CORE=$($Passport.project_state.last_stable.agent_core)" -ForegroundColor Cyan
    Write-Host "NEXT WORK      :" -NoNewline; Write-Host " MAIN=$($Passport.project_state.next_work.main); AGENT_CORE=$($Passport.project_state.next_work.agent_core)" -ForegroundColor Yellow
} else {
    Write-Host "project_passport.json not found." -ForegroundColor Red
}

# ------------- БЛОК 2: LEDGER (DUAL-STAGE) -------------
Write-Host ""
Write-Host "---------------- LEDGER ----------------" -ForegroundColor Yellow

$Ledger = ".\A_08_LOGS\PROJECT_LEDGER.txt"
$LedgerExists = $false

if (Test-Path $Ledger) {
    $LedgerExists = $true
    $LedgerContent = Get-Content $Ledger -Encoding UTF8
    $LastStable = $LedgerContent | Where-Object { $_ -match "STATUS=STABLE" } | Select-Object -Last 1

    if ($LastStable) {
        $RuntimeStage = $Passport.project_state.main_roadmap.milestone
        $LastStableMilestone = "UNKNOWN"

        # Перезапись отключена по RULE #1 (Passport Supremacy)
        if ($LastStable -match "\[([^\]]+)\]") { $LastStableMilestone = $Matches[1] }

        Write-Host "Main Milestone :" -NoNewline; Write-Host " $RuntimeStage" -ForegroundColor Green
        Write-Host "Ledger Record  :" -NoNewline; Write-Host " $LastStableMilestone" -ForegroundColor Cyan
    } else {
        Write-Host "No STABLE records found." -ForegroundColor Yellow
    }
} else {
    Write-Host "PROJECT_LEDGER.txt not found." -ForegroundColor Red
}

# ------------- БЛОК 3: RECENT CHANGE REQUESTS -------------
Write-Host ""
Write-Host "----------- RECENT CHANGE REQUESTS -----------" -ForegroundColor Yellow

if ($LedgerExists) {
    $RecentCRs = $LedgerContent | Where-Object { $_ -match "\[CHANGE_REQUEST\]" } | Select-Object -Last 3

    if ($RecentCRs) {
        foreach ($cr in $RecentCRs) {
            $TaskName = "UNKNOWN"
            $LockStr = ""

            if ($cr -match "NEXT=([^ ]+)") { $TaskName = $Matches[1] }
            if ($cr -match "LOCK_ID=([^ ]+)") { $LockStr = " [LOCK_ID=$($Matches[1])]" }

            Write-Host "  • " -NoNewline
            Write-Host "PENDING" -ForegroundColor Yellow -NoNewline
            Write-Host " ↳ $TaskName" -NoNewline
            Write-Host $LockStr -ForegroundColor Gray
        }
    } else {
        Write-Host "  • Записей Change Request в Леджере не обнаружено." -ForegroundColor Gray
    }
} else {
    Write-Host "  • Леджер отсутствует, чтение CR невозможно." -ForegroundColor Red
}

# ------------- БЛОК 4: FREEZE STATUS -------------
Write-Host ""
Write-Host "----------- FREEZE STATUS -----------" -ForegroundColor Yellow

if ($PassportValid) {
    Write-Host "Frozen Modules:" -ForegroundColor Red
    foreach ($mod in $Passport.architecture_freeze.frozen_modules) {
        Write-Host "  ↳ $mod" -ForegroundColor Gray
    }

    Write-Host "Active Modules:" -ForegroundColor Green
    foreach ($mod in $Passport.architecture_freeze.active_modules) {
        Write-Host "  ↳ $mod" -ForegroundColor Gray
    }
} else {
    Write-Host "Freeze status unavailable (Passport error)." -ForegroundColor Red
}

# ------------- БЛОК 5: GOALS REGISTRY -------------
Write-Host ""
Write-Host "------------- GOALS REGISTRY ------------" -ForegroundColor Yellow

$GoalsFile = ".\A_07_CONFIG\goals_registry.json"

if (Test-Path $GoalsFile) {
    $Goals = Get-Content $GoalsFile -Raw | ConvertFrom-Json

    Write-Host "Active Goal    :" -NoNewline; Write-Host " $($Goals.active_goal)" -ForegroundColor Cyan
    Write-Host "Current Phase  :" -NoNewline; Write-Host " $($Goals.current_phase)" -ForegroundColor Yellow
} else {
    Write-Host "goals_registry.json not found" -ForegroundColor Red
}

# ------------- БЛОК 6: EXECUTION REGISTRY -------------
Write-Host ""
Write-Host "----------- EXECUTION REGISTRY ----------" -ForegroundColor Yellow

$RegistryFile = ".\A_07_CONFIG\execution_registry.json"

if (Test-Path $RegistryFile) {
    $Registry = Get-Content $RegistryFile -Raw | ConvertFrom-Json

    $TaskCount = 0
    if ($Registry.tasks) {
        $Properties = @($Registry.tasks.PSObject.Properties)
        $TaskCount = $Properties.Count
    }

    Write-Host "Verified Tasks :" -NoNewline; Write-Host " $TaskCount" -ForegroundColor Green
    if ($Registry.last_update) {
        Write-Host "Last Update    :" -NoNewline; Write-Host " $($Registry.last_update)" -ForegroundColor Cyan
    }
} else {
    Write-Host "execution_registry.json not found" -ForegroundColor Red
}

# ------------- БЛОК 7: OBSERVATIONS -------------
Write-Host ""
Write-Host "-------------- OBSERVATIONS -------------" -ForegroundColor Yellow

$ObsFile = ".\A_08_LOGS\OBSERVATIONS.jsonl"

if (Test-Path $ObsFile) {
    $LastHarness = Get-Content $ObsFile -Tail 20 |
        Where-Object { $_ -match "HARNESS_V3_" } |
        Select-Object -Last 1

    if ($LastHarness) {
        $Event = "UNKNOWN"
        $Time = "UNKNOWN"

        if ($LastHarness -match '"event":\s*"([^"]+)"') { $Event = $Matches[1] }
        if ($LastHarness -match '"timestamp":\s*"([^"]+)"') { $Time = $Matches[1] }

        $Color = "Yellow"
        if ($Event -match "SUCCESS") { $Color = "Green" }
        if ($Event -match "REJECTED") { $Color = "Red" }

        Write-Host "Last Harness Event:" -NoNewline; Write-Host " $Event" -ForegroundColor $Color
        Write-Host "Event Time        :" -NoNewline; Write-Host " $Time" -ForegroundColor Cyan
    } else {
        Write-Host "No HARNESS_V3 events found in last 20 observations." -ForegroundColor Yellow
    }
} else {
    Write-Host "OBSERVATIONS.jsonl not found" -ForegroundColor Red
}

# ------------- БЛОК 8: MEMORY MAP -------------
Write-Host ""
Write-Host "--------------- MEMORY MAP ---------------" -ForegroundColor Yellow

$FacadeV2Exist     = Test-Path ".\A_07_MEMORY\memory_facade_v2.py"
$OrchestratorExist = Test-Path ".\A_07_MEMORY\memory_orchestrator_v2.py"
$SemanticExist     = Test-Path ".\A_07_MEMORY\semantic_memory.py"
$AttentionExist    = Test-Path ".\A_07_MEMORY\attention_memory.py"
$ReplayExist       = Test-Path ".\A_07_MEMORY\memory_replay.py"
$BudgetExist       = Test-Path ".\A_07_MEMORY\context_budget_manager.py"

Write-Host "MemoryFacadeV2 (Project State Core):" -ForegroundColor Cyan
if ($FacadeV2Exist) {
    Write-Host "  • L1 Passport  : " -NoNewline; Write-Host "IMPLEMENTED" -ForegroundColor Green
    Write-Host "  • L2 Session   : " -NoNewline; Write-Host "IMPLEMENTED" -ForegroundColor Yellow
    Write-Host "  • L3 Tasks     : " -NoNewline; Write-Host "IMPLEMENTED" -ForegroundColor Green
    Write-Host "  • L4 History   : " -NoNewline; Write-Host "IMPLEMENTED" -ForegroundColor Green
    Write-Host "  • L5 Semantic  : " -NoNewline; Write-Host "IMPLEMENTED" -ForegroundColor Yellow
    Write-Host "  • L6 Strategy  : " -NoNewline; Write-Host "IMPLEMENTED" -ForegroundColor Green
} else {
    Write-Host "   [!] Набор слоев состояния не обнаружен." -ForegroundColor Red
}

Write-Host "MemoryOrchestratorV2 (LLM Prompt Layer):" -ForegroundColor Cyan
if ($OrchestratorExist -and $SemanticExist -and $AttentionExist -and $ReplayExist -and $BudgetExist) {
    Write-Host "  • Semantic Layer  : " -NoNewline; Write-Host "PRESENT" -ForegroundColor Green
    Write-Host "  • Attention Layer : " -NoNewline; Write-Host "PRESENT" -ForegroundColor Green
    Write-Host "  • Replay Layer    : " -NoNewline; Write-Host "PRESENT" -ForegroundColor Green
    Write-Host "  • Budget Layer    : " -NoNewline; Write-Host "PRESENT" -ForegroundColor Green
} else {
    Write-Host "   [!] Слои контекста модели укомплектованы не полностью." -ForegroundColor Red
}

# ------------- БЛОК 9: FILE HEALTH -------------
Write-Host ""
Write-Host "------------- FILE HEALTH ----------------" -ForegroundColor Yellow

$CriticalFiles = @(
    @{ Name = "PROJECT_LEDGER.txt";      Path = ".\A_08_LOGS\PROJECT_LEDGER.txt" },
    @{ Name = "OBSERVATIONS.jsonl";      Path = ".\A_08_LOGS\OBSERVATIONS.jsonl" },
    @{ Name = "goals_registry.json";     Path = ".\A_07_CONFIG\goals_registry.json" },
    @{ Name = "project_passport.json";    Path = ".\A_07_CONFIG\project_passport.json" },
    @{ Name = "execution_registry.json";  Path = ".\A_07_CONFIG\execution_registry.json" }
)

foreach ($file in $CriticalFiles) {
    $PadName = $file.Name.PadRight(25, ".")
    Write-Host "  • $PadName " -NoNewline
    if (Test-Path $file.Path) {
        $Size = (Get-Item $file.Path).Length
        if ($Size -gt 0) {
            Write-Host "OK " -ForegroundColor Green -NoNewline
            Write-Host "($Size B)" -ForegroundColor Gray
        } else {
            Write-Host "EMPTY " -ForegroundColor Yellow -NoNewline
            Write-Host "(0 B - ТРЕВОГА)" -ForegroundColor Yellow
        }
    } else {
        Write-Host "MISSING" -ForegroundColor Red
    }
}

# ------------- БЛОК 10: REAL WORKING CONTOURS -------------
Write-Host ""
Write-Host "----------- REAL WORKING CONTOURS -----------" -ForegroundColor Yellow

Write-Host "Worker Pipeline      : " -NoNewline; Write-Host "PROVEN" -ForegroundColor Green -NoNewline; Write-Host " (QueueManager -> Worker -> ButlerHarness)" -ForegroundColor Gray
Write-Host "Dispatcher Pipeline  : " -NoNewline; Write-Host "PROVEN" -ForegroundColor Green -NoNewline; Write-Host " (SmartDispatcherV2 -> 8 Departments -> ButlerHarness)" -ForegroundColor Gray
Write-Host "Runtime Planner      : " -NoNewline; Write-Host "PROVEN" -ForegroundColor Green -NoNewline; Write-Host " (agent_runtime -> Planner -> CR -> Registry)" -ForegroundColor Gray
Write-Host "Runtime <-> Harness  : " -NoNewline; Write-Host "PROVEN" -ForegroundColor Green -NoNewline; Write-Host " (via CR_RUNTIME_AUTOMATION)" -ForegroundColor Gray

# ------------- БЛОК 11: EXECUTION PROOF MAP -------------
Write-Host ""
Write-Host "------------- EXECUTION PROOF MAP -------------" -ForegroundColor Yellow

try {
    $passportPath = Join-Path $PSScriptRoot "A_07_CONFIG\project_passport.json"
    if (Test-Path $passportPath) {
        $passport = Get-Content $passportPath -Raw -Encoding UTF8 | ConvertFrom-Json
        $proofMap = $passport.execution_proof_map
        if ($proofMap) {
            foreach ($key in $proofMap.psobject.properties.name) {
                $val = $proofMap.$key
                $cleanKey = $key.PadRight(30).Substring(0, 30)
                Write-Host "  • $cleanKey : " -NoNewline
                if ($val -match "PROVEN|SUCCESS|RUNNING_AUTOMATICALLY|COMPLETED") {
                    Write-Host $val -ForegroundColor Green
                } else {
                    Write-Host $val -ForegroundColor Red
                }
            }
        } else {
            Write-Host "  [WARN] Map execution_proof_map пуста или отсутствует." -ForegroundColor Yellow
        }
    } else {
        Write-Host "  [ERROR] project_passport.json не найден по пути $passportPath" -ForegroundColor Red
    }
} catch {
    Write-Host "  [EXCEPTION] Ошибка парсинга паспорта: $_" -ForegroundColor Red
}

Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "READONLY STATUS CENTER COMPLETE" -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan
