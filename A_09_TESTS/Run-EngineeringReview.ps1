# -*- coding: utf-8 -*-
<#
.SYNOPSIS
    Run-EngineeringReview — официальный сценарий запуска инженерской ревизии Butler.

.DESCRIPTION
    Запускает EngineeringReviewDepartment через существующую архитектуру Butler:
        1. Импортирует модуль проверок напрямую (read-only).
        2. Выполняет полный цикл проверок.
        3. Формирует и выводит единый инженерный отчёт.

    НЕ изменяет файлы проекта — только анализирует и формирует отчёт.

.USAGE
    .\A_09_TESTS\Run-EngineeringReview.ps1
#>

[CmdletBinding()]
param()

$ErrorActionPreference = "Stop"
$ProjectRoot = $PSScriptRoot | Split-Path -Parent
$PythonExe = (Get-Content (Join-Path $ProjectRoot ".butler_python_path") -Raw).Trim()

Write-Host ""
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "  BUTLER ENGINEERING REVIEW v1.0" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

# Ensure the project root is in Python path
$env:PYTHONPATH = "$ProjectRoot;$env:PYTHONPATH"

try {
    & $PythonExe -c "from A_04_AGENTS.EngineeringReviewDepartment.checker import run_full_review, print_report; print_report(run_full_review())" 2>&1

    Write-Host ""
    Write-Host "--- Engineering Review Complete ---" -ForegroundColor Green
    Write-Host ""
}
catch {
    Write-Host "ERROR: Engineering review failed:" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    exit 1
}
