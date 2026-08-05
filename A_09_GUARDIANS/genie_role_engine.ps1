Write-Host ""
Write-Host "========== GENIE ROLE ENGINE ==========" -ForegroundColor Cyan
Write-Host ""

$Manifest = Get-Content .\A_09_GUARDIANS\role_manifest.json -Raw -Encoding UTF8 | ConvertFrom-Json

$Files = @{
    Dispatcher            = ".\A_02_MANAGERS\smart_dispatcher_v2.py"
    ReferenceResolver     = ".\A_07_MEMORY\SESSION\reference_resolver.py"
    SearchDepartment      = ".\A_04_AGENTS\SearchDepartment\runner.py"
    DocumentsDepartment   = ".\A_04_AGENTS\DocumentsDepartment\runner.py"
    OpenDocumentDepartment= ".\A_04_AGENTS\OpenDocumentDepartment\runner.py"
}

foreach($role in $Manifest.PSObject.Properties){

    $RoleName = $role.Name

    Write-Host "ROLE : $RoleName" -ForegroundColor Yellow

    if(-not $Files.ContainsKey($RoleName)){
        Write-Host "FILE : UNKNOWN"
        Write-Host ""
        continue
    }

    $File = $Files[$RoleName]

    if(-not (Test-Path $File)){
        Write-Host "FILE NOT FOUND"
        Write-Host ""
        continue
    }

    $Content = Get-Content $File -Raw -Encoding UTF8

    $Total = 0
    $Found = 0

    foreach($marker in $role.Value.critical){

        $Total++

        if($Content -match [regex]::Escape($marker)){
            Write-Host "  OK    $marker" -ForegroundColor Green
            $Found++
        }
        else{
            Write-Host "  FAIL  $marker" -ForegroundColor Red
        }
    }

    $Integrity = [math]::Round(($Found/$Total)*100)

    Write-Host ""
    Write-Host "Integrity : $Integrity%" -ForegroundColor Cyan

    if($Integrity -eq 100){
        Write-Host "STATUS : HEALTHY" -ForegroundColor Green
    }
    elseif($Integrity -ge 80){
        Write-Host "STATUS : WARNING" -ForegroundColor Yellow
    }
    else{
        Write-Host "STATUS : CRITICAL" -ForegroundColor Red
    }

    Write-Host ""
}

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "ROLE ENGINE COMPLETE."
