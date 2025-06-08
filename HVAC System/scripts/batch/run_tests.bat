@echo off
REM HVAC System - Test Runner
REM Run integration tests for the restructured HVAC system

echo ============================================
echo HVAC System - Integration Tests
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

echo Running HVAC System Integration Tests...
echo.

REM Change to project root directory
cd /d "%~dp0..\.."

REM Check if test file exists
if not exist "tests\test_integration.py" (
    echo ERROR: Test file not found at tests\test_integration.py
    echo Please ensure the file exists
    pause
    exit /b 1
)

REM Run the integration tests
echo Running: python tests\test_integration.py
echo.
python tests\test_integration.py

REM Check exit code
if errorlevel 1 (
    echo.
    echo ERROR: Some tests failed
    echo Check the output above for details
) else (
    echo.
    echo All tests completed successfully!
)

echo.
echo Press any key to exit...
pause >nul
