@echo off
REM Water Treatment System - Simulator Launcher
REM Run the Python-based system simulator

echo ============================================
echo Water Treatment System - Simulator
echo ============================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.7 or higher
    pause
    exit /b 1
)

echo Starting Water Treatment Simulator...
echo.

REM Install required packages if not present
echo Checking required packages...
pip install tkinter matplotlib numpy sqlite3 configparser >nul 2>&1

REM Start the simulator
echo Launching Simulator...
cd /d "%~dp0..\.."
python src\simulation\water_treatment_simulator.py

if errorlevel 1 (
    echo.
    echo ERROR: Failed to start Simulator
    echo Check the error messages above
    pause
    exit /b 1
)

echo.
echo Simulator closed
pause
