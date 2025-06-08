@echo off
echo Wastewater Treatment Plant Diagram Generator

:: Check for Python installation
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Error: Python is not installed or not in PATH.
    echo Please install Python 3.6 or higher.
    pause
    exit /b 1
)

:: Check for required Python packages
python -c "import matplotlib, networkx, numpy" >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Installing required Python packages...
    pip install matplotlib networkx numpy
)

:: Set script directory
set SCRIPT_DIR=%~dp0..

:: Run the diagram generator
echo Running diagram generator...
python "%SCRIPT_DIR%\..\src\core\diagram_generator.py" --all

:: Check if diagrams were created
if exist "%SCRIPT_DIR%\..\diagrams\treatment_control_flowchart.png" (
    echo.
    echo Diagram generation successful.
    echo Diagrams saved to the 'diagrams' directory.
    echo.
    
    :: Open the diagrams folder
    echo Opening diagrams folder...
    start "" "%SCRIPT_DIR%\diagrams"
) else (
    echo Error: Diagram generation failed.
)

echo.
pause
