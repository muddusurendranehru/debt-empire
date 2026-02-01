# Debt Empire Backend - Manual Start (PowerShell) - FIXED
# Port: 8000

Write-Host "🚀 Starting Debt Empire Backend (Port 8000)..." -ForegroundColor Green

$backendPath = Join-Path $PSScriptRoot "backend"

if (-not (Test-Path $backendPath)) {
    Write-Host "❌ Backend folder not found: $backendPath" -ForegroundColor Red
    exit 1
}

Set-Location $backendPath
Write-Host "Current directory: $(Get-Location)" -ForegroundColor Yellow

# Check Python
Write-Host "Checking Python..." -ForegroundColor Yellow
$pythonVersion = python --version 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Python not found. Please install Python 3.8+" -ForegroundColor Red
    Write-Host "Try: py --version or python3 --version" -ForegroundColor Yellow
    exit 1
}
Write-Host "✅ $pythonVersion" -ForegroundColor Green

# Check for virtual environment
if (-not (Test-Path "venv")) {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Failed to create venv. Trying alternative..." -ForegroundColor Red
        py -m venv venv
        if ($LASTEXITCODE -ne 0) {
            Write-Host "❌ Virtual environment creation failed" -ForegroundColor Red
            exit 1
        }
    }
    Write-Host "✅ Virtual environment created" -ForegroundColor Green
} else {
    Write-Host "✅ Virtual environment already exists" -ForegroundColor Green
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
if (Test-Path "venv\Scripts\Activate.ps1") {
    & "venv\Scripts\Activate.ps1"
} else {
    Write-Host "❌ Activation script not found" -ForegroundColor Red
    exit 1
}

# Install requirements if needed
if (-not (Test-Path "venv\.requirements_installed")) {
    Write-Host "Installing requirements..." -ForegroundColor Yellow
    pip install -r requirements.txt
    if ($LASTEXITCODE -eq 0) {
        New-Item -ItemType File -Path "venv\.requirements_installed" -Force | Out-Null
        Write-Host "✅ Requirements installed" -ForegroundColor Green
    } else {
        Write-Host "⚠️ Requirements installation had issues" -ForegroundColor Yellow
    }
} else {
    Write-Host "✅ Requirements already installed" -ForegroundColor Green
}

# Start FastAPI server
Write-Host ""
Write-Host "=" * 70 -ForegroundColor Cyan
Write-Host "Starting FastAPI server on http://localhost:8000..." -ForegroundColor Green
Write-Host "=" * 70 -ForegroundColor Cyan
Write-Host ""
python main.py
