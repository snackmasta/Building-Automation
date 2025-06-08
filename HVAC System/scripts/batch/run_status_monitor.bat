@echo off
REM HVAC System - Status Monitor Launcher
REM Run the system status monitoring dashboard

echo ============================================
echo HVAC System - Status Monitor
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

echo Starting HVAC System Status Monitor...
echo.

REM Change to project root directory
cd /d "%~dp0..\.."

REM Check if system status monitor exists
if not exist "src\monitoring\system_status.py" (
    echo ERROR: System status monitor not found at src\monitoring\system_status.py
    echo Please ensure the file exists
    pause
    exit /b 1
)

REM Run the system status monitor
echo Running: python src\monitoring\system_status.py
echo.
python src\monitoring\system_status.py

REM Check exit code
if errorlevel 1 (
    echo.
    echo ERROR: System status monitor exited with error code %errorlevel%
    echo Check the logs for more information
) else (
    echo.
    echo System status monitor completed successfully
)

echo.
echo Press any key to exit...
pause >nul
