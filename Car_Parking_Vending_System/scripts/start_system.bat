@echo off
REM Automated Car Parking System - Startup Script
REM This script starts all system components in the correct order

echo ========================================
echo Automated Car Parking System
echo Starting System Components...
echo ========================================

REM Set working directory
cd /d "%~dp0"

REM Check Python installation
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or later
    pause
    exit /b 1
)

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo Creating Python virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment
        pause
        exit /b 1
    )
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install/update dependencies
echo Installing/updating dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

REM Create necessary directories
echo Creating system directories...
if not exist "logs" mkdir logs
if not exist "backups" mkdir backups
if not exist "data" mkdir data
if not exist "temp" mkdir temp

REM Initialize database
echo Initializing database...
python src\database\database_manager.py
if errorlevel 1 (
    echo WARNING: Database initialization failed
)

REM Start communication services
echo Starting communication services...
start "Communication Services" python src\communication\protocols.py

REM Wait for services to start
timeout /t 3 /nobreak >nul

REM Start simulation (if enabled)
echo Starting parking simulator...
start "Parking Simulator" python src\simulation\parking_simulator.py

REM Start desktop HMI
echo Starting desktop HMI...
start "Desktop HMI" python src\gui\main_hmi.py

REM Start web server for web HMI
echo Starting web HMI server...
cd hmi\web
start "Web HMI" python -m http.server 8080

REM Return to root directory
cd ..\..

echo ========================================
echo System startup complete!
echo ========================================
echo.
echo Services running:
echo - Communication Services (background)
echo - Parking Simulator (background)
echo - Desktop HMI (window)
echo - Web HMI Server (http://localhost:8080)
echo.
echo Press any key to open system monitoring...
pause >nul

REM Open system monitoring
start "System Monitor" python src\utilities\system_monitor.py

echo System is running. Check individual windows for status.
echo Press any key to return to menu...
pause >nul
