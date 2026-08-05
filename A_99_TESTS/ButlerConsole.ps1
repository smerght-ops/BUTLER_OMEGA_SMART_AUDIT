# Butler Omega Smart — единая PowerShell-консоль управления

$script:ButlerRoot = Split-Path -Parent $PSScriptRoot
$script:ReportsDir = Join-Path $PSScriptRoot "reports"
$script:BackupRoot = Join-Path (Split-Path $script:ButlerRoot -Parent) "BUTLER_BACKUPS"
$script:FastBat = Join-Path $script:ButlerRoot "START_FAST_ACCEPTANCE.bat"
$script:FullBat = Join-Path $script:ButlerRoot "START_FULL_ACCEPTANCE.bat"
$script:RuntimeBat = Join-Path $script:ButlerRoot "START_BUTLER_OS.bat"

function Write-ButlerHeader([string]$Text) {
    Write-Host ""
    Write-Host "============================================================" -ForegroundColor Cyan
    Write-Host " BUTLER OMEGA SMART — $Text" -ForegroundColor Yellow
    Write-Host "============================================================" -ForegroundColor Cyan
}

function Invoke-ButlerFast {
    Write-ButlerHeader "FAST ACCEPTANCE"
    Push-Location $script:ButlerRoot
    try { & $script:FastBat; return $LASTEXITCODE }
    finally { Pop-Location }
}

function Invoke-ButlerFull {
    Write-ButlerHeader "FULL ACCEPTANCE"
    Push-Location $script:ButlerRoot
    try { & $script:FullBat; return $LASTEXITCODE }
    finally { Pop-Location }
}

function Start-ButlerRuntime {
    Write-ButlerHeader "RUNTIME"
    Push-Location $script:ButlerRoot
    try { & $script:RuntimeBat }
    finally { Pop-Location }
}

function Backup-ButlerProject {
    Write-ButlerHeader "BACKUP"
    New-Item -ItemType Directory -Path $script:BackupRoot -Force | Out-Null
    $stamp = Get-Date -Format "yyyyMMdd_HHmmss"
    $target = Join-Path $script:BackupRoot "BUTLER_OMEGA_SMART_$stamp"

    & robocopy $script:ButlerRoot $target /E `
        /XD ".git" "__pycache__" "GENERATED_IMAGES" `
        /XF "*.pyc" "*.bak" `
        /R:1 /W:1 /NFL /NDL /NJH /NJS

    $rc = $LASTEXITCODE
    if ($rc -le 7 -and (Test-Path $target)) {
        Write-Host "BACKUP CREATED: $target" -ForegroundColor Green
        return $target
    }

    throw "Ошибка robocopy. Exit code: $rc"
}

function Get-ButlerStatus {
    Write-ButlerHeader "LATEST ACCEPTANCE REPORT"
    $report = Join-Path $script:ReportsDir "latest_acceptance_report.md"
    if (Test-Path $report) { Get-Content $report -Encoding UTF8 }
    else { Write-Host "Отчёт не найден: $report" -ForegroundColor Red }
}

function Test-ButlerHealth {
    Write-ButlerHeader "HEALTH"
    [pscustomobject]@{
        ProjectRoot = Test-Path $script:ButlerRoot
        FastBAT     = Test-Path $script:FastBat
        FullBAT     = Test-Path $script:FullBat
        RuntimeBAT  = Test-Path $script:RuntimeBat
        Reports     = Test-Path $script:ReportsDir
        LatestMD    = Test-Path (Join-Path $script:ReportsDir "latest_acceptance_report.md")
        LatestJSON  = Test-Path (Join-Path $script:ReportsDir "latest_acceptance_report.json")
        BackupRoot  = Test-Path $script:BackupRoot
    } | Format-List
}

function Invoke-ButlerRegression {

    Write-ButlerHeader "REGRESSION PIPELINE"

    Invoke-ButlerFast

    if ($LASTEXITCODE -ne 0) {
        Write-Host ""
        Write-Host "FAST ACCEPTANCE FAILED." -ForegroundColor Red
        return
    }

    Invoke-ButlerFull

    if ($LASTEXITCODE -ne 0) {
        Write-Host ""
        Write-Host "FULL ACCEPTANCE FAILED." -ForegroundColor Red
        return
    }

    $backup = Backup-ButlerProject

    Write-Host ""
    Write-Host "==============================================" -ForegroundColor Green
    Write-Host " REGRESSION PASSED" -ForegroundColor Green
    Write-Host " BACKUP: $backup" -ForegroundColor Green
    Write-Host "==============================================" -ForegroundColor Green

}

function Show-ButlerHelp {
    Write-ButlerHeader "COMMANDS"
    Write-Host "Invoke-ButlerFast        — быстрая проверка"
    Write-Host "Invoke-ButlerFull        — полная проверка"
    Write-Host "Invoke-ButlerRegression  — FAST → FULL → BACKUP"
    Write-Host "Start-ButlerRuntime      — запустить Butler"
    Write-Host "Backup-ButlerProject     — создать отдельный бэкап"
    Write-Host "Get-ButlerStatus         — показать последний отчёт"
    Write-Host "Test-ButlerHealth        — проверить инфраструктуру"
}

Write-Host "ButlerConsole загружен. Команда: Show-ButlerHelp" -ForegroundColor Green
