# Web server for Wastewater Treatment Plant Web HMI
import os
import flask
from flask import Flask, send_from_directory, jsonify
import random
import time
import json
import datetime

app = Flask(__name__)

# Simulated PLC data
process_values = {
    "systemRunning": False,
    "maintenanceMode": False,
    "autoMode": True,
    "stormMode": False,
    "alarmActive": False,
    "flowRate": 300.0,
    "tankLevel1": 2.5,
    "tankLevel2": 1.8,
    "phValue": 7.2,
    "dissolvedOxygen": 5.5,
    "turbidity": 35.0,
    "chlorine": 2.3,
    "temperature": 18.5,
    "treatmentEfficiency": 95.0,
    "energyConsumption": 175.0,
    "totalFlowToday": 2568.0,
    "chemicalUsage": 120.5,
    "pumpP101Status": False,
    "pumpP102Status": False,
    "blowerStatus": False,
    "mixerM101Status": False,
    "mixerM102Status": False,
    "uvSystemStatus": False,
    "alarms": []
}

# Historical data for trends
historical_data = {
    "timestamps": [],
    "flowValues": [],
    "phValues": [],
    "doValues": []
}

# Initialize with some historical data
def init_historical_data():
    now = time.time()
    for i in range(20):
        historical_data["timestamps"].append(now - (20 - i) * 60)
        historical_data["flowValues"].append(300 + random.uniform(-25, 25))
        historical_data["phValues"].append(7.2 + random.uniform(-0.2, 0.2))
        historical_data["doValues"].append(5.5 + random.uniform(-0.5, 0.5))

# Update the simulated process values
def update_process_values():
    if process_values["systemRunning"]:
        # Simulate random variations in process values
        process_values["flowRate"] += random.uniform(-10, 10)
        process_values["flowRate"] = max(0, min(500, process_values["flowRate"]))
        
        process_values["tankLevel1"] += random.uniform(-0.1, 0.1)
        process_values["tankLevel1"] = max(0, min(5, process_values["tankLevel1"]))
        
        process_values["tankLevel2"] += random.uniform(-0.1, 0.1)
        process_values["tankLevel2"] = max(0, min(5, process_values["tankLevel2"]))
        
        process_values["phValue"] += random.uniform(-0.1, 0.1)
        process_values["phValue"] = max(6, min(9, process_values["phValue"]))
        
        process_values["dissolvedOxygen"] += random.uniform(-0.2, 0.2)
        process_values["dissolvedOxygen"] = max(2, min(8, process_values["dissolvedOxygen"]))
        
        process_values["turbidity"] += random.uniform(-2.5, 2.5)
        process_values["turbidity"] = max(10, min(100, process_values["turbidity"]))
        
        process_values["chlorine"] += random.uniform(-0.15, 0.15)
        process_values["chlorine"] = max(1, min(4, process_values["chlorine"]))
        
        process_values["temperature"] += random.uniform(-0.1, 0.1)
        process_values["temperature"] = max(15, min(25, process_values["temperature"]))
        
        process_values["treatmentEfficiency"] = 93 + random.uniform(0, 5)
        process_values["energyConsumption"] = 150 + random.uniform(0, 50)
        process_values["totalFlowToday"] += process_values["flowRate"] / 3600  # per second
        process_values["chemicalUsage"] += random.uniform(0, 0.01)
        
        # Update equipment status randomly
        if random.random() < 0.02:
            if process_values["pumpP101Status"] and process_values["pumpP102Status"]:
                process_values["pumpP102Status"] = random.random() < 0.3
            elif not process_values["pumpP101Status"] and not process_values["pumpP102Status"]:
                process_values["pumpP101Status"] = True
            else:
                process_values["pumpP101Status"] = not process_values["pumpP101Status"]
                process_values["pumpP102Status"] = not process_values["pumpP102Status"]
        
        # Generate random alarms
        if random.random() < 0.01:
            alarm_types = [
                {"message": "High pH level detected", "severity": "warning"},
                {"message": "Low oxygen level in aeration tank", "severity": "warning"},
                {"message": "High turbidity in final effluent", "severity": "warning"},
                {"message": "Pump P101 high current", "severity": "warning"},
                {"message": "Communication error with dosing system", "severity": "warning"}
            ]
            random_alarm = random.choice(alarm_types)
            timestamp = datetime.datetime.now().strftime("%H:%M:%S")
            process_values["alarms"].append({
                "time": timestamp,
                "message": random_alarm["message"],
                "severity": random_alarm["severity"]
            })
            # Keep only the most recent 10 alarms
            if len(process_values["alarms"]) > 10:
                process_values["alarms"] = process_values["alarms"][-10:]
        
        # Update historical data
        now = time.time()
        historical_data["timestamps"].append(now)
        historical_data["flowValues"].append(process_values["flowRate"])
        historical_data["phValues"].append(process_values["phValue"])
        historical_data["doValues"].append(process_values["dissolvedOxygen"])
        
        # Keep only the last 20 data points
        if len(historical_data["timestamps"]) > 20:
            historical_data["timestamps"].pop(0)
            historical_data["flowValues"].pop(0)
            historical_data["phValues"].pop(0)
            historical_data["doValues"].pop(0)

# Serve the main HTML page
@app.route('/')
def index():
    return send_from_directory(os.path.dirname(os.path.abspath(__file__)), 'web_hmi.html')

# API endpoint to get current process data
@app.route('/api/data', methods=['GET'])
def get_data():
    """Get the current state of the process values"""
    update_process_values()
    
    # Format timestamps for JSON
    formatted_timestamps = [datetime.datetime.fromtimestamp(ts).strftime("%H:%M:%S") 
                          for ts in historical_data["timestamps"]]
    
    return jsonify({
        "processValues": process_values,
        "historicalData": {
            "timestamps": formatted_timestamps,
            "flowValues": historical_data["flowValues"],
            "phValues": historical_data["phValues"],
            "doValues": historical_data["doValues"]
        }
    })

# API endpoint to control the system
@app.route('/api/control/<action>', methods=['POST'])
def control_system(action):
    """Control system operations"""
    if action == "start":
        process_values["systemRunning"] = True
        process_values["pumpP101Status"] = True
        process_values["blowerStatus"] = True
        process_values["mixerM101Status"] = True
        process_values["uvSystemStatus"] = True
        return jsonify({"status": "success", "message": "System started"})
    
    elif action == "stop":
        process_values["systemRunning"] = False
        process_values["pumpP101Status"] = False
        process_values["pumpP102Status"] = False
        process_values["blowerStatus"] = False
        process_values["mixerM101Status"] = False
        process_values["mixerM102Status"] = False
        process_values["uvSystemStatus"] = False
        return jsonify({"status": "success", "message": "System stopped"})
    
    elif action == "emergency_stop":
        process_values["systemRunning"] = False
        process_values["pumpP101Status"] = False
        process_values["pumpP102Status"] = False
        process_values["blowerStatus"] = False
        process_values["mixerM101Status"] = False
        process_values["mixerM102Status"] = False
        process_values["uvSystemStatus"] = False
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        process_values["alarms"].append({
            "time": timestamp,
            "message": "EMERGENCY STOP ACTIVATED",
            "severity": "critical"
        })
        return jsonify({"status": "success", "message": "Emergency stop activated"})
    
    elif action == "toggle_auto":
        process_values["autoMode"] = not process_values["autoMode"]
        return jsonify({
            "status": "success", 
            "message": f"System switched to {process_values['autoMode'] and 'auto' or 'manual'} mode"
        })
    
    elif action == "toggle_maintenance":
        process_values["maintenanceMode"] = not process_values["maintenanceMode"]
        return jsonify({
            "status": "success", 
            "message": f"Maintenance mode {process_values['maintenanceMode'] and 'activated' or 'deactivated'}"
        })
    
    elif action == "toggle_storm":
        process_values["stormMode"] = not process_values["stormMode"]
        return jsonify({
            "status": "success", 
            "message": f"Storm mode {process_values['stormMode'] and 'activated' or 'deactivated'}"
        })
    
    elif action == "acknowledge_alarms":
        process_values["alarms"] = []
        return jsonify({"status": "success", "message": "Alarms acknowledged"})
    
    else:
        return jsonify({"status": "error", "message": f"Unknown action: {action}"})

# Serve static files (CSS, JS, etc.)
@app.route('/<path:path>')
def static_files(path):
    return send_from_directory(os.path.dirname(os.path.abspath(__file__)), path)

if __name__ == '__main__':
    init_historical_data()
    print("Starting Wastewater Treatment Plant Web HMI Server...")
    print("Web HMI available at: http://127.0.0.1:5000")
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=True)
