# How to Open HTML Files

## Method 1: Double-Click Script (Easiest)
1. Double-click `OPEN_HTML.ps1` in File Explorer
2. All HTML files will open automatically in your browser

## Method 2: PowerShell Commands
Open PowerShell in the `debt-empire` folder and run:

```powershell
# Open main dashboard
start dashboard.html

# Open monthly projections
start "monthly projections.html"

# Open L&T OTS letter
start ots-pdfs\lt-ots.html
```

## Method 3: File Explorer (Manual)
1. Open File Explorer
2. Navigate to: `C:\Users\MYPC\Desktop\debt-arbitrage\debt-empire`
3. Double-click any `.html` file:
   - `dashboard.html` → Main dashboard
   - `monthly projections.html` → EMI schedule
   - `ots-pdfs\lt-ots.html` → L&T OTS letter

## Method 4: Browser Address Bar
1. Open your browser (Chrome, Edge, Firefox)
2. Press `Ctrl+L` to focus address bar
3. Type or paste:
   ```
   file:///C:/Users/MYPC/Desktop/debt-arbitrage/debt-empire/dashboard.html
   ```
4. Press Enter

## Quick Access
- **Dashboard**: `dashboard.html`
- **Projections**: `monthly projections.html`
- **L&T OTS**: `ots-pdfs\lt-ots.html`
- **HDFC OTS**: `ots-pdfs\hdfc-ots.html`
- **Tata OTS**: `ots-pdfs\tata-ots.html`
- **Bajaj OTS**: `ots-pdfs\bajaj-ots.html`

## To Print/Save as PDF
1. Open HTML file in browser
2. Press `Ctrl+P`
3. Choose "Save as PDF" or select printer
