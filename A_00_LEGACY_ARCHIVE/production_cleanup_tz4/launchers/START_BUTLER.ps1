[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$env:PYTHONUTF8="1"
$Host.UI.RawUI.WindowTitle = "BUTLER OMEGA CHAT ROUTER"

$Root = "C:\Users\KOS\Desktop\Butler_Agent\BUTLER_OMEGA"
Set-Location $Root

Clear-Host
Write-Host "======================================================================" -ForegroundColor DarkCyan
Write-Host "                     BUTLER OMEGA — LIVE CHAT                         " -ForegroundColor Cyan
Write-Host "======================================================================" -ForegroundColor DarkCyan
Write-Host ""
Write-Host "[1/3] Проверка Ollama..." -ForegroundColor Yellow

try {
    Invoke-RestMethod "http://127.0.0.1:11434/api/tags" -TimeoutSec 3 | Out-Null
    Write-Host "[OK] Ollama уже работает." -ForegroundColor Green
}
catch {
    Write-Host "[INFO] Ollama не отвечает. Запускаю ollama serve..." -ForegroundColor Yellow
    Start-Process -FilePath "ollama" -ArgumentList "serve" -WindowStyle Minimized
    Start-Sleep -Seconds 5
}

Write-Host ""
Write-Host "[2/3] Точка входа:" -ForegroundColor Yellow
Write-Host "A_03_ORCHESTRATION\chat_router.py" -ForegroundColor Green
Write-Host ""
Write-Host "[3/3] Запуск живого чата Butler..." -ForegroundColor Yellow
Write-Host "Команда 'нарисуй ...' вызывает выбор художника." -ForegroundColor Cyan
Write-Host ""

python ".\A_03_ORCHESTRATION\chat_router.py"

Write-Host ""
Write-Host "======================================================================" -ForegroundColor DarkCyan
Write-Host "                     BUTLER OMEGA ЗАВЕРШЁН                            " -ForegroundColor Cyan
Write-Host "======================================================================" -ForegroundColor DarkCyan
Read-Host "Нажми Enter для выхода"
