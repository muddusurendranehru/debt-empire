# Run EMPIRE DEMO

## Quick Start

### If pandas is installed:
```powershell
cd C:\Users\MYPC\Desktop\debt-arbitrage
python agent.py --demo-csv file:344
```

### If pandas installation failed (Python 3.13 issue):

**Option 1: Use CSV instead of Excel**
```powershell
# Convert Excel to CSV manually, then:
python debt-empire\DEMO_WITHOUT_PANDAS.py file:344
```

**Option 2: Install pandas for Python 3.11/3.12**
```powershell
py -3.11 -m pip install pandas openpyxl
py -3.11 agent.py --demo-csv file:344
```

---

## What You Need

1. **Excel/CSV file** with columns:
   - Date
   - Description (containing: L&T, HDFC, Tata, Bajaj)
   - Debit (amounts > ₹20,000)

2. **Python packages:**
   - pandas + openpyxl (for Excel)
   - OR just Python (for CSV version)

---

## Expected Output

```
======================================================================
EMPIRE DEMO: PARSE 25aprilcsv.xlsx
======================================================================

[Step 1] LOAD Excel...
[OK] Loaded 150 rows

[Step 2] FILTER Debits >₹20k + keywords...
[OK] Filtered 5 transactions

[Step 3] OUTPUT loans.json...
[OK] Saved: loans.json
  Count: 5
  Total: Rs 250,000.00 (Rs 2.50L)

[Step 4] HDFC Projection: 12 rows (P+I split)...
======================================================================
HDFC PROJECTION (12-Month P+I Split)
======================================================================
Month    EMI Total    Principal    Interest    OS Bal
----------------------------------------------------------------------
Mo1      Rs   52,842  Rs   31,705  Rs   21,137  Rs 2,500,000
...
======================================================================

[OK] Saved: hdfc_projection.xlsx

======================================================================
MONTHLY RITUAL LIVE
======================================================================
Transactions filtered: 5
Total debits: Rs 250,000.00 (Rs 2.50L)
Loans.json: loans.json
HDFC Projection: hdfc_projection.xlsx
======================================================================

Verify human: 'EMIs correct? y/n'
EMIs correct? (y/n):
```

---

## Files Created

- `loans.json` - Filtered transactions
- `hdfc_projection.xlsx` (or `.json` if no pandas)

---

**Ready to demo!** 🚀
