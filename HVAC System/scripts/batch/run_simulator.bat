@echo off
:: HVAC System - Simulator Launcher
:: This script launches the HVAC system simulator

echo ============================================
echo       HVAC System - Plant Simulator
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

:: Check if the simulator file exists
if not exist "src\simulation\hvac_simulator.py" (
    echo ERROR: HVAC simulator file not found
    echo Expected location: src\simulation\hvac_simulator.py
    pause
    exit /b 1
)

:: Install required packages if needed
echo Checking Python dependencies...
python -c "import numpy, json, time, random, math" >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing required Python packages...
    pip install numpy >nul 2>&1
    if %errorlevel% neq 0 (
        echo WARNING: Could not install numpy automatically
        echo Please run: pip install numpy
        echo.
    )
)

:: Create logs directory if it doesn't exist
if not exist "logs" mkdir logs

:: Launch the simulator
echo Starting HVAC Plant Simulator...
echo.
echo Simulation Features:
echo - 8-zone thermal dynamics modeling
echo - Realistic equipment behavior
echo - Weather simulation
echo - Occupancy patterns
echo - Energy consumption tracking
echo - Data logging to logs\hvac_sim_data.csv
echo.
echo The simulator will run continuously until stopped
echo Press Ctrl+C to stop the simulation
echo.

python src\simulation\hvac_simulator.py

if %errorlevel% neq 0 (
    echo.
    echo ERROR: HVAC Simulator failed to start
    echo Check the error messages above
    pause
)
