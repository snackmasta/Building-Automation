@echo off
echo Starting Integrated Water Treatment System...
echo.
echo This will launch the combined HMI and Simulator
echo in a single application with compact interface
echo and LED indicators for component status.
echo.
pause

cd /d "%~dp0"
python integrated_water_treatment_system.py

pause
