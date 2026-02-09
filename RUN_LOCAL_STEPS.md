# Manual Steps to Run and Test Locally

## Prerequisites Check

### Step 1: Check Python Installation
```powershell
python --version
# Should show Python 3.8 or higher
```

### Step 2: Check Node.js Installation
```powershell
node --version
npm --version
# Should show Node.js 18+ and npm
```

---

## Backend Setup (Terminal 1)

### Step 1: Navigate to Backend
```powershell
cd C:\Users\pc\Desktop\DEBT-EMPIRE\backend
```

### Step 2: Create .env File
```powershell
# Copy the example file
Copy-Item env.example .env

# Edit .env file and add:
# DATABASE_URL=your-neon-postgresql-connection-string
# JWT_SECRET=your-secret-key-min-32-chars
```

**IMPORTANT:** 
- Get your Neon PostgreSQL connection string from https://neon.tech
- Generate a JWT secret (at least 32 characters)
- If you don't have a database yet, you can test without it (some features won't work)

### Step 3: Install Python Dependencies
```powershell
pip install -r requirements.txt
```

### Step 4: Start Backend Server
```powershell
python main.py
```

**Expected Output:**
```
======================================================================
DEBT EMPIRE API - Starting on http://localhost:8000
Database: Neon PostgreSQL
Authentication: JWT enabled
======================================================================
INFO:     Started server process
INFO:     Waiting for application startup.
✅ Database connection successful
✅ Database schema initialized
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

**If Database Connection Fails:**
- The server will still start but show a warning
- You can test authentication endpoints without database
- Some features (like /api/masters) will require database

---

## Frontend Setup (Terminal 2)

### Step 1: Navigate to Frontend
```powershell
cd C:\Users\pc\Desktop\DEBT-EMPIRE\frontend
```

### Step 2: Install Node Dependencies
```powershell
npm install
```

### Step 3: Start Frontend Server
```powershell
npm run dev
```

**Expected Output:**
```
> debt-empire-frontend@2.0.0 dev
> next dev -p 3000

   ▲ Next.js 14.0.0
   - Local:        http://localhost:3000
   - ready started server on 0.0.0.0:3000
```

---

## Testing Locally

### Test 1: Backend Health Check
Open browser or use curl:
```
http://localhost:8000/
```

**Expected Response:**
```json
{
  "status": "ok",
  "service": "Debt Empire API",
  "version": "2.0",
  "database": "enabled"
}
```

### Test 2: Frontend Home Page
Open browser:
```
http://localhost:3000
```

**Expected Behavior:**
- Redirects to `/login` if not authenticated
- Redirects to `/dashboard` if already logged in

### Test 3: Sign Up (Manual)
1. Go to: `http://localhost:3000/signup`
2. Fill in:
   - Email: `test@example.com`
   - Password: `test123`
   - Confirm Password: `test123`
   - Phone: (optional)
3. Click "Sign Up"
4. Should redirect to `/dashboard`

### Test 4: Login (Manual)
1. Go to: `http://localhost:3000/login`
2. Fill in:
   - Email: `test@example.com`
   - Password: `test123`
3. Click "Log In"
4. Should redirect to `/dashboard`

### Test 5: Dashboard (Manual)
1. After login, you should see:
   - Portfolio Overview section
   - Upload CSV section
   - Loan details table (if you have loans)
2. Check browser console (F12) for any errors

### Test 6: API Endpoints (Using curl or Postman)

**Sign Up:**
```powershell
curl -X POST http://localhost:8000/api/auth/signup `
  -H "Content-Type: application/json" `
  -d '{\"email\":\"test@example.com\",\"password\":\"test123\",\"confirm_password\":\"test123\"}'
```

**Login:**
```powershell
curl -X POST http://localhost:8000/api/auth/login `
  -H "Content-Type: application/json" `
  -d '{\"email\":\"test@example.com\",\"password\":\"test123\"}'
```

**Get Masters (Protected - requires token):**
```powershell
# First login to get token, then:
curl -X GET http://localhost:8000/api/masters `
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

---

## Troubleshooting

### Backend Issues

**Issue: Module not found**
```powershell
# Reinstall dependencies
pip install -r requirements.txt
```

**Issue: Database connection failed**
- Check `.env` file has correct `DATABASE_URL`
- Verify Neon database is active (not paused)
- Server will still run, but database features won't work

**Issue: Port 8000 already in use**
```powershell
# Find and kill process using port 8000
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### Frontend Issues

**Issue: Module not found**
```powershell
# Reinstall dependencies
npm install
```

**Issue: Port 3000 already in use**
```powershell
# Find and kill process using port 3000
netstat -ano | findstr :3000
taskkill /PID <PID> /F
```

**Issue: CORS errors**
- Make sure backend is running on port 8000
- Check backend CORS settings in `main.py`

### Authentication Issues

**Issue: "Network error" on signup/login**
- Check backend is running: `http://localhost:8000/`
- Check browser console (F12) for errors
- Verify API_URL in frontend pages matches backend URL

**Issue: "Invalid token" errors**
- Clear localStorage: Open browser console, run `localStorage.clear()`
- Try logging in again

---

## Quick Start Commands (Copy-Paste)

### Terminal 1 - Backend:
```powershell
cd C:\Users\pc\Desktop\DEBT-EMPIRE\backend
pip install -r requirements.txt
python main.py
```

### Terminal 2 - Frontend:
```powershell
cd C:\Users\pc\Desktop\DEBT-EMPIRE\frontend
npm install
npm run dev
```

### Browser:
```
http://localhost:3000
```

---

## Success Indicators

✅ Backend running: `http://localhost:8000/` shows JSON response  
✅ Frontend running: `http://localhost:3000` loads login page  
✅ Sign up works: Can create account and redirects to dashboard  
✅ Login works: Can login with credentials  
✅ Dashboard loads: Shows portfolio overview (may be empty if no loans)  
✅ No console errors: Browser console (F12) shows no red errors  

---

## Next Steps After Testing

1. **Set up Neon Database** (if not done):
   - See `SETUP_DATABASE.md` for instructions
   - Update `.env` with `DATABASE_URL`

2. **Migrate Existing Data** (if you have `masters.json`):
   ```powershell
   cd backend
   python migrate_json_to_db.py
   ```

3. **Test Full Flow**:
   - Sign up → Login → Dashboard → Upload CSV → View Loans
