Write-Host ""
Write-Host "========== GENIE CHANGE LOGGER ==========" -ForegroundColor Cyan
Write-Host ""

$Log = ".\A_09_GUARDIANS\watch_changes.jsonl"

if(!(Test-Path ".\A_09_GUARDIANS\watch_state.json")){
    Write-Host "[FAIL] watch_state.json not found." -ForegroundColor Red
    exit 1
}

$Manifest = Get-Content ".\A_09_GUARDIANS\watch_manifest.json" -Encoding UTF8 | ConvertFrom-Json
$State    = Get-Content ".\A_09_GUARDIANS\watch_state.json" -Encoding UTF8 | ConvertFrom-Json

foreach($File in $Manifest.watch){

    if(!(Test-Path $File)){
        continue
    }

    $Hash = (Get-FileHash $File -Algorithm SHA256).Hash

    if($State.PSObject.Properties.Name -contains $File){

        if($State.$File -ne $Hash){

            $Entry = [ordered]@{
                timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
                file      = $File
                old_hash  = $State.$File
                new_hash  = $Hash
            }

            $Entry |
            ConvertTo-Json -Compress |
            Add-Content $Log -Encoding UTF8

            Write-Host "[CHANGE] $File" -ForegroundColor Yellow

        }

    }

}

Write-Host ""
Write-Host "CHANGE LOG UPDATED." -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Cyan
