@echo off
echo ========================================================
echo Starting AstroRize Vedic Research Lab - Backend (FastAPI)
echo ========================================================
cd backend
"C:\Users\balok\AppData\Local\Programs\Python\Python311\python.exe" -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
pause
