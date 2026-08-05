$Baseline = Get-Content .\A_09_GUARDIANS\baseline_path.txt -ErrorAction SilentlyContinue
$Current = ".\A_02_MANAGERS\smart_dispatcher_v2.py"

Write-Host ""
Write-Host "========== GENIE RECOVERY CHECK ==========" -ForegroundColor Cyan
Write-Host ""

if(!(Test-Path $Current)){
    Write-Host "[FAIL] Current dispatcher missing" -ForegroundColor Red
    exit 10
}

Write-Host "[OK] Current dispatcher found" -ForegroundColor Green

if(!(Test-Path $Baseline)){
    Write-Host "[FAIL] Baseline dispatcher missing" -ForegroundColor Red
    exit 11
}

Write-Host "[OK] Baseline dispatcher found" -ForegroundColor Green

$currHash = (Get-FileHash $Current -Algorithm SHA256).Hash
$baseHash = (Get-FileHash $Baseline -Algorithm SHA256).Hash

Write-Host ""
Write-Host "Current SHA256 : $currHash"
Write-Host "Baseline SHA256: $baseHash"

if($currHash -eq $baseHash){

    Write-Host ""
    Write-Host "[INFO] Files are identical." -ForegroundColor Yellow

}
else{

    Write-Host ""
    Write-Host "[INFO] Files differ." -ForegroundColor Yellow
    Write-Host "[OK] Recovery source is available." -ForegroundColor Green

}

Write-Host ""
Write-Host "RECOVERY CHECK COMPLETE." -ForegroundColor Cyan
