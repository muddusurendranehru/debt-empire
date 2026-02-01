# Open verifier.html in browser (no server needed)
# Double-click this file or run: .\OPEN_VERIFIER.ps1

Write-Host "`n=== Opening VERIFIER.HTML ===" -ForegroundColor Cyan
Write-Host ""

# Navigate to script directory
Set-Location $PSScriptRoot

# Check if verifier.html exists
if (-not (Test-Path "verifier.html")) {
    Write-Host "ERROR: verifier.html not found!" -ForegroundColor Red
    Write-Host "Run: py generate_verifier_html.py" -ForegroundColor Yellow
    Write-Host "Or double-click: GENERATE_VERIFIER.ps1" -ForegroundColor Yellow
    Write-Host "`nPress any key to exit..."
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    exit
}

# Get absolute path
$verifierPath = (Resolve-Path "verifier.html").Path

Write-Host "Opening: $verifierPath" -ForegroundColor Green
Write-Host ""

# Open in default browser (file:// protocol - no server needed)
Start-Process $verifierPath

Write-Host "✅ Opened in browser!" -ForegroundColor Green
Write-Host "`nNote: This is a local file (file://) - no server needed." -ForegroundColor Cyan
Write-Host "Press any key to exit..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
