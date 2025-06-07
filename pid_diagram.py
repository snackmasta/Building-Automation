#!/usr/bin/env python3
"""
P&ID (Piping and Instrumentation Diagram) Generator
===================================================
This script generates a P&ID diagram for the industrial process control system.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Circle, Rectangle, Polygon
import numpy as np

class PIDDiagram:
    def __init__(self):
        self.fig, self.ax = plt.subplots(1, 1, figsize=(16, 12))
        self.ax.set_xlim(0, 100)
        self.ax.set_ylim(0, 80)
        self.ax.set_aspect('equal')
        self.ax.grid(True, alpha=0.3)
        
    def draw_tank(self, x, y, width, height, label):
        """Draw a process tank"""
        # Tank body
        tank = Rectangle((x, y), width, height, 
                        linewidth=3, edgecolor='black', facecolor='lightblue', alpha=0.7)
        self.ax.add_patch(tank)
        
        # Tank label
        self.ax.text(x + width/2, y + height/2, label, 
                    ha='center', va='center', fontsize=12, fontweight='bold')
        
        # Liquid level indicator
        liquid_height = height * 0.7  # 70% filled
        liquid = Rectangle((x+1, y+1), width-2, liquid_height-1, 
                          facecolor='blue', alpha=0.5)
        self.ax.add_patch(liquid)
        
        return x + width/2, y + height  # Return top center point
    
    def draw_pump(self, x, y, label):
        """Draw a centrifugal pump"""
        # Pump body (circle)
        pump = Circle((x, y), 3, linewidth=2, edgecolor='black', facecolor='yellow')
        self.ax.add_patch(pump)
        
        # Pump impeller
        self.ax.plot([x-2, x+2], [y, y], 'k-', linewidth=2)
        self.ax.plot([x, x], [y-2, y+2], 'k-', linewidth=2)
        
        # Label
        self.ax.text(x, y-5, label, ha='center', va='top', fontsize=10, fontweight='bold')
        
        return x, y
    
    def draw_valve(self, x, y, valve_type='gate', label='', angle=0):
        """Draw different types of valves"""
        if valve_type == 'gate':
            # Gate valve symbol
            valve_body = Rectangle((x-2, y-1), 4, 2, 
                                 linewidth=2, edgecolor='black', facecolor='white')
            self.ax.add_patch(valve_body)
            
            # Valve stem
            self.ax.plot([x, x], [y+1, y+4], 'k-', linewidth=2)
            self.ax.plot([x-1, x+1], [y+4, y+4], 'k-', linewidth=3)
            
        elif valve_type == 'control':
            # Control valve symbol
            triangle = Polygon([(x-2, y-1), (x+2, y-1), (x, y+1)], 
                             linewidth=2, edgecolor='black', facecolor='lightgreen')
            self.ax.add_patch(triangle)
            
            # Actuator
            actuator = Rectangle((x-1.5, y+1), 3, 2, 
                               linewidth=2, edgecolor='black', facecolor='orange')
            self.ax.add_patch(actuator)
        
        # Label
        if label:
            self.ax.text(x, y-3, label, ha='center', va='top', fontsize=9, fontweight='bold')
        
        return x, y
    
    def draw_pipe(self, start_x, start_y, end_x, end_y, pipe_type='process'):
        """Draw piping"""
        if pipe_type == 'process':
            self.ax.plot([start_x, end_x], [start_y, end_y], 'k-', linewidth=3)
        elif pipe_type == 'signal':
            self.ax.plot([start_x, end_x], [start_y, end_y], 'r--', linewidth=1.5)
        elif pipe_type == 'power':
            self.ax.plot([start_x, end_x], [start_y, end_y], 'g-', linewidth=2)
    
    def draw_instrument(self, x, y, tag, description, instrument_type='indicator'):
        """Draw process instruments"""
        if instrument_type == 'indicator':
            # Circle for indicator
            circle = Circle((x, y), 2, linewidth=2, edgecolor='red', facecolor='white')
            self.ax.add_patch(circle)
        elif instrument_type == 'transmitter':
            # Square for transmitter
            square = Rectangle((x-2, y-2), 4, 4, 
                             linewidth=2, edgecolor='blue', facecolor='lightcyan')
            self.ax.add_patch(square)
        elif instrument_type == 'controller':
            # Diamond for controller
            diamond = Polygon([(x, y+2), (x+2, y), (x, y-2), (x-2, y)], 
                            linewidth=2, edgecolor='green', facecolor='lightgreen')
            self.ax.add_patch(diamond)
        
        # Tag number
        self.ax.text(x, y, tag, ha='center', va='center', fontsize=8, fontweight='bold')
        
        # Description below
        self.ax.text(x, y-4, description, ha='center', va='top', fontsize=7)
        
        return x, y
    
    def draw_heater(self, x, y, width, height, label):
        """Draw heating element"""
        # Heater body
        heater = Rectangle((x, y), width, height, 
                          linewidth=2, edgecolor='red', facecolor='lightyellow')
        self.ax.add_patch(heater)
        
        # Heating elements (zigzag)
        for i in range(3):
            x_start = x + 2 + i * (width-4)/2
            y_line = y + height/2
            self.ax.plot([x_start, x_start + 2, x_start + 4], 
                        [y_line - 1, y_line + 1, y_line - 1], 'r-', linewidth=2)
        
        # Label
        self.ax.text(x + width/2, y + height + 2, label, 
                    ha='center', va='bottom', fontsize=10, fontweight='bold')
        
        return x + width/2, y + height/2
    
    def create_pid(self):
        """Create the complete P&ID diagram"""
        # Title
        self.ax.text(50, 75, 'P&ID - Industrial Process Control System', 
                    ha='center', va='center', fontsize=16, fontweight='bold')
        
        # Draw main process tank
        tank_x, tank_top = self.draw_tank(20, 30, 20, 25, 'PROCESS\nTANK\nT-001')
        
        # Draw heater in tank
        heater_x, heater_y = self.draw_heater(22, 32, 16, 8, 'HEATER\nE-001')
        
        # Draw pump
        pump_x, pump_y = self.draw_pump(50, 20, 'PUMP\nP-001')
        
        # Draw valves
        valve1_x, valve1_y = self.draw_valve(15, 42, 'control', 'PV-001')  # Inlet valve
        valve2_x, valve2_y = self.draw_valve(45, 42, 'control', 'PV-002')  # Outlet valve
        
        # Draw instruments
        # Temperature
        self.draw_instrument(25, 50, 'TT-001', 'Temp Transmitter', 'transmitter')
        self.draw_instrument(25, 60, 'TIC-001', 'Temp Controller', 'controller')
        
        # Pressure
        self.draw_instrument(35, 50, 'PT-001', 'Press Transmitter', 'transmitter')
        self.draw_instrument(35, 60, 'PI-001', 'Press Indicator', 'indicator')
        
        # Level
        self.draw_instrument(30, 35, 'LS-001', 'Level Switch', 'indicator')
        
        # Flow
        self.draw_instrument(55, 25, 'FT-001', 'Flow Transmitter', 'transmitter')
        
        # Draw piping
        # Inlet line
        self.draw_pipe(5, 42, 13, 42)  # Feed line to valve
        self.draw_pipe(17, 42, 20, 42)  # Valve to tank
        
        # Outlet line from tank
        self.draw_pipe(40, 42, 43, 42)  # Tank to valve
        self.draw_pipe(47, 42, 60, 42)  # Valve to pump suction
        self.draw_pipe(60, 42, 60, 25)  # Down to pump level
        self.draw_pipe(60, 25, 53, 25)  # To pump suction
        
        # Pump discharge
        self.draw_pipe(47, 20, 75, 20)  # Pump discharge
        self.draw_pipe(75, 20, 75, 5)   # Down to outlet
        
        # Draw signal lines (dashed red)
        # Temperature signals
        self.draw_pipe(25, 48, 25, 45, 'signal')  # TT to process
        self.draw_pipe(25, 52, 25, 58, 'signal')  # TT to controller
        
        # Pressure signals
        self.draw_pipe(35, 48, 35, 45, 'signal')  # PT to process
        self.draw_pipe(35, 52, 35, 58, 'signal')  # PT to indicator
        
        # Level signal
        self.draw_pipe(30, 37, 30, 40, 'signal')  # LS to process
        
        # Control signals to valves
        self.draw_pipe(25, 58, 15, 48, 'signal')  # TIC to PV-001
        self.draw_pipe(25, 58, 45, 48, 'signal')  # TIC to PV-002
        
        # Power lines (green)
        self.draw_pipe(22, 40, 22, 35, 'power')   # Power to heater
        self.draw_pipe(50, 17, 50, 10, 'power')   # Power to pump
        
        # Add legend
        legend_x, legend_y = 75, 65
        self.ax.text(legend_x, legend_y, 'LEGEND:', fontsize=12, fontweight='bold')
        self.ax.plot([legend_x, legend_x+5], [legend_y-3, legend_y-3], 'k-', linewidth=3)
        self.ax.text(legend_x+6, legend_y-3, 'Process Line', fontsize=10)
        self.ax.plot([legend_x, legend_x+5], [legend_y-6, legend_y-6], 'r--', linewidth=1.5)
        self.ax.text(legend_x+6, legend_y-6, 'Signal Line', fontsize=10)
        self.ax.plot([legend_x, legend_x+5], [legend_y-9, legend_y-9], 'g-', linewidth=2)
        self.ax.text(legend_x+6, legend_y-9, 'Power Line', fontsize=10)
        
        # Add process data
        data_x, data_y = 5, 65
        self.ax.text(data_x, data_y, 'PROCESS DATA:', fontsize=12, fontweight='bold')
        self.ax.text(data_x, data_y-3, '• Operating Temperature: 75°C', fontsize=10)
        self.ax.text(data_x, data_y-6, '• Operating Pressure: 3.0 bar', fontsize=10)
        self.ax.text(data_x, data_y-9, '• Tank Capacity: 1000L', fontsize=10)
        self.ax.text(data_x, data_y-12, '• Pump Flow: 100 L/min', fontsize=10)
        
        # Add I/O list
        io_x, io_y = 5, 20
        self.ax.text(io_x, io_y, 'I/O SUMMARY:', fontsize=12, fontweight='bold')
        self.ax.text(io_x, io_y-3, 'Digital Inputs: 8', fontsize=10)
        self.ax.text(io_x, io_y-6, 'Digital Outputs: 8', fontsize=10)
        self.ax.text(io_x, io_y-9, 'Analog Inputs: 4', fontsize=10)
        self.ax.text(io_x, io_y-12, 'Analog Outputs: 2', fontsize=10)
        
        # Remove axes
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        
        # Add border
        border = Rectangle((1, 1), 98, 78, linewidth=3, edgecolor='black', facecolor='none')
        self.ax.add_patch(border)
        
        plt.tight_layout()
        return self.fig

def main():
    """Generate and save the P&ID diagram"""
    pid = PIDDiagram()
    fig = pid.create_pid()
    
    # Save the diagram
    plt.savefig('c:/Users/Legion/Desktop/PLC/pid_diagram.png', dpi=300, bbox_inches='tight')
    plt.savefig('c:/Users/Legion/Desktop/PLC/pid_diagram.pdf', bbox_inches='tight')
    
    print("P&ID diagram saved as:")
    print("- pid_diagram.png (high resolution)")
    print("- pid_diagram.pdf (vector format)")
    
    plt.show()

if __name__ == "__main__":
    main()
