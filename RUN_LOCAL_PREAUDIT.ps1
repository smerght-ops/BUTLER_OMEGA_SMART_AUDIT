param(
    [int]$Chunks = 0
)

$ErrorActionPreference = "Stop"

$Pack = Join-Path $PSScriptRoot "PROJECT_TECHNICAL_AUDIT_PACK_V2.md"
$Out  = Join-Path $PSScriptRoot "LOCAL_AUDIT_OUTPUT_TEST"

$Model = "DeepSeek-Coder-V2-Lite-Instruct-Q6_K:latest"
$Uri   = "http://127.0.0.1:11434/api/generate"

# Уменьшаем и контекст, и размер чанка.
$ContextSize = 32768
$MaxChars    = 70000

if (!(Test-Path $Pack)) {
    throw "Не найден пакет: $Pack"
}

New-Item -ItemType Directory -Path $Out -Force | Out-Null

$Text = Get-Content $Pack -Raw -Encoding UTF8

# Разделение строго перед каждым FILE-блоком.
$Parts = [regex]::Split(
    $Text,
    '(?m)(?=^## FILE:\s)'
) | Where-Object { $_.Trim().Length -gt 0 }

$ChunkList = [System.Collections.Generic.List[string]]::new()
$Current = [System.Text.StringBuilder]::new()

foreach ($Part in $Parts) {

    if ($Current.Length -gt 0 -and
        ($Current.Length + $Part.Length) -gt $MaxChars) {

        $ChunkList.Add($Current.ToString())
        $Current.Clear() | Out-Null
    }

    # Большой FILE-блок не разрезаем посередине.
    if ($Part.Length -gt $MaxChars -and $Current.Length -eq 0) {
        $ChunkList.Add($Part)
    }
    else {
        [void]$Current.Append($Part)
    }
}

if ($Current.Length -gt 0) {
    $ChunkList.Add($Current.ToString())
}

$RunCount = $ChunkList.Count

if ($Chunks -gt 0) {
    $RunCount = [Math]::Min($Chunks, $ChunkList.Count)
}

Write-Host "PACK      : $Pack" -ForegroundColor Cyan
Write-Host "MODEL     : $Model" -ForegroundColor Cyan
Write-Host "ALL CHUNKS: $($ChunkList.Count)" -ForegroundColor Cyan
Write-Host "THIS RUN  : $RunCount" -ForegroundColor Cyan
Write-Host "NUM_CTX   : $ContextSize" -ForegroundColor Cyan
Write-Host ""

for ($i = 0; $i -lt $RunCount; $i++) {

    $N = $i + 1
    $ResultFile = Join-Path $Out ("CHUNK_{0:D3}_AUDIT.md" -f $N)

    $Prompt = @"
Ты выполняешь ДОКАЗАТЕЛЬНЫЙ ПРЕДВАРИТЕЛЬНЫЙ АУДИТ
проекта Butler Omega Smart.

ВАЖНО: весь текст для анализа УЖЕ ПЕРЕДАН НИЖЕ.

Тебе НЕ требуется:
- открывать файлы;
- получать доступ к файловой системе;
- выполнять код;
- изменять код;
- обращаться к Интернету.

Ты должен ТОЛЬКО ПРОЧИТАТЬ И ПРОАНАЛИЗИРОВАТЬ
предоставленный ниже текст.

Это ОДИН ФРАГМЕНТ большого проекта.

Поэтому ЗАПРЕЩЕНО объявлять компонент DEAD или DELETE CANDIDATE
только потому, что его вызов не найден в этом фрагменте.

Если доказательств недостаточно, используй:
REQUIRES_CROSS_CHUNK_VERIFICATION.

Для КАЖДОГО существенного обнаруженного компонента укажи:

1. FILE
2. SYMBOL — класс, функция или объект
3. ROLE
4. IMPORTS
5. CALLS_OR_REFERENCES
6. EVIDENCE — конкретный фрагмент доказательства
7. PRELIMINARY_STATUS:
   KEEP_EVIDENCE
   RUNTIME_EVIDENCE
   MEMORY_EVIDENCE
   SECURITY_EVIDENCE
   DUPLICATE_SUSPECT
   OFFLINE_TOOL
   REQUIRES_CROSS_CHUNK_VERIFICATION

Отдельно сформируй:

RUNTIME_EVIDENCE
MEMORY_EVIDENCE
SECURITY_EVIDENCE
SSOT_EVIDENCE
DUPLICATE_EVIDENCE

Не придумывай отсутствующие связи.
Не делай глобальных выводов обо всём проекте.
Не отказывайся от анализа.
Не отвечай, что не можешь читать файлы:
их содержимое уже находится перед тобой.

Ответ дай в Markdown.
Для каждого вывода обязательно указывай FILE и SYMBOL.

========================
ТЕКСТ ДЛЯ АНАЛИЗА
========================

$($ChunkList[$i])
"@

    $Body = @{
        model  = $Model
        prompt = $Prompt
        stream = $false
        options = @{
            num_ctx = $ContextSize
            temperature = 0.1
        }
    } | ConvertTo-Json -Depth 10

    Write-Host "[$N/$RunCount] Анализ..." -ForegroundColor Yellow

    try {
        $Response = Invoke-RestMethod `
            -Uri $Uri `
            -Method Post `
            -ContentType "application/json; charset=utf-8" `
            -Body ([Text.Encoding]::UTF8.GetBytes($Body)) `
            -TimeoutSec 3600

        $Response.response |
            Set-Content $ResultFile -Encoding UTF8

        Write-Host "OK: $ResultFile" -ForegroundColor Green
    }
    catch {
        Write-Host "FAIL CHUNK $N" -ForegroundColor Red
        Write-Host $_.Exception.Message -ForegroundColor Red
        break
    }
}

Write-Host ""
Write-Host "=== ТЕСТОВЫЙ ЛОКАЛЬНЫЙ АУДИТ ЗАВЕРШЁН ===" -ForegroundColor Green
Write-Host "Результаты: $Out"
