# Debt Empire: Step-by-step ADD NEW LOAN
# Run from any location; script CDs to debt-empire.

$ErrorActionPreference = "Stop"
$empireRoot = "C:\Users\MYPC\Desktop\debt-arbitrage\debt-empire"
$newUploads = Join-Path $empireRoot "loans\new_uploads"

Set-Location $empireRoot

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  ADD NEW LOAN - Step by Step" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Step 1: Drag your documents into new_uploads/" -ForegroundColor Yellow
Write-Host "  Folder: $newUploads" -ForegroundColor Gray
Write-Host "  (Opening folder in Explorer...)" -ForegroundColor Gray
if (Test-Path $newUploads) {
    Start-Process explorer.exe -ArgumentList "`"$newUploads`""
} else {
    New-Item -ItemType Directory -Path $newUploads -Force | Out-Null
    Start-Process explorer.exe -ArgumentList "`"$newUploads`""
}
Write-Host "  -> Drop your PDF (e.g. bjmagnarepay1.pdf) there, then press Enter here." -ForegroundColor White
Read-Host "  Press Enter when done"

Write-Host ""
Write-Host "Step 2: Run Loan Verifier" -ForegroundColor Yellow
Write-Host "  When prompted:" -ForegroundColor Gray
Write-Host "    Enter choice [1-4]: 1   (Verify new loan)" -ForegroundColor Gray
Write-Host "    Enter choice [1-4]: 1   (Parse Bajaj PDF)" -ForegroundColor Gray
Write-Host "    PDF path: type filename only, e.g.  bjmagnarepay1.pdf" -ForegroundColor Gray
Write-Host "  Then complete the wizard and answer Y to save." -ForegroundColor Gray
Write-Host ""
Read-Host "Press Enter to start loan_verifier.py"

py loan_verifier.py
if ($LASTEXITCODE -ne 0) { Write-Host "loan_verifier.py exited with code $LASTEXITCODE" -ForegroundColor Red; exit $LASTEXITCODE }

Write-Host ""
Write-Host "Step 3: Regenerate dashboard (so new loan appears)" -ForegroundColor Yellow
py empire.py
if ($LASTEXITCODE -ne 0) { Write-Host "empire.py exited with code $LASTEXITCODE" -ForegroundColor Red; exit $LASTEXITCODE }

Write-Host ""
Write-Host "Step 4: Open dashboard → Ctrl+P → Save as PDF → Email" -ForegroundColor Yellow
Start-Process (Join-Path $empireRoot "dashboard.html")
Write-Host ""
Write-Host "Done. New loan added; dashboard opened." -ForegroundColor Green
Write-Host ""
