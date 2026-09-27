@echo off
echo ========================================================
echo Starting NWIS Full-Stack Platform (Oil India SIH 2026)
echo ========================================================

echo [1/3] Checking Docker Database Containers...
docker start nwis-postgres nwis-redis >nul 2>&1

echo [2/3] Starting FastAPI Backend on Port 8000...
start "NWIS Backend Server (FastAPI :8000)" cmd /k "cd /d %~dp0backend && set PYTHONPATH=. && venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000"

echo [3/3] Starting Next.js 16 Frontend on Port 3000...
start "NWIS Frontend Server (Next.js :3000)" cmd /k "cd /d %~dp0frontend && npm run start"

echo.
echo ========================================================
echo All services launched!
echo Frontend: http://localhost:3000
echo Backend:  http://localhost:8000/docs
echo ========================================================
timeout /t 5 >nul
start http://localhost:3000
