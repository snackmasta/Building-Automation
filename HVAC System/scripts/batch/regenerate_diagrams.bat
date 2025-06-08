@echo off
REM HVAC System - Regenerate Diagrams
REM Quick batch script to regenerate all system diagrams

echo.
echo ================================
echo  HVAC System Diagram Generator
echo ================================
echo.

cd /d "%~dp0\.."
echo Current directory: %CD%
echo.

echo Regenerating all HVAC system diagrams...
python tests\regenerate_diagrams.py

echo.
echo ================================
echo  Process Complete
echo ================================
echo.
echo Open diagrams\index.html to view all diagrams
echo.
pause
