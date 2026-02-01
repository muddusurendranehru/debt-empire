# Fix Virtual Environment - Run this first
# Run as Administrator if needed

Write-Host "🔧 Fixing Virtual Environment..." -ForegroundColor Yellow

$backendPath = Join-Path $PSScriptRoot "backend"
Set-Location $backendPath

# Remove broken venv if exists
if (Test-Path "venv") {
    Write-Host "Removing broken venv..." -ForegroundColor Yellow
    Remove-Item -Recurse -Force venv -ErrorAction SilentlyContinue
    Start-Sleep -Seconds 2
}

# Create fresh venv
Write-Host "Creating fresh virtual environment..." -ForegroundColor Green
python -m venv venv --without-pip

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed. Trying alternative method..." -ForegroundColor Red
    py -m venv venv --without-pip
}

if (Test-Path "venv\Scripts\python.exe") {
    Write-Host "✅ Virtual environment created successfully!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Cyan
    Write-Host "1. Activate: .\venv\Scripts\Activate.ps1" -ForegroundColor White
    Write-Host "2. Install pip: python -m ensurepip --upgrade" -ForegroundColor White
    Write-Host "3. Install requirements: pip install -r requirements.txt" -ForegroundColor White
} else {
    Write-Host "❌ Virtual environment creation failed" -ForegroundColor Red
    Write-Host ""
    Write-Host "Alternative: Use global Python (no venv)" -ForegroundColor Yellow
    Write-Host "cd backend" -ForegroundColor White
    Write-Host "pip install -r requirements.txt" -ForegroundColor White
    Write-Host "python main.py" -ForegroundColor White
}
