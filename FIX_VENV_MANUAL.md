# Manual Venv Fix - Step by Step

## Complete Process

### Step 1: Exit Broken Venv
```powershell
deactivate
```

**If that doesn't work:**
```powershell
$env:VIRTUAL_ENV = $null
$env:PATH = ($env:PATH -split ';' | Where-Object { $_ -notlike '*venv*' }) -join ';'
```

---

### Step 2: Delete Old Venv
```powershell
cd C:\Users\MYPC\Desktop\debt-arbitrage\debt-empire

# Remove venv folder
Remove-Item -Recurse -Force venv -ErrorAction SilentlyContinue

# Also remove backend\venv if exists
Remove-Item -Recurse -Force backend\venv -ErrorAction SilentlyContinue
```

**Or use rmdir:**
```powershell
rmdir /s /q venv
rmdir /s /q backend\venv
```

---

### Step 3: Create New Venv
```powershell
cd C:\Users\MYPC\Desktop\debt-arbitrage\debt-empire
python -m venv venv_new
```

**Wait for completion** (may take 10-30 seconds)

---

### Step 4: Activate New Venv
```powershell
.\venv_new\Scripts\Activate.ps1
```

**Your prompt should show:** `(venv_new) PS ...`

---

### Step 5: Test Python
```powershell
python --version
```

Should show: `Python 3.13.5` (or your version)

---

### Step 6: Install Packages
```powershell
# Upgrade pip first
pip install --upgrade pip

# Install required packages
pip install pandas openpyxl fastapi uvicorn

# Install backend requirements
cd backend
pip install -r requirements.txt
cd ..
```

---

### Step 7: Verify Installation
```powershell
python -c "import pandas; import fastapi; print('✅ All packages OK')"
```

---

## Quick Script (All Steps)

**Or use the automated script:**
```powershell
cd C:\Users\MYPC\Desktop\debt-arbitrage\debt-empire
.\FIX_VENV_COMPLETE.ps1
```

---

## After Fix

### Run Backend:
```powershell
cd backend
python main.py
```

### Run EMPIRE DEMO:
```powershell
cd C:\Users\MYPC\Desktop\debt-arbitrage
python debt-empire\DEMO_WITHOUT_PANDAS.py file:344
```

---

## Troubleshooting

### If venv_new creation fails:
- Try: `py -m venv venv_new`
- Or use global Python (no venv)

### If activation fails:
- Check: `Test-Path venv_new\Scripts\Activate.ps1`
- May need: `Set-ExecutionPolicy RemoteSigned -Scope CurrentUser`

### If packages fail to install:
- Python 3.13 may not have pandas wheels yet
- Use CSV version: `DEMO_WITHOUT_PANDAS.py` (no pandas needed)

---

**Ready to fix!** 🚀
