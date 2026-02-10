# Debt Empire - Quick Start Script
# Run this script to start both backend and frontend servers

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "DEBT EMPIRE - Server Startup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if .env exists
if (-not (Test-Path "backend\.env")) {
    Write-Host "⚠️  WARNING: backend\.env file not found!" -ForegroundColor Yellow
    Write-Host "   Creating from template..." -ForegroundColor Yellow
    Copy-Item backend\env.example backend\.env
    Write-Host "   Please edit backend\.env and add your DATABASE_URL and JWT_SECRET" -ForegroundColor Yellow
    Write-Host ""
}

# Start Backend
Write-Host "Starting Backend Server (Port 8000)..." -ForegroundColor Green
Write-Host "   Terminal 1 will open for backend" -ForegroundColor Gray
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD\backend'; Write-Host 'Backend Server Starting...' -ForegroundColor Green; python main.py"

# Wait a bit for backend to start
Start-Sleep -Seconds 3

# Start Frontend
Write-Host "Starting Frontend Server (Port 3000)..." -ForegroundColor Green
Write-Host "   Terminal 2 will open for frontend" -ForegroundColor Gray
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD\frontend'; Write-Host 'Frontend Server Starting...' -ForegroundColor Green; npm run dev"

Write-Host ""
Write-Host "✅ Servers starting in separate windows!" -ForegroundColor Green
Write-Host ""
Write-Host "Backend:  http://localhost:8000" -ForegroundColor Cyan
Write-Host "Frontend: http://localhost:3000" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press any key to open browser..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

# Open browser
Start-Process "http://localhost:3000"
