import tkinter as tk
from tkinter import ttk, messagebox, font
import time
import random
import threading
import datetime
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import configparser
import os
import sys

class WastewaterTreatmentHMI:
    def __init__(self, root):
        self.root = root
        self.root.title("Wastewater Treatment Plant SCADA")
        self.root.geometry("1280x800")
        self.root.minsize(1024, 768)
        
        # Set up colors and fonts
        self.bg_color = "#f0f0f0"
        self.header_color = "#2c3e50"
        self.accent_color = "#3498db"
        self.alarm_color = "#e74c3c"
        self.ok_color = "#2ecc71"
        self.warning_color = "#f39c12"
        
        self.header_font = font.Font(family="Arial", size=16, weight="bold")
        self.title_font = font.Font(family="Arial", size=14, weight="bold")
        self.normal_font = font.Font(family="Arial", size=10)
        self.small_font = font.Font(family="Arial", size=8)
        
        # Load configuration
        self.config = self.load_configuration()
        
        # Create simulation values (in a real system, these would come from the PLC)
        self.system_running = False
        self.maintenance_mode = False
        self.auto_mode = True
        self.alarm_active = False
        self.emergency_stop = False
        self.storm_mode = False
        
        # Process variables
        self.tank_level_1 = 2.5  # meters
        self.tank_level_2 = 1.8  # meters
        self.flow_rate = 300.0   # m³/hr
        self.ph_value = 7.2      # pH
        self.dissolved_oxygen = 5.5  # mg/L
        self.turbidity = 35.0    # NTU
        self.chlorine = 2.3      # mg/L
        self.temperature = 18.5  # °C
        
        # Performance metrics
        self.treatment_efficiency = 95.0  # %
        self.energy_consumption = 175.0   # kW
        self.total_flow_today = 2568.0    # m³
        self.chemical_usage = 120.5       # L
        
        # Equipment status
        self.pump_p101_status = False
        self.pump_p102_status = False
        self.blower_status = False
        self.mixer_m101_status = False
        self.mixer_m102_status = False
        self.uv_system_status = False
        
        # Alarm history
        self.alarm_history = []
        
        # Create the main UI structure
        self.create_ui()
        
        # Start simulation thread
        self.running = True
        self.sim_thread = threading.Thread(target=self.simulate_values)
        self.sim_thread.daemon = True
        self.sim_thread.start()
        
        # Update UI periodically
        self.update_ui()
        
    def load_configuration(self):
        try:
            config = configparser.ConfigParser()
            config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'config', 'wwtp_config.ini')
            config.read(config_path)
            return config
        except Exception as e:
            messagebox.showerror("Configuration Error", f"Error loading configuration: {str(e)}")
            return None
            
    def create_ui(self):
        # Create main frame
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create header
        self.header_frame = ttk.Frame(self.main_frame, style="Header.TFrame")
        self.header_frame.pack(fill=tk.X, padx=10, pady=10)
        
        header_label = ttk.Label(self.header_frame, text="WASTEWATER TREATMENT PLANT", font=self.header_font, style="Header.TLabel")
        header_label.pack(side=tk.LEFT, padx=10)
        
        # Create system status indicators
        self.system_status_frame = ttk.Frame(self.header_frame)
        self.system_status_frame.pack(side=tk.RIGHT, padx=10)
        
        self.status_indicator = ttk.Label(self.system_status_frame, text="●", font=("Arial", 24), foreground=self.alarm_color)
        self.status_indicator.pack(side=tk.LEFT, padx=5)
        
        self.status_label = ttk.Label(self.system_status_frame, text="SYSTEM STOPPED", font=self.title_font)
        self.status_label.pack(side=tk.LEFT, padx=5)
        
        # Create notebook for different screens
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create main pages
        self.overview_frame = ttk.Frame(self.notebook)
        self.process_frame = ttk.Frame(self.notebook)
        self.alarms_frame = ttk.Frame(self.notebook)
        self.trends_frame = ttk.Frame(self.notebook)
        self.reports_frame = ttk.Frame(self.notebook)
        self.settings_frame = ttk.Frame(self.notebook)
        
        self.notebook.add(self.overview_frame, text="Overview")
        self.notebook.add(self.process_frame, text="Process Detail")
        self.notebook.add(self.alarms_frame, text="Alarms & Events")
        self.notebook.add(self.trends_frame, text="Trends")
        self.notebook.add(self.reports_frame, text="Reports")
        self.notebook.add(self.settings_frame, text="Settings")
        
        # Create overview screen
        self.build_overview_screen()
        
        # Create process screen
        self.build_process_screen()
        
        # Create alarms screen
        self.build_alarms_screen()
        
        # Create trends screen
        self.build_trends_screen()
        
        # Create footer with status bar
        self.footer_frame = ttk.Frame(self.main_frame)
        self.footer_frame.pack(fill=tk.X, side=tk.BOTTOM, padx=10, pady=5)
        
        self.current_time_label = ttk.Label(self.footer_frame, text="", font=self.small_font)
        self.current_time_label.pack(side=tk.RIGHT, padx=10)
        
        self.connection_status = ttk.Label(self.footer_frame, text="PLC: Connected", font=self.small_font)
        self.connection_status.pack(side=tk.LEFT, padx=10)
        
        # Create control buttons
        self.controls_frame = ttk.Frame(self.main_frame)
        self.controls_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.start_button = ttk.Button(self.controls_frame, text="Start System", command=self.start_system)
        self.start_button.pack(side=tk.LEFT, padx=5)
        
        self.stop_button = ttk.Button(self.controls_frame, text="Stop System", command=self.stop_system)
        self.stop_button.pack(side=tk.LEFT, padx=5)
        
        self.estop_button = ttk.Button(self.controls_frame, text="EMERGENCY STOP", style="Accent.TButton", command=self.emergency_stop_system)
        self.estop_button.pack(side=tk.LEFT, padx=20)
        
        self.auto_button = ttk.Button(self.controls_frame, text="Auto Mode", command=self.toggle_auto_mode)
        self.auto_button.pack(side=tk.LEFT, padx=5)
        
        self.maintenance_button = ttk.Button(self.controls_frame, text="Maintenance Mode", command=self.toggle_maintenance)
        self.maintenance_button.pack(side=tk.LEFT, padx=5)
        
        self.storm_button = ttk.Button(self.controls_frame, text="Storm Mode", command=self.toggle_storm_mode)
        self.storm_button.pack(side=tk.LEFT, padx=5)
        
        self.acknowledge_button = ttk.Button(self.controls_frame, text="Acknowledge Alarms", command=self.acknowledge_alarms)
        self.acknowledge_button.pack(side=tk.RIGHT, padx=5)
        
        # Style configuration
        style = ttk.Style()
        style.configure("Header.TFrame", background=self.header_color)
        style.configure("Header.TLabel", background=self.header_color, foreground="white")
        style.configure("Accent.TButton", background=self.alarm_color, foreground="white")
        
    def build_overview_screen(self):
        # Main layout frames for overview screen
        left_frame = ttk.Frame(self.overview_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        right_frame = ttk.Frame(self.overview_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Process overview schematic (in real application this would be a proper P&ID diagram)
        schematic_frame = ttk.LabelFrame(left_frame, text="Process Overview")
        schematic_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Create a basic schematic canvas
        self.schematic_canvas = tk.Canvas(schematic_frame, bg="white", height=400)
        self.schematic_canvas.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Draw a basic schematic (simplified for example purposes)
        self.draw_simple_schematic()
        
        # Key process variables
        vars_frame = ttk.LabelFrame(right_frame, text="Key Process Variables")
        vars_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Create key variable indicators
        var_grid = ttk.Frame(vars_frame)
        var_grid.pack(fill=tk.BOTH, padx=10, pady=10)
        
        # Row 0
        ttk.Label(var_grid, text="Flow Rate:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        self.flow_label = ttk.Label(var_grid, text="-- m³/hr", font=self.normal_font)
        self.flow_label.grid(row=0, column=1, sticky=tk.W, padx=5, pady=2)
        
        ttk.Label(var_grid, text="Primary Tank:").grid(row=0, column=2, sticky=tk.W, padx=5, pady=2)
        self.tank1_label = ttk.Label(var_grid, text="-- m", font=self.normal_font)
        self.tank1_label.grid(row=0, column=3, sticky=tk.W, padx=5, pady=2)
        
        # Row 1
        ttk.Label(var_grid, text="pH:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)
        self.ph_label = ttk.Label(var_grid, text="--", font=self.normal_font)
        self.ph_label.grid(row=1, column=1, sticky=tk.W, padx=5, pady=2)
        
        ttk.Label(var_grid, text="Secondary Tank:").grid(row=1, column=2, sticky=tk.W, padx=5, pady=2)
        self.tank2_label = ttk.Label(var_grid, text="-- m", font=self.normal_font)
        self.tank2_label.grid(row=1, column=3, sticky=tk.W, padx=5, pady=2)
        
        # Row 2
        ttk.Label(var_grid, text="Dissolved O₂:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=2)
        self.do_label = ttk.Label(var_grid, text="-- mg/L", font=self.normal_font)
        self.do_label.grid(row=2, column=1, sticky=tk.W, padx=5, pady=2)
        
        ttk.Label(var_grid, text="Turbidity:").grid(row=2, column=2, sticky=tk.W, padx=5, pady=2)
        self.turbidity_label = ttk.Label(var_grid, text="-- NTU", font=self.normal_font)
        self.turbidity_label.grid(row=2, column=3, sticky=tk.W, padx=5, pady=2)
        
        # Row 3
        ttk.Label(var_grid, text="Chlorine:").grid(row=3, column=0, sticky=tk.W, padx=5, pady=2)
        self.chlorine_label = ttk.Label(var_grid, text="-- mg/L", font=self.normal_font)
        self.chlorine_label.grid(row=3, column=1, sticky=tk.W, padx=5, pady=2)
        
        ttk.Label(var_grid, text="Temperature:").grid(row=3, column=2, sticky=tk.W, padx=5, pady=2)
        self.temp_label = ttk.Label(var_grid, text="-- °C", font=self.normal_font)
        self.temp_label.grid(row=3, column=3, sticky=tk.W, padx=5, pady=2)
        
        # Equipment status section
        equip_frame = ttk.LabelFrame(right_frame, text="Equipment Status")
        equip_frame.pack(fill=tk.X, padx=5, pady=5)
        
        equip_grid = ttk.Frame(equip_frame)
        equip_grid.pack(fill=tk.BOTH, padx=10, pady=10)
        
        # Row 0
        ttk.Label(equip_grid, text="Intake Pump:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        self.pump1_status = ttk.Label(equip_grid, text="●", foreground=self.alarm_color)
        self.pump1_status.grid(row=0, column=1, sticky=tk.W)
        self.pump1_label = ttk.Label(equip_grid, text="STOPPED", font=self.normal_font)
        self.pump1_label.grid(row=0, column=2, sticky=tk.W, padx=5, pady=2)
        
        ttk.Label(equip_grid, text="Primary Mixer:").grid(row=0, column=3, sticky=tk.W, padx=5, pady=2)
        self.mixer1_status = ttk.Label(equip_grid, text="●", foreground=self.alarm_color)
        self.mixer1_status.grid(row=0, column=4, sticky=tk.W)
        self.mixer1_label = ttk.Label(equip_grid, text="STOPPED", font=self.normal_font)
        self.mixer1_label.grid(row=0, column=5, sticky=tk.W, padx=5, pady=2)
        
        # Row 1
        ttk.Label(equip_grid, text="Transfer Pump:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)
        self.pump2_status = ttk.Label(equip_grid, text="●", foreground=self.alarm_color)
        self.pump2_status.grid(row=1, column=1, sticky=tk.W)
        self.pump2_label = ttk.Label(equip_grid, text="STOPPED", font=self.normal_font)
        self.pump2_label.grid(row=1, column=2, sticky=tk.W, padx=5, pady=2)
        
        ttk.Label(equip_grid, text="Secondary Mixer:").grid(row=1, column=3, sticky=tk.W, padx=5, pady=2)
        self.mixer2_status = ttk.Label(equip_grid, text="●", foreground=self.alarm_color)
        self.mixer2_status.grid(row=1, column=4, sticky=tk.W)
        self.mixer2_label = ttk.Label(equip_grid, text="STOPPED", font=self.normal_font)
        self.mixer2_label.grid(row=1, column=5, sticky=tk.W, padx=5, pady=2)
        
        # Row 2
        ttk.Label(equip_grid, text="Aeration Blower:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=2)
        self.blower_status = ttk.Label(equip_grid, text="●", foreground=self.alarm_color)
        self.blower_status.grid(row=2, column=1, sticky=tk.W)
        self.blower_label = ttk.Label(equip_grid, text="STOPPED", font=self.normal_font)
        self.blower_label.grid(row=2, column=2, sticky=tk.W, padx=5, pady=2)
        
        ttk.Label(equip_grid, text="UV System:").grid(row=2, column=3, sticky=tk.W, padx=5, pady=2)
        self.uv_status = ttk.Label(equip_grid, text="●", foreground=self.alarm_color)
        self.uv_status.grid(row=2, column=4, sticky=tk.W)
        self.uv_label = ttk.Label(equip_grid, text="STOPPED", font=self.normal_font)
        self.uv_label.grid(row=2, column=5, sticky=tk.W, padx=5, pady=2)
        
        # Performance metrics
        perf_frame = ttk.LabelFrame(right_frame, text="Performance Metrics")
        perf_frame.pack(fill=tk.X, padx=5, pady=5)
        
        perf_grid = ttk.Frame(perf_frame)
        perf_grid.pack(fill=tk.BOTH, padx=10, pady=10)
        
        # Row 0
        ttk.Label(perf_grid, text="Treatment Efficiency:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        self.efficiency_label = ttk.Label(perf_grid, text="-- %", font=self.normal_font)
        self.efficiency_label.grid(row=0, column=1, sticky=tk.W, padx=5, pady=2)
        
        ttk.Label(perf_grid, text="Energy Consumption:").grid(row=0, column=2, sticky=tk.W, padx=5, pady=2)
        self.energy_label = ttk.Label(perf_grid, text="-- kW", font=self.normal_font)
        self.energy_label.grid(row=0, column=3, sticky=tk.W, padx=5, pady=2)
        
        # Row 1
        ttk.Label(perf_grid, text="Total Flow Today:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)
        self.total_flow_label = ttk.Label(perf_grid, text="-- m³", font=self.normal_font)
        self.total_flow_label.grid(row=1, column=1, sticky=tk.W, padx=5, pady=2)
        
        ttk.Label(perf_grid, text="Chemical Usage:").grid(row=1, column=2, sticky=tk.W, padx=5, pady=2)
        self.chemical_label = ttk.Label(perf_grid, text="-- L", font=self.normal_font)
        self.chemical_label.grid(row=1, column=3, sticky=tk.W, padx=5, pady=2)
        
        # Current alarms section
        alarm_summary_frame = ttk.LabelFrame(right_frame, text="Active Alarms")
        alarm_summary_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Scrollable alarm list
        alarm_scroll = ttk.Scrollbar(alarm_summary_frame)
        alarm_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.active_alarm_list = tk.Listbox(alarm_summary_frame, height=4, yscrollcommand=alarm_scroll.set, font=self.small_font)
        self.active_alarm_list.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        alarm_scroll.config(command=self.active_alarm_list.yview)
        
    def build_process_screen(self):
        # Placeholder for a more detailed process screen
        ttk.Label(self.process_frame, text="Process Detail View", font=self.title_font).pack(pady=20)
        ttk.Label(self.process_frame, text="This screen would show detailed process diagrams and controls").pack()
        
    def build_alarms_screen(self):
        # Alarms and events history
        alarms_frame = ttk.LabelFrame(self.alarms_frame, text="Alarm History")
        alarms_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Toolbar
        toolbar = ttk.Frame(alarms_frame)
        toolbar.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(toolbar, text="Filter Alarms", command=self.filter_alarms).pack(side=tk.LEFT, padx=5)
        ttk.Button(toolbar, text="Export", command=self.export_alarms).pack(side=tk.LEFT, padx=5)
        ttk.Button(toolbar, text="Clear History", command=self.clear_alarms).pack(side=tk.LEFT, padx=5)
        
        # Columns
        columns = ('timestamp', 'priority', 'area', 'description', 'status')
        self.alarm_tree = ttk.Treeview(alarms_frame, columns=columns, show='headings')
        
        # Define headings
        self.alarm_tree.heading('timestamp', text='Timestamp')
        self.alarm_tree.heading('priority', text='Priority')
        self.alarm_tree.heading('area', text='Area')
        self.alarm_tree.heading('description', text='Description')
        self.alarm_tree.heading('status', text='Status')
        
        # Define columns
        self.alarm_tree.column('timestamp', width=150)
        self.alarm_tree.column('priority', width=70)
        self.alarm_tree.column('area', width=120)
        self.alarm_tree.column('description', width=400)
        self.alarm_tree.column('status', width=100)
        
        self.alarm_tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Add some sample alarms
        self.add_sample_alarms()
        
    def build_trends_screen(self):
        # Trends visualization
        trends_frame = ttk.LabelFrame(self.trends_frame, text="Process Trends")
        trends_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Controls for trends
        controls_frame = ttk.Frame(trends_frame)
        controls_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(controls_frame, text="Time Range:").pack(side=tk.LEFT, padx=5)
        time_range = ttk.Combobox(controls_frame, values=['1 Hour', '8 Hours', '24 Hours', '7 Days'])
        time_range.current(0)
        time_range.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(controls_frame, text="Variables:").pack(side=tk.LEFT, padx=5)
        variables = ttk.Combobox(controls_frame, values=['Flow Rate', 'pH', 'Dissolved Oxygen', 'Turbidity', 'All'])
        variables.current(4)
        variables.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(controls_frame, text="Update", command=self.update_trends).pack(side=tk.LEFT, padx=5)
        
        # Create matplotlib figure
        self.fig = Figure(figsize=(10, 6), dpi=100)
        
        # Create trend plots (sample data)
        self.create_trend_plots()
        
        # Add figure to canvas
        self.canvas = FigureCanvasTkAgg(self.fig, master=trends_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
    def draw_simple_schematic(self):
        # This is a very simplified schematic for demonstration
        # In a real application, this would be a properly designed P&ID
        
        # Clear canvas
        self.schematic_canvas.delete("all")
        
        # Colors for different states
        active_color = "#4CAF50"  # Green
        inactive_color = "#757575"  # Gray
        warning_color = "#FFC107"  # Amber
        alarm_color = "#F44336"  # Red
        water_color = "#03A9F4"  # Light Blue
        pipe_color = "#607D8B"  # Blue Gray
        
        # Canvas dimensions
        w = self.schematic_canvas.winfo_width()
        h = self.schematic_canvas.winfo_height()
        
        # Draw tanks
        # Primary tank
        tank1_fill_color = water_color
        if self.tank_level_1 > 4.5:  # Near full
            tank1_fill_color = warning_color
        tank1_fill_height = int((self.tank_level_1 / 5.0) * 150)  # Scale to 150px height
        
        self.schematic_canvas.create_rectangle(100, 100, 200, 250, outline="black", width=2, tag="tank1")
        self.schematic_canvas.create_rectangle(100, 250-tank1_fill_height, 200, 250, 
                                               fill=tank1_fill_color, outline="", tag="tank1_fill")
        self.schematic_canvas.create_text(150, 80, text="Primary Tank", font=self.small_font)
        self.schematic_canvas.create_text(150, 270, text=f"{self.tank_level_1:.1f} m", font=self.small_font)
        
        # Secondary tank
        tank2_fill_color = water_color
        tank2_fill_height = int((self.tank_level_2 / 5.0) * 150)  # Scale to 150px height
        
        self.schematic_canvas.create_rectangle(400, 100, 500, 250, outline="black", width=2, tag="tank2")
        self.schematic_canvas.create_rectangle(400, 250-tank2_fill_height, 500, 250, 
                                               fill=tank2_fill_color, outline="", tag="tank2_fill")
        self.schematic_canvas.create_text(450, 80, text="Secondary Tank", font=self.small_font)
        self.schematic_canvas.create_text(450, 270, text=f"{self.tank_level_2:.1f} m", font=self.small_font)
        
        # Draw pipes
        # Inlet pipe
        self.schematic_canvas.create_line(50, 200, 100, 200, fill=pipe_color, width=3)
        
        # Transfer pipe
        self.schematic_canvas.create_line(200, 200, 400, 200, fill=pipe_color, width=3)
        
        # Outlet pipe
        self.schematic_canvas.create_line(500, 200, 550, 200, fill=pipe_color, width=3)
        
        # Draw pumps
        pump1_color = active_color if self.pump_p101_status else inactive_color
        pump2_color = active_color if self.pump_p102_status else inactive_color
        
        # Pump symbols (simplified)
        self.schematic_canvas.create_oval(60, 190, 80, 210, fill=pump1_color, outline="black", tag="pump1")
        self.schematic_canvas.create_text(70, 180, text="P-101", font=self.small_font)
        
        self.schematic_canvas.create_oval(280, 190, 300, 210, fill=pump2_color, outline="black", tag="pump2")
        self.schematic_canvas.create_text(290, 180, text="P-102", font=self.small_font)
        
        # Draw mixers
        mixer1_color = active_color if self.mixer_m101_status else inactive_color
        mixer2_color = active_color if self.mixer_m102_status else inactive_color
        
        # Mixer symbols (simplified)
        self.schematic_canvas.create_line(150, 150, 150, 220, fill=mixer1_color, width=2, tag="mixer1")
        self.schematic_canvas.create_line(135, 210, 165, 210, fill=mixer1_color, width=2, tag="mixer1")
        self.schematic_canvas.create_line(140, 200, 160, 200, fill=mixer1_color, width=2, tag="mixer1")
        self.schematic_canvas.create_text(150, 130, text="M-101", font=self.small_font)
        
        self.schematic_canvas.create_line(450, 150, 450, 220, fill=mixer2_color, width=2, tag="mixer2")
        self.schematic_canvas.create_line(435, 210, 465, 210, fill=mixer2_color, width=2, tag="mixer2")
        self.schematic_canvas.create_line(440, 200, 460, 200, fill=mixer2_color, width=2, tag="mixer2")
        self.schematic_canvas.create_text(450, 130, text="M-102", font=self.small_font)
        
        # Draw blower
        blower_color = active_color if self.blower_status else inactive_color
        
        self.schematic_canvas.create_oval(340, 290, 380, 330, fill=blower_color, outline="black", tag="blower")
        self.schematic_canvas.create_line(350, 300, 370, 320, fill="white", width=2, tag="blower")
        self.schematic_canvas.create_line(350, 320, 370, 300, fill="white", width=2, tag="blower")
        self.schematic_canvas.create_text(360, 350, text="Blower", font=self.small_font)
        
        # Draw UV system
        uv_color = active_color if self.uv_system_status else inactive_color
        
        self.schematic_canvas.create_rectangle(520, 190, 540, 210, fill=uv_color, outline="black", tag="uv")
        self.schematic_canvas.create_text(530, 180, text="UV", font=self.small_font)
        
        # Add flow indicators
        flow_arrow_color = water_color if self.flow_rate > 20 else inactive_color
        
        # Flow arrows
        self.create_arrow(75, 200, "right", flow_arrow_color, 5)
        self.create_arrow(300, 200, "right", flow_arrow_color, 5)
        self.create_arrow(525, 200, "right", flow_arrow_color, 5)
        
    def create_arrow(self, x, y, direction, color, size):
        # Helper function to create flow direction arrows
        if direction == "right":
            self.schematic_canvas.create_line(x-size, y-size, x, y, fill=color, width=2)
            self.schematic_canvas.create_line(x-size, y+size, x, y, fill=color, width=2)
        elif direction == "left":
            self.schematic_canvas.create_line(x+size, y-size, x, y, fill=color, width=2)
            self.schematic_canvas.create_line(x+size, y+size, x, y, fill=color, width=2)
        elif direction == "up":
            self.schematic_canvas.create_line(x-size, y+size, x, y, fill=color, width=2)
            self.schematic_canvas.create_line(x+size, y+size, x, y, fill=color, width=2)
        elif direction == "down":
            self.schematic_canvas.create_line(x-size, y-size, x, y, fill=color, width=2)
            self.schematic_canvas.create_line(x+size, y-size, x, y, fill=color, width=2)
            
    def create_trend_plots(self):
        # Generate some sample data for trends
        self.fig.clear()
        
        # Generate sample data
        t = list(range(60))  # 60 time points
        
        # Sample data with some noise and trends
        flow_data = [300 + random.uniform(-20, 20) for _ in range(60)]
        ph_data = [7.2 + random.uniform(-0.3, 0.3) for _ in range(60)]
        do_data = [5.5 + random.uniform(-0.5, 0.5) for _ in range(60)]
        turbidity_data = [35 + random.uniform(-5, 5) for _ in range(60)]
        
        # Create subplots
        ax1 = self.fig.add_subplot(221)
        ax1.plot(t, flow_data, 'b-')
        ax1.set_title('Flow Rate (m³/hr)')
        ax1.grid(True)
        
        ax2 = self.fig.add_subplot(222)
        ax2.plot(t, ph_data, 'g-')
        ax2.set_title('pH Value')
        ax2.grid(True)
        
        ax3 = self.fig.add_subplot(223)
        ax3.plot(t, do_data, 'r-')
        ax3.set_title('Dissolved Oxygen (mg/L)')
        ax3.grid(True)
        
        ax4 = self.fig.add_subplot(224)
        ax4.plot(t, turbidity_data, 'y-')
        ax4.set_title('Turbidity (NTU)')
        ax4.grid(True)
        
        self.fig.tight_layout()
        
    def add_sample_alarms(self):
        # Add some sample alarms to the alarm history
        current_time = datetime.datetime.now()
        
        alarms = [
            (current_time - datetime.timedelta(minutes=5), 'High', 'Primary Tank', 'High level warning', 'Acknowledged'),
            (current_time - datetime.timedelta(minutes=15), 'Medium', 'pH Control', 'pH deviation from setpoint', 'Acknowledged'),
            (current_time - datetime.timedelta(hours=1), 'Low', 'Blower', 'Maintenance due', 'Acknowledged'),
            (current_time - datetime.timedelta(hours=2), 'High', 'Chlorine', 'Low chlorine level', 'Cleared'),
            (current_time - datetime.timedelta(days=1), 'Critical', 'Control System', 'Communication error', 'Cleared')
        ]
        
        # Clear existing items
        for item in self.alarm_tree.get_children():
            self.alarm_tree.delete(item)
            
        # Add new items
        for alarm in alarms:
            timestamp = alarm[0].strftime('%Y-%m-%d %H:%M:%S')
            self.alarm_tree.insert('', tk.END, values=(timestamp, alarm[1], alarm[2], alarm[3], alarm[4]))
            
    def start_system(self):
        self.system_running = True
        self.status_indicator.config(foreground=self.ok_color)
        self.status_label.config(text="SYSTEM RUNNING")
        messagebox.showinfo("System Control", "System starting in automatic mode")
        
    def stop_system(self):
        self.system_running = False
        self.status_indicator.config(foreground=self.warning_color)
        self.status_label.config(text="SYSTEM STOPPED")
        messagebox.showinfo("System Control", "System stopping. All processes will be safely shut down.")
        
    def emergency_stop_system(self):
        self.system_running = False
        self.emergency_stop = True
        self.status_indicator.config(foreground=self.alarm_color)
        self.status_label.config(text="EMERGENCY STOP")
        messagebox.showwarning("EMERGENCY STOP", "Emergency stop activated! All processes immediately stopped.")
        
    def toggle_auto_mode(self):
        self.auto_mode = not self.auto_mode
        if self.auto_mode:
            messagebox.showinfo("Mode Change", "System switched to Automatic mode")
            self.auto_button.config(text="Auto Mode")
        else:
            messagebox.showinfo("Mode Change", "System switched to Manual mode")
            self.auto_button.config(text="Manual Mode")
            
    def toggle_maintenance(self):
        self.maintenance_mode = not self.maintenance_mode
        if self.maintenance_mode:
            messagebox.showinfo("Mode Change", "Maintenance mode activated")
            self.maintenance_button.config(text="Exit Maintenance")
        else:
            messagebox.showinfo("Mode Change", "Maintenance mode deactivated")
            self.maintenance_button.config(text="Maintenance Mode")
            
    def toggle_storm_mode(self):
        self.storm_mode = not self.storm_mode
        if self.storm_mode:
            messagebox.showinfo("Mode Change", "Storm mode activated")
            self.storm_button.config(text="Exit Storm Mode")
        else:
            messagebox.showinfo("Mode Change", "Storm mode deactivated")
            self.storm_button.config(text="Storm Mode")
            
    def acknowledge_alarms(self):
        if self.alarm_active:
            self.alarm_active = False
            messagebox.showinfo("Alarms", "All alarms acknowledged")
        else:
            messagebox.showinfo("Alarms", "No active alarms to acknowledge")
            
    def filter_alarms(self):
        messagebox.showinfo("Feature Placeholder", "Alarm filtering would be implemented here")
        
    def export_alarms(self):
        messagebox.showinfo("Feature Placeholder", "Alarm export function would be implemented here")
        
    def clear_alarms(self):
        if messagebox.askyesno("Clear Alarms", "Are you sure you want to clear all alarm history?"):
            for item in self.alarm_tree.get_children():
                self.alarm_tree.delete(item)
                
    def update_trends(self):
        # Refresh trend data when requested
        self.create_trend_plots()
        self.canvas.draw()
        
    def simulate_values(self):
        # Simulate changing process values (in a real system, these would come from the PLC)
        while self.running:
            if self.system_running and not self.emergency_stop:
                # Simulate tank levels
                self.tank_level_1 += random.uniform(-0.05, 0.05)
                self.tank_level_1 = max(0.1, min(5.0, self.tank_level_1))
                
                self.tank_level_2 += random.uniform(-0.03, 0.03)
                self.tank_level_2 = max(0.1, min(5.0, self.tank_level_2))
                
                # Simulate flow rate
                if self.pump_p101_status:
                    target_flow = 300
                    self.flow_rate = self.flow_rate * 0.9 + target_flow * 0.1 + random.uniform(-10, 10)
                else:
                    self.flow_rate = max(0, self.flow_rate * 0.8 + random.uniform(-5, 0))
                    
                # Simulate other parameters
                self.ph_value += random.uniform(-0.05, 0.05)
                self.ph_value = max(6.0, min(9.0, self.ph_value))
                
                self.dissolved_oxygen += random.uniform(-0.1, 0.1)
                if self.blower_status:
                    self.dissolved_oxygen = max(2.0, min(8.0, self.dissolved_oxygen + 0.05))
                else:
                    self.dissolved_oxygen = max(0.5, min(8.0, self.dissolved_oxygen - 0.05))
                    
                self.turbidity += random.uniform(-1.0, 1.0)
                self.turbidity = max(5.0, min(100.0, self.turbidity))
                
                self.chlorine += random.uniform(-0.05, 0.05)
                self.chlorine = max(0.1, min(5.0, self.chlorine))
                
                self.temperature += random.uniform(-0.1, 0.1)
                self.temperature = max(10.0, min(30.0, self.temperature))
                
                # Simulate performance metrics
                self.treatment_efficiency = 100 * (1.0 - self.turbidity / 1000.0) + random.uniform(-2, 2)
                self.treatment_efficiency = max(0, min(100, self.treatment_efficiency))
                
                self.energy_consumption = 100 + self.flow_rate / 4.0 + random.uniform(-10, 10)
                if self.blower_status:
                    self.energy_consumption += 50 + random.uniform(-5, 5)
                    
                self.total_flow_today += self.flow_rate / 3600.0
                
                if self.ph_value < 7.0 or self.ph_value > 8.0:
                    self.chemical_usage += 0.01
                    
                # Randomly toggle equipment status for simulation
                if random.random() < 0.01:
                    self.pump_p101_status = not self.pump_p101_status
                if random.random() < 0.01:
                    self.pump_p102_status = not self.pump_p102_status
                if random.random() < 0.02:
                    self.mixer_m101_status = not self.mixer_m101_status
                if random.random() < 0.02:
                    self.mixer_m102_status = not self.mixer_m102_status
                if random.random() < 0.01:
                    self.blower_status = not self.blower_status
                if random.random() < 0.01:
                    self.uv_system_status = not self.uv_system_status
                    
                # Randomly generate alarms
                if random.random() < 0.01:
                    self.alarm_active = True
                    alarm_text = f"Alarm at {time.strftime('%H:%M:%S')}: "
                    alarm_type = random.choice(["High pH", "Low DO", "High Turbidity", "Pump Failure", "High Level"])
                    self.active_alarm_list.insert(0, alarm_text + alarm_type)
                    
                    # Keep only the most recent alarms
                    if self.active_alarm_list.size() > 15:
                        self.active_alarm_list.delete(15)
            
            time.sleep(1)
            
    def update_ui(self):
        # Update process values display
        self.flow_label.config(text=f"{self.flow_rate:.1f} m³/hr")
        self.tank1_label.config(text=f"{self.tank_level_1:.2f} m")
        self.tank2_label.config(text=f"{self.tank_level_2:.2f} m")
        self.ph_label.config(text=f"{self.ph_value:.2f}")
        self.do_label.config(text=f"{self.dissolved_oxygen:.2f} mg/L")
        self.turbidity_label.config(text=f"{self.turbidity:.1f} NTU")
        self.chlorine_label.config(text=f"{self.chlorine:.2f} mg/L")
        self.temp_label.config(text=f"{self.temperature:.1f} °C")
        
        # Update performance metrics
        self.efficiency_label.config(text=f"{self.treatment_efficiency:.1f} %")
        self.energy_label.config(text=f"{self.energy_consumption:.1f} kW")
        self.total_flow_label.config(text=f"{self.total_flow_today:.1f} m³")
        self.chemical_label.config(text=f"{self.chemical_usage:.1f} L")
        
        # Update equipment status
        self.pump1_status.config(foreground=self.ok_color if self.pump_p101_status else self.alarm_color)
        self.pump1_label.config(text="RUNNING" if self.pump_p101_status else "STOPPED")
        
        self.pump2_status.config(foreground=self.ok_color if self.pump_p102_status else self.alarm_color)
        self.pump2_label.config(text="RUNNING" if self.pump_p102_status else "STOPPED")
        
        self.mixer1_status.config(foreground=self.ok_color if self.mixer_m101_status else self.alarm_color)
        self.mixer1_label.config(text="RUNNING" if self.mixer_m101_status else "STOPPED")
        
        self.mixer2_status.config(foreground=self.ok_color if self.mixer_m102_status else self.alarm_color)
        self.mixer2_label.config(text="RUNNING" if self.mixer_m102_status else "STOPPED")
        
        self.blower_status.config(foreground=self.ok_color if self.blower_status else self.alarm_color)
        self.blower_label.config(text="RUNNING" if self.blower_status else "STOPPED")
        
        self.uv_status.config(foreground=self.ok_color if self.uv_system_status else self.alarm_color)
        self.uv_label.config(text="RUNNING" if self.uv_system_status else "STOPPED")
        
        # Update current time on status bar
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")
        self.current_time_label.config(text=f"System Time: {current_time}")
        
        # Update schematic if window is ready
        if self.schematic_canvas.winfo_width() > 1:
            self.draw_simple_schematic()
            
        # Schedule the next update
        self.root.after(1000, self.update_ui)
        
    def on_closing(self):
        self.running = False
        self.root.destroy()

# Start the application when run directly
if __name__ == "__main__":
    root = tk.Tk()
    app = WastewaterTreatmentHMI(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()
