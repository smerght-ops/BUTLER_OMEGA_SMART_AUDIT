# -*- coding: utf-8 -*-
# GENIE_GUARDIAN: Оперативный цензор архитектурных инвариантов Butler OS

$ROOT = "."
$DISPATCHER_PATH = "$ROOT\A_02_MANAGERS\smart_dispatcher_v2.py"
$RESOLVER_PATH = "$ROOT\A_07_MEMORY\SESSION\reference_resolver.py"
$CORRUPTED = $false

Write-Host "====================================================" -ForegroundColor Cyan
Write-Host "   GENIE GUARDIAN v1.0: INVARIANT REPRESSION AUDIT  " -ForegroundColor Cyan
Write-Host "====================================================" -ForegroundColor Cyan

# I. АУДИТ ДИСПЕТЧЕРА
if (Test-Path $DISPATCHER_PATH) {
    $content = Get-Content $DISPATCHER_PATH -Raw -Encoding UTF8

    # 1. Проверка метода _execute_department
    if ($content -match "def _execute_department") {
        Write-Host "[GENIE] OK: Инвариант Диспетчера -> Метод _execute_department на месте." -ForegroundColor Green
    } else {
        Write-Host "[GENIE CRITICAL] FAIL: Исчез метод _execute_department!" -ForegroundColor Red
        $CORRUPTED = $true
    }

    # 2. Проверка использования ButlerHarness
    if ($content -match "ButlerHarness") {
        Write-Host "[GENIE] OK: Инвариант Диспетчера -> Зависимость ButlerHarness присутствует." -ForegroundColor Green
    } else {
        Write-Host "[GENIE CRITICAL] FAIL: ButlerHarness был кастрирован из кода!" -ForegroundColor Red
        $CORRUPTED = $true
    }

    # 3. Проверка Семантической памяти
    if ($content -match "SemanticMemory") {
        Write-Host "[GENIE] OK: Инвариант Диспетчера -> Семантическая память подключена." -ForegroundColor Green
    } else {
        Write-Host "[GENIE CRITICAL] FAIL: Семантическая память отключена!" -ForegroundColor Red
        $CORRUPTED = $true
    }
} else {
    Write-Host "[GENIE CRITICAL] Диспетчер не найден по пути $DISPATCHER_PATH" -ForegroundColor Red
    $CORRUPTED = $true
}

# II. АУДИТ РЕЗОЛВЕРА (КОНТРАКТ)
if (Test-Path $RESOLVER_PATH) {
    $res_content = Get-Content $RESOLVER_PATH -Raw -Encoding UTF8

    if ($res_content -match "def _success" -and $res_content -match "def _failure") {
        Write-Host "[GENIE] OK: Инвариант Контракта  -> Фабрики ответов фабрикуют симметрию." -ForegroundColor Green
    } else {
        Write-Host "[GENIE CRITICAL] FAIL: Из ReferenceResolver удален симметричный контракт!" -ForegroundColor Red
        $CORRUPTED = $true
    }
} else {
    Write-Host "[GENIE CRITICAL] Резолвер не найден по пути $RESOLVER_PATH" -ForegroundColor Red
    $CORRUPTED = $true
}

# ВЕРДИКТ ВЕХИ
Write-Host "----------------------------------------------------" -ForegroundColor Cyan
if ($CORRUPTED) {
    Write-Host "🔴 GENIE STATUS: ARCHITECTURE CORRUPTED!" -ForegroundColor Red
    Write-Host "Обновление паспорта проекта ЗАБЛОКИРОВАНО." -ForegroundColor Red
    Write-Host "----------------------------------------------------" -ForegroundColor Cyan
    Exit 1
} else {
    Write-Host "🟢 GENIE STATUS: ARCHITECTURE HEALTH 100/100" -ForegroundColor Green
    Write-Host "Разрешен переход к автономным и живым тестам." -ForegroundColor Green
    Write-Host "----------------------------------------------------" -ForegroundColor Cyan
    Exit 0
}
