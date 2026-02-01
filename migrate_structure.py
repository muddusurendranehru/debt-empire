#!/usr/bin/env python3
"""
Migrate old structure (loans/Provider/Account/) to new (loans/provider-account/).
Non-destructive: keeps old structure, creates new alongside.
"""
import json
import shutil
import sys
from pathlib import Path
from datetime import datetime

# UTF-8 for Windows console
if sys.platform == 'win32' and hasattr(sys.stdout, 'buffer'):
    try:
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    except (AttributeError, ValueError):
        pass  # stdout already wrapped or closed

from core.orchestrator import Orchestrator

def migrate_existing_loans(dry_run=True):
    """Migrate existing loans from old structure to new."""
    base_dir = Path.cwd()
    old_loans_dir = base_dir / "loans"
    orchestrator = Orchestrator(base_dir)
    
    if not old_loans_dir.exists():
        print("[INFO] No loans/ directory found. Nothing to migrate.")
        return []
    
    migrated = []
    
    # Scan old structure: loans/Provider/Account/
    for provider_dir in old_loans_dir.iterdir():
        if not provider_dir.is_dir() or provider_dir.name.startswith('.'):
            continue
        
        for account_dir in provider_dir.iterdir():
            if not account_dir.is_dir():
                continue
            
            # Read meta.json or loan.json
            meta_file = account_dir / "meta.json"
            if not meta_file.exists():
                meta_file = account_dir / "loan.json"
            
            if not meta_file.exists():
                print(f"[SKIP] No meta.json/loan.json in {account_dir}")
                continue
            
            try:
                with open(meta_file, 'r', encoding='utf-8') as f:
                    loan_data = json.load(f)
            except Exception as e:
                print(f"[ERROR] Could not read {meta_file}: {e}")
                continue
            
            # Migrate to new structure
            provider = loan_data.get('provider', provider_dir.name)
            account = loan_data.get('account_number') or loan_data.get('account_ref', account_dir.name)
            
            new_folder = orchestrator.get_loan_folder(provider, account)
            
            if dry_run:
                print(f"[DRY-RUN] Would migrate: {provider_dir.name}/{account_dir.name} → {new_folder.name}")
                migrated.append({
                    "old": str(account_dir),
                    "new": str(new_folder),
                    "provider": provider,
                    "account": account
                })
            else:
                # Ensure new structure
                orchestrator.ensure_loan_structure(new_folder)
                
                # Create loan.json
                loan_json = new_folder / "loan.json"
                loan_record = {
                    "provider": provider,
                    "account_number": account,
                    "account_ref": loan_data.get('account_ref', account),
                    "borrower_name": loan_data.get('borrower_name', ''),
                    "outstanding_principal": loan_data.get('outstanding_principal') or loan_data.get('outstanding', 0),
                    "emi_amount": loan_data.get('emi_amount') or loan_data.get('emi', 0),
                    "tenure_remaining_months": loan_data.get('tenure_remaining_months') or loan_data.get('tenure_months', 0),
                    "loan_type": loan_data.get('loan_type', 'personal'),
                    "status": loan_data.get('status') or loan_data.get('verification_status', 'RUNNING_PAID_EMI'),
                    "linked_account": loan_data.get('linked_account', ''),
                    "interest_rate": loan_data.get('interest_rate', ''),
                    "start_date": loan_data.get('start_date', ''),
                    "updated_at": datetime.now().isoformat(),
                    "migrated_from": str(account_dir)
                }
                
                with open(loan_json, 'w', encoding='utf-8') as f:
                    json.dump(loan_record, f, indent=2, ensure_ascii=False)
                
                # Copy meta.json if exists
                if meta_file.exists() and meta_file.name == "meta.json":
                    shutil.copy2(meta_file, new_folder / "meta.json")
                
                # Copy docs/ to statements/
                old_docs = account_dir / "docs"
                if old_docs.exists():
                    new_statements = new_folder / "statements"
                    for item in old_docs.iterdir():
                        if item.is_file():
                            shutil.copy2(item, new_statements / item.name)
                
                print(f"[OK] Migrated: {provider_dir.name}/{account_dir.name} → {new_folder.name}")
                migrated.append({
                    "old": str(account_dir),
                    "new": str(new_folder),
                    "provider": provider,
                    "account": account
                })
    
    return migrated

def main():
    """CLI for migration."""
    import argparse
    parser = argparse.ArgumentParser(description='Migrate loan structure')
    parser.add_argument('--dry-run', action='store_true', default=True, help='Dry run (default)')
    parser.add_argument('--force', action='store_true', help='Actually migrate (not dry-run)')
    
    args = parser.parse_args()
    dry_run = not args.force
    
    print("=" * 70)
    print("DEBT-EMPIRE Structure Migration")
    print("=" * 70)
    print(f"Mode: {'DRY-RUN' if dry_run else 'MIGRATE'}")
    print("=" * 70)
    
    migrated = migrate_existing_loans(dry_run=dry_run)
    
    print("=" * 70)
    if migrated:
        print(f"[OK] {'Would migrate' if dry_run else 'Migrated'} {len(migrated)} loans")
        if not dry_run:
            print("\n[INFO] Old structure preserved. New structure created.")
            print("  Old: loans/Provider/Account/")
            print("  New: loans/provider-account/")
    else:
        print("[INFO] No loans to migrate")
    print("=" * 70)

if __name__ == "__main__":
    main()
