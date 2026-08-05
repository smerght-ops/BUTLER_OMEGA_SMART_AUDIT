Write-Host ""
Write-Host "========== GENIE DEPENDENCY ENGINE ==========" -ForegroundColor Cyan
Write-Host ""

$roles =
Get-Content .\A_09_GUARDIANS\role_manifest.json -Encoding UTF8 |
ConvertFrom-Json

$deps =
Get-Content .\A_09_GUARDIANS\dependency_manifest.json -Encoding UTF8 |
ConvertFrom-Json

$RoleEngine = Join-Path $PSScriptRoot "genie_role_engine.ps1"

if(Test-Path $RoleEngine){
    & $RoleEngine | Out-Null
}

foreach($role in $deps.PSObject.Properties){

    Write-Host "ROLE :" $role.Name -ForegroundColor Yellow

    foreach($dep in $role.Value.depends_on){

        Write-Host ("   depends on -> {0}" -f $dep)

    }

    foreach($aff in $role.Value.affects){

        Write-Host ("   affects    -> {0}" -f $aff)

    }

    Write-Host ""

}

Write-Host "=============================================" -ForegroundColor Cyan
Write-Host "DEPENDENCY ENGINE COMPLETE."
