Write-Host ""
Write-Host "========== GENIE FREEZE VALIDATOR ==========" -ForegroundColor Cyan
Write-Host ""

$ok = $true

$files = @(
".\A_09_GUARDIANS\genie.ps1",
".\A_09_GUARDIANS\genie_state_engine.ps1",
".\A_09_GUARDIANS\genie_risk_engine_v2.ps1",
".\A_09_GUARDIANS\genie_cascade_engine_v2.ps1",
".\A_09_GUARDIANS\genie_passport_sync.ps1",
".\A_09_GUARDIANS\genie_state.json",
".\A_09_GUARDIANS\genie_passport_state.json",
".\A_09_GUARDIANS\role_manifest.json",
".\A_09_GUARDIANS\dependency_manifest.json",
".\A_09_GUARDIANS\criticality_manifest.json"
)

foreach($f in $files){

    if(Test-Path $f){
        Write-Host ("[OK]   {0}" -f $f) -ForegroundColor Green
    }
    else{
        Write-Host ("[MISS] {0}" -f $f) -ForegroundColor Red
        $ok = $false
    }

}

Write-Host ""

if($ok){

    Write-Host "GENIE VERSION : 1.0" -ForegroundColor Green
    Write-Host "STATUS        : STABLE" -ForegroundColor Green
    Write-Host "FREEZE        : APPROVED" -ForegroundColor Green

}
else{

    Write-Host "FREEZE FAILED." -ForegroundColor Red
    exit 1

}

Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
