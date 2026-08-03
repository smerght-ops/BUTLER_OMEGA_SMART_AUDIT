@echo off
title BUTLER OMEGA SMART :: LAUNCHER
chcp 65001 > nul
cls

echo ==================================================
echo BUTLER OMEGA SMART :: START
echo ==================================================
echo.

if not exist .\STATUS_CENTER_READONLY.ps1 (
    echo [OSHIBKA] STATUS_CENTER_READONLY.ps1 ne nayden!
    pause
    exit /b 1
)

powershell -NoProfile -ExecutionPolicy Bypass -File .\STATUS_CENTER_READONLY.ps1

echo.
echo ==================================================
echo [VNIMANIE] Prover' pokazaniya priborov vyshe.
echo Esli v OBSERVATIONS gorit REJECTED - ne zapuskay Runtime bez proverki.
echo ==================================================
echo.
echo Nazhmi lyubuyu klavishu dlya perehoda v Menyu Upravleniya Batlera...
pause > nul

cls

if exist .\butler_menu.ps1 (
    powershell -NoProfile -ExecutionPolicy Bypass -File .\butler_menu.ps1
) else (
    echo [OSHIBKA] butler_menu.ps1 ne nayden v tekushchey direktorii!
    pause
    exit /b 1
)
