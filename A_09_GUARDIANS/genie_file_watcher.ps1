Write-Host ""
Write-Host "========== GENIE FILE WATCHER ==========" -ForegroundColor Cyan
Write-Host ""

$ManifestPath = ".\A_09_GUARDIANS\watch_manifest.json"
$StatePath    = ".\A_09_GUARDIANS\watch_state.json"

if(!(Test-Path $ManifestPath)){
    Write-Host "[FAIL] watch_manifest.json not found." -ForegroundColor Red
    exit 1
}

$Manifest = Get-Content $ManifestPath -Encoding UTF8 | ConvertFrom-Json

$OldState = @{}

if(Test-Path $StatePath){

    $Old = Get-Content $StatePath -Encoding UTF8 | ConvertFrom-Json

    foreach($P in $Old.PSObject.Properties){
        $OldState[$P.Name] = $P.Value
    }

}

$NewState = [ordered]@{}

foreach($File in $Manifest.watch){

    if(!(Test-Path $File)){
        Write-Host "[MISS] $File" -ForegroundColor Yellow
        continue
    }

    $Hash = (Get-FileHash $File -Algorithm SHA256).Hash

    $NewState[$File] = $Hash

    if($OldState.ContainsKey($File)){

        if($OldState[$File] -ne $Hash){

            Write-Host "[CHANGED] $File" -ForegroundColor Yellow

            & ".\A_09_GUARDIANS\genie_watchdog.ps1" -Silent

        }

    }
    else{

        Write-Host "[NEW] $File" -ForegroundColor Green

    }

}

$NewState |
ConvertTo-Json |
Set-Content $StatePath -Encoding UTF8

Write-Host ""
Write-Host "WATCH STATE UPDATED." -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Cyan
