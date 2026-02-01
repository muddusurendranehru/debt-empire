# Run Loan Verifier
# Double-click this file or run: .\RUN_VERIFIER.ps1

Write-Host "`n=== LOAN VERIFIER ===" -ForegroundColor Cyan
Write-Host ""

# Navigate to script directory
Set-Location $PSScriptRoot

# Run the loan verifier
Write-Host "Starting loan verification wizard..." -ForegroundColor Yellow
Write-Host ""

py loan_verifier.py

Write-Host "`n=== DONE ===" -ForegroundColor Green
Write-Host "Press any key to exit..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
