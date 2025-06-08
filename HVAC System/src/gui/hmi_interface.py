#!/usr/bin/env python3
"""
HVAC HMI Interface
Web-based Human Machine Interface for HVAC Control System
Provides real-time monitoring and control capabilities

Author: System Engineer
Date: June 8, 2025
Version: 1.0.0
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
import json
import math
import configparser
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.animation as animation

class HVACControlPanel:
    """Main HVAC control panel GUI"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("HVAC Control System - HMI Interface")
        self.root.geometry("1200x800")
        
        # Load configuration
        self.config = configparser.ConfigParser()
        self.config.read('config/plc_config.ini')
        
        # System data
        self.system_data = {
            'system_running': False,
            'outdoor_temp': 20.0,
            'zones': {},
            'equipment': {},
            'energy': {'consumed_today': 0.0, 'peak_demand': 0.0}
        }
        
        # Data for trending
        self.trend_data = {
            'timestamps': [],
            'outdoor_temp': [],
            'zone_temps': {i: [] for i in range(1, 9)},
            'energy_consumption': []
        }
        
        # Create GUI
        self.create_widgets()
        
        # Start data update thread
        self.running = True
        self.update_thread = threading.Thread(target=self.update_loop, daemon=True)
        self.update_thread.start()
    
    def create_widgets(self):
        """Create all GUI widgets"""
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Create tabs
        self.create_overview_tab()
        self.create_zones_tab()
        self.create_equipment_tab()
        self.create_trends_tab()
        self.create_alarms_tab()
        self.create_settings_tab()
    
    def create_overview_tab(self):
        """Create system overview tab"""
        self.overview_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.overview_frame, text="System Overview")
        
        # System status frame
        status_frame = ttk.LabelFrame(self.overview_frame, text="System Status")
        status_frame.grid(row=0, column=0, columnspan=2, sticky='ew', padx=5, pady=5)
        
        self.system_status_label = tk.Label(status_frame, text="System: STOPPED", 
                                          font=('Arial', 14, 'bold'), fg='red')
        self.system_status_label.grid(row=0, column=0, padx=10, pady=5)
        
        self.start_button = tk.Button(status_frame, text="START SYSTEM", 
                                    command=self.start_system, bg='green', fg='white',
                                    font=('Arial', 12, 'bold'))
        self.start_button.grid(row=0, column=1, padx=10, pady=5)
        
        self.stop_button = tk.Button(status_frame, text="STOP SYSTEM", 
                                   command=self.stop_system, bg='red', fg='white',
                                   font=('Arial', 12, 'bold'))
        self.stop_button.grid(row=0, column=2, padx=10, pady=5)
        
        self.emergency_button = tk.Button(status_frame, text="EMERGENCY STOP", 
                                        command=self.emergency_stop, bg='darkred', fg='white',
                                        font=('Arial', 12, 'bold'))
        self.emergency_button.grid(row=0, column=3, padx=10, pady=5)
        
        # Outdoor conditions frame
        outdoor_frame = ttk.LabelFrame(self.overview_frame, text="Outdoor Conditions")
        outdoor_frame.grid(row=1, column=0, sticky='ew', padx=5, pady=5)
        
        self.outdoor_temp_label = tk.Label(outdoor_frame, text="Temperature: --°C", font=('Arial', 12))
        self.outdoor_temp_label.grid(row=0, column=0, padx=10, pady=5, sticky='w')
        
        self.outdoor_humidity_label = tk.Label(outdoor_frame, text="Humidity: --%", font=('Arial', 12))
        self.outdoor_humidity_label.grid(row=1, column=0, padx=10, pady=5, sticky='w')
        
        # Energy information frame
        energy_frame = ttk.LabelFrame(self.overview_frame, text="Energy Information")
        energy_frame.grid(row=1, column=1, sticky='ew', padx=5, pady=5)
        
        self.energy_consumed_label = tk.Label(energy_frame, text="Consumed Today: -- kWh", font=('Arial', 12))
        self.energy_consumed_label.grid(row=0, column=0, padx=10, pady=5, sticky='w')
        
        self.peak_demand_label = tk.Label(energy_frame, text="Peak Demand: -- kW", font=('Arial', 12))
        self.peak_demand_label.grid(row=1, column=0, padx=10, pady=5, sticky='w')
        
        # Zone summary frame
        zones_summary_frame = ttk.LabelFrame(self.overview_frame, text="Zone Summary")
        zones_summary_frame.grid(row=2, column=0, columnspan=2, sticky='ew', padx=5, pady=5)
        
        # Create zone summary table
        columns = ('Zone', 'Temperature', 'Setpoint', 'Status', 'Occupancy')
        self.zones_tree = ttk.Treeview(zones_summary_frame, columns=columns, show='headings', height=8)
        
        for col in columns:
            self.zones_tree.heading(col, text=col)
            self.zones_tree.column(col, width=120)
        
        self.zones_tree.grid(row=0, column=0, sticky='ew', padx=5, pady=5)
        
        # Scrollbar for zones tree
        zones_scrollbar = ttk.Scrollbar(zones_summary_frame, orient='vertical', command=self.zones_tree.yview)
        zones_scrollbar.grid(row=0, column=1, sticky='ns')
        self.zones_tree.configure(yscrollcommand=zones_scrollbar.set)
    
    def create_zones_tab(self):
        """Create zones control tab"""
        self.zones_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.zones_frame, text="Zone Control")
        
        # Zone control widgets
        self.zone_controls = {}
        
        for i in range(1, 9):
            zone_frame = ttk.LabelFrame(self.zones_frame, text=f"Zone {i}")
            row = (i - 1) // 4
            col = (i - 1) % 4
            zone_frame.grid(row=row, column=col, padx=5, pady=5, sticky='ew')
            
            # Zone name
            name_label = tk.Label(zone_frame, text=f"Zone {i}", font=('Arial', 10, 'bold'))
            name_label.grid(row=0, column=0, columnspan=2, pady=2)
            
            # Current temperature
            temp_label = tk.Label(zone_frame, text="Current: --°C")
            temp_label.grid(row=1, column=0, columnspan=2, pady=2)
            
            # Setpoint control
            setpoint_label = tk.Label(zone_frame, text="Setpoint:")
            setpoint_label.grid(row=2, column=0, pady=2, sticky='w')
            
            setpoint_var = tk.DoubleVar(value=22.0)
            setpoint_spinbox = tk.Spinbox(zone_frame, from_=15.0, to=30.0, 
                                        textvariable=setpoint_var, width=8,
                                        increment=0.5, format="%.1f")
            setpoint_spinbox.grid(row=2, column=1, pady=2)
            
            # Status indicators
            status_label = tk.Label(zone_frame, text="Status: Normal", fg='green')
            status_label.grid(row=3, column=0, columnspan=2, pady=2)
            
            # Store references
            self.zone_controls[i] = {
                'name_label': name_label,
                'temp_label': temp_label,
                'setpoint_var': setpoint_var,
                'setpoint_spinbox': setpoint_spinbox,
                'status_label': status_label
            }
    
    def create_equipment_tab(self):
        """Create equipment status tab"""
        self.equipment_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.equipment_frame, text="Equipment Status")
        
        # Fans frame
        fans_frame = ttk.LabelFrame(self.equipment_frame, text="Fans")
        fans_frame.grid(row=0, column=0, sticky='ew', padx=5, pady=5)
        
        self.supply_fan_label = tk.Label(fans_frame, text="Supply Fan: OFF (0%)", font=('Arial', 12))
        self.supply_fan_label.grid(row=0, column=0, padx=10, pady=5, sticky='w')
        
        self.return_fan_label = tk.Label(fans_frame, text="Return Fan: OFF (0%)", font=('Arial', 12))
        self.return_fan_label.grid(row=1, column=0, padx=10, pady=5, sticky='w')
        
        # Heating/Cooling frame
        hvac_frame = ttk.LabelFrame(self.equipment_frame, text="Heating & Cooling")
        hvac_frame.grid(row=0, column=1, sticky='ew', padx=5, pady=5)
        
        self.heating_stage1_label = tk.Label(hvac_frame, text="Heating Stage 1: OFF", font=('Arial', 12))
        self.heating_stage1_label.grid(row=0, column=0, padx=10, pady=5, sticky='w')
        
        self.heating_stage2_label = tk.Label(hvac_frame, text="Heating Stage 2: OFF", font=('Arial', 12))
        self.heating_stage2_label.grid(row=1, column=0, padx=10, pady=5, sticky='w')
        
        self.cooling_stage1_label = tk.Label(hvac_frame, text="Cooling Stage 1: OFF", font=('Arial', 12))
        self.cooling_stage1_label.grid(row=2, column=0, padx=10, pady=5, sticky='w')
        
        self.cooling_stage2_label = tk.Label(hvac_frame, text="Cooling Stage 2: OFF", font=('Arial', 12))
        self.cooling_stage2_label.grid(row=3, column=0, padx=10, pady=5, sticky='w')
        
        # Air handling frame
        air_frame = ttk.LabelFrame(self.equipment_frame, text="Air Handling")
        air_frame.grid(row=1, column=0, columnspan=2, sticky='ew', padx=5, pady=5)
        
        self.outside_air_label = tk.Label(air_frame, text="Outside Air Damper: --%", font=('Arial', 12))
        self.outside_air_label.grid(row=0, column=0, padx=10, pady=5, sticky='w')
        
        self.economizer_label = tk.Label(air_frame, text="Economizer: INACTIVE", font=('Arial', 12))
        self.economizer_label.grid(row=1, column=0, padx=10, pady=5, sticky='w')
    
    def create_trends_tab(self):
        """Create trends and graphs tab"""
        self.trends_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.trends_frame, text="Trends")
        
        # Create matplotlib figure
        self.fig = Figure(figsize=(12, 8), dpi=100)
        
        # Temperature trend subplot
        self.temp_subplot = self.fig.add_subplot(3, 1, 1)
        self.temp_subplot.set_title('Temperature Trends')
        self.temp_subplot.set_ylabel('Temperature (°C)')
        self.temp_subplot.grid(True)
        
        # Energy consumption subplot
        self.energy_subplot = self.fig.add_subplot(3, 1, 2)
        self.energy_subplot.set_title('Energy Consumption')
        self.energy_subplot.set_ylabel('Energy (kWh)')
        self.energy_subplot.grid(True)
        
        # Equipment status subplot
        self.equipment_subplot = self.fig.add_subplot(3, 1, 3)
        self.equipment_subplot.set_title('Equipment Status')
        self.equipment_subplot.set_ylabel('Status')
        self.equipment_subplot.set_xlabel('Time')
        self.equipment_subplot.grid(True)
        
        # Embed in tkinter
        self.canvas = FigureCanvasTkAgg(self.fig, self.trends_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill='both', expand=True)
    
    def create_alarms_tab(self):
        """Create alarms and alerts tab"""
        self.alarms_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.alarms_frame, text="Alarms")
        
        # Active alarms frame
        active_alarms_frame = ttk.LabelFrame(self.alarms_frame, text="Active Alarms")
        active_alarms_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Alarms listbox
        self.alarms_listbox = tk.Listbox(active_alarms_frame, height=15, font=('Arial', 10))
        self.alarms_listbox.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Alarm control buttons
        alarm_buttons_frame = tk.Frame(active_alarms_frame)
        alarm_buttons_frame.pack(fill='x', padx=5, pady=5)
        
        acknowledge_button = tk.Button(alarm_buttons_frame, text="Acknowledge", 
                                     command=self.acknowledge_alarm)
        acknowledge_button.pack(side='left', padx=5)
        
        clear_button = tk.Button(alarm_buttons_frame, text="Clear All", 
                               command=self.clear_alarms)
        clear_button.pack(side='left', padx=5)
    
    def create_settings_tab(self):
        """Create system settings tab"""
        self.settings_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.settings_frame, text="Settings")
        
        # Schedule settings
        schedule_frame = ttk.LabelFrame(self.settings_frame, text="Operating Schedule")
        schedule_frame.grid(row=0, column=0, sticky='ew', padx=5, pady=5)
        
        tk.Label(schedule_frame, text="Weekday Start:").grid(row=0, column=0, padx=5, pady=2, sticky='w')
        self.weekday_start_var = tk.StringVar(value="07:00")
        weekday_start_entry = tk.Entry(schedule_frame, textvariable=self.weekday_start_var, width=10)
        weekday_start_entry.grid(row=0, column=1, padx=5, pady=2)
        
        tk.Label(schedule_frame, text="Weekday End:").grid(row=1, column=0, padx=5, pady=2, sticky='w')
        self.weekday_end_var = tk.StringVar(value="18:00")
        weekday_end_entry = tk.Entry(schedule_frame, textvariable=self.weekday_end_var, width=10)
        weekday_end_entry.grid(row=1, column=1, padx=5, pady=2)
        
        # Global setpoints
        setpoints_frame = ttk.LabelFrame(self.settings_frame, text="Global Setpoints")
        setpoints_frame.grid(row=0, column=1, sticky='ew', padx=5, pady=5)
        
        tk.Label(setpoints_frame, text="Heating Setback:").grid(row=0, column=0, padx=5, pady=2, sticky='w')
        self.heating_setback_var = tk.DoubleVar(value=18.0)
        heating_setback_spinbox = tk.Spinbox(setpoints_frame, from_=15.0, to=25.0,
                                           textvariable=self.heating_setback_var,
                                           width=8, increment=0.5, format="%.1f")
        heating_setback_spinbox.grid(row=0, column=1, padx=5, pady=2)
        
        tk.Label(setpoints_frame, text="Cooling Setback:").grid(row=1, column=0, padx=5, pady=2, sticky='w')
        self.cooling_setback_var = tk.DoubleVar(value=27.0)
        cooling_setback_spinbox = tk.Spinbox(setpoints_frame, from_=20.0, to=35.0,
                                           textvariable=self.cooling_setback_var,
                                           width=8, increment=0.5, format="%.1f")
        cooling_setback_spinbox.grid(row=1, column=1, padx=5, pady=2)
        
        # Apply settings button
        apply_button = tk.Button(self.settings_frame, text="Apply Settings", 
                               command=self.apply_settings, bg='blue', fg='white')
        apply_button.grid(row=1, column=0, columnspan=2, pady=10)
    
    def start_system(self):
        """Start the HVAC system"""
        self.system_data['system_running'] = True
        self.system_status_label.config(text="System: RUNNING", fg='green')
        self.add_alarm("INFO: System started by operator")
    
    def stop_system(self):
        """Stop the HVAC system"""
        self.system_data['system_running'] = False
        self.system_status_label.config(text="System: STOPPED", fg='red')
        self.add_alarm("INFO: System stopped by operator")
    
    def emergency_stop(self):
        """Emergency stop the system"""
        result = messagebox.askyesno("Emergency Stop", 
                                   "Are you sure you want to perform an emergency stop?")
        if result:
            self.system_data['system_running'] = False
            self.system_status_label.config(text="System: EMERGENCY STOP", fg='darkred')
            self.add_alarm("CRITICAL: Emergency stop activated")
    
    def acknowledge_alarm(self):
        """Acknowledge selected alarm"""
        selection = self.alarms_listbox.curselection()
        if selection:
            self.alarms_listbox.delete(selection[0])
    
    def clear_alarms(self):
        """Clear all alarms"""
        self.alarms_listbox.delete(0, tk.END)
    
    def add_alarm(self, message):
        """Add alarm to the alarms list"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        alarm_text = f"{timestamp} - {message}"
        self.alarms_listbox.insert(0, alarm_text)
        
        # Keep only last 50 alarms
        if self.alarms_listbox.size() > 50:
            self.alarms_listbox.delete(49, tk.END)
    
    def apply_settings(self):
        """Apply system settings"""
        messagebox.showinfo("Settings", "Settings applied successfully")
        self.add_alarm("INFO: System settings updated")
    
    def update_display(self):
        """Update all display elements with current data"""
        # Update outdoor conditions
        self.outdoor_temp_label.config(text=f"Temperature: {self.system_data.get('outdoor_temp', 0):.1f}°C")
        outdoor_humidity = self.system_data.get('outdoor_humidity', 0)
        self.outdoor_humidity_label.config(text=f"Humidity: {outdoor_humidity:.1f}%")
        
        # Update energy information
        energy = self.system_data.get('energy', {})
        self.energy_consumed_label.config(text=f"Consumed Today: {energy.get('consumed_today', 0):.1f} kWh")
        self.peak_demand_label.config(text=f"Peak Demand: {energy.get('peak_demand', 0):.1f} kW")
        
        # Update zones tree
        self.zones_tree.delete(*self.zones_tree.get_children())
        zones = self.system_data.get('zones', {})
        
        for zone_id, zone_data in zones.items():
            if isinstance(zone_data, dict):
                name = zone_data.get('name', f'Zone {zone_id}')
                temp = zone_data.get('temperature', 0)
                setpoint = zone_data.get('setpoint', 0)
                
                # Determine status
                if zone_data.get('heating_demand', False):
                    status = "Heating"
                elif zone_data.get('cooling_demand', False):
                    status = "Cooling"
                else:
                    status = "Normal"
                
                occupancy = "Occupied" if zone_data.get('occupancy', False) else "Vacant"
                
                self.zones_tree.insert('', 'end', values=(
                    name, f"{temp:.1f}°C", f"{setpoint:.1f}°C", status, occupancy
                ))
        
        # Update zone controls
        for zone_id, controls in self.zone_controls.items():
            if str(zone_id) in zones:
                zone_data = zones[str(zone_id)]
                name = zone_data.get('name', f'Zone {zone_id}')
                temp = zone_data.get('temperature', 0)
                
                controls['name_label'].config(text=name)
                controls['temp_label'].config(text=f"Current: {temp:.1f}°C")
                
                # Update status color
                if zone_data.get('heating_demand', False):
                    controls['status_label'].config(text="Status: Heating", fg='red')
                elif zone_data.get('cooling_demand', False):
                    controls['status_label'].config(text="Status: Cooling", fg='blue')
                else:
                    controls['status_label'].config(text="Status: Normal", fg='green')
        
        # Update equipment status
        equipment = self.system_data.get('equipment', {})
        
        supply_fan_running = equipment.get('supply_fan_running', False)
        supply_fan_speed = equipment.get('supply_fan_speed', 0)
        self.supply_fan_label.config(
            text=f"Supply Fan: {'ON' if supply_fan_running else 'OFF'} ({supply_fan_speed:.0f}%)",
            fg='green' if supply_fan_running else 'red'
        )
        
        return_fan_running = equipment.get('return_fan_running', False)
        return_fan_speed = equipment.get('return_fan_speed', 0)
        self.return_fan_label.config(
            text=f"Return Fan: {'ON' if return_fan_running else 'OFF'} ({return_fan_speed:.0f}%)",
            fg='green' if return_fan_running else 'red'
        )
        
        # Heating/Cooling status
        heating_stage1 = equipment.get('heating_stage_1', False)
        self.heating_stage1_label.config(
            text=f"Heating Stage 1: {'ON' if heating_stage1 else 'OFF'}",
            fg='red' if heating_stage1 else 'gray'
        )
        
        heating_stage2 = equipment.get('heating_stage_2', False)
        self.heating_stage2_label.config(
            text=f"Heating Stage 2: {'ON' if heating_stage2 else 'OFF'}",
            fg='red' if heating_stage2 else 'gray'
        )
        
        cooling_stage1 = equipment.get('cooling_stage_1', False)
        self.cooling_stage1_label.config(
            text=f"Cooling Stage 1: {'ON' if cooling_stage1 else 'OFF'}",
            fg='blue' if cooling_stage1 else 'gray'
        )
        
        cooling_stage2 = equipment.get('cooling_stage_2', False)
        self.cooling_stage2_label.config(
            text=f"Cooling Stage 2: {'ON' if cooling_stage2 else 'OFF'}",
            fg='blue' if cooling_stage2 else 'gray'
        )
        
        # Air handling
        outside_air_damper = equipment.get('outside_air_damper', 0)
        self.outside_air_label.config(text=f"Outside Air Damper: {outside_air_damper:.0f}%")
        
        economizer_active = equipment.get('economizer_active', False)
        self.economizer_label.config(
            text=f"Economizer: {'ACTIVE' if economizer_active else 'INACTIVE'}",
            fg='green' if economizer_active else 'gray'
        )
    
    def update_trends(self):
        """Update trend graphs"""
        # Update data lists (keep last 50 points)
        current_time = datetime.now()
        self.trend_data['timestamps'].append(current_time)
        self.trend_data['outdoor_temp'].append(self.system_data.get('outdoor_temp', 0))
        self.trend_data['energy_consumption'].append(
            self.system_data.get('energy', {}).get('consumed_today', 0)
        )
        
        # Keep only last 50 data points
        for key in self.trend_data:
            if len(self.trend_data[key]) > 50:
                self.trend_data[key] = self.trend_data[key][-50:]
        
        # Clear and redraw plots
        self.temp_subplot.clear()
        self.energy_subplot.clear()
        self.equipment_subplot.clear()
        
        if len(self.trend_data['timestamps']) > 1:
            # Temperature trends
            self.temp_subplot.plot(self.trend_data['timestamps'], 
                                 self.trend_data['outdoor_temp'], 
                                 label='Outdoor', color='blue')
            
            # Zone temperatures
            zones = self.system_data.get('zones', {})
            for zone_id, zone_data in zones.items():
                if isinstance(zone_data, dict):
                    zone_name = zone_data.get('name', f'Zone {zone_id}')
                    zone_temp = zone_data.get('temperature', 0)
                    
                    if zone_id not in self.trend_data['zone_temps']:
                        self.trend_data['zone_temps'][zone_id] = []
                    
                    self.trend_data['zone_temps'][zone_id].append(zone_temp)
                    if len(self.trend_data['zone_temps'][zone_id]) > 50:
                        self.trend_data['zone_temps'][zone_id] = self.trend_data['zone_temps'][zone_id][-50:]
                    
                    if len(self.trend_data['zone_temps'][zone_id]) == len(self.trend_data['timestamps']):
                        self.temp_subplot.plot(self.trend_data['timestamps'],
                                             self.trend_data['zone_temps'][zone_id],
                                             label=zone_name, alpha=0.7)
            
            self.temp_subplot.set_title('Temperature Trends')
            self.temp_subplot.set_ylabel('Temperature (°C)')
            self.temp_subplot.legend()
            self.temp_subplot.grid(True)
            
            # Energy consumption
            self.energy_subplot.plot(self.trend_data['timestamps'], 
                                   self.trend_data['energy_consumption'], 
                                   color='green')
            self.energy_subplot.set_title('Energy Consumption')
            self.energy_subplot.set_ylabel('Energy (kWh)')
            self.energy_subplot.grid(True)
            
            # Equipment status (simplified)
            equipment = self.system_data.get('equipment', {})
            equipment_status = []
            for timestamp in self.trend_data['timestamps']:
                status_value = 0
                if equipment.get('supply_fan_running', False):
                    status_value += 1
                if equipment.get('heating_stage_1', False):
                    status_value += 2
                if equipment.get('cooling_stage_1', False):
                    status_value += 4
                equipment_status.append(status_value)
            
            self.equipment_subplot.plot(self.trend_data['timestamps'], 
                                      equipment_status, 
                                      color='red', marker='o')
            self.equipment_subplot.set_title('Equipment Status')
            self.equipment_subplot.set_ylabel('Status Code')
            self.equipment_subplot.set_xlabel('Time')
            self.equipment_subplot.grid(True)
        
        # Redraw canvas
        self.canvas.draw()
    
    def simulate_data_update(self):
        """Simulate data update (replace with actual data source)"""
        import random
        
        # Simulate outdoor temperature variation
        current_hour = datetime.now().hour
        base_temp = 20.0 + 8.0 * math.sin((current_hour - 6) * math.pi / 12)
        self.system_data['outdoor_temp'] = base_temp + random.uniform(-2, 2)
        self.system_data['outdoor_humidity'] = 60.0 + random.uniform(-10, 10)
        
        # Simulate zone data
        for i in range(1, 9):
            zone_names = {
                1: "Lobby", 2: "Conference Room", 3: "Office Area 1", 4: "Office Area 2",
                5: "Kitchen", 6: "Server Room", 7: "Storage", 8: "Break Room"
            }
            
            if str(i) not in self.system_data.get('zones', {}):
                self.system_data.setdefault('zones', {})[str(i)] = {}
            
            zone = self.system_data['zones'][str(i)]
            zone['name'] = zone_names.get(i, f'Zone {i}')
            zone['temperature'] = 22.0 + random.uniform(-3, 3)
            zone['setpoint'] = 22.0
            zone['humidity'] = 50.0 + random.uniform(-5, 5)
            zone['co2_level'] = 400 + random.randint(0, 200)
            zone['occupancy'] = random.choice([True, False])
            zone['heating_demand'] = zone['temperature'] < zone['setpoint'] - 0.5
            zone['cooling_demand'] = zone['temperature'] > zone['setpoint'] + 0.5
        
        # Simulate equipment status
        if self.system_data.get('system_running', False):
            any_heating = any(zone.get('heating_demand', False) 
                            for zone in self.system_data.get('zones', {}).values())
            any_cooling = any(zone.get('cooling_demand', False) 
                            for zone in self.system_data.get('zones', {}).values())
            
            equipment = self.system_data.setdefault('equipment', {})
            equipment['supply_fan_running'] = any_heating or any_cooling
            equipment['supply_fan_speed'] = 50.0 if equipment['supply_fan_running'] else 0.0
            equipment['return_fan_running'] = equipment['supply_fan_running']
            equipment['return_fan_speed'] = equipment['supply_fan_speed'] * 0.9
            equipment['heating_stage_1'] = any_heating
            equipment['heating_stage_2'] = False
            equipment['cooling_stage_1'] = any_cooling
            equipment['cooling_stage_2'] = False
            equipment['outside_air_damper'] = 15.0 + random.uniform(0, 10)
            equipment['economizer_active'] = False
        else:
            equipment = self.system_data.setdefault('equipment', {})
            for key in equipment:
                if 'running' in key or 'stage' in key or 'active' in key:
                    equipment[key] = False
                elif 'speed' in key:
                    equipment[key] = 0.0
                elif 'damper' in key:
                    equipment[key] = 0.0
        
        # Simulate energy data
        energy = self.system_data.setdefault('energy', {})
        energy['consumed_today'] = energy.get('consumed_today', 0) + random.uniform(0, 0.1)
        energy['peak_demand'] = max(energy.get('peak_demand', 0), random.uniform(20, 50))
    
    def update_loop(self):
        """Main update loop running in separate thread"""
        while self.running:
            try:
                # Simulate data update (replace with actual data source)
                self.simulate_data_update()
                
                # Schedule GUI updates on main thread
                self.root.after_idle(self.update_display)
                self.root.after_idle(self.update_trends)
                
                time.sleep(5)  # Update every 5 seconds
                
            except Exception as e:
                print(f"Update error: {e}")
                time.sleep(1)
    
    def on_closing(self):
        """Handle application closing"""
        self.running = False
        self.root.quit()
        self.root.destroy()


def main():
    """Main function"""
    
    root = tk.Tk()
    app = HVACControlPanel(root)
    
    # Handle window closing
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    
    try:
        root.mainloop()
    except KeyboardInterrupt:
        app.on_closing()


if __name__ == "__main__":
    main()
