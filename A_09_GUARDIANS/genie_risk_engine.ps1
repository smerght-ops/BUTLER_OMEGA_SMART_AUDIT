# GENIE RISK ENGINE v1.0

$ManifestPath = ".\A_09_GUARDIANS\criticality_manifest.json"
$DispatcherPath = ".\A_02_MANAGERS\smart_dispatcher_v2.py"
$ResolverPath = ".\A_07_MEMORY\SESSION\reference_resolver.py"

$Manifest = Get-Content $ManifestPath -Raw -Encoding UTF8 | ConvertFrom-Json
$Dispatcher = Get-Content $DispatcherPath -Raw -Encoding UTF8
$Resolver = Get-Content $ResolverPath -Raw -Encoding UTF8

$Violations = @()

function Test-RuleGroup {
    param(
        [string]$GroupName,
        [object]$Rules,
        [string]$Content
    )

    foreach($p in $Rules.PSObject.Properties){
        $rule = $p.Value
        if($Content -notmatch $rule.pattern){
            $script:Violations += [PSCustomObject]@{
                Group    = $GroupName
                Name     = $p.Name
                Severity = $rule.severity
                Impact   = $rule.impact
            }
        }
    }
}

Test-RuleGroup "Dispatcher" $Manifest.dispatcher $Dispatcher
Test-RuleGroup "ReferenceResolver" $Manifest.resolver $Resolver

$Risk = "LOW"

if($Violations | Where-Object Severity -eq "CRITICAL"){
    $Risk = "CRITICAL"
}
elseif($Violations | Where-Object Severity -eq "HIGH"){
    $Risk = "HIGH"
}
elseif($Violations | Where-Object Severity -eq "MEDIUM"){
    $Risk = "MEDIUM"
}

Write-Host ""
Write-Host "========== GENIE RISK ENGINE ==========" -ForegroundColor Cyan

if($Violations.Count -eq 0){
    Write-Host "No architecture violations detected." -ForegroundColor Green
}
else{
    foreach($v in $Violations){
        Write-Host ("[{0}] {1}::{2}" -f $v.Severity,$v.Group,$v.Name) -ForegroundColor Red
        if($v.Impact){
            Write-Host ("      Impact: {0}" -f $v.Impact) -ForegroundColor DarkYellow
        }
    }
}

Write-Host ""
Write-Host "TOTAL VIOLATIONS : $($Violations.Count)"
Write-Host "TOTAL RISK       : $Risk"

if($Risk -eq "CRITICAL"){
    Write-Host "RELEASE GATE     : BLOCKED" -ForegroundColor Red
}
elseif($Risk -eq "HIGH"){
    Write-Host "RELEASE GATE     : BLOCKED" -ForegroundColor Red
}
else{
    Write-Host "RELEASE GATE     : ALLOWED" -ForegroundColor Green
}

Write-Host "=======================================" -ForegroundColor Cyan
