param(
    [ValidateSet("fast", "full")]
    [string]$AcceptanceMode = "fast"
)

$ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$Gate = Join-Path $ProjectRoot "A_99_TESTS\continuous_acceptance.py"
$ConfiguredPython = Join-Path $ProjectRoot ".butler_python_path"

if (-not (Test-Path -LiteralPath $ConfiguredPython -PathType Leaf)) {
    Write-Error "CANONICAL_PYTHON_CONFIG_MISSING: $ConfiguredPython"
    exit 2
}
$PythonExe = (Get-Content -LiteralPath $ConfiguredPython -Raw).Trim()
if (-not (Test-Path -LiteralPath $PythonExe -PathType Leaf)) {
    Write-Error "CANONICAL_PYTHON_UNAVAILABLE: $PythonExe"
    exit 2
}

& $PythonExe $Gate --acceptance-mode $AcceptanceMode
exit $LASTEXITCODE
