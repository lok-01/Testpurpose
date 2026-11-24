@echo off
echo ========================================================
echo Launching AstroRize Vedic Research Lab
echo ========================================================
start "AstroRize Backend" cmd /c start_backend.bat
start "AstroRize Frontend" cmd /c start_frontend.bat
echo Both services launched.
echo Backend: http://127.0.0.1:8000/docs
echo Frontend: http://localhost:3000
