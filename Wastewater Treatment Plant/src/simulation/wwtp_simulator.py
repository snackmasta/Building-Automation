#!/usr/bin/env python3
"""
Wastewater Treatment Plant Simulator
Comprehensive wastewater treatment process simulator
Author: PLC Control System
Date: June 8, 2025
"""

import time
import random
import math
import threading
import socket
import json
import datetime
import configparser
import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

class WastewaterTreatmentSimulator:
    def __init__(self):
        self.running = True
        self.simulation_speed = 1.0
        self.host = '127.0.0.1'
        self.port = 9000
        
        print(f"Starting Wastewater Treatment Plant Simulator")
        print(f"Simulation server running on {self.host}:{self.port}")
        print("Press Ctrl+C to stop the simulator")
        
        # Initialize process variables
        self.init_process_vars()
        
        # Start simulation thread
        self.sim_thread = threading.Thread(target=self.run_simulation)
        self.sim_thread.daemon = True
        self.sim_thread.start()
        
        # Data logging
        self.data_log = []
        self.max_log_entries = 1000
        
        # Load configuration
        self.load_config()
        
        # Start communication server
        self.start_server()
    
    def load_config(self):
        """Load configuration from file"""
        try:
            config_path = os.path.join(os.path.dirname(__file__), '..', '..', 'config', 'wwtp_config.ini')
            self.config = configparser.ConfigParser()
            if os.path.exists(config_path):
                self.config.read(config_path)
        except Exception as e:
            print(f"Warning: Could not load configuration: {e}")
            self.config = configparser.ConfigParser()
    
    def init_process_vars(self):
        """Initialize process variables"""
        # System status
        self.system_running = False
        self.emergency_stop = False
        self.auto_mode = True
        self.maintenance_mode = False
        self.storm_mode = False
        self.alarm_active = False
        
        # Process variables
        self.tank_level_1 = 2.5  # Primary tank level (m)
        self.tank_level_2 = 1.8  # Secondary tank level (m)
        self.flow_rate = 300.0   # Flow rate (m³/hr)
        self.ph_value = 7.2      # pH
        self.dissolved_oxygen = 5.5  # DO (mg/L)
        self.turbidity = 35.0    # Turbidity (NTU)
        self.chlorine = 2.3      # Chlorine (mg/L)
        self.temperature = 18.5  # Temperature (°C)
        self.cod_value = 180.0   # Chemical Oxygen Demand (mg/L)
        self.bod_value = 120.0   # Biological Oxygen Demand (mg/L)
        self.tss_value = 75.0    # Total Suspended Solids (mg/L)
        self.phosphorus = 8.5    # Phosphorus (mg/L)
        self.nitrogen = 25.0     # Nitrogen (mg/L)
        
        # Equipment status
        self.pump_p101_status = False  # Intake pump
        self.pump_p102_status = False  # Transfer pump
        self.pump_p103_status = False  # Recirculation pump
        self.mixer_m101_status = False # Primary mixer
        self.mixer_m102_status = False # Secondary mixer
        self.blower_b101_status = False # Aeration blower
        self.blower_b102_status = False # Secondary blower
        self.uv_system_status = False  # UV disinfection
        self.screen_forward = False    # Bar screen forward
        self.screen_reverse = False    # Bar screen reverse
        self.clarifier_mechanism = False  # Clarifier mechanism
        self.thickener_mechanism = False  # Sludge thickener
        
        # Performance metrics
        self.treatment_efficiency = 95.0  # %
        self.energy_consumption = 175.0   # kW
        self.total_flow_today = 2568.0    # m³
        self.chemical_usage = 120.5       # L
        self.sludge_production = 45.2     # m³/day
        self.removal_efficiency_cod = 94.0  # %
        self.removal_efficiency_bod = 96.0  # %
        self.removal_efficiency_tss = 98.0  # %
        
        # Advanced process parameters
        self.mlss_concentration = 3200.0  # Mixed Liquor Suspended Solids (mg/L)
        self.svi_value = 120.0           # Sludge Volume Index (mL/g)
        self.return_sludge_rate = 75.0   # % of influent flow
        self.waste_sludge_rate = 1.2     # % of influent flow
        self.detention_time = 8.5        # hours
        self.food_to_microorganism = 0.25 # F/M ratio
        
        # Environmental parameters
        self.ambient_temperature = 22.0   # °C
        self.wind_speed = 5.2            # m/s
        self.humidity = 65.0             # %
        self.atmospheric_pressure = 1013.25  # mbar
        
        # Alarm thresholds
        self.ph_alarm_low = 6.0
        self.ph_alarm_high = 9.0
        self.do_alarm_low = 2.0
        self.turbidity_alarm_high = 50.0
        self.flow_alarm_low = 200.0
        self.flow_alarm_high = 500.0
    
    def run_simulation(self):
        """Main simulation loop"""
        last_time = time.time()
        
        while self.running:
            current_time = time.time()
            dt = current_time - last_time
            
            if self.system_running and not self.emergency_stop:
                self.update_process_variables(dt)
                self.update_equipment_status()
                self.check_alarms()
                self.calculate_performance_metrics(dt)
                self.update_biological_process(dt)
                
            self.log_data()
            last_time = current_time
            time.sleep(1.0)
    
    def update_process_variables(self, dt):
        """Update process variables with realistic dynamics"""
        # Tank level dynamics
        if self.pump_p101_status:
            # Intake pump running - tank levels increase
            self.tank_level_1 += random.uniform(0.01, 0.05) * dt
        else:
            # No intake - levels decrease due to treatment flow
            self.tank_level_1 += random.uniform(-0.03, 0.01) * dt
        
        self.tank_level_1 = max(0.1, min(5.0, self.tank_level_1))
        
        # Secondary tank influenced by treatment process
        if self.mixer_m101_status:
            self.tank_level_2 += random.uniform(-0.02, 0.02) * dt
        else:
            self.tank_level_2 += random.uniform(-0.05, 0.01) * dt
        
        self.tank_level_2 = max(0.1, min(4.5, self.tank_level_2))
        
        # Flow rate dynamics
        if self.pump_p101_status and self.pump_p102_status:
            target_flow = 350.0 if not self.storm_mode else 500.0
            self.flow_rate += (target_flow - self.flow_rate) * 0.1 * dt
            self.flow_rate += random.uniform(-5, 5) * dt
        else:
            self.flow_rate *= (1.0 - 0.05 * dt)  # Flow decreases when pumps off
        
        self.flow_rate = max(0, min(600, self.flow_rate))
        
        # pH dynamics
        if self.system_running:
            # pH influenced by chemical dosing and biological activity
            ph_change = 0.0
            if self.flow_rate > 0:
                # Biological activity tends to lower pH
                ph_change -= 0.01 * dt
                
                # Chemical correction (simulated automatic dosing)
                if self.ph_value < 6.8:
                    ph_change += 0.02 * dt  # Alkali dosing
                elif self.ph_value > 7.8:
                    ph_change -= 0.02 * dt  # Acid dosing
            
            self.ph_value += ph_change + random.uniform(-0.02, 0.02) * dt
            self.ph_value = max(5.5, min(9.5, self.ph_value))
        
        # Dissolved oxygen dynamics
        if self.blower_b101_status or self.blower_b102_status:
            # Aeration increases DO
            target_do = 6.0 if self.blower_b101_status and self.blower_b102_status else 4.0
            self.dissolved_oxygen += (target_do - self.dissolved_oxygen) * 0.05 * dt
        else:
            # DO decreases due to biological consumption
            self.dissolved_oxygen -= 0.1 * dt
        
        self.dissolved_oxygen += random.uniform(-0.05, 0.05) * dt
        self.dissolved_oxygen = max(0.5, min(10.0, self.dissolved_oxygen))
        
        # Turbidity influenced by treatment efficiency
        if self.clarifier_mechanism:
            # Clarifier operating - turbidity decreases
            self.turbidity -= 2.0 * dt
        else:
            # No clarification - turbidity increases
            self.turbidity += 1.0 * dt
        
        self.turbidity += random.uniform(-1.0, 1.0) * dt
        self.turbidity = max(5.0, min(100.0, self.turbidity))
        
        # Temperature influenced by ambient and biological heat
        temp_change = (self.ambient_temperature - self.temperature) * 0.001 * dt
        if self.blower_b101_status or self.blower_b102_status:
            temp_change += 0.01 * dt  # Aeration adds heat
        
        self.temperature += temp_change + random.uniform(-0.05, 0.05) * dt
        self.temperature = max(5.0, min(35.0, self.temperature))
        
        # Advanced parameters
        self.update_advanced_parameters(dt)
    
    def update_advanced_parameters(self, dt):
        """Update advanced process parameters"""
        # COD reduction through biological treatment
        if self.dissolved_oxygen > 2.0 and self.mixer_m101_status:
            cod_reduction_rate = 0.1 * (self.dissolved_oxygen / 6.0) * dt
            self.cod_value *= (1.0 - cod_reduction_rate)
        
        # BOD reduction (faster than COD)
        if self.dissolved_oxygen > 1.0:
            bod_reduction_rate = 0.15 * dt
            self.bod_value *= (1.0 - bod_reduction_rate)
        
        # TSS removal through settling
        if self.clarifier_mechanism:
            tss_removal_rate = 0.2 * dt
            self.tss_value *= (1.0 - tss_removal_rate)
        
        # MLSS concentration
        if self.system_running:
            # Growth and wasting balance
            growth_rate = 0.05 * (self.food_to_microorganism / 0.3) * dt
            wasting_rate = (self.waste_sludge_rate / 100.0) * 0.1 * dt
            mlss_change = self.mlss_concentration * (growth_rate - wasting_rate)
            self.mlss_concentration += mlss_change + random.uniform(-10, 10) * dt
            self.mlss_concentration = max(1500, min(5000, self.mlss_concentration))
        
        # SVI calculation (inverse relationship with settling)
        settling_factor = 1.0 if self.clarifier_mechanism else 1.2
        self.svi_value = 150.0 * settling_factor + random.uniform(-5, 5)
        self.svi_value = max(80, min(200, self.svi_value))
        
        # F/M ratio calculation
        if self.mlss_concentration > 0:
            self.food_to_microorganism = (self.bod_value * self.flow_rate) / (self.mlss_concentration * 1000)
        
        # Add noise to all parameters
        self.cod_value = max(50, min(300, self.cod_value + random.uniform(-2, 2)))
        self.bod_value = max(20, min(200, self.bod_value + random.uniform(-1, 1)))
        self.tss_value = max(10, min(150, self.tss_value + random.uniform(-1, 1)))
        self.phosphorus = max(2, min(15, self.phosphorus + random.uniform(-0.1, 0.1)))
        self.nitrogen = max(10, min(40, self.nitrogen + random.uniform(-0.2, 0.2)))
    
    def update_equipment_status(self):
        """Update equipment status with realistic behavior"""
        if self.system_running and not self.emergency_stop:
            # Pump cycling behavior
            if random.random() < 0.001:  # 0.1% chance per second
                self.pump_p101_status = not self.pump_p101_status
            
            if random.random() < 0.001:
                self.pump_p102_status = not self.pump_p102_status
            
            # Mixer operation based on process needs
            if self.tank_level_1 > 1.0:
                self.mixer_m101_status = True
            elif self.tank_level_1 < 0.5:
                self.mixer_m101_status = False
            
            # Blower operation based on DO setpoint
            if self.dissolved_oxygen < 3.0:
                self.blower_b101_status = True
                if self.dissolved_oxygen < 2.0:
                    self.blower_b102_status = True
            elif self.dissolved_oxygen > 7.0:
                self.blower_b101_status = False
                self.blower_b102_status = False
            
            # Clarifier mechanism
            if self.flow_rate > 100:
                self.clarifier_mechanism = True
            else:
                self.clarifier_mechanism = False
        else:
            # System stopped - turn off equipment
            self.pump_p101_status = False
            self.pump_p102_status = False
            self.mixer_m101_status = False
            self.mixer_m102_status = False
            self.blower_b101_status = False
            self.blower_b102_status = False
            self.clarifier_mechanism = False
    
    def check_alarms(self):
        """Check for alarm conditions"""
        alarm_conditions = []
        
        # pH alarms
        if self.ph_value < self.ph_alarm_low or self.ph_value > self.ph_alarm_high:
            alarm_conditions.append("pH out of range")
        
        # DO alarms
        if self.dissolved_oxygen < self.do_alarm_low:
            alarm_conditions.append("Low dissolved oxygen")
        
        # Turbidity alarm
        if self.turbidity > self.turbidity_alarm_high:
            alarm_conditions.append("High turbidity")
        
        # Flow alarms
        if self.flow_rate < self.flow_alarm_low:
            alarm_conditions.append("Low flow rate")
        elif self.flow_rate > self.flow_alarm_high:
            alarm_conditions.append("High flow rate")
        
        # Tank level alarms
        if self.tank_level_1 < 0.2 or self.tank_level_1 > 4.8:
            alarm_conditions.append("Tank 1 level alarm")
        
        if self.tank_level_2 < 0.2 or self.tank_level_2 > 4.2:
            alarm_conditions.append("Tank 2 level alarm")
        
        # Set alarm status
        self.alarm_active = len(alarm_conditions) > 0
        self.active_alarms = alarm_conditions
    
    def calculate_performance_metrics(self, dt):
        """Calculate treatment performance metrics"""
        # Treatment efficiency based on various factors
        base_efficiency = 90.0
        
        # DO impact on efficiency
        if self.dissolved_oxygen > 2.0:
            do_bonus = min(5.0, (self.dissolved_oxygen - 2.0) * 2.0)
        else:
            do_bonus = -10.0  # Poor aeration hurts efficiency
        
        # pH impact
        if 6.5 <= self.ph_value <= 8.0:
            ph_bonus = 2.0
        else:
            ph_bonus = -5.0
        
        # Mixing impact
        mixing_bonus = 3.0 if self.mixer_m101_status else -2.0
        
        self.treatment_efficiency = base_efficiency + do_bonus + ph_bonus + mixing_bonus
        self.treatment_efficiency += random.uniform(-1, 1)
        self.treatment_efficiency = max(70, min(99, self.treatment_efficiency))
        
        # Energy consumption calculation
        base_consumption = 150.0  # kW
        
        # Add consumption from equipment
        if self.pump_p101_status:
            base_consumption += 25.0
        if self.pump_p102_status:
            base_consumption += 30.0
        if self.pump_p103_status:
            base_consumption += 20.0
        if self.blower_b101_status:
            base_consumption += 45.0
        if self.blower_b102_status:
            base_consumption += 45.0
        if self.mixer_m101_status:
            base_consumption += 15.0
        if self.mixer_m102_status:
            base_consumption += 15.0
        if self.uv_system_status:
            base_consumption += 35.0
        
        # Flow-dependent consumption
        flow_consumption = self.flow_rate * 0.1
        
        self.energy_consumption = base_consumption + flow_consumption + random.uniform(-5, 5)
        
        # Update totals
        self.total_flow_today += self.flow_rate * dt / 3600.0  # Convert to m³
        
        # Chemical usage (pH correction)
        if abs(self.ph_value - 7.0) > 0.5:
            self.chemical_usage += abs(self.ph_value - 7.0) * 0.01 * dt
        
        # Sludge production
        sludge_rate = self.flow_rate * 0.002 * (self.tss_value / 100.0)  # m³/hr
        self.sludge_production += sludge_rate * dt / 24.0  # Convert to daily rate
        
        # Removal efficiencies
        self.removal_efficiency_cod = min(99, 85 + (self.treatment_efficiency - 90) * 0.5)
        self.removal_efficiency_bod = min(99, 90 + (self.treatment_efficiency - 90) * 0.3)
        self.removal_efficiency_tss = min(99, 95 + (self.treatment_efficiency - 90) * 0.2)
    
    def update_biological_process(self, dt):
        """Update biological treatment process parameters"""
        if self.system_running:
            # Biological growth and substrate utilization
            if self.dissolved_oxygen > 0.5:  # Aerobic conditions
                # Substrate utilization (BOD/COD reduction)
                utilization_rate = 0.8 * (self.dissolved_oxygen / 6.0) * dt
                self.bod_value *= (1.0 - utilization_rate * 0.01)
                self.cod_value *= (1.0 - utilization_rate * 0.008)
                
                # Nitrification (nitrogen removal)
                if self.dissolved_oxygen > 2.0:
                    nitrification_rate = 0.05 * dt
                    self.nitrogen *= (1.0 - nitrification_rate)
            
            # Phosphorus removal (biological and chemical)
            if self.dissolved_oxygen > 1.0:
                p_removal_rate = 0.03 * dt
                self.phosphorus *= (1.0 - p_removal_rate)
            
            # Maintain minimum values
            self.bod_value = max(10, self.bod_value)
            self.cod_value = max(30, self.cod_value)
            self.nitrogen = max(5, self.nitrogen)
            self.phosphorus = max(1, self.phosphorus)
    
    def log_data(self):
        """Log current data point"""
        data_point = {
            'timestamp': datetime.datetime.now().isoformat(),
            'system_running': self.system_running,
            'flow_rate': self.flow_rate,
            'ph_value': self.ph_value,
            'dissolved_oxygen': self.dissolved_oxygen,
            'turbidity': self.turbidity,
            'temperature': self.temperature,
            'treatment_efficiency': self.treatment_efficiency,
            'energy_consumption': self.energy_consumption,
            'cod_value': self.cod_value,
            'bod_value': self.bod_value,
            'tss_value': self.tss_value,
            'mlss_concentration': self.mlss_concentration,
            'tank_level_1': self.tank_level_1,
            'tank_level_2': self.tank_level_2,
            'alarm_active': self.alarm_active
        }
        
        self.data_log.append(data_point)
        
        # Limit log size
        if len(self.data_log) > self.max_log_entries:
            self.data_log.pop(0)
    
    def start_server(self):
        """Start a socket server to provide data to HMI and other clients"""
        def server_thread():
            try:
                server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                server_socket.bind((self.host, self.port))
                server_socket.listen(5)
                server_socket.settimeout(1) # Add a timeout to allow checking self.running
                
                print(f"Communication server started on {self.host}:{self.port}")
                
                while self.running:
                    try:
                        client_socket, addr = server_socket.accept()
                        with client_socket: # Use with statement to ensure socket is closed
                            print(f"Connection from {addr}")
                            data = client_socket.recv(1024).decode('utf-8')
                            if data:
                                try:
                                    command = json.loads(data)
                                    print(f"Received command: {command}")
                                    response = self.process_command(command)
                                except json.JSONDecodeError:
                                    response = {'status': 'error', 'message': 'Invalid JSON command'}
                                except Exception as e:
                                    print(f"Error processing command: {str(e)}")
                                    response = {'status': 'error', 'message': f'Error processing command: {str(e)}'}
                                
                                client_socket.sendall(json.dumps(response).encode('utf-8'))
                            # client_socket.close() # No longer needed due to 'with' statement
                    except socket.timeout:
                        continue # Allows checking self.running periodically
                    except Exception as e:
                        print(f"Server error: {e}")
                        
            except Exception as e:
                print(f"Server startup error: {e}")
            finally:
                try:
                    server_socket.close()
                except:
                    pass
        
        server_thread_obj = threading.Thread(target=server_thread)
        server_thread_obj.daemon = True
        server_thread_obj.start()
    
    def process_command(self, command):
        """Process commands from clients"""
        cmd_type = command.get('type', '')
        
        if cmd_type == 'get_data':
            return {
                'status': 'success',
                'data': {
                    'system_running': self.system_running,
                    'emergency_stop': self.emergency_stop,
                    'auto_mode': self.auto_mode,
                    'maintenance_mode': self.maintenance_mode,
                    'storm_mode': self.storm_mode,
                    'alarm_active': self.alarm_active,
                    'tank_level_1': self.tank_level_1,
                    'tank_level_2': self.tank_level_2,
                    'flow_rate': self.flow_rate,
                    'ph_value': self.ph_value,
                    'dissolved_oxygen': self.dissolved_oxygen,
                    'turbidity': self.turbidity,
                    'chlorine': self.chlorine,
                    'temperature': self.temperature,
                    'cod_value': self.cod_value,
                    'bod_value': self.bod_value,
                    'tss_value': self.tss_value,
                    'phosphorus': self.phosphorus,
                    'nitrogen': self.nitrogen,
                    'mlss_concentration': self.mlss_concentration,
                    'svi_value': self.svi_value,
                    'pump_p101_status': self.pump_p101_status,
                    'pump_p102_status': self.pump_p102_status,
                    'pump_p103_status': self.pump_p103_status,
                    'mixer_m101_status': self.mixer_m101_status,
                    'mixer_m102_status': self.mixer_m102_status,
                    'blower_b101_status': self.blower_b101_status,
                    'blower_b102_status': self.blower_b102_status,
                    'uv_system_status': self.uv_system_status,
                    'treatment_efficiency': self.treatment_efficiency,
                    'energy_consumption': self.energy_consumption,
                    'total_flow_today': self.total_flow_today,
                    'chemical_usage': self.chemical_usage,
                    'sludge_production': self.sludge_production,
                    'removal_efficiency_cod': self.removal_efficiency_cod,
                    'removal_efficiency_bod': self.removal_efficiency_bod,
                    'removal_efficiency_tss': self.removal_efficiency_tss,
                    'timestamp': datetime.datetime.now().isoformat()
                }
            }
        
        elif cmd_type == 'set_control':
            control = command.get('control', {})
            
            # Update system status
            if 'system_running' in control:
                self.system_running = bool(control['system_running'])
            
            if 'emergency_stop' in control:
                self.emergency_stop = bool(control['emergency_stop'])
                if self.emergency_stop:
                    # Emergency stop should halt system operations and equipment
                    self.system_running = False
                    self.pump_p101_status = False
                    self.pump_p102_status = False
                    self.pump_p103_status = False
                    self.mixer_m101_status = False
                    self.mixer_m102_status = False
                    self.blower_b101_status = False
                    self.blower_b102_status = False
                    self.uv_system_status = False
                    self.clarifier_mechanism = False
                    self.thickener_mechanism = False
                    print("EMERGENCY STOP ACTIVATED: All critical systems stopped.")
            
            if 'auto_mode' in control:
                self.auto_mode = bool(control['auto_mode'])
            
            if 'maintenance_mode' in control:
                self.maintenance_mode = bool(control['maintenance_mode'])
            
            if 'storm_mode' in control:
                self.storm_mode = bool(control['storm_mode'])
            
            # Update equipment status (if in manual mode)
            if not self.auto_mode:
                if 'pump_p101_status' in control:
                    self.pump_p101_status = bool(control['pump_p101_status'])
                if 'pump_p102_status' in control:
                    self.pump_p102_status = bool(control['pump_p102_status'])
                if 'pump_p103_status' in control:
                    self.pump_p103_status = bool(control['pump_p103_status'])
                if 'mixer_m101_status' in control:
                    self.mixer_m101_status = bool(control['mixer_m101_status'])
                if 'mixer_m102_status' in control:
                    self.mixer_m102_status = bool(control['mixer_m102_status'])
                if 'blower_b101_status' in control:
                    self.blower_b101_status = bool(control['blower_b101_status'])
                if 'blower_b102_status' in control:
                    self.blower_b102_status = bool(control['blower_b102_status'])
                if 'uv_system_status' in control:
                    self.uv_system_status = bool(control['uv_system_status'])
                if 'clarifier_mechanism' in control:
                    self.clarifier_mechanism = bool(control['clarifier_mechanism'])
                if 'thickener_mechanism' in control:
                    self.thickener_mechanism = bool(control['thickener_mechanism'])
            
            return {'status': 'success', 'message': 'Control updated'}
        
        elif cmd_type == 'acknowledge_alarms':
            self.alarm_active = False
            return {'status': 'success', 'message': 'Alarms acknowledged'}
        
        elif cmd_type == 'get_log':
            # Return recent log data
            recent_logs = self.data_log[-100:] if len(self.data_log) > 100 else self.data_log
            return {'status': 'success', 'data': recent_logs}
        
        else:
            return {'status': 'error', 'message': f'Unknown command: {cmd_type}'}
    
    def save_data_log(self, filename='wwtp_data_log.json'):
        """Save data log to file"""
        try:
            log_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'logs')
            os.makedirs(log_dir, exist_ok=True)
            
            filepath = os.path.join(log_dir, filename)
            with open(filepath, 'w') as f:
                json.dump(self.data_log, f, indent=4) # Properly dump JSON data
            
            print(f"Data log saved to {filepath}")
            return True
        except Exception as e:
            print(f"Error saving data log: {e}")
            return False
    
    def stop_simulation(self):
        """Stop the simulation"""
        print("Stopping wastewater treatment simulator...")
        self.running = False
        self.save_data_log()


class WastewaterTreatmentGUI:
    """GUI for the wastewater treatment simulator"""
    
    def __init__(self, simulator):
        self.simulator = simulator
        self.root = tk.Tk()
        self.root.title("Wastewater Treatment Plant Simulator")
        self.root.geometry("1400x900")
        
        # Colors
        self.bg_color = "#f0f0f0"
        self.header_color = "#2c3e50"
        self.accent_color = "#3498db"
        self.alarm_color = "#e74c3c"
        self.ok_color = "#2ecc71"
        
        self.create_interface()
        self.update_display()
    
    def create_interface(self):
        """Create the main interface"""
        # Main frame
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Create tabs
        self.create_overview_tab()
        self.create_process_tab()
        self.create_equipment_tab()
        self.create_quality_tab()
        self.create_trends_tab()
        self.create_control_tab()
    
    def create_overview_tab(self):
        """Create system overview tab"""
        overview_frame = ttk.Frame(self.notebook)
        self.notebook.add(overview_frame, text="System Overview")
        
        # Status indicators
        status_frame = ttk.LabelFrame(overview_frame, text="System Status")
        status_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.status_labels = {}
        status_items = [
            ('System Running', 'system_running'),
            ('Emergency Stop', 'emergency_stop'),
            ('Auto Mode', 'auto_mode'),
            ('Maintenance Mode', 'maintenance_mode'),
            ('Storm Mode', 'storm_mode'),
            ('Alarms Active', 'alarm_active')
        ]
        
        for i, (label, key) in enumerate(status_items):
            row = i // 3
            col = i % 3
            ttk.Label(status_frame, text=f"{label}:").grid(row=row*2, column=col*2, sticky=tk.W, padx=5, pady=2)
            self.status_labels[key] = ttk.Label(status_frame, text="Unknown", foreground="gray")
            self.status_labels[key].grid(row=row*2+1, column=col*2, sticky=tk.W, padx=5, pady=2)
        
        # Key process variables
        process_frame = ttk.LabelFrame(overview_frame, text="Key Process Variables")
        process_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.process_labels = {}
        process_items = [
            ('Flow Rate', 'flow_rate', 'm³/hr'),
            ('pH', 'ph_value', ''),
            ('DO', 'dissolved_oxygen', 'mg/L'),
            ('Turbidity', 'turbidity', 'NTU'),
            ('Temperature', 'temperature', '°C'),
            ('Treatment Efficiency', 'treatment_efficiency', '%')
        ]
        
        for i, (label, key, unit) in enumerate(process_items):
            row = i // 3
            col = i % 3
            ttk.Label(process_frame, text=f"{label}:").grid(row=row*2, column=col*2, sticky=tk.W, padx=5, pady=2)
            self.process_labels[key] = ttk.Label(process_frame, text=f"-- {unit}")
            self.process_labels[key].grid(row=row*2+1, column=col*2, sticky=tk.W, padx=5, pady=2)
    
    def create_process_tab(self):
        """Create process monitoring tab"""
        process_frame = ttk.Frame(self.notebook)
        self.notebook.add(process_frame, text="Process Parameters")
        
        # Tank levels
        tanks_frame = ttk.LabelFrame(process_frame, text="Tank Levels")
        tanks_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.tank_labels = {}
        tank_items = [
            ('Primary Tank', 'tank_level_1', 'm'),
            ('Secondary Tank', 'tank_level_2', 'm')
        ]
        
        for i, (label, key, unit) in enumerate(tank_items):
            ttk.Label(tanks_frame, text=f"{label}:").grid(row=i, column=0, sticky=tk.W, padx=5, pady=2)
            self.tank_labels[key] = ttk.Label(tanks_frame, text=f"-- {unit}")
            self.tank_labels[key].grid(row=i, column=1, sticky=tk.W, padx=5, pady=2)
        
        # Advanced parameters
        advanced_frame = ttk.LabelFrame(process_frame, text="Advanced Parameters")
        advanced_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.advanced_labels = {}
        advanced_items = [
            ('COD', 'cod_value', 'mg/L'),
            ('BOD', 'bod_value', 'mg/L'),
            ('TSS', 'tss_value', 'mg/L'),
            ('MLSS', 'mlss_concentration', 'mg/L'),
            ('SVI', 'svi_value', 'mL/g'),
            ('Phosphorus', 'phosphorus', 'mg/L'),
            ('Nitrogen', 'nitrogen', 'mg/L'),
            ('F/M Ratio', 'food_to_microorganism', '')
        ]
        
        for i, (label, key, unit) in enumerate(advanced_items):
            row = i // 4
            col = i % 4
            ttk.Label(advanced_frame, text=f"{label}:").grid(row=row*2, column=col, sticky=tk.W, padx=5, pady=2)
            self.advanced_labels[key] = ttk.Label(advanced_frame, text=f"-- {unit}")
            self.advanced_labels[key].grid(row=row*2+1, column=col, sticky=tk.W, padx=5, pady=2)
    
    def create_equipment_tab(self):
        """Create equipment status tab"""
        equipment_frame = ttk.Frame(self.notebook)
        self.notebook.add(equipment_frame, text="Equipment Status")
        
        # Pumps
        pumps_frame = ttk.LabelFrame(equipment_frame, text="Pumps")
        pumps_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.pump_labels = {}
        pump_items = [
            ('Intake Pump P101', 'pump_p101_status'),
            ('Transfer Pump P102', 'pump_p102_status'),
            ('Recirculation Pump P103', 'pump_p103_status')
        ]
        
        for i, (label, key) in enumerate(pump_items):
            ttk.Label(pumps_frame, text=f"{label}:").grid(row=i, column=0, sticky=tk.W, padx=5, pady=2)
            self.pump_labels[key] = ttk.Label(pumps_frame, text="OFF", foreground="red")
            self.pump_labels[key].grid(row=i, column=1, sticky=tk.W, padx=5, pady=2)
        
        # Blowers
        blowers_frame = ttk.LabelFrame(equipment_frame, text="Blowers")
        blowers_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.blower_labels = {}
        blower_items = [
            ('Primary Blower B101', 'blower_b101_status'),
            ('Secondary Blower B102', 'blower_b102_status')
        ]
        
        for i, (label, key) in enumerate(blower_items):
            ttk.Label(blowers_frame, text=f"{label}:").grid(row=i, column=0, sticky=tk.W, padx=5, pady=2)
            self.blower_labels[key] = ttk.Label(blowers_frame, text="OFF", foreground="red")
            self.blower_labels[key].grid(row=i, column=1, sticky=tk.W, padx=5, pady=2)
        
        # Other equipment
        other_frame = ttk.LabelFrame(equipment_frame, text="Other Equipment")
        other_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.other_labels = {}
        other_items = [
            ('Primary Mixer M101', 'mixer_m101_status'),
            ('Secondary Mixer M102', 'mixer_m102_status'),
            ('UV System', 'uv_system_status'),
            ('Clarifier Mechanism', 'clarifier_mechanism')
        ]
        
        for i, (label, key) in enumerate(other_items):
            ttk.Label(other_frame, text=f"{label}:").grid(row=i, column=0, sticky=tk.W, padx=5, pady=2)
            self.other_labels[key] = ttk.Label(other_frame, text="OFF", foreground="red")
            self.other_labels[key].grid(row=i, column=1, sticky=tk.W, padx=5, pady=2)
    
    def create_quality_tab(self):
        """Create water quality tab"""
        quality_frame = ttk.Frame(self.notebook)
        self.notebook.add(quality_frame, text="Water Quality")
        
        # Removal efficiencies
        removal_frame = ttk.LabelFrame(quality_frame, text="Removal Efficiencies")
        removal_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.removal_labels = {}
        removal_items = [
            ('COD Removal', 'removal_efficiency_cod', '%'),
            ('BOD Removal', 'removal_efficiency_bod', '%'),
            ('TSS Removal', 'removal_efficiency_tss', '%')
        ]
        
        for i, (label, key, unit) in enumerate(removal_items):
            ttk.Label(removal_frame, text=f"{label}:").grid(row=i, column=0, sticky=tk.W, padx=5, pady=2)
            self.removal_labels[key] = ttk.Label(removal_frame, text=f"-- {unit}")
            self.removal_labels[key].grid(row=i, column=1, sticky=tk.W, padx=5, pady=2)
        
        # Performance metrics
        performance_frame = ttk.LabelFrame(quality_frame, text="Performance Metrics")
        performance_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.performance_labels = {}
        performance_items = [
            ('Energy Consumption', 'energy_consumption', 'kW'),
            ('Chemical Usage', 'chemical_usage', 'L'),
            ('Sludge Production', 'sludge_production', 'm³/day'),
            ('Total Flow Today', 'total_flow_today', 'm³')
        ]
        
        for i, (label, key, unit) in enumerate(performance_items):
            ttk.Label(performance_frame, text=f"{label}:").grid(row=i, column=0, sticky=tk.W, padx=5, pady=2)
            self.performance_labels[key] = ttk.Label(performance_frame, text=f"-- {unit}")
            self.performance_labels[key].grid(row=i, column=1, sticky=tk.W, padx=5, pady=2)
    
    def create_trends_tab(self):
        """Create trends tab with plots"""
        trends_frame = ttk.Frame(self.notebook)
        self.notebook.add(trends_frame, text="Trends")
        
        # Matplotlib figure
        self.fig, ((self.ax1, self.ax2), (self.ax3, self.ax4)) = plt.subplots(2, 2, figsize=(12, 8))
        self.canvas = FigureCanvasTkAgg(self.fig, trends_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Initialize data arrays for plotting
        self.time_data = []
        self.flow_data = []
        self.ph_data = []
        self.do_data = []
        self.efficiency_data = []
        
        self.init_plots()
    
    def init_plots(self):
        """Initialize trend plots"""
        self.ax1.set_title('Flow Rate (m³/hr)')
        self.ax1.set_xlabel('Time')
        self.ax1.set_ylabel('Flow Rate')
        self.ax1.grid(True)
        
        self.ax2.set_title('pH Value')
        self.ax2.set_xlabel('Time')
        self.ax2.set_ylabel('pH')
        self.ax2.grid(True)
        
        self.ax3.set_title('Dissolved Oxygen (mg/L)')
        self.ax3.set_xlabel('Time')
        self.ax3.set_ylabel('DO (mg/L)')
        self.ax3.grid(True)
        
        self.ax4.set_title('Treatment Efficiency (%)')
        self.ax4.set_xlabel('Time')
        self.ax4.set_ylabel('Efficiency (%)')
        self.ax4.grid(True)
    
    def create_control_tab(self):
        """Create control tab"""
        control_frame = ttk.Frame(self.notebook)
        self.notebook.add(control_frame, text="Control")
        
        # System control
        system_frame = ttk.LabelFrame(control_frame, text="System Control")
        system_frame.pack(fill=tk.X, padx=5, pady=5)
        
        button_frame = ttk.Frame(system_frame)
        button_frame.pack(pady=10)
        
        ttk.Button(button_frame, text="Start System", command=self.start_system).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Stop System", command=self.stop_system).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Emergency Stop", command=self.emergency_stop).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Reset Alarms", command=self.reset_alarms).pack(side=tk.LEFT, padx=5)
        
        # Mode control
        mode_frame = ttk.LabelFrame(control_frame, text="Operating Modes")
        mode_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.auto_var = tk.BooleanVar()
        self.maintenance_var = tk.BooleanVar()
        self.storm_var = tk.BooleanVar()
        
        ttk.Checkbutton(mode_frame, text="Auto Mode", variable=self.auto_var, command=self.update_mode).pack(anchor=tk.W, padx=5, pady=2)
        ttk.Checkbutton(mode_frame, text="Maintenance Mode", variable=self.maintenance_var, command=self.update_mode).pack(anchor=tk.W, padx=5, pady=2)
        ttk.Checkbutton(mode_frame, text="Storm Mode", variable=self.storm_var, command=self.update_mode).pack(anchor=tk.W, padx=5, pady=2)
    
    def update_display(self):
        """Update all display elements"""
        try:
            # Update status indicators
            status_data = {
                'system_running': self.simulator.system_running,
                'emergency_stop': self.simulator.emergency_stop,
                'auto_mode': self.simulator.auto_mode,
                'maintenance_mode': self.simulator.maintenance_mode,
                'storm_mode': self.simulator.storm_mode,
                'alarm_active': self.simulator.alarm_active
            }
            
            for key, value in status_data.items():
                if key in self.status_labels:
                    text = "ON" if value else "OFF"
                    color = self.ok_color if (value and key != 'emergency_stop' and key != 'alarm_active') or (not value and (key == 'emergency_stop' or key == 'alarm_active')) else self.alarm_color
                    self.status_labels[key].config(text=text, foreground=color)
            
            # Update process variables
            process_data = {
                'flow_rate': f"{self.simulator.flow_rate:.1f} m³/hr",
                'ph_value': f"{self.simulator.ph_value:.2f}",
                'dissolved_oxygen': f"{self.simulator.dissolved_oxygen:.1f} mg/L",
                'turbidity': f"{self.simulator.turbidity:.1f} NTU",
                'temperature': f"{self.simulator.temperature:.1f} °C",
                'treatment_efficiency': f"{self.simulator.treatment_efficiency:.1f} %"
            }
            
            for key, text in process_data.items():
                if key in self.process_labels:
                    self.process_labels[key].config(text=text)
            
            # Update tank levels
            if hasattr(self, 'tank_labels'):
                self.tank_labels['tank_level_1'].config(text=f"{self.simulator.tank_level_1:.2f} m")
                self.tank_labels['tank_level_2'].config(text=f"{self.simulator.tank_level_2:.2f} m")
            
            # Update advanced parameters
            if hasattr(self, 'advanced_labels'):
                advanced_data = {
                    'cod_value': f"{self.simulator.cod_value:.1f} mg/L",
                    'bod_value': f"{self.simulator.bod_value:.1f} mg/L",
                    'tss_value': f"{self.simulator.tss_value:.1f} mg/L",
                    'mlss_concentration': f"{self.simulator.mlss_concentration:.0f} mg/L",
                    'svi_value': f"{self.simulator.svi_value:.1f} mL/g",
                    'phosphorus': f"{self.simulator.phosphorus:.1f} mg/L",
                    'nitrogen': f"{self.simulator.nitrogen:.1f} mg/L",
                    'food_to_microorganism': f"{self.simulator.food_to_microorganism:.3f}"
                }
                
                for key, text in advanced_data.items():
                    if key in self.advanced_labels:
                        self.advanced_labels[key].config(text=text)
            
            # Update equipment status
            if hasattr(self, 'pump_labels'):
                pump_data = {
                    'pump_p101_status': self.simulator.pump_p101_status,
                    'pump_p102_status': self.simulator.pump_p102_status,
                    'pump_p103_status': self.simulator.pump_p103_status
                }
                
                for key, status in pump_data.items():
                    if key in self.pump_labels:
                        text = "ON" if status else "OFF"
                        color = self.ok_color if status else "red"
                        self.pump_labels[key].config(text=text, foreground=color)
            
            if hasattr(self, 'blower_labels'):
                blower_data = {
                    'blower_b101_status': self.simulator.blower_b101_status,
                    'blower_b102_status': self.simulator.blower_b102_status
                }
                
                for key, status in blower_data.items():
                    if key in self.blower_labels:
                        text = "ON" if status else "OFF"
                        color = self.ok_color if status else "red"
                        self.blower_labels[key].config(text=text, foreground=color)
            
            if hasattr(self, 'other_labels'):
                other_data = {
                    'mixer_m101_status': self.simulator.mixer_m101_status,
                    'mixer_m102_status': self.simulator.mixer_m102_status,
                    'uv_system_status': self.simulator.uv_system_status,
                    'clarifier_mechanism': self.simulator.clarifier_mechanism
                }
                
                for key, status in other_data.items():
                    if key in self.other_labels:
                        text = "ON" if status else "OFF"
                        color = self.ok_color if status else "red"
                        self.other_labels[key].config(text=text, foreground=color)
            
            # Update removal efficiencies
            if hasattr(self, 'removal_labels'):
                removal_data = {
                    'removal_efficiency_cod': f"{self.simulator.removal_efficiency_cod:.1f} %",
                    'removal_efficiency_bod': f"{self.simulator.removal_efficiency_bod:.1f} %",
                    'removal_efficiency_tss': f"{self.simulator.removal_efficiency_tss:.1f} %"
                }
                
                for key, text in removal_data.items():
                    if key in self.removal_labels:
                        self.removal_labels[key].config(text=text)
            
            # Update performance metrics
            if hasattr(self, 'performance_labels'):
                performance_data = {
                    'energy_consumption': f"{self.simulator.energy_consumption:.1f} kW",
                    'chemical_usage': f"{self.simulator.chemical_usage:.1f} L",
                    'sludge_production': f"{self.simulator.sludge_production:.1f} m³/day",
                    'total_flow_today': f"{self.simulator.total_flow_today:.1f} m³"
                }
                
                for key, text in performance_data.items():
                    if key in self.performance_labels:
                        self.performance_labels[key].config(text=text)
            
            # Update control checkboxes
            if hasattr(self, 'auto_var'):
                self.auto_var.set(self.simulator.auto_mode)
                self.maintenance_var.set(self.simulator.maintenance_mode)
                self.storm_var.set(self.simulator.storm_mode)
            
            # Update trends
            self.update_trends()
            
        except Exception as e:
            print(f"Display update error: {e}")
        
        # Schedule next update
        self.root.after(1000, self.update_display)
    
    def update_trends(self):
        """Update trend plots"""
        try:
            if hasattr(self, 'canvas'):
                # Add current data point
                current_time = len(self.time_data)
                self.time_data.append(current_time)
                self.flow_data.append(self.simulator.flow_rate)
                self.ph_data.append(self.simulator.ph_value)
                self.do_data.append(self.simulator.dissolved_oxygen)
                self.efficiency_data.append(self.simulator.treatment_efficiency)
                
                # Keep only last 100 points
                max_points = 100
                if len(self.time_data) > max_points:
                    self.time_data = self.time_data[-max_points:]
                    self.flow_data = self.flow_data[-max_points:]
                    self.ph_data = self.ph_data[-max_points:]
                    self.do_data = self.do_data[-max_points:]
                    self.efficiency_data = self.efficiency_data[-max_points:]
                
                # Clear and replot
                self.ax1.clear()
                self.ax2.clear()
                self.ax3.clear()
                self.ax4.clear()
                
                if len(self.time_data) > 1:
                    self.ax1.plot(self.time_data, self.flow_data, 'b-')
                    self.ax1.set_title('Flow Rate (m³/hr)')
                    self.ax1.grid(True)
                    
                    self.ax2.plot(self.time_data, self.ph_data, 'g-')
                    self.ax2.set_title('pH Value')
                    self.ax2.grid(True)
                    
                    self.ax3.plot(self.time_data, self.do_data, 'r-')
                    self.ax3.set_title('Dissolved Oxygen (mg/L)')
                    self.ax3.grid(True)
                    
                    self.ax4.plot(self.time_data, self.efficiency_data, 'm-')
                    self.ax4.set_title('Treatment Efficiency (%)')
                    self.ax4.grid(True)
                
                self.canvas.draw()
        except Exception as e:
            print(f"Trends update error: {e}")
    
    def start_system(self):
        """Start the treatment system"""
        self.simulator.system_running = True
        self.simulator.emergency_stop = False
        messagebox.showinfo("System Control", "System started")
    
    def stop_system(self):
        """Stop the treatment system"""
        self.simulator.system_running = False
        messagebox.showinfo("System Control", "System stopped")
    
    def emergency_stop(self):
        """Emergency stop"""
        if messagebox.askyesno("Emergency Stop", "Are you sure you want to activate emergency stop?"):
            self.simulator.emergency_stop = True
            self.simulator.system_running = False
            messagebox.showwarning("Emergency Stop", "Emergency stop activated!")
    
    def reset_alarms(self):
        """Reset alarms"""
        self.simulator.alarm_active = False
        messagebox.showinfo("Alarms", "Alarms reset")
    
    def update_mode(self):
        """Update operating modes"""
        self.simulator.auto_mode = self.auto_var.get()
        self.simulator.maintenance_mode = self.maintenance_var.get()
        self.simulator.storm_mode = self.storm_var.get()
    
    def run(self):
        """Run the GUI"""
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            self.simulator.stop_simulation()


def main():
    """Main function"""
    try:
        print("Starting Wastewater Treatment Plant Simulator...")
        
        # Create and start simulator
        simulator = WastewaterTreatmentSimulator()
        
        # Create and run GUI
        gui = WastewaterTreatmentGUI(simulator)
        gui.run()
        
    except KeyboardInterrupt:
        print("\nSimulator shutting down...")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if 'simulator' in locals():
            simulator.stop_simulation()


if __name__ == "__main__":
    main()
