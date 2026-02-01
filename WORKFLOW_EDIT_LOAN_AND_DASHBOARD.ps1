# Debt Empire: Edit Loan → Regenerate Dashboard → Print & Email OTS
# Run from any location; script CDs to debt-empire.

$ErrorActionPreference = "Stop"
Set-Location "C:\Users\MYPC\Desktop\debt-arbitrage\debt-empire"

Write-Host ""
Write-Host "=== Debt Empire: Edit Loan → Dashboard → Print/Email ===" -ForegroundColor Cyan
Write-Host ""

# --- Step 1: Edit loans (interactive) ---
Write-Host "Step 1: Edit loans (if needed)" -ForegroundColor Yellow
Write-Host "  → Option 3 → Edit loan #1 (Bajaj) → Fix account numbers → Save" -ForegroundColor Gray
Write-Host "  Starting loan_verifier.py..." -ForegroundColor Green
Write-Host ""
py loan_verifier.py
if ($LASTEXITCODE -ne 0) { Write-Host "loan_verifier.py exited with code $LASTEXITCODE" -ForegroundColor Red; exit $LASTEXITCODE }

# --- Step 2: Regenerate dashboard ---
Write-Host ""
Write-Host "Step 2: Regenerate dashboard" -ForegroundColor Yellow
py empire.py
if ($LASTEXITCODE -ne 0) { Write-Host "empire.py exited with code $LASTEXITCODE" -ForegroundColor Red; exit $LASTEXITCODE }

# --- Step 3: Open dashboard for print & email ---
Write-Host ""
Write-Host "Step 3: Print & email to L&T" -ForegroundColor Yellow
Write-Host "  → Ctrl+P → Save as PDF" -ForegroundColor Gray
Write-Host "  → Email subject: ""OTS Settlement Offer - Account BL240910207908339""" -ForegroundColor Gray
Write-Host ""
Start-Process "dashboard.html"
Write-Host "Done. Dashboard opened. Use Ctrl+P to save as PDF, then email." -ForegroundColor Green
