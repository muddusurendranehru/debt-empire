"""
Database models and helper functions
"""

from typing import Optional, Dict, Any
from datetime import datetime
import uuid
from .connection import get_db


class User:
    """User model for authentication."""
    
    @staticmethod
    def create(email: str, password_hash: str, phone: Optional[str] = None) -> Dict[str, Any]:
        """Create a new user."""
        with get_db() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO users (email, password_hash, phone)
                    VALUES (%s, %s, %s)
                    RETURNING id, email, phone, created_at
                    """,
                    (email, password_hash, phone)
                )
                result = cur.fetchone()
                return {
                    'id': str(result[0]),
                    'email': result[1],
                    'phone': result[2],
                    'created_at': result[3].isoformat() if result[3] else None
                }
    
    @staticmethod
    def get_by_email(email: str) -> Optional[Dict[str, Any]]:
        """Get user by email."""
        with get_db() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT id, email, password_hash, phone, created_at FROM users WHERE email = %s",
                    (email,)
                )
                result = cur.fetchone()
                if result:
                    return {
                        'id': str(result[0]),
                        'email': result[1],
                        'password_hash': result[2],
                        'phone': result[3],
                        'created_at': result[4].isoformat() if result[4] else None
                    }
                return None
    
    @staticmethod
    def get_by_id(user_id: str) -> Optional[Dict[str, Any]]:
        """Get user by ID."""
        with get_db() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT id, email, phone, created_at FROM users WHERE id = %s",
                    (user_id,)
                )
                result = cur.fetchone()
                if result:
                    return {
                        'id': str(result[0]),
                        'email': result[1],
                        'phone': result[2],
                        'created_at': result[3].isoformat() if result[3] else None
                    }
                return None


class Loan:
    """Loan model."""
    
    @staticmethod
    def create(user_id: str, provider: str, outstanding: int, emi: int,
               tenure_months: int, account_ref: Optional[str] = None,
               start_date: Optional[str] = None, loan_type: str = 'personal',
               status: str = 'RUNNING_PAID_EMI') -> Dict[str, Any]:
        """Create a new loan."""
        ots_amount_70pct = round(outstanding * 0.70)
        savings = outstanding - ots_amount_70pct
        
        with get_db() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO loans (user_id, provider, account_ref, outstanding, emi,
                                     tenure_months, ots_amount_70pct, savings, start_date,
                                     loan_type, status)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    RETURNING id, user_id, provider, account_ref, outstanding, emi,
                             tenure_months, ots_amount_70pct, savings, start_date,
                             loan_type, status, created_at
                    """,
                    (user_id, provider, account_ref, outstanding, emi, tenure_months,
                     ots_amount_70pct, savings, start_date, loan_type, status)
                )
                result = cur.fetchone()
                return {
                    'id': str(result[0]),
                    'user_id': str(result[1]),
                    'provider': result[2],
                    'account_ref': result[3],
                    'outstanding': result[4],
                    'emi': result[5],
                    'tenure_months': result[6],
                    'ots_amount_70pct': result[7],
                    'savings': result[8],
                    'start_date': result[9].isoformat() if result[9] else None,
                    'loan_type': result[10],
                    'status': result[11],
                    'created_at': result[12].isoformat() if result[12] else None
                }
    
    @staticmethod
    def get_by_user(user_id: str) -> list:
        """Get all loans for a user."""
        with get_db() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT id, user_id, provider, account_ref, outstanding, emi,
                           tenure_months, ots_amount_70pct, savings, start_date,
                           loan_type, status, created_at, updated_at
                    FROM loans
                    WHERE user_id = %s
                    ORDER BY created_at DESC
                    """,
                    (user_id,)
                )
                results = cur.fetchall()
                loans = []
                for row in results:
                    loans.append({
                        'id': str(row[0]),
                        'user_id': str(row[1]),
                        'provider': row[2],
                        'account_ref': row[3],
                        'outstanding': row[4],
                        'emi': row[5],
                        'tenure_months': row[6],
                        'ots_amount_70pct': row[7],
                        'savings': row[8],
                        'start_date': row[9].isoformat() if row[9] else None,
                        'loan_type': row[10],
                        'status': row[11],
                        'created_at': row[12].isoformat() if row[12] else None,
                        'updated_at': row[13].isoformat() if row[13] else None
                    })
                return loans
    
    @staticmethod
    def get_by_id(loan_id: str) -> Optional[Dict[str, Any]]:
        """Get loan by ID."""
        with get_db() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT id, user_id, provider, account_ref, outstanding, emi,
                           tenure_months, ots_amount_70pct, savings, start_date,
                           loan_type, status, created_at, updated_at
                    FROM loans
                    WHERE id = %s
                    """,
                    (loan_id,)
                )
                result = cur.fetchone()
                if result:
                    return {
                        'id': str(result[0]),
                        'user_id': str(result[1]),
                        'provider': result[2],
                        'account_ref': result[3],
                        'outstanding': result[4],
                        'emi': result[5],
                        'tenure_months': result[6],
                        'ots_amount_70pct': result[7],
                        'savings': result[8],
                        'start_date': result[9].isoformat() if result[9] else None,
                        'loan_type': result[10],
                        'status': result[11],
                        'created_at': result[12].isoformat() if result[12] else None,
                        'updated_at': result[13].isoformat() if result[13] else None
                    }
                return None
    
    @staticmethod
    def update(loan_id: str, **kwargs) -> bool:
        """Update loan fields."""
        allowed_fields = ['outstanding', 'emi', 'tenure_months', 'status', 'account_ref']
        updates = {k: v for k, v in kwargs.items() if k in allowed_fields}
        
        if not updates:
            return False
        
        # Recalculate OTS and savings if outstanding changed
        if 'outstanding' in updates:
            updates['ots_amount_70pct'] = round(updates['outstanding'] * 0.70)
            updates['savings'] = updates['outstanding'] - updates['ots_amount_70pct']
        
        set_clause = ', '.join([f"{k} = %s" for k in updates.keys()])
        set_clause += ", updated_at = NOW()"
        values = list(updates.values()) + [loan_id]
        
        with get_db() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    f"UPDATE loans SET {set_clause} WHERE id = %s",
                    values
                )
                return cur.rowcount > 0
    
    @staticmethod
    def delete(loan_id: str) -> bool:
        """Delete a loan."""
        with get_db() as conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM loans WHERE id = %s", (loan_id,))
                return cur.rowcount > 0


class MonthlyStatement:
    """Monthly statement model."""
    
    @staticmethod
    def create(user_id: str, month_name: str, csv_path: Optional[str] = None,
               parsed_data: Optional[Dict] = None) -> Dict[str, Any]:
        """Create a monthly statement record."""
        import json
        with get_db() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO monthly_statements (user_id, month_name, csv_path, parsed_data)
                    VALUES (%s, %s, %s, %s)
                    RETURNING id, user_id, month_name, csv_path, created_at
                    """,
                    (user_id, month_name, csv_path, json.dumps(parsed_data) if parsed_data else None)
                )
                result = cur.fetchone()
                return {
                    'id': str(result[0]),
                    'user_id': str(result[1]),
                    'month_name': result[2],
                    'csv_path': result[3],
                    'created_at': result[4].isoformat() if result[4] else None
                }


class Projection:
    """Projection model."""
    
    @staticmethod
    def create(user_id: str, loan_id: str, month_name: str,
               projection_data: Optional[Dict] = None, excel_path: Optional[str] = None) -> Dict[str, Any]:
        """Create a projection record."""
        import json
        with get_db() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO projections (user_id, loan_id, month_name, projection_data, excel_path)
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING id, user_id, loan_id, month_name, created_at
                    """,
                    (user_id, loan_id, month_name,
                     json.dumps(projection_data) if projection_data else None,
                     excel_path)
                )
                result = cur.fetchone()
                return {
                    'id': str(result[0]),
                    'user_id': str(result[1]),
                    'loan_id': str(result[2]),
                    'month_name': result[3],
                    'created_at': result[4].isoformat() if result[4] else None
                }
