@echo off
:: HVAC System - Diagram Generator
:: This script generates system diagrams and documentation

echo ============================================
echo     HVAC System - Diagram Generator
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

:: Check if the diagram generator exists
if exist "utils\hvac_diagram_new.py" (
    set DIAGRAM_SCRIPT=utils\hvac_diagram_new.py
) else if exist "utils\hvac_diagram.py" (
    set DIAGRAM_SCRIPT=utils\hvac_diagram.py
) else (
    echo ERROR: HVAC diagram generator not found
    echo Expected location: utils\hvac_diagram.py or utils\hvac_diagram_new.py
    pause
    exit /b 1
)

:: Install required packages if needed
echo Checking Python dependencies...
python -c "import matplotlib, numpy" >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing required Python packages...
    pip install matplotlib numpy >nul 2>&1
    if %errorlevel% neq 0 (
        echo WARNING: Could not install packages automatically
        echo Please run: pip install matplotlib numpy
        echo.
    )
)

:: Create diagrams directory if it doesn't exist
if not exist "diagrams" mkdir diagrams

:: Generate diagrams
echo Generating HVAC system diagrams...
echo.

python %DIAGRAM_SCRIPT%

if %errorlevel% equ 0 (
    echo.
    echo ============================================
    echo Diagram generation completed successfully!
    echo ============================================
    echo.
    echo Generated files:
    echo - diagrams\hvac_system_overview.png
    echo - diagrams\zone_layout.png
    echo - diagrams\piping_schematic.png
    echo - diagrams\electrical_diagram.png
    echo - diagrams\control_flow.png
    echo.
    echo Opening diagrams folder...
    start diagrams
) else (
    echo.
    echo ERROR: Diagram generation failed
    echo Check the error messages above
)

pause
