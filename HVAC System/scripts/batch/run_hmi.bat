@echo off
:: HVAC System - HMI Interface Launcher
:: This script launches the Human Machine Interface for the HVAC control system

echo ============================================
echo         HVAC System - HMI Interface
echo ============================================
echo.

:: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher
    pause
    exit /b 1
)

:: Set the working directory to the HVAC System root
cd /d "%~dp0..\.."

:: Check if the HMI interface file exists
if not exist "src\gui\hmi_interface.py" (
    echo ERROR: HMI interface file not found
    echo Expected location: src\gui\hmi_interface.py
    pause
    exit /b 1
)

:: Install required packages if needed
echo Checking Python dependencies...
python -c "import tkinter, matplotlib, numpy" >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing required Python packages...
    pip install matplotlib numpy >nul 2>&1
    if %errorlevel% neq 0 (
        echo WARNING: Could not install some packages automatically
        echo Please run: pip install matplotlib numpy
        echo.
    )
)

:: Launch the HMI interface
echo Starting HVAC HMI Interface...
echo.
echo Controls:
echo - Use the tabs to navigate between different views
echo - Zone Control: Adjust temperature setpoints and modes
echo - Equipment Status: Monitor all HVAC equipment
echo - Trends: View historical data and graphs
echo - Alarms: Check system alerts and warnings
echo - Settings: Configure system parameters
echo.
echo Press Ctrl+C in this window to stop the HMI
echo.

python src\gui\hmi_interface.py

if %errorlevel% neq 0 (
    echo.
    echo ERROR: HMI Interface failed to start
    echo Check the error messages above
    pause
)
