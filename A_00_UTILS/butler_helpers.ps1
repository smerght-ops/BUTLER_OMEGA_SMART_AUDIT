$global:ButlerLogDir = "A_08_LOGS"

if (-not (Test-Path $global:ButlerLogDir)) {
    New-Item -ItemType Directory -Path $global:ButlerLogDir | Out-Null
}

$global:ButlerLogFile = Join-Path $global:ButlerLogDir "butler_system.log"

function Write-Log($Prefix, $Message) {
    $Timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    Add-Content -Path $global:ButlerLogFile -Value "[$Timestamp] [$Prefix] $Message" -Encoding UTF8
}

function Show-Info($Message) {
    Write-Host ""
    Write-Host "[INFO] $Message" -ForegroundColor Cyan
    Write-Log "INFO" $Message
}

function Show-Success($Message) {
    Write-Host ""
    Write-Host "==================================================" -ForegroundColor Green
    Write-Host "[OK] $Message" -ForegroundColor Green
    Write-Host "==================================================" -ForegroundColor Green
    Write-Log "SUCCESS" $Message
}

function Show-WarningMsg($Message) {
    Write-Host ""
    Write-Host "[WARNING] $Message" -ForegroundColor Yellow
    Write-Log "WARNING" $Message
}

function Show-ErrorMsg($Message) {
    Write-Host ""
    Write-Host "[ERROR] $Message" -ForegroundColor Red
    Write-Log "ERROR" $Message
}

function Assert-Success($Description) {
    if ($LASTEXITCODE -ne 0) {
        Show-ErrorMsg "$Description FAILED"
        throw "$Description FAILED"
    }

    Write-Host "[OK] $Description" -ForegroundColor Green
    Write-Log "SUCCESS" "$Description - OK"
}