#!/usr/bin/env python3
"""
Generate verifier.html from masters.json
Beautiful HTML table with print, edit, and action buttons
"""
import json
import sys
from pathlib import Path
from datetime import datetime

# Set UTF-8 encoding for Windows console
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

DATA_DIR = Path.cwd()
MASTERS_PATH = DATA_DIR / "masters.json"
VERIFIER_HTML = DATA_DIR / "verifier.html"

def load_masters():
    """Load masters.json"""
    if not MASTERS_PATH.exists():
        return {'loans': []}
    with open(MASTERS_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

def generate_shortcode(loan):
    """Generate shortcode from loan data (for table)"""
    provider = loan.get('provider', '').lower()
    account = loan.get('account_number', loan.get('account_ref', ''))
    if account:
        short = ''.join([c for c in account if c.isalnum()])[-6:].lower()
        return f"{provider[:3]}{short}"
    return f"{provider[:3]}{loan.get('id', '')[-4:]}"

def display_shortcode(loan):
    """Display shortcode: baj8L, lt26L (provider prefix + OS in Lakhs)"""
    os_amt = loan.get('outstanding_principal', loan.get('outstanding', 0))
    os_lakhs = round(os_amt / 100000) if os_amt >= 100000 else round(os_amt / 100000, 1)
    if os_lakhs == 0:
        os_lakhs = 0.1
    p = (loan.get('provider') or '').replace('&', '').replace(' ', '').lower()
    prefix = p[:3] if len(p) >= 3 else p or 'xxx'
    return f"{prefix}{os_lakhs}L"

def ots_amount(loan):
    """OTS amount to pay - uses stored value or computes from ots_percent (default 70%)."""
    os_amt = loan.get('outstanding_principal', loan.get('outstanding', 0))
    if loan.get('ots_amount_70pct') is not None:
        return loan['ots_amount_70pct']
    pct = loan.get('ots_percent', 70)
    return round(os_amt * (pct / 100))

def split_running_closed(loans):
    """Split into running (OS > 0) and closed (OS == 0 or status CLOSED)."""
    running = []
    closed = []
    for loan in loans:
        os_amt = loan.get('outstanding_principal', loan.get('outstanding', 0))
        status = (loan.get('status') or loan.get('verification_status') or '').upper()
        if os_amt <= 0 or status == 'CLOSED':
            closed.append(loan)
        else:
            running.append(loan)
    return running, closed

def get_loan_folder(loan):
    """Path to loans/Provider/Account for this loan."""
    provider = loan.get('provider', '')
    account = (loan.get('account_number') or loan.get('account_ref') or '').strip() or 'unknown'
    account = account.replace(' ', '')[:30]
    folder_name = normalize_provider_folder(provider)
    return DATA_DIR / "loans" / folder_name / account

def list_loan_branch_files(loan):
    """List files in loan folder (meta.json, docs/*, uploaded PDFs). Returns list of display strings."""
    folder = get_loan_folder(loan)
    out = []
    if not folder.exists():
        return ["meta.json", "docs/", "Add New → Upload (e.g. smart_stmt_new.pdf)"]
    
    # List root files (meta.json, PDFs, etc.)
    root_files = []
    for p in sorted(folder.iterdir()):
        if p.name.startswith('.'):
            continue
        if p.is_file():
            root_files.append(p.name)
    
    # Add meta.json first if exists, then other files
    if 'meta.json' in root_files:
        out.append('meta.json')
        root_files.remove('meta.json')
    out.extend(sorted(root_files)[:5])  # Limit to 5 root files
    
    # List docs/ subfolder
    docs_dir = folder / 'docs'
    if docs_dir.exists() and docs_dir.is_dir():
        try:
            doc_files = sorted([f.name for f in docs_dir.iterdir() if f.is_file() and not f.name.startswith('.')])[:10]
            if doc_files:
                out.append("docs/")
                for doc in doc_files:
                    out.append(f"  └── {doc}")
            else:
                out.append("docs/ (empty)")
        except OSError:
            out.append("docs/")
    
    if not out:
        out = ["meta.json", "docs/", "Add New → Upload (e.g. smart_stmt_new.pdf)"]
    elif "Add New → Upload" not in str(out):
        out.append("Add New → Upload (e.g. smart_stmt_new.pdf)")
    
    return out if out else ["meta.json", "Add New → Upload"]

def normalize_provider_folder(name):
    """Same as build_structure: safe folder name."""
    if not name:
        return "Unknown"
    return name.replace("&", "and").replace("/", "-").replace(" ", "_").strip()

def build_tree_lines(loans):
    """Build folder tree lines: loans/Provider/Account/ (grouped by provider)."""
    if not loans:
        return ["loans/", "  (no loans — run py loan_verifier.py)"]
    seen = set()
    lines = ["loans/"]
    # Group by provider (folder name)
    by_provider = {}
    for loan in loans:
        provider = loan.get('provider', 'N/A')
        folder = normalize_provider_folder(provider)
        account = (loan.get('account_number') or loan.get('account_ref') or '').strip() or 'unknown'
        account = account.replace(' ', '')[:20]
        if folder not in by_provider:
            by_provider[folder] = []
        by_provider[folder].append(account)
    for i, (folder, accounts) in enumerate(sorted(by_provider.items())):
        is_last_provider = (i == len(by_provider) - 1)
        branch = "└── " if is_last_provider else "├── "
        lines.append(branch + folder + "/")
        for j, acc in enumerate(accounts):
            is_last_acc = (j == len(accounts) - 1)
            sub = "    " if is_last_provider else "│   "
            sub += "└── " if is_last_acc else "├── "
            lines.append(sub + acc + "/")
    lines.append("archive/")
    lines.append("  └── " + str(datetime.now().year) + "/")
    return lines

def generate_html(masters_data):
    """Generate beautiful HTML verifier page"""
    loans = masters_data.get('loans', [])
    running_loans, closed_loans = split_running_closed(loans)
    
    # Tree: loans/Provider/Account/ + archive/YYYY/
    tree_lines = build_tree_lines(loans)
    tree_html = '\n'.join(tree_lines).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    
    # OTS TARGETS: running only
    total_running = sum(l.get('outstanding_principal', l.get('outstanding', 0)) for l in running_loans)
    ots_80_lakhs = (total_running * 0.80) / 100000 if running_loans else 0
    start_lakhs = max(5, round(ots_80_lakhs / 3)) if running_loans else 0
    
    # Calculate totals
    total_exposure = sum(l.get('outstanding_principal', l.get('outstanding', 0)) for l in loans)
    total_ots = sum(ots_amount(l) for l in loans)
    total_savings = total_exposure - total_ots
    total_emi = sum(l.get('emi_amount', l.get('emi', 0)) for l in loans)
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Debt Empire - MASTER DASHBOARD</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            min-height: 100vh;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }}
        
        .header {{
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }}
        
        .header h1 {{
            font-size: 32px;
            margin-bottom: 10px;
            font-weight: 600;
        }}
        
        .header .subtitle {{
            font-size: 14px;
            opacity: 0.9;
        }}
        
        .stats-bar {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            padding: 25px;
            background: #f8f9fa;
            border-bottom: 2px solid #e0e0e0;
        }}
        
        .stat-card {{
            background: white;
            padding: 15px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            text-align: center;
        }}
        
        .stat-card .label {{
            font-size: 12px;
            color: #666;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 5px;
        }}
        
        .stat-card .value {{
            font-size: 24px;
            font-weight: bold;
            color: #1e3c72;
        }}
        
        .actions-bar {{
            padding: 20px 25px;
            background: #fff;
            border-bottom: 2px solid #e0e0e0;
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
            justify-content: center;
        }}
        
        .btn {{
            padding: 12px 24px;
            border: none;
            border-radius: 8px;
            font-size: 14px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s;
            text-decoration: none;
            display: inline-block;
        }}
        
        .btn-primary {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }}
        
        .btn-primary:hover {{
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }}
        
        .btn-success {{
            background: #28a745;
            color: white;
        }}
        
        .btn-success:hover {{
            background: #218838;
            transform: translateY(-2px);
        }}
        
        .btn-info {{
            background: #17a2b8;
            color: white;
        }}
        
        .btn-info:hover {{
            background: #138496;
            transform: translateY(-2px);
        }}
        
        .btn-print {{
            background: #6c757d;
            color: white;
        }}
        
        .btn-print:hover {{
            background: #5a6268;
        }}
        
        .table-container {{
            padding: 25px;
            overflow-x: auto;
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            background: white;
        }}
        
        thead {{
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            color: white;
        }}
        
        th {{
            padding: 15px;
            text-align: left;
            font-weight: 600;
            font-size: 14px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        
        td {{
            padding: 15px;
            border-bottom: 1px solid #e0e0e0;
        }}
        
        tbody tr:hover {{
            background: #f8f9fa;
        }}
        
        .shortcode {{
            font-family: 'Courier New', monospace;
            background: #e3f2fd;
            padding: 5px 10px;
            border-radius: 5px;
            font-weight: bold;
            color: #1976d2;
        }}
        
        .lender {{
            font-weight: 600;
            color: #333;
        }}
        
        .amount {{
            font-weight: 600;
            color: #1e3c72;
        }}
        
        .btn-small {{
            padding: 6px 12px;
            font-size: 12px;
            margin: 2px;
        }}
        
        .empty-state {{
            text-align: center;
            padding: 60px 20px;
            color: #666;
        }}
        
        .empty-state h2 {{
            font-size: 24px;
            margin-bottom: 10px;
            color: #333;
        }}
        
        .tree-section {{
            padding: 20px 25px;
            background: #f0f4f8;
            border-bottom: 2px solid #e0e0e0;
        }}
        
        .tree-section h2 {{
            font-size: 16px;
            color: #1e3c72;
            margin-bottom: 12px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        
        .tree-block {{
            font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
            font-size: 13px;
            line-height: 1.6;
            background: #fff;
            padding: 15px 20px;
            border-radius: 8px;
            border: 1px solid #d0d7de;
            overflow-x: auto;
            white-space: pre;
            color: #24292f;
        }}
        
        .print-only-title {{
            display: none;
        }}
        
        .ots-targets, .closed-section, .tree-branches {{
            padding: 18px 25px;
            background: #fff;
            border-bottom: 1px solid #e0e0e0;
        }}
        
        .ots-targets {{
            background: #f0fdf4;
            border-left: 4px solid #22c55e;
        }}
        
        .closed-section {{
            background: #fef2f2;
            border-left: 4px solid #ef4444;
        }}
        
        .tree-branches {{
            background: #f8fafc;
            border-left: 4px solid #3b82f6;
        }}
        
        .ots-targets h2, .closed-section h2, .tree-branches h2 {{
            font-size: 15px;
            margin-bottom: 12px;
            color: #1e3c72;
        }}
        
        .ots-row, .closed-row {{
            padding: 8px 0;
            display: flex;
            flex-wrap: wrap;
            align-items: center;
            gap: 8px;
        }}
        
        .ots-row .shortcode {{
            font-family: 'Courier New', monospace;
            font-weight: bold;
            color: #166534;
        }}
        
        .branch-block {{
            font-family: 'Consolas', monospace;
            font-size: 12px;
            background: #fff;
            padding: 12px 16px;
            border-radius: 6px;
            border: 1px solid #e2e8f0;
            margin-bottom: 12px;
            white-space: pre-wrap;
        }}
        
        .branch-block .branch-name {{
            font-weight: bold;
            color: #1e40af;
            margin-bottom: 6px;
        }}
        
        @media print {{
            body {{
                background: white;
                padding: 10mm;
                font-size: 11pt;
            }}
            
            .container {{
                box-shadow: none;
                border-radius: 0;
                max-width: 100%;
            }}
            
            .actions-bar, .btn {{
                display: none !important;
            }}
            
            .print-only-title {{
                display: block !important;
                text-align: center;
                font-size: 20pt;
                font-weight: bold;
                padding: 10mm 0 5mm;
                color: #000;
                border-bottom: 2px solid #000;
                margin-bottom: 5mm;
            }}
            
            .header {{
                display: none;
            }}
            
            .stats-bar {{
                page-break-inside: avoid;
                margin-bottom: 5mm;
            }}
            
            .ots-targets, .closed-section {{
                page-break-inside: avoid;
                border-left: none;
                border: 1px solid #ccc;
                padding: 3mm;
                margin-bottom: 3mm;
            }}
            
            .ots-targets h2, .closed-section h2 {{
                font-size: 12pt;
                margin-bottom: 2mm;
            }}
            
            .tree-branches {{
                page-break-inside: avoid;
                border: 1px solid #ccc;
                padding: 3mm;
            }}
            
            .tree-section {{
                background: #fff;
                border: 1px solid #ccc;
                padding: 3mm;
                page-break-inside: avoid;
            }}
            
            .tree-block, .branch-block {{
                background: #fff;
                border: none;
                font-size: 9pt;
                padding: 2mm;
            }}
            
            table {{
                page-break-inside: auto;
                font-size: 9pt;
            }}
            
            tr {{
                page-break-inside: avoid;
                page-break-after: auto;
            }}
            
            thead {{
                background: #1e3c72 !important;
                color: white !important;
                -webkit-print-color-adjust: exact;
                print-color-adjust: exact;
            }}
            
            .subtitle {{
                display: none;
            }}
        }}
        
        @media (max-width: 768px) {{
            .header h1 {{
                font-size: 24px;
            }}
            
            .stats-bar {{
                grid-template-columns: 1fr;
            }}
            
            .tree-section, .ots-targets, .closed-section, .tree-branches {{
                padding: 15px;
            }}
            
            .tree-block, .branch-block {{
                font-size: 11px;
                padding: 12px;
                overflow-x: auto;
                -webkit-overflow-scrolling: touch;
            }}
            
            .ots-row, .closed-row {{
                font-size: 13px;
                flex-direction: column;
                align-items: flex-start;
                gap: 4px;
            }}
            
            table {{
                font-size: 12px;
            }}
            
            th, td {{
                padding: 10px 8px;
            }}
            
            .btn {{
                padding: 10px 16px;
                font-size: 12px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>💰 Debt Empire - MASTER DASHBOARD</h1>
            <div class="subtitle">Generated: {datetime.now().strftime('%d %B %Y %I:%M %p')}</div>
        </div>
        
        <div class="print-only-title">OTS Portfolio Dr. Nehru</div>
        
        <div class="stats-bar">
            <div class="stat-card">
                <div class="label">Total Exposure</div>
                <div class="value">Rs {total_exposure/100000:.2f}L</div>
            </div>
            <div class="stat-card">
                <div class="label">OTS Liability</div>
                <div class="value">Rs {total_ots/100000:.2f}L</div>
            </div>
            <div class="stat-card">
                <div class="label">Total Savings</div>
                <div class="value">Rs {total_savings/100000:.2f}L</div>
            </div>
            <div class="stat-card">
                <div class="label">Monthly EMI</div>
                <div class="value">Rs {total_emi:,}</div>
            </div>
        </div>
        
        <div class="ots-targets">
            <h2>🟢 OTS TARGETS (RUNNING loans only)</h2>
"""
    
    # Build OTS TARGETS rows
    if running_loans:
        for loan in running_loans:
            shortcode = display_shortcode(loan)
            os_amt = loan.get('outstanding_principal', loan.get('outstanding', 0))
            os_lakhs = os_amt / 100000
            pct = (os_amt / total_running * 100) if total_running > 0 else 0
            lender = loan.get('provider', 'N/A')
            ots_file = lender.lower().replace('&', '').replace('+', '') + '-ots.html'
            account_ref = loan.get('account_number', loan.get('account_ref', ''))
            
            # Deep edit: link to loan_verifier.py with loan context
            html += f"""
            <div class="ots-row">
                <span class="shortcode">{shortcode}</span>
                <span>(₹{os_lakhs:.1f}L, {pct:.1f}%)</span>
                <span>→</span>
                <a href="javascript:void(0)" onclick="showDeepEdit('{shortcode}', '{lender}', '{account_ref}')" style="color:#166534; text-decoration:underline; font-weight:600;">Edit</a>
                <span>|</span>
                <a href="ots-pdfs/{ots_file}" target="_blank" style="color:#166534; text-decoration:underline;">OTS Letter</a>
                <span>|</span>
                <a href="javascript:void(0)" onclick="alert('OS Today: ₹{os_amt:,}\\nAccount: {account_ref}\\nProvider: {lender}')" style="color:#166534; text-decoration:underline;">OS Today?</a>
            </div>
"""
        
        html += f"""
            <div class="ots-row" style="margin-top:10px; padding-top:10px; border-top:1px solid #d1fae5; font-weight:bold;">
                <span>Total: ₹{total_running/100000:.1f}L</span>
                <span>→</span>
                <span>80% OTS ₹{ots_80_lakhs:.1f}L</span>
                <span>(Start ₹{start_lakhs:.0f}L)</span>
                <span style="color:#666; font-size:12px; margin-left:10px;">(CLOSED loans excluded)</span>
            </div>
"""
    else:
        html += """
            <div class="ots-row">No running loans — all closed or zero OS</div>
"""
    
    html += """
        </div>
        
        <div class="closed-section">
            <h2>🔴 CLOSED (Merit proof)</h2>
"""
    
    # Build CLOSED rows
    if closed_loans:
        for loan in closed_loans:
            shortcode = display_shortcode(loan)
            html += f"""
            <div class="closed-row">
                <span class="shortcode">{shortcode}</span>
                <span>✓ Paid</span>
            </div>
"""
    else:
        html += """
            <div class="closed-row">None</div>
"""
    
    html += """
        </div>
        
        <div class="tree-branches">
            <h2>📁 TREE VIEW (branches)</h2>
"""
    
    # Build TREE VIEW branches (per loan)
    if running_loans:
        for loan in running_loans:
            shortcode = display_shortcode(loan)
            files = list_loan_branch_files(loan)
            files_escaped = [f.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;') for f in files]
            # Format as tree (already has tree chars from list_loan_branch_files for docs/)
            files_str = '\n'.join(files_escaped)
            
            html += f"""
            <div class="branch-block">
                <div class="branch-name">{shortcode}/</div>{files_str}
            </div>
"""
    else:
        html += """
            <div class="branch-block">No running loans — add loans to see branches</div>
"""
    
    html += """
        </div>
        
        <div class="actions-bar">
            <button class="btn btn-print" onclick="window.print()">🖨️ PRINT: Ctrl+P → "OTS Portfolio Dr. Nehru"</button>
            <a href="javascript:void(0)" class="btn btn-success" onclick="showEmailInstructions()">📧 EMAIL: Batch OTS (5L start each)</a>
            <a href="javascript:void(0)" class="btn btn-success" onclick="showEditInstructions()">✏️ EDIT: Status/OS/Notes → Save masters.json</a>
            <a href="javascript:void(0)" class="btn btn-primary" onclick="showAddLoanInstructions()">➕ ADD LOAN: New branch + shortcode</a>
            <a href="javascript:void(0)" class="btn btn-info" onclick="showRunEmpireInstructions()">🚀 Run Empire</a>
            <a href="dashboard.html" class="btn btn-primary" target="_blank">📊 Dashboard</a>
        </div>
        
        <div class="tree-section">
            <h2>📁 Folder tree (loans / archive)</h2>
            <pre class="tree-block">{tree_html}</pre>
        </div>
        
        <div id="instructions-modal" style="display:none; position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.7); z-index:1000; align-items:center; justify-content:center;">
            <div style="background:white; padding:30px; border-radius:10px; max-width:500px; box-shadow:0 10px 40px rgba(0,0,0,0.3);">
                <h2 style="margin-bottom:15px; color:#1e3c72;">How to Edit Loans</h2>
                <div style="margin-bottom:20px; line-height:1.8;">
                    <p><strong>Step 1:</strong> Open PowerShell</p>
                    <p><strong>Step 2:</strong> Navigate to folder:</p>
                    <code style="background:#f5f5f5; padding:8px 12px; display:block; border-radius:5px; margin:10px 0;">cd C:\\Users\\MYPC\\Desktop\\debt-arbitrage\\debt-empire</code>
                    <p><strong>Step 3:</strong> Run verifier:</p>
                    <code style="background:#f5f5f5; padding:8px 12px; display:block; border-radius:5px; margin:10px 0;">py loan_verifier.py</code>
                    <p style="margin-top:15px;"><strong>Or double-click:</strong> <code>RUN_VERIFIER.ps1</code></p>
                </div>
                <button onclick="closeInstructions()" class="btn btn-primary" style="width:100%;">Got it!</button>
            </div>
        </div>
        
        <div class="table-container">
"""
    
    if not loans:
        html += """
            <div class="empty-state">
                <h2>No Loans Found</h2>
                <p>Run <code>py loan_verifier.py</code> to add your first loan</p>
            </div>
"""
    else:
        html += """
            <table>
                <thead>
                    <tr>
                        <th>Shortcode</th>
                        <th>Lender</th>
                        <th>Outstanding</th>
                        <th>EMI</th>
                        <th>Tenure</th>
                        <th>Fees</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
"""
        
        for loan in loans:
            shortcode = generate_shortcode(loan)
            lender = loan.get('provider', 'N/A')
            os_amt = loan.get('outstanding_principal', loan.get('outstanding', 0))
            emi = loan.get('emi_amount', loan.get('emi', 0))
            tenure = loan.get('tenure_remaining_months', loan.get('tenure_months', 0))
            fees = loan.get('processing_fee', 0)
            borrower = loan.get('borrower_name', '')
            account_ref = loan.get('account_number', loan.get('account_ref', ''))
            
            html += f"""
                    <tr>
                        <td><span class="shortcode">{shortcode}</span></td>
                        <td><span class="lender">{lender}</span></td>
                        <td><span class="amount">Rs {os_amt/100000:.2f}L</span></td>
                        <td>Rs {emi:,}</td>
                        <td>{tenure} months</td>
                        <td>Rs {fees:,}</td>
                        <td>
                            <button class="btn btn-small btn-info" onclick="alert('Loan: {shortcode}\\nBorrower: {borrower}\\nAccount: {account_ref}')">ℹ️ Info</button>
                            <button class="btn btn-small btn-success" onclick="window.open('ots-pdfs/{lender.lower().replace('&', '').replace('+', '')}-ots.html', '_blank')">📧 Email OTS</button>
                        </td>
                    </tr>
"""
        
        html += """
                </tbody>
            </table>
"""
    
    html += """
        </div>
    </div>
    
    <script>
        // Print keyboard shortcut
        document.addEventListener('keydown', function(e) {
            if ((e.ctrlKey || e.metaKey) && e.key === 'p') {
                e.preventDefault();
                window.print();
            }
        });
        
        // Show edit instructions (general)
        function showEditInstructions() {
            document.getElementById('instructions-modal').style.display = 'flex';
            document.getElementById('instructions-modal').querySelector('h2').textContent = 'How to Edit Loans';
            document.getElementById('instructions-modal').querySelector('div').innerHTML = `
                <p><strong>Step 1:</strong> Open PowerShell</p>
                <p><strong>Step 2:</strong> Navigate to folder:</p>
                <code style="background:#f5f5f5; padding:8px 12px; display:block; border-radius:5px; margin:10px 0; font-size:12px;">cd C:\\Users\\MYPC\\Desktop\\debt-arbitrage\\debt-empire</code>
                <p><strong>Step 3:</strong> Run verifier:</p>
                <code style="background:#f5f5f5; padding:8px 12px; display:block; border-radius:5px; margin:10px 0; font-size:12px;">py loan_verifier.py</code>
                <p style="margin-top:15px;"><strong>Or double-click:</strong> <code>RUN_VERIFIER.ps1</code></p>
                <p style="margin-top:15px; color:#666; font-size:13px;">In the menu, choose:<br>• Option 2: Review existing loans<br>• Option 3: Edit loan details<br>• Set status=CLOSED to exclude from OTS totals</p>
            `;
        }
        
        // Deep edit: loan-specific instructions
        function showDeepEdit(shortcode, lender, account) {
            document.getElementById('instructions-modal').style.display = 'flex';
            document.getElementById('instructions-modal').querySelector('h2').textContent = '✏️ Deep Edit: ' + shortcode;
            document.getElementById('instructions-modal').querySelector('div').innerHTML = `
                <p><strong>Loan:</strong> <code>${shortcode}</code> (${lender})</p>
                <p><strong>Account:</strong> <code>${account}</code></p>
                <hr style="margin:15px 0; border:1px solid #e0e0e0;">
                <p><strong>Step 1:</strong> Open PowerShell</p>
                <p><strong>Step 2:</strong> Navigate to folder:</p>
                <code style="background:#f5f5f5; padding:8px 12px; display:block; border-radius:5px; margin:10px 0; font-size:12px;">cd C:\\Users\\MYPC\\Desktop\\debt-arbitrage\\debt-empire</code>
                <p><strong>Step 3:</strong> Run verifier:</p>
                <code style="background:#f5f5f5; padding:8px 12px; display:block; border-radius:5px; margin:10px 0; font-size:12px;">py loan_verifier.py</code>
                <p style="margin-top:15px;"><strong>In menu:</strong></p>
                <ul style="margin:10px 0; padding-left:20px; line-height:1.8;">
                    <li>Option 2: Review existing loans</li>
                    <li>Find: <code>${shortcode}</code> or Account: <code>${account}</code></li>
                    <li>Option 3: Edit loan details</li>
                    <li>Update: Status, OS, Notes → Save to masters.json</li>
                </ul>
                <p style="margin-top:15px; color:#d32f2f; font-size:13px;"><strong>Tip:</strong> Set status=CLOSED to exclude from OTS totals (Total drops)</p>
            `;
        }
        
        // Show run empire instructions
        function showRunEmpireInstructions() {
            document.getElementById('instructions-modal').style.display = 'flex';
            document.getElementById('instructions-modal').querySelector('h2').textContent = 'How to Run Empire';
            document.getElementById('instructions-modal').querySelector('div').innerHTML = `
                <p><strong>Step 1:</strong> Open PowerShell</p>
                <p><strong>Step 2:</strong> Navigate to folder:</p>
                <code style="background:#f5f5f5; padding:8px 12px; display:block; border-radius:5px; margin:10px 0; font-size:12px;">cd C:\\Users\\MYPC\\Desktop\\debt-arbitrage\\debt-empire</code>
                <p><strong>Step 3:</strong> Run analyzer:</p>
                <code style="background:#f5f5f5; padding:8px 12px; display:block; border-radius:5px; margin:10px 0; font-size:12px;">py empire.py</code>
                <p style="margin-top:15px;"><strong>Or double-click:</strong> <code>RUN.ps1</code></p>
                <p style="margin-top:15px; color:#666; font-size:13px;">This generates all reports: dashboard, projections, OTS letters</p>
            `;
        }
        
        // Show email instructions
        function showEmailInstructions() {
            document.getElementById('instructions-modal').style.display = 'flex';
            document.getElementById('instructions-modal').querySelector('h2').textContent = '📧 Batch OTS Email';
            document.getElementById('instructions-modal').querySelector('div').innerHTML = `
                <p><strong>Batch OTS Strategy:</strong></p>
                <p style="margin-top:10px;">Send OTS letters to all lenders with:</p>
                <ul style="margin:10px 0; padding-left:20px; line-height:1.8;">
                    <li>Start amount: ₹5L each (or as per negotiation)</li>
                    <li>OTS at 80% of outstanding (or 70% per RBI)</li>
                    <li>Attach OTS letters from <code>ots-pdfs/</code> folder</li>
                </ul>
                <p style="margin-top:15px;"><strong>Files:</strong> Open <code>ots-pdfs/</code> folder and attach HTML/PDF OTS letters</p>
                <p style="margin-top:10px; color:#666; font-size:13px;">Tip: Use email templates for consistent communication</p>
            `;
        }
        
        // Show add loan instructions
        function showAddLoanInstructions() {
            document.getElementById('instructions-modal').style.display = 'flex';
            document.getElementById('instructions-modal').querySelector('h2').textContent = '➕ Add New Loan';
            document.getElementById('instructions-modal').querySelector('div').innerHTML = `
                <p><strong>Step 1:</strong> Open PowerShell</p>
                <p><strong>Step 2:</strong> Navigate to folder:</p>
                <code style="background:#f5f5f5; padding:8px 12px; display:block; border-radius:5px; margin:10px 0; font-size:12px;">cd C:\\Users\\MYPC\\Desktop\\debt-arbitrage\\debt-empire</code>
                <p><strong>Step 3:</strong> Run verifier:</p>
                <code style="background:#f5f5f5; padding:8px 12px; display:block; border-radius:5px; margin:10px 0; font-size:12px;">py loan_verifier.py</code>
                <p style="margin-top:15px;"><strong>Or double-click:</strong> <code>RUN_VERIFIER.ps1</code></p>
                <p style="margin-top:15px; color:#666; font-size:13px;">In the menu, choose:<br>• Option 1: Add new loan<br>• This creates a new branch in <code>loans/</code> with shortcode</p>
            `;
        }
        
        // Close instructions modal
        function closeInstructions() {
            document.getElementById('instructions-modal').style.display = 'none';
        }
        
        // Close modal on outside click
        document.getElementById('instructions-modal').addEventListener('click', function(e) {
            if (e.target === this) {
                closeInstructions();
            }
        });
        
        // Auto-refresh every 5 minutes
        setTimeout(function() {
            location.reload();
        }, 300000);
    </script>
</body>
</html>"""
    
    return html

def main():
    print("="*70)
    print("GENERATING VERIFIER.HTML FROM MASTERS.JSON")
    print("="*70)
    
    masters_data = load_masters()
    loans_count = len(masters_data.get('loans', []))
    
    print(f"[OK] Loaded {loans_count} loans from masters.json")
    
    html_content = generate_html(masters_data)
    
    with open(VERIFIER_HTML, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"[OK] Generated verifier.html")
    print(f"[OK] Open in browser: {VERIFIER_HTML.absolute()}")
    print("\n" + "="*70)
    print("MASTER DASHBOARD FEATURES:")
    print("  • 🟢 OTS TARGETS: Running loans with shortcodes (baj8L, lt26L)")
    print("  • 🔴 CLOSED: Merit proof section")
    print("  • 📁 TREE VIEW: Per-loan branches with file list")
    print("  • 🖨️ PRINT: Ctrl+P → 'OTS Portfolio Dr. Nehru'")
    print("  • 📧 EMAIL: Batch OTS instructions")
    print("  • ✏️ EDIT: Status/OS/Notes → Save masters.json")
    print("  • ➕ ADD LOAN: New branch + shortcode")
    print("  • 📁 Folder tree: loans/Provider/Account + archive/YYYY")
    print("  • Responsive table, mobile-friendly, auto-refresh")
    print("="*70)

if __name__ == "__main__":
    main()
