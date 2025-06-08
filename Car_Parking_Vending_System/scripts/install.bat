@echo off
REM Automated Car Parking System - Installation Script
REM This script sets up the complete development environment

echo ========================================
echo Automated Car Parking System
echo Installation and Setup
echo ========================================

REM Check if running as administrator
net session >nul 2>&1
if not %errorLevel% == 0 (
    echo This script requires administrator privileges.
    echo Please run as administrator.
    pause
    exit /b 1
)

REM Set working directory
cd /d "%~dp0\.."

REM Check Python installation
echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo.
    echo Please install Python 3.8 or later from:
    echo https://www.python.org/downloads/
    echo.
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
) else (
    echo Python is installed
    python --version
)

REM Check pip
echo Checking pip installation...
pip --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: pip is not available
    echo Installing pip...
    python -m ensurepip --upgrade
)

REM Create virtual environment
echo Creating Python virtual environment...
if exist "venv" (
    echo Removing existing virtual environment...
    rmdir /s /q venv
)

python -m venv venv
if errorlevel 1 (
    echo ERROR: Failed to create virtual environment
    pause
    exit /b 1
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install required packages
echo Installing required Python packages...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install required packages
    echo Trying to install packages individually...
    
    echo Installing core packages...
    pip install tkinter-async websockets asyncio
    pip install sqlite3 json datetime threading
    pip install numpy matplotlib
    
    echo Installing optional packages...
    pip install pymodbus opcua-client pyserial
    pip install pyyaml configparser
    pip install pytest pytest-asyncio
)

REM Create system directories
echo Creating system directories...
if not exist "logs" mkdir logs
if not exist "backups" mkdir backups
if not exist "data" mkdir data
if not exist "temp" mkdir temp
if not exist "reports" mkdir reports

REM Set up database
echo Setting up database...
python src\database\database_manager.py
if errorlevel 1 (
    echo WARNING: Database setup encountered issues
)

REM Create desktop shortcuts
echo Creating desktop shortcuts...
set DESKTOP=%USERPROFILE%\Desktop
set CURRENT_DIR=%CD%

REM Create shortcut for starting system
echo Creating start system shortcut...
powershell -Command "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%DESKTOP%\Start Parking System.lnk'); $Shortcut.TargetPath = '%CURRENT_DIR%\scripts\start_system.bat'; $Shortcut.WorkingDirectory = '%CURRENT_DIR%'; $Shortcut.IconLocation = 'shell32.dll,137'; $Shortcut.Save()"

REM Create shortcut for stopping system
echo Creating stop system shortcut...
powershell -Command "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%DESKTOP%\Stop Parking System.lnk'); $Shortcut.TargetPath = '%CURRENT_DIR%\scripts\stop_system.bat'; $Shortcut.WorkingDirectory = '%CURRENT_DIR%'; $Shortcut.IconLocation = 'shell32.dll,132'; $Shortcut.Save()"

REM Create shortcut for web HMI
echo Creating web HMI shortcut...
powershell -Command "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%DESKTOP%\Parking System Web HMI.lnk'); $Shortcut.TargetPath = 'http://localhost:8080'; $Shortcut.IconLocation = 'shell32.dll,13'; $Shortcut.Save()"

REM Test installation
echo Testing installation...
echo Running basic system tests...

python -c "
import sys
print('Python version:', sys.version)

# Test imports
try:
    import tkinter
    print('✓ Tkinter available')
except ImportError:
    print('✗ Tkinter not available')

try:
    import sqlite3
    print('✓ SQLite3 available')
except ImportError:
    print('✗ SQLite3 not available')

try:
    import websockets
    print('✓ WebSockets available')
except ImportError:
    print('✗ WebSockets not available')

try:
    import yaml
    print('✓ YAML available')
except ImportError:
    print('✗ YAML not available')

try:
    import matplotlib
    print('✓ Matplotlib available')
except ImportError:
    print('✗ Matplotlib not available')

print('Installation test completed')
"

echo ========================================
echo Installation Complete!
echo ========================================
echo.
echo The following shortcuts have been created on your desktop:
echo - Start Parking System
echo - Stop Parking System  
echo - Parking System Web HMI
echo.
echo To start the system:
echo 1. Double-click "Start Parking System" on your desktop
echo 2. Or run: scripts\start_system.bat
echo.
echo To access the web interface:
echo 1. Start the system first
echo 2. Open http://localhost:8080 in your browser
echo 3. Or double-click "Parking System Web HMI" shortcut
echo.
echo System files are located in:
echo %CD%
echo.
echo Press any key to continue...
pause >nul

REM Optional: Start system demonstration
echo.
echo Would you like to start the system now for a demonstration? (Y/N)
set /p DEMO_CHOICE=
if /i "%DEMO_CHOICE%"=="Y" (
    echo Starting system demonstration...
    call scripts\start_system.bat
)

echo Setup complete. Enjoy your Automated Car Parking System!
