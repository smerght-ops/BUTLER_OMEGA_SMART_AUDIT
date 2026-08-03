Write-Host ""
Write-Host "========== GENIE CASCADE IMPACT ==========" -ForegroundColor Cyan
Write-Host ""

$RoleOutput =
& .\A_09_GUARDIANS\genie_role_engine.ps1 2>&1

$Critical=@()

foreach($line in $RoleOutput){

    if($line -match "^ROLE : (.+)$"){
        $CurrentRole=$Matches[1]
    }

    if($line -match "^STATUS : CRITICAL"){
        $Critical += $CurrentRole
    }

}

$Deps =
Get-Content .\A_09_GUARDIANS\dependency_manifest.json |
ConvertFrom-Json

foreach($Role in $Critical){

    Write-Host ""
    Write-Host "[CRITICAL ROLE] $Role" -ForegroundColor Red

    foreach($Affect in $Deps.$Role.affects){

        Write-Host ("   ↓ affects -> {0}" -f $Affect) -ForegroundColor Yellow

        if($Deps.$Affect){

            foreach($Next in $Deps.$Affect.affects){

                Write-Host ("          ↓ then -> {0}" -f $Next) -ForegroundColor DarkYellow

            }

        }

    }

}

Write-Host ""
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "CASCADE ANALYSIS COMPLETE."
