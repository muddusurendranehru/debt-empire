# Senior Arbitrage Manager → Debt Empire Master Board

**Don't destroy success.** Human in the loop - you review and edit before changes take effect.

---

## Workflow (Export → Import → Save)

1. **Edit in Senior Arbitrage Manager**
   - Add new loan: DOCUMENT EXTRACTOR tab → upload doc → EXTRACT GOOD → VERIFIER → SAVE
   - Add documents to existing: DEBT MANAGER tab → select loan → Add file
   - Export CSV when needed (backup)

2. **Export for Debt Empire Master Board**
   - DEBT MANAGER tab → **Export for Debt Empire** button
   - Downloads `masters_debt_empire.json`

3. **Import in Editable Master Dashboard**
   - Open `http://localhost:8080/editable_master_dashboard.html`
   - Click **Import / Add from file** → select the downloaded JSON
   - Loans are merged into the table (duplicates by account skipped)

4. **Review and Edit**
   - Check each loan: Provider, Outstanding, EMI, Account Ref
   - Add or remove rows as needed
   - Stats update automatically (Total Exposure, OTS, Savings)

5. **Save**
   - Click **Save (download masters.json)**
   - Replace `debt-empire/masters.json` with the downloaded file

6. **Regenerate Dashboard**
   ```bash
   cd debt-empire
   python refresh_dashboard.py
   ```

7. **View Debt Empire Dashboard**
   - `dashboard.html` — RBI OTS SETTLEMENT DASHBOARD
   - `verifier.html` — MASTER DASHBOARD with tree view

---

## Summary

| Action              | Where                                   |
|---------------------|-----------------------------------------|
| Add new loan        | Senior Arbitrage Manager                |
| Add documents       | Senior Arbitrage Manager                |
| Export CSV (backup) | Senior Arbitrage Manager                |
| Export for Debt Empire | Senior Arbitrage Manager (downloads JSON) |
| Import / Review     | Editable Master Dashboard               |
| Save changes        | Editable Master Dashboard               |
| View RBI OTS summary | dashboard.html                         |

---

## Alternative: Direct Script (Advanced)

If you prefer command line:
```bash
# After exporting from Senior Arbitrage Manager:
# 1. Save masters_debt_empire.json to debt-empire folder
# 2. Run:
python sync_to_master_board.py
```
This copies the JSON to masters.json and regenerates dashboard.html.
