param(
    [switch]$Silent
)

if(-not $Silent){

    Write-Host ""
    Write-Host "========== GENIE WATCHDOG ==========" -ForegroundColor Cyan
    Write-Host ""

}

$Modules = @(
    "genie_state_engine.ps1",
    "genie_risk_engine_v2.ps1",
    "genie_cascade_engine_v2.ps1",
    "genie_bone_index.ps1",
    "genie_bark_engine.ps1"
)

foreach($Module in $Modules){

    $Path = Join-Path $PSScriptRoot $Module

    if(Test-Path $Path){

        if(-not $Silent){
            Write-Host ("RUN -> {0}" -f $Module) -ForegroundColor Yellow
        }

        & $Path

    }
    else{

        Write-Host ("[MISSING] {0}" -f $Module) -ForegroundColor Red

    }

}

if(-not $Silent){

    Write-Host ""
    Write-Host "WATCHDOG STATUS : ACTIVE" -ForegroundColor Green
    Write-Host "Bone Cache      : ENABLED"
    Write-Host "Risk Engine     : ENABLED"
    Write-Host "Cascade Engine  : ENABLED"
    Write-Host "Bark Engine     : ENABLED"
    Write-Host ""
    Write-Host "====================================" -ForegroundColor Cyan

}
