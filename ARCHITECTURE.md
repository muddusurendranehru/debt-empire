# DEBT-EMPIRE ARCHITECTURE v2.0

**KEEP ALL** existing: `loan_verifier.py`, `empire.py`, `masters.json`, all current folders and files.

**CORE**: Folder-per-loan + Duplicate Detection + 5 Loan Types + Yearly Archive.

---

## FOLDER STRUCTURE (auto-create)

```
debt-empire/
├── masters.json                 # Master loan register (KEEP)
├── loan_verifier.py             # Interactive verifier (KEEP)
├── empire.py                    # Main analyzer (KEEP)
├── verifier.html                # MASTER DASHBOARD: TREE + PRINT + EDIT (KEEP)
├── dashboard.html               # Dashboard (KEEP)
├── ots-pdfs/                    # OTS letters (KEEP)
│
├── loans/                       # FOLDER-PER-LOAN (auto-create)
│   ├── L&T/
│   │   └── BL240910207908339/
│   │       ├── meta.json        # Loan snapshot (provider, account, OS, EMI, type)
│   │       └── docs/            # PDFs/DOCX for this loan
│   ├── HDFC/
│   │   └── HDFC24LOAN1/
│   │       ├── meta.json
│   │       └── docs/
│   ├── Tata/
│   │   └── 0086007395/
│   ├── Bajaj/
│   │   ├── 400LAP14914207/
│   │   └── 400DFR47319474/
│   └── AdityaBirla/
│       └── 2024/
│
└── archive/                     # YEARLY ARCHIVE (auto-create)
    ├── 2024/
    │   └── (closed/settled loan folders moved here)
    ├── 2025/
    └── 2026/
```

**Rules:**
- One folder per loan: `loans/<Lender>/<AccountId>/`
- Each loan folder has `meta.json` (copy of loan record) and optional `docs/`
- Settled/closed loans can be moved to `archive/<YYYY>/` to keep `loans/` current
- All existing files (verifier, empire, masters.json, ots-pdfs, etc.) stay as-is

---

## 5 LOAN TYPES

| Type    | Code   | Description                    | OTS handling        |
|---------|--------|--------------------------------|---------------------|
| Personal| personal | Standard personal loan       | RBI 70% standard    |
| LAP     | lap    | Loan Against Property         | RBI 70% standard    |
| Flexi   | flexi  | Revolving / Flexi (e.g. Bajaj)| Special RBI rules   |
| Home    | home   | Home loan                     | Usually continue    |
| OD      | od     | Overdraft / Business OD       | Negotiation-based   |

- Stored in loan record as `loan_type` (or `product`).
- Used for reporting and OTS logic (e.g. flexi vs standard).

---

## 5 LOAN STATUS TYPES (masters.json)

| Status           | Condition / Meaning              | Action / Use                          |
|------------------|-----------------------------------|----------------------------------------|
| **CLOSED**       | OS = 0                            | Keep folder; **exclude from OTS**      |
| **PARTIAL**      | Prepaid; % paid                   | Re-check OS; may still OTS             |
| **NEW_DISBURSED**| Not yet received / OS = 0 hold   | Hold; do not OTS until disbursed       |
| **RUNNING_PAID_EMI** | Active; EMI being paid        | **OTS target** (e.g. clinic closed)    |
| **NEGOTIATING**  | Offer sent                        | Track response; follow up              |

- Stored in loan record as `status` (in addition to or instead of `verification_status`).
- **OTS calculations**: Include only RUNNING_PAID_EMI, PARTIAL, NEGOTIATING (exclude CLOSED, NEW_DISBURSED).
- Keep merit folder for CLOSED; move to archive when desired.

---

## DUPLICATE DETECTION

- **Key**: `provider` + `account_number` (or `account_ref`).
- Before adding a loan (in verifier or when building structure):
  - Normalize: strip spaces, uppercase account id.
  - If same provider + account already exists in `masters.json` or in `loans/<Lender>/<Account>/` → treat as **duplicate**.
- Actions:
  - **Skip add** and show: "Loan already exists: <Lender> <Account>"
  - Or **update** existing folder/meta.json and masters entry (user choice).

---

## YEARLY ARCHIVE

- **Purpose**: Move closed/settled loans out of active `loans/` without losing history.
- **Structure**: `archive/<YYYY>/` mirrors `loans/` (e.g. `archive/2025/L&T/BL240910207908339/`).
- **When**: After OTS settlement or closure; optional script or manual move.
- **Effect**: `masters.json` can mark loan as `verification_status: "settled"` and path can point to archive.

---

## YEARLY (ritual)

- **Jan**: Move interest certs → `archive/2026/` (or current year).
- **Update OS** from new statements (re-run verifier or paste latest OS into `masters.json` / loan folder `meta.json`).

---

## AUTO-CREATE SCRIPT

- **Script**: `build_structure.py`
- **Input**: Reads `masters.json`.
- **Actions**:
  1. Create `loans/` and `archive/<current_year>/` if missing.
  2. For each loan in `masters.json`: create `loans/<Provider>/<AccountId>/`, `meta.json`, `docs/`.
  3. Duplicate check: if folder already exists for same provider+account, skip or update (configurable).
  4. Do not delete or overwrite existing files in existing folders; only add missing.

---

## DASHBOARD (verifier.html)

- **verifier.html** = Loan verifier dashboard (table: shortcode, lender, OS, EMI, tenure, fees; Print, Edit, Run Empire, Email OTS).
- Generated from `masters.json` via `generate_verifier_html.py` or when running `empire.py`.
- Open in browser → Ctrl+P to print/PDF. Do not change working behaviour.

---

## OTS Gen (Step 3)

- **Step 3** in the ritual = generate OTS letters for all lenders.
- **Trigger**: `empire.py` → `generate_ots_letters()`.
- **Output**: `ots-pdfs/` — per lender: `*-ots.html`, `*-ots.txt`; L&T also `lt-ots.pdf` if reportlab installed.
- **Input**: `masters.json` (outstanding, EMI, account_ref).
- **Use**: Email OTS (open HTML or copy .txt); print L&T PDF for formal offer. Do not change working behaviour.

---

## FILE ROLES (unchanged)

| File / Folder     | Role                                      |
|-------------------|-------------------------------------------|
| masters.json      | Single source of truth for all loans      |
| loan_verifier.py  | Add/edit loans, write to masters.json    |
| empire.py         | Reports, OTS, dashboard, projections      |
| verifier.html     | **Dashboard** — HTML table from masters.json |
| dashboard.html    | Main OTS summary dashboard                |
| ots-pdfs/         | OTS letters (HTML + text)                 |
| loans/            | One folder per loan + meta + docs         |
| archive/YYYY/    | Archived loans by year                    |

---

## VERSION

- **Architecture**: v2.0  
- **Core**: Folder-per-loan, Duplicate Detection, 5 Loan Types, Yearly Archive  
- **Compatibility**: All existing scripts and files retained.
