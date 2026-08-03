@echo off
cd /d "%~dp0"
powershell -NoProfile -ExecutionPolicy Bypass -File ".\START_BUTLER_OS.ps1" %*
exit /b %ERRORLEVEL%
