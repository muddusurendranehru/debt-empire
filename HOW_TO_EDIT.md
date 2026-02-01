# How to Edit Loans

## Quick Method (Easiest)

### Option 1: Double-Click Script
1. Open File Explorer
2. Navigate to: `C:\Users\MYPC\Desktop\debt-arbitrage\debt-empire`
3. Double-click `RUN_VERIFIER.ps1`
4. Follow the interactive menu

### Option 2: PowerShell Commands
```powershell
# Step 1: Navigate to folder
cd C:\Users\MYPC\Desktop\debt-arbitrage\debt-empire

# Step 2: Run loan verifier
py loan_verifier.py
```

## Interactive Menu Options

When `loan_verifier.py` runs, you'll see:

```
MAIN MENU
  1. Verify new loan (Bajaj/L&T/HDFC)
  2. Review existing loans      ← View all loans
  3. Edit loan details          ← Edit existing loan
  4. Save & exit → run empire.py
```

### To Edit an Existing Loan:

1. **Choose Option 3: Edit loan details**
2. **Select loan number** from the list
3. **Edit fields** as prompted:
   - Borrower Name (required)
   - Outstanding Principal
   - EMI Amount
   - Tenure
   - Dates
   - Fees
4. **Review and approve**
5. **Save** → Updates `masters.json`

### To Review Loans:

1. **Choose Option 2: Review existing loans**
2. See all loans with EMI totals
3. Press Enter to continue

## After Editing

1. **Save** in the verifier (Option 4)
2. **Run empire.py** to regenerate reports:
   ```powershell
   py empire.py
   ```
3. **Refresh verifier.html** in browser (or regenerate):
   ```powershell
   py generate_verifier_html.py
   ```

## Tips

- **Borrower Name** is required - cannot skip
- **All changes** are saved to `masters.json`
- **Run empire.py** after editing to update all reports
- **verifier.html** auto-refreshes every 5 minutes

## Quick Reference

| Action | Command |
|--------|---------|
| Edit loans | `py loan_verifier.py` → Option 3 |
| Review loans | `py loan_verifier.py` → Option 2 |
| Generate reports | `py empire.py` |
| View verifier | `start verifier.html` |
