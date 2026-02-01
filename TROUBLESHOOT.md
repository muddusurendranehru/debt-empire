# Troubleshooting Guide

## Virtual Environment Not Creating

### Issue: `python -m venv venv` does nothing

### Solutions:

**1. Check Python Installation:**
```powershell
python --version
# OR
py --version
# OR
python3 --version
```

**2. Try Alternative Command:**
```powershell
py -m venv venv
```

**3. Check PowerShell Execution Policy:**
```powershell
Get-ExecutionPolicy
# If Restricted, run:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**4. Manual Step-by-Step:**
```powershell
# Step 1: Navigate to backend
cd C:\Users\MYPC\Desktop\debt-arbitrage\debt-empire\backend

# Step 2: Check Python
python --version

# Step 3: Create venv (wait for completion)
python -m venv venv

# Step 4: Verify venv folder created
dir venv

# Step 5: Activate
.\venv\Scripts\Activate.ps1

# Step 6: Install requirements
pip install -r requirements.txt

# Step 7: Run server
python main.py
```

**5. Use Fixed Script:**
```powershell
cd C:\Users\MYPC\Desktop\debt-arbitrage\debt-empire
.\START_BACKEND_FIXED.ps1
```

---

## Common Issues

### Python Not Found
- Install Python from python.org
- Add Python to PATH during installation
- Restart PowerShell after installation

### Permission Denied
- Run PowerShell as Administrator
- Or use: `Set-ExecutionPolicy RemoteSigned -Scope CurrentUser`

### Virtual Environment Exists But Won't Activate
```powershell
# Delete and recreate
Remove-Item -Recurse -Force venv
python -m venv venv
.\venv\Scripts\Activate.ps1
```

---

## Quick Test Commands

```powershell
# Test Python
python --version

# Test pip
pip --version

# Test venv creation (in temp folder)
cd $env:TEMP
python -m venv test_venv
dir test_venv
Remove-Item -Recurse -Force test_venv
```

---

## Alternative: Use Global Python

If venv continues to fail, you can use global Python:

```powershell
cd C:\Users\MYPC\Desktop\debt-arbitrage\debt-empire\backend
pip install -r requirements.txt
python main.py
```

**Note:** This installs packages globally. Use venv when possible.
