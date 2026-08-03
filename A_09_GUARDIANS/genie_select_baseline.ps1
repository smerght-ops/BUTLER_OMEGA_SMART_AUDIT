# GENIE AUTO BASELINE

$History = ".\A_00_HISTORY\ROLLBACK_POINTS"

$Baseline = Get-ChildItem $History -Directory |
Where-Object { $_.Name -match "STABLE" } |
Sort-Object LastWriteTime -Descending |
Select-Object -First 1

Write-Host ""
Write-Host "========== GENIE BASELINE ==========" -ForegroundColor Cyan

if($null -eq $Baseline){

    Write-Host "STABLE baseline not found." -ForegroundColor Red
    return

}

Write-Host "Selected baseline:" -ForegroundColor Green
Write-Host $Baseline.FullName

$Dispatcher = Get-ChildItem $Baseline.FullName -Recurse -Filter smart_dispatcher_v2.py |
Select-Object -First 1

if($Dispatcher){

    Write-Host ""
    Write-Host "Dispatcher:" -ForegroundColor Green
    Write-Host $Dispatcher.FullName

}
else{

    Write-Host ""
    Write-Host "Dispatcher not found inside baseline." -ForegroundColor Red

}

Write-Host ""
Write-Host "====================================" -ForegroundColor Cyan
