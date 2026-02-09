# Fix Pandas Installation Issue with Python 3.13

## Problem
Pandas 2.1.3 doesn't support Python 3.13. The compilation fails with:
```
error C2198: '_PyLong_AsByteArray': too few arguments for call
```

## Solution Options

### Option 1: Use Newer Pandas (Recommended)
I've updated `requirements.txt` to use `pandas>=2.2.0` which supports Python 3.13.

**Install:**
```powershell
cd C:\Users\pc\Desktop\DEBT-EMPIRE\backend
pip install -r requirements.txt
```

### Option 2: Use Python 3.11 or 3.12 (Alternative)
If Option 1 doesn't work, use Python 3.11 or 3.12:

1. **Install Python 3.12** from https://www.python.org/downloads/
2. **Create virtual environment:**
   ```powershell
   python3.12 -m venv venv
   .\venv\Scripts\Activate.ps1
   ```
3. **Install dependencies:**
   ```powershell
   pip install -r requirements.txt
   ```

### Option 3: Install Pandas Separately (Quick Fix)
```powershell
# First install newer pandas
pip install pandas>=2.2.0

# Then install other requirements
pip install -r requirements.txt
```

## Verify Installation
```powershell
python -c "import pandas; print(f'Pandas version: {pandas.__version__}')"
```

Should show: `Pandas version: 2.2.x` or higher

## If Still Having Issues

### Try installing without pandas first:
```powershell
pip install fastapi uvicorn[standard] python-multipart psycopg2-binary pyjwt bcrypt python-dotenv openpyxl
pip install pandas --upgrade
```

### Or use pre-built wheel:
```powershell
pip install pandas --only-binary :all:
```
