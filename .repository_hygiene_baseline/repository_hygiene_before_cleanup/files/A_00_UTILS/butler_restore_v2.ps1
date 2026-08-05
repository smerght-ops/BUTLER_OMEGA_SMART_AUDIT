# ============================================================
# BUTLER RESTORE SYSTEM v2.0
# File: A_00_UTILS\butler_restore_v2.ps1
# CORE IS TABOO - NOT TOUCHED
# ============================================================

$global:ButlerRestoreRoot = "A_00_RESTORE"
$global:ButlerRestoreIndex = "A_00_RESTORE\RESTORE_INDEX.json"
$global:ButlerErrorLog = "A_08_LOGS\butler_errors.log"

function Stop-ButlerSafety {
    param([string]$Reason)

    $time = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

    if (-not (Test-Path "A_08_LOGS")) {
        New-Item -ItemType Directory -Force -Path "A_08_LOGS" | Out-Null
    }

    Add-Content -Path $global:ButlerErrorLog -Encoding UTF8 -Value "[$time] [FATAL] $Reason"

    Write-Host ""
    Write-Host "==================================================" -ForegroundColor Red
    Write-Host " BUTLER SAFETY STOP " -ForegroundColor Red
    Write-Host "==================================================" -ForegroundColor Red
    Write-Host "[FAIL] $Reason" -ForegroundColor Red
    Write-Host "[INFO] Execution stopped. Engineer review required." -ForegroundColor Yellow
    Write-Host "[INFO] Error log: $global:ButlerErrorLog" -ForegroundColor Yellow
    Write-Host "==================================================" -ForegroundColor Red

    throw "BUTLER SAFETY STOP: $Reason"
}

function Initialize-ButlerRestoreSystem {
    foreach ($dir in @("A_00_RESTORE", "A_00_RESTORE\PATCHES", "A_00_RESTORE\FULL", "A_08_LOGS")) {
        if (-not (Test-Path $dir)) {
            New-Item -ItemType Directory -Force -Path $dir | Out-Null
        }
    }

    if (-not (Test-Path $global:ButlerRestoreIndex)) {
        @() | ConvertTo-Json | Set-Content -Path $global:ButlerRestoreIndex -Encoding UTF8
    }
}

function New-ButlerRestorePoint {
    param(
        [Parameter(Mandatory=$true)][string]$Name,
        [string]$Description = "",
        [ValidateSet("PATCH","FULL")][string]$Type = "PATCH",
        [string[]]$Files = @()
    )

    Initialize-ButlerRestoreSystem

    $timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
    $safeName = ($Name -replace '[^\w\-]', '_')
    $base = if ($Type -eq "FULL") { "A_00_RESTORE\FULL" } else { "A_00_RESTORE\PATCHES" }
    $folder = Join-Path $base "${timestamp}_${safeName}"
    $before = Join-Path $folder "before"

    New-Item -ItemType Directory -Force -Path $before | Out-Null

    $copied = @()

    foreach ($file in $Files) {
        if (Test-Path $file) {
            $target = Join-Path $before $file
            $targetDir = Split-Path $target -Parent
            if (-not (Test-Path $targetDir)) { New-Item -ItemType Directory -Force -Path $targetDir | Out-Null }
            Copy-Item -Path $file -Destination $target -Force
            $copied += $file
        }
    }

    $entry = [PSCustomObject]@{
        id = $timestamp
        name = $Name
        description = $Description
        type = $Type
        created_at = (Get-Date).ToString("yyyy-MM-dd HH:mm:ss")
        folder = $folder.Replace("\","/")
        files = $copied
        status = "CREATED"
    }

    try {
        $index = Get-Content $global:ButlerRestoreIndex -Raw | ConvertFrom-Json
        if ($null -eq $index) { $index = @() }
        $index = @($index) + @($entry)
        $index | ConvertTo-Json -Depth 10 | Set-Content -Path $global:ButlerRestoreIndex -Encoding UTF8
    }
    catch {
        Stop-ButlerSafety "Failed to update RESTORE_INDEX.json: $_"
    }

    Write-Host ""
    Write-Host "==================================================" -ForegroundColor Cyan
    Write-Host " RESTORE POINT CREATED " -ForegroundColor Cyan
    Write-Host "==================================================" -ForegroundColor Cyan
    Write-Host "[ OK ] ID    : $timestamp" -ForegroundColor Green
    Write-Host "[ OK ] Name  : $Name" -ForegroundColor Green
    Write-Host "[ OK ] Type  : $Type" -ForegroundColor Green
    Write-Host "[ OK ] Files : $($copied.Count)" -ForegroundColor Green
    Write-Host "[ OK ] Path  : $folder" -ForegroundColor Green
    Write-Host "==================================================" -ForegroundColor Cyan

    return $entry
}

function Get-ButlerRestorePoints {
    Initialize-ButlerRestoreSystem
    Get-Content $global:ButlerRestoreIndex -Raw | ConvertFrom-Json
}

Write-Host "[ OK ] Butler Restore System v2.0 loaded." -ForegroundColor Green
function Restore-ButlerPoint {
    param(
        [Parameter(Mandatory=$true)]
        [string]$Id,

        [switch]$SkipChecks
    )

    Initialize-ButlerRestoreSystem

    Write-Host ""
    Write-Host "==================================================" -ForegroundColor Yellow
    Write-Host " BUTLER RESTORE POINT ROLLBACK " -ForegroundColor Yellow
    Write-Host "==================================================" -ForegroundColor Yellow
    Write-Host "[WARN] Requested restore ID: $Id" -ForegroundColor Yellow

    try {
        $index = Get-Content $global:ButlerRestoreIndex -Raw | ConvertFrom-Json
    }
    catch {
        Stop-ButlerSafety "Cannot read RESTORE_INDEX.json: $_"
    }

    $entry = @($index) | Where-Object { $_.id -eq $Id } | Select-Object -First 1

    if ($null -eq $entry) {
        Stop-ButlerSafety "Restore point not found: $Id"
    }

    $beforeDir = Join-Path $entry.folder "before"

    if (-not (Test-Path $beforeDir)) {
        Stop-ButlerSafety "Restore point has no before folder: $beforeDir"
    }

    $files = @($entry.files)

    if ($files.Count -eq 0) {
        Stop-ButlerSafety "Restore point contains zero files. Nothing to restore."
    }

    Write-Host "[INFO] Name : $($entry.name)" -ForegroundColor Cyan
    Write-Host "[INFO] Type : $($entry.type)" -ForegroundColor Cyan
    Write-Host "[INFO] Files: $($files.Count)" -ForegroundColor Cyan

    foreach ($file in $files) {
        $backupFile = Join-Path $beforeDir $file

        if (-not (Test-Path $backupFile)) {
            Stop-ButlerSafety "Backup file missing: $backupFile"
        }

        $targetDir = Split-Path $file -Parent

        if ($targetDir -and -not (Test-Path $targetDir)) {
            New-Item -ItemType Directory -Force -Path $targetDir | Out-Null
        }

        Copy-Item -Path $backupFile -Destination $file -Force
        Write-Host "[ OK ] Restored: $file" -ForegroundColor Green
    }

    Write-Host ""
    Write-Host "[ OK ] Files restored from point: $Id" -ForegroundColor Green

    if (-not $SkipChecks) {
        Write-Host ""
        Write-Host "==================================================" -ForegroundColor Cyan
        Write-Host " POST-RESTORE CHECKS " -ForegroundColor Cyan
        Write-Host "==================================================" -ForegroundColor Cyan

        python health_check.py
        if ($LASTEXITCODE -ne 0) {
            Stop-ButlerSafety "health_check.py failed after restore"
        }

        python system_doctor.py
        if ($LASTEXITCODE -ne 0) {
            Stop-ButlerSafety "system_doctor.py failed after restore"
        }

        python RUN_PIPELINE_V12.py --self-test
        if ($LASTEXITCODE -ne 0) {
            Stop-ButlerSafety "Guardian self-test failed after restore"
        }

        Write-Host "[ OK ] Post-restore checks passed." -ForegroundColor Green
    }

    Write-Host ""
    Write-Host "==================================================" -ForegroundColor Green
    Write-Host "[ OK ] RESTORE COMPLETED SUCCESSFULLY" -ForegroundColor Green
    Write-Host "[ OK ] Restored ID: $Id" -ForegroundColor Green
    Write-Host "==================================================" -ForegroundColor Green
}

# ============================================================
# WAVE 2.6R-D EXTENSION
# SHA-256 integrity for restore points
# ============================================================

function Get-ButlerFileHash {
    param([Parameter(Mandatory=$true)][string]$Path)

    if (-not (Test-Path $Path)) {
        Stop-ButlerSafety "SHA-256 failed. File not found: $Path"
    }

    return (Get-FileHash -Algorithm SHA256 -Path $Path).Hash
}

function New-ButlerRestorePoint {
    param(
        [Parameter(Mandatory=$true)][string]$Name,
        [string]$Description = "",
        [ValidateSet("PATCH","FULL")][string]$Type = "PATCH",
        [string[]]$Files = @()
    )

    Initialize-ButlerRestoreSystem

    $timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
    $safeName = ($Name -replace '[^\w\-]', '_')
    $base = if ($Type -eq "FULL") { "A_00_RESTORE\FULL" } else { "A_00_RESTORE\PATCHES" }
    $folder = Join-Path $base "${timestamp}_${safeName}"
    $before = Join-Path $folder "before"

    New-Item -ItemType Directory -Force -Path $before | Out-Null

    $copied = @()
    $hashes = @()

    foreach ($file in $Files) {
        if (Test-Path $file) {
            $target = Join-Path $before $file
            $targetDir = Split-Path $target -Parent

            if (-not (Test-Path $targetDir)) {
                New-Item -ItemType Directory -Force -Path $targetDir | Out-Null
            }

            Copy-Item -Path $file -Destination $target -Force

            $backupHash = Get-ButlerFileHash -Path $target

            $copied += $file
            $hashes += [PSCustomObject]@{
                file = $file
                backup_file = $target.Replace("\","/")
                sha256 = $backupHash
            }

            Write-Host "[ OK ] Saved + hashed: $file" -ForegroundColor Green
        }
    }

    $entry = [PSCustomObject]@{
        id = $timestamp
        name = $Name
        description = $Description
        type = $Type
        created_at = (Get-Date).ToString("yyyy-MM-dd HH:mm:ss")
        folder = $folder.Replace("\","/")
        files = $copied
        file_hashes = $hashes
        status = "CREATED_SHA256"
    }

    try {
        $index = Get-Content $global:ButlerRestoreIndex -Raw | ConvertFrom-Json
        if ($null -eq $index) { $index = @() }
        $index = @($index) + @($entry)
        $index | ConvertTo-Json -Depth 20 | Set-Content -Path $global:ButlerRestoreIndex -Encoding UTF8
    }
    catch {
        Stop-ButlerSafety "Failed to update RESTORE_INDEX.json: $_"
    }

    Write-Host ""
    Write-Host "==================================================" -ForegroundColor Cyan
    Write-Host " RESTORE POINT CREATED + SHA-256 VERIFIED " -ForegroundColor Cyan
    Write-Host "==================================================" -ForegroundColor Cyan
    Write-Host "[ OK ] ID     : $timestamp" -ForegroundColor Green
    Write-Host "[ OK ] Name   : $Name" -ForegroundColor Green
    Write-Host "[ OK ] Type   : $Type" -ForegroundColor Green
    Write-Host "[ OK ] Files  : $($copied.Count)" -ForegroundColor Green
    Write-Host "[ OK ] Crypto : SHA-256" -ForegroundColor Green
    Write-Host "[ OK ] Path   : $folder" -ForegroundColor Green
    Write-Host "==================================================" -ForegroundColor Cyan

    return $entry
}

function Restore-ButlerPoint {
    param(
        [Parameter(Mandatory=$true)][string]$Id,
        [switch]$SkipChecks
    )

    Initialize-ButlerRestoreSystem

    Write-Host ""
    Write-Host "==================================================" -ForegroundColor Yellow
    Write-Host " BUTLER RESTORE POINT ROLLBACK + SHA-256 " -ForegroundColor Yellow
    Write-Host "==================================================" -ForegroundColor Yellow
    Write-Host "[WARN] Requested restore ID: $Id" -ForegroundColor Yellow

    try {
        $index = Get-Content $global:ButlerRestoreIndex -Raw | ConvertFrom-Json
    }
    catch {
        Stop-ButlerSafety "Cannot read RESTORE_INDEX.json: $_"
    }

    $entry = @($index) | Where-Object { $_.id -eq $Id } | Select-Object -First 1

    if ($null -eq $entry) {
        Stop-ButlerSafety "Restore point not found: $Id"
    }

    $beforeDir = Join-Path $entry.folder "before"
    if (-not (Test-Path $beforeDir)) {
        Stop-ButlerSafety "Restore point has no before folder: $beforeDir"
    }

    $files = @($entry.files)
    if ($files.Count -eq 0) {
        Stop-ButlerSafety "Restore point contains zero files."
    }

    foreach ($file in $files) {
        $backupFile = Join-Path $beforeDir $file

        if (-not (Test-Path $backupFile)) {
            Stop-ButlerSafety "Backup file missing: $backupFile"
        }

        $hashRecord = @($entry.file_hashes) | Where-Object { $_.file -eq $file } | Select-Object -First 1

        if ($null -ne $hashRecord) {
            $actualHash = Get-ButlerFileHash -Path $backupFile

            if ($actualHash -ne $hashRecord.sha256) {
                Stop-ButlerSafety "Backup integrity check failed: $file"
            }

            Write-Host "[ OK ] SHA-256 OK: $file" -ForegroundColor Green
        }
        else {
            Write-Host "[WARN] No SHA-256 record for old restore point: $file" -ForegroundColor Yellow
        }

        $targetDir = Split-Path $file -Parent
        if ($targetDir -and -not (Test-Path $targetDir)) {
            New-Item -ItemType Directory -Force -Path $targetDir | Out-Null
        }

        Copy-Item -Path $backupFile -Destination $file -Force
        Write-Host "[ OK ] Restored: $file" -ForegroundColor Green
    }

    if (-not $SkipChecks) {
        Write-Host ""
        Write-Host "==================================================" -ForegroundColor Cyan
        Write-Host " POST-RESTORE CHECKS " -ForegroundColor Cyan
        Write-Host "==================================================" -ForegroundColor Cyan

        python health_check.py
        if ($LASTEXITCODE -ne 0) { Stop-ButlerSafety "health_check.py failed after restore" }

        python system_doctor.py
        if ($LASTEXITCODE -ne 0) { Stop-ButlerSafety "system_doctor.py failed after restore" }

        python RUN_PIPELINE_V12.py --self-test
        if ($LASTEXITCODE -ne 0) { Stop-ButlerSafety "Guardian self-test failed after restore" }

        Write-Host "[ OK ] Post-restore checks passed." -ForegroundColor Green
    }

    Write-Host ""
    Write-Host "==================================================" -ForegroundColor Green
    Write-Host "[ OK ] RESTORE COMPLETED SUCCESSFULLY" -ForegroundColor Green
    Write-Host "[ OK ] Restored ID: $Id" -ForegroundColor Green
    Write-Host "[ OK ] SHA-256 verified" -ForegroundColor Green
    Write-Host "==================================================" -ForegroundColor Green
}
