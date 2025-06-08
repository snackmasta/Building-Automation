#!/usr/bin/env python3
"""
Automated Car Parking Vending System - Desktop HMI Interface
Version: 2.1.0
Author: Industrial Automation Team
Date: June 2025

Advanced GUI interface for monitoring and controlling the automated car parking
vending system with real-time data visualization, system control, and analytics.
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import sqlite3
import threading
import time
import datetime
import json
import random
import math
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np

# Data structures
@dataclass
class SystemStatus:
    state: str = "IDLE"
    vehicles_parked: int = 0
    vehicles_retrieved: int = 0
    total_spaces: int = 300
    occupied_spaces: int = 0
    revenue_today: float = 0.0
    system_uptime: float = 0.0
    emergency_active: bool = False
    maintenance_mode: bool = False

@dataclass
class ElevatorStatus:
    elevator_id: int
    current_level: int = 1
    target_level: int = 1
    position: float = 0.0
    speed: float = 0.0
    state: str = "IDLE"
    load_weight: float = 0.0
    available: bool = True
    fault_code: int = 0

@dataclass
class ParkingSpace:
    level: int
    position: int
    occupied: bool = False
    vehicle_id: str = ""
    parking_time: Optional[datetime.datetime] = None
    vehicle_type: str = "STANDARD"

@dataclass
class Transaction:
    transaction_id: int
    timestamp: datetime.datetime
    customer_id: str
    vehicle_id: str
    payment_method: str
    amount: float
    duration: int  # hours
    status: str

class ParkingSystemHMI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Car Parking Vending System - Control Center")
        self.root.geometry("1600x1000")
        self.root.configure(bg='#2c3e50')
        
        # System data
        self.system_status = SystemStatus()
        self.elevators = [
            ElevatorStatus(1),
            ElevatorStatus(2),
            ElevatorStatus(3)
        ]
        self.parking_spaces = self._initialize_parking_spaces()
        self.transactions = []
        
        # Database
        self.init_database()
        
        # GUI components
        self.setup_styles()
        self.create_main_interface()
        
        # Data update thread
        self.running = True
        self.update_thread = threading.Thread(target=self.data_update_loop, daemon=True)
        self.update_thread.start()
        
        # Bind close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def _initialize_parking_spaces(self) -> List[List[ParkingSpace]]:
        """Initialize parking space grid (15 levels x 20 spaces)"""
        spaces = []
        for level in range(1, 16):  # 15 levels
            level_spaces = []
            for pos in range(1, 21):  # 20 positions per level
                space = ParkingSpace(level, pos)
                # Simulate some occupied spaces
                if random.random() < 0.3:  # 30% occupancy
                    space.occupied = True
                    space.vehicle_id = f"ABC{random.randint(100, 999)}"
                    space.parking_time = datetime.datetime.now() - datetime.timedelta(
                        hours=random.randint(1, 24)
                    )
                level_spaces.append(space)
            spaces.append(level_spaces)
        return spaces
    
    def init_database(self):
        """Initialize SQLite database"""
        self.conn = sqlite3.connect('parking_system.db', check_same_thread=False)
        self.cursor = self.conn.cursor()
        
        # Create tables
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                transaction_id INTEGER,
                timestamp TEXT,
                customer_id TEXT,
                vehicle_id TEXT,
                payment_method TEXT,
                amount REAL,
                duration INTEGER,
                status TEXT
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS system_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                event_type TEXT,
                description TEXT,
                severity TEXT
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS parking_spaces (
                level INTEGER,
                position INTEGER,
                occupied BOOLEAN,
                vehicle_id TEXT,
                parking_time TEXT,
                vehicle_type TEXT,
                PRIMARY KEY (level, position)
            )
        ''')
        
        self.conn.commit()
    
    def setup_styles(self):
        """Configure ttk styles"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure colors
        style.configure('Title.TLabel', 
                       font=('Arial', 16, 'bold'),
                       foreground='white',
                       background='#2c3e50')
        
        style.configure('Header.TLabel',
                       font=('Arial', 12, 'bold'),
                       foreground='white',
                       background='#34495e')
        
        style.configure('Status.TLabel',
                       font=('Arial', 10),
                       foreground='white',
                       background='#34495e')
        
        style.configure('Custom.TNotebook',
                       background='#2c3e50',
                       borderwidth=0)
        
        style.configure('Custom.TNotebook.Tab',
                       padding=[20, 10],
                       font=('Arial', 10, 'bold'))
    
    def create_main_interface(self):
        """Create the main GUI interface"""
        # Title bar
        title_frame = tk.Frame(self.root, bg='#2c3e50', height=60)
        title_frame.pack(fill='x', padx=10, pady=5)
        title_frame.pack_propagate(False)
        
        ttk.Label(title_frame, text="🚗 Automated Car Parking Vending System", 
                 style='Title.TLabel').pack(side='left', pady=15)
        
        # System status indicators
        status_frame = tk.Frame(title_frame, bg='#2c3e50')
        status_frame.pack(side='right', pady=15)
        
        self.status_light = tk.Canvas(status_frame, width=20, height=20, bg='#2c3e50', highlightthickness=0)
        self.status_light.pack(side='right', padx=(0, 10))
        self.status_circle = self.status_light.create_oval(2, 2, 18, 18, fill='green', outline='darkgreen')
        
        self.system_status_label = ttk.Label(status_frame, text="System: ONLINE", style='Status.TLabel')
        self.system_status_label.pack(side='right', padx=(0, 10))
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.root, style='Custom.TNotebook')
        self.notebook.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Create tabs
        self.create_overview_tab()
        self.create_parking_grid_tab()
        self.create_operations_tab()
        self.create_elevators_tab()
        self.create_analytics_tab()
        self.create_maintenance_tab()
        self.create_logs_tab()
    
    def create_overview_tab(self):
        """Create system overview tab"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="📊 System Overview")
        
        # Main metrics frame
        metrics_frame = tk.Frame(frame, bg='#34495e', relief='raised', bd=2)
        metrics_frame.pack(fill='x', padx=10, pady=10)
        
        # Create metric displays
        metrics = [
            ("Total Spaces", "300"),
            ("Occupied", "0"),
            ("Available", "300"),
            ("Queue Length", "0"),
            ("Revenue Today", "$0.00"),
            ("Throughput/Hour", "0")
        ]
        
        self.metric_labels = {}
        for i, (label, value) in enumerate(metrics):
            metric_frame = tk.Frame(metrics_frame, bg='#34495e')
            metric_frame.grid(row=0, column=i, padx=20, pady=15, sticky='ew')
            
            ttk.Label(metric_frame, text=label, style='Header.TLabel').pack()
            value_label = ttk.Label(metric_frame, text=value, 
                                   font=('Arial', 14, 'bold'),
                                   foreground='#3498db',
                                   background='#34495e')
            value_label.pack()
            self.metric_labels[label] = value_label
        
        # Configure grid weights
        for i in range(len(metrics)):
            metrics_frame.grid_columnconfigure(i, weight=1)
        
        # System state display
        state_frame = tk.Frame(frame, bg='#34495e', relief='raised', bd=2)
        state_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Label(state_frame, text="System State", style='Header.TLabel').pack(pady=5)
        self.state_label = ttk.Label(state_frame, text="IDLE", 
                                    font=('Arial', 18, 'bold'),
                                    foreground='#2ecc71',
                                    background='#34495e')
        self.state_label.pack(pady=5)
        
        # Real-time charts frame
        charts_frame = tk.Frame(frame, bg='#2c3e50')
        charts_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Occupancy chart
        self.create_occupancy_chart(charts_frame)
        
        # Revenue chart
        self.create_revenue_chart(charts_frame)
    
    def create_occupancy_chart(self, parent):
        """Create real-time occupancy chart"""
        chart_frame = tk.Frame(parent, bg='#34495e', relief='raised', bd=2)
        chart_frame.pack(side='left', fill='both', expand=True, padx=(0, 5))
        
        ttk.Label(chart_frame, text="Parking Occupancy by Level", style='Header.TLabel').pack(pady=5)
        
        self.occupancy_fig = Figure(figsize=(8, 4), facecolor='#34495e')
        self.occupancy_ax = self.occupancy_fig.add_subplot(111, facecolor='#2c3e50')
        self.occupancy_ax.set_xlabel('Level', color='white')
        self.occupancy_ax.set_ylabel('Occupancy %', color='white')
        self.occupancy_ax.tick_params(colors='white')
        
        self.occupancy_canvas = FigureCanvasTkAgg(self.occupancy_fig, chart_frame)
        self.occupancy_canvas.get_tk_widget().pack(fill='both', expand=True, padx=5, pady=5)
    
    def create_revenue_chart(self, parent):
        """Create revenue trend chart"""
        chart_frame = tk.Frame(parent, bg='#34495e', relief='raised', bd=2)
        chart_frame.pack(side='right', fill='both', expand=True, padx=(5, 0))
        
        ttk.Label(chart_frame, text="Revenue Trend (24 Hours)", style='Header.TLabel').pack(pady=5)
        
        self.revenue_fig = Figure(figsize=(8, 4), facecolor='#34495e')
        self.revenue_ax = self.revenue_fig.add_subplot(111, facecolor='#2c3e50')
        self.revenue_ax.set_xlabel('Time', color='white')
        self.revenue_ax.set_ylabel('Revenue ($)', color='white')
        self.revenue_ax.tick_params(colors='white')
        
        self.revenue_canvas = FigureCanvasTkAgg(self.revenue_fig, chart_frame)
        self.revenue_canvas.get_tk_widget().pack(fill='both', expand=True, padx=5, pady=5)
    
    def create_parking_grid_tab(self):
        """Create parking space grid visualization"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="🏢 Parking Grid")
        
        # Control panel
        control_frame = tk.Frame(frame, bg='#34495e', relief='raised', bd=2)
        control_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(control_frame, text="Parking Space Visualization", style='Header.TLabel').pack(pady=5)
        
        # Level selection
        level_frame = tk.Frame(control_frame, bg='#34495e')
        level_frame.pack(pady=5)
        
        ttk.Label(level_frame, text="Select Level:", style='Status.TLabel').pack(side='left', padx=5)
        self.level_var = tk.StringVar(value="1")
        level_combo = ttk.Combobox(level_frame, textvariable=self.level_var, 
                                  values=[str(i) for i in range(1, 16)], width=10)
        level_combo.pack(side='left', padx=5)
        level_combo.bind('<<ComboboxSelected>>', self.update_parking_grid)
        
        # Grid canvas
        grid_frame = tk.Frame(frame, bg='#2c3e50')
        grid_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.grid_canvas = tk.Canvas(grid_frame, bg='#2c3e50', highlightthickness=0)
        self.grid_canvas.pack(fill='both', expand=True)
        
        # Legend
        legend_frame = tk.Frame(frame, bg='#34495e', relief='raised', bd=2)
        legend_frame.pack(fill='x', padx=10, pady=5)
        
        legend_items = [
            ("Available", "#2ecc71"),
            ("Occupied", "#e74c3c"),
            ("Maintenance", "#f39c12"),
            ("Selected", "#3498db")
        ]
        
        for i, (label, color) in enumerate(legend_items):
            item_frame = tk.Frame(legend_frame, bg='#34495e')
            item_frame.pack(side='left', padx=20, pady=5)
            
            color_box = tk.Canvas(item_frame, width=20, height=20, bg=color, highlightthickness=1)
            color_box.pack(side='left', padx=5)
            
            ttk.Label(item_frame, text=label, style='Status.TLabel').pack(side='left')
        
        self.update_parking_grid()
    
    def create_operations_tab(self):
        """Create operations control tab"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="⚙️ Operations")
        
        # Manual controls
        control_frame = tk.Frame(frame, bg='#34495e', relief='raised', bd=2)
        control_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Label(control_frame, text="Manual Operations", style='Header.TLabel').pack(pady=5)
        
        button_frame = tk.Frame(control_frame, bg='#34495e')
        button_frame.pack(pady=10)
        
        operations = [
            ("🚗 Simulate Parking", self.simulate_parking),
            ("🔄 Simulate Retrieval", self.simulate_retrieval),
            ("🛑 Emergency Stop", self.emergency_stop),
            ("🔧 Maintenance Mode", self.toggle_maintenance),
            ("🔄 Reset System", self.reset_system)
        ]
        
        for i, (text, command) in enumerate(operations):
            btn = tk.Button(button_frame, text=text, command=command,
                           bg='#3498db', fg='white', font=('Arial', 10, 'bold'),
                           relief='raised', bd=2, padx=20, pady=10)
            btn.grid(row=i//3, column=i%3, padx=10, pady=5, sticky='ew')
        
        # Transaction queue
        queue_frame = tk.Frame(frame, bg='#34495e', relief='raised', bd=2)
        queue_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        ttk.Label(queue_frame, text="Transaction Queue", style='Header.TLabel').pack(pady=5)
        
        # Queue table
        columns = ("ID", "Customer", "Vehicle", "Amount", "Status", "Time")
        self.queue_tree = ttk.Treeview(queue_frame, columns=columns, show='headings', height=10)
        
        for col in columns:
            self.queue_tree.heading(col, text=col)
            self.queue_tree.column(col, width=120)
        
        queue_scroll = ttk.Scrollbar(queue_frame, orient="vertical", command=self.queue_tree.yview)
        self.queue_tree.configure(yscrollcommand=queue_scroll.set)
        
        self.queue_tree.pack(side='left', fill='both', expand=True, padx=5, pady=5)
        queue_scroll.pack(side='right', fill='y', pady=5)
    
    def create_elevators_tab(self):
        """Create elevator monitoring tab"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="🏗️ Elevators")
        
        self.elevator_frames = []
        
        for i, elevator in enumerate(self.elevators):
            # Elevator frame
            elev_frame = tk.Frame(frame, bg='#34495e', relief='raised', bd=2)
            elev_frame.pack(fill='x', padx=10, pady=5)
            
            # Header
            header_frame = tk.Frame(elev_frame, bg='#34495e')
            header_frame.pack(fill='x', pady=5)
            
            ttk.Label(header_frame, text=f"Elevator {elevator.elevator_id}", 
                     style='Header.TLabel').pack(side='left', padx=10)
            
            # Status indicators
            status_frame = tk.Frame(header_frame, bg='#34495e')
            status_frame.pack(side='right', padx=10)
            
            # Create elevator visualization
            viz_frame = tk.Frame(elev_frame, bg='#34495e')
            viz_frame.pack(fill='both', expand=True, padx=10, pady=5)
            
            # Elevator shaft visualization
            shaft_canvas = tk.Canvas(viz_frame, width=100, height=200, bg='#2c3e50', highlightthickness=1)
            shaft_canvas.pack(side='left', padx=10, pady=10)
            
            # Draw shaft
            shaft_canvas.create_rectangle(10, 10, 90, 190, outline='white', width=2)
            
            # Elevator car (will be updated with position)
            car_rect = shaft_canvas.create_rectangle(15, 170, 85, 190, fill='#3498db', outline='white')
            
            # Level indicators
            for level in range(1, 16):
                y = 190 - (level * 12)
                shaft_canvas.create_line(5, y, 95, y, fill='gray', dash=(2, 2))
                if level % 5 == 0:
                    shaft_canvas.create_text(100, y, text=str(level), fill='white', anchor='w')
            
            # Information panel
            info_frame = tk.Frame(viz_frame, bg='#2c3e50')
            info_frame.pack(side='left', fill='both', expand=True, padx=10, pady=10)
            
            # Create info labels
            info_labels = {}
            info_data = [
                ("Current Level", "1"),
                ("Target Level", "1"),
                ("Position", "0.0 mm"),
                ("Speed", "0.0 mm/s"),
                ("State", "IDLE"),
                ("Load Weight", "0.0 kg"),
                ("Available", "Yes"),
                ("Fault Code", "0")
            ]
            
            for j, (label, value) in enumerate(info_data):
                row_frame = tk.Frame(info_frame, bg='#2c3e50')
                row_frame.pack(fill='x', pady=2)
                
                ttk.Label(row_frame, text=f"{label}:", 
                         foreground='white', background='#2c3e50',
                         font=('Arial', 10)).pack(side='left')
                
                value_label = ttk.Label(row_frame, text=value,
                                       foreground='#3498db', background='#2c3e50',
                                       font=('Arial', 10, 'bold'))
                value_label.pack(side='right')
                
                info_labels[label] = value_label
            
            # Control buttons
            control_frame = tk.Frame(viz_frame, bg='#2c3e50')
            control_frame.pack(side='right', padx=10, pady=10)
            
            # Manual controls
            ttk.Label(control_frame, text="Manual Control", 
                     foreground='white', background='#2c3e50',
                     font=('Arial', 10, 'bold')).pack(pady=5)
            
            # Level selection
            level_frame = tk.Frame(control_frame, bg='#2c3e50')
            level_frame.pack(pady=5)
            
            ttk.Label(level_frame, text="Target Level:", 
                     foreground='white', background='#2c3e50').pack()
            
            target_var = tk.StringVar(value="1")
            target_combo = ttk.Combobox(level_frame, textvariable=target_var,
                                       values=[str(i) for i in range(1, 16)], width=5)
            target_combo.pack(pady=2)
            
            # Control buttons
            move_btn = tk.Button(control_frame, text="Move", 
                               bg='#2ecc71', fg='white', font=('Arial', 9, 'bold'),
                               command=lambda e=i, v=target_var: self.move_elevator(e, v))
            move_btn.pack(pady=2, fill='x')
            
            stop_btn = tk.Button(control_frame, text="Stop",
                               bg='#e74c3c', fg='white', font=('Arial', 9, 'bold'),
                               command=lambda e=i: self.stop_elevator(e))
            stop_btn.pack(pady=2, fill='x')
            
            reset_btn = tk.Button(control_frame, text="Reset",
                                bg='#f39c12', fg='white', font=('Arial', 9, 'bold'),
                                command=lambda e=i: self.reset_elevator(e))
            reset_btn.pack(pady=2, fill='x')
            
            self.elevator_frames.append({
                'canvas': shaft_canvas,
                'car_rect': car_rect,
                'info_labels': info_labels,
                'target_var': target_var
            })
    
    def create_analytics_tab(self):
        """Create analytics and reporting tab"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="📈 Analytics")
        
        # Performance metrics
        metrics_frame = tk.Frame(frame, bg='#34495e', relief='raised', bd=2)
        metrics_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Label(metrics_frame, text="Performance Analytics", style='Header.TLabel').pack(pady=5)
        
        # Create analytics charts
        charts_frame = tk.Frame(frame, bg='#2c3e50')
        charts_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Usage patterns chart
        usage_frame = tk.Frame(charts_frame, bg='#34495e', relief='raised', bd=2)
        usage_frame.pack(side='left', fill='both', expand=True, padx=(0, 5))
        
        ttk.Label(usage_frame, text="Hourly Usage Pattern", style='Header.TLabel').pack(pady=5)
        
        self.usage_fig = Figure(figsize=(6, 4), facecolor='#34495e')
        self.usage_ax = self.usage_fig.add_subplot(111, facecolor='#2c3e50')
        self.usage_ax.set_xlabel('Hour of Day', color='white')
        self.usage_ax.set_ylabel('Transactions', color='white')
        self.usage_ax.tick_params(colors='white')
        
        usage_canvas = FigureCanvasTkAgg(self.usage_fig, usage_frame)
        usage_canvas.get_tk_widget().pack(fill='both', expand=True, padx=5, pady=5)
        
        # Payment methods chart
        payment_frame = tk.Frame(charts_frame, bg='#34495e', relief='raised', bd=2)
        payment_frame.pack(side='right', fill='both', expand=True, padx=(5, 0))
        
        ttk.Label(payment_frame, text="Payment Methods", style='Header.TLabel').pack(pady=5)
        
        self.payment_fig = Figure(figsize=(6, 4), facecolor='#34495e')
        self.payment_ax = self.payment_fig.add_subplot(111, facecolor='#2c3e50')
        
        payment_canvas = FigureCanvasTkAgg(self.payment_fig, payment_frame)
        payment_canvas.get_tk_widget().pack(fill='both', expand=True, padx=5, pady=5)
        
        # Update charts with sample data
        self.update_analytics_charts()
    
    def create_maintenance_tab(self):
        """Create maintenance monitoring tab"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="🔧 Maintenance")
        
        # Maintenance schedule
        schedule_frame = tk.Frame(frame, bg='#34495e', relief='raised', bd=2)
        schedule_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Label(schedule_frame, text="Maintenance Schedule", style='Header.TLabel').pack(pady=5)
        
        # Schedule table
        columns = ("Component", "Last Service", "Next Due", "Status", "Priority")
        self.maintenance_tree = ttk.Treeview(schedule_frame, columns=columns, show='headings', height=8)
        
        for col in columns:
            self.maintenance_tree.heading(col, text=col)
            self.maintenance_tree.column(col, width=150)
        
        maintenance_scroll = ttk.Scrollbar(schedule_frame, orient="vertical", 
                                         command=self.maintenance_tree.yview)
        self.maintenance_tree.configure(yscrollcommand=maintenance_scroll.set)
        
        self.maintenance_tree.pack(side='left', fill='both', expand=True, padx=5, pady=5)
        maintenance_scroll.pack(side='right', fill='y', pady=5)
        
        # System health
        health_frame = tk.Frame(frame, bg='#34495e', relief='raised', bd=2)
        health_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        ttk.Label(health_frame, text="System Health Monitoring", style='Header.TLabel').pack(pady=5)
        
        # Health indicators
        self.create_health_indicators(health_frame)
        
        # Populate maintenance data
        self.populate_maintenance_schedule()
    
    def create_health_indicators(self, parent):
        """Create system health indicators"""
        indicators_frame = tk.Frame(parent, bg='#34495e')
        indicators_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        health_items = [
            ("Elevator 1", "Good", "#2ecc71"),
            ("Elevator 2", "Good", "#2ecc71"),
            ("Elevator 3", "Warning", "#f39c12"),
            ("Platform System", "Good", "#2ecc71"),
            ("Hydraulic System", "Good", "#2ecc71"),
            ("Payment System", "Good", "#2ecc71"),
            ("Safety Systems", "Good", "#2ecc71"),
            ("Network", "Good", "#2ecc71")
        ]
        
        for i, (component, status, color) in enumerate(health_items):
            row = i // 4
            col = i % 4
            
            item_frame = tk.Frame(indicators_frame, bg='#2c3e50', relief='raised', bd=1)
            item_frame.grid(row=row, column=col, padx=5, pady=5, sticky='ew')
            
            ttk.Label(item_frame, text=component, 
                     foreground='white', background='#2c3e50',
                     font=('Arial', 10, 'bold')).pack(pady=2)
            
            status_label = ttk.Label(item_frame, text=status,
                                   foreground=color, background='#2c3e50',
                                   font=('Arial', 9))
            status_label.pack(pady=2)
            
            # Status indicator
            indicator = tk.Canvas(item_frame, width=30, height=10, bg='#2c3e50', highlightthickness=0)
            indicator.pack(pady=2)
            indicator.create_oval(10, 2, 20, 8, fill=color, outline=color)
        
        for i in range(4):
            indicators_frame.grid_columnconfigure(i, weight=1)
    
    def create_logs_tab(self):
        """Create system logs tab"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="📋 System Logs")
        
        # Log filters
        filter_frame = tk.Frame(frame, bg='#34495e', relief='raised', bd=2)
        filter_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(filter_frame, text="Log Filters", style='Header.TLabel').pack(side='left', padx=10, pady=5)
        
        # Filter controls
        filter_controls = tk.Frame(filter_frame, bg='#34495e')
        filter_controls.pack(side='right', padx=10, pady=5)
        
        ttk.Label(filter_controls, text="Level:", style='Status.TLabel').pack(side='left', padx=5)
        
        self.log_level_var = tk.StringVar(value="All")
        level_combo = ttk.Combobox(filter_controls, textvariable=self.log_level_var,
                                  values=["All", "Info", "Warning", "Error", "Critical"], width=10)
        level_combo.pack(side='left', padx=5)
        
        refresh_btn = tk.Button(filter_controls, text="Refresh", command=self.refresh_logs,
                              bg='#3498db', fg='white', font=('Arial', 9, 'bold'))
        refresh_btn.pack(side='left', padx=5)
        
        # Logs display
        logs_frame = tk.Frame(frame, bg='#2c3e50')
        logs_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.logs_text = scrolledtext.ScrolledText(logs_frame, 
                                                  bg='#2c3e50', fg='white',
                                                  font=('Courier', 9),
                                                  wrap=tk.WORD)
        self.logs_text.pack(fill='both', expand=True)
        
        # Add sample logs
        self.add_sample_logs()
    
    def update_parking_grid(self, event=None):
        """Update parking grid visualization"""
        level = int(self.level_var.get())
        self.grid_canvas.delete("all")
        
        canvas_width = self.grid_canvas.winfo_width()
        canvas_height = self.grid_canvas.winfo_height()
        
        if canvas_width <= 1 or canvas_height <= 1:
            self.root.after(100, self.update_parking_grid)
            return
        
        # Grid dimensions
        cols = 20  # 20 spaces per level
        rows = 1   # 1 row for single level view
        
        cell_width = (canvas_width - 40) // cols
        cell_height = (canvas_height - 40) // rows
        
        # Draw grid
        for pos in range(20):  # 20 positions per level
            x = 20 + pos * cell_width
            y = 20
            
            space = self.parking_spaces[level-1][pos]
            
            # Determine color based on status
            if space.occupied:
                color = "#e74c3c"  # Red for occupied
            else:
                color = "#2ecc71"  # Green for available
            
            # Draw space rectangle
            rect = self.grid_canvas.create_rectangle(x, y, x + cell_width - 2, y + cell_height - 2,
                                                   fill=color, outline='white', width=2)
            
            # Add position number
            self.grid_canvas.create_text(x + cell_width//2, y + cell_height//2,
                                       text=str(pos + 1), fill='white',
                                       font=('Arial', 10, 'bold'))
            
            # Add vehicle ID if occupied
            if space.occupied and space.vehicle_id:
                self.grid_canvas.create_text(x + cell_width//2, y + cell_height//2 + 15,
                                           text=space.vehicle_id, fill='white',
                                           font=('Arial', 8))
    
    def update_analytics_charts(self):
        """Update analytics charts with sample data"""
        # Usage pattern chart
        hours = list(range(24))
        usage_data = [random.randint(5, 40) for _ in hours]
        
        self.usage_ax.clear()
        self.usage_ax.bar(hours, usage_data, color='#3498db', alpha=0.7)
        self.usage_ax.set_xlabel('Hour of Day', color='white')
        self.usage_ax.set_ylabel('Transactions', color='white')
        self.usage_ax.tick_params(colors='white')
        self.usage_ax.set_facecolor('#2c3e50')
        self.usage_fig.patch.set_facecolor('#34495e')
        
        # Payment methods pie chart
        payment_methods = ['Cash', 'Credit Card', 'RFID', 'Mobile']
        payment_data = [25, 45, 20, 10]
        colors = ['#3498db', '#2ecc71', '#f39c12', '#9b59b6']
        
        self.payment_ax.clear()
        self.payment_ax.pie(payment_data, labels=payment_methods, colors=colors,
                           autopct='%1.1f%%', textprops={'color': 'white'})
        self.payment_ax.set_facecolor('#2c3e50')
        self.payment_fig.patch.set_facecolor('#34495e')
        
        # Refresh canvases
        self.usage_fig.tight_layout()
        self.payment_fig.tight_layout()
    
    def populate_maintenance_schedule(self):
        """Populate maintenance schedule with sample data"""
        maintenance_items = [
            ("Elevator 1 Motor", "2025-05-15", "2025-07-15", "OK", "Normal"),
            ("Elevator 2 Motor", "2025-05-10", "2025-07-10", "OK", "Normal"),
            ("Elevator 3 Motor", "2025-04-20", "2025-06-20", "Due Soon", "High"),
            ("Platform System", "2025-05-01", "2025-08-01", "OK", "Normal"),
            ("Hydraulic Pump", "2025-05-20", "2025-08-20", "OK", "Normal"),
            ("Safety Systems", "2025-05-25", "2025-06-25", "Due Soon", "High"),
            ("Payment Kiosks", "2025-05-05", "2025-08-05", "OK", "Normal"),
            ("Network Equipment", "2025-04-15", "2025-07-15", "OK", "Normal")
        ]
        
        for item in maintenance_items:
            self.maintenance_tree.insert("", "end", values=item)
    
    def add_sample_logs(self):
        """Add sample system logs"""
        logs = [
            "[2025-06-08 14:30:15] INFO: System started successfully",
            "[2025-06-08 14:30:16] INFO: All elevators initialized",
            "[2025-06-08 14:30:17] INFO: Platform system ready",
            "[2025-06-08 14:30:18] INFO: Payment system online",
            "[2025-06-08 14:35:22] INFO: Vehicle ABC123 parked at Level 3, Position 15",
            "[2025-06-08 14:40:11] INFO: Payment received: $15.50 via Credit Card",
            "[2025-06-08 14:45:33] WARNING: Elevator 3 minor vibration detected",
            "[2025-06-08 14:50:44] INFO: Vehicle XYZ789 retrieved from Level 5, Position 8",
            "[2025-06-08 14:55:12] INFO: Maintenance reminder: Elevator 3 service due",
            "[2025-06-08 15:00:00] INFO: System status: 85% capacity, 45 vehicles parked"
        ]
        
        for log in logs:
            self.logs_text.insert(tk.END, log + "\n")
    
    def refresh_logs(self):
        """Refresh log display"""
        self.logs_text.delete(1.0, tk.END)
        self.add_sample_logs()
        # Add current timestamp log
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.logs_text.insert(tk.END, f"[{current_time}] INFO: Logs refreshed\n")
    
    def simulate_parking(self):
        """Simulate a parking operation"""
        vehicle_id = f"SIM{random.randint(100, 999)}"
        self.system_status.state = "PARKING"
        self.add_log(f"Simulating parking for vehicle {vehicle_id}")
        
        # Simulate parking sequence
        def parking_sequence():
            time.sleep(2)
            self.system_status.vehicles_parked += 1
            self.system_status.occupied_spaces += 1
            self.system_status.state = "IDLE"
            self.add_log(f"Vehicle {vehicle_id} parked successfully")
        
        threading.Thread(target=parking_sequence, daemon=True).start()
    
    def simulate_retrieval(self):
        """Simulate a retrieval operation"""
        if self.system_status.occupied_spaces > 0:
            vehicle_id = f"RET{random.randint(100, 999)}"
            self.system_status.state = "RETRIEVAL"
            self.add_log(f"Simulating retrieval for vehicle {vehicle_id}")
            
            def retrieval_sequence():
                time.sleep(3)
                self.system_status.vehicles_retrieved += 1
                self.system_status.occupied_spaces -= 1
                self.system_status.state = "IDLE"
                self.add_log(f"Vehicle {vehicle_id} retrieved successfully")
            
            threading.Thread(target=retrieval_sequence, daemon=True).start()
        else:
            messagebox.showinfo("Info", "No vehicles to retrieve")
    
    def emergency_stop(self):
        """Emergency stop procedure"""
        self.system_status.emergency_active = True
        self.system_status.state = "EMERGENCY"
        self.add_log("EMERGENCY STOP ACTIVATED", "ERROR")
        messagebox.showwarning("Emergency Stop", "Emergency stop activated!")
    
    def toggle_maintenance(self):
        """Toggle maintenance mode"""
        self.system_status.maintenance_mode = not self.system_status.maintenance_mode
        if self.system_status.maintenance_mode:
            self.system_status.state = "MAINTENANCE"
            self.add_log("Maintenance mode activated", "WARNING")
        else:
            self.system_status.state = "IDLE"
            self.add_log("Maintenance mode deactivated", "INFO")
    
    def reset_system(self):
        """Reset system to normal operation"""
        self.system_status.emergency_active = False
        self.system_status.maintenance_mode = False
        self.system_status.state = "IDLE"
        self.add_log("System reset to normal operation", "INFO")
        messagebox.showinfo("Reset", "System reset successfully")
    
    def move_elevator(self, elevator_index, target_var):
        """Move elevator to target level"""
        target_level = int(target_var.get())
        elevator = self.elevators[elevator_index]
        
        if elevator.available:
            elevator.target_level = target_level
            elevator.state = "MOVING"
            self.add_log(f"Elevator {elevator.elevator_id} moving to level {target_level}")
            
            def move_sequence():
                # Simulate movement
                start_level = elevator.current_level
                steps = abs(target_level - start_level)
                for i in range(steps + 1):
                    if start_level < target_level:
                        elevator.current_level = start_level + i
                    else:
                        elevator.current_level = start_level - i
                    elevator.position = (elevator.current_level - 1) * 3000.0
                    time.sleep(0.5)
                
                elevator.state = "IDLE"
                self.add_log(f"Elevator {elevator.elevator_id} reached level {target_level}")
            
            threading.Thread(target=move_sequence, daemon=True).start()
        else:
            messagebox.showwarning("Warning", f"Elevator {elevator.elevator_id} not available")
    
    def stop_elevator(self, elevator_index):
        """Stop elevator"""
        elevator = self.elevators[elevator_index]
        elevator.state = "STOPPED"
        self.add_log(f"Elevator {elevator.elevator_id} stopped", "WARNING")
    
    def reset_elevator(self, elevator_index):
        """Reset elevator"""
        elevator = self.elevators[elevator_index]
        elevator.state = "IDLE"
        elevator.available = True
        elevator.fault_code = 0
        self.add_log(f"Elevator {elevator.elevator_id} reset", "INFO")
    
    def add_log(self, message, level="INFO"):
        """Add log entry"""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {level}: {message}\n"
        self.logs_text.insert(tk.END, log_entry)
        self.logs_text.see(tk.END)
    
    def data_update_loop(self):
        """Background data update loop"""
        while self.running:
            try:
                self.update_gui_data()
                time.sleep(1)  # Update every second
            except Exception as e:
                print(f"Update error: {e}")
    
    def update_gui_data(self):
        """Update GUI with current data"""
        # Update system metrics
        self.metric_labels["Occupied"].config(text=str(self.system_status.occupied_spaces))
        self.metric_labels["Available"].config(text=str(300 - self.system_status.occupied_spaces))
        self.metric_labels["Revenue Today"].config(text=f"${self.system_status.revenue_today:.2f}")
        
        # Update system state
        state_colors = {
            "IDLE": "#2ecc71",
            "PARKING": "#f39c12",
            "RETRIEVAL": "#3498db",
            "EMERGENCY": "#e74c3c",
            "MAINTENANCE": "#9b59b6"
        }
        
        self.state_label.config(text=self.system_status.state,
                               foreground=state_colors.get(self.system_status.state, "#2ecc71"))
        
        # Update status light
        if self.system_status.emergency_active:
            self.status_light.itemconfig(self.status_circle, fill='red')
            self.system_status_label.config(text="System: EMERGENCY")
        elif self.system_status.maintenance_mode:
            self.status_light.itemconfig(self.status_circle, fill='orange')
            self.system_status_label.config(text="System: MAINTENANCE")
        else:
            self.status_light.itemconfig(self.status_circle, fill='green')
            self.system_status_label.config(text="System: ONLINE")
        
        # Update elevator displays
        for i, (elevator, frame_data) in enumerate(zip(self.elevators, self.elevator_frames)):
            # Update position on shaft
            level_height = 12  # pixels per level on display
            car_y = 190 - (elevator.current_level * level_height)
            frame_data['canvas'].coords(frame_data['car_rect'], 15, car_y-10, 85, car_y+10)
            
            # Update info labels
            frame_data['info_labels']["Current Level"].config(text=str(elevator.current_level))
            frame_data['info_labels']["Target Level"].config(text=str(elevator.target_level))
            frame_data['info_labels']["Position"].config(text=f"{elevator.position:.1f} mm")
            frame_data['info_labels']["Speed"].config(text=f"{elevator.speed:.1f} mm/s")
            frame_data['info_labels']["State"].config(text=elevator.state)
            frame_data['info_labels']["Load Weight"].config(text=f"{elevator.load_weight:.1f} kg")
            frame_data['info_labels']["Available"].config(text="Yes" if elevator.available else "No")
            frame_data['info_labels']["Fault Code"].config(text=str(elevator.fault_code))
        
        # Update occupancy chart
        if hasattr(self, 'occupancy_ax'):
            levels = list(range(1, 16))
            occupancy = [random.randint(60, 95) for _ in levels]  # Simulate occupancy data
            
            self.occupancy_ax.clear()
            self.occupancy_ax.bar(levels, occupancy, color='#3498db', alpha=0.7)
            self.occupancy_ax.set_xlabel('Level', color='white')
            self.occupancy_ax.set_ylabel('Occupancy %', color='white')
            self.occupancy_ax.tick_params(colors='white')
            self.occupancy_ax.set_facecolor('#2c3e50')
            self.occupancy_canvas.draw()
    
    def on_closing(self):
        """Handle application closing"""
        self.running = False
        self.conn.close()
        self.root.destroy()
    
    def run(self):
        """Start the GUI application"""
        self.root.mainloop()

if __name__ == "__main__":
    app = ParkingSystemHMI()
    app.run()
