@echo off
cd /d "%~dp0"
echo ========================================
echo    MEDICORE AI HOSPITAL SYSTEM
echo ========================================
echo Installing dependencies...
pip install flask numpy

echo.
echo Starting AI Hospital System...
echo Open your browser: http://localhost:5000
echo.
python hospital_ai.py

pause