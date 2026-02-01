# Fix Broken Virtual Environment
# Run this when you see "failed to locate pyvenv.cfg"

Write-Host "🔧 Fixing Broken Virtual Environment..." -ForegroundColor Yellow

$backendPath = Join-Path $PSScriptRoot "backend"
Set-Location $backendPath

# Step 1: Deactivate current venv
Write-Host "Step 1: Deactivating broken venv..." -ForegroundColor Cyan
if ($env:VIRTUAL_ENV) {
    deactivate
    Write-Host "✅ Deactivated" -ForegroundColor Green
}

# Step 2: Remove broken venv
Write-Host "Step 2: Removing broken venv folder..." -ForegroundColor Cyan
if (Test-Path "venv") {
    Remove-Item -Recurse -Force venv -ErrorAction SilentlyContinue
    Start-Sleep -Seconds 2
    Write-Host "✅ Removed broken venv" -ForegroundColor Green
}

# Step 3: Create fresh venv
Write-Host "Step 3: Creating fresh virtual environment..." -ForegroundColor Cyan
python -m venv venv

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed. Trying alternative..." -ForegroundColor Red
    py -m venv venv
}

Start-Sleep -Seconds 3

# Step 4: Verify venv created
if (Test-Path "venv\pyvenv.cfg") {
    Write-Host "✅ Virtual environment created successfully!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Cyan
    Write-Host "1. Activate: .\venv\Scripts\Activate.ps1" -ForegroundColor White
    Write-Host "2. Install requirements: pip install -r requirements.txt" -ForegroundColor White
    Write-Host "3. Run server: python main.py" -ForegroundColor White
} else {
    Write-Host "❌ Virtual environment creation failed" -ForegroundColor Red
    Write-Host ""
    Write-Host "RECOMMENDED: Use global Python instead" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Run these commands:" -ForegroundColor Cyan
    Write-Host "  deactivate" -ForegroundColor White
    Write-Host "  pip install -r requirements.txt" -ForegroundColor White
    Write-Host "  python main.py" -ForegroundColor White
}
