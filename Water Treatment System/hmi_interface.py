#!/usr/bin/env python3
"""
HMI Interface for Water Treatment System
Advanced operator interface with real-time monitoring and control
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from datetime import datetime, timedelta
import threading
import time
import json

class WaterTreatmentHMI:
    def __init__(self, root):
        self.root = root
        self.root.title("Water Treatment System - HMI Interface")
        self.root.geometry("1400x900")
        self.root.configure(bg='#2c3e50')
        
        # System data
        self.system_data = {
            'seawater_tank': {'level': 85.0, 'volume': 8500},
            'treated_tank': {'level': 62.0, 'volume': 6200},
            'roof_tanks': [
                {'id': 1, 'level': 78.0, 'volume': 7800, 'zone': 'North'},
                {'id': 2, 'level': 65.0, 'volume': 6500, 'zone': 'South'},
                {'id': 3, 'level': 71.0, 'volume': 7100, 'zone': 'East'}
            ],
            'ro_system': {
                'pressure': 55.2, 'flow_rate': 167.5, 'recovery': 45.2,
                'membrane_hours': 2847, 'efficiency': 92.1
            },
            'pumps': [
                {'id': 1, 'status': 'Running', 'flow': 125.3, 'pressure': 4.2, 'runtime': 1247},
                {'id': 2, 'status': 'Standby', 'flow': 0.0, 'pressure': 0.0, 'runtime': 1156},
                {'id': 3, 'status': 'Running', 'flow': 98.7, 'pressure': 3.8, 'runtime': 1089}
            ],
            'water_quality': {
                'ph': 7.2, 'chlorine': 0.8, 'tds': 185, 'turbidity': 0.12,
                'temperature': 22.5, 'conductivity': 280
            },
            'alarms': [],
            'energy': {'consumption': 125.8, 'efficiency': 88.5}
        }
        
        self.running = True
        self.setup_ui()
        self.start_data_update()
        
    def setup_ui(self):
        """Setup the main UI layout"""
        # Main container
        main_frame = tk.Frame(self.root, bg='#2c3e50')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title
        title_label = tk.Label(main_frame, text="Water Treatment System Control Center", 
                              font=('Arial', 24, 'bold'), fg='white', bg='#2c3e50')
        title_label.pack(pady=(0, 20))
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Create tabs
        self.create_overview_tab()
        self.create_process_tab()
        self.create_tanks_tab()
        self.create_quality_tab()
        self.create_alarms_tab()
        self.create_trends_tab()
        
    def create_overview_tab(self):
        """Create system overview tab"""
        overview_frame = ttk.Frame(self.notebook)
        self.notebook.add(overview_frame, text="System Overview")
        
        # System status grid
        status_frame = tk.LabelFrame(overview_frame, text="System Status", 
                                   font=('Arial', 14, 'bold'), bg='white')
        status_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Production metrics
        metrics_frame = tk.Frame(status_frame, bg='white')
        metrics_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.production_label = tk.Label(metrics_frame, text="Production Rate: 167.5 L/min", 
                                       font=('Arial', 12, 'bold'), bg='white')
        self.production_label.grid(row=0, column=0, padx=20)
        
        self.efficiency_label = tk.Label(metrics_frame, text="System Efficiency: 92.1%", 
                                       font=('Arial', 12, 'bold'), bg='white')
        self.efficiency_label.grid(row=0, column=1, padx=20)
        
        self.energy_label = tk.Label(metrics_frame, text="Power Consumption: 125.8 kW", 
                                   font=('Arial', 12, 'bold'), bg='white')
        self.energy_label.grid(row=0, column=2, padx=20)
        
        # Tank levels display
        tanks_frame = tk.Frame(status_frame, bg='white')
        tanks_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.create_tank_displays(tanks_frame)
        
        # Control buttons
        control_frame = tk.Frame(overview_frame, bg='white')
        control_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.start_btn = tk.Button(control_frame, text="Start System", bg='#27ae60', 
                                 fg='white', font=('Arial', 12, 'bold'), 
                                 command=self.start_system, width=15)
        self.start_btn.pack(side=tk.LEFT, padx=10)
        
        self.stop_btn = tk.Button(control_frame, text="Stop System", bg='#e74c3c', 
                                fg='white', font=('Arial', 12, 'bold'), 
                                command=self.stop_system, width=15)
        self.stop_btn.pack(side=tk.LEFT, padx=10)
        
        self.emergency_btn = tk.Button(control_frame, text="EMERGENCY STOP", bg='#c0392b', 
                                     fg='white', font=('Arial', 12, 'bold'), 
                                     command=self.emergency_stop, width=20)
        self.emergency_btn.pack(side=tk.RIGHT, padx=10)
        
    def create_process_tab(self):
        """Create process control tab"""
        process_frame = ttk.Frame(self.notebook)
        self.notebook.add(process_frame, text="Process Control")
        
        # RO System control
        ro_frame = tk.LabelFrame(process_frame, text="Reverse Osmosis System", 
                               font=('Arial', 14, 'bold'), bg='white')
        ro_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ro_metrics = tk.Frame(ro_frame, bg='white')
        ro_metrics.pack(fill=tk.X, padx=10, pady=10)
        
        self.ro_pressure_label = tk.Label(ro_metrics, text="Pressure: 55.2 bar", 
                                        font=('Arial', 12), bg='white')
        self.ro_pressure_label.grid(row=0, column=0, padx=20)
        
        self.ro_flow_label = tk.Label(ro_metrics, text="Flow Rate: 167.5 L/min", 
                                    font=('Arial', 12), bg='white')
        self.ro_flow_label.grid(row=0, column=1, padx=20)
        
        self.ro_recovery_label = tk.Label(ro_metrics, text="Recovery: 45.2%", 
                                        font=('Arial', 12), bg='white')
        self.ro_recovery_label.grid(row=0, column=2, padx=20)
        
        # Pump control
        pump_frame = tk.LabelFrame(process_frame, text="Pump Control", 
                                 font=('Arial', 14, 'bold'), bg='white')
        pump_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.create_pump_controls(pump_frame)
        
    def create_tanks_tab(self):
        """Create tank monitoring tab"""
        tanks_frame = ttk.Frame(self.notebook)
        self.notebook.add(tanks_frame, text="Tank Monitoring")
        
        # Detailed tank information
        for i, tank in enumerate(self.system_data['roof_tanks']):
            tank_frame = tk.LabelFrame(tanks_frame, text=f"Roof Tank {tank['id']} - {tank['zone']} Zone", 
                                     font=('Arial', 12, 'bold'), bg='white')
            tank_frame.pack(fill=tk.X, padx=10, pady=5)
            
            info_frame = tk.Frame(tank_frame, bg='white')
            info_frame.pack(fill=tk.X, padx=10, pady=5)
            
            tk.Label(info_frame, text=f"Level: {tank['level']:.1f}%", 
                   font=('Arial', 10), bg='white').grid(row=0, column=0, padx=10)
            tk.Label(info_frame, text=f"Volume: {tank['volume']} L", 
                   font=('Arial', 10), bg='white').grid(row=0, column=1, padx=10)
            tk.Label(info_frame, text=f"Zone: {tank['zone']}", 
                   font=('Arial', 10), bg='white').grid(row=0, column=2, padx=10)
            
    def create_quality_tab(self):
        """Create water quality monitoring tab"""
        quality_frame = ttk.Frame(self.notebook)
        self.notebook.add(quality_frame, text="Water Quality")
        
        # Quality parameters
        params_frame = tk.LabelFrame(quality_frame, text="Quality Parameters", 
                                   font=('Arial', 14, 'bold'), bg='white')
        params_frame.pack(fill=tk.X, padx=10, pady=10)
        
        params_grid = tk.Frame(params_frame, bg='white')
        params_grid.pack(padx=10, pady=10)
        
        quality = self.system_data['water_quality']
        
        self.ph_label = tk.Label(params_grid, text=f"pH: {quality['ph']:.1f}", 
                               font=('Arial', 12), bg='white')
        self.ph_label.grid(row=0, column=0, padx=20, pady=5)
        
        self.chlorine_label = tk.Label(params_grid, text=f"Free Chlorine: {quality['chlorine']:.1f} ppm", 
                                     font=('Arial', 12), bg='white')
        self.chlorine_label.grid(row=0, column=1, padx=20, pady=5)
        
        self.tds_label = tk.Label(params_grid, text=f"TDS: {quality['tds']} ppm", 
                                font=('Arial', 12), bg='white')
        self.tds_label.grid(row=1, column=0, padx=20, pady=5)
        
        self.turbidity_label = tk.Label(params_grid, text=f"Turbidity: {quality['turbidity']:.2f} NTU", 
                                      font=('Arial', 12), bg='white')
        self.turbidity_label.grid(row=1, column=1, padx=20, pady=5)
        
    def create_alarms_tab(self):
        """Create alarms and events tab"""
        alarms_frame = ttk.Frame(self.notebook)
        self.notebook.add(alarms_frame, text="Alarms & Events")
        
        # Alarms list
        alarms_list_frame = tk.LabelFrame(alarms_frame, text="Active Alarms", 
                                        font=('Arial', 14, 'bold'), bg='white')
        alarms_list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Treeview for alarms
        columns = ('Time', 'Priority', 'Description', 'Status')
        self.alarms_tree = ttk.Treeview(alarms_list_frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            self.alarms_tree.heading(col, text=col)
            self.alarms_tree.column(col, width=200)
        
        self.alarms_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Add sample alarms
        sample_alarms = [
            ('2024-01-15 10:30:25', 'Medium', 'RO Membrane pressure high', 'Active'),
            ('2024-01-15 09:45:12', 'Low', 'Pump 2 runtime exceeded schedule', 'Acknowledged'),
            ('2024-01-15 08:20:33', 'High', 'Water quality pH out of range', 'Cleared')
        ]
        
        for alarm in sample_alarms:
            self.alarms_tree.insert('', 'end', values=alarm)
        
    def create_trends_tab(self):
        """Create trends and analytics tab"""
        trends_frame = ttk.Frame(self.notebook)
        self.notebook.add(trends_frame, text="Trends & Analytics")
        
        # Create matplotlib figure
        self.fig, ((self.ax1, self.ax2), (self.ax3, self.ax4)) = plt.subplots(2, 2, figsize=(12, 8))
        self.fig.suptitle('Water Treatment System Trends', fontsize=16)
        
        # Generate sample data
        hours = np.arange(24)
        
        # Production rate trend
        production_data = 160 + 10 * np.sin(hours * np.pi / 12) + np.random.normal(0, 2, 24)
        self.ax1.plot(hours, production_data, 'b-', linewidth=2)
        self.ax1.set_title('Production Rate (L/min)')
        self.ax1.set_xlabel('Hour')
        self.ax1.grid(True, alpha=0.3)
        
        # Tank levels trend
        tank1_levels = 75 + 10 * np.sin((hours + 6) * np.pi / 12) + np.random.normal(0, 1, 24)
        tank2_levels = 70 + 8 * np.sin((hours + 3) * np.pi / 12) + np.random.normal(0, 1, 24)
        self.ax2.plot(hours, tank1_levels, 'g-', label='Tank 1', linewidth=2)
        self.ax2.plot(hours, tank2_levels, 'r-', label='Tank 2', linewidth=2)
        self.ax2.set_title('Tank Levels (%)')
        self.ax2.set_xlabel('Hour')
        self.ax2.legend()
        self.ax2.grid(True, alpha=0.3)
        
        # Water quality trend
        ph_data = 7.2 + 0.2 * np.sin(hours * np.pi / 6) + np.random.normal(0, 0.05, 24)
        self.ax3.plot(hours, ph_data, 'm-', linewidth=2)
        self.ax3.set_title('pH Levels')
        self.ax3.set_xlabel('Hour')
        self.ax3.set_ylim(6.8, 7.6)
        self.ax3.grid(True, alpha=0.3)
        
        # Energy consumption trend
        energy_data = 120 + 15 * np.sin(hours * np.pi / 12) + np.random.normal(0, 3, 24)
        self.ax4.plot(hours, energy_data, 'orange', linewidth=2)
        self.ax4.set_title('Power Consumption (kW)')
        self.ax4.set_xlabel('Hour')
        self.ax4.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        # Embed matplotlib in tkinter
        canvas = FigureCanvasTkAgg(self.fig, trends_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
    def create_tank_displays(self, parent):
        """Create visual tank level displays"""
        tanks_grid = tk.Frame(parent, bg='white')
        tanks_grid.pack(fill=tk.X, pady=10)
        
        # Seawater tank
        self.create_single_tank_display(tanks_grid, "Seawater Tank", 
                                      self.system_data['seawater_tank']['level'], 0, 0)
        
        # Treated water tank
        self.create_single_tank_display(tanks_grid, "Treated Water Tank", 
                                      self.system_data['treated_tank']['level'], 0, 1)
        
        # Roof tanks
        for i, tank in enumerate(self.system_data['roof_tanks']):
            self.create_single_tank_display(tanks_grid, f"Roof Tank {tank['id']}\n{tank['zone']}", 
                                          tank['level'], 1, i)
    
    def create_single_tank_display(self, parent, name, level, row, col):
        """Create a single tank level display"""
        tank_frame = tk.Frame(parent, bg='white', relief=tk.RAISED, bd=2)
        tank_frame.grid(row=row, column=col, padx=10, pady=10)
        
        # Tank name
        tk.Label(tank_frame, text=name, font=('Arial', 10, 'bold'), bg='white').pack(pady=5)
        
        # Tank visual (simplified rectangle)
        canvas = tk.Canvas(tank_frame, width=80, height=100, bg='lightgray')
        canvas.pack(pady=5)
        
        # Tank outline
        canvas.create_rectangle(10, 10, 70, 90, outline='black', width=2)
        
        # Water level (blue rectangle)
        water_height = int((level / 100) * 80)
        canvas.create_rectangle(12, 90 - water_height, 68, 88, fill='lightblue', outline='blue')
        
        # Level text
        tk.Label(tank_frame, text=f"{level:.1f}%", font=('Arial', 10), bg='white').pack()
        
    def create_pump_controls(self, parent):
        """Create pump control interface"""
        for i, pump in enumerate(self.system_data['pumps']):
            pump_frame = tk.Frame(parent, bg='white', relief=tk.RAISED, bd=1)
            pump_frame.pack(fill=tk.X, padx=10, pady=5)
            
            # Pump info
            info_frame = tk.Frame(pump_frame, bg='white')
            info_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
            
            tk.Label(info_frame, text=f"Pump {pump['id']}", font=('Arial', 12, 'bold'), 
                   bg='white').grid(row=0, column=0, padx=10)
            tk.Label(info_frame, text=f"Status: {pump['status']}", 
                   bg='white').grid(row=0, column=1, padx=10)
            tk.Label(info_frame, text=f"Flow: {pump['flow']:.1f} L/min", 
                   bg='white').grid(row=0, column=2, padx=10)
            tk.Label(info_frame, text=f"Runtime: {pump['runtime']} hrs", 
                   bg='white').grid(row=0, column=3, padx=10)
            
            # Control buttons
            control_frame = tk.Frame(pump_frame, bg='white')
            control_frame.pack(side=tk.RIGHT, padx=10)
            
            start_btn = tk.Button(control_frame, text="Start", bg='#27ae60', fg='white', 
                                command=lambda p=i: self.start_pump(p))
            start_btn.pack(side=tk.LEFT, padx=2)
            
            stop_btn = tk.Button(control_frame, text="Stop", bg='#e74c3c', fg='white', 
                               command=lambda p=i: self.stop_pump(p))
            stop_btn.pack(side=tk.LEFT, padx=2)
            
    def start_system(self):
        """Start the water treatment system"""
        messagebox.showinfo("System Control", "Water Treatment System Started")
        
    def stop_system(self):
        """Stop the water treatment system"""
        result = messagebox.askyesno("System Control", "Are you sure you want to stop the system?")
        if result:
            messagebox.showinfo("System Control", "Water Treatment System Stopped")
            
    def emergency_stop(self):
        """Emergency stop the system"""
        result = messagebox.askyesno("EMERGENCY STOP", 
                                   "This will immediately stop all equipment.\nAre you sure?")
        if result:
            messagebox.showwarning("EMERGENCY STOP", "EMERGENCY STOP ACTIVATED!\nAll equipment stopped.")
            
    def start_pump(self, pump_id):
        """Start a specific pump"""
        messagebox.showinfo("Pump Control", f"Pump {pump_id + 1} Started")
        
    def stop_pump(self, pump_id):
        """Stop a specific pump"""
        messagebox.showinfo("Pump Control", f"Pump {pump_id + 1} Stopped")
        
    def update_display_data(self):
        """Update all display elements with current data"""
        try:
            # Update production metrics
            ro = self.system_data['ro_system']
            energy = self.system_data['energy']
            
            self.production_label.config(text=f"Production Rate: {ro['flow_rate']:.1f} L/min")
            self.efficiency_label.config(text=f"System Efficiency: {ro['efficiency']:.1f}%")
            self.energy_label.config(text=f"Power Consumption: {energy['consumption']:.1f} kW")
            
            # Update RO system data
            self.ro_pressure_label.config(text=f"Pressure: {ro['pressure']:.1f} bar")
            self.ro_flow_label.config(text=f"Flow Rate: {ro['flow_rate']:.1f} L/min")
            self.ro_recovery_label.config(text=f"Recovery: {ro['recovery']:.1f}%")
            
            # Update water quality
            quality = self.system_data['water_quality']
            self.ph_label.config(text=f"pH: {quality['ph']:.1f}")
            self.chlorine_label.config(text=f"Free Chlorine: {quality['chlorine']:.1f} ppm")
            self.tds_label.config(text=f"TDS: {quality['tds']} ppm")
            self.turbidity_label.config(text=f"Turbidity: {quality['turbidity']:.2f} NTU")
            
        except Exception as e:
            print(f"Error updating display: {e}")
            
    def simulate_data_changes(self):
        """Simulate realistic data changes"""
        import random
        
        # Simulate tank level changes
        for tank in self.system_data['roof_tanks']:
            tank['level'] += random.uniform(-0.5, 0.3)  # Gradual consumption
            tank['level'] = max(10, min(95, tank['level']))  # Keep in realistic range
            tank['volume'] = int(tank['level'] * 100)  # Assuming 10,000L max capacity
            
        # Simulate RO system variations
        ro = self.system_data['ro_system']
        ro['pressure'] += random.uniform(-0.2, 0.2)
        ro['flow_rate'] += random.uniform(-2.0, 2.0)
        ro['recovery'] += random.uniform(-0.1, 0.1)
        ro['efficiency'] += random.uniform(-0.3, 0.3)
        
        # Keep values in realistic ranges
        ro['pressure'] = max(50, min(60, ro['pressure']))
        ro['flow_rate'] = max(150, min(180, ro['flow_rate']))
        ro['recovery'] = max(40, min(50, ro['recovery']))
        ro['efficiency'] = max(85, min(95, ro['efficiency']))
        
        # Simulate water quality variations
        quality = self.system_data['water_quality']
        quality['ph'] += random.uniform(-0.02, 0.02)
        quality['chlorine'] += random.uniform(-0.05, 0.05)
        quality['ph'] = max(6.8, min(7.6, quality['ph']))
        quality['chlorine'] = max(0.5, min(1.2, quality['chlorine']))
        
    def start_data_update(self):
        """Start the data update thread"""
        def update_loop():
            while self.running:
                self.simulate_data_changes()
                self.root.after(0, self.update_display_data)
                time.sleep(2)  # Update every 2 seconds
                
        update_thread = threading.Thread(target=update_loop, daemon=True)
        update_thread.start()
        
    def on_closing(self):
        """Handle application closing"""
        self.running = False
        self.root.destroy()

def main():
    """Main function to run the HMI"""
    root = tk.Tk()
    app = WaterTreatmentHMI(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()

if __name__ == "__main__":
    main()
