# Debt Empire API Endpoints

## Base URL
```
http://localhost:8000
```

## Available Endpoints

### Public Endpoints (No Authentication Required)

#### 1. Health Check
```
GET /
```
**Response:**
```json
{
  "status": "ok",
  "service": "Debt Empire API",
  "version": "2.0",
  "database": "enabled"
}
```

#### 2. Sign Up
```
POST /api/auth/signup
Content-Type: application/json

Body:
{
  "email": "user@example.com",
  "password": "password123",
  "confirm_password": "password123",
  "phone": "+919963721999"  // optional
}
```

#### 3. Login
```
POST /api/auth/login
Content-Type: application/json

Body:
{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response:**
```json
{
  "message": "Login successful",
  "user_id": "uuid-here",
  "email": "user@example.com",
  "token": "jwt-token-here"
}
```

---

### Protected Endpoints (Require JWT Token)

**All protected endpoints require this header:**
```
Authorization: Bearer <your-jwt-token>
```

#### 4. Get Current User Info
```
GET /api/auth/me
Authorization: Bearer <token>
```

#### 5. Logout
```
POST /api/auth/logout
Authorization: Bearer <token>
```

#### 6. Get User's Loans (Masters)
```
GET /api/masters
Authorization: Bearer <token>
```

#### 7. Get All Loans
```
GET /api/loans
Authorization: Bearer <token>
```

#### 8. Create Loan
```
POST /api/loans
Authorization: Bearer <token>
Content-Type: application/json

Body:
{
  "provider": "L&T",
  "outstanding": 2574000,
  "emi": 80000,
  "tenure_months": 32,
  "account_ref": "BL240910207908339",
  "start_date": "2024-04-03",
  "loan_type": "personal",
  "status": "RUNNING_PAID_EMI"
}
```

#### 9. Upload CSV
```
POST /api/upload-csv?month_name=feb26
Authorization: Bearer <token>
Content-Type: multipart/form-data

Body: CSV file
```

#### 10. Process Monthly Ritual
```
POST /api/process-monthly?month_name=feb26
Authorization: Bearer <token>
```

#### 11. Get Projections
```
GET /api/projections/{month_name}
Authorization: Bearer <token>
```

#### 12. List OTS PDFs
```
GET /api/ots-pdfs
Authorization: Bearer <token>
```

#### 13. Download OTS PDF
```
GET /api/ots-pdfs/{filename}
Authorization: Bearer <token>
```

#### 14. Upload Loan Document
```
POST /api/upload-loan-document
Authorization: Bearer <token>
Content-Type: multipart/form-data

Body: PDF/DOCX/XLSX file
```

---

## Testing Endpoints

### Using Browser
- Health check: http://localhost:8000/
- All other endpoints require authentication

### Using PowerShell

**Test Health Check:**
```powershell
Invoke-RestMethod -Uri "http://localhost:8000/" -Method GET
```

**Test Sign Up:**
```powershell
$body = @{
    email = "test@example.com"
    password = "test123"
    confirm_password = "test123"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/api/auth/signup" -Method POST -Body $body -ContentType "application/json"
```

**Test Login:**
```powershell
$body = @{
    email = "test@example.com"
    password = "test123"
} | ConvertTo-Json

$response = Invoke-RestMethod -Uri "http://localhost:8000/api/auth/login" -Method POST -Body $body -ContentType "application/json"
$token = $response.token
Write-Host "Token: $token"
```

**Test Protected Endpoint (with token):**
```powershell
$headers = @{
    Authorization = "Bearer $token"
}

Invoke-RestMethod -Uri "http://localhost:8000/api/masters" -Method GET -Headers $headers
```

---

## Common Errors

### 404 Not Found
- Check the URL is correct
- Make sure the server is running on port 8000
- Verify the endpoint path matches exactly

### 401 Unauthorized
- Token is missing or invalid
- Token has expired (24 hours)
- Need to login again

### 500 Internal Server Error
- Check backend console for error messages
- Database connection issues (if using database)
- Missing environment variables

---

## FastAPI Interactive Docs

FastAPI provides automatic interactive documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

These pages show all available endpoints and allow you to test them directly!
