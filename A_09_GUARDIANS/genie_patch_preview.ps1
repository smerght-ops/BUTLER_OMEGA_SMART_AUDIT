# GENIE PATCH PREVIEW
# Только просмотр. Никаких изменений в коде.

$BaselineFile = Get-Content .\A_09_GUARDIANS\baseline_path.txt -Encoding UTF8

$CurrentFile = ".\A_02_MANAGERS\smart_dispatcher_v2.py"

Write-Host ""
Write-Host "========== GENIE PATCH PREVIEW ==========" -ForegroundColor Cyan

if(!(Test-Path $BaselineFile)){
    Write-Host "Baseline not found." -ForegroundColor Red
    exit 1
}

$current = Get-Content $CurrentFile -Encoding UTF8
$baseline = Get-Content $BaselineFile -Encoding UTF8

$targets = @(
"_execute_department",
"self.harness.execute",
"def dispatch"
)

foreach($target in $targets){

    Write-Host ""
    Write-Host "----------------------------------------" -ForegroundColor DarkGray
    Write-Host "TARGET : $target" -ForegroundColor Yellow

    $found = $false

    for($i=0;$i -lt $baseline.Count;$i++){

        if($baseline[$i] -match [regex]::Escape($target)){

            $found = $true

            $start = [Math]::Max(0,$i-2)
            $end   = [Math]::Min($baseline.Count-1,$i+10)

            for($j=$start;$j -le $end;$j++){

                "{0,4}: {1}" -f ($j+1),$baseline[$j]

            }

            break
        }
    }

    if(!$found){

        Write-Host "NOT FOUND IN BASELINE" -ForegroundColor Red

    }

}

Write-Host ""
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "PATCH PREVIEW COMPLETE" -ForegroundColor Green
