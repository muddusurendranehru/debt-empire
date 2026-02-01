# DEBT EMPIRE v3.2 FULL TEST

**File**: `verifier_with_upload_v3.2.html`  
**Test PDF**: `bjnewloan2018.pdf` (place in `debt-empire` folder or any location)

**Goal**: Extract → ➕ ADD TO DASHBOARD → Verify dashboard shows the loan (e.g. `loan_147853`).

---

## RUN THIS EXACT SEQUENCE

### 1. Open the page

- Start local server (optional but recommended):
  ```powershell
  cd c:\Users\MYPC\Desktop\debt-arbitrage\debt-empire
  python -m http.server 8080
  ```
- Open: **http://localhost:8080/verifier_with_upload_v3.2.html**  
  Or double‑click `verifier_with_upload_v3.2.html` to open in browser.

---

### 2. Upload & Extract

1. Stay on **Tab 1: DOCUMENT EXTRACTOR**.
2. **Drag** `bjnewloan2018.pdf` onto the drop zone **or** click the zone and choose the file.
3. Wait for "Extracting..." to finish.

**Expect after extraction:**

- Status: `Done. Edit if needed, then click EXTRACT GOOD → NEXT.`
- Form filled with values from PDF, e.g.:
  - **Loan Name (AI suggested)**: e.g. `loan_147853` or `bjmagnarepay1` (depends on account)
  - **Account Number**: e.g. `400CFP66425054` or `H400FBL...` (if present in PDF)
  - **Borrower Name**: e.g. `muddu surendra nehru`
  - **Current OS (₹)**: number if found, else empty / "Enter amount"
  - **Monthly EMI (₹)**: number if found
  - **Disbursal Date**: e.g. `2018-02-27` or `2019-01-15`
  - **Loan Type**: e.g. `Flexi`
  - **Doc Type**: e.g. `EMI Running Statement` or `Interest Cert`
- If **onExtractComplete** is enabled: an alert "Added: …" may appear (auto‑add).

---

### 3. Add to dashboard

1. Check/correct the extracted fields if needed.
2. Click **➕ ADD TO DASHBOARD**.

**Expect:**

- Alert: `Added: <loan name>` (e.g. `Added: loan_147853`).
- Status under the buttons: `Added: <loan name> — check Tab 3.`

---

### 4. Verify dashboard shows the loan

1. Open **Tab 3: DEBT MANAGER**.
2. In **Active loans** you should see a line like:
   - `📁 loans/loan_147853/ (0/5 docs)`  
   (or whatever loan name was added.)
3. In **Select loan** dropdown you should see:
   - `loan_147853 (400CFP66425054)` or similar.

**Optional:**

- Open **Tab 2: LOAN VERIFIER**.
- In **EXISTING LOANS** dropdown you should see the same loan (e.g. `loan_147853 (...)`).

---

### 5. Alternative flow: EXTRACT GOOD → NEXT

1. After extraction (step 2), click **✅ EXTRACT GOOD → NEXT: VERIFIER**.
2. You should land on **Tab 2** with **"+ NEW LOAN"** form pre‑filled from the draft.
3. Click **✅ SAVE LOAN** to save to `debtEmpireLoans`.
4. Open **Tab 3** and confirm the loan appears in the list and dropdown.

---

## Quick checklist

| Step | Action | Expected |
|------|--------|----------|
| 1 | Open HTML | Page loads, 3 tabs visible |
| 2 | Drag/select `bjnewloan2018.pdf` | "Extracting..." then form filled |
| 3 | Click **➕ ADD TO DASHBOARD** | Alert "Added: …", status text updated |
| 4 | Go to Tab 3 | Loan row + dropdown entry visible |
| 5 (optional) | Go to Tab 2 | Loan in EXISTING LOANS dropdown |

---

## If extraction is empty or wrong

- **Account / OS / EMI empty**: PDF may not contain the expected labels; use **✏️** and type values, then **➕ ADD TO DASHBOARD**.
- **Loan name**: Uses suggested name from account (e.g. `bjmagnarepay1` for H400FBL) or `loan_<6 digits>`. You can edit before adding.
- **localStorage**: Loans are stored under `debtEmpireLoans`. In DevTools → Application → Local Storage you can inspect or clear.

---

## Console one‑liner (no PDF)

To add `loan_147853` directly without a file:

```javascript
window.addToDashboard({
  id: 'loan_147853', name: 'loan_147853',
  borrower: 'muddu surendra nehru', account: '400CFP66425054',
  os: 631268, emi: 42366, disbursal: '2018-02-27',
  type: 'Flexi', doc: 'EMI Running Statement',
  dateAdded: new Date().toISOString()
});
```

Then open **Tab 3** and confirm the loan appears.
