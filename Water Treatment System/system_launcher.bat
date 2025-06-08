@echo off
REM Water Treatment System - System Launcher
REM Main launcher for all system components

:MAIN_MENU
cls
echo ================================================================
echo             WATER TREATMENT SYSTEM - CONTROL CENTER
echo ================================================================
echo.
echo                    Seawater Desalination System
echo                   Production Capacity: 10,000 L/hr
echo                      RO Recovery Rate: 45%%
echo.
echo ================================================================
echo.
echo Please select an option:
echo.
echo   1. Launch System Simulator
echo   2. Launch HMI Interface  
echo   3. Open Web HMI (Browser)
echo   4. System Status Monitor
echo   5. Generate Process Diagrams
echo   6. View System Documentation
echo   7. Open Configuration File
echo   8. System Health Check
echo   9. Export Status Report
echo   0. Exit
echo.
echo ================================================================

set /p choice="Enter your choice (0-9): "

if "%choice%"=="1" goto SIMULATOR
if "%choice%"=="2" goto HMI
if "%choice%"=="3" goto WEB_HMI
if "%choice%"=="4" goto STATUS_MONITOR
if "%choice%"=="5" goto DIAGRAMS
if "%choice%"=="6" goto DOCUMENTATION
if "%choice%"=="7" goto CONFIG
if "%choice%"=="8" goto HEALTH_CHECK
if "%choice%"=="9" goto EXPORT_REPORT
if "%choice%"=="0" goto EXIT

echo Invalid choice. Please try again.
pause
goto MAIN_MENU

:SIMULATOR
echo.
echo Launching System Simulator...
call run_simulator.bat
goto MAIN_MENU

:HMI
echo.
echo Launching HMI Interface...
call run_hmi.bat
goto MAIN_MENU

:WEB_HMI
echo.
echo Opening Web HMI in default browser...
if exist "web_hmi.html" (
    start "" "web_hmi.html"
) else (
    echo ERROR: web_hmi.html not found
    pause
)
goto MAIN_MENU

:STATUS_MONITOR
echo.
echo Launching System Status Monitor...
call run_status_monitor.bat
goto MAIN_MENU

:DIAGRAMS
echo.
echo Generating Process Diagrams...
call generate_diagrams.bat
goto MAIN_MENU

:DOCUMENTATION
echo.
echo Opening System Documentation...
if exist "README.md" (
    start "" "README.md"
) else (
    echo ERROR: README.md not found
    pause
)
goto MAIN_MENU

:CONFIG
echo.
echo Opening Configuration File...
if exist "plc_config.ini" (
    start notepad "plc_config.ini"
) else (
    echo ERROR: plc_config.ini not found
    pause
)
goto MAIN_MENU

:HEALTH_CHECK
echo.
echo Running System Health Check...
python -c "from system_status import SystemStatusMonitor; monitor = SystemStatusMonitor(); health = monitor.check_system_health(); print(f'System Health: {health[\"status\"]} ({health[\"health_score\"]}/100)'); [print(f'  - {issue}') for issue in health['issues']]; input('Press Enter to continue...')"
goto MAIN_MENU

:EXPORT_REPORT
echo.
echo Exporting System Status Report...
python -c "from system_status import SystemStatusMonitor; monitor = SystemStatusMonitor(); filepath = monitor.export_status_report(); print(f'Report exported to: {filepath}'); input('Press Enter to continue...')"
goto MAIN_MENU

:EXIT
echo.
echo Thank you for using the Water Treatment System!
echo.
echo System Overview:
echo   - Seawater Desalination Technology
echo   - Reverse Osmosis Processing  
echo   - Multi-Zone Distribution
echo   - Full Process Automation
echo   - Real-time Monitoring
echo.
echo For technical support, refer to the README.md documentation.
echo.
pause
exit /b 0
