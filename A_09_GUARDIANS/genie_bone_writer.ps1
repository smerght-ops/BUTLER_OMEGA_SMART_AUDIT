Write-Host ""
Write-Host "========== GENIE BONE WRITER ==========" -ForegroundColor Cyan
Write-Host ""

$Role = "Dispatcher"
$Source = ".\A_02_MANAGERS\smart_dispatcher_v2.py"
$BoneRoot = ".\A_09_GUARDIANS\BONE_CACHE\$Role"
$MaxBones = 5

if(!(Test-Path $Source)){
    Write-Host "[FAIL] Source file not found: $Source" -ForegroundColor Red
    exit 1
}

if(!(Test-Path $BoneRoot)){
    New-Item -ItemType Directory -Force -Path $BoneRoot | Out-Null
}

$ExistingBones = Get-ChildItem $BoneRoot -Filter "*.py" | Sort-Object LastWriteTime

while($ExistingBones.Count -ge $MaxBones){
    $Oldest = $ExistingBones | Select-Object -First 1
    $Meta = [System.IO.Path]::ChangeExtension($Oldest.FullName, ".json")

    Remove-Item $Oldest.FullName -Force
    if(Test-Path $Meta){
        Remove-Item $Meta -Force
    }

    Write-Host "[ROTATE] Removed oldest bone: $($Oldest.Name)" -ForegroundColor Yellow

    $ExistingBones = Get-ChildItem $BoneRoot -Filter "*.py" | Sort-Object LastWriteTime
}

$Stamp = Get-Date -Format "yyyyMMdd_HHmmss"
$BoneName = "${Role}_bone_$Stamp.py"
$BonePath = Join-Path $BoneRoot $BoneName

Copy-Item $Source $BonePath -Force

$Hash = (Get-FileHash $BonePath -Algorithm SHA256).Hash

$Meta = [ordered]@{
    role = $Role
    source = $Source
    bone = $BonePath
    created = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    sha256 = $Hash
    reason = "Before critical modification"
    max_bones = $MaxBones
    genie = "WATCHDOG_BONE_WRITER_4.30.2"
}

$MetaPath = [System.IO.Path]::ChangeExtension($BonePath, ".json")

$Meta |
ConvertTo-Json -Depth 5 |
Set-Content $MetaPath -Encoding UTF8

Write-Host "[OK] Bone buried." -ForegroundColor Green
Write-Host "Role : $Role"
Write-Host "File : $BonePath"
Write-Host "Meta : $MetaPath"
Write-Host "Hash : $Hash"
Write-Host ""
Write-Host "=======================================" -ForegroundColor Cyan
