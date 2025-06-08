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
set TESTS_DIR=%PROJECT_ROOT%\tests
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

echo Step 1: Running Unit Tests and System Validation...
echo -------------------------------------------------
python "%TESTS_DIR%\test_runner.py"
if %ERRORLEVEL% NEQ 0 (
    echo Unit tests and system validation failed with code %ERRORLEVEL%
    set TEST_STATUS=FAILED
) else (
    echo Unit tests and system validation completed successfully
    set TEST_STATUS=PASSED
)
echo.

echo ======================================================
echo Final Test Summary
echo ======================================================
echo Overall Test Status: %TEST_STATUS%
echo.
echo Detailed reports can be found in: %REPORTS_DIR%
echo and %TESTS_DIR%\test_results.json for unit test specifics.
echo ======================================================

rem Commenting out the old verification and summary steps as they are now part of test_runner.py
rem echo Step 1: Running System Verification...
rem echo ----------------------------------------
rem python "%VERIFICATION_DIR%\verify_system.py"
rem if %ERRORLEVEL% NEQ 0 (
rem     echo System verification failed with code %ERRORLEVEL%
rem     set SYSTEM_VERIFICATION_STATUS=FAILED
rem ) else (
rem     echo System verification completed successfully
rem     set SYSTEM_VERIFICATION_STATUS=PASSED
rem )
rem echo.
rem
rem echo Step 2: Generating Project Summary...
rem echo ----------------------------------
rem python "%UTILS_DIR%\project_summary.py"
rem if %ERRORLEVEL% NEQ 0 (
rem     echo Project summary generation failed with code %ERRORLEVEL%
rem     set SUMMARY_STATUS=FAILED
rem ) else (
rem     echo Project summary generated successfully
rem     set SUMMARY_STATUS=PASSED
rem )
rem echo.
rem
rem echo ======================================================
rem echo Verification Summary
rem echo ======================================================
rem echo System Verification: %SYSTEM_VERIFICATION_STATUS%
rem echo Project Summary: %SUMMARY_STATUS%
rem echo.
rem echo Reports saved to: %REPORTS_DIR%
rem echo ======================================================

rem Open project summary in browser if it was generated successfully
rem if "%SUMMARY_STATUS%"=="PASSED" (
rem     echo Opening project summary in browser...
rem     rem start "" "%REPORTS_DIR%\\project_summary_%TIMESTAMP%.html"
rem )

echo.
echo Press any key to exit...
pause > nul
