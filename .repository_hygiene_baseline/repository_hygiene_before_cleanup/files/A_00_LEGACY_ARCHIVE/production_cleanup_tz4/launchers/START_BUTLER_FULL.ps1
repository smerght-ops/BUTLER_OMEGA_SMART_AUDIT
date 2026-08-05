[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$env:PYTHONUTF8="1"
$Host.UI.RawUI.WindowTitle = "BUTLER OMEGA CHAT ROUTER"

$Root = "C:\Users\KOS\Desktop\Butler_Agent\BUTLER_OMEGA"
$OutputFolder = "' + $OutputFolder + '"
Set-Location $Root
if (!(Test-Path $OutputFolder)) { New-Item -ItemType Directory -Force -Path $OutputFolder }

Clear-Host
Write-Host "======================================================================" -ForegroundColor DarkCyan
Write-Host "                     BUTLER OMEGA — FULL AUTO CHAT                     " -ForegroundColor Cyan
Write-Host "======================================================================" -ForegroundColor DarkCyan

# 1. Проверка Ollama
Write-Host "[1/3] Проверка Ollama..." -ForegroundColor Yellow
try {
    Invoke-RestMethod "http://127.0.0.1:11434/api/tags" -TimeoutSec 3 | Out-Null
    Write-Host "[OK] Ollama ONLINE" -ForegroundColor Green
}
catch {
    Write-Host "[INFO] Ollama не отвечает. Запускаю ollama serve..." -ForegroundColor Yellow
    Start-Process -FilePath "ollama" -ArgumentList "serve" -WindowStyle Minimized
    Start-Sleep -Seconds 5
}

# 2. Проверка и запуск ComfyUI
Write-Host "[2/3] Проверка ComfyUI..." -ForegroundColor Yellow
if (-not (Get-Process | Where-Object { $_.Path -eq "' + $ComfyUI + '" })) {
    Write-Host "[INFO] ComfyUI не запущен. Стартуем..." -ForegroundColor Yellow
    Start-Process -FilePath "' + $ComfyUI + '" -WindowStyle Normal
    Start-Sleep -Seconds 15
} else {
    Write-Host "[OK] ComfyUI уже запущен." -ForegroundColor Green
}

# 3. Запуск чата с автогенерацией
Write-Host "[3/3] Запуск интерактивного чата..." -ForegroundColor Yellow
Write-Host "Команды 'нарисуй ...' будут автоматически запускать генерацию в ComfyUI" -ForegroundColor Cyan

# Устанавливаем переменную окружения для автоматической генерации
$env:BUTLER_OUTPUT="$OutputFolder"
$env:BUTLER_AUTO_ART="1"  # Флаг для chat_router.py

python ".\A_03_ORCHESTRATION\chat_router.py"

Write-Host ""
Write-Host "======================================================================" -ForegroundColor DarkCyan
Write-Host "                     BUTLER OMEGA ЗАВЕРШЁН                            " -ForegroundColor Cyan
Write-Host "======================================================================" -ForegroundColor DarkCyan
Read-Host "Нажмите Enter для выхода"
