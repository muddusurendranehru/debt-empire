"""
FastAPI Backend - Debt Empire v2.0
Port: 8000
Purpose: Parse CSV, generate projections, OTS PDFs
"""

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from typing import List, Optional
import uvicorn
from pathlib import Path
import json
from datetime import datetime

from empire import DebtEmpireEngine

app = FastAPI(title="Debt Empire API", version="2.0")

# CORS: allow local HTML (verifier_with_upload.html) and Next.js
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # local file + localhost
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize engine
engine = DebtEmpireEngine()

# Debt Empire project root (for uploads + masters used by loan_verifier/empire)
DEBT_EMPIRE_ROOT = Path(__file__).resolve().parent.parent
UPLOAD_LOAN_DIR = DEBT_EMPIRE_ROOT / "loans" / "new_uploads"
MASTERS_JSON = DEBT_EMPIRE_ROOT / "masters.json"
ALLOWED_LOAN_EXT = {".pdf", ".docx", ".xlsx", ".xls", ".jpg", ".jpeg", ".png", ".csv"}


@app.get("/")
async def root():
    """Health check."""
    return {"status": "ok", "service": "Debt Empire API", "version": "2.0"}


@app.get("/api/masters")
async def get_masters():
    """Get masters.json data."""
    try:
        masters = engine.load_masters()
        return JSONResponse(content=masters)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/upload-csv")
async def upload_csv(file: UploadFile = File(...), month_name: Optional[str] = None):
    """
    Upload CSV and validate columns.
    Safety Rule: VALIDATE CSV cols before processing.
    """
    try:
        # Validate file type
        if not file.filename.endswith('.csv'):
            raise HTTPException(status_code=400, detail="File must be CSV")
        
        # Read CSV content
        content = await file.read()
        
        # Save to temp location
        temp_path = Path("temp") / file.filename
        temp_path.parent.mkdir(exist_ok=True)
        temp_path.write_bytes(content)
        
        # Validate CSV columns
        validation_result = engine.validate_csv_columns(temp_path)
        
        if not validation_result['valid']:
            return JSONResponse(
                status_code=400,
                content={
                    "error": "CSV validation failed",
                    "details": validation_result['message'],
                    "required_columns": validation_result.get('required', []),
                    "found_columns": validation_result.get('found', [])
                }
            )
        
        # Process CSV
        if not month_name:
            month_name = datetime.now().strftime('%b%y').lower()
        
        result = engine.process_monthly_csv(temp_path, month_name)
        
        return JSONResponse(content={
            "status": "success",
            "month": month_name,
            "loans_parsed": result.get('loans_count', 0),
            "files_generated": result.get('files', [])
        })
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing error: {str(e)}")


@app.post("/api/process-monthly")
async def process_monthly(month_name: str, csv_path: Optional[str] = None):
    """
    Process monthly ritual (8 steps).
    Safety Rule: SLOW - Verify each step.
    """
    try:
        if csv_path:
            csv_path_obj = Path(csv_path)
            if not csv_path_obj.exists():
                raise HTTPException(status_code=404, detail=f"CSV file not found: {csv_path}")
        else:
            # Use latest CSV from monthly/stmts/
            stmts_dir = engine.base_dir / "monthly" / "stmts"
            csv_files = list(stmts_dir.glob("*.csv"))
            if not csv_files:
                raise HTTPException(status_code=404, detail="No CSV files found in monthly/stmts/")
            csv_path_obj = max(csv_files, key=lambda p: p.stat().st_mtime)
        
        result = engine.process_monthly_csv(csv_path_obj, month_name)
        
        return JSONResponse(content={
            "status": "success",
            "month": month_name,
            "steps_completed": 8,
            "result": result
        })
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/projections/{month_name}")
async def get_projections(month_name: str):
    """Get projection Excel file."""
    projection_file = engine.base_dir / "monthly" / f"{month_name}_projection.xlsx"
    
    if not projection_file.exists():
        raise HTTPException(status_code=404, detail=f"Projection file not found for {month_name}")
    
    return FileResponse(
        path=str(projection_file),
        filename=f"{month_name}_projection.xlsx",
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )


@app.get("/api/ots-pdfs")
async def list_ots_pdfs():
    """List available OTS PDFs."""
    ots_dir = engine.base_dir / "ots-pdfs"
    pdfs = [f.name for f in ots_dir.glob("*.pdf")] if ots_dir.exists() else []
    
    return JSONResponse(content={"pdfs": pdfs})


@app.post("/api/upload-loan-document")
async def upload_loan_document(file: UploadFile = File(...)):
    """
    Upload a loan document (PDF/DOCX/JPG/CSV/XLSX) from the HTML verifier.
    Saves to loans/new_uploads/. If PDF, optionally parses and adds to masters.json.
    No PowerShell needed: use the HTML drag-drop, then click Parse All / Upload.
    """
    try:
        ext = Path(file.filename or "").suffix.lower()
        if ext not in ALLOWED_LOAN_EXT:
            raise HTTPException(
                status_code=400,
                detail=f"Allowed: {', '.join(ALLOWED_LOAN_EXT)}"
            )
        UPLOAD_LOAN_DIR.mkdir(parents=True, exist_ok=True)
        safe_name = (file.filename or "upload").replace("..", "_")
        save_path = UPLOAD_LOAN_DIR / safe_name
        content = await file.read()
        save_path.write_bytes(content)
        result = {"status": "success", "saved_to": f"loans/new_uploads/{safe_name}", "parsed": False, "loan_added": False}
        if ext == ".pdf" and MASTERS_JSON.exists():
            try:
                import sys
                sys.path.insert(0, str(DEBT_EMPIRE_ROOT))
                import loan_verifier
                parsed = loan_verifier.parse_bajaj_pdf(save_path)
                if parsed:
                    os_amt = parsed.get("outstanding_principal") or 0
                    emi = parsed.get("emi_amount") or (os_amt // 24) or 1
                    provider = (parsed.get("provider") or "Bajaj Finance").replace(" Finance", "").strip()
                    if provider == "Bajaj": pass
                    elif "L&T" in provider or "L&T" in (parsed.get("provider") or ""): provider = "L&T"
                    account_ref = (parsed.get("account_number") or parsed.get("linked_account") or "").strip() or "—"
                    start_date = parsed.get("emi_start_date") or "2024-01-01"
                    new_loan = {
                        "provider": provider,
                        "outstanding": int(os_amt),
                        "emi": int(emi),
                        "tenure_months": int(parsed.get("tenure_remaining_months") or (os_amt // emi) or 24),
                        "ots_amount_70pct": round(os_amt * 0.70),
                        "savings": int(os_amt - round(os_amt * 0.70)),
                        "start_date": start_date,
                        "account_ref": account_ref,
                    }
                    with open(MASTERS_JSON, "r", encoding="utf-8") as f:
                        masters = json.load(f)
                    masters.setdefault("loans", []).append(new_loan)
                    masters["total_exposure"] = sum(l.get("outstanding", 0) for l in masters["loans"])
                    masters["total_ots_liability"] = sum(round(l.get("outstanding", 0) * 0.70) for l in masters["loans"])
                    masters["total_savings"] = masters["total_exposure"] - masters["total_ots_liability"]
                    masters["generated_at"] = datetime.now().isoformat()
                    with open(MASTERS_JSON, "w", encoding="utf-8") as f:
                        json.dump(masters, f, indent=2, ensure_ascii=False)
                    result["parsed"] = True
                    result["loan_added"] = True
                    result["account_ref"] = account_ref
            except Exception as e:
                result["parse_error"] = str(e)
        return JSONResponse(content=result)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/ots-pdfs/{filename}")
async def get_ots_pdf(filename: str):
    """Download OTS PDF."""
    pdf_path = engine.base_dir / "ots-pdfs" / filename
    
    if not pdf_path.exists():
        raise HTTPException(status_code=404, detail="PDF not found")
    
    return FileResponse(
        path=str(pdf_path),
        filename=filename,
        media_type="application/pdf"
    )


if __name__ == "__main__":
    print("=" * 70)
    print("DEBT EMPIRE API - Starting on http://localhost:8000")
    print("=" * 70)
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
