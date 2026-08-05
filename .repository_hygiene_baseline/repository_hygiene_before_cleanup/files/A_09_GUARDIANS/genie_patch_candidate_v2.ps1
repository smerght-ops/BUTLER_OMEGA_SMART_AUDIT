param(
    [string]$File,
    [string]$ObjectName
)

Write-Host ""
Write-Host "========== GENIE PATCH CANDIDATE ==========" -ForegroundColor Cyan

if (!(Test-Path $File)) {
    Write-Host "STATUS : FAIL" -ForegroundColor Red
    Write-Host "REASON : FILE NOT FOUND"
    exit 1
}

if ([string]::IsNullOrWhiteSpace($ObjectName)) {
    Write-Host "STATUS : FAIL" -ForegroundColor Red
    Write-Host "REASON : OBJECT NAME EMPTY"
    exit 1
}

Write-Host "STATUS : INPUT VERIFIED" -ForegroundColor Green

exit 0
