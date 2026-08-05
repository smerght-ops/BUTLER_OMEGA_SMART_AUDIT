$Baseline = Get-Content .\A_09_GUARDIANS\baseline_path.txt
$Current  = ".\A_02_MANAGERS\smart_dispatcher_v2.py"

Write-Host ""
Write-Host "========== GENIE PATCH SAFETY ==========" -ForegroundColor Cyan
Write-Host ""

$Blocked = $false

if(!(Test-Path $Current)){
    Write-Host "[FAIL] Current file missing" -ForegroundColor Red
    $Blocked = $true
}

if(!(Test-Path $Baseline)){
    Write-Host "[FAIL] Baseline missing" -ForegroundColor Red
    $Blocked = $true
}

python -m py_compile $Current *> $null

if($LASTEXITCODE -eq 0){
    Write-Host "[OK] Python syntax valid" -ForegroundColor Green
}
else{
    Write-Host "[FAIL] Python syntax invalid" -ForegroundColor Red
    $Blocked = $true
}

if($Blocked){
    Write-Host ""
    Write-Host "PATCH STATUS : BLOCKED" -ForegroundColor Red
}
else{
    Write-Host ""
    Write-Host "PATCH STATUS : SAFE" -ForegroundColor Green
}

Write-Host "========================================"
