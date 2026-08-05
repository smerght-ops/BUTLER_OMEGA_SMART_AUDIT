Write-Host ""
Write-Host "========== GENIE BONE CACHE ==========" -ForegroundColor Cyan
Write-Host ""

$Root = ".\A_09_GUARDIANS\BONE_CACHE"

$Folders = @(
    "Dispatcher",
    "Harness",
    "ReferenceResolver",
    "Passport",
    "SearchDepartment",
    "DocumentsDepartment",
    "OpenDocumentDepartment"
)

if(!(Test-Path $Root)){
    New-Item -ItemType Directory -Path $Root | Out-Null
    Write-Host "[OK] Root created"
}

foreach($Folder in $Folders){

    $Path = Join-Path $Root $Folder

    if(!(Test-Path $Path)){
        New-Item -ItemType Directory -Path $Path | Out-Null
        Write-Host ("[OK] {0}" -f $Folder) -ForegroundColor Green
    }
    else{
        Write-Host ("[EXISTS] {0}" -f $Folder) -ForegroundColor Yellow
    }

}

$Manifest = [ordered]@{

    version = "1.0"

    max_bones = 5

    strategy = "ROTATING"

    created = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

    description = "GENIE Bone Cache"

}

$Manifest |
ConvertTo-Json |
Set-Content ".\A_09_GUARDIANS\bone_manifest.json" -Encoding UTF8

Write-Host ""
Write-Host "Bone Cache initialized." -ForegroundColor Green
Write-Host "Rotation : 5 bones per role"
Write-Host "=======================================" -ForegroundColor Cyan
