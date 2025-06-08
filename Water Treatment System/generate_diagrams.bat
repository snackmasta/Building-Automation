@echo off
REM Water Treatment System - Process Diagram Generator
REM Generate process flow diagrams in PNG and PDF formats

echo ============================================
echo Water Treatment System - Diagram Generator
echo ============================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.7 or higher
    pause
    exit /b 1
)

echo Generating Process Diagrams...
echo.

REM Install required packages if not present
echo Installing required packages...
pip install matplotlib numpy >nul 2>&1

REM Generate diagrams
echo Creating process flow diagrams...
python process_diagram.py

if errorlevel 1 (
    echo.
    echo ERROR: Failed to generate diagrams
    echo Check the error messages above
    pause
    exit /b 1
)

echo.
echo Diagrams generated successfully!
echo Check the following files:
echo   - water_treatment_process_diagram.png
echo   - water_treatment_pid.png
echo   - control_system_architecture.png
echo   - water_treatment_diagrams.pdf
echo.

REM Open the PDF file if it exists
if exist "water_treatment_diagrams.pdf" (
    echo Opening PDF diagrams...
    start "" "water_treatment_diagrams.pdf"
)

pause
