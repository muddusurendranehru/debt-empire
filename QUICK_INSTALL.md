# Quick Install Guide - PowerShell Commands

## Where to Run These Commands

**Run in PowerShell** (Windows Terminal, PowerShell ISE, or VS Code Terminal)

## Step-by-Step Instructions

### 1. Open PowerShell
- Press `Win + X` → Select "Windows PowerShell" or "Terminal"
- Or press `Win + R` → Type `powershell` → Enter

### 2. Navigate to Project Directory
```powershell
cd C:\Users\MYPC\Desktop\debt-arbitrage\debt-empire
```

### 3. Try Installation Methods (in order)

#### Method 1: Standard Install
```powershell
py -3.12 -m pip install --user pandas openpyxl reportlab
```

#### Method 2: With Trusted Hosts (if Method 1 fails)
```powershell
py -3.12 -m pip install --user --trusted-host pypi.org --trusted-host files.pythonhosted.org pandas openpyxl reportlab
```

#### Method 3: Upgrade pip first, then install
```powershell
py -3.12 -m pip install --upgrade pip --user
py -3.12 -m pip install --user pandas openpyxl reportlab
```

### 4. Verify Installation
```powershell
py -3.12 -c "import pandas; import reportlab; print('All packages installed!')"
```

### 5. Run Empire Script
```powershell
py -3.12 empire.py
```

## Or Use the Install Script

```powershell
cd C:\Users\MYPC\Desktop\debt-arbitrage\debt-empire
.\INSTALL_NOW.ps1
```

## Troubleshooting

### If you get "py: command not found"
- Use `python` instead: `python -m pip install pandas openpyxl reportlab`
- Or use full path: `C:\Python312\python.exe -m pip install pandas openpyxl reportlab`

### If you get permission errors
- Add `--user` flag (already included above)
- Or run PowerShell as Administrator

### If network errors persist
- Check firewall settings
- Try using mobile hotspot (bypass corporate proxy)
- Or use offline installation method

## Current Status (Without Dependencies)

Even without installing, you can:
- ✅ View `masters.json` (complete loan analysis)
- ✅ View `dashboard.html` in browser (visual dashboard)
- ✅ See all calculations (totals, OTS amounts, savings)

The script already ran successfully and generated `masters.json`!
