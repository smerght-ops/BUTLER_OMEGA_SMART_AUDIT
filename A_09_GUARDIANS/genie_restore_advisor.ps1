# GENIE RESTORE ADVISOR v1.0
# Показывает, ЧТО пропало и ОТКУДА восстанавливать

$BASELINE = "C:\Users\KOS\Desktop\Butler_Agent\BUTLER_OMEGA_SMART\A_00_HISTORY\ROLLBACK_POINTS\STABLE_BUTLER_4_22_GREEN_START_20260625_131707\smart_dispatcher_v2.py"
$CURRENT  = ".\A_02_MANAGERS\smart_dispatcher_v2.py"

Write-Host ""
Write-Host "========== GENIE RESTORE ADVISOR ==========" -ForegroundColor Cyan

if (!(Test-Path $BASELINE)) {
    Write-Host "BASELINE NOT FOUND" -ForegroundColor Red
    exit 1
}

if (!(Test-Path $CURRENT)) {
    Write-Host "CURRENT FILE NOT FOUND" -ForegroundColor Red
    exit 1
}

$base = Get-Content $BASELINE -Raw -Encoding UTF8
$curr = Get-Content $CURRENT  -Raw -Encoding UTF8

$restore = @()

function Need($Pattern,$Name){

    if(($base -match $Pattern) -and ($curr -notmatch $Pattern)){
        $script:restore += $Name
    }

}

Need "def _execute_department" "_execute_department"
Need "self\.harness\.execute" "Harness execute"
Need "return self\._execute_department" "Dispatcher routing"
Need "commit_result" "Commit pipeline"
Need "executor=" "Executor wrapper"

Write-Host ""
Write-Host "Baseline :" -NoNewline
Write-Host " $BASELINE" -ForegroundColor DarkGray

Write-Host ""
Write-Host "Current  :" -NoNewline
Write-Host " $CURRENT" -ForegroundColor DarkGray

Write-Host ""
Write-Host "----------- LOST INVARIANTS -----------"

if($restore.Count -eq 0){

    Write-Host "NONE" -ForegroundColor Green

}
else{

    foreach($r in $restore){

        Write-Host "RESTORE -> $r" -ForegroundColor Yellow

    }

}

Write-Host ""
Write-Host "----------- RESTORE PLAN -----------"

switch($restore.Count){

    0 {

        Write-Host "Dispatcher соответствует эталону." -ForegroundColor Green

    }

    default {

        Write-Host "Источник восстановления:" -ForegroundColor White
        Write-Host $BASELINE -ForegroundColor Gray

        Write-Host ""

        Write-Host "Порядок восстановления:" -ForegroundColor White

        $i=1

        foreach($r in $restore){

            Write-Host "$i. $r"

            $i++

        }

    }

}

Write-Host ""
Write-Host "========================================"
