# Open HTML Files in Browser
# Double-click this file or run: .\OPEN_HTML.ps1

Write-Host "`n=== Opening HTML Files ===" -ForegroundColor Cyan
Write-Host ""

# Navigate to script directory
Set-Location $PSScriptRoot

Write-Host "Opening SAFE_EDITING_GUIDE.html..." -ForegroundColor Yellow
Start-Process "SAFE_EDITING_GUIDE.html"

Start-Sleep -Seconds 2

Write-Host "Opening verifier.html (MASTER DASHBOARD)..." -ForegroundColor Yellow
Start-Process "verifier.html"

Start-Sleep -Seconds 2

Write-Host "Opening dashboard.html..." -ForegroundColor Yellow
Start-Process "dashboard.html"

Start-Sleep -Seconds 2

Write-Host "Opening monthly projections.html..." -ForegroundColor Yellow
Start-Process "monthly projections.html"

Start-Sleep -Seconds 2

Write-Host "Opening L&T OTS letter..." -ForegroundColor Yellow
Start-Process "ots-pdfs\lt-ots.html"

Write-Host "`nAll HTML files opened in your default browser!" -ForegroundColor Green
Write-Host "Press any key to exit..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
