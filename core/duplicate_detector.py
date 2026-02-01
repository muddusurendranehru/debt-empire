#!/usr/bin/env python3
"""
SHA256-based duplicate detection for loan documents and statements.
Prevents duplicate uploads and tracks document versions.
"""
import hashlib
import json
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

class DuplicateDetector:
    """Detect duplicate files using SHA256 hashing."""
    
    def __init__(self, loans_dir=None):
        self.loans_dir = Path(loans_dir) if loans_dir else Path.cwd() / "loans"
        self.hash_index = {}  # sha256 -> {loan_path, filename, date}
        self._load_index()
    
    def _load_index(self):
        """Load existing hash index from loans/ directories."""
        index_file = self.loans_dir.parent / ".duplicate_index.json"
        if index_file.exists():
            try:
                with open(index_file, 'r', encoding='utf-8') as f:
                    self.hash_index = json.load(f)
            except Exception as e:
                print(f"[WARN] Could not load duplicate index: {e}")
                self.hash_index = {}
    
    def _save_index(self):
        """Save hash index to disk."""
        index_file = self.loans_dir.parent / ".duplicate_index.json"
        try:
            with open(index_file, 'w', encoding='utf-8') as f:
                json.dump(self.hash_index, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"[WARN] Could not save duplicate index: {e}")
    
    def compute_hash(self, file_path):
        """Compute SHA256 hash of file."""
        sha256 = hashlib.sha256()
        try:
            with open(file_path, 'rb') as f:
                for chunk in iter(lambda: f.read(4096), b''):
                    sha256.update(chunk)
            return sha256.hexdigest()
        except Exception as e:
            print(f"[ERROR] Could not hash {file_path}: {e}")
            return None
    
    def is_duplicate(self, file_path):
        """Check if file is duplicate (by hash)."""
        file_hash = self.compute_hash(file_path)
        if not file_hash:
            return False, None
        
        if file_hash in self.hash_index:
            existing = self.hash_index[file_hash]
            return True, existing
        return False, None
    
    def register_file(self, file_path, loan_folder=None):
        """Register file in hash index."""
        file_hash = self.compute_hash(file_path)
        if not file_hash:
            return False
        
        file_path_obj = Path(file_path)
        self.hash_index[file_hash] = {
            "filename": file_path_obj.name,
            "loan_folder": str(loan_folder) if loan_folder else None,
            "full_path": str(file_path_obj.absolute()),
            "size": file_path_obj.stat().st_size,
            "registered_at": datetime.now().isoformat()
        }
        self._save_index()
        return True
    
    def find_duplicates_in_loan(self, loan_folder):
        """Find duplicate files within a loan folder."""
        loan_path = Path(loan_folder)
        if not loan_path.exists():
            return []
        
        duplicates = []
        seen_hashes = {}
        
        # Scan statements/, ots/, closure_proof/
        for subdir in ['statements', 'ots', 'closure_proof']:
            subdir_path = loan_path / subdir
            if not subdir_path.exists():
                continue
            
            for file_path in subdir_path.rglob('*'):
                if not file_path.is_file():
                    continue
                
                file_hash = self.compute_hash(file_path)
                if not file_hash:
                    continue
                
                if file_hash in seen_hashes:
                    duplicates.append({
                        "file": str(file_path.relative_to(loan_path)),
                        "duplicate_of": seen_hashes[file_hash],
                        "hash": file_hash
                    })
                else:
                    seen_hashes[file_hash] = str(file_path.relative_to(loan_path))
        
        return duplicates
    
    def cleanup_duplicates(self, loan_folder, dry_run=True):
        """Remove duplicate files (keep first occurrence)."""
        duplicates = self.find_duplicates_in_loan(loan_folder)
        if not duplicates:
            return []
        
        removed = []
        loan_path = Path(loan_folder)
        
        for dup in duplicates:
            dup_file = loan_path / dup["file"]
            if dup_file.exists():
                if not dry_run:
                    dup_file.unlink()
                removed.append(str(dup_file))
        
        return removed

def main():
    """CLI for duplicate detection."""
    import argparse
    parser = argparse.ArgumentParser(description='Detect duplicate loan documents')
    parser.add_argument('--check', type=str, help='Check file for duplicates')
    parser.add_argument('--loan', type=str, help='Check loan folder for duplicates')
    parser.add_argument('--cleanup', action='store_true', help='Remove duplicates (dry-run by default)')
    parser.add_argument('--force', action='store_true', help='Actually remove duplicates')
    
    args = parser.parse_args()
    
    detector = DuplicateDetector()
    
    if args.check:
        is_dup, existing = detector.is_duplicate(args.check)
        if is_dup:
            print(f"[DUPLICATE] {args.check}")
            print(f"  Matches: {existing.get('full_path')}")
        else:
            print(f"[UNIQUE] {args.check}")
            detector.register_file(args.check)
    
    if args.loan:
        duplicates = detector.find_duplicates_in_loan(args.loan)
        if duplicates:
            print(f"[FOUND] {len(duplicates)} duplicates in {args.loan}")
            for dup in duplicates:
                print(f"  {dup['file']} → duplicate of {dup['duplicate_of']}")
        else:
            print(f"[CLEAN] No duplicates in {args.loan}")
        
        if args.cleanup:
            removed = detector.cleanup_duplicates(args.loan, dry_run=not args.force)
            if removed:
                print(f"[REMOVED] {len(removed)} duplicate files")
                for r in removed:
                    print(f"  {r}")

if __name__ == "__main__":
    main()
