# Install Pandas for EMPIRE DEMO

## Issue: pandas installation failed

Python 3.13 is very new and pandas may not have pre-built wheels yet.

## Solutions

### Option 1: Install from Source (May Take Time)

```powershell
pip install --upgrade pip setuptools wheel
pip install pandas openpyxl
```

### Option 2: Use Python 3.11 or 3.12 (Recommended)

If you have Python 3.11 or 3.12 installed:

```powershell
# Check available Python versions
py --list

# Use Python 3.11 or 3.12
py -3.11 -m pip install pandas openpyxl
py -3.11 agent.py --demo-csv file:344
```

### Option 3: Use Conda (If Installed)

```powershell
conda install pandas openpyxl
```

### Option 4: Manual CSV Instead of Excel

If pandas continues to fail, we can modify the demo to use CSV instead:

```powershell
# Create CSV manually
# Then modify agent.py to use pd.read_csv() instead
```

---

## Quick Test

```powershell
python -c "import pandas; print('pandas OK')"
```

If this works, you're ready to run the demo!

---

## Run Demo (After pandas installed)

```powershell
cd C:\Users\MYPC\Desktop\debt-arbitrage

# Create test Excel file (if needed)
python -c "import pandas as pd; pd.DataFrame({'Date':['25/04/2025'],'Description':['HDFC EMI'],'Debit':[52842]}).to_excel('25aprilcsv.xlsx', index=False)"

# Run demo
python agent.py --demo-csv file:344
```

---

## Alternative: Skip Excel, Use CSV

If Excel continues to fail, we can modify the demo to:
1. Accept CSV files instead
2. Use built-in `csv` module (no pandas needed)
3. Still generate loans.json and projections

Let me know if you want this alternative!
