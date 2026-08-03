Write-Host ""
Write-Host "========== GENIE BONE INDEX ==========" -ForegroundColor Cyan
Write-Host ""

$Root = ".\A_09_GUARDIANS\BONE_CACHE"
$Index = @{}

Get-ChildItem $Root -Directory | ForEach-Object {

    $Role = $_.Name

    $Bones = Get-ChildItem $_.FullName -Filter "*.py" |
             Sort-Object LastWriteTime -Descending

    if($Bones.Count -gt 0){

        $Last = $Bones | Select-Object -First 1

        $Index[$Role] = [ordered]@{

            count = $Bones.Count

            lastBone = $Last.Name

            lastWrite = $Last.LastWriteTime.ToString("yyyy-MM-dd HH:mm:ss")

            sha256 = (Get-FileHash $Last.FullName -Algorithm SHA256).Hash

        }

        Write-Host ("[OK] {0,-24} {1} bone(s)" -f $Role,$Bones.Count) -ForegroundColor Green

    }
    else{

        $Index[$Role] = [ordered]@{

            count = 0

            lastBone = ""

            lastWrite = ""

            sha256 = ""

        }

        Write-Host ("[EMPTY] {0}" -f $Role) -ForegroundColor Yellow

    }

}

$Index |
ConvertTo-Json -Depth 5 |
Set-Content ".\A_09_GUARDIANS\BONE_CACHE\bone_index.json" -Encoding UTF8

Write-Host ""
Write-Host "Bone Index updated." -ForegroundColor Green
Write-Host "Saved -> bone_index.json"
Write-Host "======================================" -ForegroundColor Cyan
