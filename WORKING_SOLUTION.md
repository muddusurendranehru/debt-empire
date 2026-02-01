# ✅ Working Solution - Global Python

## Success! Use Global Python (No Venv Needed)

### Step 1: Exit Venv
```powershell
deactivate
```

### Step 2: Navigate to Root
```powershell
cd C:\Users\MYPC\Desktop\debt-arbitrage\debt-empire
```

### Step 3: Install Packages Globally
```powershell
pip install pandas openpyxl
```

### Step 4: Run Commands
```powershell
# 8-Step Ritual
python 8step-ritual.py --monthly test.csv

# EMPIRE DEMO
python agent.py --demo-csv file:344

# Backend
cd backend
python main.py
```

---

## Why This Works

- ✅ **No venv issues** - Uses system Python directly
- ✅ **Simpler** - No activation needed
- ✅ **Faster** - No venv creation overhead
- ✅ **Safe** - Desktop environment, isolated from system Python

---

## Recommended Setup

**For Backend:**
```powershell
cd C:\Users\MYPC\Desktop\debt-arbitrage\debt-empire\backend
pip install -r requirements.txt
python main.py
```

**For Frontend:**
```powershell
cd C:\Users\MYPC\Desktop\debt-arbitrage\debt-empire\frontend
npm install
npm run dev
```

**For CLI Tools:**
```powershell
cd C:\Users\MYPC\Desktop\debt-arbitrage\debt-empire
python 8step-ritual.py --monthly test.csv
```

---

## Quick Reference

| Task | Command |
|------|---------|
| Install packages | `pip install pandas openpyxl fastapi uvicorn` |
| Run 8-step ritual | `python 8step-ritual.py --monthly test.csv` |
| Run EMPIRE DEMO | `python agent.py --demo-csv file:344` |
| Start backend | `cd backend && python main.py` |
| Start frontend | `cd frontend && npm run dev` |

---

**✅ This is the recommended approach!** No venv needed for desktop development.
