$Baseline = Get-Content .\A_09_GUARDIANS\baseline_path.txt
$Current  = ".\A_02_MANAGERS\smart_dispatcher_v2.py"

Write-Host ""
Write-Host "========== GENIE AUTO RESTORE ADVISOR ==========" -ForegroundColor Cyan
Write-Host ""

$CurrentText  = Get-Content $Current  -Raw -Encoding UTF8
$BaselineText = Get-Content $Baseline -Raw -Encoding UTF8

$Targets = @(
    "def _execute_department",
    "self.harness.execute",
    "def dispatch"
)

foreach($Target in $Targets){

    Write-Host "--------------------------------------------"

    if($CurrentText.Contains($Target)){
        Write-Host "[OK] PRESENT : $Target" -ForegroundColor Green
        continue
    }

    Write-Host "[MISSING] $Target" -ForegroundColor Red

    $lines = Get-Content $Baseline -Encoding UTF8

    for($i=0;$i -lt $lines.Count;$i++){

        if($lines[$i] -match [regex]::Escape($Target)){

            Write-Host "Suggested source:"
            Write-Host "Line $($i+1)"

            $from=[Math]::Max(0,$i-3)
            $to=[Math]::Min($lines.Count-1,$i+12)

            for($j=$from;$j -le $to;$j++){

                "{0,4}: {1}" -f ($j+1),$lines[$j]

            }

            break

        }

    }

}

Write-Host ""
Write-Host "=============================================="
Write-Host "AUTO RESTORE ADVICE COMPLETE."
