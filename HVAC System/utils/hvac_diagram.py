#!/usr/bin/env python3
"""
HVAC Control System - Comprehensive Diagram Generator
====================================================

This module generates detailed technical diagrams for the HVAC control system
including system overviews, zone layouts, piping schematics, electrical diagrams,
control flow charts, and energy flow diagrams.

Author: HVAC Control System Team
Version: 2.0
Date: 2024
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Circle, Rectangle, Polygon, Arrow
import numpy as np
import os
import json
from datetime import datetime
from typing import Dict, List, Tuple, Any

class HVACDiagramGenerator:
    """
    Comprehensive HVAC system diagram generator with enhanced capabilities
    """
    
    def __init__(self, output_dir: str = None):
        """Initialize the diagram generator"""
        if output_dir is None:
            # Get the project root directory
            project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            output_dir = os.path.join(project_root, "diagrams")
        
        self.output_dir = output_dir
        self.colors = {
            'supply_air': '#4CAF50',      # Green
            'return_air': '#2196F3',      # Blue  
            'exhaust_air': '#FF9800',     # Orange
            'chilled_water': '#00BCD4',   # Cyan
            'hot_water': '#F44336',       # Red
            'equipment': '#9E9E9E',       # Grey
            'control': '#9C27B0',         # Purple
            'zone': '#FFC107',            # Amber
            'background': '#F8F9FA',      # Light background
            'text': '#212121',            # Dark text
            'border': '#424242',          # Border color
            'highlight': '#E91E63',       # Pink highlight
            'success': '#4CAF50',         # Success green
            'warning': '#FF9800',         # Warning orange
            'danger': '#F44336',          # Danger red
            'info': '#2196F3',           # Info blue
            'sensor': '#795548',          # Brown
            'valve': '#607D8B',           # Blue grey
            'fan': '#00E676',             # Light green
            'heater': '#FF5722',          # Deep orange
            'cooler': '#03A9F4'           # Light blue
        }
        
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        
        # Set matplotlib style
        plt.style.use('default')
        plt.rcParams['font.family'] = 'Arial'
        plt.rcParams['font.size'] = 10
        
        print(f"📁 Diagram output directory: {self.output_dir}")
        
    def generate_all_diagrams(self):
        """Generate all types of diagrams"""
        print("🎨 Generating comprehensive HVAC system diagrams...")
        
        diagrams = [
            ("System Overview", self.generate_system_overview),
            ("Zone Layout", self.generate_zone_layout), 
            ("Piping Schematic", self.generate_piping_schematic),
            ("Electrical Diagram", self.generate_electrical_diagram),
            ("Control Flow", self.generate_control_flow),
            ("Air Flow Diagram", self.generate_air_flow_diagram),
            ("Energy Flow", self.generate_energy_flow_diagram),
            ("Sensor Network", self.generate_sensor_network),
            ("Safety Systems", self.generate_safety_systems),
            ("Maintenance Points", self.generate_maintenance_diagram)
        ]
        
        generated_files = []
        
        for name, func in diagrams:
            try:
                print(f"  📊 Generating {name}...")
                filename = func()
                if filename:
                    generated_files.append(filename)
                    print(f"     ✅ {filename}")
            except Exception as e:
                print(f"     ❌ Error generating {name}: {e}")
        
        # Generate index file
        self.generate_diagram_index(generated_files)
        
        print(f"\n✅ Generated {len(generated_files)} diagrams successfully!")
        return generated_files
        
        print("✅ All diagrams generated successfully!")
        
    def generate_system_overview(self):
        """Generate overall system overview diagram."""
        fig, ax = plt.subplots(1, 1, figsize=(16, 12))
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 80)
        ax.set_aspect('equal')
        
        # Title
        ax.text(50, 75, 'HVAC System Overview', fontsize=20, fontweight='bold', 
                ha='center', va='center', color=self.colors['text'])
        
        # Outside air intake
        outside_air = FancyBboxPatch((5, 60), 15, 8, boxstyle="round,pad=0.5",
                                   facecolor=self.colors['supply_air'], 
                                   edgecolor='black', linewidth=2)
        ax.add_patch(outside_air)
        ax.text(12.5, 64, 'Outside\nAir Intake', ha='center', va='center', 
                fontweight='bold', fontsize=10)
        
        # Air Handling Units
        ahu1 = FancyBboxPatch((30, 55), 20, 18, boxstyle="round,pad=1",
                            facecolor=self.colors['equipment'], 
                            edgecolor='black', linewidth=2)
        ax.add_patch(ahu1)
        ax.text(40, 64, 'AHU-1', ha='center', va='center', 
                fontweight='bold', fontsize=12)
        ax.text(40, 60, 'Supply Fan\nCooling Coil\nHeating Coil\nFilters', 
                ha='center', va='center', fontsize=9)
        
        ahu2 = FancyBboxPatch((55, 55), 20, 18, boxstyle="round,pad=1",
                            facecolor=self.colors['equipment'], 
                            edgecolor='black', linewidth=2)
        ax.add_patch(ahu2)
        ax.text(65, 64, 'AHU-2', ha='center', va='center', 
                fontweight='bold', fontsize=12)
        ax.text(65, 60, 'Supply Fan\nCooling Coil\nHeating Coil\nFilters', 
                ha='center', va='center', fontsize=9)
        
        # Chiller
        chiller = FancyBboxPatch((10, 35), 18, 12, boxstyle="round,pad=1",
                               facecolor=self.colors['chilled_water'], 
                               edgecolor='black', linewidth=2)
        ax.add_patch(chiller)
        ax.text(19, 41, 'Chiller\n250 TR', ha='center', va='center', 
                fontweight='bold', fontsize=11)
        
        # Cooling Tower
        cooling_tower = FancyBboxPatch((10, 20), 18, 12, boxstyle="round,pad=1",
                                     facecolor=self.colors['exhaust_air'], 
                                     edgecolor='black', linewidth=2)
        ax.add_patch(cooling_tower)
        ax.text(19, 26, 'Cooling\nTower', ha='center', va='center', 
                fontweight='bold', fontsize=11)
        
        # Boiler
        boiler = FancyBboxPatch((35, 35), 18, 12, boxstyle="round,pad=1",
                              facecolor=self.colors['hot_water'], 
                              edgecolor='black', linewidth=2)
        ax.add_patch(boiler)
        ax.text(44, 41, 'Boiler\n150 kW', ha='center', va='center', 
                fontweight='bold', fontsize=11)
        
        # Zones
        zone_positions = [(70, 35), (85, 35), (70, 20), (85, 20), 
                         (70, 5), (85, 5), (55, 5), (40, 5)]
        zone_names = ['Zone 1\nConf A', 'Zone 2\nOffice 1', 'Zone 3\nReception', 
                     'Zone 4\nServer', 'Zone 5\nConf B', 'Zone 6\nOffice 2', 
                     'Zone 7\nBreak', 'Zone 8\nStorage']
        
        for i, (x, y) in enumerate(zone_positions):
            zone = FancyBboxPatch((x, y), 12, 8, boxstyle="round,pad=0.5",
                                facecolor=self.colors['zone'], 
                                edgecolor='black', linewidth=1)
            ax.add_patch(zone)
            ax.text(x+6, y+4, zone_names[i], ha='center', va='center', 
                    fontweight='bold', fontsize=8)
        
        # Control System
        control = FancyBboxPatch((60, 40), 15, 10, boxstyle="round,pad=1",
                               facecolor=self.colors['control'], 
                               edgecolor='black', linewidth=2)
        ax.add_patch(control)
        ax.text(67.5, 45, 'PLC\nControl\nSystem', ha='center', va='center', 
                fontweight='bold', fontsize=10, color='white')
        
        # Draw connections (simplified)
        # Supply air ducts
        self._draw_arrow(ax, 20, 64, 30, 64, self.colors['supply_air'], 3)
        self._draw_arrow(ax, 50, 64, 55, 64, self.colors['supply_air'], 3)
        
        # Chilled water pipes
        self._draw_arrow(ax, 28, 41, 30, 61, self.colors['chilled_water'], 2)
        self._draw_arrow(ax, 28, 41, 55, 61, self.colors['chilled_water'], 2)
        
        # Hot water pipes
        self._draw_arrow(ax, 53, 41, 50, 61, self.colors['hot_water'], 2)
        self._draw_arrow(ax, 53, 41, 75, 61, self.colors['hot_water'], 2)
        
        # Control connections
        for x, y in zone_positions:
            self._draw_dashed_line(ax, 67.5, 45, x+6, y+4, self.colors['control'], 1)
        
        # Legend
        legend_elements = [
            patches.Patch(color=self.colors['supply_air'], label='Supply Air'),
            patches.Patch(color=self.colors['chilled_water'], label='Chilled Water'),
            patches.Patch(color=self.colors['hot_water'], label='Hot Water'),
            patches.Patch(color=self.colors['control'], label='Control Signals'),
            patches.Patch(color=self.colors['equipment'], label='Equipment'),
            patches.Patch(color=self.colors['zone'], label='Zones')
        ]
        ax.legend(handles=legend_elements, loc='upper left', bbox_to_anchor=(0, 0.95))
        
        # Remove axes
        ax.set_xticks([])
        ax.set_yticks([])
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)
        
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, 'hvac_system_overview.png'), 
                   dpi=300, bbox_inches='tight')
        plt.close()
        print("  ✅ System overview diagram generated")
        
    def generate_zone_layout(self):
        """Generate zone layout diagram."""
        fig, ax = plt.subplots(1, 1, figsize=(14, 10))
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 70)
        ax.set_aspect('equal')
        
        # Title
        ax.text(50, 65, 'Building Zone Layout', fontsize=18, fontweight='bold', 
                ha='center', va='center', color=self.colors['text'])
        
        # Building outline
        building = Rectangle((10, 10), 80, 50, linewidth=3, edgecolor='black', 
                           facecolor=self.colors['background'])
        ax.add_patch(building)
        
        # Define zones with their positions and sizes
        zones = [
            {'name': 'Conference Room A', 'pos': (15, 35), 'size': (15, 20), 'temp': '22.5°C'},
            {'name': 'Office Area 1', 'pos': (35, 35), 'size': (20, 20), 'temp': '21.8°C'},
            {'name': 'Reception', 'pos': (60, 35), 'size': (15, 20), 'temp': '23.2°C'},
            {'name': 'Server Room', 'pos': (80, 35), 'size': (8, 20), 'temp': '18.5°C'},
            {'name': 'Conference Room B', 'pos': (15, 15), 'size': (15, 15), 'temp': '22.1°C'},
            {'name': 'Office Area 2', 'pos': (35, 15), 'size': (20, 15), 'temp': '21.5°C'},
            {'name': 'Break Room', 'pos': (60, 15), 'size': (15, 15), 'temp': '23.8°C'},
            {'name': 'Storage', 'pos': (80, 15), 'size': (8, 15), 'temp': '20.2°C'}
        ]
        
        # Draw zones
        for i, zone in enumerate(zones):
            x, y = zone['pos']
            w, h = zone['size']
            
            # Zone rectangle
            zone_rect = Rectangle((x, y), w, h, linewidth=2, edgecolor='black', 
                                facecolor=self.colors['zone'], alpha=0.7)
            ax.add_patch(zone_rect)
            
            # Zone label
            ax.text(x + w/2, y + h - 3, f"Zone {i+1}", ha='center', va='center', 
                    fontweight='bold', fontsize=10)
            ax.text(x + w/2, y + h/2, zone['name'], ha='center', va='center', 
                    fontsize=9, wrap=True)
            ax.text(x + w/2, y + 2, zone['temp'], ha='center', va='center', 
                    fontweight='bold', fontsize=9, color='red')
            
            # Temperature sensor
            sensor = Circle((x + w - 2, y + h - 2), 1, facecolor='blue', edgecolor='black')
            ax.add_patch(sensor)
            ax.text(x + w - 2, y + h - 2, 'T', ha='center', va='center', 
                    fontsize=8, color='white', fontweight='bold')
            
            # Damper
            damper_x = x + w/2
            damper_y = y + h + 1
            damper = Rectangle((damper_x - 1, damper_y - 0.5), 2, 1, 
                             facecolor='gray', edgecolor='black')
            ax.add_patch(damper)
            
            # Air flow arrows
            self._draw_arrow(ax, damper_x, damper_y + 1, damper_x, damper_y + 3, 
                           self.colors['supply_air'], 2)
        
        # Air handling unit locations
        ahu1_pos = (20, 5)
        ahu1 = Rectangle(ahu1_pos, 12, 6, facecolor=self.colors['equipment'], 
                        edgecolor='black', linewidth=2)
        ax.add_patch(ahu1)
        ax.text(ahu1_pos[0] + 6, ahu1_pos[1] + 3, 'AHU-1', ha='center', va='center', 
                fontweight='bold', fontsize=10)
        
        ahu2_pos = (65, 5)
        ahu2 = Rectangle(ahu2_pos, 12, 6, facecolor=self.colors['equipment'], 
                        edgecolor='black', linewidth=2)
        ax.add_patch(ahu2)
        ax.text(ahu2_pos[0] + 6, ahu2_pos[1] + 3, 'AHU-2', ha='center', va='center', 
                fontweight='bold', fontsize=10)
        
        # Main supply ducts
        self._draw_thick_line(ax, 26, 11, 26, 32, self.colors['supply_air'], 4)
        self._draw_thick_line(ax, 71, 11, 71, 32, self.colors['supply_air'], 4)
        
        # Branch ducts
        self._draw_thick_line(ax, 26, 32, 85, 32, self.colors['supply_air'], 4)
        
        # Return air system
        self._draw_thick_line(ax, 15, 62, 85, 62, self.colors['return_air'], 3)
        
        # Legend
        legend_elements = [
            patches.Patch(color=self.colors['zone'], label='Zones', alpha=0.7),
            patches.Patch(color=self.colors['supply_air'], label='Supply Air Ducts'),
            patches.Patch(color=self.colors['return_air'], label='Return Air Ducts'),
            patches.Patch(color=self.colors['equipment'], label='Air Handling Units'),
            patches.Circle((0, 0), 0.1, facecolor='blue', label='Temperature Sensors')
        ]
        ax.legend(handles=legend_elements, loc='upper right', bbox_to_anchor=(0.98, 0.98))
        
        # Add North arrow
        ax.annotate('N', xy=(95, 60), xytext=(95, 55), 
                   arrowprops=dict(arrowstyle='->', lw=2), 
                   fontsize=14, fontweight='bold', ha='center')
        
        # Remove axes
        ax.set_xticks([])
        ax.set_yticks([])
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)
        
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, 'zone_layout.png'), 
                   dpi=300, bbox_inches='tight')
        plt.close()
        print("  ✅ Zone layout diagram generated")
        
    def generate_piping_schematic(self):
        """Generate piping and hydronic system schematic."""
        fig, ax = plt.subplots(1, 1, figsize=(14, 10))
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 70)
        ax.set_aspect('equal')
        
        # Title
        ax.text(50, 65, 'Hydronic System Piping Schematic', fontsize=18, fontweight='bold', 
                ha='center', va='center', color=self.colors['text'])
        
        # Chiller
        chiller = FancyBboxPatch((10, 45), 20, 15, boxstyle="round,pad=1",
                               facecolor=self.colors['chilled_water'], 
                               edgecolor='black', linewidth=2)
        ax.add_patch(chiller)
        ax.text(20, 52.5, 'CHILLER\n250 TR\n5°C/12°C', ha='center', va='center', 
                fontweight='bold', fontsize=10)
        
        # Cooling Tower
        cooling_tower = FancyBboxPatch((10, 25), 20, 15, boxstyle="round,pad=1",
                                     facecolor=self.colors['exhaust_air'], 
                                     edgecolor='black', linewidth=2)
        ax.add_patch(cooling_tower)
        ax.text(20, 32.5, 'COOLING\nTOWER\n25°C/30°C', ha='center', va='center', 
                fontweight='bold', fontsize=10)
        
        # Boiler
        boiler = FancyBboxPatch((10, 5), 20, 15, boxstyle="round,pad=1",
                              facecolor=self.colors['hot_water'], 
                              edgecolor='black', linewidth=2)
        ax.add_patch(boiler)
        ax.text(20, 12.5, 'BOILER\n150 kW\n80°C/60°C', ha='center', va='center', 
                fontweight='bold', fontsize=10, color='white')
        
        # Primary chilled water pumps
        chw_pump1 = Circle((40, 55), 3, facecolor='lightblue', edgecolor='black', linewidth=2)
        ax.add_patch(chw_pump1)
        ax.text(40, 55, 'P1', ha='center', va='center', fontweight='bold', fontsize=10)
        
        chw_pump2 = Circle((40, 45), 3, facecolor='lightblue', edgecolor='black', linewidth=2)
        ax.add_patch(chw_pump2)
        ax.text(40, 45, 'P2', ha='center', va='center', fontweight='bold', fontsize=10)
        
        # Hot water pumps
        hw_pump1 = Circle((40, 15), 3, facecolor='lightcoral', edgecolor='black', linewidth=2)
        ax.add_patch(hw_pump1)
        ax.text(40, 15, 'P3', ha='center', va='center', fontweight='bold', fontsize=10)
        
        hw_pump2 = Circle((40, 8), 3, facecolor='lightcoral', edgecolor='black', linewidth=2)
        ax.add_patch(hw_pump2)
        ax.text(40, 8, 'P4', ha='center', va='center', fontweight='bold', fontsize=10)
        
        # Condenser water pumps
        cw_pump1 = Circle((40, 35), 3, facecolor='orange', edgecolor='black', linewidth=2)
        ax.add_patch(cw_pump1)
        ax.text(40, 35, 'P5', ha='center', va='center', fontweight='bold', fontsize=10)
        
        # Air Handling Units
        ahu1 = Rectangle((60, 50), 15, 10, facecolor=self.colors['equipment'], 
                        edgecolor='black', linewidth=2)
        ax.add_patch(ahu1)
        ax.text(67.5, 55, 'AHU-1\nCC & HC', ha='center', va='center', 
                fontweight='bold', fontsize=10)
        
        ahu2 = Rectangle((60, 35), 15, 10, facecolor=self.colors['equipment'], 
                        edgecolor='black', linewidth=2)
        ax.add_patch(ahu2)
        ax.text(67.5, 40, 'AHU-2\nCC & HC', ha='center', va='center', 
                fontweight='bold', fontsize=10)
        
        # Fan Coil Units
        fcu_positions = [(80, 20), (85, 20), (90, 20)]
        for i, (x, y) in enumerate(fcu_positions):
            fcu = Rectangle((x, y), 4, 6, facecolor='lightgray', 
                           edgecolor='black', linewidth=1)
            ax.add_patch(fcu)
            ax.text(x+2, y+3, f'FCU\n{i+1}', ha='center', va='center', 
                    fontsize=8, fontweight='bold')
        
        # Primary chilled water piping
        # Supply
        self._draw_thick_line(ax, 30, 55, 43, 55, self.colors['chilled_water'], 4)
        self._draw_thick_line(ax, 43, 55, 60, 55, self.colors['chilled_water'], 4)
        self._draw_thick_line(ax, 60, 55, 60, 40, self.colors['chilled_water'], 4)
        self._draw_thick_line(ax, 60, 40, 60, 25, self.colors['chilled_water'], 4)
        self._draw_thick_line(ax, 60, 25, 80, 25, self.colors['chilled_water'], 4)
        
        # Return
        self._draw_thick_line(ax, 30, 48, 43, 48, self.colors['chilled_water'], 3)
        self._draw_thick_line(ax, 43, 48, 65, 48, self.colors['chilled_water'], 3)
        self._draw_thick_line(ax, 65, 48, 65, 20, self.colors['chilled_water'], 3)
        self._draw_thick_line(ax, 65, 20, 95, 20, self.colors['chilled_water'], 3)
        
        # Hot water piping
        # Supply
        self._draw_thick_line(ax, 30, 15, 43, 15, self.colors['hot_water'], 4)
        self._draw_thick_line(ax, 43, 15, 70, 15, self.colors['hot_water'], 4)
        self._draw_thick_line(ax, 70, 15, 70, 50, self.colors['hot_water'], 4)
        
        # Return
        self._draw_thick_line(ax, 30, 8, 75, 8, self.colors['hot_water'], 3)
        self._draw_thick_line(ax, 75, 8, 75, 35, self.colors['hot_water'], 3)
        
        # Condenser water piping
        self._draw_thick_line(ax, 30, 35, 43, 35, 'brown', 4)
        self._draw_thick_line(ax, 30, 30, 43, 30, 'brown', 3)
        
        # Valves
        valve_positions = [(50, 55), (50, 48), (50, 15), (50, 8)]
        for x, y in valve_positions:
            valve = Rectangle((x-1, y-1), 2, 2, facecolor='yellow', 
                            edgecolor='black', linewidth=1)
            ax.add_patch(valve)
            ax.text(x, y, 'V', ha='center', va='center', fontweight='bold', fontsize=8)
        
        # Expansion tanks
        exp_tank_chw = Rectangle((45, 60), 6, 4, facecolor='lightblue', 
                               edgecolor='black', linewidth=2)
        ax.add_patch(exp_tank_chw)
        ax.text(48, 62, 'EXP\nTANK', ha='center', va='center', fontweight='bold', fontsize=8)
        
        exp_tank_hw = Rectangle((45, 25), 6, 4, facecolor='lightcoral', 
                              edgecolor='black', linewidth=2)
        ax.add_patch(exp_tank_hw)
        ax.text(48, 27, 'EXP\nTANK', ha='center', va='center', fontweight='bold', fontsize=8)
        
        # Temperature and pressure indicators
        indicators = [
            (35, 55, 'T1\n5°C'), (55, 55, 'T2\n12°C'),
            (35, 15, 'T3\n80°C'), (55, 15, 'T4\n60°C'),
            (35, 35, 'T5\n25°C'), (35, 30, 'T6\n30°C')
        ]
        
        for x, y, label in indicators:
            indicator = Circle((x, y), 1.5, facecolor='white', edgecolor='red', linewidth=2)
            ax.add_patch(indicator)
            ax.text(x, y, label, ha='center', va='center', fontsize=7, fontweight='bold')
        
        # Legend
        legend_elements = [
            patches.Patch(color=self.colors['chilled_water'], label='Chilled Water'),
            patches.Patch(color=self.colors['hot_water'], label='Hot Water'),
            patches.Patch(color='brown', label='Condenser Water'),
            patches.Circle((0, 0), 0.1, facecolor='lightblue', label='CHW Pumps'),
            patches.Circle((0, 0), 0.1, facecolor='lightcoral', label='HW Pumps'),
            patches.Patch(color='yellow', label='Control Valves'),
            patches.Circle((0, 0), 0.1, facecolor='white', edgecolor='red', label='Temp Sensors')
        ]
        ax.legend(handles=legend_elements, loc='upper right', bbox_to_anchor=(0.98, 0.98))
        
        # Remove axes
        ax.set_xticks([])
        ax.set_yticks([])
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)
        
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, 'piping_schematic.png'), 
                   dpi=300, bbox_inches='tight')
        plt.close()
        print("  ✅ Piping schematic generated")
        
    def generate_electrical_diagram(self):
        """Generate electrical single-line diagram."""
        fig, ax = plt.subplots(1, 1, figsize=(12, 14))
        ax.set_xlim(0, 80)
        ax.set_ylim(0, 100)
        ax.set_aspect('equal')
        
        # Title
        ax.text(40, 95, 'Electrical Single Line Diagram', fontsize=16, fontweight='bold', 
                ha='center', va='center', color=self.colors['text'])
        
        # Main electrical service
        main_service = Rectangle((35, 85), 10, 8, facecolor='red', 
                               edgecolor='black', linewidth=3)
        ax.add_patch(main_service)
        ax.text(40, 89, 'MAIN\n480V\n3Φ', ha='center', va='center', 
                fontweight='bold', fontsize=10, color='white')
        
        # Main distribution panel
        main_panel = Rectangle((30, 70), 20, 10, facecolor='gray', 
                             edgecolor='black', linewidth=2)
        ax.add_patch(main_panel)
        ax.text(40, 75, 'MAIN DISTRIBUTION\nPANEL (MDP)', ha='center', va='center', 
                fontweight='bold', fontsize=10)
        
        # HVAC panel
        hvac_panel = Rectangle((30, 55), 20, 10, facecolor='lightblue', 
                             edgecolor='black', linewidth=2)
        ax.add_patch(hvac_panel)
        ax.text(40, 60, 'HVAC PANEL\n(HP-1)', ha='center', va='center', 
                fontweight='bold', fontsize=10)
        
        # Motor control centers
        mcc1 = Rectangle((10, 40), 15, 10, facecolor='lightgreen', 
                        edgecolor='black', linewidth=2)
        ax.add_patch(mcc1)
        ax.text(17.5, 45, 'MCC-1\nChillers &\nPumps', ha='center', va='center', 
                fontweight='bold', fontsize=9)
        
        mcc2 = Rectangle((55, 40), 15, 10, facecolor='lightgreen', 
                        edgecolor='black', linewidth=2)
        ax.add_patch(mcc2)
        ax.text(62.5, 45, 'MCC-2\nAHUs &\nFans', ha='center', va='center', 
                fontweight='bold', fontsize=9)
        
        # Individual equipment
        equipment_list = [
            ('Chiller-1\n100A', 5, 25),
            ('Chiller-2\n100A', 20, 25),
            ('CHW Pump-1\n30A', 5, 15),
            ('CHW Pump-2\n30A', 20, 15),
            ('CW Pump\n25A', 5, 5),
            ('AHU-1\n50A', 55, 25),
            ('AHU-2\n50A', 70, 25),
            ('Boiler\n40A', 35, 25),
            ('Control Panel\n15A', 40, 40)
        ]
        
        for name, x, y in equipment_list:
            equip = Rectangle((x, y), 10, 8, facecolor='lightyellow', 
                            edgecolor='black', linewidth=1)
            ax.add_patch(equip)
            ax.text(x+5, y+4, name, ha='center', va='center', 
                    fontweight='bold', fontsize=8)
        
        # Electrical connections
        # Main service to MDP
        self._draw_thick_line(ax, 40, 85, 40, 80, 'black', 3)
        
        # MDP to HVAC Panel
        self._draw_thick_line(ax, 40, 70, 40, 65, 'black', 2)
        
        # HVAC Panel to MCCs
        self._draw_thick_line(ax, 30, 60, 17.5, 60, 'black', 2)
        self._draw_thick_line(ax, 17.5, 60, 17.5, 50, 'black', 2)
        
        self._draw_thick_line(ax, 50, 60, 62.5, 60, 'black', 2)
        self._draw_thick_line(ax, 62.5, 60, 62.5, 50, 'black', 2)
        
        # Direct connections from HVAC Panel
        self._draw_thick_line(ax, 40, 55, 40, 50, 'black', 2)
        self._draw_thick_line(ax, 40, 50, 45, 50, 'black', 2)
        self._draw_thick_line(ax, 45, 50, 45, 48, 'black', 2)
        
        # MCC to equipment connections
        mcc1_equipment = [(10, 29), (25, 29), (10, 19), (25, 19), (10, 9)]
        for x, y in mcc1_equipment:
            self._draw_thick_line(ax, 17.5, 40, 17.5, y+4, 'black', 1)
            self._draw_thick_line(ax, 17.5, y+4, x, y+4, 'black', 1)
        
        mcc2_equipment = [(60, 29), (75, 29)]
        for x, y in mcc2_equipment:
            self._draw_thick_line(ax, 62.5, 40, 62.5, y+4, 'black', 1)
            self._draw_thick_line(ax, 62.5, y+4, x, y+4, 'black', 1)
        
        # Circuit breakers
        breaker_positions = [(37, 82), (37, 67), (37, 62), (15, 52), (60, 52)]
        for x, y in breaker_positions:
            breaker = Rectangle((x, y), 6, 3, facecolor='black', edgecolor='black')
            ax.add_patch(breaker)
            ax.text(x+3, y+1.5, 'CB', ha='center', va='center', 
                    color='white', fontweight='bold', fontsize=7)
        
        # Ground symbols
        ground_positions = [(40, 67), (17.5, 37), (62.5, 37), (45, 37)]
        for x, y in ground_positions:
            # Draw ground symbol
            ground_lines = [
                [(x-2, y), (x+2, y)],
                [(x-1.5, y-1), (x+1.5, y-1)],
                [(x-1, y-2), (x+1, y-2)]
            ]
            for line in ground_lines:
                ax.plot([line[0][0], line[1][0]], [line[0][1], line[1][1]], 
                       'k-', linewidth=2)
        
        # Power ratings
        ax.text(5, 95, 'Electrical Specifications:', fontweight='bold', fontsize=12)
        ax.text(5, 92, '• Main Service: 480V, 3-Phase, 600A', fontsize=10)
        ax.text(5, 89, '• HVAC Load: 350kW', fontsize=10)
        ax.text(5, 86, '• Total Connected Load: 485kW', fontsize=10)
        ax.text(5, 83, '• Demand Factor: 0.8', fontsize=10)
        ax.text(5, 80, '• Power Factor: 0.9', fontsize=10)
        
        # Legend
        legend_elements = [
            patches.Patch(color='red', label='Main Service'),
            patches.Patch(color='gray', label='Distribution Panel'),
            patches.Patch(color='lightblue', label='HVAC Panel'),
            patches.Patch(color='lightgreen', label='Motor Control Center'),
            patches.Patch(color='lightyellow', label='Equipment'),
            patches.Patch(color='black', label='Circuit Breaker')
        ]
        ax.legend(handles=legend_elements, loc='upper right', bbox_to_anchor=(0.98, 0.98))
        
        # Remove axes
        ax.set_xticks([])
        ax.set_yticks([])
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)
        
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, 'electrical_diagram.png'), 
                   dpi=300, bbox_inches='tight')
        plt.close()
        print("  ✅ Electrical diagram generated")
        
    def generate_control_flow(self):
        """Generate control system flow diagram."""
        fig, ax = plt.subplots(1, 1, figsize=(14, 10))
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 70)
        ax.set_aspect('equal')
        
        # Title
        ax.text(50, 65, 'Control System Architecture', fontsize=18, fontweight='bold', 
                ha='center', va='center', color=self.colors['text'])
        
        # Main PLC
        plc = FancyBboxPatch((40, 45), 20, 15, boxstyle="round,pad=1",
                           facecolor=self.colors['control'], 
                           edgecolor='black', linewidth=2)
        ax.add_patch(plc)
        ax.text(50, 52.5, 'MAIN PLC\nCPU 1215C\nEthernet I/O', ha='center', va='center', 
                fontweight='bold', fontsize=11, color='white')
        
        # HMI
        hmi = FancyBboxPatch((70, 50), 15, 10, boxstyle="round,pad=0.5",
                           facecolor='lightblue', 
                           edgecolor='black', linewidth=2)
        ax.add_patch(hmi)
        ax.text(77.5, 55, 'HMI\nOperator\nInterface', ha='center', va='center', 
                fontweight='bold', fontsize=10)
        
        # Engineering Station
        eng_station = FancyBboxPatch((15, 50), 15, 10, boxstyle="round,pad=0.5",
                                   facecolor='lightgreen', 
                                   edgecolor='black', linewidth=2)
        ax.add_patch(eng_station)
        ax.text(22.5, 55, 'Engineering\nStation\nTIA Portal', ha='center', va='center', 
                fontweight='bold', fontsize=10)
        
        # I/O Modules
        io_modules = [
            ('AI Module\n8 Channels', 15, 30),
            ('AO Module\n4 Channels', 35, 30),
            ('DI Module\n16 Channels', 55, 30),
            ('DO Module\n16 Channels', 75, 30)
        ]
        
        for name, x, y in io_modules:
            module = Rectangle((x, y), 12, 8, facecolor='orange', 
                             edgecolor='black', linewidth=2)
            ax.add_patch(module)
            ax.text(x+6, y+4, name, ha='center', va='center', 
                    fontweight='bold', fontsize=9)
        
        # Field devices
        field_devices = [
            ('Temperature\nSensors', 10, 15, 'lightcoral'),
            ('Humidity\nSensors', 25, 15, 'lightcoral'),
            ('Pressure\nSensors', 40, 15, 'lightcoral'),
            ('CO2\nSensors', 55, 15, 'lightcoral'),
            ('Control\nValves', 10, 5, 'lightyellow'),
            ('VFDs', 25, 5, 'lightyellow'),
            ('Pumps', 40, 5, 'lightyellow'),
            ('Dampers', 55, 5, 'lightyellow'),
            ('Alarms', 70, 15, 'lightpink'),
            ('Status\nLights', 85, 15, 'lightpink')
        ]
        
        for name, x, y, color in field_devices:
            device = Rectangle((x, y), 10, 8, facecolor=color, 
                             edgecolor='black', linewidth=1)
            ax.add_patch(device)
            ax.text(x+5, y+4, name, ha='center', va='center', 
                    fontweight='bold', fontsize=8)
        
        # Communication networks
        # Ethernet network
        ethernet_points = [(30, 52.5), (40, 52.5), (60, 52.5), (70, 55)]
        for i in range(len(ethernet_points)-1):
            x1, y1 = ethernet_points[i]
            x2, y2 = ethernet_points[i+1]
            self._draw_thick_line(ax, x1, y1, x2, y2, 'blue', 3)
        
        # Profibus network to I/O
        profibus_points = [(50, 45), (50, 40), (21, 40), (21, 38)]
        for i in range(len(profibus_points)-1):
            x1, y1 = profibus_points[i]
            x2, y2 = profibus_points[i+1]
            self._draw_thick_line(ax, x1, y1, x2, y2, 'green', 2)
            
        profibus_points2 = [(50, 40), (80, 40), (80, 38)]
        for i in range(len(profibus_points2)-1):
            x1, y1 = profibus_points2[i]
            x2, y2 = profibus_points2[i+1]
            self._draw_thick_line(ax, x1, y1, x2, y2, 'green', 2)
        
        # 4-20mA connections
        analog_connections = [
            ((21, 30), (15, 23)),  # AI to temp sensors
            ((21, 30), (30, 23)),  # AI to humidity sensors
            ((21, 30), (45, 23)),  # AI to pressure sensors
            ((21, 30), (60, 23)),  # AI to CO2 sensors
            ((41, 30), (15, 13)),  # AO to valves
            ((41, 30), (30, 13)),  # AO to VFDs
        ]
        
        for (x1, y1), (x2, y2) in analog_connections:
            self._draw_dashed_line(ax, x1, y1, x2, y2, 'red', 1)
        
        # Digital connections
        digital_connections = [
            ((61, 30), (75, 23)),  # DI to alarms
            ((61, 30), (90, 23)),  # DI to status
            ((81, 30), (45, 13)),  # DO to pumps
            ((81, 30), (60, 13)),  # DO to dampers
        ]
        
        for (x1, y1), (x2, y2) in digital_connections:
            self._draw_dashed_line(ax, x1, y1, x2, y2, 'purple', 1)
        
        # Network labels
        ax.text(50, 57, 'Ethernet TCP/IP', ha='center', va='center', 
                fontweight='bold', fontsize=9, color='blue',
                bbox=dict(boxstyle="round,pad=0.3", facecolor='white', edgecolor='blue'))
        
        ax.text(35, 42, 'Profibus DP', ha='center', va='center', 
                fontweight='bold', fontsize=9, color='green',
                bbox=dict(boxstyle="round,pad=0.3", facecolor='white', edgecolor='green'))
        
        # Legend
        legend_elements = [
            patches.Patch(color=self.colors['control'], label='Main Controller'),
            patches.Patch(color='lightblue', label='HMI Interface'),
            patches.Patch(color='orange', label='I/O Modules'),
            patches.Patch(color='lightcoral', label='Input Devices'),
            patches.Patch(color='lightyellow', label='Output Devices'),
            patches.Patch(color='blue', label='Ethernet Network'),
            patches.Patch(color='green', label='Profibus Network'),
            patches.Patch(color='red', label='Analog 4-20mA'),
            patches.Patch(color='purple', label='Digital I/O')
        ]
        ax.legend(handles=legend_elements, loc='upper left', bbox_to_anchor=(0, 0.95),
                 ncol=2, fontsize=9)
        
        # Network specifications
        ax.text(5, 5, 'Network Specifications:', fontweight='bold', fontsize=11)
        ax.text(5, 3, '• Ethernet: 100 Mbps, TCP/IP Protocol', fontsize=9)
        ax.text(5, 1, '• Profibus: 12 Mbps, DP Protocol', fontsize=9)
        
        # Remove axes
        ax.set_xticks([])
        ax.set_yticks([])
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)
        
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, 'control_flow.png'), 
                   dpi=300, bbox_inches='tight')
        plt.close()
        print("  ✅ Control flow diagram generated")
        
    def _draw_arrow(self, ax, x1, y1, x2, y2, color, width):
        """Draw an arrow between two points."""
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                   arrowprops=dict(arrowstyle='->', lw=width, color=color))
        
    def _draw_thick_line(self, ax, x1, y1, x2, y2, color, width):
        """Draw a thick line between two points."""
        ax.plot([x1, x2], [y1, y2], color=color, linewidth=width, solid_capstyle='round')
        
    def _draw_dashed_line(self, ax, x1, y1, x2, y2, color, width):
        """Draw a dashed line between two points."""
        ax.plot([x1, x2], [y1, y2], color=color, linewidth=width, 
               linestyle='--', solid_capstyle='round')

def main():
    """Main function to generate all diagrams."""
    print("🎨 HVAC System Diagram Generator")
    print("=" * 40)
    
    try:
        generator = HVACDiagramGenerator()
        generator.generate_all_diagrams()
        
        print("\n📊 All diagrams have been generated in the 'diagrams' folder:")
        print("  • hvac_system_overview.png - Complete system overview")
        print("  • zone_layout.png - Building zone layout with sensors")
        print("  • piping_schematic.png - Hydronic system piping")
        print("  • electrical_diagram.png - Electrical single-line diagram")
        print("  • control_flow.png - Control system architecture")
        
    except Exception as e:
        print(f"❌ Error generating diagrams: {e}")
        return 1
        
    return 0

if __name__ == "__main__":
    exit(main())
