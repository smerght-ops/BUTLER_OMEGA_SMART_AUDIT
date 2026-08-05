# GENIE Guardian v1.1
# Проверка архитектуры через manifest

$ManifestPath = ".\A_09_GUARDIANS\architecture_manifest.json"

if (!(Test-Path $ManifestPath)) {
    Write-Host "Manifest not found." -ForegroundColor Red
    return
}

$manifest = Get-Content $ManifestPath -Raw -Encoding UTF8 | ConvertFrom-Json

$checks = @(
    @{
        Name = "Dispatcher"
        File = ".\A_02_MANAGERS\smart_dispatcher_v2.py"
        Rules = $manifest.dispatcher
    },
    @{
        Name = "ReferenceResolver"
        File = ".\A_07_MEMORY\SESSION\reference_resolver.py"
        Rules = $manifest.reference_resolver
    }
)

$Failed = $false

Write-Host ""
Write-Host "========== GENIE MANIFEST AUDIT ==========" -ForegroundColor Cyan

foreach ($check in $checks) {

    Write-Host ""
    Write-Host "[$($check.Name)]" -ForegroundColor Yellow

    if (!(Test-Path $check.File)) {
        Write-Host "  FILE NOT FOUND" -ForegroundColor Red
        $Failed = $true
        continue
    }

    $content = Get-Content $check.File -Raw -Encoding UTF8

    foreach ($m in $check.Rules.required_methods) {

        if ($content -match ("def\s+" + [regex]::Escape($m))) {
            Write-Host "  OK METHOD   $m" -ForegroundColor Green
        }
        else {
            Write-Host "  FAIL METHOD $m" -ForegroundColor Red
            $Failed = $true
        }

    }

    if ($check.Rules.PSObject.Properties.Name -contains "required_imports") {

        foreach ($i in $check.Rules.required_imports) {

            if ($content.Contains($i)) {
                Write-Host "  OK IMPORT   $i" -ForegroundColor Green
            }
            else {
                Write-Host "  FAIL IMPORT $i" -ForegroundColor Red
                $Failed = $true
            }

        }

    }

    if ($check.Rules.PSObject.Properties.Name -contains "required_calls") {

        foreach ($c in $check.Rules.required_calls) {

            if ($content.Contains($c)) {
                Write-Host "  OK CALL     $c" -ForegroundColor Green
            }
            else {
                Write-Host "  FAIL CALL   $c" -ForegroundColor Red
                $Failed = $true
            }

        }

    }

    if ($check.Rules.PSObject.Properties.Name -contains "required_constants") {

        foreach ($k in $check.Rules.required_constants) {

            if ($content.Contains($k)) {
                Write-Host "  OK CONST    $k" -ForegroundColor Green
            }
            else {
                Write-Host "  FAIL CONST  $k" -ForegroundColor Red
                $Failed = $true
            }

        }

    }

}

Write-Host ""
Write-Host "==========================================" -ForegroundColor Cyan

if ($Failed) {
    Write-Host "GENIE RESULT : FAILED" -ForegroundColor Red
}
else {
    Write-Host "GENIE RESULT : PASSED" -ForegroundColor Green
}
