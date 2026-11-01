@echo off
echo ===================================================
echo   Starting AI Personal Assistant Web Application
echo ===================================================
cd /d "%~dp0backend"

if not exist ".venv\Scripts\python.exe" (
    echo Python virtual environment not found!
    echo Creating virtual environment...
    python -m venv .venv
    echo Installing backend dependencies...
    .venv\Scripts\python.exe -m pip install -r requirements.txt
)

echo.
echo Launching full-stack AI Assistant application...
echo Backend & Web UI will be accessible at: http://localhost:8000
echo.
.venv\Scripts\python.exe run.py
pause
