# Quick Run Script for Debt Empire Analyzer
# Just double-click this file or run: .\RUN.ps1

Write-Host "`n=== DEBT EMPIRE ANALYZER ===" -ForegroundColor Cyan
Write-Host ""

# Navigate to script directory
Set-Location $PSScriptRoot

# Run the analyzer
Write-Host "Running empire.py..." -ForegroundColor Yellow
Write-Host ""

py empire.py

Write-Host "`n=== DONE ===" -ForegroundColor Green
Write-Host "Press any key to exit..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
