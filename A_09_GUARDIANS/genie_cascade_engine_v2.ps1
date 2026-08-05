Write-Host ""
Write-Host "========== GENIE CASCADE ENGINE v2 ==========" -ForegroundColor Cyan
Write-Host ""

$State = Get-Content .\A_09_GUARDIANS\genie_state.json -Raw -Encoding UTF8 | ConvertFrom-Json
$Deps  = Get-Content .\A_09_GUARDIANS\dependency_manifest.json -Raw -Encoding UTF8 | ConvertFrom-Json

$cascade = @{}

foreach($role in $State.roles.PSObject.Properties){

    if($role.Value.status -ne "CRITICAL"){
        continue
    }

    Write-Host "[CRITICAL] $($role.Name)" -ForegroundColor Red

    $affected = @()

    foreach($item in $Deps.$($role.Name).affects){

        $affected += $item
        Write-Host ("    -> {0}" -f $item) -ForegroundColor Yellow

    }

    $cascade[$role.Name] = $affected

}

$State.cascade = $cascade

$State |
ConvertTo-Json -Depth 10 |
Set-Content .\A_09_GUARDIANS\genie_state.json -Encoding UTF8

Write-Host ""
Write-Host "CASCADE SAVED -> genie_state.json" -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Cyan
