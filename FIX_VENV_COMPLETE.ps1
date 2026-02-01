# Complete Venv Fix - Step by Step
# Run this to fix broken venv and install all dependencies

Write-Host "=" * 70 -ForegroundColor Cyan
Write-Host "FIXING BROKEN VENV - COMPLETE PROCESS" -ForegroundColor Yellow
Write-Host "=" * 70 -ForegroundColor Cyan
Write-Host ""

# Step 1: Exit broken venv
Write-Host "[Step 1] Deactivating broken venv..." -ForegroundColor Yellow
if ($env:VIRTUAL_ENV) {
    deactivate
    Write-Host "✅ Deactivated" -ForegroundColor Green
} else {
    Write-Host "✅ No venv active" -ForegroundColor Green
}

# Clear venv from PATH
$env:PATH = ($env:PATH -split ';' | Where-Object { $_ -notlike '*venv*' }) -join ';'
$env:VIRTUAL_ENV = $null

# Step 2: Delete old venv
Write-Host ""
Write-Host "[Step 2] Removing old broken venv..." -ForegroundColor Yellow
$venvPath = Join-Path $PSScriptRoot "venv"
if (Test-Path $venvPath) {
    Remove-Item -Recurse -Force $venvPath -ErrorAction SilentlyContinue
    Start-Sleep -Seconds 2
    Write-Host "✅ Removed old venv" -ForegroundColor Green
} else {
    Write-Host "✅ No old venv found" -ForegroundColor Green
}

# Also check backend/venv
$backendVenvPath = Join-Path $PSScriptRoot "backend\venv"
if (Test-Path $backendVenvPath) {
    Write-Host "Removing backend\venv..." -ForegroundColor Yellow
    Remove-Item -Recurse -Force $backendVenvPath -ErrorAction SilentlyContinue
    Write-Host "✅ Removed backend\venv" -ForegroundColor Green
}

# Step 3: Create new venv
Write-Host ""
Write-Host "[Step 3] Creating new virtual environment..." -ForegroundColor Yellow
Set-Location $PSScriptRoot
python -m venv venv_new

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed. Trying alternative..." -ForegroundColor Red
    py -m venv venv_new
}

Start-Sleep -Seconds 3

# Step 4: Activate new venv
Write-Host ""
Write-Host "[Step 4] Activating new venv..." -ForegroundColor Yellow
if (Test-Path "venv_new\Scripts\Activate.ps1") {
    & "venv_new\Scripts\Activate.ps1"
    Write-Host "✅ Activated venv_new" -ForegroundColor Green
} else {
    Write-Host "❌ Activation script not found" -ForegroundColor Red
    exit 1
}

# Step 5: Test Python
Write-Host ""
Write-Host "[Step 5] Testing Python..." -ForegroundColor Yellow
$pythonVersion = python --version 2>&1
Write-Host "✅ $pythonVersion" -ForegroundColor Green

# Step 6: Install packages
Write-Host ""
Write-Host "[Step 6] Installing packages..." -ForegroundColor Yellow
Write-Host "Installing: pandas, openpyxl, fastapi, uvicorn" -ForegroundColor Cyan

pip install --upgrade pip
pip install pandas openpyxl fastapi uvicorn

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Packages installed successfully!" -ForegroundColor Green
} else {
    Write-Host "⚠️ Some packages may have failed. Check output above." -ForegroundColor Yellow
}

# Step 7: Install backend requirements
Write-Host ""
Write-Host "[Step 7] Installing backend requirements..." -ForegroundColor Yellow
$backendRequirements = Join-Path $PSScriptRoot "backend\requirements.txt"
if (Test-Path $backendRequirements) {
    pip install -r $backendRequirements
    Write-Host "✅ Backend requirements installed" -ForegroundColor Green
} else {
    Write-Host "⚠️ Backend requirements.txt not found" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "=" * 70 -ForegroundColor Cyan
Write-Host "VENV FIX COMPLETE!" -ForegroundColor Green
Write-Host "=" * 70 -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. Activate venv: .\venv_new\Scripts\Activate.ps1" -ForegroundColor White
Write-Host "2. Run backend: cd backend && python main.py" -ForegroundColor White
Write-Host "3. Run demo: python debt-empire\DEMO_WITHOUT_PANDAS.py file:344" -ForegroundColor White
Write-Host ""
