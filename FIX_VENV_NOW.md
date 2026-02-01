# Fix Broken Venv - Immediate Steps

## Problem: "failed to locate pyvenv.cfg"

Your venv is broken but still activated. Here's the immediate fix:

---

## Step 1: Deactivate Broken Venv

**In PowerShell, run:**
```powershell
deactivate
```

**If that doesn't work, manually clear environment:**
```powershell
$env:VIRTUAL_ENV = $null
$env:PATH = ($env:PATH -split ';' | Where-Object { $_ -notlike '*venv*' }) -join ';'
```

---

## Step 2: Remove Broken Venv

```powershell
cd C:\Users\MYPC\Desktop\debt-arbitrage\debt-empire\backend
Remove-Item -Recurse -Force venv -ErrorAction SilentlyContinue
```

---

## Step 3: Use Global Python (Fastest)

```powershell
# You're now using global Python (no venv)
cd C:\Users\MYPC\Desktop\debt-arbitrage

# Install requirements globally
pip install -r debt-empire\backend\requirements.txt

# Run backend
cd debt-empire\backend
python main.py
```

---

## Step 4: Run EMPIRE DEMO

```powershell
# Make sure you're deactivated (no venv in prompt)
cd C:\Users\MYPC\Desktop\debt-arbitrage

# Run demo (no pandas needed)
python debt-empire\DEMO_WITHOUT_PANDAS.py file:344
```

---

## Quick Copy-Paste Fix

```powershell
# 1. Deactivate
deactivate

# 2. Clear venv from PATH
$env:PATH = ($env:PATH -split ';' | Where-Object { $_ -notlike '*venv*' }) -join ';'
$env:VIRTUAL_ENV = $null

# 3. Remove broken venv
cd C:\Users\MYPC\Desktop\debt-arbitrage\debt-empire\backend
Remove-Item -Recurse -Force venv -ErrorAction SilentlyContinue

# 4. Verify Python works
python --version

# 5. Run demo
cd C:\Users\MYPC\Desktop\debt-arbitrage
python debt-empire\DEMO_WITHOUT_PANDAS.py file:344
```

---

## Or Use Script

```powershell
cd C:\Users\MYPC\Desktop\debt-arbitrage\debt-empire
.\DEACTIVATE_AND_RUN.ps1
```

---

**After deactivating, your prompt should NOT show `(venv)` anymore.**
