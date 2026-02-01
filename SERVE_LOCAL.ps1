# Start local HTTP server (optional - for testing)
# Double-click this file or run: .\SERVE_LOCAL.ps1
# Then open: http://localhost:8000/verifier.html

Write-Host "`n=== Starting Local HTTP Server ===" -ForegroundColor Cyan
Write-Host ""

# Navigate to script directory
Set-Location $PSScriptRoot

# Check Python
try {
    $pythonVersion = py --version 2>&1
    Write-Host "Python: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Python not found!" -ForegroundColor Red
    Write-Host "Install Python or use OPEN_VERIFIER.ps1 (no server needed)" -ForegroundColor Yellow
    Write-Host "`nPress any key to exit..."
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    exit
}

Write-Host "`nStarting server on http://localhost:8000" -ForegroundColor Yellow
Write-Host "Press Ctrl+C to stop" -ForegroundColor Cyan
Write-Host ""

# Open browser after 2 seconds
Start-Job -ScriptBlock {
    Start-Sleep -Seconds 2
    Start-Process "http://localhost:8000/verifier.html"
} | Out-Null

# Start Python HTTP server (Python 3)
try {
    py -m http.server 8000
} catch {
    Write-Host "`nERROR: Could not start server" -ForegroundColor Red
    Write-Host "Try: OPEN_VERIFIER.ps1 (no server needed)" -ForegroundColor Yellow
}
