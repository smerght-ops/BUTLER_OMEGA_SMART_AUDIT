# GENIE v2
# Manifest Driven Guardian

$Manifest = Get-Content `
".\A_09_GUARDIANS\criticality_manifest.json" `
-Raw `
-Encoding UTF8 |
ConvertFrom-Json

$Dispatcher = Get-Content `
".\A_02_MANAGERS\smart_dispatcher_v2.py" `
-Raw `
-Encoding UTF8

$Resolver = Get-Content `
".\A_07_MEMORY\SESSION\reference_resolver.py" `
-Raw `
-Encoding UTF8

$Failed = $false

Write-Host ""
Write-Host "========== GENIE MANIFEST ENGINE ==========" -ForegroundColor Cyan

Write-Host ""
Write-Host "[Dispatcher]" -ForegroundColor Yellow

foreach($p in $Manifest.dispatcher.PSObject.Properties){

    $rule = $p.Value

    if($Dispatcher -match $rule.pattern){

        Write-Host (" OK  {0,-28} [{1}]" -f $p.Name,$rule.severity) -ForegroundColor Green

    }
    else{

        Write-Host ("FAIL {0,-28} [{1}]" -f $p.Name,$rule.severity) -ForegroundColor Red

        Write-Host ("      Impact : {0}" -f $rule.impact) -ForegroundColor DarkYellow

        $Failed = $true

    }

}

Write-Host ""
Write-Host "[ReferenceResolver]" -ForegroundColor Yellow

foreach($p in $Manifest.resolver.PSObject.Properties){

    $rule = $p.Value

    if($Resolver -match $rule.pattern){

        Write-Host (" OK  {0,-28} [{1}]" -f $p.Name,$rule.severity) -ForegroundColor Green

    }
    else{

        Write-Host ("FAIL {0,-28} [{1}]" -f $p.Name,$rule.severity) -ForegroundColor Red

        $Failed = $true

    }

}

Write-Host ""
Write-Host "==========================================="

if($Failed){

    Write-Host "GENIE STATUS : FAILED" -ForegroundColor Red

}else{

    Write-Host "GENIE STATUS : PASSED" -ForegroundColor Green

}
