$Host.UI.RawUI.WindowTitle = "BUTLER OMEGA SMART - GREEN START"
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$ButlerArgs = @($args)
$OnceMode = $ButlerArgs.Count -gt 0 -and $ButlerArgs[0] -eq "--once"
Set-Location $PSScriptRoot
$env:PYTHONIOENCODING = "utf-8"

function OK($m){ Write-Host "[OK] $m" -ForegroundColor Green }
function INFO($m){ Write-Host "[..] $m" -ForegroundColor Cyan }
function WARN($m){ Write-Host "[!!] $m" -ForegroundColor Yellow }
function FAIL($m){ Write-Host "[FATAL] $m" -ForegroundColor Red; exit 1 }

function Resolve-ButlerPython {
    $checked = [System.Collections.Generic.List[string]]::new()
    $candidates = [System.Collections.Generic.List[string]]::new()
    if($env:BUTLER_PYTHON){ $candidates.Add($env:BUTLER_PYTHON) }
    if($env:VIRTUAL_ENV){ $candidates.Add((Join-Path $env:VIRTUAL_ENV "Scripts\python.exe")) }
    $pathPython = Get-Command python.exe -ErrorAction SilentlyContinue
    if($pathPython){ $candidates.Add($pathPython.Source) }
    $pyLauncher = Get-Command py.exe -ErrorAction SilentlyContinue
    if($pyLauncher){
        try {
            $resolved = & $pyLauncher.Source -3 -c "import sys; print(sys.executable)" 2>$null
            if($LASTEXITCODE -eq 0 -and $resolved){ $candidates.Add(($resolved | Select-Object -First 1).Trim()) }
        } catch {}
    }
    $candidates.Add((Join-Path $env:LOCALAPPDATA "Python\bin\python.exe"))
    $candidates.Add((Join-Path $env:LOCALAPPDATA "Programs\Python\Python312\python.exe"))
    $candidates.Add((Join-Path $env:USERPROFILE ".cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"))
    foreach($candidate in ($candidates | Select-Object -Unique)){
        if([string]::IsNullOrWhiteSpace($candidate)){ continue }
        $checked.Add($candidate)
        if(-not (Test-Path -LiteralPath $candidate -PathType Leaf)){ continue }
        try {
            # A bare interpreter is not enough: Codex can expose a bundled Python
            # which has no Butler runtime dependencies.  Validate the dependency
            # used by the dispatcher/departments before selecting the candidate.
            & $candidate -c "import sys, requests; raise SystemExit(0 if sys.version_info >= (3, 10) else 1)" 2>$null
            if($LASTEXITCODE -eq 0){ return (Resolve-Path -LiteralPath $candidate).Path }
        } catch {}
    }
    Write-Host "[FATAL] Working Python 3.10+ was not found." -ForegroundColor Red
    Write-Host "Checked locations:" -ForegroundColor Red
    foreach($item in $checked){ Write-Host "  - $item" -ForegroundColor Red }
    exit 1
}

function Wait-Port($Name, $Port, $MaxSeconds){
    $limit = [int]($MaxSeconds / 2)
    for($i=1; $i -le $limit; $i++){
        if(Test-NetConnection 127.0.0.1 -Port $Port -InformationLevel Quiet -WarningAction SilentlyContinue){
            OK "$Name ONLINE on port $Port"
            return
        }
        INFO "Waiting $Name... [$i/$limit]"
        Start-Sleep -Seconds 2
    }
    FAIL "$Name timeout on port $Port"
}

Clear-Host
$PythonExe = Resolve-ButlerPython
$env:BUTLER_RESOLVED_PYTHON = $PythonExe
Write-Host "=====================================================" -ForegroundColor Green
Write-Host "      BUTLER OMEGA SMART - GREEN START BUTTON        " -ForegroundColor Green
Write-Host "=====================================================" -ForegroundColor Green
Write-Host "[ROOT] $PWD"
Write-Host "[PYTHON] $PythonExe"
Write-Host "[PID] Launcher PowerShell: $PID"
Write-Host ""

INFO "1/6 STATUS CENTER"
if(Test-Path ".\STATUS_CENTER_READONLY.ps1"){
    powershell -NoProfile -ExecutionPolicy Bypass -File ".\STATUS_CENTER_READONLY.ps1"
} else {
    WARN "STATUS_CENTER_READONLY.ps1 not found"
}

INFO "2/6 PASSPORT + MEMORY GUARDIAN"
if(-not (Test-Path ".\A_07_CONFIG\project_passport.json")){
    FAIL "project_passport.json not found"
}
OK "Passport detected"

$Guardian = & $PythonExe -m A_01_CORE.memory_guardian --self-test 2>&1 | Out-String
Write-Host $Guardian
if($LASTEXITCODE -ne 0 -or $Guardian.Contains("FATAL LOCKDOWN")){
    FAIL "Memory Guardian blocked start"
}
OK "Memory Guardian passed"

INFO "3/6 OLLAMA"
if(-not (Test-NetConnection 127.0.0.1 -Port 11434 -InformationLevel Quiet -WarningAction SilentlyContinue)){
    Start-Process "C:\Users\KOS\AppData\Local\Programs\Ollama\ollama.exe" -ArgumentList "serve" -WindowStyle Minimized
}
Wait-Port "Ollama" 11434 60

INFO "4/6 COMFYUI"
if(-not (Test-NetConnection 127.0.0.1 -Port 8188 -InformationLevel Quiet -WarningAction SilentlyContinue)){
    Start-Process "D:\AI_Studio\ComfyUI_windows_portable\python_embeded\python.exe" -ArgumentList "-s ComfyUI\main.py --windows-standalone-build" -WorkingDirectory "D:\AI_Studio\ComfyUI_windows_portable" -WindowStyle Minimized
}
Wait-Port "ComfyUI" 8188 120

INFO "5/6 SYSTEM GUARDIAN"
if(Test-Path ".\A_01_CORE\system_guardian.py"){
    & $PythonExe ".\A_01_CORE\system_guardian.py"
} else {
    WARN "system_guardian.py not found"
}

INFO "6/6 START BUTLER OS"
if(-not (Test-Path ".\BUTLER_OS.py")){
    FAIL "BUTLER_OS.py not found"
}

Write-Host "=====================================================" -ForegroundColor Green
Write-Host "              STARTING BUTLER OS                     " -ForegroundColor Green
Write-Host "=====================================================" -ForegroundColor Green

INFO "Starting RunnerLoop"

$RunnerProcess = Start-Process -FilePath $PythonExe `
    -ArgumentList "-m A_02_MANAGERS.TaskRunner.runner_loop" `
    -WorkingDirectory $PSScriptRoot `
    -WindowStyle Minimized `
    -PassThru
Write-Host "[PID] RunnerLoop: $($RunnerProcess.Id)"

Start-Sleep -Seconds 2

try {
    & $PythonExe ".\BUTLER_OS.py" @ButlerArgs
    $ButlerExitCode = $LASTEXITCODE
} finally {
    if($RunnerProcess -and -not $RunnerProcess.HasExited){
        Stop-Process -Id $RunnerProcess.Id -Force -ErrorAction SilentlyContinue
        Write-Host "[OK] RunnerLoop stopped: $($RunnerProcess.Id)"
    }
}

Write-Host ""
OK "Butler session closed"
exit $ButlerExitCode
