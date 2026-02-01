# Install Dependencies for Debt Empire
# Run this script in PowerShell

Write-Host "Installing dependencies for Debt Empire..." -ForegroundColor Green
Write-Host ""

# Method 1: Try with Python 3.12
Write-Host "Method 1: Installing with Python 3.12..." -ForegroundColor Yellow
py -3.12 -m pip install --user pandas openpyxl reportlab

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "SUCCESS! Dependencies installed." -ForegroundColor Green
    Write-Host "You can now run: py -3.12 empire.py" -ForegroundColor Cyan
    exit 0
}

Write-Host ""
Write-Host "Method 1 failed. Trying Method 2..." -ForegroundColor Yellow

# Method 2: Try with trusted hosts (bypass SSL/firewall issues)
Write-Host "Method 2: Installing with trusted hosts..." -ForegroundColor Yellow
py -3.12 -m pip install --user --trusted-host pypi.org --trusted-host files.pythonhosted.org pandas openpyxl reportlab

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "SUCCESS! Dependencies installed." -ForegroundColor Green
    Write-Host "You can now run: py -3.12 empire.py" -ForegroundColor Cyan
    exit 0
}

Write-Host ""
Write-Host "Both methods failed. Possible issues:" -ForegroundColor Red
Write-Host "1. Network/firewall blocking pip"
Write-Host "2. Python 3.12 not properly configured"
Write-Host "3. Corporate proxy blocking downloads"
Write-Host ""
Write-Host "Current status: Script works without dependencies (masters.json only)" -ForegroundColor Yellow
Write-Host "View dashboard.html in browser for visual dashboard" -ForegroundColor Cyan
