@echo off
cd /d "%~dp0"
powershell -NoProfile -ExecutionPolicy Bypass -File ".\STOP_BUTLER_OS.ps1"
pause
