param(
    [string]$Root = (Resolve-Path ".").Path,
    [string]$RunId = (Get-Date -Format "yyyyMMdd_HHmmss")
)

$ErrorActionPreference = "Stop"

$RootPath = (Resolve-Path -LiteralPath $Root).Path
$ArchiveRoot = Join-Path $RootPath "A_00_LEGACY_ARCHIVE"
$ArchiveDir = Join-Path $ArchiveRoot "${RunId}_SANITARY_ARCHIVE"
$PayloadDir = Join-Path $ArchiveDir "payload"
$ManifestPath = Join-Path $ArchiveDir "manifest.json"
$MovedCsv = Join-Path $ArchiveDir "moved_files.csv"
$FailureCsv = Join-Path $ArchiveDir "failures.csv"

New-Item -ItemType Directory -Force -Path $PayloadDir | Out-Null

$protectedExact = @(
    ".git",
    "A_00_LEGACY_ARCHIVE",
    "A_01_CORE",
    "A_02_MANAGERS",
    "A_03_ORCHESTRATION",
    "A_04_AGENTS",
    "A_05_STORAGE",
    "A_07_CONFIG",
    "A_07_MEMORY",
    "BUTLER_OS.py",
    "START_BUTLER_OS.ps1"
)

$explicitDirs = @(
    "A_00_ARCHIVE_BACKUPS",
    "A_00_ARCHIVE_SCRIPTS",
    "A_00_BACKUPS",
    "A_00_HISTORY",
    "A_00_SNAPSHOTS",
    "A_01_CORE_BACKUP",
    "A_02_MANAGERS_BACKUP",
    "A_04_AGENTS_BACKUP",
    "STABLE_SNAPSHOTS",
    "A_00_ARCHITECTURE\SNAPSHOTS",
    "A_00_HEALER_UNIT\backups",
    "A_00_RESTORE\SEARCH_ENGINE_BACKUPS",
    "A_04_AGENTS\DocumentsDepartment.BAK_20260703_124909",
    "A_04_AGENTS\ProjectDocumentationDepartment\Core_BACKUP_UTF8SIG",
    "A_07_MEMORY\memory_backups"
)

$moved = New-Object System.Collections.Generic.List[object]
$failures = New-Object System.Collections.Generic.List[object]
$plannedRoots = New-Object System.Collections.Generic.List[string]

function Get-RelativePath {
    param([string]$FullPath)
    $rootWithSep = $RootPath.TrimEnd("\") + "\"
    if ($FullPath.StartsWith($rootWithSep, [StringComparison]::OrdinalIgnoreCase)) {
        return $FullPath.Substring($rootWithSep.Length)
    }
    return $FullPath
}

function Is-ProtectedRel {
    param([string]$Rel)
    $clean = $Rel.Trim("\")
    foreach ($item in $protectedExact) {
        if ($clean.Equals($item, [StringComparison]::OrdinalIgnoreCase)) {
            return $true
        }
    }
    return $false
}

function Is-UnderArchive {
    param([string]$FullPath)
    return $FullPath.StartsWith($ArchiveRoot, [StringComparison]::OrdinalIgnoreCase)
}

function Is-UnderPlannedRoot {
    param([string]$FullPath)
    foreach ($root in $plannedRoots) {
        $prefix = $root.TrimEnd("\") + "\"
        if ($FullPath.StartsWith($prefix, [StringComparison]::OrdinalIgnoreCase)) {
            return $true
        }
    }
    return $false
}

function Get-UniqueDestination {
    param([string]$Rel)
    $dest = Join-Path $PayloadDir $Rel
    if (-not (Test-Path -LiteralPath $dest)) {
        return $dest
    }

    $parent = Split-Path -Parent $dest
    $leaf = Split-Path -Leaf $dest
    $stamp = Get-Date -Format "yyyyMMdd_HHmmss_fff"
    return (Join-Path $parent "$leaf.moved_$stamp")
}

function Move-Candidate {
    param(
        [string]$FullPath,
        [string]$Category
    )

    try {
        if (-not (Test-Path -LiteralPath $FullPath)) {
            return
        }

        $resolved = (Resolve-Path -LiteralPath $FullPath).Path
        if (Is-UnderArchive $resolved) {
            return
        }

        $rel = Get-RelativePath $resolved
        if (Is-ProtectedRel $rel) {
            return
        }

        $dest = Get-UniqueDestination $rel
        $destParent = Split-Path -Parent $dest
        New-Item -ItemType Directory -Force -Path $destParent | Out-Null

        Move-Item -LiteralPath $resolved -Destination $dest

        $moved.Add([pscustomobject]@{
            category = $Category
            source = $rel
            destination = Get-RelativePath $dest
            moved_at = (Get-Date).ToString("s")
        })
    }
    catch {
        $failures.Add([pscustomobject]@{
            category = $Category
            source = Get-RelativePath $FullPath
            error = $_.Exception.Message
        })
    }
}

foreach ($rel in $explicitDirs) {
    $path = Join-Path $RootPath $rel
    if (Test-Path -LiteralPath $path) {
        $resolved = (Resolve-Path -LiteralPath $path).Path
        $plannedRoots.Add($resolved)
    }
}

foreach ($rel in $explicitDirs) {
    $path = Join-Path $RootPath $rel
    if (Test-Path -LiteralPath $path) {
        Move-Candidate -FullPath $path -Category "explicit_legacy_dir"
    }
}

$cacheDirs = Get-ChildItem -LiteralPath $RootPath -Directory -Recurse -Force -ErrorAction SilentlyContinue |
    Where-Object {
        $_.Name -eq "__pycache__" -and
        -not (Is-UnderArchive $_.FullName) -and
        -not (Is-UnderPlannedRoot $_.FullName)
    }

foreach ($dir in $cacheDirs) {
    Move-Candidate -FullPath $dir.FullName -Category "python_cache_dir"
}

$backupPattern = "(?i)(\.bak|bak_|backup|before|stable_|_stable|recovery_template|ansi_bak)"
$backupFiles = Get-ChildItem -LiteralPath $RootPath -File -Recurse -Force -ErrorAction SilentlyContinue |
    Where-Object {
        -not (Is-UnderArchive $_.FullName) -and
        -not (Is-UnderPlannedRoot $_.FullName) -and
        $_.Name -match $backupPattern
    }

foreach ($file in $backupFiles) {
    Move-Candidate -FullPath $file.FullName -Category "legacy_backup_file"
}

$bytecodeFiles = Get-ChildItem -LiteralPath $RootPath -File -Recurse -Force -ErrorAction SilentlyContinue |
    Where-Object {
        -not (Is-UnderArchive $_.FullName) -and
        -not (Is-UnderPlannedRoot $_.FullName) -and
        ($_.Extension -in @(".pyc", ".pyo"))
    }

foreach ($file in $bytecodeFiles) {
    Move-Candidate -FullPath $file.FullName -Category "python_bytecode_file"
}

$moved | Export-Csv -LiteralPath $MovedCsv -NoTypeInformation -Encoding UTF8
$failures | Export-Csv -LiteralPath $FailureCsv -NoTypeInformation -Encoding UTF8

$summary = [ordered]@{
    run_id = $RunId
    root = $RootPath
    archive_dir = $ArchiveDir
    moved_count = $moved.Count
    failure_count = $failures.Count
    protected = $protectedExact
    explicit_dirs = $explicitDirs
    categories = ($moved | Group-Object category | ForEach-Object {
        [ordered]@{
            category = $_.Name
            count = $_.Count
        }
    })
}

($summary | ConvertTo-Json -Depth 8) | Set-Content -LiteralPath $ManifestPath -Encoding UTF8

Write-Host "SANITARY ARCHIVE COMPLETE"
Write-Host "Archive:" $ArchiveDir
Write-Host "Moved:" $moved.Count
Write-Host "Failures:" $failures.Count
Write-Host "Manifest:" $ManifestPath
Write-Host "Moved CSV:" $MovedCsv
Write-Host "Failures CSV:" $FailureCsv
