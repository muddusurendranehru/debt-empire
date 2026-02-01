# DEBT-EMPIRE Architecture v2.0

**Non-destructive enhancement** - All existing files preserved: `verifier.py`, `empire.py`, `masters.json`, `loan_verifier.py`.

---

## New Structure

```
debt-empire/
├── core/                          # NEW orchestration layer
│   ├── orchestrator.py            # Main controller
│   ├── duplicate_detector.py      # SHA256-based duplicate detection
│   └── archive_manager.py         # Yearly auto-archiving
├── loans/                         # FOLDER-PER-LOAN (NEW CORE)
│   ├── lt-bl240910207908339/      # L&T Finance (standard term loan)
│   │   ├── loan.json              # Metadata: status, OS, EMI, dates, borrower name
│   │   ├── statements/            # Raw documents
│   │   │   └── FORECLOSURE_BL240910207908339.pdf
│   │   ├── ots/                   # OTS negotiation artifacts
│   │   │   ├── offer_2026-01-29.pdf
│   │   │   └── email_thread.txt
│   │   └── closure_proof/         # Merit proof (if closed)
│   ├── bajaj-400dfr47319474/      # Bajaj Flexi Loan (revolving credit)
│   │   ├── loan.json              # Metadata: type="flexi", linked_account="400LAP14914207"
│   │   ├── statements/
│   │   │   └── 2017-18bajdoctorsflexiloanstmnt.pdf
│   │   └── ots/
│   ├── hdfc-hdfc24loan1/          # HDFC Personal Loan (standard term)
│   ├── tata-tata24/               # Tata Capital (standard term)
│   └── bajaj-400lap14914207/      # Bajaj LAP (linked to flexi above)
├── archives/                      # YEARLY AUTO-ARCHIVE
│   ├── 2024/
│   ├── 2025/
│   └── 2026/
├── reports/                       # PRINT-OPTIMIZED OUTPUTS
│   ├── dashboard.html             # Browser → Ctrl+P → Save as PDF
│   ├── negotiation_dashboard.html # Account numbers visible (400DFR47319474 → 400LAP14914207)
│   └── monthly_projections.csv
├── verifier.py                    # ✅ UNCHANGED (still works)
├── empire.py                      # ✅ UNCHANGED (still works)
├── loan_verifier.py               # ✅ UNCHANGED (still works)
├── masters.json                   # ✅ BACKWARDS COMPATIBLE (now aggregate view)
├── loan_types.json                # Schema: 5 loan types with validation rules
└── README.architecture.md         # This file
```

---

## Core Orchestration

### `core/orchestrator.py`
- Main controller that coordinates all operations
- Syncs `masters.json` from loan folders (aggregate view)
- Manages loan folder structure
- Integrates duplicate detection and archiving

**Usage:**
```bash
py -m core.orchestrator --sync          # Sync masters.json
py -m core.orchestrator --archive      # Auto-archive closed loans
```

### `core/duplicate_detector.py`
- SHA256-based duplicate detection
- Prevents duplicate document uploads
- Tracks document versions

**Usage:**
```bash
py -m core.duplicate_detector --check file.pdf
py -m core.duplicate_detector --loan loans/lt-bl240910207908339
```

### `core/archive_manager.py`
- Yearly auto-archiving for closed loans
- Moves from `loans/` to `archives/YYYY/`
- Based on closure date or status

**Usage:**
```bash
py -m core.archive_manager --auto      # Auto-archive closed
py -m core.archive_manager --list     # List archived loans
```

---

## Loan Structure

### Folder Naming
- **Old**: `loans/Provider/Account/` (e.g., `loans/LandT/BL240910207908339/`)
- **New**: `loans/provider-account/` (e.g., `loans/lt-bl240910207908339/`)

### `loan.json` Schema
```json
{
  "provider": "L&T",
  "account_number": "BL240910207908339",
  "borrower_name": "Dr. Muddu Surendra Nehru",
  "outstanding_principal": 2574000,
  "emi_amount": 80000,
  "tenure_remaining_months": 32,
  "loan_type": "personal",
  "status": "RUNNING_PAID_EMI",
  "linked_account": "",
  "start_date": "2024-04-03",
  "updated_at": "2026-01-29T..."
}
```

### Subdirectories
- **`statements/`**: Raw documents (PDFs, statements, foreclosure notices)
- **`ots/`**: OTS negotiation artifacts (offers, email threads, responses)
- **`closure_proof/`**: Merit proof documents (if loan closed)

---

## Migration

### From Old to New Structure
```bash
py migrate_structure.py --dry-run     # Preview migration
py migrate_structure.py --force        # Actually migrate
```

**Non-destructive**: Old structure preserved, new created alongside.

---

## Backwards Compatibility

### `masters.json`
- Still works as before
- Now generated from loan folders (aggregate view)
- Sync with: `py -m core.orchestrator --sync`

### Existing Scripts
- `verifier.py` ✅ Unchanged
- `empire.py` ✅ Unchanged
- `loan_verifier.py` ✅ Unchanged
- `generate_verifier_html.py` ✅ Unchanged

---

## Loan Types (`loan_types.json`)

1. **personal**: Standard personal loan (RBI 70% OTS)
2. **lap**: Loan Against Property (RBI 70% OTS)
3. **flexi**: Revolving credit (special rules, may have linked accounts)
4. **home**: Home loan (usually continue, not OTS target)
5. **od**: Overdraft / Business OD (negotiation-based)

---

## Status Types

- **CLOSED**: OS = 0, exclude from OTS, archive eligible
- **PARTIAL**: Partially paid, still OTS target
- **NEW_DISBURSED**: Not yet received, exclude from OTS
- **RUNNING_PAID_EMI**: Active, OTS target
- **NEGOTIATING**: OTS offer sent, track response

---

## Reports

### `reports/dashboard.html`
- Browser → Ctrl+P → Save as PDF
- Print-optimized layout

### `reports/negotiation_dashboard.html`
- Account numbers visible (for negotiation)
- Linked accounts shown (400DFR47319474 → 400LAP14914207)

---

## Expandable Forever

- Add new loan types in `loan_types.json`
- Add new status types as needed
- Core orchestration handles all coordination
- Non-destructive: never breaks existing functionality
