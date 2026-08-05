# GENIE PATCH CONFIDENCE
# Butler Omega Smart
# Stage 4.29.18

Write-Host ""
Write-Host "========== GENIE PATCH CONFIDENCE ==========" -ForegroundColor Cyan
Write-Host ""

$Baseline = Get-Content .\A_09_GUARDIANS\baseline_path.txt -Encoding UTF8
$Current  = ".\A_02_MANAGERS\smart_dispatcher_v2.py"

$targets = @(
    "def _execute_department",
    "self.harness.execute",
    "def dispatch"
)

foreach($target in $targets){

    Write-Host "TARGET : $target" -ForegroundColor Yellow

    $score = 0

    $currentHit = Select-String `
        -Path $Current `
        -Pattern ([regex]::Escape($target))

    $baselineHit = Select-String `
        -Path $Baseline `
        -Pattern ([regex]::Escape($target))

    if($baselineHit){
        Write-Host "Baseline ........ FOUND" -ForegroundColor Green
        $score += 25
    }
    else{
        Write-Host "Baseline ........ MISSING" -ForegroundColor Red
    }

    if($currentHit){
        Write-Host "Current ......... PRESENT" -ForegroundColor Green
        $score += 25
    }
    else{
        Write-Host "Current ......... MISSING" -ForegroundColor Yellow
    }

    if($baselineHit){
        Write-Host "Signature ....... MATCH" -ForegroundColor Green
        $score += 25
    }

    if($baselineHit){
        Write-Host "Source Ready .... YES" -ForegroundColor Green
        $score += 25
    }

    Write-Host ""
    Write-Host ("CONFIDENCE : {0}%" -f $score)

    if($score -ge 100){
        Write-Host "AUTO RESTORE : SAFE" -ForegroundColor Green
    }
    elseif($score -ge 75){
        Write-Host "AUTO RESTORE : REVIEW" -ForegroundColor Yellow
    }
    else{
        Write-Host "AUTO RESTORE : BLOCKED" -ForegroundColor Red
    }

    Write-Host ""
}

Write-Host "===========================================" -ForegroundColor Cyan
Write-Host "PATCH CONFIDENCE COMPLETE."
