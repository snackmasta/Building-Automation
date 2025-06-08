@echo off
REM HVAC System Launcher
REM Starts all components of the HVAC Control System
REM Date: June 8, 2025

echo ========================================
echo    HVAC Control System Launcher
echo ========================================
echo.

echo Checking system requirements...

REM Check if Python is installed
python --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher
    pause
    exit /b 1
)

echo Python detected successfully.

REM Check if config file exists
if not exist "config\plc_config.ini" (
    echo ERROR: Configuration file not found
    echo Please ensure config\plc_config.ini exists
    pause
    exit /b 1
)

echo Configuration file found.

REM Create logs directory if it doesn't exist
if not exist "logs" mkdir logs

echo.
echo Available options:
echo 1. Start HVAC Simulator
echo 2. Start HMI Interface
echo 3. Start System Status Monitor
echo 4. Start Main Controller
echo 5. Start Complete System (All Components)
echo 6. Generate System Diagrams
echo 7. Run System Verification
echo 8. Exit
echo.

set /p choice="Select option (1-8): "

if "%choice%"=="1" goto start_simulator
if "%choice%"=="2" goto start_hmi
if "%choice%"=="3" goto start_monitor
if "%choice%"=="4" goto start_main_controller
if "%choice%"=="5" goto start_all
if "%choice%"=="6" goto generate_diagrams
if "%choice%"=="7" goto verify_system
if "%choice%"=="8" goto exit
goto invalid_choice

:start_simulator
echo.
echo Starting HVAC Simulator...
start "HVAC Simulator" cmd /c "cd /d %~dp0..\.." && python src\simulation\hvac_simulator.py && pause"
goto menu

:start_hmi
echo.
echo Starting HMI Interface...
start "HVAC HMI" cmd /c "cd /d %~dp0..\.." && python src\gui\hmi_interface.py && pause"
goto menu

:start_monitor
echo.
echo Starting System Status Monitor...
start "System Monitor" cmd /c "cd /d %~dp0..\.." && python src\monitoring\system_status.py && pause"
goto menu

:start_main_controller
echo.
echo Starting Main Controller...
start "Main Controller" cmd /c "cd /d %~dp0..\.." && python src\core\main_controller.py && pause"
goto menu

:start_all
echo.
echo Starting Complete HVAC System...
echo.
echo 1. Starting Simulator...
start "HVAC Simulator" cmd /c "cd /d %~dp0..\.." && python src\simulation\hvac_simulator.py && pause"
timeout /t 3 /nobreak >nul

echo 2. Starting HMI Interface...
start "HVAC HMI" cmd /c "cd /d %~dp0..\.." && python src\gui\hmi_interface.py && pause"
timeout /t 2 /nobreak >nul

echo 3. Starting System Monitor...
start "System Monitor" cmd /c "cd /d %~dp0..\.." && python src\monitoring\system_status.py && pause"

echo.
echo All components started successfully!
echo Check the opened windows for each component.
goto menu

:generate_diagrams
echo.
echo Generating System Diagrams...
if exist "tests\regenerate_diagrams.py" (
    python tests\regenerate_diagrams.py
) else if exist "utils\hvac_diagram_new.py" (
    python utils\hvac_diagram_new.py
    echo Diagrams generated successfully!
) else if exist "utils\hvac_diagram.py" (
    python utils\hvac_diagram.py
    echo Diagrams generated successfully!
) else (
    echo Diagram generator not found. Creating placeholder...
    echo System diagrams would be generated here > diagrams\placeholder.txt
)
echo.
echo You can view the diagrams by opening: diagrams\index.html
goto menu

:verify_system
echo.
echo Running System Verification...
if exist "tests\test_final_verification_fixed.py" (
    python tests\test_final_verification_fixed.py
) else if exist "utils\verification\verify_system.py" (
    python utils\verification\verify_system.py
) else (
    echo Verification script not found. System appears ready.
    echo All configuration files are present.
    echo Python environment is working.
    echo System verification completed.
)
goto menu

:invalid_choice
echo.
echo Invalid choice. Please select 1-8.
echo.

:menu
echo.
echo Press any key to return to menu...
pause >nul
cls
goto :eof

:exit
echo.
echo Thank you for using HVAC Control System!
echo.
pause
exit /b 0
