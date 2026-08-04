[CmdletBinding()]
param(
    [switch]$ValidateOnly,
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$ButlerArgs
)

$ErrorActionPreference = "Stop"
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$ProjectRoot = $PSScriptRoot
Set-Location -LiteralPath $ProjectRoot
$StateDirectory = Join-Path $ProjectRoot "A_08_LOGS\runtime"
$StatePath = Join-Path $StateDirectory "active_session.json"
$Utf8NoBom = [System.Text.UTF8Encoding]::new($false)

function Write-State([hashtable]$State) {
    [System.IO.Directory]::CreateDirectory($StateDirectory) | Out-Null
    $json = $State | ConvertTo-Json -Depth 8
    [System.IO.File]::WriteAllText($StatePath, $json + [Environment]::NewLine, $Utf8NoBom)
}

function Resolve-ButlerPython {
    $configured = Join-Path $ProjectRoot ".butler_python_path"
    if (Test-Path -LiteralPath $configured -PathType Leaf) {
        $candidate = (Get-Content -LiteralPath $configured -Raw).Trim()
        if (Test-Path -LiteralPath $candidate -PathType Leaf) {
            & $candidate -c "import requests,yaml,fitz" 2>$null
            if ($LASTEXITCODE -eq 0) { return (Resolve-Path -LiteralPath $candidate).Path }
        }
    }
    if ($env:BUTLER_PYTHON -and (Test-Path -LiteralPath $env:BUTLER_PYTHON -PathType Leaf)) {
        & $env:BUTLER_PYTHON -c "import requests,yaml,fitz" 2>$null
        if ($LASTEXITCODE -eq 0) { return (Resolve-Path -LiteralPath $env:BUTLER_PYTHON).Path }
    }
    throw "CANONICAL_PYTHON_UNAVAILABLE"
}

function Test-ServicePort([int]$Port) {
    return Test-NetConnection 127.0.0.1 -Port $Port -InformationLevel Quiet -WarningAction SilentlyContinue
}

function Stop-OwnedProcesses([hashtable]$State) {
    foreach ($entry in @($State.processes)) {
        if (-not $entry.owned) { continue }
        $process = Get-Process -Id $entry.pid -ErrorAction SilentlyContinue
        if ($null -eq $process) { continue }
        $process.CloseMainWindow() | Out-Null
        if (-not $process.WaitForExit(3000)) {
            Stop-Process -Id $entry.pid -Force -ErrorAction SilentlyContinue
        }
    }
}

$PythonExe = Resolve-ButlerPython
$SessionId = [guid]::NewGuid().ToString("N")
$state = @{
    schema = "butler.runtime-session.v1"
    session_id = $SessionId
    project_root = $ProjectRoot
    launcher_pid = $PID
    created_at = [DateTime]::UtcNow.ToString("o")
    status = "STARTING"
    processes = @()
    external_services = @(
        @{ name = "Ollama"; mode = $(if (Test-ServicePort 11434) { "EXTERNAL_PREEXISTING" } else { "UNAVAILABLE" }) },
        @{ name = "ComfyUI"; mode = $(if (Test-ServicePort 8188) { "EXTERNAL_PREEXISTING" } else { "UNAVAILABLE" }) },
        @{ name = "LM Studio"; mode = "NOT_REQUIRED" },
        @{ name = "System Guardian"; mode = "NOT_REQUIRED" }
    )
}

if (Test-Path -LiteralPath $StatePath) {
    throw "ACTIVE_BUTLER_SESSION_EXISTS: $StatePath"
}
Write-State $state

if ($ValidateOnly) {
    $state.status = "VALIDATED"
    Write-State $state
    Write-Host "BUTLER_RUNTIME_VALIDATED session=$SessionId python=$PythonExe"
    Remove-Item -LiteralPath $StatePath -Force
    exit 0
}

try {
    $runner = Start-Process -FilePath $PythonExe -ArgumentList @("-m", "A_02_MANAGERS.TaskRunner.runner_loop") -WorkingDirectory $ProjectRoot -WindowStyle Hidden -PassThru
    $state.processes += @{ role = "RunnerLoop"; pid = $runner.Id; command_token = "A_02_MANAGERS.TaskRunner.runner_loop"; owned = $true }
    Write-State $state

    $butlerArguments = @(".\BUTLER_OS.py") + @($ButlerArgs | Where-Object { $null -ne $_ -and $_ -ne "" })
    $butler = Start-Process -FilePath $PythonExe -ArgumentList $butlerArguments -WorkingDirectory $ProjectRoot -WindowStyle Hidden -PassThru
    $state.processes += @{ role = "ButlerOS"; pid = $butler.Id; command_token = "BUTLER_OS.py"; owned = $true }
    $state.status = "RUNNING"
    Write-State $state
    Write-Host "BUTLER_RUNTIME_STARTED session=$SessionId butler_pid=$($butler.Id) runner_pid=$($runner.Id)"
    $butler.WaitForExit()
    $exitCode = $butler.ExitCode
    $state.status = "STOPPING"
    Write-State $state
    Stop-OwnedProcesses $state
    Remove-Item -LiteralPath $StatePath -Force
    exit $exitCode
}
catch {
    $state.status = "PARTIAL_START_FAILED"
    $state.error = $_.Exception.Message
    Write-State $state
    Stop-OwnedProcesses $state
    Remove-Item -LiteralPath $StatePath -Force -ErrorAction SilentlyContinue
    throw
}
