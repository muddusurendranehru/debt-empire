# Create Test Excel File for EMPIRE DEMO
# Run this if you don't have 25aprilcsv.xlsx

Write-Host "Creating test Excel file: 25aprilcsv.xlsx..." -ForegroundColor Yellow

$pythonCode = @"
import pandas as pd
from datetime import datetime

# Create sample data
data = {
    'Date': ['25/04/2025', '25/04/2025', '25/04/2025', '25/04/2025', '15/04/2025'],
    'Description': ['HDFC EMI Payment', 'L&T EMI Payment', 'Tata Capital EMI', 'Bajaj Finance EMI', 'Other Payment'],
    'Debit': [52842, 80311, 28000, 66000, 5000],
    'Credit': [0, 0, 0, 0, 0],
    'Balance': [2324000, 2500000, 2300000, 1400000, 500000]
}

df = pd.DataFrame(data)
df.to_excel('25aprilcsv.xlsx', index=False)
print('✅ Created 25aprilcsv.xlsx with sample loan EMI data')
"@

python -c $pythonCode

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Test Excel file created!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Now run:" -ForegroundColor Cyan
    Write-Host "  python agent.py --demo-csv file:344" -ForegroundColor White
} else {
    Write-Host "❌ Failed to create test file. Install pandas:" -ForegroundColor Red
    Write-Host "  pip install pandas openpyxl" -ForegroundColor White
}
