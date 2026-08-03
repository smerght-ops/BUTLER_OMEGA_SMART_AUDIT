param(
    [string]$File,
    [string]$ObjectName
)

Write-Host ""
Write-Host "========== GENIE PATCH GATE ==========" -ForegroundColor Cyan

if (!(Test-Path $File)) {
    Write-Host "STATUS : FAIL" -ForegroundColor Red
    Write-Host "REASON : FILE NOT FOUND"
    exit 1
}

$Code = Get-Content $File -Raw -Encoding UTF8

if (-not $Code.Contains($ObjectName)) {
    Write-Host "STATUS : FAIL" -ForegroundColor Red
    Write-Host "REASON : OBJECT NOT FOUND"
    exit 1
}

# =====================================
# STRUCTURE RECONSTRUCTION
# =====================================

$Match = Select-String -Path $File -Pattern ([regex]::Escape($ObjectName)) | Select-Object -First 1

$LineText = $Match.Line
$Indent = $LineText.Length - $LineText.TrimStart().Length

$ObjectType = "UNKNOWN"
if ($LineText.TrimStart().StartsWith("def ")) {
    $ObjectType = "METHOD"
}
elseif ($LineText.TrimStart().StartsWith("class ")) {
    $ObjectType = "CLASS"
}

Write-Host "STATUS : PASS" -ForegroundColor Green
Write-Host "OBJECT : $ObjectName"
Write-Host "TYPE   : $ObjectType"
Write-Host "LINE   : $($Match.LineNumber)"
Write-Host "INDENT : $Indent"
Write-Host ""
Write-Host "RESULT : PATCH ALLOWED" -ForegroundColor Green
Write-Host "======================================"
exit 0
