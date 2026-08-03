@echo off
setlocal EnableDelayedExpansion
cd /d "%~dp0"
for /f "delims=" %%P in ('where python 2^>nul') do if not defined PYTHON_EXE set "PYTHON_EXE=%%P"
if not defined PYTHON_EXE (
  echo [FATAL] Official Python from START_BUTLER_OS.ps1 was not found in PATH.
  set "RC=2"
) else (
  echo [PYTHON] %PYTHON_EXE%
  "%PYTHON_EXE%" "A_99_TESTS\full_acceptance.py" --mode full
  set "RC=!ERRORLEVEL!"
)
echo.
echo FULL ACCEPTANCE EXIT CODE: !RC!
pause
exit /b !RC!
