# Quick Fix: Broken Virtual Environment

## Problem: "failed to locate pyvenv.cfg"

Your venv is broken. Here's the quick fix:

### Solution 1: Fix Script (Easiest)

```powershell
cd C:\Users\MYPC\Desktop\debt-arbitrage\debt-empire
.\FIX_BROKEN_VENV.ps1
```

Then follow the instructions it prints.

---

### Solution 2: Manual Fix

**Step 1: Deactivate broken venv**
```powershell
deactivate
```

**Step 2: Remove broken venv**
```powershell
cd C:\Users\MYPC\Desktop\debt-arbitrage\debt-empire\backend
Remove-Item -Recurse -Force venv
```

**Step 3: Create fresh venv**
```powershell
python -m venv venv
```

**Step 4: Activate**
```powershell
.\venv\Scripts\Activate.ps1
```

**Step 5: Install requirements**
```powershell
pip install -r requirements.txt
```

**Step 6: Run server**
```powershell
python main.py
```

---

### Solution 3: Skip Venv (Fastest)

**Just use global Python:**

```powershell
# Deactivate broken venv
deactivate

# Install globally
cd C:\Users\MYPC\Desktop\debt-arbitrage\debt-empire\backend
pip install -r requirements.txt

# Run server
python main.py
```

**Or use the no-venv script:**
```powershell
cd C:\Users\MYPC\Desktop\debt-arbitrage\debt-empire
.\START_BACKEND_NO_VENV.ps1
```

---

## Why This Happened

The venv was created but the `pyvenv.cfg` file is missing, making it incomplete. This happens when:
- File copy errors during venv creation
- Permission issues
- Interrupted creation process

**Fix:** Remove and recreate the venv, or use global Python.
