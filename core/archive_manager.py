#!/usr/bin/env python3
"""
Yearly auto-archiving for closed/settled loans.
Moves loans from loans/ to archives/YYYY/ based on closure date or status.
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

class ArchiveManager:
    """Manage yearly archiving of closed loans."""
    
    def __init__(self, loans_dir=None, archives_dir=None):
        self.loans_dir = Path(loans_dir) if loans_dir else Path.cwd() / "loans"
        self.archives_dir = Path(archives_dir) if archives_dir else Path.cwd() / "archives"
        self.archives_dir.mkdir(exist_ok=True)
    
    def get_archive_year(self, loan_data=None, closure_date=None):
        """Determine archive year from loan data or closure date."""
        if closure_date:
            try:
                if isinstance(closure_date, str):
                    year = datetime.fromisoformat(closure_date).year
                else:
                    year = closure_date.year
                return year
            except:
                pass
        
        if loan_data:
            # Check closure_date, closed_at, settlement_date
            for date_field in ['closure_date', 'closed_at', 'settlement_date', 'end_date']:
                if date_field in loan_data and loan_data[date_field]:
                    try:
                        year = datetime.fromisoformat(loan_data[date_field]).year
                        return year
                    except:
                        pass
        
        # Default to current year
        return datetime.now().year
    
    def is_closed(self, loan_data):
        """Check if loan is closed (status=CLOSED or OS=0)."""
        status = (loan_data.get('status') or loan_data.get('verification_status') or '').upper()
        os_amt = loan_data.get('outstanding_principal') or loan_data.get('outstanding', 0)
        
        return status == 'CLOSED' or os_amt <= 0
    
    def archive_loan(self, loan_folder, loan_data=None, dry_run=True):
        """Archive a single loan folder to archives/YYYY/."""
        loan_path = Path(loan_folder)
        if not loan_path.exists():
            return False, f"Loan folder not found: {loan_folder}"
        
        # Determine archive year
        archive_year = self.get_archive_year(loan_data)
        archive_path = self.archives_dir / str(archive_year)
        archive_path.mkdir(exist_ok=True)
        
        # Destination: archives/YYYY/loan-folder-name/
        dest_path = archive_path / loan_path.name
        
        if dest_path.exists():
            return False, f"Already archived: {dest_path}"
        
        if dry_run:
            return True, f"[DRY-RUN] Would move {loan_path} → {dest_path}"
        
        try:
            shutil.move(str(loan_path), str(dest_path))
            return True, f"Archived: {loan_path.name} → {archive_year}/"
        except Exception as e:
            return False, f"Error archiving: {e}"
    
    def auto_archive_closed(self, dry_run=True):
        """Auto-archive all closed loans from loans/ directory."""
        if not self.loans_dir.exists():
            return []
        
        archived = []
        
        # Scan all loan folders
        for provider_dir in self.loans_dir.iterdir():
            if not provider_dir.is_dir():
                continue
            
            for loan_dir in provider_dir.iterdir():
                if not loan_dir.is_dir():
                    continue
                
                # Check loan.json or meta.json
                loan_json = loan_dir / "loan.json"
                if not loan_json.exists():
                    loan_json = loan_dir / "meta.json"
                
                loan_data = {}
                if loan_json.exists():
                    try:
                        with open(loan_json, 'r', encoding='utf-8') as f:
                            loan_data = json.load(f)
                    except:
                        pass
                
                # Check if closed
                if self.is_closed(loan_data):
                    success, message = self.archive_loan(loan_dir, loan_data, dry_run=dry_run)
                    if success:
                        archived.append({
                            "loan": loan_dir.name,
                            "provider": provider_dir.name,
                            "message": message
                        })
        
        return archived
    
    def list_archived(self, year=None):
        """List archived loans (optionally filter by year)."""
        if not self.archives_dir.exists():
            return []
        
        archived = []
        
        for year_dir in sorted(self.archives_dir.iterdir()):
            if not year_dir.is_dir():
                continue
            
            if year and year_dir.name != str(year):
                continue
            
            for loan_dir in year_dir.iterdir():
                if loan_dir.is_dir():
                    archived.append({
                        "year": year_dir.name,
                        "loan": loan_dir.name,
                        "path": str(loan_dir)
                    })
        
        return archived

def main():
    """CLI for archive management."""
    import argparse
    parser = argparse.ArgumentParser(description='Manage loan archives')
    parser.add_argument('--auto', action='store_true', help='Auto-archive closed loans')
    parser.add_argument('--loan', type=str, help='Archive specific loan folder')
    parser.add_argument('--year', type=int, help='Archive year (default: current)')
    parser.add_argument('--list', action='store_true', help='List archived loans')
    parser.add_argument('--force', action='store_true', help='Actually archive (not dry-run)')
    
    args = parser.parse_args()
    
    manager = ArchiveManager()
    
    if args.auto:
        archived = manager.auto_archive_closed(dry_run=not args.force)
        if archived:
            print(f"[ARCHIVED] {len(archived)} loans")
            for a in archived:
                print(f"  {a['provider']}/{a['loan']}: {a['message']}")
        else:
            print("[INFO] No closed loans to archive")
    
    if args.loan:
        loan_path = Path(args.loan)
        loan_data = {}
        loan_json = loan_path / "loan.json"
        if loan_json.exists():
            with open(loan_json, 'r', encoding='utf-8') as f:
                loan_data = json.load(f)
        
        success, message = manager.archive_loan(loan_path, loan_data, dry_run=not args.force)
        print(message)
    
    if args.list:
        archived = manager.list_archived(year=args.year)
        if archived:
            print(f"[ARCHIVED LOANS] {len(archived)} found")
            for a in archived:
                print(f"  {a['year']}/{a['loan']}")
        else:
            print("[INFO] No archived loans found")

if __name__ == "__main__":
    main()
