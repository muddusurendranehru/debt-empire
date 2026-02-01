# Run EMPIRE Function (Simple Version - No pandas/reportlab needed)

# Clear broken venv
$env:VIRTUAL_ENV = $null
$env:PATH = ($env:PATH -split ';' | Where-Object { $_ -notlike '*venv*' }) -join ';'

# Navigate to debt-empire
Set-Location "debt-empire"

Write-Host "Running EMPIRE function (simple version)..." -ForegroundColor Green
Write-Host ""

# Run empire function
python empire_simple.py
