@echo off
title Industrial Process Control System Launcher
color 0A

echo.
echo ====================================================
echo   INDUSTRIAL PROCESS CONTROL SYSTEM LAUNCHER
echo ====================================================
echo.
echo Available Applications:
echo.
echo   1. PLC Simulator (Command Line)
echo   2. Desktop HMI Interface
echo   3. Web HMI Interface
echo   4. Generate P^&ID Diagram
echo   5. View Documentation
echo   6. Run All Applications
echo   7. Exit
echo.

:menu
set /p choice="Enter your choice (1-7): "

if "%choice%"=="1" goto simulator
if "%choice%"=="2" goto desktop_hmi
if "%choice%"=="3" goto web_hmi
if "%choice%"=="4" goto generate_pid
if "%choice%"=="5" goto documentation
if "%choice%"=="6" goto run_all
if "%choice%"=="7" goto exit

echo Invalid choice! Please try again.
goto menu

:simulator
echo.
echo Starting PLC Simulator...
echo ========================
start cmd /k "python plc_simulator.py"
goto menu

:desktop_hmi
echo.
echo Starting Desktop HMI...
echo =======================
start python hmi_interface.py
goto menu

:web_hmi
echo.
echo Opening Web HMI...
echo ==================
start web_hmi.html
goto menu

:generate_pid
echo.
echo Generating P^&ID Diagram...
echo ===========================
python pid_diagram.py
echo.
echo P^&ID diagram generated successfully!
pause
goto menu

:documentation
echo.
echo Opening Documentation...
echo ========================
start README.md
start PID_HMI_Documentation.md
goto menu

:run_all
echo.
echo Starting All Applications...
echo ============================
echo.
echo 1. Starting PLC Simulator...
start cmd /k "python plc_simulator.py"
timeout /t 2 /nobreak >nul

echo 2. Starting Desktop HMI...
start python hmi_interface.py
timeout /t 2 /nobreak >nul

echo 3. Opening Web HMI...
start web_hmi.html
timeout /t 2 /nobreak >nul

echo.
echo All applications started successfully!
echo You can now test the complete system.
pause
goto menu

:exit
echo.
echo Thank you for using the Industrial Process Control System!
echo.
pause
exit

:end
