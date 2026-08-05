# GENIE RELEASE GATE v1.0

$RiskScript = ".\A_09_GUARDIANS\genie_risk_engine.ps1"

Write-Host ""
Write-Host "========== GENIE RELEASE GATE ==========" -ForegroundColor Cyan

if(!(Test-Path $RiskScript)){
    Write-Host "GENIE RISK ENGINE NOT FOUND" -ForegroundColor Red
    exit 1
}

$result = powershell -ExecutionPolicy Bypass -File $RiskScript

$riskLine = $result | Select-String "TOTAL RISK"

if(!$riskLine){

    Write-Host "Cannot determine project risk." -ForegroundColor Red
    exit 1

}

$risk = ($riskLine.ToString().Split(":")[1]).Trim()

Write-Host ""
Write-Host "Detected Risk : $risk"

switch($risk){

    "LOW"{

        Write-Host ""
        Write-Host "PASSPORT UPDATE : ALLOWED" -ForegroundColor Green
        exit 0

    }

    "MEDIUM"{

        Write-Host ""
        Write-Host "PASSPORT UPDATE : ALLOWED WITH REVIEW" -ForegroundColor Yellow
        exit 0

    }

    "HIGH"{

        Write-Host ""
        Write-Host "PASSPORT UPDATE : BLOCKED" -ForegroundColor Red
        exit 2

    }

    "CRITICAL"{

        Write-Host ""
        Write-Host "PASSPORT UPDATE : BLOCKED" -ForegroundColor Red
        exit 3

    }

    default{

        Write-Host ""
        Write-Host "UNKNOWN RISK LEVEL" -ForegroundColor Red
        exit 10

    }

}
