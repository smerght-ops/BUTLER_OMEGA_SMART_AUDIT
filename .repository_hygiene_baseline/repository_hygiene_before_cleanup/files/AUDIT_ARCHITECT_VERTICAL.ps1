$ErrorActionPreference = "SilentlyContinue"
$Root = (Get-Location).Path
$Report = Join-Path $Root "ARCHITECT_VERTICAL_AUDIT_REPORT.txt"

$Exclude = '\\A_00_(LEGACY|HISTORY|RESTORE|ARCHIVE|BACKUPS|SNAPSHOTS|AVARIYKA|QUARANTINE)\\|\\AUDIT_PACKS\\|\\A_99_TESTS\\|\\A_09_TESTS\\|\\__pycache__\\|\\\.git\\|\\\.venv\\|\\venv\\'

$Files = @(Get-ChildItem $Root -Recurse -File -ErrorAction SilentlyContinue |
    Where-Object {
        $_.Extension -in @(".py",".json",".jsonl",".md",".ps1") -and
        $_.FullName -notmatch $Exclude -and
        $_.Name -notin @(
            "PROJECT_TECHNICAL_AUDIT_PACK.md",
            "PROJECT_TECHNICAL_AUDIT_PACK_V2.md",
            "PROJECT_FULL_CONTEXT_PACK.md"
        )
    })

$Lines = [System.Collections.Generic.List[string]]::new()

function Add-Line([string]$Text="") {
    $Lines.Add($Text)
    Write-Host $Text
}

function Add-Hits($Title, $Hits, [int]$Limit=200) {
    Add-Line ""
    Add-Line "============================================================"
    Add-Line $Title
    Add-Line "============================================================"

    $arr = @($Hits)

    if ($arr.Count -eq 0) {
        Add-Line "NO EVIDENCE FOUND"
        return
    }

    Add-Line "HITS: $($arr.Count)"

    foreach ($h in ($arr | Select-Object -First $Limit)) {
        $rel = $h.Path.Replace($Root + "\", "")
        Add-Line "$rel : $($h.LineNumber)"
        Add-Line "  $($h.Line.Trim())"
    }
}

Add-Line "BUTLER ARCHITECT VERTICAL AUDIT"
Add-Line "DATE: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
Add-Line "ROOT: $Root"
Add-Line "FILES SCANNED: $($Files.Count)"
Add-Line "MODE: STRICT READ ONLY"

# 1. Inspector outputs / architecture facts
$Inspector = $Files | Select-String -Pattern `
'Inspector[0-9]|PhysicalMap|EntityMap|ImportMap|RegistrationAST|CallGraph|LinkMap|UnifiedInspectorFacts|PROJECT_GRAPH|PROJECT_EVIDENCE' `
-CaseSensitive:$false

Add-Hits "1. INSPECTORS AND ARCHITECTURE FACTS" $Inspector

# 2. Кто создаёт/пишет архитектурные данные
$Writers = $Files | Select-String -Pattern `
'PhysicalMap|EntityMap|ImportMap|RegistrationAST|CallGraph|LinkMap|UnifiedInspectorFacts|PROJECT_GRAPH|PROJECT_EVIDENCE' `
-CaseSensitive:$false |
Where-Object {
    $_.Line -match 'write|dump|save|open\(|Set-Content|Out-File|json'
}

Add-Hits "2. INSPECTOR OUTPUT WRITERS" $Writers

# 3. Кто читает архитектурные данные
$Readers = $Files | Select-String -Pattern `
'PhysicalMap|EntityMap|ImportMap|RegistrationAST|CallGraph|LinkMap|UnifiedInspectorFacts|PROJECT_GRAPH|PROJECT_EVIDENCE|PROJECT_STATE|PROJECT_MEMORY_INDEX|CAPABILITY_AUDIT|CapabilityRegistry' `
-CaseSensitive:$false |
Where-Object {
    $_.Path -match 'Architect|Context|Memory|Department|Manager|Provider'
}

Add-Hits "3. ARCHITECTURE KNOWLEDGE CONSUMERS" $Readers

# 4. ContextProvider
$ContextProviderFiles = @($Files | Where-Object {
    $_.Name -match 'context_provider'
})

$ContextHits = foreach ($f in $ContextProviderFiles) {
    Select-String -Path $f.FullName -Pattern `
    'open\(|json|sqlite|Inspector|Map|Registry|PROJECT_|Memory|Facade|load|read|get_' `
    -CaseSensitive:$false
}

Add-Hits "4. CONTEXT PROVIDER INPUTS" $ContextHits

# 5. ArchitectAgent subsystem
$ArchitectFiles = @($Files | Where-Object {
    $_.FullName -match '\\ArchitectAgent\\'
})

$ArchitectLinks = foreach ($f in $ArchitectFiles) {
    Select-String -Path $f.FullName -Pattern `
    '^\s*(from|import)\s|ContextProvider|goal_analyzer|planner|audit|status|self_test|release|ollama|model|generate|chat|requests' `
    -CaseSensitive:$false
}

Add-Hits "5. ARCHITECT AGENT INTERNAL CONNECTIONS" $ArchitectLinks

# 6. Кто вызывает ArchitectAgent снаружи
$ArchitectCallers = $Files |
Where-Object { $_.FullName -notmatch '\\ArchitectAgent\\' } |
Select-String -Pattern `
'ArchitectAgent|architect_agent|architect_status|architect_audit|architect_self_test|architect_release_check|ContextProvider|goal_analyzer' `
-CaseSensitive:$false

Add-Hits "6. EXTERNAL CALLERS OF ARCHITECT SUBSYSTEM" $ArchitectCallers

# 7. Регистрация Department / Dispatcher
$RouteFiles = $Files | Where-Object {
    $_.Name -match 'dispatcher|department|router|BUTLER_OS|harness'
}

$Routes = $RouteFiles | Select-String -Pattern `
'ARCHITECT|Architect|architecture|архитект|GOAL_MANAGER|GoalManager' `
-CaseSensitive:$false

Add-Hits "7. ARCHITECTURE DEPARTMENT AND DISPATCHER ROUTE" $Routes

# 8. Связь ArchitectAgent с LLM
$ModelHits = foreach ($f in $ArchitectFiles) {
    Select-String -Path $f.FullName -Pattern `
    'ollama|11434|api/chat|api/generate|ProviderManager|model|requests\.|generate\(|chat\(' `
    -CaseSensitive:$false
}

Add-Hits "8. ARCHITECT AGENT TO MODEL / LLM" $ModelHits

# 9. Ключевые файлы ArchitectAgent
Add-Line ""
Add-Line "============================================================"
Add-Line "9. ARCHITECT AGENT FILES FOUND"
Add-Line "============================================================"

foreach ($f in $ArchitectFiles) {
    Add-Line $f.FullName.Replace($Root + "\", "")
}

# 10. Итоговая диагностическая матрица
Add-Line ""
Add-Line "============================================================"
Add-Line "10. VERTICAL DIAGNOSTIC SUMMARY"
Add-Line "============================================================"

Add-Line "Inspector/Facts evidence : $(@($Inspector).Count)"
Add-Line "Inspector writers        : $(@($Writers).Count)"
Add-Line "Knowledge consumers      : $(@($Readers).Count)"
Add-Line "ContextProvider files    : $($ContextProviderFiles.Count)"
Add-Line "ContextProvider evidence : $(@($ContextHits).Count)"
Add-Line "ArchitectAgent files     : $($ArchitectFiles.Count)"
Add-Line "Architect internal links : $(@($ArchitectLinks).Count)"
Add-Line "External architect calls : $(@($ArchitectCallers).Count)"
Add-Line "Dispatcher route evidence: $(@($Routes).Count)"
Add-Line "Architect LLM evidence   : $(@($ModelHits).Count)"

Add-Line ""
Add-Line "TARGET VERTICAL:"
Add-Line "INSPECTORS -> KNOWLEDGE STORAGE -> CONTEXT PROVIDER -> ARCHITECT AGENT -> LLM -> DEPARTMENT/RUNTIME"
Add-Line ""
Add-Line "AUDIT COMPLETE - READ ONLY"

$Lines | Set-Content -Path $Report -Encoding UTF8

Write-Host ""
Write-Host "============================================================" -ForegroundColor Green
Write-Host " AUDIT FINISHED" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Green
Write-Host "REPORT: $Report" -ForegroundColor Yellow
