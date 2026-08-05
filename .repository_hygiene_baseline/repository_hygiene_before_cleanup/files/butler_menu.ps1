# -*- coding: utf-8 -*-
Clear-Host

function Show-Menu {
    Write-Host "==========================================" -ForegroundColor Cyan
    Write-Host "        BUTLER CONTROL PANEL v1.4" -ForegroundColor Cyan
    Write-Host "==========================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "[1] Паспорт        - Чтение стейта из JSON истины"
    Write-Host "[2] Безопасный Цикл- Запустить рантайм ядра"
    Write-Host "[3] Бэкап          - Запустить core_backup_worker"
    Write-Host "[4] Уборка         - Запустить desktop_cleaner_worker"
    Write-Host "[5] Тест Ollama    - Проверить ИИ (19 моделей)"
    Write-Host "[6] Выход          - Закрыть панель"
    Write-Host ""
}

while ($true) {
    Show-Menu
    $choice = Read-Host "Выбери действие (1-6)"

    switch ($choice) {
        "1" {
            Clear-Host
            Write-Host "[PASSPORT] Чтение goals_registry.json..." -ForegroundColor Green

            if (Test-Path ".\A_07_CONFIG\goals_registry.json") {
                try {
                    $data = Get-Content ".\A_07_CONFIG\goals_registry.json" -Raw | ConvertFrom-Json

                    Write-Host "`n=== BUTLER STATUS ===" -ForegroundColor Cyan
                    Write-Host "Active Goal : $($data.active_goal)" -ForegroundColor Yellow
                    Write-Host "Current Phase: $($data.current_phase)" -ForegroundColor Yellow
                    Write-Host "-------------------------------------"

                    if ($data.subgoals) {
                        foreach ($sg in $data.subgoals) {
                            Write-Host "Subgoal: $($sg.id) | [$($sg.status)]" -ForegroundColor Magenta
                            if ($sg.tasks) {
                                foreach ($t in $sg.tasks) {
                                    $color = if ($t.status -eq "COMPLETED") { "Green" } else { "Gray" }
                                    Write-Host "   - Task: $($t.id) | [$($t.status)]" -ForegroundColor $color
                                }
                            }
                        }
                    }
                    Write-Host "=====================" -ForegroundColor Cyan
                }
                catch {
                    Write-Host "[FAIL] Ошибка парсинга JSON структуры!" -ForegroundColor Red
                    Write-Host $_.Exception.Message -ForegroundColor DarkRed
                }
            }
            else {
                Write-Host "[FAIL] goals_registry.json не найден!" -ForegroundColor Red
            }

            Read-Host "`nНажми Enter для возврата..."
            Clear-Host
        }

        "2" {
            Clear-Host
            Write-Host "[SAFE START] Инициализация проверки и запуск ядра..." -ForegroundColor Cyan
            if (Test-Path ".\A_07_MEMORY\agent_runtime.py") {
                python .\A_07_MEMORY\agent_runtime.py
            } else { Write-Host "[FAIL] agent_runtime.py не найден!" -ForegroundColor Red }
            Read-Host "`nНажми Enter..."
            Clear-Host
        }

        "3" {
            Clear-Host
            Write-Host "[BACKUP] Запуск core_backup_worker.py..." -ForegroundColor Yellow
            if (Test-Path ".\A_07_MEMORY\core_backup_worker.py") { python .\A_07_MEMORY\core_backup_worker.py }
            Read-Host "`nНажми Enter..."
            Clear-Host
        }

        "4" {
            Clear-Host
            Write-Host "[CLEANUP] Запуск desktop_cleaner_worker.py..." -ForegroundColor Yellow
            if (Test-Path ".\A_07_MEMORY\desktop_cleaner_worker.py") { python .\A_07_MEMORY\desktop_cleaner_worker.py }
            Read-Host "`nНажми Enter..."
            Clear-Host
        }

        "5" {
            Clear-Host
            Write-Host "[OLLAMA] Запуск моста интерфейса..." -ForegroundColor Green
            if (Test-Path ".\A_09_INTERFACE\test_ollama_connect.py") { python .\A_09_INTERFACE\test_ollama_connect.py }
            Read-Host "`nНажми Enter для возврата..."
            Clear-Host
        }

        "6" {
            Write-Host "Выход из Butler Control Panel. Контур сохранен." -ForegroundColor Red
            break
        }

        default {
            Write-Host "Неверный выбор. Введите число от 1 до 6." -ForegroundColor Red
            Start-Sleep -Seconds 1
            Clear-Host
        }
    }
}
