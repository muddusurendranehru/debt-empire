# Debt Empire Backend - Start with Global Python (Recommended)
# Port: 8000

Write-Host "🚀 Starting Debt Empire Backend (Port 8000) - Global Python..." -ForegroundColor Green

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
    Write-Host "❌ Python not found" -ForegroundColor Red
    exit 1
}
Write-Host "✅ $pythonVersion" -ForegroundColor Green

# Check if requirements installed
Write-Host "Checking requirements..." -ForegroundColor Yellow
try {
    python -c "import fastapi" 2>&1 | Out-Null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ FastAPI installed" -ForegroundColor Green
    } else {
        Write-Host "Installing requirements globally..." -ForegroundColor Yellow
        pip install -r requirements.txt
    }
} catch {
    Write-Host "Installing requirements globally..." -ForegroundColor Yellow
    pip install -r requirements.txt
}

# Start FastAPI server
Write-Host ""
Write-Host "=" * 70 -ForegroundColor Cyan
Write-Host "Starting FastAPI server on http://localhost:8000..." -ForegroundColor Green
Write-Host "=" * 70 -ForegroundColor Cyan
Write-Host ""
python main.py
