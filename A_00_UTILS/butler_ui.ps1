# ============================================================
# BUTLER UI UTILITIES v2.0
# ASCII-safe for Windows PowerShell 5.1
# CORE IS TABOO - NOT TOUCHED
# ============================================================

$global:ButlerSessionLog = "A_08_LOGS\butler_session.log"
$global:ButlerSpinnerFrames = @("|", "/", "-", "\")

function Write-ButlerLog {
    param(
        [string]$Level,
        [string]$Message
    )

    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

    if (-not (Test-Path "A_08_LOGS")) {
        New-Item -ItemType Directory -Force -Path "A_08_LOGS" | Out-Null
    }

    Add-Content `
        -Path $global:ButlerSessionLog `
        -Value "[$timestamp] [$Level] $Message" `
        -Encoding UTF8
}

function Show-ButlerHeader {
    param([string]$Title)

    Write-Host ""
    Write-Host "==================================================" -ForegroundColor Cyan
    Write-Host " $Title" -ForegroundColor Cyan
    Write-Host "==================================================" -ForegroundColor Cyan
}

function Show-ButlerInfo {
    param([string]$Message)

    Write-Host "[INFO] $Message" -ForegroundColor Cyan
    Write-ButlerLog "INFO" $Message
}

function Show-ButlerSuccess {
    param([string]$Message)

    Write-Host "[ OK ] $Message" -ForegroundColor Green
    Write-ButlerLog "OK" $Message
}

function Show-ButlerWarning {
    param([string]$Message)

    Write-Host "[WARN] $Message" -ForegroundColor Yellow
    Write-ButlerLog "WARN" $Message
}

function Show-ButlerError {
    param([string]$Message)

    Write-Host "[FAIL] $Message" -ForegroundColor Red
    Write-ButlerLog "FAIL" $Message
}

function Start-ButlerStep {
    param([string]$Name)

    Write-Host ""
    Write-Host "--------------------------------------------------" -ForegroundColor DarkCyan
    Write-Host ">>> $Name" -ForegroundColor Cyan
    Write-Host "--------------------------------------------------" -ForegroundColor DarkCyan
    Write-ButlerLog "START" $Name
}

function Complete-ButlerStep {
    param(
        [string]$Name,
        [double]$Seconds = 0
    )

    Write-Progress -Activity $Name -Completed

    if ($Seconds -gt 0) {
        Show-ButlerSuccess "$Name completed in $Seconds sec"
    }
    else {
        Show-ButlerSuccess "$Name completed"
    }
}

function Show-ButlerProgress {
    param(
        [string]$Activity,
        [int]$Current,
        [int]$Total,
        [string]$Status = ""
    )

    if ($Total -gt 0) {
        $percent = [math]::Floor(($Current / $Total) * 100)
    }
    else {
        $percent = 0
    }

    Write-Progress `
        -Activity $Activity `
        -Status $Status `
        -PercentComplete $percent
}

function Invoke-ButlerTask {
    param(
        [string]$Title,
        [scriptblock]$Command
    )

    Start-ButlerStep $Title

    $started = Get-Date
    Show-ButlerInfo "Started: $($started.ToString('HH:mm:ss'))"

    try {
        & $Command

        $exit = $LASTEXITCODE

        if ($null -ne $exit -and $exit -ne 0) {
            throw "$Title failed with exit code $exit"
        }

        $finished = Get-Date
        $seconds = [math]::Round(($finished - $started).TotalSeconds, 2)

        Complete-ButlerStep $Title $seconds
    }
    catch {
        Show-ButlerError "$Title failed: $_"
        throw
    }
}

function Invoke-ButlerPython {
    param(
        [string]$Title,
        [string]$Arguments
    )

    Invoke-ButlerTask -Title $Title -Command {
        Show-ButlerInfo "python $Arguments"

        $parts = $Arguments.Split(" ")
        & python @parts
    }
}

function Test-ButlerUI {
    Show-ButlerHeader "BUTLER UI v2.0 SELF TEST"

    Invoke-ButlerTask -Title "Progress Demo" -Command {
        for ($i = 1; $i -le 100; $i++) {
            Show-ButlerProgress `
                -Activity "Butler UI Progress Demo" `
                -Current $i `
                -Total 100 `
                -Status "Step $i / 100"

            Start-Sleep -Milliseconds 10
        }
    }

    Show-ButlerSuccess "Butler UI v2.0 self-test finished"
}

Show-ButlerSuccess "Butler UI Utilities v2.0 loaded"