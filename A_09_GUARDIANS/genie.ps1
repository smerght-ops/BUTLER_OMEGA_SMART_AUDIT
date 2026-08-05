param(
    [ValidateSet("full","state","risk","cascade")]
    [string]$Mode="full"
)

Write-Host ""
Write-Host "========== GENIE COMMAND CENTER v2 ==========" -ForegroundColor Cyan
Write-Host ("MODE : {0}" -f $Mode)
Write-Host ""

$Root = Split-Path $MyInvocation.MyCommand.Path

function Run-Step($Name){

    $Script = Join-Path $Root $Name

    if(Test-Path $Script){

        Write-Host ("RUN -> {0}" -f $Name) -ForegroundColor Yellow
        & $Script
        Write-Host ""

    }
    else{

        Write-Host ("SKIP -> {0} (not found)" -f $Name) -ForegroundColor DarkYellow

    }

}

switch($Mode){

    "state" {

        Run-Step "genie_state_engine.ps1"

    }

    "risk" {

        Run-Step "genie_risk_engine_v2.ps1"

    }

    "cascade" {

        Run-Step "genie_cascade_engine_v2.ps1"

    }

    "full" {

        Run-Step "genie_state_engine.ps1"
        Run-Step "genie_risk_engine_v2.ps1"
        Run-Step "genie_cascade_engine_v2.ps1"

    }

}

Write-Host ""
Write-Host "GENIE COMMAND CENTER COMPLETE." -ForegroundColor Green
