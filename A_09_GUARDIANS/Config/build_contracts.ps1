# ======================================================================
# GENIE V2: CONTRACT BUILDER (PURE GENERATOR)
# ======================================================================
$ConfigDir = $PSScriptRoot
Write-Host "[BUILDER] Запуск генерации контрактов GENIE V2..." -ForegroundColor Cyan

# 1. Сборка объекта Guardians
$GuardiansData = [ordered]@{
    "version" = "1.0"
    "guardians" = [ordered]@{
        "Gate"       = [ordered]@{ "enabled" = $true;  "state" = "MANDATORY"; "script" = "gate.ps1"; "requires" = @() }
        "Candidate"  = [ordered]@{ "enabled" = $true;  "state" = "MANDATORY"; "script" = "candidate.ps1"; "requires" = @("Gate") }
        "Preview"    = [ordered]@{ "enabled" = $false; "state" = "OFF";       "script" = "preview.ps1"; "requires" = @("Candidate") }
        "Validator"  = [ordered]@{ "enabled" = $true;  "state" = "SHADOW";    "script" = "validator.ps1"; "requires" = @("Candidate") }
        "Safety"     = [ordered]@{ "enabled" = $false; "state" = "OFF";       "script" = "safety.ps1"; "requires" = @("Validator") }
        "Confidence" = [ordered]@{ "enabled" = $false; "state" = "OFF";       "script" = "confidence.ps1"; "requires" = @() }
    }
}

# 2. Сборка объекта Pipeline
$PipelineData = [ordered]@{
    "version" = "1.0"
    "pipeline" = @("Gate", "Candidate", "Preview", "Validator", "Safety", "Confidence")
}

# 3. Физическая запись
$GuardiansData | ConvertTo-Json -Depth 5 | Out-File -FilePath "$ConfigDir\guardians.json" -Encoding UTF8
$PipelineData | ConvertTo-Json -Depth 5 | Out-File -FilePath "$ConfigDir\pipeline.json" -Encoding UTF8

Write-Host "[BUILDER] Файлы контрактов (guardians.json, pipeline.json) успешно записаны на диск." -ForegroundColor Green