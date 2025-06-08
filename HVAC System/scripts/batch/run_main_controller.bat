@echo off
REM HVAC System - Main Controller Launcher
REM Run the main HVAC control system

echo ============================================
echo HVAC System - Main Controller
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

echo Starting HVAC Main Controller...
echo.

REM Change to project root directory
cd /d "%~dp0..\.."

REM Check if main controller exists
if not exist "src\core\main_controller.py" (
    echo ERROR: Main controller not found at src\core\main_controller.py
    echo Please ensure the file exists
    pause
    exit /b 1
)

REM Create necessary directories
if not exist "logs" mkdir logs
if not exist "data" mkdir data

REM Run the main controller
echo Running: python src\core\main_controller.py
echo.
echo Press Ctrl+C to stop the controller
echo.
python src\core\main_controller.py

REM Check exit code
if errorlevel 1 (
    echo.
    echo ERROR: Main controller exited with error code %errorlevel%
    echo Check the logs for more information
) else (
    echo.
    echo Main controller stopped successfully
)

echo.
echo Press any key to exit...
pause >nul
