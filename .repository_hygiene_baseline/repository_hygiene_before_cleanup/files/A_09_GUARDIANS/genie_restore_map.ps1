# GENIE RESTORE MAP

$Manifest = ".\A_09_GUARDIANS\criticality_manifest.json"
$Baseline = ".\A_09_GUARDIANS\baseline_path.txt"

Write-Host ""
Write-Host "========== GENIE RESTORE MAP ==========" -ForegroundColor Cyan

if(!(Test-Path $Manifest)){
    Write-Host "Manifest not found." -ForegroundColor Red
    exit 1
}

if(!(Test-Path $Baseline)){
    Write-Host "Baseline path not found." -ForegroundColor Red
    exit 2
}

$base = Get-Content $Baseline -Encoding UTF8

$json = Get-Content $Manifest -Raw -Encoding UTF8 | ConvertFrom-Json

Write-Host ""
Write-Host "[Dispatcher]" -ForegroundColor Yellow

$json.dispatcher.PSObject.Properties | ForEach-Object{

    Write-Host ("{0,-25}  ->  {1}" -f $_.Name,$base)

}

Write-Host ""

Write-Host "[ReferenceResolver]" -ForegroundColor Yellow

$json.resolver.PSObject.Properties | ForEach-Object{

    Write-Host ("{0,-25}  ->  .\A_07_MEMORY\SESSION\reference_resolver.py" -f $_.Name)

}

Write-Host ""

Write-Host "RESTORE MAP READY." -ForegroundColor Green

