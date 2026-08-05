# GENIE FIND BASELINE

Write-Host ""
Write-Host "=========== GENIE BASELINE SCAN ===========" -ForegroundColor Cyan

$Candidates = Get-ChildItem . -Recurse -Filter smart_dispatcher_v2.py |
Sort-Object LastWriteTime -Descending

if($Candidates.Count -eq 0){
    Write-Host "Dispatcher not found." -ForegroundColor Red
    return
}

Write-Host ""
Write-Host "Найденные кандидаты:" -ForegroundColor Yellow

$i=1

foreach($f in $Candidates){

    Write-Host ("[{0}] {1}" -f $i,$f.FullName)

    $i++
}

Write-Host ""
Write-Host "=========== END SCAN ===========" -ForegroundColor Cyan
