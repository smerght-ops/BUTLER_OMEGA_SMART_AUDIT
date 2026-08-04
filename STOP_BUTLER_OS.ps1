[CmdletBinding()]
param([int]$GracefulTimeoutSeconds = 5)

$ErrorActionPreference = "Stop"
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$ProjectRoot = $PSScriptRoot
$StatePath = Join-Path $ProjectRoot "A_08_LOGS\runtime\active_session.json"

if (-not (Test-Path -LiteralPath $StatePath -PathType Leaf)) {
    Write-Host "BUTLER_RUNTIME_ALREADY_STOPPED"
    exit 0
}

try {
    $state = Get-Content -LiteralPath $StatePath -Raw -Encoding UTF8 | ConvertFrom-Json
}
catch {
    Write-Error "BLOCKED_INVALID_SESSION_STATE: $($_.Exception.Message)"
    exit 2
}

if ($state.schema -ne "butler.runtime-session.v1" -or [string]::IsNullOrWhiteSpace($state.session_id)) {
    Write-Error "BLOCKED_INVALID_SESSION_OWNERSHIP"
    exit 2
}

$failures = @()
foreach ($entry in @($state.processes)) {
    if (-not $entry.owned) { continue }
    $processInfo = Get-CimInstance Win32_Process -Filter "ProcessId = $($entry.pid)" -ErrorAction SilentlyContinue
    if ($null -eq $processInfo) { continue }
    if ([string]::IsNullOrWhiteSpace($processInfo.CommandLine) -or $processInfo.CommandLine -notmatch [regex]::Escape($entry.command_token)) {
        $failures += "PID_COMMAND_MISMATCH:$($entry.pid):$($entry.role)"
        continue
    }
    $process = Get-Process -Id $entry.pid -ErrorAction SilentlyContinue
    if ($null -eq $process) { continue }
    $process.CloseMainWindow() | Out-Null
    if (-not $process.WaitForExit($GracefulTimeoutSeconds * 1000)) {
        Stop-Process -Id $entry.pid -Force -ErrorAction SilentlyContinue
        $process = Get-Process -Id $entry.pid -ErrorAction SilentlyContinue
        if ($null -ne $process) { $failures += "STOP_TIMEOUT:$($entry.pid):$($entry.role)" }
    }
}

if ($failures.Count -gt 0) {
    Write-Error ("PARTIAL_STOP: " + ($failures -join ", "))
    exit 1
}

Remove-Item -LiteralPath $StatePath -Force
Write-Host "BUTLER_RUNTIME_STOPPED session=$($state.session_id)"
exit 0
