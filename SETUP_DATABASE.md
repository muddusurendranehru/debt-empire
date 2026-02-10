# Database Setup Guide - Debt Empire

## Step 1: Set Up Neon PostgreSQL Database

1. **Create Neon Account** (if you don't have one):
   - Go to https://neon.tech
   - Sign up for a free account

2. **Create a New Project**:
   - Click "Create Project"
   - Choose a project name (e.g., "debt-empire")
   - Select a region close to you
   - Click "Create Project"

3. **Get Connection String**:
   - In your Neon dashboard, go to your project
   - Click on "Connection Details"
   - Copy the connection string (it looks like: `postgresql://user:password@host/database?sslmode=require`)

## Step 2: Configure Environment Variables

1. **Create `.env` file in `backend/` directory**:
   ```bash
   cd backend
   cp env.example .env
   ```

2. **Edit `.env` file**:
   - Paste your Neon connection string into `DATABASE_URL`
   - Generate a strong JWT secret (at least 32 characters):
     ```bash
     # On Linux/Mac:
     openssl rand -hex 32
     
     # Or use an online generator
     ```
   - Paste the JWT secret into `JWT_SECRET`

Example `.env` file:
```
DATABASE_URL=postgresql://user:password@ep-xxx.region.aws.neon.tech/dbname?sslmode=require
JWT_SECRET=your-generated-secret-key-here-min-32-chars
API_PORT=8000
```

## Step 3: Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

## Step 4: Initialize Database Schema

The database schema will be automatically created when you start the backend server for the first time.

Alternatively, you can manually run:

```python
from database import init_db
init_db()
```

## Step 5: Test Database Connection

```python
from database.connection import test_connection
if test_connection():
    print("✅ Database connected!")
else:
    print("❌ Database connection failed")
```

## Step 6: Start Backend Server

```bash
cd backend
python main.py
```

You should see:
```
✅ Database connection successful
✅ Database schema initialized
DEBT EMPIRE API - Starting on http://localhost:8000
Database: Neon PostgreSQL
Authentication: JWT enabled
```

## Step 7: Test Authentication

### Sign Up:
```bash
curl -X POST http://localhost:8000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "test123",
    "confirm_password": "test123"
  }'
```

### Login:
```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "test123"
  }'
```

## Database Schema

The following tables are created:

1. **users** - User authentication (email, password_hash, phone)
2. **loans** - Loan records (provider, outstanding, emi, etc.)
3. **monthly_statements** - CSV upload records
4. **projections** - Monthly projection data

All tables use UUID primary keys as required.

## Troubleshooting

### Connection Error
- Check your `DATABASE_URL` in `.env`
- Ensure your Neon database is active (not paused)
- Verify network connectivity

### Schema Not Created
- Check backend logs for errors
- Manually run `init_db()` from Python
- Verify database permissions

### Authentication Not Working
- Check `JWT_SECRET` is set in `.env`
- Verify token is being sent in Authorization header
- Check backend logs for JWT errors

## Next Steps

1. Start frontend: `cd frontend && npm install && npm run dev`
2. Open http://localhost:3000
3. Sign up for a new account
4. Login and access the dashboard
