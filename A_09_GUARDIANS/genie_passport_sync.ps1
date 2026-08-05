Write-Host ""
Write-Host "========== GENIE PASSPORT SYNC ==========" -ForegroundColor Cyan
Write-Host ""

$StatePath = ".\A_09_GUARDIANS\genie_state.json"

if(!(Test-Path $StatePath)){
    Write-Host "GENIE STATE NOT FOUND." -ForegroundColor Red
    exit 1
}

$state = Get-Content $StatePath -Raw -Encoding UTF8 | ConvertFrom-Json

$passport = [ordered]@{

    genie_version = "1.0"

    generated = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

    total_risk = $state.risk.total_risk

    release_gate = $state.risk.release_gate

    dispatcher_integrity = $state.roles.Dispatcher.integrity

    dispatcher_status = $state.roles.Dispatcher.status

}

$passport |
ConvertTo-Json -Depth 5 |
Set-Content .\A_09_GUARDIANS\genie_passport_state.json -Encoding UTF8

Write-Host "Passport synchronized." -ForegroundColor Green
Write-Host "Saved -> genie_passport_state.json" -ForegroundColor Green
Write-Host ""
Write-Host "==========================================" -ForegroundColor Cyan
