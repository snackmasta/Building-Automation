@echo off
rem System Verification Script for Wastewater Treatment Plant
rem This script runs all system verification tools and generates reports

echo.
echo ======================================================
echo Wastewater Treatment Plant System Verification
echo ======================================================
echo Timestamp: %date% %time%
echo.

rem Define paths
set PROJECT_ROOT=%~dp0..\..
set UTILS_DIR=%PROJECT_ROOT%\utils
set VERIFICATION_DIR=%UTILS_DIR%\verification
set REPORTS_DIR=%PROJECT_ROOT%\reports
set TIMESTAMP=%date:~-4,4%%date:~-7,2%%date:~-10,2%_%time:~0,2%%time:~3,2%%time:~6,2%
set TIMESTAMP=%TIMESTAMP: =0%

rem Create directories if they don't exist
if not exist "%VERIFICATION_DIR%" (
    echo Creating verification directory...
    mkdir "%VERIFICATION_DIR%"
)

rem Create reports directory if it doesn't exist
if not exist "%REPORTS_DIR%" (
    mkdir "%REPORTS_DIR%"
    echo Created reports directory: %REPORTS_DIR%
)

echo Step 1: Running System Verification...
echo ----------------------------------------
python "%VERIFICATION_DIR%\verify_system.py"
if %ERRORLEVEL% NEQ 0 (
    echo System verification failed with code %ERRORLEVEL%
    set SYSTEM_VERIFICATION_STATUS=FAILED
) else (
    echo System verification completed successfully
    set SYSTEM_VERIFICATION_STATUS=PASSED
)
echo.

echo Step 2: Generating Project Summary...
echo ----------------------------------
python "%UTILS_DIR%\project_summary.py"
if %ERRORLEVEL% NEQ 0 (
    echo Project summary generation failed with code %ERRORLEVEL%
    set SUMMARY_STATUS=FAILED
) else (
    echo Project summary generated successfully
    set SUMMARY_STATUS=PASSED
)
echo.

echo ======================================================
echo Verification Summary
echo ======================================================
echo System Verification: %SYSTEM_VERIFICATION_STATUS%
echo Project Summary: %SUMMARY_STATUS%
echo.
echo Reports saved to: %REPORTS_DIR%
echo ======================================================

rem Open project summary in browser if it was generated successfully
if "%SUMMARY_STATUS%"=="PASSED" (
    echo Opening project summary in browser...
    start "" "%REPORTS_DIR%\project_summary_%TIMESTAMP%.html"
)

echo.
echo Press any key to exit...
pause > nul
