# Debt Empire v2.0 - Full-Stack Application

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green.svg)](https://fastapi.tiangolo.com/)
[![Next.js](https://img.shields.io/badge/Next.js-14-black.svg)](https://nextjs.org/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

**Monthly Ritual System:** Parse → Track → Project → Docs → OTS → Legal

> Full-stack debt management system with 8-step monthly ritual workflow, CSV validation, and safety checks.

---

## 🏗️ Architecture

```
debt-empire/
├── README.md (this file)
├── frontend/          # Next.js (localhost:3000)
│   ├── pages/index.js # Dashboard UI
│   └── package.json
├── backend/           # FastAPI (localhost:8000)
│   ├── main.py       # API endpoints
│   ├── empire.py     # 8-step engine
│   └── requirements.txt
├── 8step-ritual.py   # CLI core
└── local-run.sh      # One-click start
```

---

## 🚀 Quick Start

### Option 1: One-Click Startup

**Linux/Mac:**
```bash
./local-run.sh    # Backend:8000 Frontend:3000
```

**Windows:**
```bash
local-run.bat    # Separate windows
```

→ **Empire LIVE localhost:3000**

### Option 2: Global Python (Recommended for Desktop)

**No venv needed - use global Python:**

```powershell
# Install packages once
pip install pandas openpyxl fastapi uvicorn

# Run commands directly
python 8step-ritual.py --monthly test.csv
cd backend && python main.py
cd frontend && npm run dev
```

**✅ Simpler, faster, proven to work!**

### Manual Startup (Alternative)

**Recommended: Use Global Python (No Venv)**

**Terminal 1 - Backend:**
```powershell
cd backend
pip install -r requirements.txt
python main.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm install
npm run dev
```

**Note:** Global Python works fine for desktop development. Venv is optional.

---

## 📋 Monthly Ritual

### Via Web UI (Frontend)
1. Open http://localhost:3000
2. Upload LoanLens CSV
3. Enter month name (e.g., feb26)
4. Auto-executes all 8 steps

### Via CLI
```bash
python 8step-ritual.py --monthly feb26.csv
```

**With validation:**
```bash
python 8step-ritual.py --monthly feb26.csv --auto
```

**Validate only:**
```bash
python 8step-ritual.py --validate-only loanlens.csv
```

---

## 🔄 8-Step Ritual

1. **Copy CSV** → `monthly/stmts/[month].csv`
2. **Parse CSV** → Extract loan data
3. **Save Parsed** → `[month]_parsed.json`
4. **Update Masters** → `masters.json`
5. **Generate Projections** → `[month]_projection.xlsx`
6. **Update Docs** → `docs-checklist.md`
7. **Generate OTS PDFs** → `ots-pdfs/`
8. **Update Vision** → `vision.md`

---

## 🛡️ Safety Rules

1. **VALIDATE:** CSV columns checked before processing
2. **NO ASSUME:** Missing data prompts for confirmation
3. **SLOW:** Each step verified with approval
4. **ERRORS:** Try/except + Log + STOP on errors
5. **FACTS:** Only cite actual files
6. **NO SEND:** Drafts only (you email)
7. **2 Servers:** Frontend (3000) | Backend (8000)

---

## 📊 API Endpoints

### GET `/api/masters`
Get masters.json data

### POST `/api/upload-csv`
Upload CSV and process monthly ritual
- Query param: `month_name` (optional)
- Body: CSV file

### POST `/api/process-monthly`
Process monthly ritual
- Body: `{ "month_name": "feb26", "csv_path": "..." }`

### GET `/api/projections/{month_name}`
Download projection Excel file

### GET `/api/ots-pdfs`
List available OTS PDFs

### GET `/api/ots-pdfs/{filename}`
Download OTS PDF

---

## 📁 Output Structure

```
empire/
├── masters.json              # 7 loans master data
├── monthly/
│   ├── stmts/               # CSV statements
│   ├── [month]_parsed.json  # Parsed data
│   └── [month]_projection.xlsx
├── docs-checklist.md
├── ots-pdfs/                # OTS PDFs
└── vision.md               # Clean summary
```

---

## ✅ Features

- ✅ **8-Step Workflow** - Complete automation
- ✅ **CSV Validation** - Column checking before processing
- ✅ **Safety Checks** - No assumptions, verify steps
- ✅ **Error Handling** - Try/except + logging
- ✅ **Web UI** - Next.js dashboard
- ✅ **API** - FastAPI backend
- ✅ **CLI** - Command-line interface

---

## 🔧 Requirements

**Backend:**
- Python 3.8+
- FastAPI, uvicorn, pandas, openpyxl

**Frontend:**
- Node.js 18+
- Next.js 14+

---

## 📝 Usage Examples

### Upload CSV via API
```bash
curl -X POST "http://localhost:8000/api/upload-csv?month_name=feb26" \
  -F "file=@loanlens_feb26.csv"
```

### Process Monthly via CLI
```bash
python 8step-ritual.py --monthly feb26.csv
```

### Validate CSV Only
```bash
python 8step-ritual.py --validate-only loanlens.csv
```

---

**Status:** ✅ **FULLY FUNCTIONAL**

Ready for monthly ritual! 🚀

---

## 📦 Installation

```bash
git clone https://github.com/muddusurendranehru/debt-empire.git
cd debt-empire
```

See [GITHUB_SETUP.md](GITHUB_SETUP.md) for GitHub deployment instructions.

---

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

---

## 👤 Author

**Muddu Surendra Nehru**

- GitHub: [@muddusurendranehru](https://github.com/muddusurendranehru)
- Repository: [debt-empire](https://github.com/muddusurendranehru/debt-empire)

---

## 🤝 Contributing

Contributions welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.
