# DEBT EMPIRE - COMMAND REFERENCE GUIDE
**All commands in one place - Quick Reference**

---

## 📋 MAIN SCRIPTS

### 1. **empire.py** - Main Analyzer (Generate Reports)
```powershell
py empire.py
```
**What it does:**
- Generates `masters.json` with loan analysis
- Creates `dashboard.html` (main dashboard)
- Creates `monthly projections.html` (EMI schedule)
- Creates `monthly projections.csv` (Excel-compatible)
- Generates OTS letters in `ots-pdfs/` folder (HTML + text)
- Calculates total exposure, OTS liability, savings

**Output files:**
- `masters.json` - Complete loan data
- `dashboard.html` - Open in browser → Ctrl+P to print
- `monthly projections.html` - EMI schedule table
- `monthly projections.csv` - Open in Excel
- `ots-pdfs/*.html` - HTML OTS letters (all lenders)
- `ots-pdfs/*.txt` - Plain text OTS letters

---

### 2. **loan_verifier.py** - Interactive Loan Verifier
```powershell
py loan_verifier.py
```
**What it does:**
- Interactive wizard to verify/add loans
- Fillable fields: borrower name, amounts, EMI, dates, fees
- Mock data templates for Bajaj/L&T/HDFC
- Edit existing loans
- Saves to `masters.json`

**Menu options:**
1. Verify new loan (Bajaj/L&T/HDFC)
2. Review existing loans
3. Edit loan details
4. Save & exit → run empire.py

---

### 3. **8step-ritual.py** - 8-Step Ritual CLI
```powershell
py 8step-ritual.py --empire
```
**What it does:**
- Runs the complete 8-step ritual
- Calls `empire()` function from `empire.py`

---

## 🚀 QUICK START SCRIPTS

### 4. **RUN.ps1** - Run Main Analyzer
```powershell
.\RUN.ps1
```
**What it does:**
- Runs `empire.py` automatically
- Shows output

---

### 5. **OPEN_HTML.ps1** - Open All HTML Files
```powershell
.\OPEN_HTML.ps1
```
**What it does:**
- Opens `dashboard.html` in browser
- Opens `monthly projections.html` in browser
- Opens `ots-pdfs\lt-ots.html` in browser

---

### 6. **INSTALL_NOW.ps1** - Install Dependencies
```powershell
.\INSTALL_NOW.ps1
```
**What it does:**
- Tries to install pandas, openpyxl, reportlab
- Uses Python 3.12 if available
- Shows installation status

---

## 📁 FILE STRUCTURE

```
debt-empire/
├── empire.py              ← Main analyzer (run this most often)
├── loan_verifier.py      ← Verify/add loans interactively
├── 8step-ritual.py        ← 8-step ritual CLI
├── RUN.ps1                ← Quick run script
├── OPEN_HTML.ps1          ← Open HTML files in browser
├── INSTALL_NOW.ps1        ← Install dependencies
├── masters.json           ← Loan master data (auto-generated)
├── dashboard.html         ← Main dashboard (open in browser)
├── monthly projections.html ← EMI schedule (open in browser)
├── monthly projections.csv  ← Excel-compatible CSV
└── ots-pdfs/              ← OTS letters folder
    ├── lt-ots.html        ← L&T OTS letter
    ├── hdfc-ots.html      ← HDFC OTS letter
    ├── tata-ots.html      ← Tata OTS letter
    ├── bajaj-ots.html     ← Bajaj OTS letter
    └── *.txt              ← Plain text versions
```

---

## 🔄 TYPICAL WORKFLOW

### **First Time Setup:**
```powershell
# 1. Navigate to folder
cd C:\Users\MYPC\Desktop\debt-arbitrage\debt-empire

# 2. (Optional) Install dependencies
.\INSTALL_NOW.ps1

# 3. Verify/add loans
py loan_verifier.py

# 4. Generate reports
py empire.py

# 5. View results
.\OPEN_HTML.ps1
```

### **Daily Use:**
```powershell
# Quick run (generates all reports)
py empire.py

# Or use script
.\RUN.ps1

# View HTML files
.\OPEN_HTML.ps1
```

---

## 📊 COMMON COMMANDS

### **Generate Reports:**
```powershell
py empire.py
```

### **Verify/Add Loans:**
```powershell
py loan_verifier.py
```

### **Open Dashboard:**
```powershell
start dashboard.html
```

### **Open Monthly Projections:**
```powershell
start "monthly projections.html"
```

### **Open L&T OTS Letter:**
```powershell
start ots-pdfs\lt-ots.html
```

### **View All Files:**
```powershell
Get-ChildItem *.html
Get-ChildItem ots-pdfs\*.html
```

---

## 🎯 QUICK REFERENCE

| Command | Purpose | Output |
|---------|---------|--------|
| `py empire.py` | Generate all reports | HTML, CSV, JSON files |
| `py loan_verifier.py` | Add/verify loans | Updates masters.json |
| `.\RUN.ps1` | Quick run analyzer | Same as empire.py |
| `.\OPEN_HTML.ps1` | Open HTML files | Opens in browser |
| `start dashboard.html` | View dashboard | Opens in browser |
| `start "monthly projections.html"` | View EMI schedule | Opens in browser |

---

## 💡 TIPS

1. **Most Used:** `py empire.py` - Run this to generate all reports
2. **Add Loans:** `py loan_verifier.py` - Use this to add new loans
3. **View Results:** `.\OPEN_HTML.ps1` - Opens all HTML files
4. **Print Dashboard:** Open `dashboard.html` → Press `Ctrl+P` → Save as PDF
5. **Email OTS:** Copy content from `ots-pdfs\lt-ots.html` or `.txt` file

---

## 🔧 TROUBLESHOOTING

### **"File not found" error:**
```powershell
# Make sure you're in the right folder
cd C:\Users\MYPC\Desktop\debt-arbitrage\debt-empire
```

### **"pandas not installed" warning:**
```powershell
# This is OK! Script works without it
# CSV files are generated instead of Excel
# HTML files always work
```

### **"reportlab not installed" warning:**
```powershell
# This is OK! Script works without it
# HTML OTS letters are generated instead of PDFs
# You can print HTML to PDF using Ctrl+P
```

---

## 📝 NOTES

- All scripts work **without dependencies** (pandas/reportlab optional)
- HTML files can be printed to PDF using `Ctrl+P`
- `masters.json` is the central data file (auto-updated)
- OTS letters are generated for all 4 lenders automatically
- Dashboard shows totals: Exposure, OTS Liability, Savings

---

## 🎯 ONE-LINER COMMANDS

```powershell
# Generate everything
py empire.py

# Add new loan
py loan_verifier.py

# View dashboard
start dashboard.html

# Open all HTML files
.\OPEN_HTML.ps1

# Quick run
.\RUN.ps1
```

---

**Last Updated:** January 2026
**Version:** Debt Empire v2.0
