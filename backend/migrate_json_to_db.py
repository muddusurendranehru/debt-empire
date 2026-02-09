"""
Migration script: Migrate masters.json data to database
Run this once to migrate existing JSON data to PostgreSQL
"""

import json
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from database import init_db
from database.models import User, Loan
from database.connection import test_connection

def migrate_masters_json():
    """Migrate masters.json to database."""
    
    # Check database connection
    if not test_connection():
        print("❌ Database connection failed. Please check DATABASE_URL in .env")
        return False
    
    # Initialize schema
    print("Initializing database schema...")
    init_db()
    
    # Load masters.json
    masters_json_path = Path(__file__).parent.parent / "masters.json"
    
    if not masters_json_path.exists():
        print(f"❌ masters.json not found at {masters_json_path}")
        return False
    
    print(f"Loading {masters_json_path}...")
    with open(masters_json_path, 'r', encoding='utf-8') as f:
        masters_data = json.load(f)
    
    # Create a default user for migration (or use existing)
    # In production, you should create users through signup
    print("\n⚠️  NOTE: This script creates a default user for migration.")
    print("   In production, users should sign up through the frontend.")
    
    default_email = "migrated@debt-empire.local"
    default_password = "migration-temp-password-change-me"
    
    # Check if user exists
    user = User.get_by_email(default_email)
    if not user:
        from auth import hash_password
        password_hash = hash_password(default_password)
        user = User.create(
            email=default_email,
            password_hash=password_hash,
            phone=None
        )
        print(f"✅ Created default user: {default_email}")
    else:
        print(f"✅ Using existing user: {default_email}")
    
    user_id = user['id']
    
    # Migrate loans
    loans_data = masters_data.get('loans', [])
    
    if not loans_data:
        print("⚠️  No loans found in masters.json")
        return True
    
    print(f"\nMigrating {len(loans_data)} loans...")
    
    migrated_count = 0
    for loan_data in loans_data:
        try:
            # Create loan in database
            loan = Loan.create(
                user_id=user_id,
                provider=loan_data.get('provider', 'Unknown'),
                outstanding=loan_data.get('outstanding', 0),
                emi=loan_data.get('emi', 0),
                tenure_months=loan_data.get('tenure_months', 0),
                account_ref=loan_data.get('account_ref'),
                start_date=loan_data.get('start_date'),
                loan_type=loan_data.get('loan_type', 'personal'),
                status=loan_data.get('status', 'RUNNING_PAID_EMI')
            )
            migrated_count += 1
            print(f"  ✅ Migrated: {loan['provider']} - {loan.get('account_ref', 'N/A')}")
        except Exception as e:
            print(f"  ❌ Failed to migrate loan {loan_data.get('provider', 'Unknown')}: {e}")
    
    print(f"\n✅ Migration complete: {migrated_count}/{len(loans_data)} loans migrated")
    print(f"\n⚠️  IMPORTANT: Change the password for user {default_email} or create a new user through signup!")
    
    return True


if __name__ == "__main__":
    print("=" * 70)
    print("DEBT EMPIRE - JSON to Database Migration")
    print("=" * 70)
    
    success = migrate_masters_json()
    
    if success:
        print("\n✅ Migration completed successfully!")
    else:
        print("\n❌ Migration failed. Please check the errors above.")
        sys.exit(1)
