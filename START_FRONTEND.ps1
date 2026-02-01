# Debt Empire Frontend - Manual Start (PowerShell)
# Port: 3000

Write-Host "🚀 Starting Debt Empire Frontend (Port 3000)..." -ForegroundColor Green

$frontendPath = Join-Path $PSScriptRoot "frontend"

if (-not (Test-Path $frontendPath)) {
    Write-Host "❌ Frontend folder not found: $frontendPath" -ForegroundColor Red
    exit 1
}

Set-Location $frontendPath

# Install dependencies if needed
if (-not (Test-Path "node_modules")) {
    Write-Host "Installing dependencies..." -ForegroundColor Yellow
    npm install
}

# Start Next.js dev server
Write-Host "Starting Next.js dev server on http://localhost:3000..." -ForegroundColor Green
npm run dev
