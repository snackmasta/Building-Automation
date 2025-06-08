@echo off
rem Interactive Project Summary Generator for Wastewater Treatment Plant
rem This script launches the interactive project summary generator CLI

echo.
echo ======================================================
echo Wastewater Treatment Plant Project Summary Generator
echo ======================================================
echo.

set PROJECT_ROOT=%~dp0..\
set UTILS_DIR=%PROJECT_ROOT%\utils

rem Check if Python is available
where python >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Error: Python is not found in the PATH.
    echo Please make sure Python is installed and added to the PATH.
    goto :exit
)

rem Run the interactive summary generator
python "%UTILS_DIR%\summary_generator_cli.py" --project-root "%PROJECT_ROOT%"

:exit
echo.
if %ERRORLEVEL% NEQ 0 (
    echo Summary generation failed with code %ERRORLEVEL%
) else (
    echo Summary generation completed successfully
)

echo.
echo Press any key to exit...
pause > nul
