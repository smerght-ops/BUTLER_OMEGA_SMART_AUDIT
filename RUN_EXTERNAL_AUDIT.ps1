#requires -Version 5.1
<#
.SYNOPSIS
    Внешний аудит Markdown-документации проекта через OpenRouter.

.DESCRIPTION
    1. Находит Markdown-файлы проекта.
    2. Исключает служебные и архивные каталоги.
    3. Делит крупные документы на части.
    4. Отправляет части в OpenRouter с повторными попытками.
    5. Сохраняет промежуточные отчёты.
    6. Выполняет многоступенчатый синтез итогового аудита.

.NOTES
    Запускайте из корня проекта Butler.
    API-ключ можно передать параметром -ApiKey либо через:
    $env:OPENROUTER_API_KEY = "..."
#>

[CmdletBinding()]
param(
    [string]$ApiKey = $env:OPENROUTER_API_KEY,

    [string]$Model = "tencent/hy3:free",

    [string]$ProjectRoot = (Get-Location).Path,

    [string]$OutputDir = "A_06_WORKSPACE\EXTERNAL_AUDIT",

    [ValidateRange(1000, 12000)]
    [int]$MaxInputTokens = 10000,

    [ValidateRange(256, 16000)]
    [int]$MaxOutputTokens = 1200,

    [ValidateRange(1, 10)]
    [int]$MaxRetries = 4,

    [ValidateRange(2, 50)]
    [int]$SynthesisBatchSize = 10,

    [ValidateRange(0, 10000)]
    [int]$DelayMilliseconds = 750
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$OpenRouterUri = "https://openrouter.ai/api/v1/chat/completions"
$script:TotalPromptTokens = 0L
$script:TotalCompletionTokens = 0L
$script:TotalTokens = 0L
$script:SuccessfulRequests = 0
$script:FailedRequests = 0
$script:RequestNumber = 0

function Write-AuditLog {
    param(
        [Parameter(Mandatory)]
        [string]$Message,

        [ValidateSet("INFO", "WARN", "ERROR", "SUCCESS")]
        [string]$Level = "INFO"
    )

    $line = "[{0:yyyy-MM-dd HH:mm:ss}] [{1}] {2}" -f (Get-Date), $Level, $Message
    Add-Content -LiteralPath $script:LogFile -Value $line -Encoding UTF8

    switch ($Level) {
        "WARN"    { Write-Host $line -ForegroundColor Yellow }
        "ERROR"   { Write-Host $line -ForegroundColor Red }
        "SUCCESS" { Write-Host $line -ForegroundColor Green }
        default   { Write-Host $line }
    }
}

function Convert-ToSafeFileName {
    param(
        [Parameter(Mandatory)]
        [string]$Name
    )

    $invalid = [IO.Path]::GetInvalidFileNameChars()
    $result = $Name

    foreach ($char in $invalid) {
        $result = $result.Replace([string]$char, "_")
    }

    $result = $result -replace '\s+', '_'
    $result = $result.Trim('_', '.', ' ')

    if ([string]::IsNullOrWhiteSpace($result)) {
        return "unnamed"
    }

    if ($result.Length -gt 120) {
        $result = $result.Substring(0, 120)
    }

    return $result
}

function Get-RelativeProjectPath {
    param(
        [Parameter(Mandatory)]
        [string]$FullPath
    )

    $root = [IO.Path]::GetFullPath($script:ProjectRootResolved)
    if (-not $root.EndsWith([IO.Path]::DirectorySeparatorChar)) {
        $root += [IO.Path]::DirectorySeparatorChar
    }

    $file = [IO.Path]::GetFullPath($FullPath)
    $rootUri = [Uri]$root
    $fileUri = [Uri]$file
    $relative = $rootUri.MakeRelativeUri($fileUri).ToString()
    return [Uri]::UnescapeDataString($relative).Replace('/', '\')
}

function Get-ProjectMarkdownFiles {
    param(
        [Parameter(Mandatory)]
        [string]$Root
    )

    $excludedDirectoryNames = @(
        ".git",
        "__pycache__",
        ".pytest_cache",
        ".mypy_cache",
        ".ruff_cache",
        "node_modules",
        ".venv",
        "venv",
        "A_00_RESTORE",
        "A_00_ARCHIVE",
        "A_00_BACKUP",
        "A_00_LEGACY_ARCHIVE",
        "A_00_HISTORY",
        "SNAPSHOTS",
        "ARCHIVE_BACKUPS",
        "payload",
        "EXTERNAL_AUDIT"
    )

    $outputFullPath = [IO.Path]::GetFullPath($script:OutputDirResolved)

    $files = Get-ChildItem -LiteralPath $Root -Recurse -File -Filter "*.md" -ErrorAction SilentlyContinue |
        Where-Object {
            $full = [IO.Path]::GetFullPath($_.FullName)

            if ($full.StartsWith($outputFullPath, [StringComparison]::OrdinalIgnoreCase)) {
                return $false
            }

            foreach ($directoryName in $excludedDirectoryNames) {
                $escaped = [Regex]::Escape($directoryName)
                if ($full -match "[\\/](?:$escaped)(?:[\\/]|$)") {
                    return $false
                }
            }

            return $true
        } |
        Sort-Object FullName

    return @($files)
}

function Split-TextByApproximateTokens {
    param(
        [Parameter(Mandatory)]
        [string]$Text,

        [Parameter(Mandatory)]
        [int]$TokenLimit
    )

    if ([string]::IsNullOrWhiteSpace($Text)) {
        return @()
    }

    # Приближённо: один токен ~= 4 символа.
    # Оставляем резерв для системных инструкций и служебного текста.
    $characterLimit = [Math]::Max(2000, [int]($TokenLimit * 4 * 0.82))

    if ($Text.Length -le $characterLimit) {
        return @($Text)
    }

    $parts = New-Object System.Collections.Generic.List[string]
    $remaining = $Text

    while ($remaining.Length -gt $characterLimit) {
        $cut = $remaining.LastIndexOf("`n`n", $characterLimit)

        if ($cut -lt [int]($characterLimit * 0.55)) {
            $cut = $remaining.LastIndexOf("`n", $characterLimit)
        }

        if ($cut -lt [int]($characterLimit * 0.40)) {
            $cut = $remaining.LastIndexOf(". ", $characterLimit)
            if ($cut -ge 0) {
                $cut += 1
            }
        }

        if ($cut -lt 1) {
            $cut = $characterLimit
        }

        $piece = $remaining.Substring(0, $cut).Trim()
        if (-not [string]::IsNullOrWhiteSpace($piece)) {
            $parts.Add($piece)
        }

        $remaining = $remaining.Substring($cut).TrimStart()
    }

    if (-not [string]::IsNullOrWhiteSpace($remaining)) {
        $parts.Add($remaining.Trim())
    }

    return @($parts)
}

function Get-HttpErrorDetails {
    param(
        [Parameter(Mandatory)]
        $ErrorRecord
    )

    $statusCode = $null
    $responseText = $null

    try {
        if ($ErrorRecord.Exception.Response) {
            $response = $ErrorRecord.Exception.Response

            try {
                $statusCode = [int]$response.StatusCode
            }
            catch {
                $statusCode = $null
            }

            try {
                $stream = $response.GetResponseStream()
                if ($stream) {
                    $reader = New-Object IO.StreamReader($stream)
                    try {
                        $responseText = $reader.ReadToEnd()
                    }
                    finally {
                        $reader.Dispose()
                    }
                }
            }
            catch {
                $responseText = $null
            }
        }
    }
    catch {
        $statusCode = $null
    }

    return [PSCustomObject]@{
        StatusCode = $statusCode
        Body       = $responseText
    }
}

function Invoke-OpenRouterRequest {
    param(
        [Parameter(Mandatory)]
        [string]$Prompt,

        [string]$Purpose = "analysis"
    )

    $headers = @{
        Authorization  = "Bearer $script:ApiKeyResolved"
        "Content-Type" = "application/json"
        "HTTP-Referer" = "https://localhost/butler-external-audit"
        "X-Title"       = "Butler External Audit"
    }

    $bodyObject = @{
        model       = $Model
        max_tokens  = $MaxOutputTokens
        temperature = 0.1
        messages    = @(
            @{
                role    = "user"
                content = $Prompt
            }
        )
    }

    $body = $bodyObject | ConvertTo-Json -Depth 8 -Compress

    for ($attempt = 1; $attempt -le $MaxRetries; $attempt++) {
        $script:RequestNumber++
        $requestId = $script:RequestNumber

        try {
            Write-AuditLog -Message (
                "Запрос #{0}; назначение={1}; попытка={2}/{3}; символов={4}" -f
                $requestId, $Purpose, $attempt, $MaxRetries, $Prompt.Length
            )

            $response = Invoke-RestMethod `
                -Uri $OpenRouterUri `
                -Method Post `
                -Headers $headers `
                -Body $body `
                -TimeoutSec 240

            if ($null -eq $response.choices -or $response.choices.Count -eq 0) {
                throw "OpenRouter вернул ответ без choices."
            }

            $choice = $response.choices[0]
            $content = [string]$choice.message.content
            $finishReason = [string]$choice.finish_reason

            if ([string]::IsNullOrWhiteSpace($content)) {
                throw "Модель вернула пустое содержание."
            }

            if ($response.usage) {
                $promptTokens = [long]$response.usage.prompt_tokens
                $completionTokens = [long]$response.usage.completion_tokens
                $totalTokens = [long]$response.usage.total_tokens

                $script:TotalPromptTokens += $promptTokens
                $script:TotalCompletionTokens += $completionTokens
                $script:TotalTokens += $totalTokens

                Write-AuditLog -Message (
                    "Запрос #{0}: prompt={1}; completion={2}; total={3}; finish_reason={4}" -f
                    $requestId, $promptTokens, $completionTokens, $totalTokens, $finishReason
                )
            }
            else {
                Write-AuditLog -Message (
                    "Запрос #{0}: usage отсутствует; finish_reason={1}" -f
                    $requestId, $finishReason
                ) -Level "WARN"
            }

            if ($finishReason -eq "length") {
                Write-AuditLog -Message (
                    "Запрос #{0} завершён по лимиту длины. Полученный текст сохранится, но может быть оборван." -f
                    $requestId
                ) -Level "WARN"
            }

            $script:SuccessfulRequests++

            return [PSCustomObject]@{
                Content      = $content.Trim()
                FinishReason = $finishReason
                RawResponse  = $response
            }
        }
        catch {
            $details = Get-HttpErrorDetails -ErrorRecord $_
            $status = $details.StatusCode
            $bodyText = $details.Body

            $message = $_.Exception.Message
            if (-not [string]::IsNullOrWhiteSpace($bodyText)) {
                $message += " | Ответ сервера: $bodyText"
            }

            $retryable = (
                $null -eq $status -or
                $status -eq 408 -or
                $status -eq 409 -or
                $status -eq 429 -or
                $status -ge 500
            )

            Write-AuditLog -Message (
                "Ошибка запроса #{0}; HTTP={1}; попытка={2}/{3}; {4}" -f
                $requestId, $status, $attempt, $MaxRetries, $message
            ) -Level "ERROR"

            if (-not $retryable -or $attempt -ge $MaxRetries) {
                $script:FailedRequests++
                throw
            }

            $waitSeconds = [Math]::Min(60, [Math]::Pow(2, $attempt))
            Write-AuditLog -Message "Повтор через $waitSeconds сек." -Level "WARN"
            Start-Sleep -Seconds $waitSeconds
        }
    }

    throw "Запрос не выполнен после $MaxRetries попыток."
}

function Save-Utf8Text {
    param(
        [Parameter(Mandatory)]
        [string]$Path,

        [Parameter(Mandatory)]
        [AllowEmptyString()]
        [string]$Content
    )

    $parent = Split-Path -Parent $Path
    if ($parent -and -not (Test-Path -LiteralPath $parent)) {
        New-Item -ItemType Directory -Path $parent -Force | Out-Null
    }

    Set-Content -LiteralPath $Path -Value $Content -Encoding UTF8
}

function Invoke-BatchedSynthesis {
    param(
        [Parameter(Mandatory)]
        [string[]]$ReportPaths
    )

    $currentLevel = @($ReportPaths)
    $level = 1

    while ($currentLevel.Count -gt 1) {
        Write-AuditLog -Message (
            "Синтез уровня {0}: входных материалов={1}" -f $level, $currentLevel.Count
        )

        $nextLevel = New-Object System.Collections.Generic.List[string]
        $batchNumber = 0

        for ($start = 0; $start -lt $currentLevel.Count; $start += $SynthesisBatchSize) {
            $batchNumber++
            $end = [Math]::Min($start + $SynthesisBatchSize - 1, $currentLevel.Count - 1)
            $batch = @($currentLevel[$start..$end])

            $combinedBuilder = New-Object Text.StringBuilder

            foreach ($path in $batch) {
                if (-not (Test-Path -LiteralPath $path)) {
                    continue
                }

                $name = Split-Path -Leaf $path
                $text = Get-Content -LiteralPath $path -Raw -Encoding UTF8

                [void]$combinedBuilder.AppendLine("")
                [void]$combinedBuilder.AppendLine("============================================================")
                [void]$combinedBuilder.AppendLine("МАТЕРИАЛ: $name")
                [void]$combinedBuilder.AppendLine("============================================================")
                [void]$combinedBuilder.AppendLine($text)
            }

            $combined = $combinedBuilder.ToString()

            $synthesisPrompt = @"
Ты — независимый главный архитектор программного обеспечения.

Ниже переданы промежуточные результаты аудита проекта Butler Omega Smart.
Сделай одну компактную, доказательную сводку без потери существенных замечаний.

Обязательные правила:
- не выдумывай факты;
- отделяй подтверждённые дефекты от предположений;
- объединяй дубли;
- сохраняй названия файлов и конкретные доказательства;
- не предлагай переписывание архитектуры без подтверждённой необходимости;
- ответ только в Markdown.

Структура:
# Подтверждённые факты
# Завершённые и стабильные области
# Подтверждённые дефекты и риски
# Дублирование и потеря времени
# Что можно заморозить
# Открытые вопросы

МАТЕРИАЛЫ:
$combined
"@

            $result = Invoke-OpenRouterRequest `
                -Prompt $synthesisPrompt `
                -Purpose ("synthesis-level-{0}-batch-{1}" -f $level, $batchNumber)

            $summaryPath = Join-Path `
                $script:SynthesisDir `
                ("level_{0:D2}_batch_{1:D3}.md" -f $level, $batchNumber)

            Save-Utf8Text -Path $summaryPath -Content $result.Content
            $nextLevel.Add($summaryPath)

            Write-AuditLog -Message "Сводка сохранена: $summaryPath" -Level "SUCCESS"

            if ($DelayMilliseconds -gt 0) {
                Start-Sleep -Milliseconds $DelayMilliseconds
            }
        }

        $currentLevel = @($nextLevel)
        $level++
    }

    return $currentLevel[0]
}

# ----------------------------------------------------------------------
# Инициализация
# ----------------------------------------------------------------------

if ([string]::IsNullOrWhiteSpace($ApiKey)) {
    throw @"
API-ключ OpenRouter не найден.

Укажите его одним из способов:

1. Только для текущего окна PowerShell:
   `$env:OPENROUTER_API_KEY = "ваш_ключ"

2. Через параметр:
   .\RUN_EXTERNAL_AUDIT.ps1 -ApiKey "ваш_ключ"
"@
}

$script:ApiKeyResolved = $ApiKey.Trim()
$script:ProjectRootResolved = [IO.Path]::GetFullPath($ProjectRoot)

if (-not (Test-Path -LiteralPath $script:ProjectRootResolved -PathType Container)) {
    throw "Корень проекта не найден: $script:ProjectRootResolved"
}

if ([IO.Path]::IsPathRooted($OutputDir)) {
    $script:OutputDirResolved = [IO.Path]::GetFullPath($OutputDir)
}
else {
    $script:OutputDirResolved = [IO.Path]::GetFullPath(
        (Join-Path $script:ProjectRootResolved $OutputDir)
    )
}

$script:PartsDir = Join-Path $script:OutputDirResolved "PART_REPORTS"
$script:SynthesisDir = Join-Path $script:OutputDirResolved "SYNTHESIS"
$script:LogFile = Join-Path $script:OutputDirResolved "audit.log"
$script:ManifestFile = Join-Path $script:OutputDirResolved "audit_manifest.csv"
$script:FinalReport = Join-Path $script:OutputDirResolved "BUTLER_EXTERNAL_AUDIT.md"

New-Item -ItemType Directory -Path $script:OutputDirResolved -Force | Out-Null
New-Item -ItemType Directory -Path $script:PartsDir -Force | Out-Null
New-Item -ItemType Directory -Path $script:SynthesisDir -Force | Out-Null

Set-Content -LiteralPath $script:LogFile -Value "" -Encoding UTF8

Write-AuditLog -Message "Проект: $script:ProjectRootResolved"
Write-AuditLog -Message "Модель: $Model"
Write-AuditLog -Message "Каталог отчётов: $script:OutputDirResolved"
Write-AuditLog -Message "MaxInputTokens=$MaxInputTokens; MaxOutputTokens=$MaxOutputTokens"

# ----------------------------------------------------------------------
# Поиск и анализ документов
# ----------------------------------------------------------------------

$documents = Get-ProjectMarkdownFiles -Root $script:ProjectRootResolved

if ($documents.Count -eq 0) {
    throw "В проекте не найдено Markdown-файлов для анализа."
}

Write-AuditLog -Message "Найдено Markdown-файлов: $($documents.Count)" -Level "SUCCESS"

$manifest = New-Object System.Collections.Generic.List[object]
$partReports = New-Object System.Collections.Generic.List[string]
$documentNumber = 0

foreach ($document in $documents) {
    $documentNumber++
    $relativePath = Get-RelativeProjectPath -FullPath $document.FullName
    $text = Get-Content -LiteralPath $document.FullName -Raw -Encoding UTF8

    if ([string]::IsNullOrWhiteSpace($text)) {
        Write-AuditLog -Message "Пропущен пустой файл: $relativePath" -Level "WARN"

        $manifest.Add([PSCustomObject]@{
            Document = $relativePath
            Part     = 0
            Parts    = 0
            Status   = "SKIPPED_EMPTY"
            Report   = ""
            Error    = ""
        })
        continue
    }

$chunks = @(
    Split-TextByApproximateTokens `
        -Text $text `
        -TokenLimit $MaxInputTokens
)

    Write-AuditLog -Message (
        "Документ {0}/{1}: {2}; частей={3}" -f
        $documentNumber, @($documents).Count, $relativePath, @($chunks).Count
    )

    $safeBase = Convert-ToSafeFileName `
        -Name ([IO.Path]::GetFileNameWithoutExtension($document.Name))

    for ($partIndex = 0; $partIndex -lt $chunks.Count; $partIndex++) {
        $partNumber = $partIndex + 1
        $chunk = $chunks[$partIndex]

        $analysisPrompt = @"
Ты — независимый архитектор программного обеспечения.
Проведи строгий аудит переданного фрагмента документа проекта Butler Omega Smart.

Контекст:
- путь документа: $relativePath
- часть: $partNumber из $($chunks.Count)

Правила:
- анализируй только переданный материал;
- не выдумывай отсутствующие сведения;
- разделяй подтверждённые факты, дефекты и предположения;
- не предлагай новое техническое задание;
- не предлагай изменение согласованной архитектуры без подтверждённого дефекта;
- не пересказывай документ целиком;
- сохраняй конкретные названия компонентов, файлов и контрактов;
- ответ только в Markdown.

Структура:
# Назначение
# Подтверждённые факты
# Что уже завершено
# Подтверждённые дефекты
# Риски и противоречия
# Дублирование и лишняя работа
# Что можно заморозить
# Открытые вопросы

ДОКУМЕНТ:
$chunk
"@

        try {
            $result = Invoke-OpenRouterRequest `
                -Prompt $analysisPrompt `
                -Purpose ("document:{0}:part:{1}" -f $relativePath, $partNumber)

            $reportName = "{0:D4}_{1}_part_{2:D3}_of_{3:D3}.md" -f `
                $documentNumber, $safeBase, $partNumber, $chunks.Count

            $reportPath = Join-Path $script:PartsDir $reportName
            Save-Utf8Text -Path $reportPath -Content $result.Content
            $partReports.Add($reportPath)

            $manifest.Add([PSCustomObject]@{
                Document = $relativePath
                Part     = $partNumber
                Parts    = $chunks.Count
                Status   = "SUCCESS"
                Report   = $reportPath
                Error    = ""
            })

            Write-AuditLog -Message "Сохранён отчёт: $reportPath" -Level "SUCCESS"
        }
        catch {
            $errorText = $_.Exception.Message

            $manifest.Add([PSCustomObject]@{
                Document = $relativePath
                Part     = $partNumber
                Parts    = $chunks.Count
                Status   = "FAILED"
                Report   = ""
                Error    = $errorText
            })

            Write-AuditLog -Message (
                "Не обработан документ: {0}; часть={1}; ошибка={2}" -f
                $relativePath, $partNumber, $errorText
            ) -Level "ERROR"
        }

        if ($DelayMilliseconds -gt 0) {
            Start-Sleep -Milliseconds $DelayMilliseconds
        }
    }
}

$manifest | Export-Csv `
    -LiteralPath $script:ManifestFile `
    -NoTypeInformation `
    -Encoding UTF8

Write-AuditLog -Message "Манифест сохранён: $script:ManifestFile" -Level "SUCCESS"

if ($partReports.Count -eq 0) {
    throw "Не создано ни одного промежуточного отчёта. См. audit.log."
}

# ----------------------------------------------------------------------
# Многоступенчатый синтез
# ----------------------------------------------------------------------

$topSummaryPath = Invoke-BatchedSynthesis -ReportPaths @($partReports)
$topSummary = Get-Content -LiteralPath $topSummaryPath -Raw -Encoding UTF8

$finalPrompt = @"
Ты — главный независимый архитектор проекта Butler Omega Smart.

На основании сводного материала подготовь окончательный архитектурный аудит.
Это итоговый документ для владельца проекта.

Обязательные правила:
- не выдумывай факты;
- каждое серьёзное замечание связывай с имеющимся доказательством;
- явно разделяй подтверждённое, предположительное и неизвестное;
- не переписывай техническое задание;
- не меняй согласованную архитектуру без подтверждённого дефекта;
- не предлагай аудит ради аудита;
- покажи, где время было потрачено впустую;
- покажи, что завершено;
- покажи, что можно заморозить навсегда;
- выбери только одну следующую пользовательскую возможность с минимальным изменением архитектуры;
- ответ только в Markdown.

Обязательная структура:

# BUTLER OMEGA SMART — ВНЕШНИЙ АРХИТЕКТУРНЫЙ АУДИТ

## 1. Итоговый статус

## 2. Подтверждённо завершённые области

## 3. Что можно заморозить навсегда

## 4. Подтверждённые дефекты и блокировки

## 5. Архитектурные риски

## 6. Где время было потрачено впустую

## 7. Противоречия и дублирование

## 8. Одна следующая пользовательская возможность

## 9. Что делать сейчас

## 10. Что не делать

## 11. Итоговая оценка зрелости

СВОДНЫЙ МАТЕРИАЛ:
$topSummary
"@

$finalResult = Invoke-OpenRouterRequest `
    -Prompt $finalPrompt `
    -Purpose "final-audit"

$runSummary = @"

---

## Техническая информация о запуске

- Дата: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")
- Проект: $script:ProjectRootResolved
- Модель: $Model
- Найдено Markdown-файлов: $($documents.Count)
- Промежуточных отчётов: $($partReports.Count)
- Успешных запросов: $script:SuccessfulRequests
- Неуспешных запросов: $script:FailedRequests
- Prompt tokens: $script:TotalPromptTokens
- Completion tokens: $script:TotalCompletionTokens
- Total tokens: $script:TotalTokens
- Манифест: $script:ManifestFile
- Журнал: $script:LogFile
"@

Save-Utf8Text `
    -Path $script:FinalReport `
    -Content ($finalResult.Content.Trim() + $runSummary)

Write-AuditLog -Message "Финальный аудит сохранён: $script:FinalReport" -Level "SUCCESS"
Write-AuditLog -Message (
    "ИТОГ: запросов успешно={0}; ошибок={1}; токенов={2}" -f
    $script:SuccessfulRequests, $script:FailedRequests, $script:TotalTokens
) -Level "SUCCESS"

Write-Host ""
Write-Host "============================================================" -ForegroundColor Green
Write-Host "ВНЕШНИЙ АУДИТ ЗАВЕРШЁН" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Green
Write-Host "Итоговый отчёт : $script:FinalReport"
Write-Host "Манифест       : $script:ManifestFile"
Write-Host "Журнал         : $script:LogFile"
Write-Host "Всего токенов  : $script:TotalTokens"
Write-Host "============================================================" -ForegroundColor Green
