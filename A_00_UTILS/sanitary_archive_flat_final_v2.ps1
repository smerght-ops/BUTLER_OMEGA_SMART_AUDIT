<#
.SYNOPSIS
    Sanitary Archive Flat — архивация служебных файлов в плоский архив с контролем дубликатов.

.DESCRIPTION
    Ищет файлы по паттернам, копирует новые в A_00_LEGACY_ARCHIVE\SANITARY_ARCHIVE
    с именем YYYYMMDD_<имя> (при коллизии добавляет _1, _2...).
    Ведёт manifest.json с версией формата и хеш-таблицей:
    ключ — SHA256, значение — объект с полями:
    ArchiveName, OriginalPaths (массив), Size, LastWriteTime, FirstSeen, LastSeen.
    Обеспечивает атомарную запись, блокировку одновременных запусков и ротацию лога.

.PARAMETER DryRun
    Только показывает, что будет сделано. По умолчанию включён.

.PARAMETER Execute
    Выполняет реальное копирование. Без этого параметра ничего не копируется.

.PARAMETER Validate
    Проверяет целостность архива и manifest.json, ничего не копирует.

.EXAMPLE
    .\sanitary_archive_flat_final_v2.ps1 -DryRun
    .\sanitary_archive_flat_final_v2.ps1 -Execute
    .\sanitary_archive_flat_final_v2.ps1 -Validate
#>

param(
    [switch]$DryRun = $true,
    [switch]$Execute = $false,
    [switch]$Validate = $false
)

# Приоритет: Validate > Execute > DryRun
if ($Validate) {
    $DryRun = $false
    $Execute = $false
} elseif ($Execute) {
    $DryRun = $false
}

# --- Определение корня проекта ---
$ScriptPath = $MyInvocation.MyCommand.Path
$ScriptDir = Split-Path -Parent $ScriptPath
$ProjectRoot = Split-Path -Parent $ScriptDir          # предполагаем, что скрипт в A_00_UTILS

$ArchiveRoot = Join-Path $ProjectRoot "A_00_LEGACY_ARCHIVE\SANITARY_ARCHIVE"
$ManifestPath = Join-Path $ArchiveRoot "manifest.json"
$TempManifestPath = Join-Path $ArchiveRoot "manifest.tmp"
$LogPath = Join-Path $ArchiveRoot "archive.log"
$LockPath = Join-Path $ArchiveRoot "archive.lock"

# Паттерны и исключения
function ShouldArchive {
    param($File)

    $Name = $File.Name.ToLowerInvariant()

    switch -Wildcard ($Name) {
        "*backup*"            { return $true }
        "*.bak"               { return $true }
        "*.old"               { return $true }
        "*.copy"              { return $true }
        "snapshot_*"          { return $true }
        "*.snapshot"          { return $true }
        "*.checkpoint"        { return $true }
        "config_backup*.json" { return $true }
        default               { return $false }
    }
}
$ExcludeDirs = @("A_00_LEGACY_ARCHIVE", "__pycache__")
# --- Функции ---

function Is-Excluded {
    param([string]$Path)
    foreach ($dir in $ExcludeDirs) {
        if ($Path -match "(^|\\|/)$dir($|\\|/)") {
            return $true
        }
    }
    return $false
}

function Get-FileHashSafe {
    param([string]$Path)
    try {
        return (Get-FileHash -Path $Path -Algorithm SHA256).Hash
    } catch {
        Write-Warning "Не удалось вычислить хеш для $Path : $_"
        return $null
    }
}

function Get-RelativePath {
    param([string]$FullPath, [string]$BasePath)
    # Возвращает относительный путь (слеш-разделители Windows)
    $BasePath = $BasePath.TrimEnd('\')
    if ($FullPath.StartsWith($BasePath)) {
        return $FullPath.Substring($BasePath.Length + 1)
    } else {
        # Если путь не в проекте, возвращаем имя файла
        return [System.IO.Path]::GetFileName($FullPath)
    }
}

function Load-Manifest {
    if (Test-Path $ManifestPath) {
        try {
            $content = Get-Content -Path $ManifestPath -Raw -Encoding UTF8
            $data = $content | ConvertFrom-Json
            # Проверка версии
            if ($data.Version -ne 1) {
                Write-Warning "Неизвестная версия манифеста ($($data.Version)). Будет создан новый."
                return @{}
            }
            # Преобразуем массив записей в хеш-таблицу
            $hashTable = @{}
            foreach ($item in $data.Entries) {
                $hashTable[$item.Hash] = $item
            }
            return $hashTable
        } catch {
            Write-Warning "Ошибка чтения manifest.json: $_ . Будет создан новый."
            return @{}
        }
    } else {
        return @{}
    }
}

function Save-Manifest {
    param($Manifest)
    if (-not (Test-Path $ArchiveRoot)) {
        New-Item -ItemType Directory -Path $ArchiveRoot -Force | Out-Null
    }
    # Преобразуем хеш-таблицу в массив и оборачиваем в объект с версией
    $entries = @()
    foreach ($key in $Manifest.Keys) {
        $entries += $Manifest[$key]
    }
    $manifestObj = @{
        "Version" = 1
        "Entries" = $entries
    }
    # Атомарная запись через временный файл
    $manifestObj | ConvertTo-Json -Depth 5 | Set-Content -Path $TempManifestPath -Encoding UTF8
    # Проверка корректности JSON
    try {
        $test = Get-Content -Path $TempManifestPath -Raw -Encoding UTF8 | ConvertFrom-Json
        # Если ошибок нет, заменяем основной файл
        Move-Item -Path $TempManifestPath -Destination $ManifestPath -Force
    } catch {
        Write-Error "Ошибка валидации манифеста: $_ . Файл не сохранён."
    }
}

function Get-UniqueArchiveName {
    param([string]$OriginalName, [string]$ArchiveDir)
    $dateStamp = Get-Date -Format "yyyyMMdd"
    $base = [System.IO.Path]::GetFileNameWithoutExtension($OriginalName)
    $ext  = [System.IO.Path]::GetExtension($OriginalName)

    # Ограничим длину имени (без даты) до 200 символов
    if ($base.Length -gt 200) {
        $base = $base.Substring(0, 200)
    }

    $candidate = "$dateStamp`_$base$ext"
    $counter = 1
    while (Test-Path (Join-Path $ArchiveDir $candidate)) {
        $candidate = "$dateStamp`_$base`_$counter$ext"
        $counter++
    }
    return $candidate
}

function Write-Log {
    param([string]$Message)
    if ($DryRun -or $Validate) { return }  # лог только при реальном выполнении
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $logLine = "$timestamp $Message"
    # Если файла нет, создаём
    if (-not (Test-Path $LogPath)) {
        New-Item -ItemType File -Path $LogPath -Force | Out-Null
    }
    Add-Content -Path $LogPath -Value $logLine -Encoding UTF8
    # Ротация лога (если превышает 10 МБ)
    if ((Get-Item $LogPath).Length -gt 10MB) {
        $backupLog = "$LogPath.$(Get-Date -Format 'yyyyMMddHHmmss').bak"
        Move-Item -Path $LogPath -Destination $backupLog -Force
        New-Item -ItemType File -Path $LogPath -Force | Out-Null
    }
}

function Acquire-Lock {
    # Пытаемся создать файл блокировки, если он уже существует — ждём и повторяем
    $attempts = 0
    while ($attempts -lt 10) {
        if (-not (Test-Path $LockPath)) {
            # Создаём файл блокировки с PID и временем
            $lockContent = @{
                PID = $PID
                Timestamp = (Get-Date -Format "yyyy-MM-dd HH:mm:ss")
            } | ConvertTo-Json
            Set-Content -Path $LockPath -Value $lockContent -Encoding UTF8 -Force
            return $true
        }
        Start-Sleep -Milliseconds 500
        $attempts++
    }
    Write-Error "Не удалось получить блокировку. Другой процесс уже работает с архивом."
    exit 1
}

function Release-Lock {
    if (Test-Path $LockPath) {
        Remove-Item -Path $LockPath -Force
    }
}
# --- Основной скрипт ---

Write-Host "=== SANITARY ARCHIVE FLAT FINAL V2 ===" -ForegroundColor Cyan
Write-Host "Корень проекта: $ProjectRoot"
if ($Validate) {
    Write-Host "Режим: VALIDATE (только проверка)" -ForegroundColor Yellow
} elseif ($DryRun) {
    Write-Host "Режим: DRY RUN (только просмотр)" -ForegroundColor Yellow
} else {
    Write-Host "Режим: РЕАЛЬНОЕ КОПИРОВАНИЕ" -ForegroundColor Green
}

# Блокировка (только для Execute, т.к. Validate и DryRun не изменяют архив)
if ($Execute) {
    Acquire-Lock
}

try {
    # Загрузка манифеста (хеш-таблица)
    $Manifest = Load-Manifest
    Write-Host "Загружен манифест, содержит $($Manifest.Count) уникальных хешей."

    # Если режим Validate, проверяем целостность архива
    if ($Validate) {
        Write-Host "Проверка целостности..."
        $errors = 0
        foreach ($key in $Manifest.Keys) {
            $entry = $Manifest[$key]
            $destPath = Join-Path $ArchiveRoot $entry.ArchiveName
            if (-not (Test-Path $destPath)) {
                Write-Warning "Отсутствует файл: $($entry.ArchiveName)"
                $errors++
            } else {
                $hash = Get-FileHashSafe -Path $destPath
                if ($hash -ne $key) {
                    Write-Warning "Хеш не совпадает: $($entry.ArchiveName)"
                    $errors++
                }
            }
        }
        Write-Host "Проверка завершена. Ошибок: $errors" -ForegroundColor Cyan
        return  # завершаем, не выходя из процесса
    }

    # Сбор файлов: один проход с фильтрацией по паттернам
    $files = @()
    $allFiles = Get-ChildItem -Path $ProjectRoot -Recurse -File -ErrorAction SilentlyContinue
    foreach ($f in $allFiles) {
        if (Is-Excluded -Path $f.FullName) { continue }
        if ($f.FullName -like "$ArchiveRoot\*") { continue }
        if (ShouldArchive $f) {
            $files += $f
        }
    }
    $files = $files | Sort-Object -Unique -Property FullName
    Write-Host "Найдено файлов для рассмотрения: $($files.Count)"

    # Перебор файлов
    $copied = 0
    $skipped = 0
    $errors = 0
    $manifestChanged = $false  # флаг, что манифест изменился

    foreach ($file in $files) {
        $hash = Get-FileHashSafe -Path $file.FullName
        if ($null -eq $hash) {
            Write-Warning "Не удалось получить хеш для $($file.FullName), пропускаем."
            $errors++
            continue
        }

        $relPath = Get-RelativePath -FullPath $file.FullName -BasePath $ProjectRoot

        # Проверка дубликата через хеш-таблицу
        if ($Manifest.ContainsKey($hash)) {
            $entry = $Manifest[$hash]
            if ($entry.OriginalPaths -notcontains $relPath) {
                $entry.OriginalPaths += $relPath
                Write-Host "ДОБАВЛЕН ПУТЬ (дубликат по хешу): $relPath" -ForegroundColor Gray
                $manifestChanged = $true
            }
            # Обновляем LastSeen всегда
            $entry.LastSeen = (Get-Date -Format "yyyy-MM-dd HH:mm:ss")
            $manifestChanged = $true
            Write-Host "ПРОПУСК (дубликат по хешу): $relPath" -ForegroundColor Gray
            $skipped++
            continue
        }

        # Новый файл — генерируем имя в архиве
        $archiveName = Get-UniqueArchiveName -OriginalName $file.Name -ArchiveDir $ArchiveRoot
        $destPath = Join-Path $ArchiveRoot $archiveName

        if ($DryRun) {
            Write-Host "DRY: Будет скопирован: $($file.FullName) -> $archiveName" -ForegroundColor Magenta
            $copied++
        } else {
            try {
                # Создаём архивную папку при необходимости
                if (-not (Test-Path $ArchiveRoot)) {
                    New-Item -ItemType Directory -Path $ArchiveRoot -Force | Out-Null
                }

                # Проверка свободного места (хотя бы 10 МБ) — теперь безопасно
                $drive = (Get-Item $ArchiveRoot).PSDrive
                if ($drive.Free -lt 10MB) {
                    Write-Error "Недостаточно свободного места на диске $($drive.Name)."
                    $errors++
                    continue
                }

                Copy-Item -Path $file.FullName -Destination $destPath -Force -ErrorAction Stop

                # Проверяем хеш после копирования
                $copiedHash = Get-FileHashSafe -Path $destPath
                if ($copiedHash -ne $hash) {
                    Write-Warning "Хеш копии не совпадает с оригиналом! $($file.FullName) -> $destPath"
                    $errors++
                    # Удаляем повреждённую копию
                    Remove-Item -Path $destPath -Force -ErrorAction SilentlyContinue
                    continue
                }

                $entry = @{
                    "Hash"          = $hash
                    "ArchiveName"   = $archiveName
                    "OriginalPaths" = @($relPath)
                    "Size"          = $file.Length
                    "LastWriteTime" = $file.LastWriteTime.ToString("yyyy-MM-dd HH:mm:ss")
                    "FirstSeen"     = (Get-Date -Format "yyyy-MM-dd HH:mm:ss")
                    "LastSeen"      = (Get-Date -Format "yyyy-MM-dd HH:mm:ss")
                }
                $Manifest[$hash] = $entry
                $manifestChanged = $true
                Write-Host "СКОПИРОВАН: $($file.FullName) -> $archiveName" -ForegroundColor Green
                Write-Log -Message "COPY $($file.FullName) -> $archiveName (SHA256: $hash)"
                $copied++
            } catch {
                Write-Error "Ошибка копирования $($file.FullName) : $_"
                $errors++
                Write-Log -Message "ERROR $($file.FullName) : $_"
            }
        }
    }

    # Сохранение манифеста (только если не DryRun и были изменения)
    if (-not $DryRun -and $manifestChanged) {
        Save-Manifest -Manifest $Manifest
        Write-Host "Манифест обновлён."
    } elseif (-not $DryRun -and -not $manifestChanged) {
        Write-Host "Нет изменений, манифест не изменён."
    }

    # Итоговый отчёт
    Write-Host ""
    Write-Host "=== ИТОГИ ===" -ForegroundColor Cyan
    Write-Host "Рассмотрено: $($files.Count)"
    Write-Host "Скопировано (будет скопировано): $copied"
    Write-Host "Пропущено (дубликаты): $skipped"
    Write-Host "Ошибок: $errors"
    if ($DryRun) {
        Write-Host "Это был DRY RUN. Для реального копирования запустите с параметром -Execute." -ForegroundColor Yellow
    }
    Write-Host "=== ЗАВЕРШЕНО ===" -ForegroundColor Cyan

} finally {
    # Снимаем блокировку, если она была установлена
    if ($Execute) {
        Release-Lock
    }
}
