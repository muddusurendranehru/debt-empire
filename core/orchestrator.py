#!/usr/bin/env python3
"""
DEBT-EMPIRE Orchestrator
Main controller that coordinates: duplicate detection, archiving, loan structure, reports.
Non-destructive: works alongside existing verifier.py, empire.py, masters.json
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

# Import core modules
from .duplicate_detector import DuplicateDetector
from .archive_manager import ArchiveManager

class Orchestrator:
    """Main orchestration controller."""
    
    def __init__(self, base_dir=None):
        self.base_dir = Path(base_dir) if base_dir else Path.cwd()
        self.loans_dir = self.base_dir / "loans"
        self.archives_dir = self.base_dir / "archives"
        self.reports_dir = self.base_dir / "reports"
        self.masters_path = self.base_dir / "masters.json"
        self.loan_types_path = self.base_dir / "loan_types.json"
        
        # Initialize core modules
        self.duplicate_detector = DuplicateDetector(self.loans_dir)
        self.archive_manager = ArchiveManager(self.loans_dir, self.archives_dir)
        
        # Ensure directories exist
        self.loans_dir.mkdir(exist_ok=True)
        self.archives_dir.mkdir(exist_ok=True)
        self.reports_dir.mkdir(exist_ok=True)
    
    def normalize_loan_folder_name(self, provider, account):
        """Create normalized folder name: provider-account (lowercase, safe)."""
        provider_clean = provider.lower().replace('&', '').replace(' ', '-').replace('/', '-')
        account_clean = str(account).lower().replace(' ', '').replace('/', '-')[:30]
        return f"{provider_clean}-{account_clean}"
    
    def get_loan_folder(self, provider, account):
        """Get or create loan folder path."""
        folder_name = self.normalize_loan_folder_name(provider, account)
        return self.loans_dir / folder_name
    
    def ensure_loan_structure(self, loan_folder):
        """Ensure loan folder has required structure: loan.json, statements/, ots/, closure_proof/"""
        loan_path = Path(loan_folder)
        loan_path.mkdir(parents=True, exist_ok=True)
        
        # Create subdirectories
        (loan_path / "statements").mkdir(exist_ok=True)
        (loan_path / "ots").mkdir(exist_ok=True)
        (loan_path / "closure_proof").mkdir(exist_ok=True)
        
        return loan_path
    
    def migrate_loan(self, loan_data, source_folder=None):
        """Migrate loan from old structure (Provider/Account/) to new (provider-account/)."""
        provider = loan_data.get('provider', 'Unknown')
        account = loan_data.get('account_number') or loan_data.get('account_ref', 'unknown')
        
        # New folder structure
        new_folder = self.get_loan_folder(provider, account)
        self.ensure_loan_structure(new_folder)
        
        # Create/update loan.json
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
            "migrated_from": str(source_folder) if source_folder else None
        }
        
        with open(loan_json, 'w', encoding='utf-8') as f:
            json.dump(loan_record, f, indent=2, ensure_ascii=False)
        
        # Migrate existing files from old structure
        if source_folder:
            old_path = Path(source_folder)
            if old_path.exists():
                # Move meta.json if exists
                old_meta = old_path / "meta.json"
                if old_meta.exists() and not (new_folder / "meta.json").exists():
                    shutil.copy2(old_meta, new_folder / "meta.json")
                
                # Move docs/ to statements/
                old_docs = old_path / "docs"
                if old_docs.exists():
                    new_statements = new_folder / "statements"
                    for item in old_docs.iterdir():
                        if item.is_file():
                            shutil.copy2(item, new_statements / item.name)
        
        return new_folder
    
    def sync_masters_json(self):
        """Sync masters.json with loan folders (aggregate view)."""
        if not self.masters_path.exists():
            return {"loans": [], "total_exposure": 0, "total_ots_liability": 0, "total_savings": 0}
        
        with open(self.masters_path, 'r', encoding='utf-8') as f:
            masters = json.load(f)
        
        # Aggregate from loan folders
        loans = []
        for loan_folder in self.loans_dir.iterdir():
            if not loan_folder.is_dir():
                continue
            
            loan_json = loan_folder / "loan.json"
            if not loan_json.exists():
                continue
            
            try:
                with open(loan_json, 'r', encoding='utf-8') as f:
                    loan_data = json.load(f)
                
                # Convert to masters.json format (backwards compatible)
                loan_record = {
                    "provider": loan_data.get('provider', ''),
                    "outstanding": loan_data.get('outstanding_principal', 0),
                    "emi": loan_data.get('emi_amount', 0),
                    "tenure_months": loan_data.get('tenure_remaining_months', 0),
                    "account_ref": loan_data.get('account_number') or loan_data.get('account_ref', ''),
                    "start_date": loan_data.get('start_date', ''),
                    "status": loan_data.get('status', 'RUNNING_PAID_EMI')
                }
                
                # Calculate OTS (70%)
                loan_record["ots_amount_70pct"] = round(loan_record["outstanding"] * 0.70)
                loan_record["savings"] = loan_record["outstanding"] - loan_record["ots_amount_70pct"]
                
                loans.append(loan_record)
            except Exception as e:
                print(f"[WARN] Could not load {loan_json}: {e}")
        
        # Calculate totals
        total_exposure = sum(l.get('outstanding', 0) for l in loans)
        total_ots = sum(l.get('ots_amount_70pct', 0) for l in loans)
        total_savings = total_exposure - total_ots
        
        masters["loans"] = loans
        masters["total_exposure"] = total_exposure
        masters["total_ots_liability"] = total_ots
        masters["total_savings"] = total_savings
        masters["generated_at"] = datetime.now().isoformat()
        
        # Save updated masters.json
        with open(self.masters_path, 'w', encoding='utf-8') as f:
            json.dump(masters, f, indent=2, ensure_ascii=False)
        
        return masters
    
    def auto_archive_closed(self, dry_run=True):
        """Auto-archive closed loans."""
        return self.archive_manager.auto_archive_closed(dry_run=dry_run)
    
    def check_duplicates(self, file_path):
        """Check if file is duplicate."""
        return self.duplicate_detector.is_duplicate(file_path)
    
    def register_document(self, file_path, loan_folder):
        """Register document in duplicate index."""
        return self.duplicate_detector.register_file(file_path, loan_folder)

def main():
    """CLI for orchestrator."""
    import argparse
    parser = argparse.ArgumentParser(description='DEBT-EMPIRE Orchestrator')
    parser.add_argument('--sync', action='store_true', help='Sync masters.json from loan folders')
    parser.add_argument('--archive', action='store_true', help='Auto-archive closed loans')
    parser.add_argument('--migrate', action='store_true', help='Migrate old structure to new')
    parser.add_argument('--force', action='store_true', help='Actually perform actions (not dry-run)')
    
    args = parser.parse_args()
    
    orchestrator = Orchestrator()
    
    if args.sync:
        print("[SYNC] Syncing masters.json from loan folders...")
        masters = orchestrator.sync_masters_json()
        print(f"[OK] Synced {len(masters['loans'])} loans")
        print(f"  Total Exposure: ₹{masters['total_exposure']/100000:.2f}L")
        print(f"  Total OTS: ₹{masters['total_ots_liability']/100000:.2f}L")
    
    if args.archive:
        archived = orchestrator.auto_archive_closed(dry_run=not args.force)
        if archived:
            print(f"[ARCHIVED] {len(archived)} loans")
        else:
            print("[INFO] No closed loans to archive")
    
    if args.migrate:
        print("[MIGRATE] Migrating old structure to new...")
        # Migration logic (see migration script)
        print("[INFO] Use migrate_structure.py for full migration")

if __name__ == "__main__":
    main()
