# Generate verifier.html
# Double-click this file or run: .\GENERATE_VERIFIER.ps1

Write-Host "`n=== GENERATING VERIFIER.HTML ===" -ForegroundColor Cyan
Write-Host ""

# Navigate to script directory
Set-Location $PSScriptRoot

# Run the generator
Write-Host "Running generator..." -ForegroundColor Yellow
Write-Host ""

py generate_verifier_html.py

Write-Host "`n=== DONE ===" -ForegroundColor Green
Write-Host "Opening verifier.html in browser..." -ForegroundColor Yellow

Start-Sleep -Seconds 1
Start-Process "verifier.html"

Write-Host "Press any key to exit..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
