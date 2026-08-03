$Host.UI.RawUI.WindowTitle = "BUTLER OMEGA SMART - RED STOP"
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
Set-Location $PSScriptRoot

function OK($m){ Write-Host "[OK] $m" -ForegroundColor Green }
function INFO($m){ Write-Host "[..] $m" -ForegroundColor Cyan }

Clear-Host
Write-Host "=====================================================" -ForegroundColor Red
Write-Host "       BUTLER OMEGA SMART - RED STOP BUTTON          " -ForegroundColor Red
Write-Host "=====================================================" -ForegroundColor Red
Write-Host "[ROOT] $PWD"
Write-Host ""

$patterns = @(
    "BUTLER_OS\.py",
    "TaskRunner\.runner_loop",
    "ComfyUI\\main\.py"
)

$procs = Get-CimInstance Win32_Process | Where-Object {
    $cmd = $_.CommandLine
    if([string]::IsNullOrWhiteSpace($cmd)){ return $false }

    foreach($p in $patterns){
        if($cmd -match $p){ return $true }
    }
    return $false
}

if($procs.Count -eq 0){
    OK "Butler Runtime already stopped."
}
else{
    foreach($proc in $procs){
        INFO "Stopping PID $($proc.ProcessId)"
        try{
            Stop-Process -Id $proc.ProcessId -Force -ErrorAction Stop
            OK "Stopped PID $($proc.ProcessId)"
        }
        catch{
            Write-Host "[SKIP] PID $($proc.ProcessId)" -ForegroundColor Yellow
        }
    }
}

Write-Host ""
Write-Host "Checking remaining Butler processes..."
$left = Get-CimInstance Win32_Process | Where-Object {
    $_.CommandLine -match "BUTLER_OS|TaskRunner\.runner_loop|ComfyUI\\main\.py"
}

if($left){
    Write-Host ""
    Write-Host "[WARNING] Remaining processes:" -ForegroundColor Yellow
    $left | Select-Object ProcessId,CommandLine | Format-Table -Auto
}
else{
    OK "All Butler Runtime processes stopped."
}

Pause
