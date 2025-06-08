@echo off
echo Starting Wastewater Treatment Plant HMI...
echo.

set BASE_PATH=%~dp0..\..
set PYTHON_PATH=python
set HMI_PATH=%BASE_PATH%\src\gui\hmi_interface.py

:: Check if Python is available
%PYTHON_PATH% --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Python not found in PATH. Please install Python 3.8 or higher.
    exit /b 1
)

:: Check if the required Python packages are installed
%PYTHON_PATH% -c "import tkinter, matplotlib" >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Installing required Python packages...
    %PYTHON_PATH% -m pip install matplotlib >nul 2>&1
)

:: Check if the HMI script exists
if not exist "%HMI_PATH%" (
    echo HMI interface script not found at: %HMI_PATH%
    exit /b 1
)

:: Run the HMI
cd %BASE_PATH%
echo Launching HMI interface...
%PYTHON_PATH% %HMI_PATH%

exit /b 0
