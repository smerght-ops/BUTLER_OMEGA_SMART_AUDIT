Write-Host ""
Write-Host "========== GENIE STATE ENGINE ==========" -ForegroundColor Cyan
Write-Host ""

$statePath = ".\A_09_GUARDIANS\genie_state.json"

if(!(Test-Path $statePath)){
    Write-Host "STATE FILE NOT FOUND" -ForegroundColor Red
    exit 1
}

$state = Get-Content $statePath -Raw -Encoding UTF8 | ConvertFrom-Json

$state.timestamp = (Get-Date).ToString("yyyy-MM-dd HH:mm:ss")

$RoleManifest =
Get-Content .\A_09_GUARDIANS\role_manifest.json -Raw -Encoding UTF8 |
ConvertFrom-Json

$Files = @{
    Dispatcher=".\\A_02_MANAGERS\\smart_dispatcher_v2.py"
    ReferenceResolver=".\\A_07_MEMORY\\SESSION\\reference_resolver.py"
    SearchDepartment=".\\A_04_AGENTS\\SearchDepartment\\runner.py"
    DocumentsDepartment=".\\A_04_AGENTS\\DocumentsDepartment\\runner.py"
    OpenDocumentDepartment=".\\A_04_AGENTS\\OpenDocumentDepartment\\runner.py"
}

$result=@{}

foreach($role in $RoleManifest.PSObject.Properties){

    $name=$role.Name
    $file=$Files[$name]

    $ok=0
    $total=0

    if(Test-Path $file){

        $content=Get-Content $file -Raw -Encoding UTF8

        foreach($marker in $role.Value.critical){

            $total++

            if($content -match [regex]::Escape($marker)){
                $ok++
            }

        }

    }

    if($total -eq 0){
        $integrity=0
    }
    else{
        $integrity=[math]::Round(($ok/$total)*100)
    }

    if($integrity -eq 100){
        $status="HEALTHY"
    }
    elseif($integrity -ge 80){
        $status="WARNING"
    }
    else{
        $status="CRITICAL"
    }

    $result[$name]=@{
        integrity=$integrity
        status=$status
    }

    Write-Host ("{0,-24} {1,3}%  {2}" -f $name,$integrity,$status)

}

$state.roles=$result

$state |
ConvertTo-Json -Depth 10 |
Set-Content $statePath -Encoding UTF8

Write-Host ""
Write-Host "STATE SAVED -> genie_state.json" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Cyan
