#!/bin/bash
echo '🚀 Local Empire: Backend 8000 | Frontend 3000'

# Backend stub
echo 'Backend ready: localhost:8000/api/parse'
cd backend
python main.py &
BACKEND_PID=$!
cd ..

# Frontend stub  
echo 'Frontend: localhost:3000'
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

# Wait for both processes
wait $BACKEND_PID $FRONTEND_PID
