#requires -Version 5.1
[CmdletBinding()]
param()

$ProjectRoot = Split-Path $PSScriptRoot -Parent

$ExcludedRoots = @(
    ".git",
    "A_00_LEGACY_ARCHIVE",
    "__pycache__"
)

$Patterns = @(
    "*.bak",
    "*.backup",
    "*.old",
    "*.copy",
    "*.tmp",
    "*.pyc",
    "*before_*",
    "*backup_*"
)

function Test-ExcludedPath {
    param([string]$FullName)

    $Relative = $FullName.Substring($ProjectRoot.Length).TrimStart("\")

    foreach ($RootName in $ExcludedRoots) {
        if ($Relative -eq $RootName -or
            $Relative.StartsWith("$RootName\", [System.StringComparison]::OrdinalIgnoreCase) -or
            $Relative -match "(^|\\)$([regex]::Escape($RootName))(\\|$)") {
            return $true
        }
    }

    return $false
}

$Candidates = foreach ($Pattern in $Patterns) {
    Get-ChildItem $ProjectRoot -Recurse -File -Filter $Pattern -Force `
        -ErrorAction SilentlyContinue |
    Where-Object { -not (Test-ExcludedPath $_.FullName) }
}

$Candidates = $Candidates |
    Sort-Object FullName -Unique |
    ForEach-Object {
        [pscustomobject]@{
            Chars = $_.FullName.Length
            Bytes = $_.Length
            Path  = $_.FullName.Substring($ProjectRoot.Length).TrimStart("\")
        }
    }

Write-Host "SANITARY ARCHIVE V2 — READ ONLY" -ForegroundColor Cyan
Write-Host "PROJECT    : $ProjectRoot"
Write-Host "CANDIDATES : $($Candidates.Count)"
Write-Host "CHANGES    : 0" -ForegroundColor Green
Write-Host ""

$Candidates |
    Sort-Object Chars -Descending |
    Select-Object -First 30 |
    Format-Table Chars,Bytes,Path -Wrap
