function Assert-LastExit {
    param(
        [string]$Description = "Native command"
    )

    if ($null -ne $global:LASTEXITCODE -and [int]$global:LASTEXITCODE -ne 0) {
        throw "[FATAL] $Description failed. ExitCode=$global:LASTEXITCODE"
    }
}

function Invoke-ButlerProtectedCommand {
    param(
        [Parameter(Mandatory=$true)][string]$Description,
        [Parameter(Mandatory=$true)][scriptblock]$Command
    )

    $ErrorActionPreference = "Stop"
    $global:LASTEXITCODE = 0

    Write-Host "[RUN] $Description" -ForegroundColor Yellow

    try {
        & $Command
        Assert-LastExit $Description
        Write-Host "[OK] $Description" -ForegroundColor Green
    }
    catch {
        Write-Host ""
        Write-Host "==================================================" -ForegroundColor Red
        Write-Host "[FATAL] BUTLER SAFETY GATE STOPPED EXECUTION" -ForegroundColor Red
        Write-Host "Step : $Description" -ForegroundColor Red
        Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
        Write-Host "NO FURTHER STEPS SHOULD BE EXECUTED" -ForegroundColor Red
        Write-Host "==================================================" -ForegroundColor Red
        throw
    }
}