#!/usr/bin/env python3
"""
EMPIRE DEMO - Without pandas (uses built-in csv module)
Alternative if pandas installation fails
"""

import csv
import json
from pathlib import Path
from datetime import datetime

def demo_csv_no_pandas(csv_file: str):
    """Run EMPIRE DEMO using built-in csv module (no pandas needed)."""
    
    print("=" * 70)
    print("EMPIRE DEMO: PARSE CSV (No Pandas Version)")
    print("=" * 70)
    
    # Handle file:344 format
    if csv_file.startswith('file:'):
        file_ref = csv_file.replace('file:', '')
        possible_paths = [
            Path('25aprilcsv.csv'),
            Path(f'{file_ref}.csv'),
            Path('25aprilcsv.csv'),
        ]
        csv_path = None
        for path in possible_paths:
            if path.exists():
                csv_path = path
                break
        if not csv_path:
            print(f"[ERROR] CSV file not found. Tried: {possible_paths}")
            return
    else:
        csv_path = Path(csv_file)
        if not csv_path.exists():
            print(f"[ERROR] CSV file not found: {csv_path}")
            return
    
    # Step 1: LOAD CSV
    print("\n[Step 1] LOAD CSV...")
    rows = []
    try:
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        print(f"[OK] Loaded {len(rows)} rows")
    except Exception as e:
        print(f"[ERROR] Failed to load CSV: {e}")
        return
    
    # Step 2: FILTER Debits >₹20k + keywords
    print("\n[Step 2] FILTER Debits >₹20k + keywords (L&T/HDFC/Tata/Bajaj)...")
    keywords = ['L&T', 'HDFC', 'Tata', 'Bajaj', 'LT', 'lt', 'hdfc', 'tata', 'bajaj']
    
    # Find columns
    if not rows:
        print("[ERROR] No rows in CSV")
        return
    
    debit_col = None
    desc_col = None
    for col in rows[0].keys():
        col_lower = col.lower()
        if 'debit' in col_lower or 'amount' in col_lower:
            debit_col = col
        if 'desc' in col_lower or 'description' in col_lower or 'narration' in col_lower:
            desc_col = col
    
    if not debit_col:
        print(f"[ERROR] Debit/Amount column not found. Columns: {list(rows[0].keys())}")
        return
    
    if not desc_col:
        # Use first text column
        desc_col = [k for k in rows[0].keys() if k != debit_col][0]
        print(f"[WARNING] Using '{desc_col}' as description column")
    
    # Filter rows
    filtered = []
    for row in rows:
        try:
            debit_val = float(str(row.get(debit_col, '0')).replace(',', ''))
            desc_val = str(row.get(desc_col, '')).upper()
            
            if debit_val > 20000:
                # Check keywords
                if any(kw.upper() in desc_val for kw in keywords):
                    filtered.append(row)
        except (ValueError, TypeError):
            continue
    
    print(f"[OK] Filtered {len(filtered)} transactions")
    
    # Step 3: OUTPUT loans.json
    print("\n[Step 3] OUTPUT loans.json...")
    loans_data = {
        'count': len(filtered),
        'total': sum(float(str(r.get(debit_col, '0')).replace(',', '')) for r in filtered),
        'transactions': []
    }
    
    for row in filtered:
        try:
            loans_data['transactions'].append({
                'date': str(row.get('Date', row.get('DATE', ''))),
                'description': str(row.get(desc_col, '')),
                'debit': float(str(row.get(debit_col, '0')).replace(',', ''))
            })
        except:
            continue
    
    loans_json_path = Path('loans.json')
    with open(loans_json_path, 'w', encoding='utf-8') as f:
        json.dump(loans_data, f, indent=2, ensure_ascii=False)
    
    print(f"[OK] Saved: {loans_json_path}")
    print(f"  Count: {loans_data['count']}")
    print(f"  Total: Rs {loans_data['total']:,.2f} (Rs {loans_data['total']/100000:.2f}L)")
    
    # Step 4: HDFC Projection
    print("\n[Step 4] HDFC Projection: 12 rows (P+I split)...")
    hdfc_transactions = [r for r in filtered if 'HDFC' in str(r.get(desc_col, '')).upper()]
    hdfc_total = sum(float(str(r.get(debit_col, '0')).replace(',', '')) for r in hdfc_transactions)
    
    if hdfc_total > 0:
        monthly_emi = hdfc_total / len(hdfc_transactions) if hdfc_transactions else hdfc_total
        principal_part = monthly_emi * 0.60
        interest_part = monthly_emi * 0.40
        outstanding = hdfc_total * 12
        
        print("\n" + "=" * 70)
        print("HDFC PROJECTION (12-Month P+I Split)")
        print("=" * 70)
        print(f"{'Month':<8} {'EMI Total':<12} {'Principal':<12} {'Interest':<12} {'OS Bal':<12}")
        print("-" * 70)
        
        projection_data = []
        for month in range(1, 13):
            outstanding -= principal_part
            if outstanding < 0:
                outstanding = 0
            projection_data.append({
                'Month': f'Mo{month}',
                'EMI Total': round(monthly_emi, 2),
                'Principal Part': round(principal_part, 2),
                'Interest Part': round(interest_part, 2),
                'OS Bal': round(outstanding, 2)
            })
            print(f"{f'Mo{month}':<8} Rs {monthly_emi:>8,.0f} Rs {principal_part:>8,.0f} Rs {interest_part:>8,.0f} Rs {outstanding:>8,.0f}")
        
        print("=" * 70)
        
        # Save as JSON (since we can't create Excel without pandas)
        projection_json = Path('hdfc_projection.json')
        with open(projection_json, 'w', encoding='utf-8') as f:
            json.dump(projection_data, f, indent=2, ensure_ascii=False)
        print(f"\n[OK] Saved: {projection_json} (Excel requires pandas)")
    else:
        print("[WARNING] No HDFC transactions found. Skipping projection.")
    
    # Step 5: PRINT Table + "Monthly ritual LIVE"
    print("\n" + "=" * 70)
    print("MONTHLY RITUAL LIVE")
    print("=" * 70)
    print(f"Transactions filtered: {len(filtered)}")
    print(f"Total debits: Rs {loans_data['total']:,.2f} (Rs {loans_data['total']/100000:.2f}L)")
    print(f"Loans.json: {loans_json_path}")
    if hdfc_total > 0:
        print(f"HDFC Projection: {projection_json}")
    print("=" * 70)
    
    # Verify human
    print("\nVerify human: 'EMIs correct? y/n'")
    response = input("EMIs correct? (y/n): ").strip().lower()
    if response == 'y':
        print("[OK] Verified by human. Demo complete!")
    else:
        print("[NOTE] Human verification skipped or marked incorrect.")

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print("Usage: python DEMO_WITHOUT_PANDAS.py file:344")
        print("   OR: python DEMO_WITHOUT_PANDAS.py 25aprilcsv.csv")
        sys.exit(1)
    
    demo_csv_no_pandas(sys.argv[1])
