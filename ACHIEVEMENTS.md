# Debt Empire — What We Achieved

---

## What We Achieved Today (Session Summary)

- **Print button (🖨️) in Senior Arbitrage Manager** — In the Manager tab, next to each loan’s “Manage” (✏️) button, added a **Print** button. Clicking it opens a new window with **only that loan’s** OTS Settlement Offer (DEBT EMPIRE: OTS SETTLEMENT OFFER, loan name, borrower, account, OS, OTS amount %, savings, RBI footer). No other loans visible in the print output.
- **STEPS_OPEN_HTML.txt** — Marked `verifier_with_upload_v3.2.html` as **RECOMMENDED (BEST)**. Added a clear **“How to use this web app — after closing and opening your PC”** section with Option A (open file, no server) and Option B (run server + open localhost), plus notes: use same browser, use same “way” (file vs localhost) so data stays, and put URL in the **address bar** not in Google search.
- **Data clarification** — Explained that loan data is stored per “origin”: opening as **file** vs **http://localhost:8080** are different; use one way consistently so your loans show up.

---

## What We Achieved Now (Latest)

- **Export / Backup (Manager tab)** — In Debt Manager, below the Print instructions, added **⬇️ Export / Backup** card with **“⬇️ Export Loans as CSV”** button. Downloads all loans as CSV (loanId, loanName, borrower, accountNumber, lenderName, status, outstanding, emi, otsPercent, youPay, youSave, docsCount, customFieldsJson, paymentDetailsJson) for Google Sheets/Excel backup. Filename: `debt-empire-loans-YYYY-MM-DD.csv`. Section has `no-print` class so it does not appear in per-loan print. No loans → friendly alert; no other logic changed.
- **Intelligent duplicate handling (Extractor tab only)** — After user clicks **“EXTRACT GOOD → NEXT: VERIFIER”** and Account + OS are valid, the app checks if any loan has the **same account number** (exact match).  
  - **No match** → Same as before: create new loan and switch to Verifier.  
  - **Match found** → Show modal **“⚠️ Account Already Exists”** with existing loan details (name, borrower, account, OS, EMI) and three choices:  
    - **🔗 USE EXISTING LOAN** — Only fill empty fields on the existing loan (never overwrite), add current document to that loan’s docs, save, switch to Verifier, open that loan’s folder, toast: “Enriched existing loan! Review details in folder.”  
    - **➕ CREATE NEW LOAN** — Close modal and create a new loan (same flow as today; Verifier duplicate warning can still appear later).  
    - **❌ CANCEL** — Close modal and stay in Extractor (all fields preserved).  
  - Helper `findLoanByAccount(account)`; modal state `modalExistingLoan`. Modal has `z-index: 10000` and is hidden in print. No auto-merge; human chooses. Verifier/Manager/print/export unchanged.
- **CHANGE_SAFETY_RULES.md** — Rules: (1) Before any change, duplicate HTML as `*_STABLE.html` and only edit the copy; (2) One tiny feature per prompt; (3) After change, run 5 checks (open app, add loan, Verifier + Manager, print one loan, test new feature); (4) If anything breaks, delete edited file and restore from `_STABLE`.
- **RUN.txt** — Added **MANUAL START** section with full paths: folder path, PowerShell commands to start server (semicolon for PowerShell), URL for browser address bar, and option to open HTML without server.

---

## 1. verifier_with_upload_v3.2.html — Fully Dynamic

- **Loans only from `localStorage.debtEmpireLoans`** — no hardcoded/dummy loans.
- **Tab 2 (Verifier):** Account required; validation + focus if empty. Fallback loan name from borrower + date. SAVE LOAN updates in-memory and refreshes all dashboards; `saveLoans()` with console log.
- **Tab 3 (Debt Manager):** Active loans list and dropdown from the loans array. Embedded dashboard replaced with **live summary** (“X loans active | Total Exposure: ₹Y”) and **OPEN FULL DASHBOARD** button.
- **Console:** `window.loans` and `window.saveLoans()` for inspection and persist.

## 2. How to Open & Run

- **STEPS_OPEN_HTML.txt** — Run server first (`cd debt-empire` → `python -m http.server 8080`), then open `http://localhost:8080/verifier_with_upload_v3.2.html`.
- **Save As / broken file fix** — In-app “Download as .html (correct name)” link; STEPS explain using filename `verifier_with_upload_v3.2.html` (no trailing underscore).

## 3. Debt Manager — Add File & Print

- **“Add file / Add image”** label and **ADD FILE** button when a loan is selected; accept PDF and images (.pdf, .jpg, .png, .gif, .webp).
- **Per-loan Print** — Each loan has a **Print (Ctrl+P)** button; opens print dialog with that loan’s details only.

## 4. Senior Arbitrage Manager (senior_arbitrage_manager.html)

- New file with card layout, loan folder sidebar, status/OTS % in Manager table.
- Same `localStorage.debtEmpireLoans` — data shared with v3.2.
- Fixes: folder status badge markup, Close button label, robustness (HTML escaping, OTS %, max 5 docs).
- **Per-loan Print (🖨️):** Print button next to each loan’s Manage button; opens new window with only that loan’s OTS offer (no other loans in output).
- **Export / Backup:** Manager tab has “⬇️ Export Loans as CSV” for full backup (no-print).
- **Duplicate handling (Extractor):** On “EXTRACT GOOD”, if account already exists → modal: USE EXISTING (enrich only blanks + add doc) / CREATE NEW / CANCEL.

## 5. Extractor Tab Upgrades (Extractor Only — Verifier/Manager Unchanged)

- **Lender details (optional)** — Lender name, branch, RM, RM contact; stored in `extractorState.lenderDetails`.
- **Single EMI snapshot (optional)** — EMI number, date, amount paid, principal/interest parts, transaction ID; stored in `extractorState.emiSnapshot`.
- **Extra fields (advanced)** — “+ Add custom field” (max 20); label + value + remove; stored in `extractorState.extraFields`.
- **CSV EMI import (collapsible)** — Upload CSV → preview table (EMI date, amount, transaction ID, Keep checkbox) → **APPLY TO CURRENT LOAN** (enabled when a loan is selected in Verifier); rows stored in `extractorState.csvEmiRows` and applied to loan as `loan.csvEmiRows` on APPLY.
- **Core rule:** Only Account number + OS required; “EXTRACT GOOD → NEXT: VERIFIER” unchanged; all new sections optional; extras saved to `localStorage.debtEmpireExtractorExtras`.
- **Human-in-the-loop:** No auto-decisions; user can skip any new section; parsing failures show “Parsing incomplete - please fill manually.”

## 6. Confirmed Working

- Document Extractor → Loan Verifier → Debt Manager flow.
- Add file, print per loan, dynamic data from localStorage.
- Extractor: Account + OS only required; lender/EMI snapshot/extra fields/CSV optional; EXTRACT GOOD saves core loan + extras and switches to Verifier.

---

**Files**

- `verifier_with_upload_v3.2.html` — Extractor/Verifier/Manager with upload, print-per-loan, dynamic loans.
- `senior_arbitrage_manager.html` — Same data; card UI; Extractor extended with lender, EMI snapshot, extra fields, CSV import.
- `STEPS_OPEN_HTML.txt` — How to open (server first), demo steps, Save As fix.
- `ACHIEVEMENTS.md` — This summary.

---

## What’s Left to Achieve (Optional, Not Done Yet)

- **Edit / remove** — Edit or remove loans and documents (beyond current doc delete).
- **Generate OTS Proposal** — Button to generate a formal OTS proposal (beyond current print view).
- **Copy Email Template** — Button to copy a ready-made email template (e.g. for OTS / negotiation).
- **Import CSV** — Import loans from a CSV backup (e.g. debt-empire-loans-*.csv) back into the app.
