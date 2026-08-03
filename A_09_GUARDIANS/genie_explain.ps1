# GENIE EXPLAINER

$Current = ".\A_02_MANAGERS\smart_dispatcher_v2.py"

$Baseline = Get-ChildItem .\A_00_HISTORY\ROLLBACK_POINTS -Recurse -Filter smart_dispatcher_v2.py |
Sort-Object LastWriteTime -Descending |
Select-Object -First 1

$currentText  = Get-Content $Current -Encoding UTF8
$baselineText = Get-Content $Baseline.FullName -Encoding UTF8

Write-Host ""
Write-Host "========== GENIE EXPLAIN ==========" -ForegroundColor Cyan

Compare-Object $baselineText $currentText |
Where-Object {
    $_.InputObject -match "_execute_department" -or
    $_.InputObject -match "self\.harness\.execute"
} |
ForEach-Object {

    if ($_.SideIndicator -eq "<=") {
        Write-Host ""
        Write-Host "REMOVED:" -ForegroundColor Red
        Write-Host $_.InputObject -ForegroundColor Red
    }

    if ($_.SideIndicator -eq "=>") {
        Write-Host ""
        Write-Host "ADDED:" -ForegroundColor Yellow
        Write-Host $_.InputObject -ForegroundColor Yellow
    }

}

Write-Host ""
Write-Host "===================================" -ForegroundColor Cyan
