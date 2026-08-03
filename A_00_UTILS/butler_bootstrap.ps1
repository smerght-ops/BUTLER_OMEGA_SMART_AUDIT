# ============================================================
# BUTLER BOOTSTRAP v1.0
# Loads Butler development environment
# ============================================================

Write-Host ""
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "        BUTLER OMEGA DEVELOPMENT ENV" -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan

# -----------------------------
# Load UI
# -----------------------------

if (Test-Path ".\A_00_UTILS\butler_ui.ps1") {
    . .\A_00_UTILS\butler_ui.ps1
    Write-Host "✓ Butler UI loaded" -ForegroundColor Green
}
else {
    Write-Host "⚠ Butler UI not found" -ForegroundColor Yellow
}

# -----------------------------
# Load Helpers
# -----------------------------

if (Test-Path ".\A_00_UTILS\butler_helpers.ps1") {
    Remove-Variable ButlerHelpersLoaded -Scope Global -ErrorAction SilentlyContinue
    . .\A_00_UTILS\butler_helpers.ps1
    Write-Host "✓ Butler Helpers loaded" -ForegroundColor Green
}
else {
    Write-Host "⚠ Butler Helpers not found" -ForegroundColor Yellow
}

# -----------------------------
# Environment info
# -----------------------------

Write-Host ""
Write-Host "Working Directory :" -NoNewline
Write-Host " $(Get-Location)" -ForegroundColor DarkGray

Write-Host "PowerShell Version:" -NoNewline
Write-Host " $($PSVersionTable.PSVersion)" -ForegroundColor DarkGray

# -----------------------------
# Python check
# -----------------------------

try {
    $pythonVersion = python --version 2>&1
    Write-Host "Python           :" -NoNewline
    Write-Host " $pythonVersion" -ForegroundColor DarkGray
}
catch {
    Write-Host "Python           : NOT FOUND" -ForegroundColor Red
}

# -----------------------------
# Git check
# -----------------------------

try {
    $gitVersion = git --version 2>&1
    Write-Host "Git              :" -NoNewline
    Write-Host " $gitVersion" -ForegroundColor DarkGray
}
catch {
    Write-Host "Git              : NOT FOUND" -ForegroundColor Yellow
}

# -----------------------------
# Ready
# -----------------------------

Write-Host ""
Write-Host "==================================================" -ForegroundColor Green
Write-Host "✓ Environment Ready" -ForegroundColor Green
Write-Host "✓ Progress Enabled" -ForegroundColor Green
Write-Host "✓ UI Enabled" -ForegroundColor Green
Write-Host "✓ Core Untouched" -ForegroundColor Green
Write-Host "==================================================" -ForegroundColor Green