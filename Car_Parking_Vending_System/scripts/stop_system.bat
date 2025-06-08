@echo off
REM Automated Car Parking System - Stop Script
REM This script safely stops all system components

echo ========================================
echo Automated Car Parking System
echo Stopping System Components...
echo ========================================

REM Kill Python processes related to the parking system
echo Stopping Python services...
taskkill /f /im python.exe /fi "WINDOWTITLE eq Communication Services*" 2>nul
taskkill /f /im python.exe /fi "WINDOWTITLE eq Parking Simulator*" 2>nul
taskkill /f /im python.exe /fi "WINDOWTITLE eq Desktop HMI*" 2>nul
taskkill /f /im python.exe /fi "WINDOWTITLE eq Web HMI*" 2>nul
taskkill /f /im python.exe /fi "WINDOWTITLE eq System Monitor*" 2>nul

REM Stop web server
echo Stopping web server...
for /f "tokens=5" %%a in ('netstat -aon ^| find ":8080" ^| find "LISTENING"') do taskkill /f /pid %%a 2>nul

REM Wait a moment for processes to terminate
timeout /t 2 /nobreak >nul

echo ========================================
echo System shutdown complete!
echo ========================================

pause
