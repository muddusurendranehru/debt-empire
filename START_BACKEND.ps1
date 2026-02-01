# Debt Empire Backend - Manual Start (PowerShell)
# Port: 8000

Write-Host "🚀 Starting Debt Empire Backend (Port 8000)..." -ForegroundColor Green

$backendPath = Join-Path $PSScriptRoot "backend"

if (-not (Test-Path $backendPath)) {
    Write-Host "❌ Backend folder not found: $backendPath" -ForegroundColor Red
    exit 1
}

Set-Location $backendPath

# Check for virtual environment
if (-not (Test-Path "venv")) {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& "venv\Scripts\Activate.ps1"

# Install requirements if needed
if (-not (Test-Path "venv\.requirements_installed")) {
    Write-Host "Installing requirements..." -ForegroundColor Yellow
    pip install -r requirements.txt
    New-Item -ItemType File -Path "venv\.requirements_installed" -Force | Out-Null
}

# Start FastAPI server
Write-Host "Starting FastAPI server on http://localhost:8000..." -ForegroundColor Green
python main.py
