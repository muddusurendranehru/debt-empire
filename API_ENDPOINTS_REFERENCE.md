# API Endpoints Reference - Debt Empire

## Base URL
```
http://localhost:8000
```

## Public Endpoints (No Authentication Required)

### 1. Health Check
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

### 2. Sign Up
```
POST /api/auth/signup
```
**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "password123",
  "confirm_password": "password123",
  "phone": "+919963721999"  // Optional
}
```
**Response:**
```json
{
  "message": "User created successfully",
  "user_id": "uuid-here",
  "email": "user@example.com",
  "token": "jwt-token-here"
}
```

### 3. Login
```
POST /api/auth/login
```
**Request Body:**
```json
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

## Protected Endpoints (Require JWT Token)

**All protected endpoints require:**
```
Authorization: Bearer <your-jwt-token>
```

### 4. Get Current User
```
GET /api/auth/me
```

### 5. Logout
```
POST /api/auth/logout
```

### 6. Get Masters (User's Loans)
```
GET /api/masters
```

### 7. Get All Loans
```
GET /api/loans
```

### 8. Create Loan
```
POST /api/loans
```
**Query Parameters:**
- `provider` (required)
- `outstanding` (required, integer)
- `emi` (required, integer)
- `tenure_months` (required, integer)
- `account_ref` (optional)
- `start_date` (optional, YYYY-MM-DD)
- `loan_type` (optional, default: 'personal')
- `status` (optional, default: 'RUNNING_PAID_EMI')

### 9. Upload CSV
```
POST /api/upload-csv
```
**Query Parameters:**
- `month_name` (optional, e.g., "feb26")

**Form Data:**
- `file` (CSV file)

### 10. Process Monthly Ritual
```
POST /api/process-monthly
```
**Request Body:**
```json
{
  "month_name": "feb26",
  "csv_path": "optional-path"
}
```

### 11. Get Projections
```
GET /api/projections/{month_name}
```

### 12. List OTS PDFs
```
GET /api/ots-pdfs
```

### 13. Download OTS PDF
```
GET /api/ots-pdfs/{filename}
```

### 14. Upload Loan Document
```
POST /api/upload-loan-document
```
**Form Data:**
- `file` (PDF/DOCX/XLSX/CSV/Image)

---

## Common Errors

### Method Not Allowed (405)
- **Cause:** Using wrong HTTP method (GET instead of POST, etc.)
- **Solution:** Check the endpoint documentation above for correct method

### Unauthorized (401)
- **Cause:** Missing or invalid JWT token
- **Solution:** Login first to get token, then include in Authorization header

### Not Found (404)
- **Cause:** Wrong endpoint URL
- **Solution:** Check the endpoint path is correct

### Internal Server Error (500)
- **Cause:** Database connection issue or server error
- **Solution:** Check server logs and database connection

---

## Testing Examples

### Using PowerShell

**Sign Up:**
```powershell
$body = @{
    email = "test@example.com"
    password = "test123"
    confirm_password = "test123"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/api/auth/signup" `
    -Method POST `
    -Body $body `
    -ContentType "application/json"
```

**Login:**
```powershell
$body = @{
    email = "test@example.com"
    password = "test123"
} | ConvertTo-Json

$response = Invoke-RestMethod -Uri "http://localhost:8000/api/auth/login" `
    -Method POST `
    -Body $body `
    -ContentType "application/json"

$token = $response.token
```

**Get Masters (Protected):**
```powershell
$headers = @{
    Authorization = "Bearer $token"
}

Invoke-RestMethod -Uri "http://localhost:8000/api/masters" `
    -Method GET `
    -Headers $headers
```

### Using curl

**Sign Up:**
```bash
curl -X POST http://localhost:8000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"test123","confirm_password":"test123"}'
```

**Login:**
```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"test123"}'
```

**Get Masters (Protected):**
```bash
curl -X GET http://localhost:8000/api/masters \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

---

## Interactive API Documentation

FastAPI provides automatic interactive documentation:

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

These pages show all available endpoints, methods, and allow you to test them directly!
