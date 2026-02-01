#!/usr/bin/env python3
"""
DEBT-EMPIRE v2.0 - Folder Structure Builder
Auto-create: folder-per-loan + duplicate detection + yearly archive.
KEEPS ALL existing files (masters.json, loan_verifier.py, empire.py, etc.).
"""
import json
import sys
from pathlib import Path
from datetime import datetime

# UTF-8 for Windows console
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

DATA_DIR = Path.cwd()
MASTERS_PATH = DATA_DIR / "masters.json"
LOANS_DIR = DATA_DIR / "loans"
ARCHIVE_DIR = DATA_DIR / "archive"

# 5 Loan Types
LOAN_TYPES = ("personal", "lap", "flexi", "home", "od")

def normalize_provider(name):
    """Normalize lender name for folder (safe path)."""
    if not name:
        return "Unknown"
    return name.replace("&", "and").replace("/", "-").replace(" ", "_").strip()

def normalize_account(account):
    """Normalize account id for folder."""
    if account is None:
        return "unknown"
    return str(account).strip().upper().replace(" ", "")

def get_loan_key(loan):
    """Unique key for duplicate detection: provider + account."""
    provider = normalize_provider(loan.get("provider", ""))
    account = normalize_account(loan.get("account_number") or loan.get("account_ref", ""))
    return (provider, account)

def load_masters():
    if not MASTERS_PATH.exists():
        return {"loans": []}
    with open(MASTERS_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
        if "loans" not in data:
            data["loans"] = []
        return data

# 5 LOAN STATUS TYPES (masters.json): CLOSED | PARTIAL | NEW_DISBURSED | RUNNING_PAID_EMI | NEGOTIATING
LOAN_STATUSES = ("CLOSED", "PARTIAL", "NEW_DISBURSED", "RUNNING_PAID_EMI", "NEGOTIATING")

def build_meta(loan):
    """Build meta.json content for a loan folder."""
    os_amt = loan.get("outstanding_principal") or loan.get("outstanding", 0)
    status = loan.get("status") or loan.get("verification_status", "RUNNING_PAID_EMI")
    if status not in LOAN_STATUSES:
        status = "RUNNING_PAID_EMI" if os_amt and os_amt > 0 else "CLOSED"
    return {
        "provider": loan.get("provider", ""),
        "product": loan.get("product", ""),
        "account_number": loan.get("account_number") or loan.get("account_ref", ""),
        "linked_account": loan.get("linked_account", ""),
        "borrower_name": loan.get("borrower_name", ""),
        "outstanding_principal": os_amt,
        "emi_amount": loan.get("emi_amount") or loan.get("emi", 0),
        "tenure_remaining_months": loan.get("tenure_remaining_months") or loan.get("tenure_months", 0),
        "loan_type": loan.get("loan_type", "personal"),
        "status": status,
        "verification_status": loan.get("verification_status", "pending"),
        "updated_at": datetime.now().isoformat(),
    }

def run():
    print("=" * 70)
    print("DEBT-EMPIRE v2.0 - Structure Builder")
    print("=" * 70)
    print(f"Working dir: {DATA_DIR}")
    print(f"masters.json: {MASTERS_PATH}")
    print("=" * 70)

    masters = load_masters()
    loans = masters.get("loans", [])
    if not loans:
        print("[!] No loans in masters.json. Run loan_verifier.py first.")
        return

    # Create archive for current year
    year = datetime.now().year
    (ARCHIVE_DIR / str(year)).mkdir(parents=True, exist_ok=True)
    print(f"[OK] archive/{year}/")

    seen = set()
    created = 0
    skipped_dup = 0

    for loan in loans:
        provider = normalize_provider(loan.get("provider", ""))
        account = normalize_account(
            loan.get("account_number") or loan.get("account_ref") or loan.get("id", "")
        )
        if not account or account == "UNKNOWN":
            account = f"loan_{created + 1}"

        key = (provider, account)
        if key in seen:
            skipped_dup += 1
            print(f"  [SKIP duplicate] {provider} / {account}")
            continue
        seen.add(key)

        loan_dir = LOANS_DIR / provider / account
        loan_dir.mkdir(parents=True, exist_ok=True)
        docs_dir = loan_dir / "docs"
        docs_dir.mkdir(exist_ok=True)

        meta_path = loan_dir / "meta.json"
        meta = build_meta(loan)
        with open(meta_path, "w", encoding="utf-8") as f:
            json.dump(meta, f, indent=2, ensure_ascii=False)

        created += 1
        print(f"  [OK] loans/{provider}/{account}/")

    print("=" * 70)
    print(f"Created/updated: {created} loan folders")
    if skipped_dup:
        print(f"Skipped (duplicate): {skipped_dup}")
    print("  loans/  = folder-per-loan + meta.json + docs/")
    print("  archive/ = yearly archive (manual move for settled loans)")
    print("=" * 70)

if __name__ == "__main__":
    run()
