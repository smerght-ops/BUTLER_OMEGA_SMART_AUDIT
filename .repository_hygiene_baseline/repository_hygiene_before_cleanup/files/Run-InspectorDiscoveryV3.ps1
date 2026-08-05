param(
    [Parameter(Mandatory=$true)]
    [string]$Query
)

$ErrorActionPreference = "Stop"

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "INSPECTOR DISCOVERY V3 RUNNER" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan

$Root = "C:\Users\KOS\Desktop\Butler_Agent\BUTLER_OMEGA_SMART"
Set-Location $Root

$Inspector = $null

if (Test-Path ".\Inspector-Discovery_v2.py") {
    $Inspector = ".\Inspector-Discovery_v2.py"
}
elseif (Test-Path ".\Inspector-Discovery.py") {
    $Inspector = ".\Inspector-Discovery.py"
}
else {
    Write-Host "ERROR: Inspector-Discovery not found." -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "REALITY INSPECTOR:" $Inspector -ForegroundColor Yellow
python $Inspector $Query

Write-Host ""
Write-Host "KNOWLEDGE / HISTORY LAYER" -ForegroundColor Yellow
python ".\InspectorKnowledgeLayer.py" $Query
