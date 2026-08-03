@echo off
title BUTLER OMEGA SMART - MAIN ENTRY POINT v4.15.3 (DYNAMIC + VISUAL)
color 0A
cd /d "%~dp0"
chcp 65001 >nul
set PYTHONIOENCODING=utf-8

cls
echo =====================================================
echo      BUTLER OMEGA SMART - MAIN ENTRY POINT
echo =====================================================
echo [ROOT] %CD%
echo.

:: =====================================================
:: [1/5] STATUS CENTER
:: =====================================================
powershell -Command "Write-Host ' [STATUS] ' -ForegroundColor White -BackgroundColor Blue -NoNewline; Write-Host ' [1/5] Снятие слепка системы из Status Center...' -ForegroundColor Cyan"
echo.
if exist ".\STATUS_CENTER_READONLY.ps1" (
    powershell -NoProfile -ExecutionPolicy Bypass -File ".\STATUS_CENTER_READONLY.ps1"
) else (
    color 0C
    echo [CRITICAL] STATUS_CENTER_READONLY.ps1 not found
    pause
    exit /b 1
)

echo.
echo =====================================================
echo [2/5] PASSPORT & GUARDIAN CHECK
echo =====================================================
powershell -Command "Write-Host ' [STATUS] ' -ForegroundColor White -BackgroundColor Blue -NoNewline; Write-Host ' [2/5] Проверка паспорта и Стража Памяти...' -ForegroundColor Cyan"
if exist ".\A_07_CONFIG\project_passport.json" (
    echo [OK] Passport detected
) else (
    color 0C
    echo [CRITICAL] project_passport.json not found
    pause
    exit /b 1
)

:: Проверка Стража
python .\A_01_CORE\memory_guardian.py --self-test
if %errorlevel% neq 0 (
    color 0C
    echo.
    powershell -Command "Write-Host ' [FATAL] ' -ForegroundColor White -BackgroundColor Red -NoNewline; Write-Host ' MEMORY GUARDIAN FAILED! Запуск блокирован.' -ForegroundColor Red"
    pause
    exit /b 1
)
powershell -Command "Write-Host ' [SUCCESS] ' -ForegroundColor White -BackgroundColor Green -NoNewline; Write-Host ' Контроль инвариантов ядра пройден.' -ForegroundColor Green"

echo.
echo =====================================================
echo [3/5] OLLAMA ENGINE & MODEL CHECK
echo =====================================================
powershell -Command "Write-Host ' [STATUS] ' -ForegroundColor White -BackgroundColor Blue -NoNewline; Write-Host ' [3/5] Верификация окружения Ollama Engine...' -ForegroundColor Cyan"

tasklist | find /i "ollama.exe" >nul
if errorlevel 1 (
    powershell -NoProfile -Command "if(-not (Test-NetConnection 127.0.0.1 -Port 11434 -WarningAction SilentlyContinue).TcpTestSucceeded){Start-Process 'C:\Users\KOS\AppData\Local\Programs\Ollama\ollama.exe' -ArgumentList 'serve'; Start-Sleep 5}"
)

:: Динамический цикл ожидания с синей строкой состояния
set OLLAMA_WAIT=0
:WAIT_OLLAMA
powershell -NoProfile -Command ^
"exit(-not (Test-NetConnection 127.0.0.1 -Port 11434 -WarningAction SilentlyContinue).TcpTestSucceeded)"

if %errorlevel% equ 0 goto OLLAMA_OK
set /a OLLAMA_WAIT+=1
if %OLLAMA_WAIT% geq 15 goto OLLAMA_FAIL
powershell -Command "Write-Host ' [WAITING] ' -ForegroundColor White -BackgroundColor Blue -NoNewline; Write-Host ' Ожидание ответа сокета Ollama (порт 11434)... [%OLLAMA_WAIT%/15]' -ForegroundColor Yellow"
timeout /t 2 >nul
goto WAIT_OLLAMA

:OLLAMA_FAIL
color 0C
echo.
powershell -Command "Write-Host ' [FATAL] ' -ForegroundColor White -BackgroundColor Red -NoNewline; Write-Host ' OLLAMA PORT 11434 OFFLINE! Превышено время ожидания.' -ForegroundColor Red"
pause
exit /b 1

:OLLAMA_OK
powershell -Command "Write-Host ' [ONLINE] ' -ForegroundColor White -BackgroundColor Green -NoNewline; Write-Host ' Ollama успешно отвечает на порту 11434.' -ForegroundColor Green"

:: Проверка пула моделей
echo.
echo Локальные модели в рантайме:
ollama list
echo.

echo.
echo =====================================================
echo [4/5] COMFYUI CHECK
echo =====================================================
powershell -Command "Write-Host ' [STATUS] ' -ForegroundColor White -BackgroundColor Blue -NoNewline; Write-Host ' [4/5] Верификация генеративного моста ComfyUI...' -ForegroundColor Cyan"

powershell -NoProfile -Command "if(-not (Test-NetConnection 127.0.0.1 -Port 8188 -WarningAction SilentlyContinue).TcpTestSucceeded){Start-Process 'D:\AI_Studio\ComfyUI_windows_portable\python_embeded\python.exe' -ArgumentList '-s ComfyUI\main.py --windows-standalone-build' -WorkingDirectory 'D:\AI_Studio\ComfyUI_windows_portable' -WindowStyle Minimized; Start-Sleep 5}"

:: Динамический цикл ожидания ComfyUI с синей строкой состояния
set COMFY_WAIT=0
:WAIT_COMFY
powershell -NoProfile -Command ^
"exit(-not (Test-NetConnection 127.0.0.1 -Port 8188 -WarningAction SilentlyContinue).TcpTestSucceeded)"

if %errorlevel% equ 0 goto COMFY_OK
set /a COMFY_WAIT+=1
if %COMFY_WAIT% geq 15 goto COMFY_FAIL
powershell -Command "Write-Host ' [WAITING] ' -ForegroundColor White -BackgroundColor Blue -NoNewline; Write-Host ' Ожидание инициализации API ComfyUI (порт 8188)... [%COMFY_WAIT%/15]' -ForegroundColor Yellow"
timeout /t 2 >nul
goto WAIT_COMFY

:COMFY_FAIL
color 0C
echo.
powershell -Command "Write-Host ' [FATAL] ' -ForegroundColor White -BackgroundColor Red -NoNewline; Write-Host ' COMFYUI PORT 8188 OFFLINE! Превышено время ожидания.' -ForegroundColor Red"
pause
exit /b 1

:COMFY_OK
powershell -Command "Write-Host ' [ONLINE] ' -ForegroundColor White -BackgroundColor Green -NoNewline; Write-Host ' Мост ComfyUI успешно поднят на порту 8188!' -ForegroundColor Green"

echo.
echo =====================================================
echo [5/5] START CHAT ROUTER
echo =====================================================
powershell -Command "Write-Host ' [LAUNCH] ' -ForegroundColor White -BackgroundColor Green -NoNewline; Write-Host ' Запуск ядра операционной системы БАТЛЕРА...' -ForegroundColor Green"
echo.
python .\BUTLER_OS.py

if %errorlevel% neq 0 (
    color 0C
    echo.
    echo [CRITICAL] CHAT ROUTER FAILED
    pause
    exit /b 1
)

echo.
echo =====================================================
echo [SUCCESS] SESSION CLOSED NORMALLY
echo =====================================================
pause