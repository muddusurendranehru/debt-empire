"""
FastAPI Backend - Debt Empire v2.0
Port: 8000
Purpose: Parse CSV, generate projections, OTS PDFs
Now with Database (Neon PostgreSQL) and Authentication
"""

from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from typing import List, Optional
import uvicorn
from pathlib import Path
import json
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import database and auth
from database import init_db, get_db
from database.models import Loan, User
from middleware import get_current_user
from routes.auth import router as auth_router

# Import existing empire engine (for backward compatibility)
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

# Include auth routes
app.include_router(auth_router)

# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    """Initialize database on application startup."""
    try:
        # Test database connection
        from database.connection import test_connection
        if test_connection():
            print("✅ Database connection successful")
            # Initialize schema
            init_db()
            print("✅ Database schema initialized")
        else:
            print("⚠️  Database connection failed - check DATABASE_URL")
    except Exception as e:
        print(f"⚠️  Database initialization error: {e}")
        print("   Continuing without database (some features may not work)")

# Initialize engine (for backward compatibility with JSON files)
engine = DebtEmpireEngine()

# Debt Empire project root (for uploads + masters used by loan_verifier/empire)
DEBT_EMPIRE_ROOT = Path(__file__).resolve().parent.parent
UPLOAD_LOAN_DIR = DEBT_EMPIRE_ROOT / "loans" / "new_uploads"
MASTERS_JSON = DEBT_EMPIRE_ROOT / "masters.json"
ALLOWED_LOAN_EXT = {".pdf", ".docx", ".xlsx", ".xls", ".jpg", ".jpeg", ".png", ".csv"}


@app.get("/")
async def root():
    """Health check."""
    return {"status": "ok", "service": "Debt Empire API", "version": "2.0", "database": "enabled"}


# ==================== AUTHENTICATED ROUTES ====================

@app.get("/api/masters")
async def get_masters(current_user: dict = Depends(get_current_user)):
    """
    Get user's loans from database.
    Protected route - requires authentication.
    """
    try:
        user_id = current_user['id']
        loans = Loan.get_by_user(user_id)
        
        # Calculate totals
        total_outstanding = sum(loan['outstanding'] for loan in loans)
        total_emi = sum(loan['emi'] for loan in loans)
        total_ots_liability = sum(loan['ots_amount_70pct'] for loan in loans)
        total_savings = sum(loan['savings'] for loan in loans)
        
        # Format response similar to old masters.json structure
        response = {
            'loans': {f"{loan['provider']}_{loan.get('account_ref', loan['id'])}": loan for loan in loans},
            'total_exposure': total_outstanding,
            'total_ots_liability': total_ots_liability,
            'total_savings': total_savings,
            'total_emi': total_emi,
            'last_updated': datetime.now().isoformat(),
            'user_id': user_id
        }
        
        return JSONResponse(content=response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/loans")
async def create_loan(
    provider: str,
    outstanding: int,
    emi: int,
    tenure_months: int,
    account_ref: Optional[str] = None,
    start_date: Optional[str] = None,
    loan_type: str = 'personal',
    status: str = 'RUNNING_PAID_EMI',
    current_user: dict = Depends(get_current_user)
):
    """
    Create a new loan.
    Protected route - requires authentication.
    """
    try:
        user_id = current_user['id']
        loan = Loan.create(
            user_id=user_id,
            provider=provider,
            outstanding=outstanding,
            emi=emi,
            tenure_months=tenure_months,
            account_ref=account_ref,
            start_date=start_date,
            loan_type=loan_type,
            status=status
        )
        return JSONResponse(content={"status": "success", "loan": loan})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/loans")
async def get_loans(current_user: dict = Depends(get_current_user)):
    """
    Get all loans for current user.
    Protected route - requires authentication.
    """
    try:
        user_id = current_user['id']
        loans = Loan.get_by_user(user_id)
        return JSONResponse(content={"loans": loans, "count": len(loans)})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/upload-csv")
async def upload_csv(
    file: UploadFile = File(...),
    month_name: Optional[str] = None,
    current_user: dict = Depends(get_current_user)
):
    """
    Upload CSV and validate columns.
    Safety Rule: VALIDATE CSV cols before processing.
    Protected route - requires authentication.
    """
    try:
        user_id = current_user['id']
        
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
        
        # TODO: Save to database monthly_statements table
        # For now, keep backward compatibility with JSON files
        
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
async def process_monthly(
    month_name: str,
    csv_path: Optional[str] = None,
    current_user: dict = Depends(get_current_user)
):
    """
    Process monthly ritual (8 steps).
    Safety Rule: SLOW - Verify each step.
    Protected route - requires authentication.
    """
    try:
        user_id = current_user['id']
        
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
async def get_projections(month_name: str, current_user: dict = Depends(get_current_user)):
    """Get projection Excel file. Protected route."""
    projection_file = engine.base_dir / "monthly" / f"{month_name}_projection.xlsx"
    
    if not projection_file.exists():
        raise HTTPException(status_code=404, detail=f"Projection file not found for {month_name}")
    
    return FileResponse(
        path=str(projection_file),
        filename=f"{month_name}_projection.xlsx",
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )


@app.get("/api/ots-pdfs")
async def list_ots_pdfs(current_user: dict = Depends(get_current_user)):
    """List available OTS PDFs. Protected route."""
    ots_dir = engine.base_dir / "ots-pdfs"
    pdfs = [f.name for f in ots_dir.glob("*.pdf")] if ots_dir.exists() else []
    
    return JSONResponse(content={"pdfs": pdfs})


@app.post("/api/upload-loan-document")
async def upload_loan_document(
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user)
):
    """
    Upload a loan document (PDF/DOCX/JPG/CSV/XLSX) from the HTML verifier.
    Saves to loans/new_uploads/. If PDF, optionally parses and adds to database.
    Protected route - requires authentication.
    """
    try:
        user_id = current_user['id']
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
                    
                    # Create loan in database instead of JSON
                    new_loan = Loan.create(
                        user_id=user_id,
                        provider=provider,
                        outstanding=int(os_amt),
                        emi=int(emi),
                        tenure_months=int(parsed.get("tenure_remaining_months") or (os_amt // emi) or 24),
                        account_ref=account_ref,
                        start_date=start_date
                    )
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
async def get_ots_pdf(filename: str, current_user: dict = Depends(get_current_user)):
    """Download OTS PDF. Protected route."""
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
    print("Database: Neon PostgreSQL")
    print("Authentication: JWT enabled")
    print("=" * 70)
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
