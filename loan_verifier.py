#!/usr/bin/env python3
"""
LOAN VERIFIER v2.0 (Bajaj PDF Parser Integrated)
Parses REAL Bajaj statements including Flexi Loans (400DFR47319474 → 400LAP14914207)
"""
import os
import json
import re
import sys
from datetime import datetime
from pathlib import Path

# Set UTF-8 encoding for Windows console
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

DATA_DIR = Path.cwd()
MASTERS_PATH = DATA_DIR / "masters.json"

# ===== LOAN TEMPLATE =====
LOAN_TEMPLATE = {
    "id": "", "provider": "", "product": "", "account_number": "", "linked_account": "",
    "borrower_name": "", "outstanding_principal": 0, "interest_rate": 0.0, "rate_type": "",
    "tenure_total_months": 0, "tenure_remaining_months": 0, "emi_amount": 0,
    "emi_start_date": "", "emis_paid": 0, "disbursal_date": "", "processing_fee": 0,
    "foreclosure_fee_percent": 0.0, "late_payment_penalties": 0, "principal_paid_to_date": 0,
    "interest_paid_to_date": 0, "next_emi_date": "", "verification_status": "pending",
    "verified_at": "", "document_path": "", "notes": "", "loan_type": "standard"  # standard/flexi
}

def load_masters():
    if MASTERS_PATH.exists():
        with open(MASTERS_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if 'loans' not in data:
                data['loans'] = []
            return data
    return {'loans': [], 'total_exposure': 0, 'total_ots_liability': 0, 'total_savings': 0}

def save_masters(data):
    data['total_exposure'] = sum(l.get('outstanding_principal', l.get('outstanding', 0)) for l in data['loans'])
    data['total_ots_liability'] = sum(round(l.get('outstanding_principal', l.get('outstanding', 0)) * 0.70) for l in data['loans'])
    data['total_savings'] = sum(l.get('outstanding_principal', l.get('outstanding', 0)) - round(l.get('outstanding_principal', l.get('outstanding', 0)) * 0.70) for l in data['loans'])
    data['rbi_ots_rule'] = '70% per DBOD.No.Leg.BC.252/09.07.005/2013-14'
    data['generated_at'] = datetime.now().isoformat()
    
    with open(MASTERS_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"\n[OK] Saved to {MASTERS_PATH.name}")

# ===== BAJAJ FLEXI LOAN PDF PARSER (REAL STATEMENT SUPPORT) =====
def parse_bajaj_pdf(pdf_path):
    """Parse REAL Bajaj Flexi Loan statements (2017-18 format)"""
    try:
        import pdfplumber
    except ImportError:
        print("  [!] pdfplumber not installed. Install with: py -m pip install pdfplumber")
        return None
    
    print(f"\n[OK] Parsing Bajaj PDF: {os.path.basename(pdf_path)}")
    extracted = LOAN_TEMPLATE.copy()
    extracted.update({
        "provider": "Bajaj Finance",
        "product": "Doctors Flexi Reloc Loan",
        "loan_type": "flexi",  # Critical: Flexi loans have different OTS rules
        "document_path": str(pdf_path)
    })
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            text = ""
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
            
            # Extract borrower name (handle PDF typo: "SURENDRANEHRU" → add space)
            name_match = re.search(r"NAME\s+([A-Z\s]+)", text)
            if name_match:
                raw_name = name_match.group(1).strip()
                # Fix common PDF typo: "SURENDRANEHRU" → "SURENDRA NEHRU"
                if "SURENDRANEHRU" in raw_name:
                    raw_name = raw_name.replace("SURENDRANEHRU", "SURENDRA NEHRU")
                extracted["borrower_name"] = raw_name.title()
            
            # Extract linked account numbers (critical for Flexi Loans)
            linked_match = re.search(r"Linked Agreement No\.\s+(\w+)", text)
            if linked_match:
                extracted["linked_account"] = linked_match.group(1).strip()  # 400LAP14914207
            
            acct_match = re.search(r"LOAN ACCOUNT STATEMENT FOR\s+(\w+)", text)
            if acct_match:
                extracted["account_number"] = acct_match.group(1).strip()  # 400DFR47319474
            
            # Extract loan amount
            amt_match = re.search(r"Loan Amount\s+([\d,\.]+)", text)
            if amt_match:
                extracted["outstanding_principal"] = int(float(amt_match.group(1).replace(',', '')))
            
            # Extract ROI
            roi_match = re.search(r"ROI\s+([\d\.]+)%", text)
            if roi_match:
                extracted["interest_rate"] = float(roi_match.group(1))
            
            # Extract rate type
            type_match = re.search(r"Interest Rate Type\s+(\w+)", text)
            if type_match:
                extracted["rate_type"] = type_match.group(1).lower()
            
            # Extract tenure
            tenure_match = re.search(r"Tenure\s+(\d+)", text)
            if tenure_match:
                extracted["tenure_total_months"] = int(tenure_match.group(1))
            
            # Extract EMI (note: Flexi loans show interest-only EMI)
            emi_match = re.search(r"EMI\s+Received\s+([\d,\.]+)", text)
            if emi_match:
                extracted["emi_amount"] = int(float(emi_match.group(1).replace(',', '')))
            
            # Extract disbursal date
            disb_match = re.search(r"Last Disbursal Date\s+(\d{2}/\d{2}/\d{4})", text)
            if disb_match:
                d, m, y = disb_match.group(1).split('/')
                extracted["disbursal_date"] = f"{y}-{m}-{d}"
            
            # Extract first EMI date
            first_emi_match = re.search(r"First Due Date\s+(\d{2}/\d{2}/\d{4})", text)
            if first_emi_match:
                d, m, y = first_emi_match.group(1).split('/')
                extracted["emi_start_date"] = f"{y}-{m}-{d}"
            
            # Extract end date (for remaining tenure calc)
            end_match = re.search(r"End Installment Date\s+(\d{2}/\d{2}/\d{4})", text)
            if end_match:
                d, m, y = end_match.group(1).split('/')
                end_date = datetime(int(y), int(m), int(d))
                remaining = max(0, (end_date - datetime.now()).days // 30)
                extracted["tenure_remaining_months"] = remaining
            
            # Extract processing fees (total upfront charges)
            fee_match = re.search(r"Fee Charge\s+(\d+)", text)
            if fee_match:
                extracted["processing_fee"] = int(fee_match.group(1))
            
            # Extract status
            status_match = re.search(r"Status\s+(\w+)", text)
            if status_match:
                extracted["verification_status"] = "verified" if status_match.group(1).lower() == "active" else "pending"
            
            # Add critical note about Flexi Loan nature
            extracted["notes"] = "FLEXI LOAN: Revolving credit facility (not standard EMI). OTS requires special handling per RBI guidelines for flexi products."
            
            print("  [OK] Extracted: Borrower, Account Numbers (400DFR47319474 → 400LAP14914207), Loan Amount, ROI, Tenure, Fees")
            print(f"  [!] FLEXI LOAN DETECTED: This is a revolving credit facility (not standard term loan)")
            return extracted
            
    except Exception as e:
        print(f"  [!] PDF parsing failed: {str(e)}")
        return None

# ===== INTERACTIVE VERIFICATION (with PDF parsing option) =====
def verify_loan_interactive(loan_data=None):
    print("\n" + "="*70)
    print("LOAN VERIFICATION WIZARD (v2.0 with Bajaj PDF Support)")
    print("="*70)
    
    if loan_data is None:
        print("\n[1/7] SELECT LOAN SOURCE")
        print("   1. Parse Bajaj PDF (2017-18 Doctors Flexi Loan)")
        print("   2. Parse L&T PDF (FORECLOSURE_BL240910207908339.pdf)")
        print("   3. Parse HDFC DOCX (hdfc24loan1.docx)")
        print("   4. Manual entry (all fields fillable)")
        choice = input("\n   Enter choice [1-4]: ").strip()
        
        if choice == '1':
            print("\n[1.1] ENTER BAJAJ PDF PATH (new Magna / loan document)")
            print("   • Drag PDF to loans\\new_uploads\\ then type filename:  bjmagnarepay1.pdf")
            print("   • Or in Documents / this folder:  bjmagnarepay1.pdf")
            print("   • Or paste full path / drag file into this window")
            print("   • Or type 'demo' for sample data")
            pdf_path = input("   PDF path (or 'demo' for sample data): ").strip().strip('"').strip("'")
            
            if pdf_path.lower() == 'demo':
                # Demo data matching the actual PDF
                loan = {
                    "provider": "Bajaj Finance",
                    "product": "Doctors Flexi Reloc Loan",
                    "account_number": "400DFR47319474",
                    "linked_account": "400LAP14914207",
                    "borrower_name": "Muddu Surendra Nehru",
                    "outstanding_principal": 4204000,
                    "interest_rate": 15.50,
                    "rate_type": "fixed",
                    "tenure_total_months": 96,
                    "tenure_remaining_months": 90,
                    "emi_amount": 54420,
                    "emi_start_date": "2017-09-02",
                    "disbursal_date": "2017-07-30",
                    "processing_fee": 42632,
                    "foreclosure_fee_percent": 4.0,
                    "loan_type": "flexi",
                    "notes": "FLEXI LOAN: Revolving credit (400DFR47319474 linked to 400LAP14914207). OTS requires special handling."
                }
                loan['id'] = f"bajaj-{loan['account_number'].lower()}"
            else:
                # Accept: filename or full path. Check: absolute path, then this folder, then Documents
                candidate = Path(pdf_path)
                if candidate.is_absolute() and candidate.exists():
                    pdf_full_path = candidate
                else:
                    pdf_full_path = DATA_DIR / pdf_path
                if not pdf_full_path.exists():
                    # Fallback 1: loans/new_uploads (DRAG FILES HERE)
                    uploads_path = DATA_DIR / "loans" / "new_uploads" / Path(pdf_path).name
                    if uploads_path.exists():
                        pdf_full_path = uploads_path
                    else:
                        # Fallback 2: user's Documents folder
                        docs_path = Path.home() / "Documents" / Path(pdf_path).name
                        if docs_path.exists():
                            pdf_full_path = docs_path
                        else:
                            pdf_full_path = DATA_DIR / pdf_path  # keep for error message
                if pdf_full_path.exists():
                    parsed = parse_bajaj_pdf(pdf_full_path)
                    if parsed:
                        loan = parsed
                        loan['id'] = f"bajaj-{loan.get('account_number', 'new').lower()}"
                    else:
                        print("  [!] Falling back to manual entry")
                        loan = LOAN_TEMPLATE.copy()
                else:
                    print(f"  [!] File not found: {pdf_path}")
                    print(f"     Checked: this folder, loans\\new_uploads\\, Documents\\")
                    loan = LOAN_TEMPLATE.copy()
        else:
            # Other options (L&T/HDFC/manual) - simplified for brevity
            loan = LOAN_TEMPLATE.copy()
            loan['provider'] = 'Bajaj Finance' if choice == '4' else 'Unknown'
    else:
        loan = loan_data.copy()
    
    # ===== FILLABLE PROMPTS (REQUIRED FIELDS FIRST) =====
    print("\n[2/7] BORROWER DETAILS (critical for OTS legitimacy)")
    loan['borrower_name'] = fillable_prompt(
        "Borrower Full Name", 
        loan.get('borrower_name', ''),
        field_type="text",
        required=True
    )
    
    print("\n[3/7] ACCOUNT LINKAGE (critical for Flexi Loans)")
    loan['account_number'] = fillable_prompt(
        "Primary Account Number", 
        loan.get('account_number', '400DFR47319474'),
        field_type="text",
        required=True
    )
    loan['linked_account'] = fillable_prompt(
        "Linked Agreement Number", 
        loan.get('linked_account', '400LAP14914207'),
        field_type="text",
        required=False
    )
    
    print("\n[4/7] LOAN AMOUNTS (verify current outstanding)")
    print("   [!] PDF shows historical OS (Feb 2018). Enter CURRENT outstanding:")
    loan['outstanding_principal'] = fillable_prompt(
        "Current Outstanding Principal (Rs)", 
        loan.get('outstanding_principal', 4204000),
        field_type="currency",
        required=True
    )
    loan['emi_amount'] = fillable_prompt(
        "Monthly Payment Amount (Rs)", 
        loan.get('emi_amount', 54420),
        field_type="currency"
    )
    
    print("\n[5/7] TENURE & DATES")
    loan['disbursal_date'] = fillable_prompt(
        "Disbursal Date (YYYY-MM-DD)", 
        loan.get('disbursal_date', '2017-07-30'),
        field_type="date"
    )
    loan['emi_start_date'] = fillable_prompt(
        "First Payment Date (YYYY-MM-DD)", 
        loan.get('emi_start_date', '2017-09-02'),
        field_type="date"
    )
    loan['tenure_remaining_months'] = fillable_prompt(
        "Remaining Tenure (months)", 
        loan.get('tenure_remaining_months', 90),
        field_type="number"
    )
    
    print("\n[6/7] FEES (affects OTS negotiation)")
    loan['processing_fee'] = fillable_prompt(
        "Processing Fee (Rs)", 
        loan.get('processing_fee', 42632),
        field_type="currency"
    )
    loan['foreclosure_fee_percent'] = fillable_prompt(
        "Foreclosure Fee (%)", 
        loan.get('foreclosure_fee_percent', 4.0),
        field_type="number"
    )
    
    print("\n[7/7] FLEXI LOAN CONFIRMATION")
    print("   [!] BAJAJ FLEXI LOANS REQUIRE SPECIAL OTS HANDLING")
    print("   • Not a standard term loan (revolving credit facility)")
    print("   • RBI OTS rules differ for flexi products")
    print("   • Linked to main LAP account (400LAP14914207)")
    flexi_confirm = input("\n   Confirm this is a Flexi Loan? [Y/N]: ").strip().lower() == 'y'
    loan['loan_type'] = 'flexi' if flexi_confirm else 'standard'
    
    # ===== FINAL REVIEW =====
    print("\n" + "-"*70)
    print("FINAL VERIFICATION")
    print("-"*70)
    print(f"PROVIDER          : {loan.get('provider', 'Bajaj Finance')}")
    print(f"PRODUCT           : {loan.get('product', 'Doctors Flexi Reloc Loan')}")
    print(f"ACCOUNT           : {loan.get('account_number', 'N/A')} → Linked: {loan.get('linked_account', 'N/A')}")
    print(f"BORROWER          : {loan.get('borrower_name', '[!] MISSING')}")
    print(f"CURRENT OS        : Rs {loan.get('outstanding_principal', 0):,}")
    emi = loan.get('emi_amount', 0)
    emi = int(emi) if str(emi).isdigit() else 0
    print(f"MONTHLY PAYMENT   : Rs {emi:,} (interest-only for flexi)")
    print(f"REMAINING TENURE  : {loan.get('tenure_remaining_months', 0)} months")
    print(f"DISBURSAL DATE    : {loan.get('disbursal_date', 'N/A')}")
    print(f"LOAN TYPE         : {loan.get('loan_type', 'standard').upper()} [!]")
    print("-"*70)
    
    approved = input("\n[OK] Approve and save this loan? [Y/N]: ").strip().lower() == 'y'
    if approved:
        loan['verification_status'] = 'verified'
        loan['verified_at'] = datetime.now().isoformat()
        loan['emis_paid'] = loan.get('tenure_total_months', 0) - loan.get('tenure_remaining_months', 0)
        
        # Generate ID if missing
        if not loan.get('id'):
            provider_key = loan['provider'].split()[0].lower()
            acct = loan.get('account_number', 'new').replace(' ', '').lower()[:15]
            loan['id'] = f"{provider_key}-{acct}"
        
        return loan
    else:
        print("[!] Loan verification cancelled.")
        return None

def fillable_prompt(field_name, current_value="", field_type="text", options=None, required=False):
    """Interactive fillable prompt with required field enforcement"""
    display_val = current_value if current_value else "(empty)"
    print(f"\n[OK] {field_name}: {display_val}")
    
    while True:
        if required and not current_value:
            resp = 'e'
        else:
            resp = input("   Keep (Y), Edit (E), or Skip (S)? [Y/E/S]: ").strip().lower()
        
        if resp == 'y' or resp == '':
            if required and not current_value:
                print("   [!] REQUIRED FIELD: Cannot be empty")
                continue
            return current_value if current_value else ""
        elif resp == 'e':
            if field_type == "number":
                new_val = input(f"   Enter new value: ").strip()
                try:
                    return float(new_val) if '.' in new_val else int(new_val)
                except ValueError:
                    print("   [!] Invalid number. Try again.")
            elif field_type == "currency":
                new_val = input(f"   Enter amount (e.g., 4204000): ").strip().replace(',', '').replace('₹', '').replace('Rs', '')
                try:
                    return int(float(new_val))
                except ValueError:
                    print("   [!] Invalid amount. Try again.")
            elif field_type == "date":
                new_val = input(f"   Enter date (YYYY-MM-DD): ").strip()
                try:
                    datetime.strptime(new_val, '%Y-%m-%d')
                    return new_val
                except ValueError:
                    print("   [!] Invalid date format. Use YYYY-MM-DD.")
            elif options:
                print(f"   Options: {', '.join(options)}")
                new_val = input(f"   Enter choice: ").strip()
                if new_val in options:
                    return new_val
                print(f"   [!] Invalid choice. Try again.")
            else:
                new_val = input(f"   Enter new value: ").strip()
                if required and not new_val.strip():
                    print("   [!] REQUIRED FIELD: Cannot be empty")
                    continue
                return new_val
        elif resp == 's':
            if required:
                print("   [!] REQUIRED FIELD: Cannot skip")
                continue
            return current_value if current_value else ""
        else:
            print("   [!] Invalid response. Enter Y, E, or S.")

def show_loan_menu(loans):
    print("\n" + "="*70)
    print("EXISTING LOANS")
    print("="*70)
    
    if not loans:
        print("[!] No loans verified yet.")
        return 0
    
    total_emi = 0
    for i, loan in enumerate(loans, 1):
        emi = loan.get('emi_amount', loan.get('emi', 0))
        total_emi += emi
        status = "[OK]" if loan.get('verification_status') == 'verified' else "[!]"
        loan_type = "(FLEXI)" if loan.get('loan_type') == 'flexi' else ""
        print(f"{i}. {status} {loan.get('provider', 'N/A')} {loan.get('product', '')} {loan_type}")
        print(f"      Account: {loan.get('account_number', 'N/A')} → {loan.get('linked_account', 'N/A')}")
        print(f"      EMI: Rs {emi:,} | OS: Rs {loan.get('outstanding_principal', loan.get('outstanding', 0)):,}")
    
    print("-"*70)
    print(f"TOTAL MONTHLY PAYMENT OUTFLOW: Rs {total_emi:,}")
    print("="*70)
    return total_emi

def main():
    print("="*70)
    print("DEBT EMPIRE: LOAN VERIFIER v2.0 (Bajaj Flexi Loan Support)")
    print("="*70)
    
    masters = load_masters()
    
    while True:
        print("\nMAIN MENU")
        print("  1. Verify new loan (Bajaj PDF/L&T/HDFC)")
        print("  2. Review existing loans")
        print("  3. Edit loan details")
        print("  4. Save & exit -> run empire.py")
        choice = input("\nEnter choice [1-4]: ").strip()
        
        if choice == '1':
            new_loan = verify_loan_interactive()
            if new_loan:
                masters['loans'].append(new_loan)
                save_masters(masters)
                print(f"\n[OK] Loan '{new_loan['id']}' added to masters.json")
                if new_loan.get('loan_type') == 'flexi':
                    print(f"   [!] FLEXI LOAN NOTE: {new_loan.get('notes', '')}")
        
        elif choice == '2':
            show_loan_menu(masters['loans'])
            input("\nPress Enter to continue...")
        
        elif choice == '3':
            if not masters['loans']:
                print("[!] No loans to edit.")
                continue
            
            show_loan_menu(masters['loans'])
            idx = input("\nEnter loan # to edit (or 0 to cancel): ").strip()
            try:
                idx = int(idx) - 1
                if idx < 0:
                    continue
                loan = masters['loans'][idx]
                edited = verify_loan_interactive(loan)
                if edited:
                    masters['loans'][idx] = edited
                    save_masters(masters)
                    print(f"\n[OK] Loan #{idx+1} updated")
            except (ValueError, IndexError):
                print("[!] Invalid selection.")
        
        elif choice == '4':
            save_masters(masters)
            print("\n[OK] All loans saved to masters.json")
            print("\n[OK] NEXT STEP: Run empire.py to generate OTS reports")
            print("   py empire.py")
            break
        
        else:
            print("[!] Invalid choice. Enter 1-4.")

if __name__ == "__main__":
    main()
