Write-Host ""
Write-Host "========== GENIE BARK ENGINE ==========" -ForegroundColor Cyan
Write-Host ""

$IndexFile = ".\A_09_GUARDIANS\BONE_CACHE\bone_index.json"

if(!(Test-Path $IndexFile)){
    Write-Host "[FAIL] bone_index.json not found." -ForegroundColor Red
    exit 1
}

$Index = Get-Content $IndexFile -Encoding UTF8 | ConvertFrom-Json

foreach($Role in $Index.PSObject.Properties){

    $Name = $Role.Name
    $Info = $Role.Value

    Write-Host "🐕 $Name" -ForegroundColor Cyan

    if($Info.count -eq 0){

        Write-Host "  STATUS : NO BONE" -ForegroundColor Yellow
        Write-Host "  Bark   : No backup has been buried yet."
        Write-Host ""

        continue
    }

    Write-Host ("  Bones  : {0}" -f $Info.count)
    Write-Host ("  Latest : {0}" -f $Info.lastBone)
    Write-Host ("  Time   : {0}" -f $Info.lastWrite)

    $Age = (Get-Date) - [datetime]$Info.lastWrite

    if($Age.TotalMinutes -lt 30){

        Write-Host "  STATUS : CALM" -ForegroundColor Green
        Write-Host "  Bark   : Everything is under control."

    }
    elseif($Age.TotalHours -lt 24){

        Write-Host "  STATUS : WATCH" -ForegroundColor Yellow
        Write-Host "  Bark   : Consider running GENIE."

    }
    else{

        Write-Host "  STATUS : ALERT" -ForegroundColor Red
        Write-Host "  Bark   : Bone is old. Architecture should be checked."

    }

    Write-Host ""

}

Write-Host "=======================================" -ForegroundColor Cyan
Write-Host "GENIE BARK COMPLETE." -ForegroundColor Green
