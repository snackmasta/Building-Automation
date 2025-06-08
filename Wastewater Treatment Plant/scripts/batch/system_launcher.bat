@echo off
echo ===============================================
echo   Wastewater Treatment Plant Control System    
echo ===============================================
echo.
echo Starting system components...

:: Set environment variables
set BASE_PATH=%~dp0..\..
set PYTHON_PATH=python
set CONFIG_PATH=%BASE_PATH%\config

echo Checking environment...
%PYTHON_PATH% --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Python not found in PATH. Please install Python 3.8 or higher.
    exit /b 1
)

echo.
echo Starting HMI interface...
start "Wastewater Treatment HMI" cmd /c "%~dp0run_hmi.bat"
timeout /t 3 >nul

echo Starting system simulator...
start "Wastewater Treatment Simulator" cmd /c "%~dp0run_simulator.bat"
timeout /t 3 >nul

echo Starting monitoring system...
start "System Monitoring" cmd /c "%~dp0run_status_monitor.bat"
timeout /t 1 >nul

echo.
echo System startup complete.
echo.
echo Control interfaces:
echo - HMI: http://localhost:8050 (Web interface)
echo - Desktop HMI: Running in separate window
echo - System monitoring: http://localhost:8051
echo.
echo Press any key to shut down all system components...

pause >nul

echo.
echo Shutting down system components...
taskkill /FI "WINDOWTITLE eq Wastewater Treatment HMI*" /F >nul 2>&1
taskkill /FI "WINDOWTITLE eq Wastewater Treatment Simulator*" /F >nul 2>&1
taskkill /FI "WINDOWTITLE eq System Monitoring*" /F >nul 2>&1

echo System shutdown complete.
exit /b 0
