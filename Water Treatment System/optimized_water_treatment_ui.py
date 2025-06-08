#!/usr/bin/env python3
"""
Optimized Water Treatment System UI
Compact design for standard screen ratios (1920x1080, 1366x768, etc.)
No scrolling required - all components fit on screen
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
import json
import os
import math
import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime, timedelta


class OptimizedWaterTreatmentSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Water Treatment System - Compact Control Interface")
        self.root.geometry("1400x900")  # Optimized for standard screens
        self.root.configure(bg='#1e3d59')
        self.root.resizable(True, True)
        
        # Simulation variables
        self.running = False
        self.simulation_speed = 1.0
        self.log_file = "water_treatment_log.json"
        
        # Initialize simulator state
        self.init_simulator_state()
        
        # Control variables
        self.control_inputs = {
            'start_button': False,
            'stop_button': False,
            'emergency_stop': False,
            'auto_mode': True,
            'maintenance_mode': False
        }
        
        # LED colors
        self.led_colors = {
            'on': '#00ff00',      # Green
            'off': '#333333',     # Dark gray
            'fault': '#ff0000',   # Red
            'warning': '#ffaa00', # Orange
            'standby': '#0099ff'  # Blue
        }
        
        # Create optimized GUI layout
        self.create_optimized_interface()
        
        # Start simulation thread
        self.simulation_thread = threading.Thread(target=self.simulation_loop, daemon=True)
        self.simulation_thread.start()
        
        # Start GUI update thread
        self.gui_update_thread = threading.Thread(target=self.gui_update_loop, daemon=True)
        self.gui_update_thread.start()

    def init_simulator_state(self):
        """Initialize all simulator state variables"""
        self.system_state = {
            'mode': 'STOPPED',
            'running': False,
            'emergency_stop': False,
            'maintenance_mode': False,
            'auto_mode': True
        }
        
        # Tank states
        self.ground_tank = {
            'level': 50.0, 'capacity': 50000, 'volume': 25000,
            'temperature': 25.0, 'inlet_flow': 0.0, 'outlet_flow': 0.0
        }
        
        self.roof_tank = {
            'level': 30.0, 'capacity': 10000, 'volume': 3000,
            'temperature': 25.0, 'inlet_flow': 0.0, 'outlet_flow': 0.0
        }
        
        # Seawater parameters
        self.seawater = {
            'tds': 35000, 'temperature': 25.0, 'pressure': 1.0,
            'flow_rate': 0.0, 'ph': 8.1, 'conductivity': 55000
        }
        
        # Product water parameters
        self.product_water = {
            'tds': 150, 'ph': 7.2, 'turbidity': 0.1, 'chlorine': 0.5,
            'temperature': 24.0, 'flow_rate': 0.0, 'conductivity': 250
        }
        
        # RO system
        self.ro_system = {
            'pressure': 0.0, 'recovery_rate': 0.0, 'salt_rejection': 99.5,
            'permeate_flow': 0.0, 'concentrate_flow': 0.0,
            'fouling_index': 10.0, 'cleaning_cycles': 0, 'membrane_hours': 0.0
        }
        
        # Pumps
        self.pumps = {
            'intake': {'running': False, 'speed': 0.0, 'current': 0.0, 'hours': 0.0, 'fault': False},
            'prefilter': {'running': False, 'speed': 0.0, 'current': 0.0, 'hours': 0.0, 'fault': False},
            'ro': {'running': False, 'speed': 0.0, 'current': 0.0, 'hours': 0.0, 'fault': False},
            'booster1': {'running': False, 'speed': 0.0, 'current': 0.0, 'hours': 0.0, 'fault': False},
            'booster2': {'running': False, 'speed': 0.0, 'current': 0.0, 'hours': 0.0, 'fault': False}
        }
        
        # Energy monitoring
        self.energy = {
            'total_power': 0.0, 'daily_consumption': 0.0,
            'specific_energy': 0.0, 'efficiency': 85.0
        }
        
        # Process variables
        self.production_rate = 0.0
        self.total_produced = 0.0
        self.system_efficiency = 0.0
        
        # Initialize trend data for plotting
        self.trend_data = {
            'time': [],
            'production_rate': [],
            'tank_levels': [],
            'ro_pressure': [],
            'power_consumption': []
        }
        
        # Alarms and monitoring
        self.alarms = {
            'emergency_stop': False,
            'high_tank_level': False,
            'low_tank_level': False,
            'pump_fault': False,
            'ro_pressure_low': False,
            'water_quality_alarm': False,
            'system_leak': False,
            'maintenance_due': False
        }
        
        # Alarm limits
        self.alarm_limits = {
            'tank_high_level': 95.0,
            'tank_low_level': 10.0,
            'ro_pressure_min': 45.0,
            'max_tds': 300.0,
            'min_ph': 6.5,
            'max_ph': 8.5
        }

    def create_optimized_interface(self):
        """Create optimized single-page interface for standard screen ratios"""
        # Configure styles
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Title.TLabel', font=('Arial', 11, 'bold'), background='#1e3d59', foreground='white')
        style.configure('Header.TLabel', font=('Arial', 9, 'bold'), background='#2c3e50', foreground='white')
        style.configure('Data.TLabel', font=('Arial', 8), background='#34495e', foreground='white')
        style.configure('Compact.TLabelframe.Label', font=('Arial', 9, 'bold'))
        style.configure('Compact.TLabelframe', padding=3)
        
        # Main container - use grid layout for better control
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Configure grid weights
        main_frame.grid_rowconfigure(0, weight=0)  # Control panel - fixed height
        main_frame.grid_rowconfigure(1, weight=0)  # Overview - fixed height
        main_frame.grid_rowconfigure(2, weight=0)  # Components and data - fixed height
        main_frame.grid_rowconfigure(3, weight=1)  # Trends - expandable
        main_frame.grid_columnconfigure(0, weight=1)
        
        # Row 1: Control Panel (compact)
        self.create_compact_control_panel(main_frame)
        
        # Row 2: System Overview (horizontal layout)
        self.create_compact_overview(main_frame)
        
        # Row 3: Components, Alarms, and Process Data (horizontal layout)
        self.create_middle_section(main_frame)
        
        # Row 4: Trends (optimized size)
        self.create_compact_trends(main_frame)

    def create_compact_control_panel(self, parent):
        """Create compact control panel"""
        control_frame = ttk.LabelFrame(parent, text="System Control", style='Compact.TLabelframe')
        control_frame.grid(row=0, column=0, sticky='ew', padx=2, pady=2)
        
        # Single row with all controls
        inner_frame = ttk.Frame(control_frame)
        inner_frame.pack(fill='x', padx=5, pady=5)
        
        # System status LED
        self.system_led = tk.Canvas(inner_frame, width=25, height=25, bg='#2c3e50', highlightthickness=0)
        self.system_led.pack(side='left', padx=(0, 8))
        self.system_led_circle = self.system_led.create_oval(3, 3, 22, 22, fill=self.led_colors['off'], outline='white')
        
        # Status label
        self.status_label = ttk.Label(inner_frame, text="SYSTEM STOPPED", font=('Arial', 10, 'bold'))
        self.status_label.pack(side='left', padx=(0, 15))
        
        # Control buttons
        self.start_btn = ttk.Button(inner_frame, text="START", command=self.start_system, width=8)
        self.start_btn.pack(side='left', padx=3)
        
        self.stop_btn = ttk.Button(inner_frame, text="STOP", command=self.stop_system, width=8)
        self.stop_btn.pack(side='left', padx=3)
        
        self.emergency_btn = ttk.Button(inner_frame, text="E-STOP", command=self.emergency_stop, width=8)
        self.emergency_btn.pack(side='left', padx=3)
        
        # Mode controls
        self.auto_var = tk.BooleanVar(value=True)
        self.auto_check = ttk.Checkbutton(inner_frame, text="Auto Mode", variable=self.auto_var)
        self.auto_check.pack(side='left', padx=(15, 5))
        
        self.maintenance_var = tk.BooleanVar()
        self.maintenance_check = ttk.Checkbutton(inner_frame, text="Maintenance", variable=self.maintenance_var)
        self.maintenance_check.pack(side='left', padx=5)

    def create_compact_overview(self, parent):
        """Create compact system overview"""
        overview_frame = ttk.LabelFrame(parent, text="System Overview", style='Compact.TLabelframe')
        overview_frame.grid(row=1, column=0, sticky='ew', padx=2, pady=2)
        
        metrics_frame = ttk.Frame(overview_frame)
        metrics_frame.pack(fill='x', padx=5, pady=5)
        
        # 6 columns for key metrics
        metrics = [
            ("Production Rate", "production_rate_label", "0.0 L/min"),
            ("Total Produced", "total_produced_label", "0.0 L"),
            ("Ground Tank", "ground_tank_label", "50.0%"),
            ("RO Pressure", "ro_pressure_label", "0.0 bar"),
            ("Power", "power_label", "0.0 kW"),
            ("Efficiency", "efficiency_label", "85.0%")
        ]
        
        for i, (title, attr_name, initial_value) in enumerate(metrics):
            col_frame = ttk.Frame(metrics_frame)
            col_frame.pack(side='left', fill='both', expand=True, padx=3)
            
            ttk.Label(col_frame, text=title, font=('Arial', 8, 'bold')).pack()
            label = ttk.Label(col_frame, text=initial_value, font=('Arial', 10, 'bold'), foreground='#00ff00')
            label.pack()
            setattr(self, attr_name, label)

    def create_middle_section(self, parent):
        """Create middle section with components, alarms, and process data"""
        middle_frame = ttk.Frame(parent)
        middle_frame.grid(row=2, column=0, sticky='ew', padx=2, pady=2)
        
        # Three columns: Components, Alarms, Process Data
        middle_frame.grid_columnconfigure(0, weight=1)
        middle_frame.grid_columnconfigure(1, weight=1)
        middle_frame.grid_columnconfigure(2, weight=1)
        
        # Column 1: Component Status
        self.create_compact_components(middle_frame)
        
        # Column 2: Alarms
        self.create_compact_alarms(middle_frame)
        
        # Column 3: Process Data
        self.create_compact_process_data(middle_frame)

    def create_compact_components(self, parent):
        """Create compact component status"""
        comp_frame = ttk.LabelFrame(parent, text="Components", style='Compact.TLabelframe')
        comp_frame.grid(row=0, column=0, sticky='nsew', padx=2, pady=2)
        
        # Pumps section
        pumps_frame = ttk.LabelFrame(comp_frame, text="Pumps")
        pumps_frame.pack(fill='x', padx=3, pady=3)
        
        self.pump_leds = {}
        self.pump_labels = {}
        
        for i, (pump_name, pump_data) in enumerate(self.pumps.items()):
            pump_row = ttk.Frame(pumps_frame)
            pump_row.pack(fill='x', padx=2, pady=1)
            
            # LED indicator
            led = tk.Canvas(pump_row, width=16, height=16, bg='#2c3e50', highlightthickness=0)
            led.pack(side='left', padx=(0, 3))
            led_circle = led.create_oval(2, 2, 14, 14, fill=self.led_colors['off'], outline='white')
            self.pump_leds[pump_name] = (led, led_circle)
            
            # Pump info
            ttk.Label(pump_row, text=f"{pump_name.title()}", width=8, font=('Arial', 8)).pack(side='left')
            label = ttk.Label(pump_row, text="STOPPED", width=12, font=('Arial', 8))
            label.pack(side='left')
            self.pump_labels[pump_name] = label
        
        # Tanks section
        tanks_frame = ttk.LabelFrame(comp_frame, text="Tanks")
        tanks_frame.pack(fill='x', padx=3, pady=3)
          # Ground tank
        ttk.Label(tanks_frame, text="Ground Tank", font=('Arial', 8)).pack(fill='x')
        self.ground_tank_progress = ttk.Progressbar(tanks_frame, length=150, mode='determinate')
        self.ground_tank_progress.pack(fill='x', padx=2, pady=1)
        self.ground_tank_progress['value'] = 50
        
        # Roof tank
        ttk.Label(tanks_frame, text="Roof Tank", font=('Arial', 8)).pack(fill='x', pady=(5,0))
        self.roof_tank_progress = ttk.Progressbar(tanks_frame, length=150, mode='determinate')
        self.roof_tank_progress.pack(fill='x', padx=2, pady=1)
        self.roof_tank_progress['value'] = 30

    def create_compact_alarms(self, parent):
        """Create compact alarms section"""
        alarms_frame = ttk.LabelFrame(parent, text="System Alarms", style='Compact.TLabelframe')
        alarms_frame.grid(row=0, column=1, sticky='nsew', padx=2, pady=2)
        
        # Alarm grid
        alarms_grid = ttk.Frame(alarms_frame)
        alarms_grid.pack(fill='both', expand=True, padx=3, pady=3)
        
        self.alarm_indicators = {}
        
        alarm_definitions = [
            ('Emergency Stop', 'emergency_stop', 'CRITICAL'),
            ('High Tank Level', 'high_tank_level', 'WARNING'),
            ('Low Tank Level', 'low_tank_level', 'WARNING'),
            ('Pump Fault', 'pump_fault', 'ALARM'),
            ('RO Pressure Low', 'ro_pressure_low', 'ALARM'),
            ('Water Quality', 'water_quality_alarm', 'ALARM'),
            ('System Leak', 'system_leak', 'CRITICAL'),
            ('Maintenance Due', 'maintenance_due', 'INFO')
        ]
        
        for i, (alarm_name, alarm_key, alarm_type) in enumerate(alarm_definitions):
            row = i // 2
            col = i % 2
            
            alarm_frame = ttk.Frame(alarms_grid)
            alarm_frame.grid(row=row, column=col, padx=2, pady=1, sticky='w')
            
            # LED indicator
            led = tk.Canvas(alarm_frame, width=12, height=12, bg='#2c3e50', highlightthickness=0)
            led.pack(side='left', padx=(0, 3))
            led_circle = led.create_oval(1, 1, 11, 11, fill=self.led_colors['off'], outline='gray')
            
            # Alarm label
            label = ttk.Label(alarm_frame, text=alarm_name, font=('Arial', 7))
            label.pack(side='left')
            
            self.alarm_indicators[alarm_key] = {
                'led': led,
                'led_circle': led_circle,
                'label': label,
                'type': alarm_type
            }
        
        # Alarm summary
        summary_frame = ttk.Frame(alarms_frame)
        summary_frame.pack(fill='x', padx=3, pady=(0, 3))
        
        ttk.Label(summary_frame, text="Active:", font=('Arial', 8, 'bold')).pack(side='left')
        self.active_alarms_label = ttk.Label(summary_frame, text="None", foreground='green', font=('Arial', 8))
        self.active_alarms_label.pack(side='left', padx=(5, 0))

    def create_compact_process_data(self, parent):
        """Create compact process data section"""
        process_frame = ttk.LabelFrame(parent, text="Process Data", style='Compact.TLabelframe')
        process_frame.grid(row=0, column=2, sticky='nsew', padx=2, pady=2)
        
        # Water Quality section
        quality_frame = ttk.LabelFrame(process_frame, text="Water Quality")
        quality_frame.pack(fill='x', padx=3, pady=3)
        
        quality_params = [
            ('pH', 'ph'), ('TDS', 'tds'), ('Turbidity', 'turbidity'),
            ('Chlorine', 'chlorine'), ('Temp', 'temperature'), ('Conductivity', 'conductivity')
        ]
        
        self.quality_labels = {}
        for i, (param_name, param_key) in enumerate(quality_params):
            row = i // 2
            col = i % 2
            
            param_frame = ttk.Frame(quality_frame)
            param_frame.grid(row=row, column=col, padx=2, pady=1, sticky='ew')
            
            ttk.Label(param_frame, text=f"{param_name}:", font=('Arial', 7)).pack(side='left')
            label = ttk.Label(param_frame, text="--", font=('Arial', 8, 'bold'))
            label.pack(side='right')
            self.quality_labels[param_key] = label
        
        quality_frame.grid_columnconfigure(0, weight=1)
        quality_frame.grid_columnconfigure(1, weight=1)
        
        # Energy section
        energy_frame = ttk.LabelFrame(process_frame, text="Energy")
        energy_frame.pack(fill='x', padx=3, pady=3)
        
        self.energy_labels = {}
        energy_params = [
            ('Total Power', 'total_power', 'kW'),
            ('Daily kWh', 'daily_consumption', 'kWh'),
            ('Specific', 'specific_energy', 'kWh/m³'),
            ('Efficiency', 'efficiency', '%')
        ]
        
        for i, (param_name, param_key, unit) in enumerate(energy_params):
            row = i // 2
            col = i % 2
            
            param_frame = ttk.Frame(energy_frame)
            param_frame.grid(row=row, column=col, padx=2, pady=1, sticky='ew')
            
            ttk.Label(param_frame, text=f"{param_name}:", font=('Arial', 7)).pack(side='left')
            label = ttk.Label(param_frame, text=f"-- {unit}", font=('Arial', 8, 'bold'))
            label.pack(side='right')
            self.energy_labels[param_key] = (label, unit)
        
        energy_frame.grid_columnconfigure(0, weight=1)
        energy_frame.grid_columnconfigure(1, weight=1)

    def create_compact_trends(self, parent):
        """Create compact trends section optimized for screen space"""
        trends_frame = ttk.LabelFrame(parent, text="Real-Time Trends", style='Compact.TLabelframe')
        trends_frame.grid(row=3, column=0, sticky='nsew', padx=2, pady=2)
        
        # Create matplotlib figure with smaller size
        self.fig, ((self.ax1, self.ax2), (self.ax3, self.ax4)) = plt.subplots(2, 2, figsize=(10, 4.5))
        self.fig.patch.set_facecolor('#2c3e50')
        plt.subplots_adjust(left=0.08, bottom=0.15, right=0.98, top=0.92, wspace=0.3, hspace=0.4)
        
        # Configure subplot styles
        for ax in [self.ax1, self.ax2, self.ax3, self.ax4]:
            ax.set_facecolor('#34495e')
            ax.tick_params(colors='white', labelsize=7)
            ax.xaxis.label.set_color('white')
            ax.yaxis.label.set_color('white')
            ax.title.set_color('white')
            ax.title.set_fontsize(8)
        
        # Create canvas
        self.trends_canvas = FigureCanvasTkAgg(self.fig, trends_frame)
        self.trends_canvas.draw()
        self.trends_canvas.get_tk_widget().pack(fill='both', expand=True, padx=3, pady=3)

    # System control methods
    def start_system(self):
        """Start the water treatment system"""
        self.control_inputs['start_button'] = True
        self.control_inputs['stop_button'] = False
        self.control_inputs['emergency_stop'] = False
        self.running = True
        self.system_state['running'] = True
        self.system_state['mode'] = 'RUNNING'
        
        # Update GUI
        self.status_label.config(text="SYSTEM RUNNING")
        self.update_led(self.system_led, self.system_led_circle, 'running')
        
        messagebox.showinfo("System Control", "Water Treatment System Started")

    def stop_system(self):
        """Stop the water treatment system"""
        self.control_inputs['stop_button'] = True
        self.control_inputs['start_button'] = False
        self.running = False
        self.system_state['running'] = False
        self.system_state['mode'] = 'STOPPED'
        
        # Update GUI
        self.status_label.config(text="SYSTEM STOPPED")
        self.update_led(self.system_led, self.system_led_circle, 'off')
        
        # Stop all pumps
        for pump_name in self.pumps:
            self.pumps[pump_name]['running'] = False
            self.pumps[pump_name]['speed'] = 0.0
            self.pumps[pump_name]['current'] = 0.0
        
        messagebox.showinfo("System Control", "Water Treatment System Stopped")

    def emergency_stop(self):
        """Emergency stop the system"""
        self.control_inputs['emergency_stop'] = True
        self.control_inputs['start_button'] = False
        self.control_inputs['stop_button'] = False
        self.running = False
        self.system_state['running'] = False
        self.system_state['emergency_stop'] = True
        self.system_state['mode'] = 'EMERGENCY STOP'
        
        # Update GUI
        self.status_label.config(text="EMERGENCY STOP")
        self.update_led(self.system_led, self.system_led_circle, 'fault')
        
        # Stop all equipment immediately
        for pump_name in self.pumps:
            self.pumps[pump_name]['running'] = False
            self.pumps[pump_name]['speed'] = 0.0
            self.pumps[pump_name]['current'] = 0.0
        
        messagebox.showwarning("Emergency Stop", "EMERGENCY STOP ACTIVATED!")

    def update_led(self, led_canvas, led_circle, status):
        """Update LED indicator color based on status"""
        if status == 'running':
            color = self.led_colors['on']
        elif status == 'fault':
            color = self.led_colors['fault']
        elif status == 'warning':
            color = self.led_colors['warning']
        elif status == 'standby':
            color = self.led_colors['standby']
        else:
            color = self.led_colors['off']
        
        led_canvas.itemconfig(led_circle, fill=color)

    def simulation_loop(self):
        """Main simulation loop"""
        simulation_time = 0.0
        
        while True:
            try:
                if self.running and not self.system_state['emergency_stop']:
                    self.update_simulation(simulation_time)
                    simulation_time += 0.1
                
                self.log_system_data(simulation_time)
                time.sleep(0.1)
                
            except Exception as e:
                print(f"Simulation error: {e}")
                time.sleep(1)

    def update_simulation(self, simulation_time):
        """Update simulation calculations"""
        # Start pumps in sequence if system is running
        if self.system_state['running']:
            if simulation_time > 2.0:
                self.pumps['intake']['running'] = True
                self.pumps['intake']['speed'] = 85.0
                self.pumps['intake']['current'] = 12.5
                
            if simulation_time > 5.0:
                self.pumps['prefilter']['running'] = True
                self.pumps['prefilter']['speed'] = 90.0
                self.pumps['prefilter']['current'] = 15.2
                
            if simulation_time > 8.0:
                self.pumps['ro']['running'] = True
                self.pumps['ro']['speed'] = 92.0
                self.pumps['ro']['current'] = 18.7
                self.ro_system['pressure'] = 55.0 + random.uniform(-2, 2)
                
            if simulation_time > 12.0:
                self.pumps['booster1']['running'] = True
                self.pumps['booster1']['speed'] = 88.0
                self.pumps['booster1']['current'] = 14.8
                
                self.pumps['booster2']['running'] = True
                self.pumps['booster2']['speed'] = 87.0
                self.pumps['booster2']['current'] = 14.3
        
        # Calculate flows and production
        if self.pumps['ro']['running']:
            self.seawater['flow_rate'] = 220.0 + random.uniform(-10, 10)
            self.ro_system['permeate_flow'] = 167.0 + random.uniform(-8, 8)
            self.ro_system['concentrate_flow'] = self.seawater['flow_rate'] - self.ro_system['permeate_flow']
            self.ro_system['recovery_rate'] = (self.ro_system['permeate_flow'] / self.seawater['flow_rate']) * 100
            self.production_rate = self.ro_system['permeate_flow']
            self.total_produced += self.production_rate * (0.1/60)
        else:
            self.production_rate = 0.0
            self.ro_system['permeate_flow'] = 0.0
            self.ro_system['concentrate_flow'] = 0.0
            self.ro_system['recovery_rate'] = 0.0
        
        # Update tank levels
        if self.production_rate > 0:
            flow_in = self.production_rate * (0.1/60)
            self.ground_tank['volume'] += flow_in
            self.ground_tank['level'] = (self.ground_tank['volume'] / self.ground_tank['capacity']) * 100
            
            if self.ground_tank['level'] > 95:
                self.ground_tank['level'] = 95
                self.ground_tank['volume'] = self.ground_tank['capacity'] * 0.95
        
        # Update water quality
        if self.production_rate > 0:
            self.product_water['tds'] = 150 + random.uniform(-20, 20)
            self.product_water['ph'] = 7.2 + random.uniform(-0.2, 0.2)
            self.product_water['turbidity'] = 0.1 + random.uniform(-0.05, 0.05)
            self.product_water['chlorine'] = 0.5 + random.uniform(-0.1, 0.1)
            self.product_water['conductivity'] = 250 + random.uniform(-30, 30)
            self.product_water['temperature'] = 24.0 + random.uniform(-1, 1)
        
        # Update energy consumption
        total_power = 0.0
        for pump_name, pump_data in self.pumps.items():
            if pump_data['running']:
                power = pump_data['current'] * 0.4 * 0.85
                total_power += power
                pump_data['hours'] += 0.1/3600
        
        self.energy['total_power'] = total_power
        self.energy['daily_consumption'] += total_power * (0.1/3600)
        
        if self.production_rate > 0:
            self.energy['specific_energy'] = self.energy['total_power'] / (self.production_rate * 60 / 1000)
        
        self.check_alarms()

    def check_alarms(self):
        """Check all alarm conditions"""
        # Reset alarms first (except emergency stop)
        for alarm_key in self.alarms:
            if alarm_key != 'emergency_stop':
                self.alarms[alarm_key] = False
        
        # Check tank levels
        if self.ground_tank['level'] > self.alarm_limits['tank_high_level']:
            self.alarms['high_tank_level'] = True
        
        if self.ground_tank['level'] < self.alarm_limits['tank_low_level']:
            self.alarms['low_tank_level'] = True
        
        # Check RO pressure
        if self.ro_system['pressure'] < self.alarm_limits['ro_pressure_min'] and self.pumps['ro']['running']:
            self.alarms['ro_pressure_low'] = True
        
        # Check water quality
        if (self.product_water['tds'] > self.alarm_limits['max_tds'] or 
            self.product_water['ph'] < self.alarm_limits['min_ph'] or 
            self.product_water['ph'] > self.alarm_limits['max_ph']):
            self.alarms['water_quality_alarm'] = True
        
        # Check pump faults
        for pump_name, pump_data in self.pumps.items():
            if pump_data['fault']:
                self.alarms['pump_fault'] = True
                break

    def log_system_data(self, simulation_time):
        """Log system data to file"""
        data = {
            'timestamp': datetime.now().isoformat(),
            'simulation_time': simulation_time,
            'system_state': self.system_state,
            'production_rate': self.production_rate,
            'total_produced': self.total_produced,
            'ground_tank': self.ground_tank,
            'roof_tank': self.roof_tank,
            'ro_system': self.ro_system,
            'pumps': self.pumps,
            'product_water': self.product_water,
            'energy': self.energy
        }
        
        try:
            if os.path.exists(self.log_file):
                try:
                    with open(self.log_file, 'r') as f:
                        log_data = json.load(f)
                except:
                    log_data = []
            else:
                log_data = []
            
            log_data.append(data)
            
            if len(log_data) > 1000:
                log_data = log_data[-1000:]
            
            with open(self.log_file, 'w') as f:
                json.dump(log_data, f, indent=2)
                
        except Exception as e:
            print(f"Logging error: {e}")

    def gui_update_loop(self):
        """Update GUI elements in separate thread"""
        while True:
            try:
                self.root.after(0, self.update_gui_elements)
                time.sleep(0.5)
            except Exception as e:
                print(f"GUI update error: {e}")
                time.sleep(1)

    def update_gui_elements(self):
        """Update all GUI elements with current data"""
        try:
            # Update overview metrics
            self.production_rate_label.config(text=f"{self.production_rate:.1f} L/min")
            self.total_produced_label.config(text=f"{self.total_produced:.0f} L")
            self.ground_tank_label.config(text=f"{self.ground_tank['level']:.1f}%")
            self.ro_pressure_label.config(text=f"{self.ro_system['pressure']:.1f} bar")
            self.power_label.config(text=f"{self.energy['total_power']:.1f} kW")
            self.efficiency_label.config(text=f"{self.energy['efficiency']:.1f}%")
            
            # Update pump status and LEDs
            for pump_name, pump_data in self.pumps.items():
                if pump_name in self.pump_labels:
                    if pump_data['running']:
                        status_text = f"RUN {pump_data['current']:.1f}A"
                        led_status = 'running'
                    elif pump_data['fault']:
                        status_text = "FAULT"
                        led_status = 'fault'
                    else:
                        status_text = "STOPPED"
                        led_status = 'off'
                    
                    self.pump_labels[pump_name].config(text=status_text)
                    if pump_name in self.pump_leds:
                        led_canvas, led_circle = self.pump_leds[pump_name]
                        self.update_led(led_canvas, led_circle, led_status)
            
            # Update tank progress bars
            self.ground_tank_progress['value'] = self.ground_tank['level']
            self.roof_tank_progress['value'] = self.roof_tank['level']
            
            # Update water quality parameters
            quality_data = {
                'ph': f"{self.product_water['ph']:.1f}",
                'tds': f"{self.product_water['tds']:.0f}",
                'turbidity': f"{self.product_water['turbidity']:.2f}",
                'chlorine': f"{self.product_water['chlorine']:.1f}",
                'temperature': f"{self.product_water['temperature']:.1f}°C",
                'conductivity': f"{self.product_water['conductivity']:.0f}"
            }
            
            for param_key, value in quality_data.items():
                if param_key in self.quality_labels:
                    self.quality_labels[param_key].config(text=value)
            
            # Update energy parameters
            energy_data = {
                'total_power': self.energy['total_power'],
                'daily_consumption': self.energy['daily_consumption'],
                'specific_energy': self.energy['specific_energy'],
                'efficiency': self.energy['efficiency']
            }
            
            for param_key, value in energy_data.items():
                if param_key in self.energy_labels:
                    label, unit = self.energy_labels[param_key]
                    label.config(text=f"{value:.1f} {unit}")
            
            # Update alarm indicators
            self.update_alarm_indicators()
            
            # Update trends
            self.update_trend_plots()
            
        except Exception as e:
            print(f"GUI update error: {e}")

    def update_alarm_indicators(self):
        """Update alarm indicator LEDs and status"""
        active_alarms = []
        
        for alarm_key, is_active in self.alarms.items():
            if alarm_key in self.alarm_indicators:
                indicator = self.alarm_indicators[alarm_key]
                
                if is_active:
                    if indicator['type'] == 'CRITICAL':
                        led_color = self.led_colors['fault']
                    elif indicator['type'] == 'ALARM':
                        led_color = self.led_colors['warning']
                    elif indicator['type'] == 'WARNING':
                        led_color = self.led_colors['standby']
                    else:
                        led_color = self.led_colors['on']
                    
                    indicator['led'].itemconfig(indicator['led_circle'], fill=led_color)
                    active_alarms.append(alarm_key.replace('_', ' ').title())
                else:
                    indicator['led'].itemconfig(indicator['led_circle'], fill=self.led_colors['off'])
        
        # Update active alarms summary
        if active_alarms:
            alarm_text = ", ".join(active_alarms[:2])  # Show max 2 alarms
            if len(active_alarms) > 2:
                alarm_text += f" +{len(active_alarms)-2} more"
            self.active_alarms_label.config(text=alarm_text, foreground='red')
        else:
            self.active_alarms_label.config(text="None", foreground='green')

    def update_trend_plots(self):
        """Update trend plots with recent data"""
        try:
            # Add current data point to trends
            current_time = datetime.now()
            self.trend_data['time'].append(current_time)
            self.trend_data['production_rate'].append(self.production_rate)
            self.trend_data['tank_levels'].append(self.ground_tank['level'])
            self.trend_data['ro_pressure'].append(self.ro_system['pressure'])
            self.trend_data['power_consumption'].append(self.energy['total_power'])
            
            # Keep only last 30 points for better performance
            max_points = 30
            for key in self.trend_data:
                if len(self.trend_data[key]) > max_points:
                    self.trend_data[key] = self.trend_data[key][-max_points:]
            
            # Clear and plot
            for ax in [self.ax1, self.ax2, self.ax3, self.ax4]:
                ax.clear()
                ax.set_facecolor('#34495e')
                ax.tick_params(colors='white', labelsize=7)
                ax.xaxis.label.set_color('white')
                ax.yaxis.label.set_color('white')
                ax.title.set_color('white')
                ax.title.set_fontsize(8)
            
            if len(self.trend_data['time']) > 1:
                # Production rate
                self.ax1.plot(self.trend_data['time'], self.trend_data['production_rate'], 'g-', linewidth=2)
                self.ax1.set_title('Production (L/min)')
                self.ax1.grid(True, alpha=0.3)
                
                # Tank levels
                self.ax2.plot(self.trend_data['time'], self.trend_data['tank_levels'], 'b-', linewidth=2)
                self.ax2.set_title('Tank Level (%)')
                self.ax2.grid(True, alpha=0.3)
                
                # RO pressure
                self.ax3.plot(self.trend_data['time'], self.trend_data['ro_pressure'], 'r-', linewidth=2)
                self.ax3.set_title('RO Pressure (bar)')
                self.ax3.grid(True, alpha=0.3)
                
                # Power consumption
                self.ax4.plot(self.trend_data['time'], self.trend_data['power_consumption'], 'orange', linewidth=2)
                self.ax4.set_title('Power (kW)')
                self.ax4.grid(True, alpha=0.3)
                      # Format x-axis - show fewer labels
            for ax in [self.ax1, self.ax2, self.ax3, self.ax4]:
                ax.tick_params(axis='x', rotation=45, labelsize=6)
                # Use fewer ticks on x-axis for better readability
                if len(self.trend_data['time']) > 5:
                    ax.set_xticks(self.trend_data['time'][::max(1, len(self.trend_data['time'])//3)])
            
            plt.tight_layout()
            self.trends_canvas.draw()
            
        except Exception as e:
            print(f"Trend plot error: {e}")


def main():
    """Main function to start the optimized system"""
    root = tk.Tk()
    app = OptimizedWaterTreatmentSystem(root)
    
    try:
        root.mainloop()
    except KeyboardInterrupt:
        print("\nShutting down system...")
    except Exception as e:
        print(f"Application error: {e}")


if __name__ == "__main__":
    main()
