#!/usr/bin/env python3
"""
Water Treatment System Simulator
Seawater Desalination and Distribution System Simulator
Author: PLC Control System
Date: June 2025
"""

import time
import random
import math
import configparser
import json
from datetime import datetime
import threading
import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

class WaterTreatmentSimulator:
    def __init__(self):
        self.running = False
        self.simulation_speed = 1.0  # Real-time multiplier
        
        # Load configuration
        self.load_config()
        
        # System state variables
        self.system_state = {
            'mode': 'STOPPED',
            'running': False,
            'emergency_stop': False,
            'maintenance_mode': False,
            'auto_mode': True
        }
        
        # Tank states
        self.ground_tank = {
            'level': 50.0,      # %
            'capacity': 50000,  # L
            'volume': 25000,    # L
            'temperature': 25.0, # °C
            'inlet_flow': 0.0,  # L/min
            'outlet_flow': 0.0  # L/min
        }
        
        self.roof_tank = {
            'level': 30.0,      # %
            'capacity': 10000,  # L
            'volume': 3000,     # L
            'temperature': 25.0, # °C
            'inlet_flow': 0.0,  # L/min
            'outlet_flow': 0.0  # L/min
        }
        
        # Seawater parameters
        self.seawater = {
            'tds': 35000,       # ppm
            'temperature': 25.0, # °C
            'pressure': 1.0,    # bar
            'flow_rate': 0.0,   # L/min
            'ph': 8.1,          # pH
            'conductivity': 55000 # µS/cm
        }
        
        # Product water parameters
        self.product_water = {
            'tds': 0.0,         # ppm
            'ph': 7.0,          # pH
            'turbidity': 0.0,   # NTU
            'chlorine': 0.0,    # mg/L
            'temperature': 25.0, # °C
            'flow_rate': 0.0,   # L/min
            'conductivity': 0.0 # µS/cm
        }
        
        # RO system parameters
        self.ro_system = {
            'pressure': 0.0,        # bar
            'recovery_rate': 0.0,   # %
            'salt_rejection': 0.0,  # %
            'permeate_flow': 0.0,   # L/min
            'concentrate_flow': 0.0, # L/min
            'fouling_index': 10.0,  # %
            'cleaning_cycles': 0,
            'membrane_hours': 0.0
        }
        
        # Pump states
        self.pumps = {
            'intake': {'running': False, 'speed': 0.0, 'current': 0.0, 'hours': 0.0, 'fault': False},
            'prefilter': {'running': False, 'speed': 0.0, 'current': 0.0, 'hours': 0.0, 'fault': False},
            'ro': {'running': False, 'speed': 0.0, 'current': 0.0, 'hours': 0.0, 'fault': False},
            'booster1': {'running': False, 'speed': 0.0, 'current': 0.0, 'hours': 0.0, 'fault': False},
            'booster2': {'running': False, 'speed': 0.0, 'current': 0.0, 'hours': 0.0, 'fault': False}
        }
        
        # Valve states
        self.valves = {
            'intake': False,
            'permeate': False,
            'concentrate': False,
            'ground_tank': False,
            'roof_tank': False
        }
        
        # Treatment systems
        self.treatment = {
            'uv_sterilizer': False,
            'chlorine_dosing': False,
            'ph_dosing': False,
            'chlorine_rate': 0.0,
            'ph_dose_rate': 0.0
        }
        
        # Alarms and status
        self.alarms = {
            'emergency_stop': False,
            'water_quality': False,
            'tank_level': False,
            'pump_fault': False,
            'ro_system': False,
            'leakage': False,
            'maintenance': False
        }
        
        # Energy monitoring
        self.energy = {
            'power_consumption': 0.0,   # kW
            'energy_today': 0.0,        # kWh
            'energy_total': 1250.5,     # kWh
            'specific_energy': 0.0      # kWh/m³
        }
        
        # Production tracking
        self.production = {
            'volume_today': 0.0,        # L
            'volume_total': 250000.0,   # L
            'production_rate': 0.0,     # L/min
            'uptime_today': 0.0,        # hours
            'efficiency': 0.0           # %
        }
        
        # Distribution network
        self.distribution = {
            'pressure': 0.0,            # bar
            'flow_rate': 0.0,          # L/min
            'zones': {
                'zone1': {'pressure': 0.0, 'flow': 0.0},
                'zone2': {'pressure': 0.0, 'flow': 0.0},
                'zone3': {'pressure': 0.0, 'flow': 0.0},
                'zone4': {'pressure': 0.0, 'flow': 0.0}
            }
        }
        
        # Control inputs (from PLC simulation)
        self.control_inputs = {
            'start_button': False,
            'stop_button': False,
            'emergency_button': False,
            'maintenance_mode': False,
            'pump_speeds': {
                'intake': 0.0,
                'ro': 0.0,
                'booster1': 0.0,
                'booster2': 0.0
            },
            'valve_commands': {
                'intake': False,
                'permeate': False,
                'concentrate': False,
                'ground_tank': False,
                'roof_tank': False
            },
            'treatment_commands': {
                'uv_sterilizer': False,
                'chlorine_dosing': False,
                'ph_dosing': False,
                'chlorine_rate': 0.0,
                'ph_dose_rate': 0.0
            }
        }
        
        # Simulation parameters
        self.time_step = 1.0  # seconds
        self.simulation_time = 0.0
        self.last_update = time.time()
        
        # Data logging
        self.data_log = []
        self.max_log_entries = 1000
        
    def load_config(self):
        """Load configuration from file"""
        try:
            config = configparser.ConfigParser()
            config.read('plc_config.ini')
            
            # Load system parameters if config exists
            if 'SYSTEM' in config:
                self.simulation_speed = config.getfloat('SYSTEM', 'simulation_speed', fallback=1.0)
                
        except FileNotFoundError:
            print("Configuration file not found, using defaults")
    
    def start_simulation(self):
        """Start the simulation"""
        self.running = True
        self.simulation_thread = threading.Thread(target=self.simulation_loop)
        self.simulation_thread.daemon = True
        self.simulation_thread.start()
    
    def stop_simulation(self):
        """Stop the simulation"""
        self.running = False
    
    def simulation_loop(self):
        """Main simulation loop"""
        while self.running:
            current_time = time.time()
            dt = (current_time - self.last_update) * self.simulation_speed
            
            if dt >= self.time_step:
                self.update_simulation(dt)
                self.last_update = current_time
                
            time.sleep(0.1)
    
    def update_simulation(self, dt):
        """Update simulation state"""
        # Update system based on control inputs
        self.update_system_state()
        
        # Simulate pump operations
        self.simulate_pumps(dt)
        
        # Simulate RO process
        self.simulate_ro_process(dt)
        
        # Simulate tank levels
        self.simulate_tanks(dt)
        
        # Simulate water quality
        self.simulate_water_quality(dt)
        
        # Simulate treatment systems
        self.simulate_treatment_systems(dt)
        
        # Simulate distribution system
        self.simulate_distribution(dt)
        
        # Update energy consumption
        self.update_energy_consumption(dt)
        
        # Update production statistics
        self.update_production_stats(dt)
        
        # Generate realistic variations
        self.add_realistic_variations()
        
        # Check for alarms
        self.check_alarms()
        
        # Log data
        self.log_data()
        
        # Update simulation time
        self.simulation_time += dt
    
    def update_system_state(self):
        """Update system state based on control inputs"""
        # Emergency stop handling
        if self.control_inputs['emergency_button']:
            self.system_state['mode'] = 'ALARM'
            self.system_state['emergency_stop'] = True
            self.alarms['emergency_stop'] = True
            
            # Stop all pumps
            for pump in self.pumps.values():
                pump['running'] = False
                pump['speed'] = 0.0
        
        # Start/stop control
        if self.control_inputs['start_button'] and not self.system_state['emergency_stop']:
            if self.system_state['mode'] == 'STOPPED':
                self.system_state['mode'] = 'STARTUP'
        
        if self.control_inputs['stop_button']:
            if self.system_state['mode'] == 'RUNNING':
                self.system_state['mode'] = 'SHUTDOWN'
        
        # Update pump states based on commands
        self.pumps['intake']['running'] = self.control_inputs['pump_speeds']['intake'] > 0
        self.pumps['intake']['speed'] = self.control_inputs['pump_speeds']['intake']
        
        self.pumps['ro']['running'] = self.control_inputs['pump_speeds']['ro'] > 0
        self.pumps['ro']['speed'] = self.control_inputs['pump_speeds']['ro']
        
        self.pumps['booster1']['running'] = self.control_inputs['pump_speeds']['booster1'] > 0
        self.pumps['booster1']['speed'] = self.control_inputs['pump_speeds']['booster1']
        
        self.pumps['booster2']['running'] = self.control_inputs['pump_speeds']['booster2'] > 0
        self.pumps['booster2']['speed'] = self.control_inputs['pump_speeds']['booster2']
        
        # Update valve states
        self.valves.update(self.control_inputs['valve_commands'])
        
        # Update treatment systems
        self.treatment['uv_sterilizer'] = self.control_inputs['treatment_commands']['uv_sterilizer']
        self.treatment['chlorine_dosing'] = self.control_inputs['treatment_commands']['chlorine_dosing']
        self.treatment['ph_dosing'] = self.control_inputs['treatment_commands']['ph_dosing']
        self.treatment['chlorine_rate'] = self.control_inputs['treatment_commands']['chlorine_rate']
        self.treatment['ph_dose_rate'] = self.control_inputs['treatment_commands']['ph_dose_rate']
    
    def simulate_pumps(self, dt):
        """Simulate pump operations"""
        for pump_name, pump in self.pumps.items():
            if pump['running']:
                # Update operating hours
                pump['hours'] += dt / 3600.0  # Convert seconds to hours
                
                # Simulate motor current based on speed and load
                base_current = {'intake': 8.0, 'prefilter': 6.0, 'ro': 20.0, 
                               'booster1': 10.0, 'booster2': 10.0}.get(pump_name, 5.0)
                pump['current'] = base_current * (pump['speed'] / 100.0) * (0.8 + random.random() * 0.4)
                
                # Simulate pump faults (very low probability)
                if random.random() < 0.0001:  # 0.01% chance per update
                    pump['fault'] = True
                    pump['running'] = False
                    self.alarms['pump_fault'] = True
            else:
                pump['current'] = 0.0
    
    def simulate_ro_process(self, dt):
        """Simulate reverse osmosis process"""
        if self.pumps['ro']['running'] and self.valves['permeate']:
            # Calculate RO pressure based on pump speed
            target_pressure = 55.0 * (self.pumps['ro']['speed'] / 100.0)
            pressure_rate = 10.0  # bar/minute
            
            if self.ro_system['pressure'] < target_pressure:
                self.ro_system['pressure'] += pressure_rate * (dt / 60.0)
            else:
                self.ro_system['pressure'] = target_pressure
            
            # Calculate flows based on pressure and recovery rate
            if self.ro_system['pressure'] > 20.0:
                max_permeate_flow = 200.0  # L/min at full pressure
                pressure_factor = min(self.ro_system['pressure'] / 55.0, 1.0)
                self.ro_system['permeate_flow'] = max_permeate_flow * pressure_factor
                
                # Recovery rate typically 45% for seawater RO
                target_recovery = 45.0
                self.ro_system['recovery_rate'] = target_recovery * pressure_factor
                
                # Calculate concentrate flow
                total_feed = self.ro_system['permeate_flow'] / (self.ro_system['recovery_rate'] / 100.0)
                self.ro_system['concentrate_flow'] = total_feed - self.ro_system['permeate_flow']
                
                # Salt rejection calculation
                self.ro_system['salt_rejection'] = 98.5 - (self.ro_system['fouling_index'] / 10.0)
                
                # Update membrane hours
                self.ro_system['membrane_hours'] += dt / 3600.0
                
                # Fouling increase over time
                self.ro_system['fouling_index'] += 0.001 * dt / 3600.0
                
            else:
                self.ro_system['permeate_flow'] = 0.0
                self.ro_system['concentrate_flow'] = 0.0
                self.ro_system['recovery_rate'] = 0.0
        else:
            # RO system is off
            self.ro_system['pressure'] *= 0.95  # Pressure decay
            self.ro_system['permeate_flow'] = 0.0
            self.ro_system['concentrate_flow'] = 0.0
            self.ro_system['recovery_rate'] = 0.0
    
    def simulate_tanks(self, dt):
        """Simulate tank level changes"""
        # Ground tank simulation
        inlet_flow = 0.0
        if self.valves['ground_tank'] and self.ro_system['permeate_flow'] > 0:
            inlet_flow = self.ro_system['permeate_flow']
        
        outlet_flow = 0.0
        if self.pumps['booster1']['running'] or self.pumps['booster2']['running']:
            # Flow from ground tank to roof tank
            total_booster_speed = 0.0
            if self.pumps['booster1']['running']:
                total_booster_speed += self.pumps['booster1']['speed']
            if self.pumps['booster2']['running']:
                total_booster_speed += self.pumps['booster2']['speed']
            
            max_flow_per_pump = 150.0  # L/min per pump at 100% speed
            outlet_flow = max_flow_per_pump * (total_booster_speed / 100.0)
        
        # Update ground tank volume
        volume_change = (inlet_flow - outlet_flow) * (dt / 60.0)  # Convert to L
        self.ground_tank['volume'] += volume_change
        self.ground_tank['volume'] = max(0, min(self.ground_tank['volume'], self.ground_tank['capacity']))
        self.ground_tank['level'] = (self.ground_tank['volume'] / self.ground_tank['capacity']) * 100.0
        self.ground_tank['inlet_flow'] = inlet_flow
        self.ground_tank['outlet_flow'] = outlet_flow
        
        # Roof tank simulation
        roof_inlet_flow = 0.0
        if self.valves['roof_tank'] and outlet_flow > 0:
            roof_inlet_flow = outlet_flow * 0.95  # 5% losses in piping
        
        # Simulate distribution consumption
        distribution_demand = 80.0  # Base demand L/min
        if self.roof_tank['level'] > 10.0:  # Only if tank has water
            distribution_consumption = distribution_demand * (1.0 + 0.3 * math.sin(self.simulation_time / 3600.0))  # Daily variation
        else:
            distribution_consumption = 0.0
        
        # Update roof tank volume
        roof_volume_change = (roof_inlet_flow - distribution_consumption) * (dt / 60.0)
        self.roof_tank['volume'] += roof_volume_change
        self.roof_tank['volume'] = max(0, min(self.roof_tank['volume'], self.roof_tank['capacity']))
        self.roof_tank['level'] = (self.roof_tank['volume'] / self.roof_tank['capacity']) * 100.0
        self.roof_tank['inlet_flow'] = roof_inlet_flow
        self.roof_tank['outlet_flow'] = distribution_consumption
    
    def simulate_water_quality(self, dt):
        """Simulate water quality parameters"""
        if self.ro_system['permeate_flow'] > 0:
            # Calculate product water TDS based on salt rejection
            feed_tds = self.seawater['tds']
            rejection_rate = self.ro_system['salt_rejection'] / 100.0
            self.product_water['tds'] = feed_tds * (1.0 - rejection_rate)
            
            # pH is typically neutral after RO
            self.product_water['ph'] = 6.8 + random.random() * 0.4  # 6.8-7.2 range
            
            # Turbidity is very low after RO
            self.product_water['turbidity'] = 0.05 + random.random() * 0.05  # 0.05-0.1 NTU
            
            # Calculate conductivity from TDS
            self.product_water['conductivity'] = self.product_water['tds'] * 1.8
            
            # Flow rate
            self.product_water['flow_rate'] = self.ro_system['permeate_flow']
            
            # Temperature (slightly cooler than seawater)
            self.product_water['temperature'] = self.seawater['temperature'] - 2.0
        else:
            # No production
            self.product_water['flow_rate'] = 0.0
    
    def simulate_treatment_systems(self, dt):
        """Simulate post-treatment systems"""
        if self.treatment['chlorine_dosing'] and self.product_water['flow_rate'] > 0:
            # Chlorine dosing effect
            dose_rate = self.treatment['chlorine_rate'] / 100.0  # Convert percentage to factor
            target_chlorine = 0.5  # mg/L
            self.product_water['chlorine'] += (target_chlorine * dose_rate - self.product_water['chlorine']) * 0.1
        else:
            # Chlorine decay
            self.product_water['chlorine'] *= 0.999
        
        if self.treatment['ph_dosing'] and self.product_water['flow_rate'] > 0:
            # pH adjustment
            dose_rate = self.treatment['ph_dose_rate'] / 100.0
            target_ph = 7.2
            ph_adjustment = (target_ph - self.product_water['ph']) * dose_rate * 0.05
            self.product_water['ph'] += ph_adjustment
        
        if self.treatment['uv_sterilizer']:
            # UV sterilization reduces turbidity slightly and ensures disinfection
            self.product_water['turbidity'] *= 0.998
    
    def simulate_distribution(self, dt):
        """Simulate distribution system"""
        if self.pumps['booster1']['running'] or self.pumps['booster2']['running']:
            # Calculate distribution pressure
            total_speed = 0.0
            if self.pumps['booster1']['running']:
                total_speed += self.pumps['booster1']['speed']
            if self.pumps['booster2']['running']:
                total_speed += self.pumps['booster2']['speed']
            
            max_pressure = 4.0  # bar
            self.distribution['pressure'] = max_pressure * (total_speed / 200.0)  # Two pumps max
            
            # Distribution flow
            self.distribution['flow_rate'] = self.roof_tank['outlet_flow']
            
            # Simulate zone pressures (pressure drop through network)
            base_pressure = self.distribution['pressure']
            self.distribution['zones']['zone1']['pressure'] = base_pressure * 0.95
            self.distribution['zones']['zone2']['pressure'] = base_pressure * 0.90
            self.distribution['zones']['zone3']['pressure'] = base_pressure * 0.85
            self.distribution['zones']['zone4']['pressure'] = base_pressure * 0.80
            
            # Distribute flow among zones
            total_flow = self.distribution['flow_rate']
            self.distribution['zones']['zone1']['flow'] = total_flow * 0.3
            self.distribution['zones']['zone2']['flow'] = total_flow * 0.25
            self.distribution['zones']['zone3']['flow'] = total_flow * 0.25
            self.distribution['zones']['zone4']['flow'] = total_flow * 0.2
        else:
            self.distribution['pressure'] = 0.0
            self.distribution['flow_rate'] = 0.0
            for zone in self.distribution['zones'].values():
                zone['pressure'] = 0.0
                zone['flow'] = 0.0
    
    def update_energy_consumption(self, dt):
        """Update energy consumption calculations"""
        total_power = 0.0
        
        # Calculate power for each pump
        if self.pumps['intake']['running']:
            total_power += 2.5 * (self.pumps['intake']['speed'] / 100.0)
        
        if self.pumps['ro']['running']:
            total_power += 7.5 * (self.pumps['ro']['speed'] / 100.0)
        
        if self.pumps['booster1']['running']:
            total_power += 3.0 * (self.pumps['booster1']['speed'] / 100.0)
        
        if self.pumps['booster2']['running']:
            total_power += 3.0 * (self.pumps['booster2']['speed'] / 100.0)
        
        # Add auxiliary equipment power
        if self.treatment['uv_sterilizer']:
            total_power += 1.2
        
        if self.treatment['chlorine_dosing']:
            total_power += 0.2
        
        if self.treatment['ph_dosing']:
            total_power += 0.2
        
        self.energy['power_consumption'] = total_power
        
        # Update energy totals
        energy_increment = total_power * (dt / 3600.0)  # kWh
        self.energy['energy_today'] += energy_increment
        self.energy['energy_total'] += energy_increment
        
        # Calculate specific energy consumption
        if self.production['production_rate'] > 0:
            self.energy['specific_energy'] = total_power / (self.production['production_rate'] * 0.06)  # kWh/m³
        else:
            self.energy['specific_energy'] = 0.0
    
    def update_production_stats(self, dt):
        """Update production statistics"""
        # Production rate
        self.production['production_rate'] = self.ro_system['permeate_flow']
        
        # Volume tracking
        volume_increment = self.production['production_rate'] * (dt / 60.0)  # L
        self.production['volume_today'] += volume_increment
        self.production['volume_total'] += volume_increment
        
        # Uptime tracking
        if self.system_state['running']:
            self.production['uptime_today'] += dt / 3600.0  # hours
        
        # System efficiency calculation
        if self.pumps['ro']['running']:
            theoretical_max = 200.0  # L/min theoretical maximum
            self.production['efficiency'] = (self.production['production_rate'] / theoretical_max) * 100.0
        else:
            self.production['efficiency'] = 0.0
    
    def add_realistic_variations(self):
        """Add realistic variations to sensor readings"""
        # Add small random variations to simulate real sensor readings
        self.seawater['temperature'] += random.gauss(0, 0.1)
        self.seawater['tds'] += random.gauss(0, 100)
        
        # Ensure values stay within realistic bounds
        self.seawater['temperature'] = max(20.0, min(35.0, self.seawater['temperature']))
        self.seawater['tds'] = max(30000, min(40000, self.seawater['tds']))
        
        # Add variations to product water quality
        self.product_water['ph'] += random.gauss(0, 0.05)
        self.product_water['turbidity'] += random.gauss(0, 0.01)
        self.product_water['chlorine'] += random.gauss(0, 0.02)
        
        # Ensure product water stays within bounds
        self.product_water['ph'] = max(6.0, min(8.0, self.product_water['ph']))
        self.product_water['turbidity'] = max(0.0, min(2.0, self.product_water['turbidity']))
        self.product_water['chlorine'] = max(0.0, min(2.0, self.product_water['chlorine']))
    
    def check_alarms(self):
        """Check for alarm conditions"""
        # Tank level alarms
        self.alarms['tank_level'] = (self.ground_tank['level'] < 10.0 or 
                                    self.ground_tank['level'] > 95.0 or
                                    self.roof_tank['level'] < 5.0 or 
                                    self.roof_tank['level'] > 95.0)
        
        # Water quality alarms
        self.alarms['water_quality'] = (self.product_water['tds'] > 500.0 or
                                       self.product_water['ph'] < 6.5 or
                                       self.product_water['ph'] > 8.5 or
                                       self.product_water['turbidity'] > 1.0)
        
        # RO system alarms
        self.alarms['ro_system'] = (self.ro_system['pressure'] > 65.0 or
                                   self.ro_system['salt_rejection'] < 95.0 or
                                   self.ro_system['fouling_index'] > 80.0)
        
        # Pump fault alarms
        self.alarms['pump_fault'] = any(pump['fault'] for pump in self.pumps.values())
        
        # Maintenance alarms
        self.alarms['maintenance'] = (self.ro_system['membrane_hours'] > 17520.0 or  # 2 years
                                     any(pump['hours'] > 8760.0 for pump in self.pumps.values()) or  # 1 year
                                     self.ro_system['fouling_index'] > 70.0)
    
    def log_data(self):
        """Log current data point"""
        if len(self.data_log) >= self.max_log_entries:
            self.data_log.pop(0)  # Remove oldest entry
        
        data_point = {
            'timestamp': datetime.now().isoformat(),
            'simulation_time': self.simulation_time,
            'system_state': self.system_state.copy(),
            'ground_tank': self.ground_tank.copy(),
            'roof_tank': self.roof_tank.copy(),
            'ro_system': self.ro_system.copy(),
            'product_water': self.product_water.copy(),
            'energy': self.energy.copy(),
            'production': self.production.copy(),
            'alarms': self.alarms.copy()
        }
        
        self.data_log.append(data_point)
    
    def get_system_data(self):
        """Get current system data for external interfaces"""
        return {
            'system_state': self.system_state,
            'ground_tank': self.ground_tank,
            'roof_tank': self.roof_tank,
            'seawater': self.seawater,
            'product_water': self.product_water,
            'ro_system': self.ro_system,
            'pumps': self.pumps,
            'valves': self.valves,
            'treatment': self.treatment,
            'distribution': self.distribution,
            'energy': self.energy,
            'production': self.production,
            'alarms': self.alarms,
            'simulation_time': self.simulation_time
        }
    
    def set_control_inputs(self, inputs):
        """Set control inputs from external control system"""
        self.control_inputs.update(inputs)
    
    def save_data_log(self, filename='water_treatment_log.json'):
        """Save data log to file"""
        try:
            with open(filename, 'w') as f:
                json.dump(self.data_log, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving data log: {e}")
            return False

class WaterTreatmentGUI:
    def __init__(self, simulator):
        self.simulator = simulator
        self.root = tk.Tk()
        self.root.title("Water Treatment System Simulator")
        self.root.geometry("1400x900")
        
        # Create main frame
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        self.create_overview_tab()
        self.create_process_tab()
        self.create_quality_tab()
        self.create_alarms_tab()
        self.create_trends_tab()
        
        # Update timer
        self.update_display()
    
    def create_overview_tab(self):
        """Create system overview tab"""
        self.overview_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.overview_frame, text="System Overview")
        
        # Control buttons
        control_frame = ttk.LabelFrame(self.overview_frame, text="System Control")
        control_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(control_frame, text="Start System", 
                  command=self.start_system).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Stop System", 
                  command=self.stop_system).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Emergency Stop", 
                  command=self.emergency_stop).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Reset Alarms", 
                  command=self.reset_alarms).pack(side=tk.LEFT, padx=5)
        
        # Status displays
        status_frame = ttk.LabelFrame(self.overview_frame, text="System Status")
        status_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Create status labels
        self.status_labels = {}
        row = 0
        
        for label_text in ['System Mode:', 'Production Rate:', 'Ground Tank Level:', 
                          'Roof Tank Level:', 'RO Pressure:', 'Distribution Pressure:',
                          'Power Consumption:', 'Water Quality:', 'Active Alarms:']:
            ttk.Label(status_frame, text=label_text).grid(row=row, column=0, sticky=tk.W, padx=5, pady=2)
            self.status_labels[label_text] = ttk.Label(status_frame, text="--")
            self.status_labels[label_text].grid(row=row, column=1, sticky=tk.W, padx=20, pady=2)
            row += 1
    
    def create_process_tab(self):
        """Create process monitoring tab"""
        self.process_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.process_frame, text="Process Monitoring")
        
        # Tank levels
        tanks_frame = ttk.LabelFrame(self.process_frame, text="Tank Levels")
        tanks_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.tank_labels = {}
        for i, tank in enumerate(['Ground Tank', 'Roof Tank']):
            frame = ttk.Frame(tanks_frame)
            frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=5)
            
            ttk.Label(frame, text=tank, font=('Arial', 12, 'bold')).pack()
            self.tank_labels[f'{tank}_level'] = ttk.Label(frame, text="0%", font=('Arial', 14))
            self.tank_labels[f'{tank}_level'].pack()
            self.tank_labels[f'{tank}_volume'] = ttk.Label(frame, text="0 L")
            self.tank_labels[f'{tank}_volume'].pack()
    
    def create_quality_tab(self):
        """Create water quality monitoring tab"""
        self.quality_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.quality_frame, text="Water Quality")
        
        # Quality parameters
        quality_frame = ttk.LabelFrame(self.quality_frame, text="Product Water Quality")
        quality_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.quality_labels = {}
        parameters = [
            ('TDS (ppm):', 'tds'), ('pH:', 'ph'), ('Turbidity (NTU):', 'turbidity'),
            ('Chlorine (mg/L):', 'chlorine'), ('Temperature (°C):', 'temperature'),
            ('Conductivity (µS/cm):', 'conductivity')
        ]
        
        for i, (label_text, param) in enumerate(parameters):
            row = i // 2
            col = i % 2
            
            ttk.Label(quality_frame, text=label_text).grid(row=row, column=col*2, sticky=tk.W, padx=5, pady=5)
            self.quality_labels[param] = ttk.Label(quality_frame, text="--", font=('Arial', 12, 'bold'))
            self.quality_labels[param].grid(row=row, column=col*2+1, sticky=tk.W, padx=20, pady=5)
    
    def create_alarms_tab(self):
        """Create alarms tab"""
        self.alarms_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.alarms_frame, text="Alarms & Events")
        
        # Active alarms
        alarms_list_frame = ttk.LabelFrame(self.alarms_frame, text="Active Alarms")
        alarms_list_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.alarms_listbox = tk.Listbox(alarms_list_frame, height=10)
        self.alarms_listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        scrollbar = ttk.Scrollbar(alarms_list_frame, orient=tk.VERTICAL, command=self.alarms_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.alarms_listbox.config(yscrollcommand=scrollbar.set)
    
    def create_trends_tab(self):
        """Create trends tab with matplotlib plots"""
        self.trends_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.trends_frame, text="Trends")
        
        # Create matplotlib figure
        self.fig, ((self.ax1, self.ax2), (self.ax3, self.ax4)) = plt.subplots(2, 2, figsize=(12, 8))
        self.fig.tight_layout(pad=3.0)
        
        # Create canvas
        self.canvas = FigureCanvasTkAgg(self.fig, self.trends_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Initialize plots
        self.init_plots()
    
    def init_plots(self):
        """Initialize trend plots"""
        self.ax1.set_title('Tank Levels (%)')
        self.ax1.set_xlabel('Time')
        self.ax1.set_ylabel('Level (%)')
        self.ax1.grid(True)
        
        self.ax2.set_title('Production Rate (L/min)')
        self.ax2.set_xlabel('Time')
        self.ax2.set_ylabel('Flow Rate (L/min)')
        self.ax2.grid(True)
        
        self.ax3.set_title('Water Quality (TDS & pH)')
        self.ax3.set_xlabel('Time')
        self.ax3.set_ylabel('Value')
        self.ax3.grid(True)
        
        self.ax4.set_title('Energy Consumption (kW)')
        self.ax4.set_xlabel('Time')
        self.ax4.set_ylabel('Power (kW)')
        self.ax4.grid(True)
    
    def update_display(self):
        """Update all display elements"""
        data = self.simulator.get_system_data()
        
        # Update overview tab
        self.status_labels['System Mode:'].config(text=data['system_state']['mode'])
        self.status_labels['Production Rate:'].config(text=f"{data['production']['production_rate']:.1f} L/min")
        self.status_labels['Ground Tank Level:'].config(text=f"{data['ground_tank']['level']:.1f}%")
        self.status_labels['Roof Tank Level:'].config(text=f"{data['roof_tank']['level']:.1f}%")
        self.status_labels['RO Pressure:'].config(text=f"{data['ro_system']['pressure']:.1f} bar")
        self.status_labels['Distribution Pressure:'].config(text=f"{data['distribution']['pressure']:.1f} bar")
        self.status_labels['Power Consumption:'].config(text=f"{data['energy']['power_consumption']:.1f} kW")
        
        # Water quality status
        quality_ok = not data['alarms']['water_quality']
        quality_text = "OK" if quality_ok else "ALARM"
        quality_color = "green" if quality_ok else "red"
        self.status_labels['Water Quality:'].config(text=quality_text, foreground=quality_color)
        
        # Active alarms count
        active_alarms = sum(1 for alarm in data['alarms'].values() if alarm)
        self.status_labels['Active Alarms:'].config(text=str(active_alarms))
        
        # Update process tab
        self.tank_labels['Ground Tank_level'].config(text=f"{data['ground_tank']['level']:.1f}%")
        self.tank_labels['Ground Tank_volume'].config(text=f"{data['ground_tank']['volume']:.0f} L")
        self.tank_labels['Roof Tank_level'].config(text=f"{data['roof_tank']['level']:.1f}%")
        self.tank_labels['Roof Tank_volume'].config(text=f"{data['roof_tank']['volume']:.0f} L")
        
        # Update quality tab
        self.quality_labels['tds'].config(text=f"{data['product_water']['tds']:.0f}")
        self.quality_labels['ph'].config(text=f"{data['product_water']['ph']:.2f}")
        self.quality_labels['turbidity'].config(text=f"{data['product_water']['turbidity']:.2f}")
        self.quality_labels['chlorine'].config(text=f"{data['product_water']['chlorine']:.2f}")
        self.quality_labels['temperature'].config(text=f"{data['product_water']['temperature']:.1f}")
        self.quality_labels['conductivity'].config(text=f"{data['product_water']['conductivity']:.0f}")
        
        # Update alarms tab
        self.update_alarms_list(data['alarms'])
        
        # Update trends
        self.update_trends()
        
        # Schedule next update
        self.root.after(1000, self.update_display)
    
    def update_alarms_list(self, alarms):
        """Update alarms listbox"""
        self.alarms_listbox.delete(0, tk.END)
        
        alarm_messages = {
            'emergency_stop': 'EMERGENCY STOP ACTIVATED',
            'water_quality': 'Water Quality Out of Specification',
            'tank_level': 'Tank Level Alarm',
            'pump_fault': 'Pump Fault Detected',
            'ro_system': 'RO System Alarm',
            'leakage': 'Water Leakage Detected',
            'maintenance': 'Maintenance Required'
        }
        
        for alarm_key, active in alarms.items():
            if active and alarm_key in alarm_messages:
                timestamp = datetime.now().strftime("%H:%M:%S")
                message = f"[{timestamp}] {alarm_messages[alarm_key]}"
                self.alarms_listbox.insert(tk.END, message)
    
    def update_trends(self):
        """Update trend plots"""
        if len(self.simulator.data_log) < 2:
            return
        
        # Get last 50 data points
        recent_data = self.simulator.data_log[-50:]
        times = [i for i in range(len(recent_data))]
        
        # Clear previous plots
        for ax in [self.ax1, self.ax2, self.ax3, self.ax4]:
            ax.clear()
        
        # Tank levels plot
        ground_levels = [d['ground_tank']['level'] for d in recent_data]
        roof_levels = [d['roof_tank']['level'] for d in recent_data]
        
        self.ax1.plot(times, ground_levels, label='Ground Tank', color='blue')
        self.ax1.plot(times, roof_levels, label='Roof Tank', color='red')
        self.ax1.set_title('Tank Levels (%)')
        self.ax1.set_ylabel('Level (%)')
        self.ax1.legend()
        self.ax1.grid(True)
        
        # Production rate plot
        production_rates = [d['production']['production_rate'] for d in recent_data]
        
        self.ax2.plot(times, production_rates, color='green')
        self.ax2.set_title('Production Rate (L/min)')
        self.ax2.set_ylabel('Flow Rate (L/min)')
        self.ax2.grid(True)
          # Water quality plot
        tds_values = [d['product_water']['tds'] for d in recent_data]
        ph_values = [d['product_water']['ph'] * 100 for d in recent_data]  # Scale pH for visibility
        
        self.ax3.plot(times, tds_values, label='TDS (ppm)', color='orange')
        self.ax3.plot(times, ph_values, label='pH x100', color='purple')
        self.ax3.set_title('Water Quality')
        self.ax3.set_ylabel('Value')
        self.ax3.legend()
        self.ax3.grid(True)
        
        # Energy consumption plot
        power_values = [d['energy']['power_consumption'] for d in recent_data]
        self.ax4.plot(times, power_values, color='red')
        self.ax4.set_title('Energy Consumption (kW)')
        self.ax4.set_ylabel('Power (kW)')
        self.ax4.grid(True)
        
        # Refresh canvas
        self.canvas.draw()
    
    def start_system(self):
        """Start the water treatment system"""
        self.simulator.control_inputs['start_button'] = True
        self.root.after(100, lambda: self.simulator.control_inputs.update({'start_button': False}))
    
    def stop_system(self):
        """Stop the water treatment system"""
        self.simulator.control_inputs['stop_button'] = True
        self.root.after(100, lambda: self.simulator.control_inputs.update({'stop_button': False}))
    
    def emergency_stop(self):
        """Activate emergency stop"""
        result = messagebox.askyesno("Emergency Stop", "Are you sure you want to activate emergency stop?")
        if result:
            self.simulator.control_inputs['emergency_button'] = True
    
    def reset_alarms(self):
        """Reset all alarms"""
        self.simulator.control_inputs['emergency_button'] = False
        for alarm in self.simulator.alarms:
            self.simulator.alarms[alarm] = False
        
        # Reset pump faults
        for pump in self.simulator.pumps.values():
            pump['fault'] = False
    
    def run(self):
        """Run the GUI"""
        self.root.mainloop()

def main():
    """Main function"""
    print("Starting Water Treatment System Simulator...")
    
    # Create simulator
    simulator = WaterTreatmentSimulator()
    
    # Start simulation
    simulator.start_simulation()
    
    # Create and run GUI
    gui = WaterTreatmentGUI(simulator)
    
    try:
        gui.run()
    except KeyboardInterrupt:
        print("\nSimulation stopped by user")
    finally:
        simulator.stop_simulation()
        
        # Save data log
        if simulator.save_data_log():
            print("Data log saved successfully")
        else:
            print("Failed to save data log")

if __name__ == "__main__":
    main()
