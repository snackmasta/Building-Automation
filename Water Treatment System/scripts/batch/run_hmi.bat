@echo off
REM Water Treatment System - HMI Interface Launcher
REM Run the Python-based HMI interface

echo ============================================
echo Water Treatment System - HMI Interface
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

echo Starting HMI Interface...
echo.

REM Install required packages if not present
echo Checking required packages...
pip install tkinter matplotlib numpy sqlite3 >nul 2>&1

REM Start the HMI interface
echo Launching HMI Interface...
cd /d "%~dp0..\.."
python src\gui\hmi_interface.py

if errorlevel 1 (
    echo.
    echo ERROR: Failed to start HMI Interface
    echo Check the error messages above
    pause
    exit /b 1
)

echo.
echo HMI Interface closed
pause
