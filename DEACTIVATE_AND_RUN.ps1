# Deactivate Broken Venv and Run Demo

Write-Host "🔧 Deactivating broken venv..." -ForegroundColor Yellow

# Deactivate venv
if ($env:VIRTUAL_ENV) {
    deactivate
    Write-Host "✅ Deactivated broken venv" -ForegroundColor Green
} else {
    Write-Host "No venv active" -ForegroundColor Yellow
}

# Remove broken venv reference from PATH
$env:PATH = ($env:PATH -split ';' | Where-Object { $_ -notlike '*venv*' }) -join ';'
$env:VIRTUAL_ENV = $null

Write-Host ""
Write-Host "Running EMPIRE DEMO (using global Python)..." -ForegroundColor Green
Write-Host ""

# Run demo
python debt-empire\DEMO_WITHOUT_PANDAS.py file:344
