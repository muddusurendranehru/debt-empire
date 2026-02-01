#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Debt Empire v2.0 - Core Empire Function (Simple Version)
Works without pandas/reportlab - generates JSON only
"""

import os
import json
import sys
from pathlib import Path
from datetime import datetime, timedelta

# Set UTF-8 encoding for Windows console
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')


def empire():
    """Main EMPIRE function - Generate masters.json and projections (JSON format)."""
    
    # Create output directories
    os.makedirs('ots-pdfs', exist_ok=True)
    
    # Hardcode outstanding balances (from provided documents)
    loans = [
        {
            'provider': 'L&T',
            'outstanding': 2574000,  # ₹25.74L from FORECLOSURE_BL240910207908339.pdf
            'emi': 80000,
            'start_date': '2024-04-03'
        },
        {
            'provider': 'HDFC',
            'outstanding': 2450000,  # ₹24.5L from hdfc24loan1.docx
            'emi': 189000,
            'start_date': '2024-04-05'
        }
    ]
    
    # Generate masters.json
    masters_data = {'loans': []}
    for loan in loans:
        tenure = round(loan['outstanding'] / loan['emi'])
        masters_data['loans'].append({
            'provider': loan['provider'],
            'outstanding': loan['outstanding'],
            'emi': loan['emi'],
            'tenure_months': tenure,
            'ots_amount': round(loan['outstanding'] * 0.70),  # RBI OTS 70% rule
            'start_date': loan['start_date']
        })
    
    masters_file = Path('masters.json')
    with open(masters_file, 'w', encoding='utf-8') as f:
        json.dump(masters_data, f, indent=2, ensure_ascii=False)
    print(f"[OK] masters.json created: {masters_file.absolute()}")
    
    # Generate monthly projections (JSON format)
    projections = []
    for loan in loans:
        balance = loan['outstanding']
        date = datetime.strptime(loan['start_date'], '%Y-%m-%d')
        month = 1
        
        while balance > 0 and month <= 60:  # Cap at 5 years
            emi_amt = min(loan['emi'], balance)
            projections.append({
                'Month': month,
                'Date': date.strftime('%Y-%m-%d'),
                'Provider': loan['provider'],
                'EMI_Amount': emi_amt,
                'Balance_Remaining': max(0, balance - emi_amt)
            })
            balance -= emi_amt
            date += timedelta(days=30)
            month += 1
    
    projections_file = Path('monthly_projections.json')
    with open(projections_file, 'w', encoding='utf-8') as f:
        json.dump(projections, f, indent=2, ensure_ascii=False)
    print(f"[OK] monthly_projections.json created: {projections_file.absolute()}")
    
    # Summary
    print("\n" + "=" * 70)
    print("DEBT EMPIRE ANALYSIS COMPLETE")
    print("=" * 70)
    total_exposure = sum(l['outstanding'] for l in loans)
    total_ots = sum(round(l['outstanding'] * 0.7) for l in loans)
    print(f"Total Exposure: Rs {total_exposure:,.0f} (Rs {total_exposure/100000:.2f}L)")
    print(f"Total OTS Liability (70%): Rs {total_ots:,.0f} (Rs {total_ots/100000:.2f}L)")
    print(f"Total Savings: Rs {total_exposure - total_ots:,.0f} (Rs {(total_exposure - total_ots)/100000:.2f}L)")
    print("=" * 70)
    
    # L&T OTS details
    lt_loan = [l for l in loans if l['provider'] == 'L&T'][0]
    lt_ots = round(lt_loan['outstanding'] * 0.70)
    print(f"\nL&T OTS Details:")
    print(f"  Outstanding: Rs {lt_loan['outstanding']:,.0f} (Rs {lt_loan['outstanding']/100000:.2f}L)")
    print(f"  OTS Amount (70%): Rs {lt_ots:,.0f} (Rs {lt_ots/100000:.2f}L)")
    print(f"  Savings: Rs {lt_loan['outstanding'] - lt_ots:,.0f} (Rs {(lt_loan['outstanding'] - lt_ots)/100000:.2f}L)")


if __name__ == '__main__':
    empire()
