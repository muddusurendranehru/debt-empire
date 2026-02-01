# EMPIRE DEMO: Parse Excel CSV

## Command

```powershell
cd C:\Users\MYPC\Desktop\debt-arbitrage
python agent.py --demo-csv file:344
```

**Or with direct filename:**
```powershell
python agent.py --demo-csv 25aprilcsv.xlsx
```

---

## What It Does

### Step 1: LOAD Excel
```python
df = pd.read_excel('25aprilcsv.xlsx')
```
- Loads Excel file into pandas DataFrame
- Shows row count

### Step 2: FILTER Debits >₹20k + Keywords
- Filters transactions where:
  - Debit/Amount > ₹20,000
  - Description contains: L&T, HDFC, Tata, Bajaj (case-insensitive)

### Step 3: OUTPUT loans.json
- Creates `loans.json` with:
  - `count`: Number of filtered transactions
  - `total`: Sum of all debits
  - `transactions`: Array of transaction details

### Step 4: HDFC Projection
- Finds HDFC transactions
- Calculates monthly EMI
- Generates 12-month projection with:
  - Principal Part (60%)
  - Interest Part (40%)
  - Outstanding Balance
- Saves to `hdfc_projection.xlsx`

### Step 5: PRINT Table + "Monthly ritual LIVE"
- Displays formatted table
- Shows summary statistics
- Prints "MONTHLY RITUAL LIVE"

### Step 6: Verify Human
- Prompts: "EMIs correct? y/n"
- Waits for human verification

---

## Excel File Format Required

Your Excel file should have columns like:

| Date | Description | Debit | Credit | Balance |
|------|-------------|-------|--------|---------|
| 25/04/2025 | HDFC EMI | 52842 | - | - |
| 25/04/2025 | L&T EMI | 80311 | - | - |
| 25/04/2025 | Tata EMI | 28000 | - | - |

**Required Columns:**
- Date (or DATE)
- Description (or DESC, NARRATION)
- Debit (or AMOUNT)

**Keywords to match:**
- L&T, LT, lt
- HDFC, hdfc
- Tata, tata
- Bajaj, bajaj

---

## Output Files

1. **loans.json** - Filtered transaction data
   ```json
   {
     "count": 5,
     "total": 250000,
     "transactions": [...]
   }
   ```

2. **hdfc_projection.xlsx** - 12-month projection
   - Month | EMI Total | Principal Part | Interest Part | OS Bal

---

## Example Output

```
======================================================================
EMPIRE DEMO: PARSE 25aprilcsv.xlsx
======================================================================

[Step 1] LOAD Excel...
[OK] Loaded 150 rows

[Step 2] FILTER Debits >₹20k + keywords (L&T/HDFC/Tata/Bajaj)...
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
Mo2      Rs   52,842  Rs   31,705  Rs   21,137  Rs 2,468,295
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

## Troubleshooting

### File Not Found
- Place `25aprilcsv.xlsx` in the project root
- Or provide full path: `python agent.py --demo-csv "C:\path\to\file.xlsx"`

### pandas Not Installed
```powershell
pip install pandas openpyxl
```

### No Transactions Found
- Check Excel has Debit column
- Check Description column contains lender keywords
- Check amounts are > ₹20,000

---

## Quick Start

1. **Install dependencies:**
   ```powershell
   pip install pandas openpyxl
   ```

2. **Place Excel file:**
   - Copy `25aprilcsv.xlsx` to project root
   - Or use file:344 reference

3. **Run demo:**
   ```powershell
   python agent.py --demo-csv file:344
   ```

4. **Verify:**
   - Check `loans.json`
   - Check `hdfc_projection.xlsx`
   - Answer verification prompt

---

**Ready to demo!** 🚀
