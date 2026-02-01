# Installing Dependencies for Debt Empire

## Problem
Python 3.13 doesn't have pre-built wheels for `pandas` and `reportlab` yet.

## Solutions

### Option 1: Use Python 3.11 or 3.12 (Recommended)

```powershell
# Check available Python versions
py --list

# Install with Python 3.11
py -3.11 -m pip install --user pandas openpyxl reportlab

# Or Python 3.12
py -3.12 -m pip install --user pandas openpyxl reportlab

# Then run with that version
py -3.11 empire.py
# or
py -3.12 empire.py
```

### Option 2: Current Status (Works Without Dependencies)

The script currently runs successfully and generates:
- ✅ `masters.json` (all 4 loans with totals)
- ❌ `monthly projections.xlsx` (requires pandas)
- ❌ `ots-pdfs/lt-ots.pdf` (requires reportlab)
- ❌ `Debt_Empire_Dashboard.pdf` (requires reportlab)

### Option 3: Install from Source (Slow, but works)

```powershell
# This will compile from source - takes longer
py -m pip install --user --no-binary pandas pandas openpyxl reportlab
```

### Option 4: Use Conda (If Available)

```powershell
conda install pandas openpyxl reportlab
```

## Current Output

Even without dependencies, you get:
- Complete loan analysis in `masters.json`
- All 4 loans (L&T, HDFC, Tata, Bajaj)
- Total exposure: ₹61.34L
- Total OTS liability: ₹42.94L
- Total savings: ₹18.40L

## Next Steps

1. If you have Python 3.11/3.12: Use Option 1
2. If only Python 3.13: Use Option 2 (current status) or Option 3
3. View `masters.json` for complete analysis
4. View `dashboard.html` in browser for visual dashboard
