#!/usr/bin/env python3
"""
HMI (Human Machine Interface) for Industrial Process Control
============================================================
This creates a graphical HMI interface for monitoring and controlling the PLC system.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
import json
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np

class ProcessHMI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Industrial Process Control HMI")
        self.root.geometry("1400x900")
        self.root.configure(bg='#2C3E50')
        
        # Process variables (simulated PLC data)
        self.process_data = {
            'temperature': 20.0,
            'pressure': 1.0,
            'level': True,
            'pump_status': False,
            'heater_status': False,
            'valve1_status': False,
            'valve2_status': False,
            'system_running': False,
            'alarm_active': False,
            'emergency_stop': False,
            'cycle_count': 0,
            'setpoint_temp': 75.0,
            'setpoint_pressure': 3.0
        }
        
        # Historical data for trends
        self.history = {
            'time': [],
            'temperature': [],
            'pressure': [],
            'timestamps': []
        }
        
        # Control flags
        self.running = True
        self.auto_mode = True
        
        self.create_widgets()
        self.start_data_simulation()
        
    def create_widgets(self):
        """Create all HMI widgets"""
        # Main title
        title_frame = tk.Frame(self.root, bg='#2C3E50', height=60)
        title_frame.pack(fill='x', padx=10, pady=5)
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(title_frame, text="INDUSTRIAL PROCESS CONTROL SYSTEM", 
                              font=('Arial', 20, 'bold'), fg='white', bg='#2C3E50')
        title_label.pack(pady=15)
        
        # Create main container
        main_frame = tk.Frame(self.root, bg='#2C3E50')
        main_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Left panel - Process overview
        self.create_process_overview(main_frame)
        
        # Center panel - Controls and setpoints
        self.create_control_panel(main_frame)
        
        # Right panel - Trends and alarms
        self.create_trends_panel(main_frame)
        
        # Bottom panel - Status bar
        self.create_status_bar()
        
    def create_process_overview(self, parent):
        """Create process overview panel"""
        overview_frame = tk.LabelFrame(parent, text="Process Overview", 
                                     font=('Arial', 12, 'bold'), fg='white', bg='#34495E',
                                     width=450, height=400)
        overview_frame.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')
        overview_frame.grid_propagate(False)
        
        # Process diagram canvas
        self.canvas = tk.Canvas(overview_frame, bg='white', width=430, height=350)
        self.canvas.pack(padx=10, pady=10)
        
        self.draw_process_diagram()
        
    def draw_process_diagram(self):
        """Draw simplified process diagram on canvas"""
        # Clear canvas
        self.canvas.delete("all")
        
        # Tank
        tank_color = '#3498DB' if self.process_data['level'] else '#E74C3C'
        self.canvas.create_rectangle(150, 100, 250, 200, fill=tank_color, outline='black', width=2)
        self.canvas.create_text(200, 150, text="TANK\nT-001", font=('Arial', 10, 'bold'))
          # Liquid level
        if self.process_data['level']:
            level_height = 70  # 70% of tank height
            self.canvas.create_rectangle(155, 200-level_height, 245, 195, 
                                       fill='#2980B9', outline='')
        
        # Heater
        heater_color = '#E74C3C' if self.process_data['heater_status'] else '#BDC3C7'
        self.canvas.create_rectangle(160, 170, 240, 190, fill=heater_color, outline='black')
        self.canvas.create_text(200, 180, text="HEATER", font=('Arial', 8, 'bold'))
        
        # Pump
        pump_color = '#27AE60' if self.process_data['pump_status'] else '#BDC3C7'
        self.canvas.create_oval(300, 180, 340, 220, fill=pump_color, outline='black', width=2)
        self.canvas.create_text(320, 200, text="PUMP\nP-001", font=('Arial', 8, 'bold'))
        
        # Valves
        valve1_color = '#27AE60' if self.process_data['valve1_status'] else '#E74C3C'
        valve2_color = '#27AE60' if self.process_data['valve2_status'] else '#E74C3C'
        
        # Valve 1 (inlet)
        self.canvas.create_polygon(80, 140, 120, 140, 100, 160, fill=valve1_color, outline='black')
        self.canvas.create_text(100, 170, text="PV-001", font=('Arial', 8))
        
        # Valve 2 (outlet)
        self.canvas.create_polygon(280, 140, 320, 140, 300, 160, fill=valve2_color, outline='black')
        self.canvas.create_text(300, 170, text="PV-002", font=('Arial', 8))
        
        # Piping
        # Inlet pipe
        self.canvas.create_line(20, 150, 80, 150, width=3, fill='black')
        self.canvas.create_line(120, 150, 150, 150, width=3, fill='black')
        
        # Outlet pipe
        self.canvas.create_line(250, 150, 280, 150, width=3, fill='black')
        self.canvas.create_line(320, 150, 360, 150, width=3, fill='black')
        self.canvas.create_line(360, 150, 360, 200, width=3, fill='black')
        self.canvas.create_line(340, 200, 360, 200, width=3, fill='black')
        
        # Discharge pipe
        self.canvas.create_line(300, 200, 280, 200, width=3, fill='black')
        self.canvas.create_line(280, 200, 280, 250, width=3, fill='black')
        self.canvas.create_line(280, 250, 400, 250, width=3, fill='black')
        
        # Labels
        self.canvas.create_text(20, 130, text="FEED", font=('Arial', 8, 'bold'))
        self.canvas.create_text(400, 230, text="PRODUCT", font=('Arial', 8, 'bold'))
        
        # Temperature and pressure indicators
        temp_color = '#E74C3C' if self.process_data['temperature'] > 80 else '#27AE60'
        self.canvas.create_oval(180, 80, 220, 120, fill=temp_color, outline='black')
        self.canvas.create_text(200, 100, text=f"T\n{self.process_data['temperature']:.1f}°C", 
                               font=('Arial', 8, 'bold'))
        
        press_color = '#E74C3C' if self.process_data['pressure'] > 5 else '#27AE60'
        self.canvas.create_oval(260, 80, 300, 120, fill=press_color, outline='black')
        self.canvas.create_text(280, 100, text=f"P\n{self.process_data['pressure']:.1f} bar", 
                               font=('Arial', 8, 'bold'))
        
    def create_control_panel(self, parent):
        """Create control panel"""
        control_frame = tk.LabelFrame(parent, text="Control Panel", 
                                    font=('Arial', 12, 'bold'), fg='white', bg='#34495E',
                                    width=450, height=400)
        control_frame.grid(row=0, column=1, padx=5, pady=5, sticky='nsew')
        control_frame.grid_propagate(False)
        
        # System control buttons
        button_frame = tk.Frame(control_frame, bg='#34495E')
        button_frame.pack(pady=10)
        
        # Start/Stop buttons
        self.start_btn = tk.Button(button_frame, text="START", font=('Arial', 14, 'bold'),
                                  bg='#27AE60', fg='white', width=8, height=2,
                                  command=self.start_system)
        self.start_btn.grid(row=0, column=0, padx=5)
        
        self.stop_btn = tk.Button(button_frame, text="STOP", font=('Arial', 14, 'bold'),
                                 bg='#E74C3C', fg='white', width=8, height=2,
                                 command=self.stop_system)
        self.stop_btn.grid(row=0, column=1, padx=5)
        
        # Emergency stop
        self.estop_btn = tk.Button(button_frame, text="E-STOP", font=('Arial', 12, 'bold'),
                                  bg='#C0392B', fg='white', width=8, height=2,
                                  command=self.emergency_stop)
        self.estop_btn.grid(row=0, column=2, padx=5)
        
        # Mode selection
        mode_frame = tk.Frame(control_frame, bg='#34495E')
        mode_frame.pack(pady=10)
        
        tk.Label(mode_frame, text="Operation Mode:", font=('Arial', 12), 
                fg='white', bg='#34495E').pack()
        
        self.mode_var = tk.StringVar(value="AUTO")
        auto_radio = tk.Radiobutton(mode_frame, text="AUTO", variable=self.mode_var, 
                                   value="AUTO", font=('Arial', 11), fg='white', bg='#34495E',
                                   command=self.toggle_mode)
        auto_radio.pack(side='left', padx=10)
        
        manual_radio = tk.Radiobutton(mode_frame, text="MANUAL", variable=self.mode_var, 
                                     value="MANUAL", font=('Arial', 11), fg='white', bg='#34495E',
                                     command=self.toggle_mode)
        manual_radio.pack(side='left', padx=10)
        
        # Setpoints
        setpoint_frame = tk.LabelFrame(control_frame, text="Setpoints", 
                                     font=('Arial', 11, 'bold'), fg='white', bg='#34495E')
        setpoint_frame.pack(pady=10, fill='x', padx=10)
        
        # Temperature setpoint
        temp_frame = tk.Frame(setpoint_frame, bg='#34495E')
        temp_frame.pack(pady=5, fill='x')
        
        tk.Label(temp_frame, text="Temperature SP:", font=('Arial', 10), 
                fg='white', bg='#34495E').pack(side='left')
        
        self.temp_sp_var = tk.DoubleVar(value=75.0)
        temp_spinbox = tk.Spinbox(temp_frame, from_=20, to=100, increment=1,
                                 textvariable=self.temp_sp_var, font=('Arial', 10),
                                 width=10, command=self.update_setpoints)
        temp_spinbox.pack(side='right', padx=5)
        
        tk.Label(temp_frame, text="°C", font=('Arial', 10), 
                fg='white', bg='#34495E').pack(side='right')
        
        # Pressure setpoint
        press_frame = tk.Frame(setpoint_frame, bg='#34495E')
        press_frame.pack(pady=5, fill='x')
        
        tk.Label(press_frame, text="Pressure SP:", font=('Arial', 10), 
                fg='white', bg='#34495E').pack(side='left')
        
        self.press_sp_var = tk.DoubleVar(value=3.0)
        press_spinbox = tk.Spinbox(press_frame, from_=0.5, to=8.0, increment=0.1,
                                  textvariable=self.press_sp_var, font=('Arial', 10),
                                  width=10, command=self.update_setpoints)
        press_spinbox.pack(side='right', padx=5)
        
        tk.Label(press_frame, text="bar", font=('Arial', 10), 
                fg='white', bg='#34495E').pack(side='right')
        
        # Manual control (only visible in manual mode)
        self.manual_frame = tk.LabelFrame(control_frame, text="Manual Control", 
                                        font=('Arial', 11, 'bold'), fg='white', bg='#34495E')
        
        # Equipment control checkboxes
        self.pump_var = tk.BooleanVar()
        pump_check = tk.Checkbutton(self.manual_frame, text="Pump", variable=self.pump_var,
                                   font=('Arial', 10), fg='white', bg='#34495E',
                                   command=self.manual_control)
        pump_check.pack(anchor='w', padx=10, pady=2)
        
        self.heater_var = tk.BooleanVar()
        heater_check = tk.Checkbutton(self.manual_frame, text="Heater", variable=self.heater_var,
                                     font=('Arial', 10), fg='white', bg='#34495E',
                                     command=self.manual_control)
        heater_check.pack(anchor='w', padx=10, pady=2)
        
        self.valve1_var = tk.BooleanVar()
        valve1_check = tk.Checkbutton(self.manual_frame, text="Valve 1 (Inlet)", variable=self.valve1_var,
                                     font=('Arial', 10), fg='white', bg='#34495E',
                                     command=self.manual_control)
        valve1_check.pack(anchor='w', padx=10, pady=2)
        
        self.valve2_var = tk.BooleanVar()
        valve2_check = tk.Checkbutton(self.manual_frame, text="Valve 2 (Outlet)", variable=self.valve2_var,
                                     font=('Arial', 10), fg='white', bg='#34495E',
                                     command=self.manual_control)
        valve2_check.pack(anchor='w', padx=10, pady=2)
        
    def create_trends_panel(self, parent):
        """Create trends and alarms panel"""
        trends_frame = tk.LabelFrame(parent, text="Trends & Alarms", 
                                   font=('Arial', 12, 'bold'), fg='white', bg='#34495E',
                                   width=450, height=400)
        trends_frame.grid(row=0, column=2, padx=5, pady=5, sticky='nsew')
        trends_frame.grid_propagate(False)
        
        # Create matplotlib figure for trends
        self.fig = Figure(figsize=(6, 4), dpi=70, facecolor='#34495E')
        self.fig.patch.set_facecolor('#34495E')
        
        # Temperature trend
        self.ax1 = self.fig.add_subplot(211, facecolor='#2C3E50')
        self.ax1.set_ylabel('Temp (°C)', color='white')
        self.ax1.tick_params(colors='white')
        self.ax1.grid(True, alpha=0.3)
        
        # Pressure trend  
        self.ax2 = self.fig.add_subplot(212, facecolor='#2C3E50')
        self.ax2.set_ylabel('Press (bar)', color='white')
        self.ax2.set_xlabel('Time', color='white')
        self.ax2.tick_params(colors='white')
        self.ax2.grid(True, alpha=0.3)
        
        self.canvas_plot = FigureCanvasTkAgg(self.fig, trends_frame)
        self.canvas_plot.get_tk_widget().pack(fill='both', expand=True, padx=5, pady=5)
        
        # Alarms list
        alarm_frame = tk.Frame(trends_frame, bg='#34495E', height=100)
        alarm_frame.pack(fill='x', padx=5, pady=5)
        alarm_frame.pack_propagate(False)
        
        tk.Label(alarm_frame, text="Active Alarms:", font=('Arial', 10, 'bold'),
                fg='white', bg='#34495E').pack(anchor='w')
        
        self.alarm_listbox = tk.Listbox(alarm_frame, height=4, font=('Arial', 9),
                                       bg='#2C3E50', fg='white')
        self.alarm_listbox.pack(fill='both', expand=True)
        
    def create_status_bar(self):
        """Create status bar at bottom"""
        status_frame = tk.Frame(self.root, bg='#2C3E50', height=30)
        status_frame.pack(fill='x', side='bottom')
        status_frame.pack_propagate(False)
        
        # System status
        self.status_label = tk.Label(status_frame, text="System: STOPPED", 
                                    font=('Arial', 10), fg='white', bg='#2C3E50')
        self.status_label.pack(side='left', padx=10)
        
        # Date/time
        self.time_label = tk.Label(status_frame, text="", 
                                  font=('Arial', 10), fg='white', bg='#2C3E50')
        self.time_label.pack(side='right', padx=10)
        
        # Update time
        self.update_time()
        
    def start_system(self):
        """Start the process system"""
        if not self.process_data['emergency_stop']:
            self.process_data['system_running'] = True
            messagebox.showinfo("System", "Process started successfully!")
        else:
            messagebox.showerror("Error", "Cannot start - Emergency stop active!")
    
    def stop_system(self):
        """Stop the process system"""
        self.process_data['system_running'] = False
        messagebox.showinfo("System", "Process stopped.")
    
    def emergency_stop(self):
        """Emergency stop"""
        self.process_data['emergency_stop'] = not self.process_data['emergency_stop']
        self.process_data['system_running'] = False
        
        if self.process_data['emergency_stop']:
            messagebox.showwarning("Emergency Stop", "EMERGENCY STOP ACTIVATED!")
            self.estop_btn.config(text="RESET\nE-STOP")
        else:
            messagebox.showinfo("Reset", "Emergency stop reset.")
            self.estop_btn.config(text="E-STOP")
    
    def toggle_mode(self):
        """Toggle between auto and manual mode"""
        self.auto_mode = (self.mode_var.get() == "AUTO")
        
        if self.auto_mode:
            self.manual_frame.pack_forget()
        else:
            self.manual_frame.pack(pady=10, fill='x', padx=10)
    
    def manual_control(self):
        """Handle manual control changes"""
        if not self.auto_mode:
            self.process_data['pump_status'] = self.pump_var.get()
            self.process_data['heater_status'] = self.heater_var.get()
            self.process_data['valve1_status'] = self.valve1_var.get()
            self.process_data['valve2_status'] = self.valve2_var.get()
    
    def update_setpoints(self):
        """Update setpoint values"""
        self.process_data['setpoint_temp'] = self.temp_sp_var.get()
        self.process_data['setpoint_pressure'] = self.press_sp_var.get()
    
    def start_data_simulation(self):
        """Start simulated PLC data updates"""
        def simulate_data():
            while self.running:
                self.simulate_process()
                self.update_display()
                time.sleep(1)  # Update every second
        
        thread = threading.Thread(target=simulate_data, daemon=True)
        thread.start()
    
    def simulate_process(self):
        """Simulate process behavior"""
        if self.auto_mode and self.process_data['system_running']:
            # Auto mode logic
            # Temperature control
            if self.process_data['temperature'] < self.process_data['setpoint_temp'] - 2:
                self.process_data['heater_status'] = True
            elif self.process_data['temperature'] > self.process_data['setpoint_temp'] + 2:
                self.process_data['heater_status'] = False
                
            # Pump and valve control
            self.process_data['pump_status'] = True
            self.process_data['valve1_status'] = True
            
            if self.process_data['temperature'] >= self.process_data['setpoint_temp']:
                self.process_data['valve2_status'] = True
        
        elif not self.process_data['system_running']:
            # System stopped
            self.process_data['pump_status'] = False
            self.process_data['heater_status'] = False
            self.process_data['valve1_status'] = False
            self.process_data['valve2_status'] = False
        
        # Simulate temperature changes
        if self.process_data['heater_status']:
            self.process_data['temperature'] += 0.5
        else:
            if self.process_data['temperature'] > 20:
                self.process_data['temperature'] -= 0.3
        
        # Simulate pressure changes
        if self.process_data['pump_status']:
            if self.process_data['pressure'] < 4.0:
                self.process_data['pressure'] += 0.1
        else:
            if self.process_data['pressure'] > 0.5:
                self.process_data['pressure'] -= 0.05
        
        # Update history for trends
        now = time.time()
        self.history['time'].append(now)
        self.history['temperature'].append(self.process_data['temperature'])
        self.history['pressure'].append(self.process_data['pressure'])
        self.history['timestamps'].append(datetime.now())
        
        # Keep only last 100 points
        if len(self.history['time']) > 100:
            for key in self.history:
                self.history[key] = self.history[key][-100:]
        
        # Check alarms
        self.check_alarms()
    
    def check_alarms(self):
        """Check for alarm conditions"""
        alarms = []
        
        if self.process_data['temperature'] > 90:
            alarms.append("HIGH TEMPERATURE ALARM")
        
        if self.process_data['pressure'] > 5.0:
            alarms.append("HIGH PRESSURE ALARM")
        
        if self.process_data['emergency_stop']:
            alarms.append("EMERGENCY STOP ACTIVE")
        
        if not self.process_data['level'] and self.process_data['system_running']:
            alarms.append("LOW LEVEL ALARM")
        
        # Update alarm display
        self.alarm_listbox.delete(0, tk.END)
        for alarm in alarms:
            self.alarm_listbox.insert(tk.END, alarm)
        
        self.process_data['alarm_active'] = len(alarms) > 0
    
    def update_display(self):
        """Update all display elements"""
        # Update process diagram
        self.draw_process_diagram()
        
        # Update status
        if self.process_data['system_running']:
            status_text = "System: RUNNING"
            status_color = '#27AE60'
        elif self.process_data['emergency_stop']:
            status_text = "System: E-STOP"
            status_color = '#E74C3C'
        else:
            status_text = "System: STOPPED"
            status_color = '#F39C12'
        
        self.status_label.config(text=status_text, fg=status_color)
        
        # Update manual controls if in manual mode
        if not self.auto_mode:
            self.pump_var.set(self.process_data['pump_status'])
            self.heater_var.set(self.process_data['heater_status'])
            self.valve1_var.set(self.process_data['valve1_status'])
            self.valve2_var.set(self.process_data['valve2_status'])
        
        # Update trends
        self.update_trends()
    
    def update_trends(self):
        """Update trend plots"""
        if len(self.history['time']) > 1:
            # Clear axes
            self.ax1.clear()
            self.ax2.clear()
            
            # Plot temperature
            time_points = [(t - self.history['time'][0])/60 for t in self.history['time']]  # Minutes
            self.ax1.plot(time_points, self.history['temperature'], 'r-', linewidth=2, label='Temperature')
            self.ax1.axhline(y=self.process_data['setpoint_temp'], color='r', linestyle='--', alpha=0.7, label='SP')
            self.ax1.set_ylabel('Temp (°C)', color='white')
            self.ax1.tick_params(colors='white')
            self.ax1.grid(True, alpha=0.3)
            self.ax1.legend()
            
            # Plot pressure
            self.ax2.plot(time_points, self.history['pressure'], 'b-', linewidth=2, label='Pressure')
            self.ax2.axhline(y=self.process_data['setpoint_pressure'], color='b', linestyle='--', alpha=0.7, label='SP')
            self.ax2.set_ylabel('Press (bar)', color='white')
            self.ax2.set_xlabel('Time (min)', color='white')
            self.ax2.tick_params(colors='white')
            self.ax2.grid(True, alpha=0.3)
            self.ax2.legend()
            
            # Style the plots
            for ax in [self.ax1, self.ax2]:
                ax.set_facecolor('#2C3E50')
                for spine in ax.spines.values():
                    spine.set_color('white')
            
            self.canvas_plot.draw()
    
    def update_time(self):
        """Update time display"""
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.time_label.config(text=current_time)
        self.root.after(1000, self.update_time)
    
    def run(self):
        """Start the HMI application"""
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()
    
    def on_closing(self):
        """Handle application closing"""
        self.running = False
        self.root.destroy()

def main():
    """Start the HMI application"""
    hmi = ProcessHMI()
    hmi.run()

if __name__ == "__main__":
    main()
