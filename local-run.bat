@echo off
echo 🚀 Local Empire: Backend 8000 | Frontend 3000

REM Backend stub
echo Backend ready: localhost:8000/api/parse
start "Debt Empire Backend" cmd /c "cd backend && python main.py"

REM Frontend stub
echo Frontend: localhost:3000
start "Debt Empire Frontend" cmd /c "cd frontend && npm run dev"

pause
