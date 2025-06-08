#!/usr/bin/env python3
"""
Process Diagram Generator for Water Treatment System
Creates visual process flow diagrams in PNG and PDF formats
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, ConnectionPatch, Circle, Rectangle
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages
import os

class ProcessDiagramGenerator:
    def __init__(self):
        self.fig_size = (16, 12)
        self.colors = {
            'water': '#2196F3',
            'seawater': '#006064',
            'treated_water': '#4FC3F7',
            'equipment': '#FFB74D',
            'tank': '#81C784',
            'pump': '#FF8A65',
            'filter': '#A1887F',
            'membrane': '#9C27B0',
            'chemical': '#FFC107',
            'pipe': '#455A64',
            'text': '#212121'
        }
        
    def create_main_process_diagram(self):
        """Create the main process flow diagram"""
        fig, ax = plt.subplots(1, 1, figsize=self.fig_size)
        ax.set_xlim(0, 20)
        ax.set_ylim(0, 15)
        ax.set_aspect('equal')
        ax.axis('off')
        
        # Title
        ax.text(10, 14.5, 'Water Treatment System - Process Flow Diagram', 
                fontsize=20, fontweight='bold', ha='center', color=self.colors['text'])
        
        # Seawater intake
        seawater_intake = FancyBboxPatch((0.5, 12), 2, 1.5, boxstyle="round,pad=0.1", 
                                       facecolor=self.colors['seawater'], edgecolor='black', linewidth=2)
        ax.add_patch(seawater_intake)
        ax.text(1.5, 12.75, 'Seawater\nIntake', ha='center', va='center', fontweight='bold', color='white')
        
        # Seawater storage tank
        seawater_tank = Rectangle((4, 11.5), 2, 2.5, facecolor=self.colors['tank'], 
                                edgecolor='black', linewidth=2)
        ax.add_patch(seawater_tank)
        ax.text(5, 12.75, 'Seawater\nStorage\nTank', ha='center', va='center', fontweight='bold')
        
        # Pre-treatment system
        pretreat_box = FancyBboxPatch((8, 11.5), 3, 2.5, boxstyle="round,pad=0.1", 
                                    facecolor=self.colors['filter'], edgecolor='black', linewidth=2)
        ax.add_patch(pretreat_box)
        ax.text(9.5, 12.75, 'Pre-Treatment\n• Sand Filter\n• Carbon Filter\n• Antiscalant', 
                ha='center', va='center', fontweight='bold')
        
        # High pressure pump
        hp_pump = Circle((13, 12.75), 0.8, facecolor=self.colors['pump'], 
                        edgecolor='black', linewidth=2)
        ax.add_patch(hp_pump)
        ax.text(13, 12.75, 'HP\nPump', ha='center', va='center', fontweight='bold')
        
        # RO membrane system
        ro_system = FancyBboxPatch((15, 11), 3.5, 3.5, boxstyle="round,pad=0.1", 
                                 facecolor=self.colors['membrane'], edgecolor='black', linewidth=2)
        ax.add_patch(ro_system)
        ax.text(16.75, 12.75, 'Reverse Osmosis\nMembrane System\n\nPermeate ↓\nConcentrate →', 
                ha='center', va='center', fontweight='bold', color='white')
        
        # Treated water tank
        treated_tank = Rectangle((15.5, 7.5), 2.5, 2.5, facecolor=self.colors['treated_water'], 
                                edgecolor='black', linewidth=2)
        ax.add_patch(treated_tank)
        ax.text(16.75, 8.75, 'Treated\nWater\nTank', ha='center', va='center', fontweight='bold')
        
        # Post-treatment
        posttreat_box = FancyBboxPatch((12, 7.5), 2.5, 2.5, boxstyle="round,pad=0.1", 
                                     facecolor=self.colors['chemical'], edgecolor='black', linewidth=2)
        ax.add_patch(posttreat_box)
        ax.text(13.25, 8.75, 'Post-Treatment\n• pH Adjustment\n• Chlorination', 
                ha='center', va='center', fontweight='bold')
        
        # Distribution pumps
        dist_pump1 = Circle((9, 8.75), 0.6, facecolor=self.colors['pump'], 
                          edgecolor='black', linewidth=2)
        ax.add_patch(dist_pump1)
        ax.text(9, 8.75, 'P1', ha='center', va='center', fontweight='bold')
        
        dist_pump2 = Circle((7, 8.75), 0.6, facecolor=self.colors['pump'], 
                          edgecolor='black', linewidth=2)
        ax.add_patch(dist_pump2)
        ax.text(7, 8.75, 'P2', ha='center', va='center', fontweight='bold')
        
        dist_pump3 = Circle((5, 8.75), 0.6, facecolor=self.colors['pump'], 
                          edgecolor='black', linewidth=2)
        ax.add_patch(dist_pump3)
        ax.text(5, 8.75, 'P3', ha='center', va='center', fontweight='bold')
        
        # Roof tanks
        roof_tank1 = Rectangle((1, 4), 2, 2.5, facecolor=self.colors['tank'], 
                             edgecolor='black', linewidth=2)
        ax.add_patch(roof_tank1)
        ax.text(2, 5.25, 'Roof Tank 1\nNorth Zone', ha='center', va='center', fontweight='bold')
        
        roof_tank2 = Rectangle((5, 4), 2, 2.5, facecolor=self.colors['tank'], 
                             edgecolor='black', linewidth=2)
        ax.add_patch(roof_tank2)
        ax.text(6, 5.25, 'Roof Tank 2\nSouth Zone', ha='center', va='center', fontweight='bold')
        
        roof_tank3 = Rectangle((9, 4), 2, 2.5, facecolor=self.colors['tank'], 
                             edgecolor='black', linewidth=2)
        ax.add_patch(roof_tank3)
        ax.text(10, 5.25, 'Roof Tank 3\nEast Zone', ha='center', va='center', fontweight='bold')
        
        # Waste/concentrate handling
        waste_tank = Rectangle((19, 8), 1.5, 1.5, facecolor='#F44336', 
                             edgecolor='black', linewidth=2)
        ax.add_patch(waste_tank)
        ax.text(19.75, 8.75, 'Waste\nTank', ha='center', va='center', fontweight='bold', color='white')
        
        # Connections (pipes)
        self.draw_pipe(ax, [(2.5, 12.75), (4, 12.75)], self.colors['seawater'])
        self.draw_pipe(ax, [(6, 12.75), (8, 12.75)], self.colors['seawater'])
        self.draw_pipe(ax, [(11, 12.75), (12.2, 12.75)], self.colors['seawater'])
        self.draw_pipe(ax, [(13.8, 12.75), (15, 12.75)], self.colors['seawater'])
        
        # Permeate line
        self.draw_pipe(ax, [(16.75, 11), (16.75, 10)], self.colors['treated_water'])
        
        # Post-treatment line
        self.draw_pipe(ax, [(15.5, 8.75), (14.5, 8.75)], self.colors['treated_water'])
        self.draw_pipe(ax, [(12, 8.75), (9.6, 8.75)], self.colors['treated_water'])
        
        # Distribution lines
        self.draw_pipe(ax, [(7, 8.15), (6, 6.5)], self.colors['treated_water'])
        self.draw_pipe(ax, [(5, 8.15), (2, 6.5)], self.colors['treated_water'])
        self.draw_pipe(ax, [(9, 8.15), (10, 6.5)], self.colors['treated_water'])
        
        # Concentrate line
        self.draw_pipe(ax, [(18.5, 12.75), (19.75, 9.5)], '#F44336')
        
        # Add flow direction arrows
        self.add_flow_arrows(ax)
        
        # Add legend
        self.add_legend(ax)
        
        # Add process parameters
        self.add_process_parameters(ax)
        
        plt.tight_layout()
        return fig
    
    def draw_pipe(self, ax, points, color, linewidth=3):
        """Draw a pipe connection between points"""
        for i in range(len(points) - 1):
            x_start, y_start = points[i]
            x_end, y_end = points[i + 1]
            ax.plot([x_start, x_end], [y_start, y_end], color=color, linewidth=linewidth)
    
    def add_flow_arrows(self, ax):
        """Add flow direction arrows"""
        arrow_props = dict(arrowstyle='->', connectionstyle='arc3', color='red', lw=2)
        
        # Main flow arrows
        ax.annotate('', xy=(3.8, 13), xytext=(2.7, 13), arrowprops=arrow_props)
        ax.annotate('', xy=(7.8, 13), xytext=(6.2, 13), arrowprops=arrow_props)
        ax.annotate('', xy=(12, 13), xytext=(11.2, 13), arrowprops=arrow_props)
        ax.annotate('', xy=(14.8, 13), xytext=(14, 13), arrowprops=arrow_props)
        
        # Permeate arrow
        ax.annotate('', xy=(16.5, 10.2), xytext=(16.5, 10.8), arrowprops=arrow_props)
        
        # Distribution arrows
        ax.annotate('', xy=(5.8, 6.8), xytext=(6.8, 8), arrowprops=arrow_props)
        ax.annotate('', xy=(2.2, 6.8), xytext=(4.8, 8), arrowprops=arrow_props)
        ax.annotate('', xy=(9.8, 6.8), xytext=(9.2, 8), arrowprops=arrow_props)
    
    def add_legend(self, ax):
        """Add color legend"""
        legend_x = 0.5
        legend_y = 2
        
        ax.text(legend_x, legend_y + 0.8, 'Legend:', fontsize=12, fontweight='bold')
        
        # Legend items
        legend_items = [
            ('Seawater', self.colors['seawater']),
            ('Treated Water', self.colors['treated_water']),
            ('Equipment', self.colors['equipment']),
            ('Storage Tank', self.colors['tank']),
            ('Pump', self.colors['pump']),
            ('Waste', '#F44336')
        ]
        
        for i, (label, color) in enumerate(legend_items):
            y_pos = legend_y - i * 0.3
            legend_patch = Rectangle((legend_x, y_pos - 0.1), 0.3, 0.2, 
                                   facecolor=color, edgecolor='black')
            ax.add_patch(legend_patch)
            ax.text(legend_x + 0.4, y_pos, label, fontsize=10, va='center')
    
    def add_process_parameters(self, ax):
        """Add key process parameters"""
        param_x = 13
        param_y = 2.5
        
        ax.text(param_x, param_y + 1, 'Key Process Parameters:', 
                fontsize=12, fontweight='bold')
        
        parameters = [
            'Production Capacity: 10,000 L/hour',
            'RO Recovery Rate: 45%',
            'Operating Pressure: 55 bar',
            'Energy Consumption: ~125 kW',
            'Water Quality: <200 ppm TDS',
            'Distribution Zones: 3',
            'Storage Capacity: 30,000 L'
        ]
        
        for i, param in enumerate(parameters):
            ax.text(param_x, param_y - i * 0.25, f'• {param}', fontsize=9)
    
    def create_piping_instrumentation_diagram(self):
        """Create P&ID (Piping and Instrumentation Diagram)"""
        fig, ax = plt.subplots(1, 1, figsize=self.fig_size)
        ax.set_xlim(0, 20)
        ax.set_ylim(0, 15)
        ax.set_aspect('equal')
        ax.axis('off')
        
        # Title
        ax.text(10, 14.5, 'Water Treatment System - P&ID', 
                fontsize=20, fontweight='bold', ha='center')
        
        # Add instrumentation symbols
        self.add_instrumentation_symbols(ax)
        
        # Add valve symbols
        self.add_valve_symbols(ax)
        
        # Add sensor locations
        self.add_sensor_symbols(ax)
        
        plt.tight_layout()
        return fig
    
    def add_instrumentation_symbols(self, ax):
        """Add standard P&ID instrumentation symbols"""
        # Pressure indicators
        pi_circle1 = Circle((3, 13), 0.3, facecolor='white', edgecolor='black', linewidth=2)
        ax.add_patch(pi_circle1)
        ax.text(3, 13, 'PI\n001', ha='center', va='center', fontsize=8, fontweight='bold')
        
        # Flow indicators
        fi_circle1 = Circle((7, 13), 0.3, facecolor='white', edgecolor='black', linewidth=2)
        ax.add_patch(fi_circle1)
        ax.text(7, 13, 'FI\n001', ha='center', va='center', fontsize=8, fontweight='bold')
        
        # Level indicators
        li_circle1 = Circle((5, 11), 0.3, facecolor='white', edgecolor='black', linewidth=2)
        ax.add_patch(li_circle1)
        ax.text(5, 11, 'LI\n001', ha='center', va='center', fontsize=8, fontweight='bold')
        
        # Quality analyzers
        qi_circle1 = Circle((16, 9), 0.3, facecolor='white', edgecolor='black', linewidth=2)
        ax.add_patch(qi_circle1)
        ax.text(16, 9, 'QI\n001', ha='center', va='center', fontsize=8, fontweight='bold')
    
    def add_valve_symbols(self, ax):
        """Add valve symbols"""
        # Ball valves
        valve_positions = [(4.5, 12.75), (7.5, 12.75), (11.5, 12.75)]
        for pos in valve_positions:
            valve = Rectangle((pos[0] - 0.2, pos[1] - 0.2), 0.4, 0.4, 
                            facecolor='white', edgecolor='black', linewidth=2)
            ax.add_patch(valve)
            ax.plot([pos[0] - 0.15, pos[0] + 0.15], [pos[1] - 0.15, pos[1] + 0.15], 
                   'k-', linewidth=2)
    
    def add_sensor_symbols(self, ax):
        """Add sensor symbols"""
        # Temperature sensors
        temp_positions = [(6, 12.5), (14, 12.5), (17, 8.5)]
        for pos in temp_positions:
            temp_sensor = Circle(pos, 0.15, facecolor='yellow', edgecolor='black')
            ax.add_patch(temp_sensor)
            ax.text(pos[0], pos[1], 'T', ha='center', va='center', fontsize=8, fontweight='bold')
        
        # Pressure sensors
        press_positions = [(8.5, 12.3), (13.5, 12.3), (16.5, 12.3)]
        for pos in press_positions:
            press_sensor = Circle(pos, 0.15, facecolor='lightblue', edgecolor='black')
            ax.add_patch(press_sensor)
            ax.text(pos[0], pos[1], 'P', ha='center', va='center', fontsize=8, fontweight='bold')
    
    def create_control_system_diagram(self):
        """Create control system architecture diagram"""
        fig, ax = plt.subplots(1, 1, figsize=(14, 10))
        ax.set_xlim(0, 14)
        ax.set_ylim(0, 10)
        ax.set_aspect('equal')
        ax.axis('off')
        
        # Title
        ax.text(7, 9.5, 'Control System Architecture', 
                fontsize=18, fontweight='bold', ha='center')
        
        # HMI/SCADA Level
        hmi_box = FancyBboxPatch((5, 8), 4, 1, boxstyle="round,pad=0.1", 
                               facecolor='lightgreen', edgecolor='black', linewidth=2)
        ax.add_patch(hmi_box)
        ax.text(7, 8.5, 'HMI/SCADA System\nOperator Interface', 
                ha='center', va='center', fontweight='bold')
        
        # PLC Level
        plc_box = FancyBboxPatch((5.5, 6), 3, 1, boxstyle="round,pad=0.1", 
                               facecolor='lightblue', edgecolor='black', linewidth=2)
        ax.add_patch(plc_box)
        ax.text(7, 6.5, 'PLC Controller\nProcess Control Logic', 
                ha='center', va='center', fontweight='bold')
        
        # I/O Modules
        io_boxes = [
            (1, 4, 'Digital\nInputs'),
            (3.5, 4, 'Digital\nOutputs'),
            (6, 4, 'Analog\nInputs'),
            (8.5, 4, 'Analog\nOutputs'),
            (11, 4, 'Communication\nModules')
        ]
        
        for x, y, label in io_boxes:
            io_box = FancyBboxPatch((x, y), 2, 1, boxstyle="round,pad=0.1", 
                                  facecolor='lightyellow', edgecolor='black', linewidth=2)
            ax.add_patch(io_box)
            ax.text(x + 1, y + 0.5, label, ha='center', va='center', fontweight='bold')
        
        # Field devices
        field_devices = [
            (1, 2, 'Pumps\nMotors'),
            (3.5, 2, 'Valves\nActuators'),
            (6, 2, 'Sensors\nTransmitters'),
            (8.5, 2, 'VFDs\nControls'),
            (11, 2, 'Remote\nI/O')
        ]
        
        for x, y, label in field_devices:
            device_box = FancyBboxPatch((x, y), 2, 1, boxstyle="round,pad=0.1", 
                                      facecolor='lightcoral', edgecolor='black', linewidth=2)
            ax.add_patch(device_box)
            ax.text(x + 1, y + 0.5, label, ha='center', va='center', fontweight='bold')
        
        # Connections
        connection_lines = [
            [(7, 8), (7, 7)],  # HMI to PLC
            [(6, 6), (2, 5)],  # PLC to Digital Inputs
            [(6.5, 6), (4.5, 5)],  # PLC to Digital Outputs
            [(7, 6), (7, 5)],  # PLC to Analog Inputs
            [(7.5, 6), (9.5, 5)],  # PLC to Analog Outputs
            [(8, 6), (12, 5)],  # PLC to Communication
            [(2, 4), (2, 3)],  # I/O to Field devices
            [(4.5, 4), (4.5, 3)],
            [(7, 4), (7, 3)],
            [(9.5, 4), (9.5, 3)],
            [(12, 4), (12, 3)]
        ]
        
        for line in connection_lines:
            ax.plot([line[0][0], line[1][0]], [line[0][1], line[1][1]], 
                   'k-', linewidth=2)
        
        plt.tight_layout()
        return fig
    
    def create_process_flowchart(self):
        """Create detailed process flowchart with decision points and control logic"""
        fig, ax = plt.subplots(1, 1, figsize=(20, 24))
        ax.set_xlim(0, 20)
        ax.set_ylim(0, 24)
        ax.set_aspect('equal')
        ax.axis('off')
        
        # Title
        ax.text(10, 23.5, 'Water Treatment System - Process Control Flowchart', 
                fontsize=20, fontweight='bold', ha='center', color=self.colors['text'])
        
        # Define flowchart elements
        flowchart_elements = []
        
        # Start
        start_oval = patches.Ellipse((10, 22.5), 3, 0.8, facecolor='lightgreen', 
                                   edgecolor='black', linewidth=2)
        ax.add_patch(start_oval)
        ax.text(10, 22.5, 'SYSTEM START', ha='center', va='center', fontweight='bold', fontsize=12)
        
        # System initialization
        init_rect = FancyBboxPatch((8.5, 21), 3, 0.8, boxstyle="round,pad=0.1", 
                                 facecolor='lightblue', edgecolor='black', linewidth=2)
        ax.add_patch(init_rect)
        ax.text(10, 21.4, 'Initialize System\nCheck Safety Interlocks', ha='center', va='center', fontweight='bold')
        
        # Decision: Emergency stop?
        self.draw_diamond(ax, 10, 19.8, 2.5, 1, 'Emergency\nStop?', 'yellow')
        
        # Emergency stop path
        emergency_rect = FancyBboxPatch((15, 19.3), 3, 0.8, boxstyle="round,pad=0.1", 
                                      facecolor='red', edgecolor='black', linewidth=2)
        ax.add_patch(emergency_rect)
        ax.text(16.5, 19.7, 'EMERGENCY STOP\nShutdown All Systems', ha='center', va='center', 
                fontweight='bold', color='white')
        
        # Check tank levels
        self.draw_diamond(ax, 10, 18.5, 3, 1, 'Seawater Tank\nLevel > 20%?', 'lightcyan')
        
        # Low level alarm
        low_level_rect = FancyBboxPatch((1, 18), 3, 0.8, boxstyle="round,pad=0.1", 
                                      facecolor='orange', edgecolor='black', linewidth=2)
        ax.add_patch(low_level_rect)
        ax.text(2.5, 18.4, 'LOW LEVEL ALARM\nWait for Fill', ha='center', va='center', fontweight='bold')
        
        # Start intake pump
        intake_rect = FancyBboxPatch((8.5, 17), 3, 0.8, boxstyle="round,pad=0.1", 
                                   facecolor='lightgreen', edgecolor='black', linewidth=2)
        ax.add_patch(intake_rect)
        ax.text(10, 17.4, 'Start Intake Pump\nFill Seawater Tank', ha='center', va='center', fontweight='bold')
        
        # Check pre-treatment system
        self.draw_diamond(ax, 10, 15.8, 3, 1, 'Pre-treatment\nSystem Ready?', 'lightcyan')
        
        # Pre-treatment maintenance
        pretreat_maint = FancyBboxPatch((15, 15.3), 3.5, 0.8, boxstyle="round,pad=0.1", 
                                      facecolor='orange', edgecolor='black', linewidth=2)
        ax.add_patch(pretreat_maint)
        ax.text(16.75, 15.7, 'MAINTENANCE REQUIRED\nCheck Filters & Antiscalant', 
                ha='center', va='center', fontweight='bold')
        
        # Start pre-treatment
        pretreat_rect = FancyBboxPatch((8.5, 14.5), 3, 0.8, boxstyle="round,pad=0.1", 
                                     facecolor='lightgreen', edgecolor='black', linewidth=2)
        ax.add_patch(pretreat_rect)
        ax.text(10, 14.9, 'Start Pre-treatment\nSand & Carbon Filters', ha='center', va='center', fontweight='bold')
        
        # Check feed pressure
        self.draw_diamond(ax, 10, 13.3, 3, 1, 'Feed Pressure\n2-4 bar?', 'lightcyan')
        
        # Pressure control
        pressure_rect = FancyBboxPatch((15, 12.8), 3.5, 0.8, boxstyle="round,pad=0.1", 
                                     facecolor='yellow', edgecolor='black', linewidth=2)
        ax.add_patch(pressure_rect)
        ax.text(16.75, 13.2, 'ADJUST PRESSURE\nControl Feed Pump VFD', ha='center', va='center', fontweight='bold')
        
        # Start RO system
        ro_rect = FancyBboxPatch((8.5, 12), 3, 0.8, boxstyle="round,pad=0.1", 
                               facecolor='lightgreen', edgecolor='black', linewidth=2)
        ax.add_patch(ro_rect)
        ax.text(10, 12.4, 'Start RO System\nHigh Pressure Pump', ha='center', va='center', fontweight='bold')
        
        # RO pressure control
        self.draw_diamond(ax, 10, 10.8, 3, 1, 'RO Pressure\n50-60 bar?', 'lightcyan')
        
        # Pressure adjustment
        ro_pressure_rect = FancyBboxPatch((15, 10.3), 3.5, 0.8, boxstyle="round,pad=0.1", 
                                        facecolor='yellow', edgecolor='black', linewidth=2)
        ax.add_patch(ro_pressure_rect)
        ax.text(16.75, 10.7, 'ADJUST RO PRESSURE\nPID Control HP Pump', ha='center', va='center', fontweight='bold')
        
        # Check permeate quality
        self.draw_diamond(ax, 10, 9.3, 3, 1, 'Permeate Quality\n< 200 ppm?', 'lightcyan')
        
        # Quality control
        quality_rect = FancyBboxPatch((1, 8.8), 3.5, 0.8, boxstyle="round,pad=0.1", 
                                    facecolor='orange', edgecolor='black', linewidth=2)
        ax.add_patch(quality_rect)
        ax.text(2.75, 9.2, 'QUALITY ALARM\nCheck Membrane Integrity', ha='center', va='center', fontweight='bold')
        
        # Post-treatment
        posttreat_rect = FancyBboxPatch((8.5, 8), 3, 0.8, boxstyle="round,pad=0.1", 
                                      facecolor='lightgreen', edgecolor='black', linewidth=2)
        ax.add_patch(posttreat_rect)
        ax.text(10, 8.4, 'Start Post-treatment\npH & Chlorine Dosing', ha='center', va='center', fontweight='bold')
        
        # Check treated water tank
        self.draw_diamond(ax, 10, 6.8, 3, 1, 'Treated Tank\nLevel < 90%?', 'lightcyan')
        
        # Tank full condition
        tank_full_rect = FancyBboxPatch((15, 6.3), 3.5, 0.8, boxstyle="round,pad=0.1", 
                                      facecolor='red', edgecolor='black', linewidth=2)
        ax.add_patch(tank_full_rect)
        ax.text(16.75, 6.7, 'TANK FULL\nStop RO Production', ha='center', va='center', 
                fontweight='bold', color='white')
        
        # Distribution control
        dist_rect = FancyBboxPatch((8.5, 5.5), 3, 0.8, boxstyle="round,pad=0.1", 
                                 facecolor='lightgreen', edgecolor='black', linewidth=2)
        ax.add_patch(dist_rect)
        ax.text(10, 5.9, 'Control Distribution\nPump Sequencing', ha='center', va='center', fontweight='bold')
        
        # Check roof tank levels
        self.draw_diamond(ax, 10, 4.3, 3, 1, 'Roof Tanks\nNeed Filling?', 'lightcyan')
        
        # Pump selection logic
        pump_select_rect = FancyBboxPatch((8.5, 3), 3, 0.8, boxstyle="round,pad=0.1", 
                                        facecolor='lightblue', edgecolor='black', linewidth=2)
        ax.add_patch(pump_select_rect)
        ax.text(10, 3.4, 'Select Distribution Pump\nBased on Zone Demand', ha='center', va='center', fontweight='bold')
        
        # Monitor operation
        monitor_rect = FancyBboxPatch((8.5, 1.5), 3, 0.8, boxstyle="round,pad=0.1", 
                                    facecolor='lightgreen', edgecolor='black', linewidth=2)
        ax.add_patch(monitor_rect)
        ax.text(10, 1.9, 'Monitor Operation\nLog Data & Alarms', ha='center', va='center', fontweight='bold')
        
        # Draw flowchart connections
        self.draw_flowchart_connections(ax)
        
        # Add decision labels
        self.add_decision_labels(ax)
        
        plt.tight_layout()
        return fig
    
    def draw_diamond(self, ax, x, y, width, height, text, color):
        """Draw a diamond shape for decision points"""
        diamond = patches.Polygon([(x, y + height/2), (x + width/2, y), 
                                 (x, y - height/2), (x - width/2, y)], 
                                facecolor=color, edgecolor='black', linewidth=2)
        ax.add_patch(diamond)
        ax.text(x, y, text, ha='center', va='center', fontweight='bold', fontsize=10)
    
    def draw_flowchart_connections(self, ax):
        """Draw all flowchart connection lines and arrows"""
        # Main flow connections
        connections = [
            [(10, 22.1), (10, 21.8)],  # Start to Init
            [(10, 20.6), (10, 20.3)],  # Init to Emergency check
            [(10, 19.3), (10, 19)],    # Emergency to Tank check
            [(10, 18), (10, 17.8)],    # Tank to Intake
            [(10, 16.6), (10, 16.3)],  # Intake to Pre-treatment check
            [(10, 15.3), (10, 15.3)],  # Pre-treatment check to start
            [(10, 14.1), (10, 13.8)],  # Pre-treatment to Pressure check
            [(10, 12.8), (10, 12.8)],  # Pressure check to RO
            [(10, 11.6), (10, 11.3)],  # RO to RO pressure check
            [(10, 10.3), (10, 9.8)],   # RO pressure to Quality check
            [(10, 8.8), (10, 8.8)],    # Quality to Post-treatment
            [(10, 7.6), (10, 7.3)],    # Post-treatment to Tank check
            [(10, 6.3), (10, 6.3)],    # Tank check to Distribution
            [(10, 5.1), (10, 4.8)],    # Distribution to Roof tanks
            [(10, 3.8), (10, 3.8)],    # Roof tanks to Pump selection
            [(10, 2.6), (10, 2.3)]     # Pump selection to Monitor
        ]
        
        for start, end in connections:
            ax.annotate('', xy=end, xytext=start, 
                       arrowprops=dict(arrowstyle='->', lw=2, color='blue'))
        
        # Decision branch connections
        decision_branches = [
            # Emergency stop - YES
            [(11.25, 19.8), (15, 19.7)],
            # Tank level - NO
            [(8.75, 18.5), (4, 18.4)],
            # Pre-treatment - NO
            [(11.5, 15.8), (15, 15.7)],
            # Feed pressure - NO
            [(11.5, 13.3), (15, 13.2)],
            # RO pressure - NO
            [(11.5, 10.8), (15, 10.7)],
            # Quality - NO
            [(8.5, 9.3), (4.5, 9.2)],
            # Tank full - YES
            [(11.5, 6.8), (15, 6.7)]
        ]
        
        for start, end in decision_branches:
            ax.annotate('', xy=end, xytext=start, 
                       arrowprops=dict(arrowstyle='->', lw=2, color='red'))
    
    def add_decision_labels(self, ax):
        """Add YES/NO labels to decision branches"""
        # YES/NO labels for decisions
        labels = [
            (11.5, 20.1, 'YES', 'red'),
            (10.3, 19.5, 'NO', 'green'),
            (8.5, 18.8, 'NO', 'red'),
            (10.3, 18.2, 'YES', 'green'),
            (11.8, 16.1, 'NO', 'red'),
            (10.3, 15.5, 'YES', 'green'),
            (11.8, 13.6, 'NO', 'red'),
            (10.3, 13, 'YES', 'green'),
            (11.8, 11.1, 'NO', 'red'),
            (10.3, 10.5, 'YES', 'green'),
            (8.2, 9.6, 'NO', 'red'),
            (10.3, 9, 'YES', 'green'),
            (11.8, 7.1, 'YES', 'red'),
            (10.3, 6.5, 'NO', 'green'),
            (10.3, 4, 'YES', 'green')
        ]
        
        for x, y, text, color in labels:
            ax.text(x, y, text, fontsize=9, fontweight='bold', 
                   color=color, ha='center', va='center',
                   bbox=dict(boxstyle="round,pad=0.2", facecolor='white', edgecolor=color))
    
    def create_system_states_diagram(self):
        """Create system states and transitions diagram"""
        fig, ax = plt.subplots(1, 1, figsize=(16, 12))
        ax.set_xlim(0, 16)
        ax.set_ylim(0, 12)
        ax.set_aspect('equal')
        ax.axis('off')
        
        # Title
        ax.text(8, 11.5, 'Water Treatment System - State Diagram', 
                fontsize=18, fontweight='bold', ha='center')
        
        # Define states
        states = [
            (2, 9, 'IDLE', 'lightgray'),
            (6, 9, 'STARTUP', 'lightblue'),
            (10, 9, 'RUNNING', 'lightgreen'),
            (14, 9, 'SHUTDOWN', 'orange'),
            (2, 6, 'MAINTENANCE', 'yellow'),
            (6, 6, 'ALARM', 'red'),
            (10, 6, 'CLEANING', 'lightcyan'),
            (14, 6, 'EMERGENCY', 'darkred'),
            (8, 3, 'STANDBY', 'lightpink')
        ]
        
        # Draw states
        for x, y, label, color in states:
            state_circle = Circle((x, y), 1, facecolor=color, edgecolor='black', linewidth=2)
            ax.add_patch(state_circle)
            text_color = 'white' if color in ['red', 'darkred'] else 'black'
            ax.text(x, y, label, ha='center', va='center', fontweight='bold', color=text_color)
        
        # Define transitions
        transitions = [
            # From IDLE
            [(2, 9), (6, 9), 'Start Command'],
            [(2, 9), (2, 6), 'Maintenance Mode'],
            
            # From STARTUP
            [(6, 9), (10, 9), 'All Systems OK'],
            [(6, 9), (6, 6), 'Startup Failure'],
            [(6, 9), (14, 6), 'Emergency Stop'],
            
            # From RUNNING
            [(10, 9), (14, 9), 'Stop Command'],
            [(10, 9), (6, 6), 'Process Alarm'],
            [(10, 9), (10, 6), 'Cleaning Cycle'],
            [(10, 9), (14, 6), 'Emergency Stop'],
            [(10, 9), (8, 3), 'Low Demand'],
            
            # From SHUTDOWN
            [(14, 9), (2, 9), 'Shutdown Complete'],
            
            # From MAINTENANCE
            [(2, 6), (2, 9), 'Maintenance Complete'],
            
            # From ALARM
            [(6, 6), (10, 9), 'Alarm Reset'],
            [(6, 6), (14, 9), 'Manual Shutdown'],
            [(6, 6), (14, 6), 'Critical Alarm'],
            
            # From CLEANING
            [(10, 6), (10, 9), 'Cleaning Complete'],
            
            # From EMERGENCY
            [(14, 6), (2, 9), 'Emergency Reset'],
            
            # From STANDBY
            [(8, 3), (10, 9), 'Demand Increase']
        ]
        
        # Draw transitions
        for start, end, label in transitions:
            # Calculate arrow position
            dx = end[0] - start[0]
            dy = end[1] - start[1]
            length = np.sqrt(dx**2 + dy**2)
            
            # Normalize and offset from circle edge
            offset = 1.1
            start_x = start[0] + (dx/length) * offset
            start_y = start[1] + (dy/length) * offset
            end_x = end[0] - (dx/length) * offset
            end_y = end[1] - (dy/length) * offset
            
            ax.annotate('', xy=(end_x, end_y), xytext=(start_x, start_y),
                       arrowprops=dict(arrowstyle='->', lw=1.5, color='blue'))
            
            # Add transition label
            mid_x = (start_x + end_x) / 2
            mid_y = (start_y + end_y) / 2
            ax.text(mid_x, mid_y, label, fontsize=8, ha='center', va='bottom',
                   bbox=dict(boxstyle="round,pad=0.2", facecolor='white', alpha=0.8))
        
        plt.tight_layout()
        return fig

    def generate_all_diagrams(self, output_dir=""):
        """Generate all diagrams and save as PNG and PDF"""
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Create main process diagram
        print("Generating main process flow diagram...")
        fig1 = self.create_main_process_diagram()
        
        # Save as PNG
        png_path1 = os.path.join(output_dir, "water_treatment_process_diagram.png")
        fig1.savefig(png_path1, dpi=300, bbox_inches='tight', 
                    facecolor='white', edgecolor='none')
        print(f"Saved: {png_path1}")
        
        # Create P&ID
        print("Generating P&ID diagram...")
        fig2 = self.create_piping_instrumentation_diagram()
        
        # Save as PNG
        png_path2 = os.path.join(output_dir, "water_treatment_pid.png")
        fig2.savefig(png_path2, dpi=300, bbox_inches='tight', 
                    facecolor='white', edgecolor='none')
        print(f"Saved: {png_path2}")
        
        # Create control system diagram
        print("Generating control system diagram...")
        fig3 = self.create_control_system_diagram()
        
        # Save as PNG
        png_path3 = os.path.join(output_dir, "control_system_architecture.png")
        fig3.savefig(png_path3, dpi=300, bbox_inches='tight', 
                    facecolor='white', edgecolor='none')
        print(f"Saved: {png_path3}")
        
        # Create process control flowchart
        print("Generating process control flowchart...")
        fig4 = self.create_process_flowchart()
        
        # Save as PNG
        png_path4 = os.path.join(output_dir, "process_control_flowchart.png")
        fig4.savefig(png_path4, dpi=300, bbox_inches='tight', 
                    facecolor='white', edgecolor='none')
        print(f"Saved: {png_path4}")
        
        # Create system states diagram
        print("Generating system states diagram...")
        fig5 = self.create_system_states_diagram()
        
        # Save as PNG
        png_path5 = os.path.join(output_dir, "system_states_diagram.png")
        fig5.savefig(png_path5, dpi=300, bbox_inches='tight', 
                    facecolor='white', edgecolor='none')
        print(f"Saved: {png_path5}")
        
        # Create combined PDF
        print("Creating combined PDF...")
        pdf_path = os.path.join(output_dir, "water_treatment_diagrams.pdf")
        with PdfPages(pdf_path) as pdf:
            pdf.savefig(fig1, bbox_inches='tight', facecolor='white')
            pdf.savefig(fig2, bbox_inches='tight', facecolor='white')
            pdf.savefig(fig3, bbox_inches='tight', facecolor='white')
            pdf.savefig(fig4, bbox_inches='tight', facecolor='white')
            pdf.savefig(fig5, bbox_inches='tight', facecolor='white')
        print(f"Saved: {pdf_path}")
        
        plt.close('all')
        print("All diagrams generated successfully!")
        
        return [png_path1, png_path2, png_path3, png_path4, png_path5, pdf_path]

def main():
    """Main function to generate all process diagrams"""
    print("Water Treatment System - Process Diagram Generator")
    print("=" * 50)
    
    generator = ProcessDiagramGenerator()
    
    # Get script directory and navigate to project root
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.join(script_dir, "..", "..")
    diagrams_dir = os.path.join(project_root, "diagrams")
    
    # Ensure diagrams directory exists
    if not os.path.exists(diagrams_dir):
        os.makedirs(diagrams_dir)
    
    # Generate diagrams in diagrams folder
    output_files = generator.generate_all_diagrams(diagrams_dir)
    
    print("\nGenerated files:")
    for file_path in output_files:
        # Show relative path from project root
        rel_path = os.path.relpath(file_path, project_root)
        print(f"  • {rel_path}")
    
    print("\nDiagram generation complete!")

if __name__ == "__main__":
    main()
