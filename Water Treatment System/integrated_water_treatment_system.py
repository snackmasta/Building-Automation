#!/usr/bin/env python3
"""
Integrated Water Treatment System
Combined HMI and Simulator with Compact Single-Page Interface
Includes LED indicators for actual component status
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


class WaterTreatmentIntegratedSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Water Treatment System - Integrated Control & Monitoring")
        self.root.geometry("1600x1000")
        self.root.configure(bg='#1e3d59')
        self.root.state('zoomed')  # Maximize window
        
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
            'maintenance_mode': False,
            'pump_override': {},
            'valve_override': {}
        }
        
        # LED colors
        self.led_colors = {
            'on': '#00ff00',      # Green
            'off': '#333333',     # Dark gray
            'fault': '#ff0000',   # Red
            'warning': '#ffaa00', # Orange
            'standby': '#0099ff'  # Blue
        }
        
        # Create GUI
        self.create_integrated_interface()
        
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
        }        # Process variables
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
        
    def create_integrated_interface(self):
        """Create the integrated single-page interface"""
        # Main container with scrollable frame
        main_canvas = tk.Canvas(self.root, bg='#1e3d59')
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=main_canvas.yview)
        self.scrollable_frame = ttk.Frame(main_canvas)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: main_canvas.configure(scrollregion=main_canvas.bbox("all"))
        )
        
        main_canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        main_canvas.configure(yscrollcommand=scrollbar.set)
        
        main_canvas.pack(side="left", fill="both", expand=True)        scrollbar.pack(side="right", fill="y")
        
        # Configure styles
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Title.TLabel', font=('Arial', 14, 'bold'), background='#1e3d59', foreground='white')
        style.configure('Header.TLabel', font=('Arial', 12, 'bold'), background='#2c3e50', foreground='white')
        style.configure('Data.TLabel', font=('Arial', 10), background='#34495e', foreground='white')
        
        # Create main sections
        self.create_control_panel()
        self.create_system_overview()
        self.create_component_status()
        self.create_alarms_section()
        self.create_process_data()
        self.create_trends_section()
        
        # Bind mouse wheel scrolling
        def _on_mousewheel(event):
            main_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        main_canvas.bind_all("<MouseWheel>", _on_mousewheel)

    def create_control_panel(self):
        """Create the main control panel at the top"""
        control_frame = ttk.LabelFrame(self.scrollable_frame, text="System Control", style='Title.TLabel')
        control_frame.pack(fill='x', padx=10, pady=5)
        
        # Control buttons row
        button_frame = ttk.Frame(control_frame)
        button_frame.pack(fill='x', padx=10, pady=10)
        
        # System status LED
        self.system_led = tk.Canvas(button_frame, width=30, height=30, bg='#2c3e50', highlightthickness=0)
        self.system_led.pack(side='left', padx=(0, 10))
        self.system_led_circle = self.system_led.create_oval(5, 5, 25, 25, fill=self.led_colors['off'], outline='white')
        
        # Status label
        self.status_label = ttk.Label(button_frame, text="SYSTEM STOPPED", style='Header.TLabel')
        self.status_label.pack(side='left', padx=(0, 20))
        
        # Control buttons
        self.start_btn = ttk.Button(button_frame, text="START SYSTEM", command=self.start_system)
        self.start_btn.pack(side='left', padx=5)
        
        self.stop_btn = ttk.Button(button_frame, text="STOP SYSTEM", command=self.stop_system)
        self.stop_btn.pack(side='left', padx=5)
        
        self.emergency_btn = ttk.Button(button_frame, text="EMERGENCY STOP", command=self.emergency_stop)
        self.emergency_btn.pack(side='left', padx=5)
        
        # Mode controls
        mode_frame = ttk.Frame(button_frame)
        mode_frame.pack(side='right', padx=10)
        
        self.auto_var = tk.BooleanVar(value=True)
        self.auto_check = ttk.Checkbutton(mode_frame, text="Auto Mode", variable=self.auto_var)
        self.auto_check.pack(side='left', padx=5)
        
        self.maintenance_var = tk.BooleanVar()
        self.maintenance_check = ttk.Checkbutton(mode_frame, text="Maintenance", variable=self.maintenance_var)
        self.maintenance_check.pack(side='left', padx=5)

    def create_system_overview(self):
        """Create system overview with key metrics"""
        overview_frame = ttk.LabelFrame(self.scrollable_frame, text="System Overview", style='Title.TLabel')
        overview_frame.pack(fill='x', padx=10, pady=5)
        
        metrics_frame = ttk.Frame(overview_frame)
        metrics_frame.pack(fill='x', padx=10, pady=10)
        
        # Key metrics in columns
        col1 = ttk.Frame(metrics_frame)
        col1.pack(side='left', fill='both', expand=True, padx=5)
        
        col2 = ttk.Frame(metrics_frame)
        col2.pack(side='left', fill='both', expand=True, padx=5)
        
        col3 = ttk.Frame(metrics_frame)
        col3.pack(side='left', fill='both', expand=True, padx=5)
        
        col4 = ttk.Frame(metrics_frame)
        col4.pack(side='left', fill='both', expand=True, padx=5)
        
        # Production metrics
        ttk.Label(col1, text="Production Rate", style='Header.TLabel').pack()
        self.production_rate_label = ttk.Label(col1, text="0.0 L/min", style='Data.TLabel')
        self.production_rate_label.pack()
        
        ttk.Label(col1, text="Total Produced", style='Header.TLabel').pack()
        self.total_produced_label = ttk.Label(col1, text="0.0 L", style='Data.TLabel')
        self.total_produced_label.pack()
        
        # Tank levels
        ttk.Label(col2, text="Ground Tank", style='Header.TLabel').pack()
        self.ground_tank_label = ttk.Label(col2, text="50.0%", style='Data.TLabel')
        self.ground_tank_label.pack()
        
        ttk.Label(col2, text="Roof Tank", style='Header.TLabel').pack()
        self.roof_tank_label = ttk.Label(col2, text="30.0%", style='Data.TLabel')
        self.roof_tank_label.pack()
        
        # RO system
        ttk.Label(col3, text="RO Pressure", style='Header.TLabel').pack()
        self.ro_pressure_label = ttk.Label(col3, text="0.0 bar", style='Data.TLabel')
        self.ro_pressure_label.pack()
        
        ttk.Label(col3, text="Recovery Rate", style='Header.TLabel').pack()
        self.recovery_rate_label = ttk.Label(col3, text="0.0%", style='Data.TLabel')
        self.recovery_rate_label.pack()
        
        # Energy
        ttk.Label(col4, text="Power Consumption", style='Header.TLabel').pack()
        self.power_label = ttk.Label(col4, text="0.0 kW", style='Data.TLabel')
        self.power_label.pack()
        
        ttk.Label(col4, text="Efficiency", style='Header.TLabel').pack()
        self.efficiency_label = ttk.Label(col4, text="85.0%", style='Data.TLabel')
        self.efficiency_label.pack()

    def create_component_status(self):
        """Create component status section with LED indicators"""
        components_frame = ttk.LabelFrame(self.scrollable_frame, text="Component Status", style='Title.TLabel')
        components_frame.pack(fill='x', padx=10, pady=5)
        
        # Pumps section
        pumps_frame = ttk.LabelFrame(components_frame, text="Pumps")
        pumps_frame.pack(side='left', fill='both', expand=True, padx=5, pady=5)
        
        self.pump_leds = {}
        self.pump_labels = {}
        
        for i, (pump_name, pump_data) in enumerate(self.pumps.items()):
            pump_row = ttk.Frame(pumps_frame)
            pump_row.pack(fill='x', padx=5, pady=2)
            
            # LED indicator
            led = tk.Canvas(pump_row, width=20, height=20, bg='#2c3e50', highlightthickness=0)
            led.pack(side='left', padx=(0, 5))
            led_circle = led.create_oval(3, 3, 17, 17, fill=self.led_colors['off'], outline='white')
            self.pump_leds[pump_name] = (led, led_circle)
            
            # Pump info
            ttk.Label(pump_row, text=f"{pump_name.title()} Pump", width=12).pack(side='left')
            label = ttk.Label(pump_row, text="STOPPED - 0.0 A", width=15)
            label.pack(side='left')
            self.pump_labels[pump_name] = label
        
        # Tanks section
        tanks_frame = ttk.LabelFrame(components_frame, text="Tank Levels")
        tanks_frame.pack(side='left', fill='both', expand=True, padx=5, pady=5)
        
        # Ground tank progress bar
        ttk.Label(tanks_frame, text="Ground Tank (50,000L)").pack(fill='x', padx=5)
        self.ground_tank_progress = ttk.Progressbar(tanks_frame, length=200, mode='determinate')
        self.ground_tank_progress.pack(fill='x', padx=5, pady=2)
        self.ground_tank_progress['value'] = 50
        
        # Roof tank progress bar
        ttk.Label(tanks_frame, text="Roof Tank (10,000L)").pack(fill='x', padx=5, pady=(10,0))
        self.roof_tank_progress = ttk.Progressbar(tanks_frame, length=200, mode='determinate')
        self.roof_tank_progress.pack(fill='x', padx=5, pady=2)
        self.roof_tank_progress['value'] = 30
          # RO System section
        ro_frame = ttk.LabelFrame(components_frame, text="RO System")
        ro_frame.pack(side='left', fill='both', expand=True, padx=5, pady=5)
        
        # RO status LED
        ro_led_frame = ttk.Frame(ro_frame)
        ro_led_frame.pack(fill='x', padx=5, pady=2)
        
        self.ro_led = tk.Canvas(ro_led_frame, width=20, height=20, bg='#2c3e50', highlightthickness=0)
        self.ro_led.pack(side='left', padx=(0, 5))
        self.ro_led_circle = self.ro_led.create_oval(3, 3, 17, 17, fill=self.led_colors['off'], outline='white')
        
        self.ro_status_label = ttk.Label(ro_led_frame, text="RO System: OFFLINE")
        self.ro_status_label.pack(side='left')

    def create_alarms_section(self):
        """Create alarms and status monitoring section"""
        alarms_frame = ttk.LabelFrame(self.scrollable_frame, text="System Alarms & Status", style='Title.TLabel')
        alarms_frame.pack(fill='x', padx=10, pady=5)
        
        # Create alarm indicators in a grid
        alarms_grid = ttk.Frame(alarms_frame)
        alarms_grid.pack(fill='x', padx=10, pady=10)
        
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
            row = i // 4
            col = i % 4
            
            alarm_frame = ttk.Frame(alarms_grid)
            alarm_frame.grid(row=row, column=col, padx=5, pady=5, sticky='w')
            
            # LED indicator
            led = tk.Canvas(alarm_frame, width=16, height=16, bg='#2c3e50', highlightthickness=0)
            led.pack(side='left', padx=(0, 5))
            led_circle = led.create_oval(2, 2, 14, 14, fill=self.led_colors['off'], outline='gray')
            
            # Alarm label
            label = ttk.Label(alarm_frame, text=alarm_name, font=('Arial', 9))
            label.pack(side='left')
            
            self.alarm_indicators[alarm_key] = {
                'led': led,
                'led_circle': led_circle,
                'label': label,
                'type': alarm_type
            }
        
        # Configure grid
        for i in range(4):
            alarms_grid.columnconfigure(i, weight=1)
        
        # Alarm summary
        summary_frame = ttk.Frame(alarms_frame)
        summary_frame.pack(fill='x', padx=10, pady=(0, 10))
        
        ttk.Label(summary_frame, text="Active Alarms:", font=('Arial', 10, 'bold')).pack(side='left')
        self.active_alarms_label = ttk.Label(summary_frame, text="None", foreground='green')
        self.active_alarms_label.pack(side='left', padx=(10, 0))
        
        # Acknowledge button
        ack_button = ttk.Button(summary_frame, text="Acknowledge All", command=self.acknowledge_alarms)
        ack_button.pack(side='right', padx=5)

    def acknowledge_alarms(self):
        """Acknowledge all active alarms"""
        for alarm_key in self.alarms:
            if alarm_key != 'emergency_stop':  # Emergency stop requires manual reset
                self.alarms[alarm_key] = False

    def create_process_data(self):
        """Create process data section"""
        process_frame = ttk.LabelFrame(self.scrollable_frame, text="Process Data", style='Title.TLabel')
        process_frame.pack(fill='x', padx=10, pady=5)
        
        data_notebook = ttk.Notebook(process_frame)
        data_notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Water Quality tab
        quality_frame = ttk.Frame(data_notebook)
        data_notebook.add(quality_frame, text="Water Quality")
        
        quality_grid = ttk.Frame(quality_frame)
        quality_grid.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Quality parameters in grid
        quality_params = [
            ('pH', 'ph'), ('TDS', 'tds'), ('Turbidity', 'turbidity'),
            ('Chlorine', 'chlorine'), ('Temperature', 'temperature'), ('Conductivity', 'conductivity')
        ]
        
        self.quality_labels = {}
        for i, (param_name, param_key) in enumerate(quality_params):
            row = i // 3
            col = i % 3
            
            param_frame = ttk.LabelFrame(quality_grid, text=param_name)
            param_frame.grid(row=row, column=col, padx=5, pady=5, sticky='ew')
            
            label = ttk.Label(param_frame, text="--", font=('Arial', 12, 'bold'))
            label.pack(padx=10, pady=10)
            self.quality_labels[param_key] = label
        
        # Configure grid weights
        for i in range(3):
            quality_grid.columnconfigure(i, weight=1)
        
        # Energy tab
        energy_frame = ttk.Frame(data_notebook)
        data_notebook.add(energy_frame, text="Energy")
        
        energy_grid = ttk.Frame(energy_frame)
        energy_grid.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.energy_labels = {}
        energy_params = [
            ('Total Power', 'total_power', 'kW'),
            ('Daily Consumption', 'daily_consumption', 'kWh'),
            ('Specific Energy', 'specific_energy', 'kWh/m³'),
            ('System Efficiency', 'efficiency', '%')
        ]
        
        for i, (param_name, param_key, unit) in enumerate(energy_params):
            param_frame = ttk.LabelFrame(energy_grid, text=param_name)
            param_frame.grid(row=i//2, column=i%2, padx=5, pady=5, sticky='ew')
            
            label = ttk.Label(param_frame, text=f"-- {unit}", font=('Arial', 12, 'bold'))
            label.pack(padx=10, pady=10)
            self.energy_labels[param_key] = (label, unit)
        
        energy_grid.columnconfigure(0, weight=1)
        energy_grid.columnconfigure(1, weight=1)

    def create_trends_section(self):
        """Create trends section with real-time plots"""
        trends_frame = ttk.LabelFrame(self.scrollable_frame, text="Real-Time Trends", style='Title.TLabel')
        trends_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Create matplotlib figure
        self.fig, ((self.ax1, self.ax2), (self.ax3, self.ax4)) = plt.subplots(2, 2, figsize=(12, 8))
        self.fig.patch.set_facecolor('#2c3e50')
        
        # Configure subplot styles
        for ax in [self.ax1, self.ax2, self.ax3, self.ax4]:
            ax.set_facecolor('#34495e')
            ax.tick_params(colors='white')
            ax.xaxis.label.set_color('white')
            ax.yaxis.label.set_color('white')
            ax.title.set_color('white')
        
        # Initialize data storage for trends
        self.trend_data = {
            'time': [],
            'production_rate': [],
            'tank_levels': [],
            'ro_pressure': [],
            'power_consumption': []
        }
        
        # Create canvas
        self.trends_canvas = FigureCanvasTkAgg(self.fig, trends_frame)
        self.trends_canvas.draw()
        self.trends_canvas.get_tk_widget().pack(fill='both', expand=True, padx=10, pady=10)

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
        
        messagebox.showwarning("Emergency Stop", "EMERGENCY STOP ACTIVATED!\nAll equipment stopped immediately.")

    def simulation_loop(self):
        """Main simulation loop"""
        simulation_time = 0.0
        
        while True:
            try:
                if self.running and not self.system_state['emergency_stop']:
                    # Update system based on running state
                    self.update_simulation(simulation_time)
                    simulation_time += 0.1  # 100ms simulation step
                
                # Log data
                self.log_system_data(simulation_time)
                
                time.sleep(0.1)  # 100ms real-time step
                
            except Exception as e:
                print(f"Simulation error: {e}")
                time.sleep(1)

    def update_simulation(self, simulation_time):
        """Update simulation calculations"""
        # Start pumps in sequence if system is running
        if self.system_state['running']:
            # Start intake pump first
            if simulation_time > 2.0:  # 2 second delay
                self.pumps['intake']['running'] = True
                self.pumps['intake']['speed'] = 85.0
                self.pumps['intake']['current'] = 12.5
                
            # Start prefilter pump
            if simulation_time > 5.0:
                self.pumps['prefilter']['running'] = True
                self.pumps['prefilter']['speed'] = 90.0
                self.pumps['prefilter']['current'] = 15.2
                
            # Start RO pump
            if simulation_time > 8.0:
                self.pumps['ro']['running'] = True
                self.pumps['ro']['speed'] = 92.0
                self.pumps['ro']['current'] = 18.7
                self.ro_system['pressure'] = 55.0 + random.uniform(-2, 2)
                
            # Start booster pumps
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
            self.total_produced += self.production_rate * (0.1/60)  # L per 0.1 second
        else:
            self.production_rate = 0.0
            self.ro_system['permeate_flow'] = 0.0
            self.ro_system['concentrate_flow'] = 0.0
            self.ro_system['recovery_rate'] = 0.0
        
        # Update tank levels
        if self.production_rate > 0:
            # Ground tank receives product water
            flow_in = self.production_rate * (0.1/60)  # L per 0.1 second
            self.ground_tank['volume'] += flow_in
            self.ground_tank['level'] = (self.ground_tank['volume'] / self.ground_tank['capacity']) * 100
            
            # Limit tank overflow
            if self.ground_tank['level'] > 95:
                self.ground_tank['level'] = 95
                self.ground_tank['volume'] = self.ground_tank['capacity'] * 0.95
        
        # Update water quality (product water)
        if self.production_rate > 0:
            self.product_water['tds'] = 150 + random.uniform(-20, 20)
            self.product_water['ph'] = 7.2 + random.uniform(-0.2, 0.2)
            self.product_water['turbidity'] = 0.1 + random.uniform(-0.05, 0.05)
            self.product_water['chlorine'] = 0.5 + random.uniform(-0.1, 0.1)
            self.product_water['conductivity'] = 250 + random.uniform(-30, 30)
        
        # Update energy consumption
        total_power = 0.0
        for pump_name, pump_data in self.pumps.items():
            if pump_data['running']:
                # Power consumption based on current
                power = pump_data['current'] * 0.4 * 0.85  # kW (assuming 400V, 85% efficiency)
                total_power += power
                pump_data['hours'] += 0.1/3600  # Add runtime hours
        
        self.energy['total_power'] = total_power
        self.energy['daily_consumption'] += total_power * (0.1/3600)  # kWh
          # Calculate specific energy consumption
        if self.production_rate > 0:
            self.energy['specific_energy'] = self.energy['total_power'] / (self.production_rate * 60 / 1000)  # kWh/m³
        
        # Check alarms
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
        
        # Check maintenance due (every 1000 hours)
        total_pump_hours = sum(pump['hours'] for pump in self.pumps.values())
        if total_pump_hours > 1000:
            self.alarms['maintenance_due'] = True

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
            # Read existing data
            if os.path.exists(self.log_file):
                with open(self.log_file, 'r') as f:
                    log_data = json.load(f)
            else:
                log_data = []
            
            # Add new data point
            log_data.append(data)
            
            # Keep only last 1000 entries
            if len(log_data) > 1000:
                log_data = log_data[-1000:]
            
            # Write back to file
            with open(self.log_file, 'w') as f:
                json.dump(log_data, f, indent=2)
                
        except Exception as e:
            print(f"Logging error: {e}")

    def gui_update_loop(self):
        """Update GUI elements in separate thread"""
        while True:
            try:
                self.root.after(0, self.update_gui_elements)
                time.sleep(0.5)  # Update GUI every 500ms
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
            self.roof_tank_label.config(text=f"{self.roof_tank['level']:.1f}%")
            self.ro_pressure_label.config(text=f"{self.ro_system['pressure']:.1f} bar")
            self.recovery_rate_label.config(text=f"{self.ro_system['recovery_rate']:.1f}%")
            self.power_label.config(text=f"{self.energy['total_power']:.1f} kW")
            self.efficiency_label.config(text=f"{self.energy['efficiency']:.1f}%")
            
            # Update pump status and LEDs
            for pump_name, pump_data in self.pumps.items():
                if pump_name in self.pump_labels:
                    if pump_data['running']:
                        status_text = f"RUNNING - {pump_data['current']:.1f} A"
                        led_status = 'running'
                    elif pump_data['fault']:
                        status_text = "FAULT"
                        led_status = 'fault'
                    else:
                        status_text = "STOPPED - 0.0 A"
                        led_status = 'off'
                    
                    self.pump_labels[pump_name].config(text=status_text)
                    if pump_name in self.pump_leds:
                        led_canvas, led_circle = self.pump_leds[pump_name]
                        self.update_led(led_canvas, led_circle, led_status)
            
            # Update tank progress bars
            self.ground_tank_progress['value'] = self.ground_tank['level']
            self.roof_tank_progress['value'] = self.roof_tank['level']
            
            # Update RO system LED
            if self.ro_system['pressure'] > 20:
                self.update_led(self.ro_led, self.ro_led_circle, 'running')
                self.ro_status_label.config(text=f"RO System: ONLINE - {self.ro_system['pressure']:.1f} bar")
            else:
                self.update_led(self.ro_led, self.ro_led_circle, 'off')
                self.ro_status_label.config(text="RO System: OFFLINE")
              # Update water quality parameters
            quality_data = {
                'ph': f"{self.product_water['ph']:.1f}",
                'tds': f"{self.product_water['tds']:.0f} ppm",
                'turbidity': f"{self.product_water['turbidity']:.2f} NTU",
                'chlorine': f"{self.product_water['chlorine']:.1f} mg/L",
                'temperature': f"{self.product_water['temperature']:.1f} °C",
                'conductivity': f"{self.product_water['conductivity']:.0f} µS/cm"
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
                    # Set LED color based on alarm type
                    if indicator['type'] == 'CRITICAL':
                        led_color = self.led_colors['fault']  # Red
                    elif indicator['type'] == 'ALARM':
                        led_color = self.led_colors['warning']  # Orange
                    elif indicator['type'] == 'WARNING':
                        led_color = self.led_colors['standby']  # Blue
                    else:  # INFO
                        led_color = self.led_colors['on']  # Green
                    
                    indicator['led'].itemconfig(indicator['led_circle'], fill=led_color)
                    active_alarms.append(alarm_key.replace('_', ' ').title())
                else:
                    indicator['led'].itemconfig(indicator['led_circle'], fill=self.led_colors['off'])
        
        # Update active alarms summary
        if active_alarms:
            alarm_text = ", ".join(active_alarms)
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
            
            # Keep only last 50 points
            max_points = 50
            for key in self.trend_data:
                if len(self.trend_data[key]) > max_points:
                    self.trend_data[key] = self.trend_data[key][-max_points:]
            
            # Clear and plot
            for ax in [self.ax1, self.ax2, self.ax3, self.ax4]:
                ax.clear()
                ax.set_facecolor('#34495e')
                ax.tick_params(colors='white')
                ax.xaxis.label.set_color('white')
                ax.yaxis.label.set_color('white')
                ax.title.set_color('white')
            
            if len(self.trend_data['time']) > 1:
                # Production rate
                self.ax1.plot(self.trend_data['time'], self.trend_data['production_rate'], 'g-', linewidth=2)
                self.ax1.set_title('Production Rate (L/min)')
                self.ax1.grid(True, alpha=0.3)
                
                # Tank levels
                self.ax2.plot(self.trend_data['time'], self.trend_data['tank_levels'], 'b-', linewidth=2)
                self.ax2.set_title('Ground Tank Level (%)')
                self.ax2.grid(True, alpha=0.3)
                
                # RO pressure
                self.ax3.plot(self.trend_data['time'], self.trend_data['ro_pressure'], 'r-', linewidth=2)
                self.ax3.set_title('RO Pressure (bar)')
                self.ax3.grid(True, alpha=0.3)
                
                # Power consumption
                self.ax4.plot(self.trend_data['time'], self.trend_data['power_consumption'], 'orange', linewidth=2)
                self.ax4.set_title('Power Consumption (kW)')
                self.ax4.grid(True, alpha=0.3)
                
                # Format x-axis
                for ax in [self.ax1, self.ax2, self.ax3, self.ax4]:
                    ax.tick_params(axis='x', rotation=45)
            
            plt.tight_layout()
            self.trends_canvas.draw()
            
        except Exception as e:
            print(f"Trend plot error: {e}")


def main():
    """Main function to start the integrated system"""
    root = tk.Tk()
    app = WaterTreatmentIntegratedSystem(root)
    
    try:
        root.mainloop()
    except KeyboardInterrupt:
        print("\nShutting down system...")
    except Exception as e:
        print(f"Application error: {e}")


if __name__ == "__main__":
    main()
