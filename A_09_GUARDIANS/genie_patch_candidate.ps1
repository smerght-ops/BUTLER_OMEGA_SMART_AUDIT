$Baseline = Get-Content .\A_09_GUARDIANS\baseline_path.txt -Encoding UTF8

$Current = ".\A_02_MANAGERS\smart_dispatcher_v2.py"

Write-Host ""
Write-Host "========== GENIE PATCH CANDIDATE ==========" -ForegroundColor Cyan
Write-Host ""

$targets = @(
    "def _execute_department",
    "self.harness.execute",
    "def dispatch"
)

foreach($target in $targets){

    Write-Host "TARGET : $target" -ForegroundColor Yellow

    $currentFound = Select-String -Path $Current -Pattern ([regex]::Escape($target)) -Quiet

    if($currentFound){
        Write-Host "STATUS : PRESENT"
        Write-Host ""
        continue
    }

    Write-Host "STATUS : MISSING" -ForegroundColor Red

    $hit = Select-String `
        -Path $Baseline `
        -Pattern ([regex]::Escape($target))

    if($hit){

        Write-Host "SOURCE LINE :" $hit.LineNumber
        Write-Host "READY FOR SAFE RESTORE" -ForegroundColor Green

    }
    else{

        Write-Host "NOT FOUND IN BASELINE" -ForegroundColor Red

    }

    Write-Host ""
}

Write-Host "==========================================="
Write-Host "PATCH CANDIDATES READY."
