Write-Host ""
Write-Host "========== GENIE RISK ENGINE v2 ==========" -ForegroundColor Cyan
Write-Host ""

$StatePath = ".\A_09_GUARDIANS\genie_state.json"

if(!(Test-Path $StatePath)){
    Write-Host "STATE NOT FOUND. Run genie_state_engine.ps1 first." -ForegroundColor Red
    exit 1
}

$state = Get-Content $StatePath -Raw -Encoding UTF8 | ConvertFrom-Json

$critical = @()
$warning = @()
$healthy = @()

foreach($role in $state.roles.PSObject.Properties){

    $name = $role.Name
    $status = $role.Value.status
    $integrity = $role.Value.integrity

    if($status -eq "CRITICAL"){
        $critical += $name
        Write-Host ("CRITICAL  {0,-24} {1}%" -f $name,$integrity) -ForegroundColor Red
    }
    elseif($status -eq "WARNING"){
        $warning += $name
        Write-Host ("WARNING   {0,-24} {1}%" -f $name,$integrity) -ForegroundColor Yellow
    }
    else{
        $healthy += $name
        Write-Host ("HEALTHY   {0,-24} {1}%" -f $name,$integrity) -ForegroundColor Green
    }
}

if($critical.Count -gt 0){
    $risk = "CRITICAL"
}
elseif($warning.Count -gt 0){
    $risk = "WARNING"
}
else{
    $risk = "LOW"
}

$state.risk = @{
    total_roles = $state.roles.PSObject.Properties.Count
    critical_count = $critical.Count
    warning_count = $warning.Count
    healthy_count = $healthy.Count
    total_risk = $risk
    release_gate = $(if($risk -eq "CRITICAL"){"BLOCKED"}else{"ALLOWED"})
}

$state |
ConvertTo-Json -Depth 10 |
Set-Content $StatePath -Encoding UTF8

Write-Host ""
Write-Host "TOTAL RISK   : $risk"
Write-Host "RELEASE GATE : $($state.risk.release_gate)"
Write-Host ""
Write-Host "STATE UPDATED -> risk" -ForegroundColor Green
Write-Host "===========================================" -ForegroundColor Cyan
