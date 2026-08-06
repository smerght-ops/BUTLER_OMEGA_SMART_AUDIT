$ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path

$ContinuousAcceptance = Join-Path $ProjectRoot "RUN_CONTINUOUS_ACCEPTANCE.ps1"
Write-Host "[CHECK] Phase 9 Continuous Acceptance (FULL)" -ForegroundColor Cyan
& $ContinuousAcceptance -AcceptanceMode full
if ($LASTEXITCODE -ne 0) {
    Write-Host "[FAIL] Release blocked by Phase 9 Continuous Acceptance." -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "      BUTLER OMEGA RELEASE CHECK" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

$Profile = Join-Path $ProjectRoot "A_05_STORAGE\user_profile.json"

if (-not (Test-Path $Profile)) {
    Write-Host ""
    Write-Host "[FAIL] user_profile.json не найден." -ForegroundColor Red
    Pause
    exit 1
}

Write-Host "[OK] user_profile.json найден." -ForegroundColor Green

$CompileFiles = @(
    "A_03_ORCHESTRATION\chat_router.py",
    "A_03_ORCHESTRATION\context_builder.py",
    "A_07_MEMORY\profile_manager.py",
    "A_03_ORCHESTRATION\worker.py"
)

foreach ($RelFile in $CompileFiles) {
    $Full = Join-Path $ProjectRoot $RelFile

    if (Test-Path $Full) {
        Write-Host "[CHECK] py_compile -> $RelFile"
        python -m py_compile $Full

        if ($LASTEXITCODE -ne 0) {
            Write-Host ""
            Write-Host "[FAIL] Ошибка компиляции: $RelFile" -ForegroundColor Red
            Pause
            exit 1
        }
    }
}

Write-Host "[OK] py_compile пройден." -ForegroundColor Green

$MemoryTest = Join-Path $ProjectRoot "MEMORY_TEST.bat"

if (Test-Path $MemoryTest) {
    Write-Host "[CHECK] Запуск MEMORY_TEST.bat"
    cmd /c "`"$MemoryTest`""

    if ($LASTEXITCODE -ne 0) {
        Write-Host ""
        Write-Host "[FAIL] MEMORY_TEST завершился с ошибкой." -ForegroundColor Red
        Pause
        exit 1
    }

    Write-Host "[OK] MEMORY_TEST пройден." -ForegroundColor Green

$LabSelfTest = Join-Path $ProjectRoot "A_00_AVARIYKA\LAB_CHAT_ROUTER\self_test.py"

if (Test-Path $LabSelfTest) {

    Write-Host ""
    Write-Host "[CHECK] Запуск LAB_CHAT_ROUTER self_test.py" -ForegroundColor Cyan

    python $LabSelfTest

    if ($LASTEXITCODE -ne 0) {
        Write-Host ""
        Write-Host "[FAIL] LAB_CHAT_ROUTER self_test.py завершился ошибкой." -ForegroundColor Red
        Pause
        exit 1
    }

    Write-Host "[OK] LAB_CHAT_ROUTER self_test.py успешно пройден." -ForegroundColor Green
}

}

$ReleaseRoot = Join-Path $ProjectRoot "A_00_RELEASES"
New-Item -ItemType Directory -Force -Path $ReleaseRoot | Out-Null

$Stamp = Get-Date -Format "yyyyMMdd_HHmmss"
$ReleaseDir = Join-Path $ReleaseRoot ("RELEASE_" + $Stamp)

New-Item -ItemType Directory -Force -Path $ReleaseDir | Out-Null

Copy-Item `
    -Path (Join-Path $ProjectRoot "*") `
    -Destination $ReleaseDir `
    -Recurse `
    -Force `
    -Exclude @(
        "A_00_RELEASES",
        "A_00_HISTORY",
        "A_00_SNAPSHOTS",
        "A_00_ARCHIVE_BACKUPS",
        "__pycache__",
        "*.pyc"
    )

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "RELEASE СОЗДАН УСПЕШНО" -ForegroundColor Green
Write-Host $ReleaseDir -ForegroundColor Cyan
Write-Host "Все проверки пройдены." -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green

Pause
