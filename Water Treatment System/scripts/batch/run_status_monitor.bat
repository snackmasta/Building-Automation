@echo off
REM Water Treatment System - Status Monitor Launcher
REM Run the system status monitoring dashboard

echo ============================================
echo Water Treatment System - Status Monitor
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

echo Starting System Status Monitor...
echo.

REM Install required packages if not present
echo Checking required packages...
pip install psutil sqlite3 configparser >nul 2>&1

REM Start the status monitor with dashboard
echo Launching Status Dashboard...
cd /d "%~dp0..\.."
python src\monitoring\system_status.py --dashboard

if errorlevel 1 (
    echo.
    echo ERROR: Failed to start Status Monitor
    echo Check the error messages above
    pause
    exit /b 1
)

echo.
echo Status Monitor closed
pause
