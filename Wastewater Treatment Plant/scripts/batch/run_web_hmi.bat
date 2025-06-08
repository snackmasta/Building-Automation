@echo off
echo Starting Wastewater Treatment Plant Web HMI Server...

:: Check if Python is installed
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Error: Python is not installed or not in PATH.
    echo Please install Python 3.6 or higher.
    pause
    exit /b 1
)

:: Check if required Python modules are installed
python -c "import flask" >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Installing Flask web framework...
    pip install flask
)

:: Set environment variables
set FLASK_APP=web_server.py
set FLASK_ENV=development

:: Create the web server script if it doesn't exist
if not exist "%~dp0..\..\src\gui\web\web_server.py" (
    echo Creating web server script...
    (
        echo # Web server for Wastewater Treatment Plant Web HMI
        echo import os
        echo import flask
        echo from flask import Flask, send_from_directory
        echo.
        echo app = Flask^(__name__^)
        echo.
        echo @app.route^('/'^)
        echo def index^(^):
        echo     return send_from_directory^(os.path.dirname^(os.path.abspath^(__file__^)^), 'web_hmi.html'^)
        echo.
        echo @app.route^('/api/data', methods=['GET']^)
        echo def get_data^(^):
        echo     """In a real application, this would connect to the PLC or OPC UA server."""
        echo     import random
        echo     import time
        echo     import json
        echo     data = {
        echo         "timestamp": time.time^(^),
        echo         "systemRunning": random.choice^([True, False]^),
        echo         "flowRate": round^(random.uniform^(280, 320^), 1^),
        echo         "tankLevel1": round^(random.uniform^(2.0, 3.0^), 1^),
        echo         "phValue": round^(random.uniform^(6.8, 7.5^), 1^),
        echo         "dissolvedOxygen": round^(random.uniform^(4.5, 6.5^), 1^)
        echo     }
        echo     return json.dumps^(data^)
        echo.
        echo if __name__ == '__main__':
        echo     print^("Starting Wastewater Treatment Plant Web HMI Server..."^)
        echo     print^("Web HMI available at: http://127.0.0.1:5000"^)
        echo     app.run^(host='0.0.0.0', port=5000, debug=True^)
    ) > "%~dp0..\..\src\gui\web\web_server.py"
)

:: Change to the web directory
cd "%~dp0..\..\src\gui\web"

:: Start the web server
echo Starting Flask Web Server...
python web_server.py

echo Web Server stopped.
pause
