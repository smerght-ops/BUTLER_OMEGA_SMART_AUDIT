$Baseline = Get-Content .\A_09_GUARDIANS\baseline_path.txt
$Current  = ".\A_02_MANAGERS\smart_dispatcher_v2.py"

Write-Host ""
Write-Host "========== GENIE PATCH VALIDATOR ==========" -ForegroundColor Cyan
Write-Host ""

$CurrentText  = Get-Content $Current  -Raw -Encoding UTF8
$BaselineText = Get-Content $Baseline -Raw -Encoding UTF8

$Targets = @(
    "def _execute_department",
    "self.harness.execute",
    "def dispatch"
)

foreach($Target in $Targets){

    Write-Host "------------------------------------------"

    $CurrentCount  = ([regex]::Matches($CurrentText,[regex]::Escape($Target))).Count
    $BaselineCount = ([regex]::Matches($BaselineText,[regex]::Escape($Target))).Count

    Write-Host "TARGET : $Target"

    Write-Host "Current  : $CurrentCount"
    Write-Host "Baseline : $BaselineCount"

    if($BaselineCount -eq 0){

        Write-Host "[ERROR] Target absent in baseline." -ForegroundColor Red
        continue

    }

    if($CurrentCount -gt $BaselineCount){

        Write-Host "[WARNING] Duplicate detected." -ForegroundColor Yellow
        continue

    }

    if($CurrentCount -eq $BaselineCount){

        Write-Host "[OK] Already synchronized." -ForegroundColor Green
        continue

    }

    if($CurrentCount -lt $BaselineCount){

        Write-Host "[RESTORE REQUIRED]" -ForegroundColor Red

    }

}

Write-Host ""
Write-Host "==========================================="
Write-Host "PATCH VALIDATION COMPLETE."
