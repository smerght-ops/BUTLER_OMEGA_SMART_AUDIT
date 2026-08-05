# GENIE Architecture Diff v1

$Current = ".\A_02_MANAGERS\smart_dispatcher_v2.py"

$BaselineDir = Get-ChildItem .\A_00_HISTORY\ROLLBACK_POINTS -Directory |
Where-Object {$_.Name -match "STABLE"} |
Sort-Object LastWriteTime -Descending |
Select-Object -First 1

if($null -eq $BaselineDir){
    Write-Host "Baseline not found." -ForegroundColor Red
    return
}

$Baseline = Get-ChildItem $BaselineDir.FullName -Recurse -Filter smart_dispatcher_v2.py |
Select-Object -First 1

if($null -eq $Baseline){
    Write-Host "Dispatcher not found inside baseline." -ForegroundColor Red
    return
}

$currentContent = Get-Content $Current -Raw -Encoding UTF8
$baselineContent = Get-Content $Baseline.FullName -Raw -Encoding UTF8

Write-Host ""
Write-Host "========== GENIE ARCHITECTURE DIFF ==========" -ForegroundColor Cyan

$Methods = @(
"_execute_department",
"dispatch"
)

foreach($m in $Methods){

    $old = $baselineContent -match ("def\s+"+[regex]::Escape($m))
    $new = $currentContent -match ("def\s+"+[regex]::Escape($m))

    if($old -and $new){
        Write-Host "[OK]   METHOD $m" -ForegroundColor Green
    }
    elseif($old -and -not $new){
        Write-Host "[FAIL] METHOD REMOVED -> $m" -ForegroundColor Red
    }
    elseif(-not $old -and $new){
        Write-Host "[INFO] METHOD ADDED   -> $m" -ForegroundColor Yellow
    }

}

$Calls=@(
"self.harness.execute"
)

foreach($c in $Calls){

    $old=$baselineContent.Contains($c)
    $new=$currentContent.Contains($c)

    if($old -and $new){
        Write-Host "[OK]   CALL $c" -ForegroundColor Green
    }
    elseif($old -and -not $new){
        Write-Host "[FAIL] CALL REMOVED -> $c" -ForegroundColor Red
    }
    elseif(-not $old -and $new){
        Write-Host "[INFO] CALL ADDED -> $c" -ForegroundColor Yellow
    }

}

Write-Host "============================================" -ForegroundColor Cyan
