# CASS Intelligence Reports — Portal Launcher
# Run: .\start_portal.ps1

$ErrorActionPreference = "Stop"
$Root = $PSScriptRoot

Write-Host ""
Write-Host "  ╔══════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "  ║        CASS Intelligence Reports Portal          ║" -ForegroundColor Cyan
Write-Host "  ║        FCA · CASS · Cyber · Physical Security    ║" -ForegroundColor Cyan
Write-Host "  ╚══════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# Check Python
try {
    $py = & python --version 2>&1
    Write-Host "  [OK] Python: $py" -ForegroundColor Green
} catch {
    Write-Host "  [!] Python not found. Install Python 3.10+." -ForegroundColor Red
    exit 1
}

# Install / verify deps
Write-Host "  [>>] Checking dependencies..." -ForegroundColor Yellow
python -m pip install -q -r "$Root\requirements.txt"
Write-Host "  [OK] Dependencies ready" -ForegroundColor Green

# Check .env
$envFile = "$Root\.env"
if (Test-Path $envFile) {
    Write-Host "  [OK] .env found" -ForegroundColor Green
} else {
    Write-Host "  [!] .env not found — AI scans will be disabled" -ForegroundColor Yellow
}

# Create .tmp if needed
$tmpDir = "$Root\.tmp"
if (-not (Test-Path $tmpDir)) { New-Item -ItemType Directory -Path $tmpDir | Out-Null }

Write-Host ""
Write-Host "  Starting portal at http://localhost:8080" -ForegroundColor Cyan
Write-Host "  Press Ctrl+C to stop" -ForegroundColor DarkGray
Write-Host ""

# Launch
Set-Location $Root
python -m uvicorn api.gateway:app --host 0.0.0.0 --port 8080 --reload
