param(
    [Parameter(Mandatory=$true)]
    [string]$Goal
)

Set-Location "C:\Users\KOS\Desktop\Butler_Agent\BUTLER_OMEGA_SMART"

Write-Host ""
Write-Host "BUTLER GOAL:" $Goal
Write-Host ""

python -c "from A_02_MANAGERS.Planner.planner_engine import PlannerEngine; PlannerEngine.execute('$Goal')"
