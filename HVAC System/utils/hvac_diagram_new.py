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

try:
    import matplotlib.pyplot as plt
    import matplotlib.patches as patches
    from matplotlib.patches import FancyBboxPatch, Circle, Rectangle, Polygon, Arrow
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False
    print("⚠️  Warning: matplotlib not available. Install with: pip install matplotlib")

try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False
    print("⚠️  Warning: numpy not available. Install with: pip install numpy")

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
        if not MATPLOTLIB_AVAILABLE:
            raise ImportError("matplotlib is required for diagram generation")
            
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
        if not MATPLOTLIB_AVAILABLE:
            print("❌ Cannot generate diagrams: matplotlib not available")
            return []
            
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
    
    def generate_system_overview(self) -> str:
        """Generate system overview diagram"""
        try:
            fig, ax = plt.subplots(1, 1, figsize=(16, 12))
            fig.patch.set_facecolor(self.colors['background'])
            
            # Title
            ax.text(0.5, 0.95, 'HVAC CONTROL SYSTEM - OVERVIEW', 
                   horizontalalignment='center', fontsize=20, fontweight='bold',
                   transform=ax.transAxes)
            
            # AHU (Air Handling Unit)
            ahu = FancyBboxPatch((0.1, 0.7), 0.25, 0.15, 
                               boxstyle="round,pad=0.01",
                               facecolor=self.colors['equipment'],
                               edgecolor=self.colors['border'], linewidth=2)
            ax.add_patch(ahu)
            ax.text(0.225, 0.775, 'AIR HANDLING UNIT\n(AHU)', 
                   ha='center', va='center', fontweight='bold', fontsize=12)
            
            # Chiller
            chiller = FancyBboxPatch((0.65, 0.7), 0.25, 0.15,
                                   boxstyle="round,pad=0.01", 
                                   facecolor=self.colors['cooler'],
                                   edgecolor=self.colors['border'], linewidth=2)
            ax.add_patch(chiller)
            ax.text(0.775, 0.775, 'CHILLER\nSYSTEM', 
                   ha='center', va='center', fontweight='bold', fontsize=12)
            
            # Boiler
            boiler = FancyBboxPatch((0.65, 0.5), 0.25, 0.15,
                                  boxstyle="round,pad=0.01",
                                  facecolor=self.colors['heater'], 
                                  edgecolor=self.colors['border'], linewidth=2)
            ax.add_patch(boiler)
            ax.text(0.775, 0.575, 'BOILER\nSYSTEM', 
                   ha='center', va='center', fontweight='bold', fontsize=12)
            
            # Control System
            plc = FancyBboxPatch((0.375, 0.45), 0.25, 0.1,
                               boxstyle="round,pad=0.01",
                               facecolor=self.colors['control'],
                               edgecolor=self.colors['border'], linewidth=2)
            ax.add_patch(plc)
            ax.text(0.5, 0.5, 'PLC CONTROL SYSTEM', 
                   ha='center', va='center', fontweight='bold', 
                   fontsize=12, color='white')
            
            # Zones
            zone_positions = [
                (0.1, 0.25), (0.3, 0.25), (0.5, 0.25), (0.7, 0.25),
                (0.1, 0.05), (0.3, 0.05), (0.5, 0.05), (0.7, 0.05)
            ]
            zone_names = ['Office', 'Conference', 'Production', 'Storage',
                         'Lobby', 'Kitchen', 'Server Room', 'Warehouse']
            
            for i, (pos, name) in enumerate(zip(zone_positions, zone_names)):
                zone = FancyBboxPatch(pos, 0.15, 0.12,
                                    boxstyle="round,pad=0.01",
                                    facecolor=self.colors['zone'],
                                    edgecolor=self.colors['border'], linewidth=1)
                ax.add_patch(zone)
                ax.text(pos[0] + 0.075, pos[1] + 0.06, f'ZONE {i+1}\n{name}',
                       ha='center', va='center', fontsize=10, fontweight='bold')
            
            # Add connection lines
            # AHU to zones
            for pos in zone_positions:
                ax.plot([0.35, pos[0] + 0.075], [0.7, pos[1] + 0.12], 
                       color=self.colors['supply_air'], linewidth=2, alpha=0.7)
            
            # PLC to equipment
            ax.plot([0.375, 0.225], [0.5, 0.7], 
                   color=self.colors['control'], linewidth=3, alpha=0.8)
            ax.plot([0.625, 0.775], [0.5, 0.7], 
                   color=self.colors['control'], linewidth=3, alpha=0.8)
            ax.plot([0.625, 0.775], [0.5, 0.65], 
                   color=self.colors['control'], linewidth=3, alpha=0.8)
            
            # Legend
            legend_elements = [
                plt.Line2D([0], [0], color=self.colors['supply_air'], lw=3, label='Supply Air'),
                plt.Line2D([0], [0], color=self.colors['control'], lw=3, label='Control Signals'),
                plt.Rectangle((0, 0), 1, 1, facecolor=self.colors['equipment'], label='Equipment'),
                plt.Rectangle((0, 0), 1, 1, facecolor=self.colors['zone'], label='Zones')
            ]
            ax.legend(handles=legend_elements, loc='upper right', bbox_to_anchor=(1, 0.4))
            
            # Add timestamp
            ax.text(0.02, 0.02, f'Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}',
                   transform=ax.transAxes, fontsize=8, alpha=0.7)
            
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1) 
            ax.set_aspect('equal')
            ax.axis('off')
            
            filename = os.path.join(self.output_dir, 'system_overview.png')
            plt.savefig(filename, dpi=300, bbox_inches='tight', 
                       facecolor=self.colors['background'])
            plt.close()
            
            return filename
            
        except Exception as e:
            print(f"Error generating system overview: {e}")
            plt.close()
            return None
    
    def generate_zone_layout(self) -> str:
        """Generate zone layout diagram"""
        try:
            fig, ax = plt.subplots(1, 1, figsize=(14, 10))
            fig.patch.set_facecolor(self.colors['background'])
            
            # Title
            ax.text(0.5, 0.95, 'HVAC SYSTEM - ZONE LAYOUT', 
                   horizontalalignment='center', fontsize=18, fontweight='bold',
                   transform=ax.transAxes)
            
            # Building outline
            building = Rectangle((0.1, 0.15), 0.8, 0.7, 
                               facecolor='none', edgecolor=self.colors['border'], 
                               linewidth=3)
            ax.add_patch(building)
            
            # Zone definitions with detailed layout
            zones = [
                {'name': 'Zone 1 - Office', 'pos': (0.15, 0.65), 'size': (0.35, 0.15), 'temp': '22°C'},
                {'name': 'Zone 2 - Conference', 'pos': (0.55, 0.65), 'size': (0.3, 0.15), 'temp': '22°C'},
                {'name': 'Zone 3 - Production', 'pos': (0.15, 0.45), 'size': (0.4, 0.15), 'temp': '23°C'},
                {'name': 'Zone 4 - Storage', 'pos': (0.6, 0.45), 'size': (0.25, 0.15), 'temp': '20°C'},
                {'name': 'Zone 5 - Lobby', 'pos': (0.15, 0.25), 'size': (0.2, 0.15), 'temp': '22°C'},
                {'name': 'Zone 6 - Kitchen', 'pos': (0.4, 0.25), 'size': (0.2, 0.15), 'temp': '24°C'},
                {'name': 'Zone 7 - Server Room', 'pos': (0.65, 0.25), 'size': (0.2, 0.15), 'temp': '18°C'},
                {'name': 'Zone 8 - Warehouse', 'pos': (0.25, 0.15), 'size': (0.5, 0.08), 'temp': '20°C'}
            ]
            
            # Draw zones
            for i, zone in enumerate(zones):
                # Zone rectangle
                zone_rect = FancyBboxPatch(zone['pos'], zone['size'][0], zone['size'][1],
                                         boxstyle="round,pad=0.005",
                                         facecolor=self.colors['zone'],
                                         edgecolor=self.colors['border'],
                                         linewidth=1.5, alpha=0.8)
                ax.add_patch(zone_rect)
                
                # Zone label
                center_x = zone['pos'][0] + zone['size'][0] / 2
                center_y = zone['pos'][1] + zone['size'][1] / 2
                ax.text(center_x, center_y + 0.02, zone['name'],
                       ha='center', va='center', fontweight='bold', fontsize=10)
                ax.text(center_x, center_y - 0.02, f"Target: {zone['temp']}",
                       ha='center', va='center', fontsize=9, style='italic')
                
                # Add sensors
                sensor_x = zone['pos'][0] + zone['size'][0] - 0.02
                sensor_y = zone['pos'][1] + zone['size'][1] - 0.02
                sensor = Circle((sensor_x, sensor_y), 0.01, 
                              facecolor=self.colors['sensor'], 
                              edgecolor=self.colors['border'])
                ax.add_patch(sensor)
                ax.text(sensor_x + 0.015, sensor_y, f'T{i+1}', 
                       fontsize=8, ha='left', va='center')
                
                # Add air supply/return
                supply_x = zone['pos'][0] + 0.02
                supply_y = zone['pos'][1] + zone['size'][1] - 0.02
                supply = Rectangle((supply_x, supply_y), 0.03, 0.01,
                                 facecolor=self.colors['supply_air'])
                ax.add_patch(supply)
                
                return_x = zone['pos'][0] + 0.02
                return_y = zone['pos'][1] + 0.01
                return_vent = Rectangle((return_x, return_y), 0.03, 0.01,
                                      facecolor=self.colors['return_air'])
                ax.add_patch(return_vent)
            
            # Add HVAC equipment locations
            # AHU location
            ahu_pos = (0.05, 0.87)
            ahu = FancyBboxPatch(ahu_pos, 0.15, 0.08,
                               boxstyle="round,pad=0.005",
                               facecolor=self.colors['equipment'],
                               edgecolor=self.colors['border'], linewidth=2)
            ax.add_patch(ahu)
            ax.text(ahu_pos[0] + 0.075, ahu_pos[1] + 0.04, 'AHU',
                   ha='center', va='center', fontweight='bold', fontsize=12)
            
            # Main ducts
            # Supply duct
            supply_duct = Rectangle((0.2, 0.85), 0.6, 0.02,
                                  facecolor=self.colors['supply_air'], alpha=0.7)
            ax.add_patch(supply_duct)
            
            # Return duct  
            return_duct = Rectangle((0.2, 0.12), 0.6, 0.02,
                                  facecolor=self.colors['return_air'], alpha=0.7)
            ax.add_patch(return_duct)
            
            # Branch connections
            branch_points = [0.25, 0.35, 0.45, 0.55, 0.65, 0.75]
            for point in branch_points:
                # Supply branches
                ax.plot([point, point], [0.85, 0.8], 
                       color=self.colors['supply_air'], linewidth=3)
                # Return branches
                ax.plot([point, point], [0.2, 0.14], 
                       color=self.colors['return_air'], linewidth=3)
            
            # Legend
            legend_elements = [
                plt.Rectangle((0, 0), 1, 1, facecolor=self.colors['zone'], label='Climate Zones'),
                plt.Rectangle((0, 0), 1, 1, facecolor=self.colors['supply_air'], label='Supply Air'),
                plt.Rectangle((0, 0), 1, 1, facecolor=self.colors['return_air'], label='Return Air'),
                plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=self.colors['sensor'], 
                          markersize=8, label='Temperature Sensors'),
                plt.Rectangle((0, 0), 1, 1, facecolor=self.colors['equipment'], label='HVAC Equipment')
            ]
            ax.legend(handles=legend_elements, loc='lower left', bbox_to_anchor=(0, 0))
            
            # Add scale
            ax.text(0.02, 0.88, 'Scale: 1 unit = 10 meters', 
                   transform=ax.transAxes, fontsize=10, 
                   bbox=dict(boxstyle="round,pad=0.3", facecolor='white', alpha=0.8))
            
            # Add timestamp
            ax.text(0.98, 0.02, f'Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}',
                   transform=ax.transAxes, fontsize=8, alpha=0.7, ha='right')
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
            ax.set_aspect('equal')
            ax.axis('off')
            
            filename = os.path.join(self.output_dir, 'zone_layout.png')
            plt.savefig(filename, dpi=300, bbox_inches='tight',
                       facecolor=self.colors['background'])
            plt.close()
            return filename
            
        except Exception as e:
            print(f"Error generating zone layout: {e}")
            plt.close()
            return None
    
    def generate_piping_schematic(self) -> str:
        """Generate piping schematic"""
        try:
            fig, ax = plt.subplots(1, 1, figsize=(14, 10))
            fig.patch.set_facecolor(self.colors['background'])
            
            ax.text(0.5, 0.95, 'PIPING & HYDRONIC SCHEMATIC', 
                   horizontalalignment='center', fontsize=18, fontweight='bold',
                   transform=ax.transAxes)
            
            # Chiller system
            chiller = FancyBboxPatch((0.05, 0.7), 0.2, 0.15,
                                   boxstyle="round,pad=0.01",
                                   facecolor=self.colors['cooler'],
                                   edgecolor=self.colors['border'], linewidth=2)
            ax.add_patch(chiller)
            ax.text(0.15, 0.775, 'CHILLER\n400 kW', ha='center', va='center', 
                   fontweight='bold', fontsize=11)
            
            # Boiler system
            boiler = FancyBboxPatch((0.05, 0.5), 0.2, 0.15,
                                  boxstyle="round,pad=0.01",
                                  facecolor=self.colors['heater'],
                                  edgecolor=self.colors['border'], linewidth=2)
            ax.add_patch(boiler)
            ax.text(0.15, 0.575, 'BOILER\n300 kW', ha='center', va='center', 
                   fontweight='bold', fontsize=11)
            
            # Primary pumps
            for i, y in enumerate([0.82, 0.62]):
                pump = Circle((0.3, y), 0.03, facecolor=self.colors['equipment'],
                            edgecolor=self.colors['border'], linewidth=2)
                ax.add_patch(pump)
                ax.text(0.3, y, 'P', ha='center', va='center', fontweight='bold', fontsize=10)
                ax.text(0.35, y, f'P{i+1}', ha='left', va='center', fontsize=9)
            
            # Main distribution pipes
            # Chilled water supply
            ax.plot([0.25, 0.9], [0.8, 0.8], color=self.colors['chilled_water'], 
                   linewidth=6, label='Chilled Water Supply')
            # Chilled water return
            ax.plot([0.9, 0.25], [0.75, 0.75], color=self.colors['chilled_water'], 
                   linewidth=4, alpha=0.7)
            
            # Hot water supply
            ax.plot([0.25, 0.9], [0.6, 0.6], color=self.colors['hot_water'], 
                   linewidth=6, label='Hot Water Supply')
            # Hot water return
            ax.plot([0.9, 0.25], [0.55, 0.55], color=self.colors['hot_water'], 
                   linewidth=4, alpha=0.7)
            
            # Zone connections
            zone_x_positions = [0.4, 0.5, 0.6, 0.7, 0.8]
            for i, x in enumerate(zone_x_positions):
                # Chilled water connections
                ax.plot([x, x], [0.8, 0.4], color=self.colors['chilled_water'], linewidth=3)
                ax.plot([x, x], [0.4, 0.75], color=self.colors['chilled_water'], linewidth=2, alpha=0.7)
                
                # Hot water connections
                ax.plot([x, x], [0.6, 0.35], color=self.colors['hot_water'], linewidth=3)
                ax.plot([x, x], [0.35, 0.55], color=self.colors['hot_water'], linewidth=2, alpha=0.7)
                
                # Zone equipment
                zone_box = Rectangle((x-0.03, 0.35), 0.06, 0.05, 
                                   facecolor=self.colors['zone'], 
                                   edgecolor=self.colors['border'])
                ax.add_patch(zone_box)
                ax.text(x, 0.32, f'Z{i+1}', ha='center', va='top', fontsize=9)
                
                # Valves
                valve1 = Circle((x, 0.42), 0.015, facecolor=self.colors['valve'])
                valve2 = Circle((x, 0.37), 0.015, facecolor=self.colors['valve'])
                ax.add_patch(valve1)
                ax.add_patch(valve2)
            
            # Expansion tank
            tank = Rectangle((0.85, 0.85), 0.08, 0.1, facecolor=self.colors['equipment'],
                           edgecolor=self.colors['border'], linewidth=2)
            ax.add_patch(tank)
            ax.text(0.89, 0.9, 'EXP\nTANK', ha='center', va='center', fontsize=9, fontweight='bold')
            
            # Pressure relief
            ax.plot([0.89, 0.89], [0.85, 0.8], color=self.colors['border'], linewidth=2)
            
            # Legend
            legend_elements = [
                plt.Line2D([0], [0], color=self.colors['chilled_water'], lw=4, label='Chilled Water'),
                plt.Line2D([0], [0], color=self.colors['hot_water'], lw=4, label='Hot Water'),
                plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=self.colors['valve'],
                          markersize=8, label='Control Valves'),
                plt.Rectangle((0, 0), 1, 1, facecolor=self.colors['equipment'], label='Equipment')
            ]
            ax.legend(handles=legend_elements, loc='lower left')
            
            # Technical specifications
            specs = """
SYSTEM SPECIFICATIONS:
• Chilled Water: 6°C Supply / 12°C Return
• Hot Water: 80°C Supply / 60°C Return
• Operating Pressure: 150 kPa
• Flow Rate: 200 L/min per zone
            """
            ax.text(0.02, 0.3, specs, transform=ax.transAxes, fontsize=9,
                   bbox=dict(boxstyle="round,pad=0.5", facecolor='white', alpha=0.9))
            
            # Add timestamp
            ax.text(0.98, 0.02, f'Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}',
                   transform=ax.transAxes, fontsize=8, alpha=0.7, ha='right')
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
            ax.set_aspect('equal')
            ax.axis('off')
            
            filename = os.path.join(self.output_dir, 'piping_schematic.png')
            plt.savefig(filename, dpi=300, bbox_inches='tight',
                       facecolor=self.colors['background'])
            plt.close()
            return filename
            
        except Exception as e:
            print(f"Error generating piping schematic: {e}")
            plt.close()
            return None
    
    def generate_electrical_diagram(self) -> str:
        """Generate electrical diagram"""
        try:
            fig, ax = plt.subplots(1, 1, figsize=(12, 14))
            fig.patch.set_facecolor(self.colors['background'])
            
            ax.text(0.5, 0.95, 'ELECTRICAL SINGLE LINE DIAGRAM', 
                   horizontalalignment='center', fontsize=18, fontweight='bold',
                   transform=ax.transAxes)
            
            # Main electrical panel
            main_panel = FancyBboxPatch((0.1, 0.8), 0.8, 0.1,
                                      boxstyle="round,pad=0.01",
                                      facecolor=self.colors['equipment'],
                                      edgecolor=self.colors['border'], linewidth=3)
            ax.add_patch(main_panel)
            ax.text(0.5, 0.85, 'MAIN ELECTRICAL PANEL - 480V/3Φ', 
                   ha='center', va='center', fontweight='bold', fontsize=14)
            
            # Transformers
            transformer_positions = [(0.2, 0.65), (0.8, 0.65)]
            for i, pos in enumerate(transformer_positions):
                transformer = Circle(pos, 0.06, facecolor=self.colors['equipment'],
                                   edgecolor=self.colors['border'], linewidth=2)
                ax.add_patch(transformer)
                ax.text(pos[0], pos[1], f'T{i+1}\n480/120V', ha='center', va='center', 
                       fontsize=10, fontweight='bold')
            
            # Main feeder lines
            ax.plot([0.2, 0.2], [0.8, 0.71], color='black', linewidth=6, label='480V 3Φ')
            ax.plot([0.8, 0.8], [0.8, 0.71], color='black', linewidth=6)
            
            # Equipment connections
            equipment_data = [
                {'name': 'Chiller\n150A', 'pos': (0.15, 0.5), 'load': '150A'},
                {'name': 'Boiler\n100A', 'pos': (0.35, 0.5), 'load': '100A'},
                {'name': 'AHU-1\n75A', 'pos': (0.55, 0.5), 'load': '75A'},
                {'name': 'AHU-2\n75A', 'pos': (0.75, 0.5), 'load': '75A'},
                {'name': 'Pumps\n50A', 'pos': (0.25, 0.35), 'load': '50A'},
                {'name': 'Controls\n20A', 'pos': (0.75, 0.35), 'load': '20A'}
            ]
            
            for equipment in equipment_data:
                # Equipment box
                eq_box = FancyBboxPatch((equipment['pos'][0]-0.06, equipment['pos'][1]-0.04), 
                                      0.12, 0.08, boxstyle="round,pad=0.005",
                                      facecolor=self.colors['zone'],
                                      edgecolor=self.colors['border'], linewidth=1)
                ax.add_patch(eq_box)
                ax.text(equipment['pos'][0], equipment['pos'][1], equipment['name'],
                       ha='center', va='center', fontsize=9, fontweight='bold')
                
                # Connection lines
                if equipment['pos'][0] < 0.5:
                    ax.plot([0.2, equipment['pos'][0]], [0.65, equipment['pos'][1]+0.04],
                           color='red', linewidth=3)
                else:
                    ax.plot([0.8, equipment['pos'][0]], [0.65, equipment['pos'][1]+0.04],
                           color='red', linewidth=3)
                
                # Circuit breakers
                cb_y = equipment['pos'][1] + 0.08
                cb = Rectangle((equipment['pos'][0]-0.01, cb_y), 0.02, 0.02,
                             facecolor='black', edgecolor='black')
                ax.add_patch(cb)
                ax.text(equipment['pos'][0]+0.02, cb_y+0.01, equipment['load'],
                       ha='left', va='center', fontsize=8)
            
            # Control panel connections (120V)
            control_equipment = [
                {'name': 'PLC', 'pos': (0.1, 0.2)},
                {'name': 'HMI', 'pos': (0.3, 0.2)},
                {'name': 'I/O Modules', 'pos': (0.5, 0.2)},
                {'name': 'Sensors', 'pos': (0.7, 0.2)},
                {'name': 'Emergency Stop', 'pos': (0.9, 0.2)}
            ]
            
            for ctrl in control_equipment:
                ctrl_box = Rectangle((ctrl['pos'][0]-0.04, ctrl['pos'][1]-0.03), 
                                   0.08, 0.06, facecolor=self.colors['control'],
                                   edgecolor=self.colors['border'], linewidth=1)
                ax.add_patch(ctrl_box)
                ax.text(ctrl['pos'][0], ctrl['pos'][1], ctrl['name'],
                       ha='center', va='center', fontsize=8, fontweight='bold', color='white')
                
                # 120V connections
                ax.plot([0.8, ctrl['pos'][0]], [0.59, ctrl['pos'][1]+0.03],
                       color='blue', linewidth=2, linestyle='--')
            
            # Ground system
            ground_points = [(0.05, 0.05), (0.95, 0.05)]
            for point in ground_points:
                # Ground symbol
                for i in range(3):
                    width = 0.04 - i * 0.01
                    ground_line = Rectangle((point[0] - width/2, point[1] - i*0.01), 
                                          width, 0.005, facecolor='green', edgecolor='green')
                    ax.add_patch(ground_line)
                ax.text(point[0], point[1]+0.03, 'GRD', ha='center', va='bottom', 
                       fontsize=8, fontweight='bold', color='green')
            
            # Legend
            legend_elements = [
                plt.Line2D([0], [0], color='black', lw=4, label='480V 3Φ'),
                plt.Line2D([0], [0], color='red', lw=3, label='Equipment Feeders'),
                plt.Line2D([0], [0], color='blue', lw=2, linestyle='--', label='120V Control'),
                plt.Line2D([0], [0], color='green', lw=2, label='Grounding'),
                plt.Rectangle((0, 0), 1, 1, facecolor=self.colors['control'], label='Control Equipment')
            ]
            ax.legend(handles=legend_elements, loc='lower left')
            
            # Electrical specifications
            specs = """
ELECTRICAL SPECIFICATIONS:
• Main Supply: 480V, 3Φ, 60Hz
• Total Load: 500A
• Control Voltage: 120V, 1Φ
• Emergency Power: Backup Generator
• Protection: Arc Flash Protection
            """
            ax.text(0.02, 0.45, specs, transform=ax.transAxes, fontsize=9,
                   bbox=dict(boxstyle="round,pad=0.5", facecolor='white', alpha=0.9))
            
            # Add timestamp
            ax.text(0.98, 0.02, f'Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}',
                   transform=ax.transAxes, fontsize=8, alpha=0.7, ha='right')
            
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
            ax.set_aspect('equal')
            ax.axis('off')
            filename = os.path.join(self.output_dir, 'electrical_diagram.png')
            plt.savefig(filename, dpi=300, bbox_inches='tight',
                       facecolor=self.colors['background'])
            plt.close()
            return filename
            
        except Exception as e:
            print(f"Error generating electrical diagram: {e}")
            plt.close()
            return None
    
    def generate_control_flow(self) -> str:
        """Generate control flow diagram"""
        try:
            fig, ax = plt.subplots(1, 1, figsize=(14, 10))
            fig.patch.set_facecolor(self.colors['background'])
            
            ax.text(0.5, 0.95, 'CONTROL SYSTEM ARCHITECTURE', 
                   horizontalalignment='center', fontsize=18, fontweight='bold',
                   transform=ax.transAxes)
            
            # PLC System (Central)
            plc_main = FancyBboxPatch((0.35, 0.65), 0.3, 0.15,
                                    boxstyle="round,pad=0.01",
                                    facecolor=self.colors['control'],
                                    edgecolor=self.colors['border'], linewidth=3)
            ax.add_patch(plc_main)
            ax.text(0.5, 0.725, 'PLC CONTROL SYSTEM\nModbus TCP/IP\nEthernet Network', 
                   ha='center', va='center', fontweight='bold', fontsize=12, color='white')
            
            # HMI Interface
            hmi = FancyBboxPatch((0.05, 0.75), 0.2, 0.1,
                               boxstyle="round,pad=0.01",
                               facecolor=self.colors['info'],
                               edgecolor=self.colors['border'], linewidth=2)
            ax.add_patch(hmi)
            ax.text(0.15, 0.8, 'HMI\nOperator Interface', ha='center', va='center', 
                   fontweight='bold', fontsize=10, color='white')
            
            # SCADA System
            scada = FancyBboxPatch((0.75, 0.75), 0.2, 0.1,
                                 boxstyle="round,pad=0.01",
                                 facecolor=self.colors['info'],
                                 edgecolor=self.colors['border'], linewidth=2)
            ax.add_patch(scada)
            ax.text(0.85, 0.8, 'SCADA\nRemote Monitoring', ha='center', va='center', 
                   fontweight='bold', fontsize=10, color='white')
            
            # Input/Output Modules
            io_modules = [
                {'name': 'Analog Input\n(16 CH)', 'pos': (0.1, 0.5), 'type': 'AI'},
                {'name': 'Analog Output\n(8 CH)', 'pos': (0.3, 0.5), 'type': 'AO'},
                {'name': 'Digital Input\n(32 CH)', 'pos': (0.7, 0.5), 'type': 'DI'},
                {'name': 'Digital Output\n(16 CH)', 'pos': (0.9, 0.5), 'type': 'DO'}
            ]
            
            for module in io_modules:
                io_box = FancyBboxPatch((module['pos'][0]-0.08, module['pos'][1]-0.05), 
                                      0.16, 0.1, boxstyle="round,pad=0.005",
                                      facecolor=self.colors['equipment'],
                                      edgecolor=self.colors['border'], linewidth=1)
                ax.add_patch(io_box)
                ax.text(module['pos'][0], module['pos'][1], module['name'],
                       ha='center', va='center', fontsize=9, fontweight='bold')
                
                # Connection to PLC
                if module['pos'][0] < 0.5:
                    ax.plot([module['pos'][0]+0.08, 0.35], [module['pos'][1], 0.65],
                           color=self.colors['control'], linewidth=2, alpha=0.8)
                else:
                    ax.plot([module['pos'][0]-0.08, 0.65], [module['pos'][1], 0.65],
                           color=self.colors['control'], linewidth=2, alpha=0.8)
            
            # Field Devices
            field_devices = [
                {'name': 'Temperature\nSensors', 'pos': (0.1, 0.3), 'connection': 'AI'},
                {'name': 'Pressure\nSensors', 'pos': (0.25, 0.3), 'connection': 'AI'},
                {'name': 'Flow\nSensors', 'pos': (0.4, 0.3), 'connection': 'AI'},
                {'name': 'Control\nValves', 'pos': (0.55, 0.3), 'connection': 'AO'},
                {'name': 'Motor\nStarters', 'pos': (0.7, 0.3), 'connection': 'DO'},
                {'name': 'Alarm\nIndicators', 'pos': (0.85, 0.3), 'connection': 'DO'}
            ]
            
            for device in field_devices:
                device_circle = Circle(device['pos'], 0.04, facecolor=self.colors['sensor'],
                                     edgecolor=self.colors['border'], linewidth=1)
                ax.add_patch(device_circle)
                ax.text(device['pos'][0], device['pos'][1]-0.08, device['name'],
                       ha='center', va='center', fontsize=8, fontweight='bold')
                
                # Connect to appropriate I/O module
                io_y = 0.5
                if device['connection'] == 'AI':
                    if device['pos'][0] < 0.3:
                        io_x = 0.1
                    else:
                        io_x = 0.25
                elif device['connection'] == 'AO':
                    io_x = 0.3
                elif device['connection'] == 'DI':
                    io_x = 0.7
                else:  # DO
                    io_x = 0.9
                
                ax.plot([device['pos'][0], io_x], [device['pos'][1]+0.04, io_y-0.05],
                       color=self.colors['sensor'], linewidth=1.5, alpha=0.7)
            
            # Network connections
            # HMI to PLC
            ax.plot([0.25, 0.35], [0.8, 0.725], color=self.colors['info'], 
                   linewidth=3, alpha=0.8)
            ax.text(0.3, 0.76, 'Ethernet', ha='center', va='bottom', fontsize=8, 
                   style='italic', color=self.colors['info'])
            
            # SCADA to PLC
            ax.plot([0.75, 0.65], [0.8, 0.725], color=self.colors['info'], 
                   linewidth=3, alpha=0.8)
            ax.text(0.7, 0.76, 'Ethernet', ha='center', va='bottom', fontsize=8, 
                   style='italic', color=self.colors['info'])
            
            # Control Logic Flow
            logic_steps = [
                "1. Sensor Data Acquisition",
                "2. PID Control Processing", 
                "3. Equipment Command Output",
                "4. Status Monitoring",
                "5. Alarm Processing"
            ]
            
            ax.text(0.02, 0.2, "CONTROL LOGIC FLOW:\n" + "\n".join(logic_steps),
                   transform=ax.transAxes, fontsize=10, fontweight='bold',
                   bbox=dict(boxstyle="round,pad=0.5", facecolor=self.colors['background'], 
                           edgecolor=self.colors['border'], alpha=0.9))
            
            # System specifications
            specs = """
COMMUNICATION PROTOCOLS:
• Modbus TCP/IP (Ethernet)
• RS-485 (Serial Devices)  
• BACnet (Building Automation)
• OPC UA (SCADA Integration)

RESPONSE TIMES:
• Critical Control: <50ms
• Normal Control: <200ms
• HMI Updates: <1s
• SCADA Updates: <5s
            """
            ax.text(0.7, 0.2, specs, transform=ax.transAxes, fontsize=9,
                   bbox=dict(boxstyle="round,pad=0.5", facecolor='white', alpha=0.9))
            
            # Add timestamp
            ax.text(0.98, 0.02, f'Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}',
                   transform=ax.transAxes, fontsize=8, alpha=0.7, ha='right')
            
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
            ax.set_aspect('equal')
            ax.axis('off')
            
            filename = os.path.join(self.output_dir, 'control_flow.png')
            plt.savefig(filename, dpi=300, bbox_inches='tight',
                       facecolor=self.colors['background'])
            plt.close()
            return filename
            
        except Exception as e:
            print(f"Error generating control flow: {e}")
            plt.close()
            return None
    
    def generate_air_flow_diagram(self) -> str:
        """Generate air flow diagram"""
        try:
            fig, ax = plt.subplots(1, 1, figsize=(14, 10))
            fig.patch.set_facecolor(self.colors['background'])
            
            ax.text(0.5, 0.95, 'AIR FLOW DIAGRAM', 
                   horizontalalignment='center', fontsize=18, fontweight='bold',
                   transform=ax.transAxes)
            
            # Air Handling Unit (AHU)
            ahu = FancyBboxPatch((0.05, 0.4), 0.3, 0.2,
                               boxstyle="round,pad=0.01",
                               facecolor=self.colors['equipment'],
                               edgecolor=self.colors['border'], linewidth=3)
            ax.add_patch(ahu)
            ax.text(0.2, 0.5, 'AIR HANDLING UNIT\n• Supply Fan: 5000 CFM\n• Return Fan: 4500 CFM\n• Filters: MERV 13',
                   ha='center', va='center', fontweight='bold', fontsize=10)
            
            # Outdoor Air Intake
            outdoor_air = FancyBboxPatch((0.05, 0.7), 0.15, 0.1,
                                       boxstyle="round,pad=0.01",
                                       facecolor=self.colors['supply_air'],
                                       edgecolor=self.colors['border'], linewidth=2)
            ax.add_patch(outdoor_air)
            ax.text(0.125, 0.75, 'OUTDOOR AIR\n1000 CFM', ha='center', va='center', 
                   fontweight='bold', fontsize=9)
            
            # Exhaust Air
            exhaust_air = FancyBboxPatch((0.05, 0.2), 0.15, 0.1,
                                       boxstyle="round,pad=0.01",
                                       facecolor=self.colors['exhaust_air'],
                                       edgecolor=self.colors['border'], linewidth=2)
            ax.add_patch(exhaust_air)
            ax.text(0.125, 0.25, 'EXHAUST AIR\n500 CFM', ha='center', va='center', 
                   fontweight='bold', fontsize=9)
            
            # Main Supply Duct
            supply_duct = FancyBboxPatch((0.35, 0.47), 0.55, 0.06,
                                       boxstyle="round,pad=0.005",
                                       facecolor=self.colors['supply_air'],
                                       edgecolor=self.colors['border'], linewidth=2)
            ax.add_patch(supply_duct)
            ax.text(0.625, 0.5, 'MAIN SUPPLY DUCT - 4500 CFM', ha='center', va='center', 
                   fontweight='bold', fontsize=11)
            
            # Main Return Duct
            return_duct = FancyBboxPatch((0.35, 0.39), 0.55, 0.06,
                                       boxstyle="round,pad=0.005",
                                       facecolor=self.colors['return_air'],
                                       edgecolor=self.colors['border'], linewidth=2)
            ax.add_patch(return_duct)
            ax.text(0.625, 0.42, 'MAIN RETURN DUCT - 4000 CFM', ha='center', va='center', 
                   fontweight='bold', fontsize=11)
            
            # Zone Supply/Return Connections
            zone_positions = [
                {'x': 0.45, 'name': 'Office Zone\n800 CFM', 'supply_cfm': 800, 'return_cfm': 750},
                {'x': 0.55, 'name': 'Conference\n600 CFM', 'supply_cfm': 600, 'return_cfm': 550},
                {'x': 0.65, 'name': 'Production\n1200 CFM', 'supply_cfm': 1200, 'return_cfm': 1100},
                {'x': 0.75, 'name': 'Storage\n400 CFM', 'supply_cfm': 400, 'return_cfm': 350},
                {'x': 0.85, 'name': 'Server Room\n1000 CFM', 'supply_cfm': 1000, 'return_cfm': 900}
            ]
            
            for zone in zone_positions:
                # Zone box
                zone_box = FancyBboxPatch((zone['x']-0.04, 0.7), 0.08, 0.15,
                                        boxstyle="round,pad=0.005",
                                        facecolor=self.colors['zone'],
                                        edgecolor=self.colors['border'], linewidth=1)
                ax.add_patch(zone_box)
                ax.text(zone['x'], 0.775, zone['name'], ha='center', va='center', 
                       fontsize=8, fontweight='bold')
                
                # Supply branch
                ax.plot([zone['x'], zone['x']], [0.53, 0.7], 
                       color=self.colors['supply_air'], linewidth=4)
                # Supply diffuser
                diffuser = Circle((zone['x'], 0.68), 0.015, 
                                facecolor=self.colors['supply_air'],
                                edgecolor=self.colors['border'])
                ax.add_patch(diffuser)
                
                # Return branch
                ax.plot([zone['x'], zone['x']], [0.39, 0.15], 
                       color=self.colors['return_air'], linewidth=3)
                # Return grille  
                grille = Rectangle((zone['x']-0.02, 0.13), 0.04, 0.02,
                                 facecolor=self.colors['return_air'],
                                 edgecolor=self.colors['border'])
                ax.add_patch(grille)
                
                # Flow arrows
                ax.arrow(zone['x'], 0.6, 0, 0.08, head_width=0.01, head_length=0.01,
                        fc=self.colors['supply_air'], ec=self.colors['supply_air'])
                ax.arrow(zone['x'], 0.25, 0, -0.08, head_width=0.01, head_length=0.01,
                        fc=self.colors['return_air'], ec=self.colors['return_air'])
            
            # Dampers and Controls
            damper_positions = [0.42, 0.52, 0.62, 0.72, 0.82]
            for pos in damper_positions:
                # Supply damper
                damper_s = Rectangle((pos-0.01, 0.51), 0.02, 0.02, 
                                   facecolor=self.colors['valve'], 
                                   edgecolor=self.colors['border'])
                ax.add_patch(damper_s)
                ax.text(pos, 0.52, 'D', ha='center', va='center', fontsize=6, fontweight='bold')
                
                # Return damper
                damper_r = Rectangle((pos-0.01, 0.41), 0.02, 0.02,
                                   facecolor=self.colors['valve'],
                                   edgecolor=self.colors['border'])
                ax.add_patch(damper_r)
                ax.text(pos, 0.42, 'D', ha='center', va='center', fontsize=6, fontweight='bold')
            
            # Air flow paths
            # Outdoor air to AHU
            ax.arrow(0.125, 0.7, 0, -0.08, head_width=0.01, head_length=0.01,
                    fc=self.colors['supply_air'], ec=self.colors['supply_air'], linewidth=2)
            
            # Exhaust from AHU
            ax.arrow(0.125, 0.4, 0, -0.08, head_width=0.01, head_length=0.01,
                    fc=self.colors['exhaust_air'], ec=self.colors['exhaust_air'], linewidth=2)
            
            # Supply fan indicator
            fan_supply = Circle((0.3, 0.5), 0.02, facecolor=self.colors['fan'],
                              edgecolor=self.colors['border'], linewidth=2)
            ax.add_patch(fan_supply)
            ax.text(0.3, 0.5, 'SF', ha='center', va='center', fontweight='bold', fontsize=8)
            
            # Return fan indicator  
            fan_return = Circle((0.3, 0.42), 0.02, facecolor=self.colors['fan'],
                              edgecolor=self.colors['border'], linewidth=2)
            ax.add_patch(fan_return)
            ax.text(0.3, 0.42, 'RF', ha='center', va='center', fontweight='bold', fontsize=8)
            
            # Legend
            legend_elements = [
                plt.Line2D([0], [0], color=self.colors['supply_air'], lw=4, label='Supply Air'),
                plt.Line2D([0], [0], color=self.colors['return_air'], lw=4, label='Return Air'),
                plt.Line2D([0], [0], color=self.colors['exhaust_air'], lw=4, label='Exhaust Air'),
                plt.Rectangle((0, 0), 1, 1, facecolor=self.colors['valve'], label='Dampers'),
                plt.Rectangle((0, 0), 1, 1, facecolor=self.colors['fan'], label='Fans')
            ]
            ax.legend(handles=legend_elements, loc='upper right')
            
            # Air balance information
            balance_info = """
AIR BALANCE:
• Total Supply: 4500 CFM
• Total Return: 4000 CFM  
• Outdoor Air: 1000 CFM
• Exhaust Air: 500 CFM
• Building Pressurization: +0.02" WC
            """
            ax.text(0.02, 0.15, balance_info, transform=ax.transAxes, fontsize=9,
                   bbox=dict(boxstyle="round,pad=0.5", facecolor='white', alpha=0.9))
            
            # Add timestamp
            ax.text(0.98, 0.02, f'Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}',
                   transform=ax.transAxes, fontsize=8, alpha=0.7, ha='right')
            
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
            ax.set_aspect('equal')
            ax.axis('off')
            
            filename = os.path.join(self.output_dir, 'air_flow_diagram.png')
            plt.savefig(filename, dpi=300, bbox_inches='tight',
                       facecolor=self.colors['background'])
            plt.close()
            return filename
            
        except Exception as e:
            print(f"Error generating air flow diagram: {e}")
            plt.close()
            return None
    
    def generate_energy_flow_diagram(self) -> str:
        """Generate energy flow diagram"""
        try:
            fig, ax = plt.subplots(1, 1, figsize=(14, 10))
            fig.patch.set_facecolor(self.colors['background'])
            
            ax.text(0.5, 0.95, 'ENERGY FLOW DIAGRAM', 
                   horizontalalignment='center', fontsize=18, fontweight='bold',
                   transform=ax.transAxes)
            
            # Energy Sources
            grid = FancyBboxPatch((0.05, 0.8), 0.15, 0.1,
                                boxstyle="round,pad=0.01",
                                facecolor=self.colors['warning'],
                                edgecolor=self.colors['border'], linewidth=2)
            ax.add_patch(grid)
            ax.text(0.125, 0.85, 'ELECTRICAL\nGRID\n480V 3Φ', ha='center', va='center', 
                   fontweight='bold', fontsize=10)
            
            gas_supply = FancyBboxPatch((0.25, 0.8), 0.15, 0.1,
                                      boxstyle="round,pad=0.01",
                                      facecolor=self.colors['heater'],
                                      edgecolor=self.colors['border'], linewidth=2)
            ax.add_patch(gas_supply)
            ax.text(0.325, 0.85, 'NATURAL GAS\nSUPPLY\n150 kW', ha='center', va='center', 
                   fontweight='bold', fontsize=10)
            
            # Main Distribution Panel
            main_panel = FancyBboxPatch((0.1, 0.6), 0.25, 0.1,
                                      boxstyle="round,pad=0.01",
                                      facecolor=self.colors['equipment'],
                                      edgecolor=self.colors['border'], linewidth=2)
            ax.add_patch(main_panel)
            ax.text(0.225, 0.65, 'MAIN ELECTRICAL PANEL\n500A - 480V', ha='center', va='center', 
                   fontweight='bold', fontsize=11)
            
            # Major Equipment Energy Consumption
            equipment_data = [
                {'name': 'Chiller\n150 kW', 'pos': (0.5, 0.7), 'power': 150, 'type': 'cooling'},
                {'name': 'Boiler\n120 kW', 'pos': (0.7, 0.7), 'power': 120, 'type': 'heating'},
                {'name': 'AHU Fans\n45 kW', 'pos': (0.5, 0.5), 'power': 45, 'type': 'air'},
                {'name': 'Pumps\n25 kW', 'pos': (0.7, 0.5), 'power': 25, 'type': 'water'},
                {'name': 'Lighting\n30 kW', 'pos': (0.5, 0.3), 'power': 30, 'type': 'lighting'},
                {'name': 'Controls\n5 kW', 'pos': (0.7, 0.3), 'power': 5, 'type': 'controls'}
            ]
            
            colors_by_type = {
                'cooling': self.colors['cooler'],
                'heating': self.colors['heater'],
                'air': self.colors['fan'],
                'water': self.colors['chilled_water'],
                'lighting': self.colors['warning'],
                'controls': self.colors['control']
            }
            
            total_power = 0
            for equipment in equipment_data:
                # Equipment box
                eq_color = colors_by_type.get(equipment['type'], self.colors['equipment'])
                eq_box = FancyBboxPatch((equipment['pos'][0]-0.06, equipment['pos'][1]-0.04), 
                                      0.12, 0.08, boxstyle="round,pad=0.005",
                                      facecolor=eq_color,
                                      edgecolor=self.colors['border'], linewidth=1)
                ax.add_patch(eq_box)
                ax.text(equipment['pos'][0], equipment['pos'][1], equipment['name'],
                       ha='center', va='center', fontsize=9, fontweight='bold')
                
                # Power flow lines
                ax.plot([0.35, equipment['pos'][0]-0.06], [0.65, equipment['pos'][1]],
                       color='red', linewidth=3, alpha=0.8)
                
                # Power consumption indicator
                power_width = equipment['power'] / 200 * 0.1  # Scale to fit
                power_rect = Rectangle((equipment['pos'][0]-power_width/2, equipment['pos'][1]-0.08), 
                                     power_width, 0.02, facecolor='red', alpha=0.7)
                ax.add_patch(power_rect)
                
                total_power += equipment['power']
            
            # Energy flow connections
            # Grid to main panel
            ax.plot([0.125, 0.125, 0.1], [0.8, 0.7, 0.7], color='red', linewidth=6)
            ax.plot([0.1, 0.1], [0.7, 0.65], color='red', linewidth=6)
            
            # Gas to boiler
            ax.plot([0.325, 0.325, 0.7], [0.8, 0.74, 0.74], color='orange', linewidth=4)
            
            # Energy efficiency indicators
            efficiency_data = """
ENERGY EFFICIENCY:
• Chiller COP: 3.2
• Boiler Efficiency: 85%
• Overall System Efficiency: 78%
• Peak Demand: 375 kW
• Annual Consumption: 1,250 MWh
            """
            ax.text(0.02, 0.5, efficiency_data, transform=ax.transAxes, fontsize=10,
                   bbox=dict(boxstyle="round,pad=0.5", facecolor='white', alpha=0.9))
            
            # Energy cost breakdown (pie chart)
            costs = [150, 120, 45, 25, 30, 5]  # kW values
            labels = ['Chiller', 'Boiler', 'AHU', 'Pumps', 'Lighting', 'Controls']
            colors = [colors_by_type['cooling'], colors_by_type['heating'], 
                     colors_by_type['air'], colors_by_type['water'],
                     colors_by_type['lighting'], colors_by_type['controls']]
            
            # Create small pie chart
            pie_ax = fig.add_axes([0.75, 0.05, 0.2, 0.2])
            pie_ax.pie(costs, labels=labels, colors=colors, autopct='%1.1f%%', 
                      textprops={'fontsize': 8})
            pie_ax.set_title('Power Distribution', fontsize=10, fontweight='bold')
            
            # Peak demand graph
            hours = list(range(0, 24, 2))
            demand = [200, 180, 170, 165, 180, 220, 280, 320, 350, 375, 360, 340]
            
            graph_ax = fig.add_axes([0.45, 0.05, 0.25, 0.15])
            graph_ax.plot(hours, demand, color=self.colors['danger'], linewidth=2, marker='o')
            graph_ax.set_xlabel('Hour of Day', fontsize=8)
            graph_ax.set_ylabel('Demand (kW)', fontsize=8)
            graph_ax.set_title('Daily Energy Demand Profile', fontsize=9, fontweight='bold')
            graph_ax.grid(True, alpha=0.3)
            graph_ax.tick_params(labelsize=7)
            
            # Total power consumption display
            total_box = FancyBboxPatch((0.8, 0.6), 0.15, 0.1,
                                     boxstyle="round,pad=0.01",
                                     facecolor=self.colors['danger'],
                                     edgecolor=self.colors['border'], linewidth=2)
            ax.add_patch(total_box)
            ax.text(0.875, 0.65, f'TOTAL LOAD\n{total_power} kW', ha='center', va='center', 
                   fontweight='bold', fontsize=11, color='white')
            
            # Legend
            legend_elements = [
                plt.Line2D([0], [0], color='red', lw=4, label='Electrical Power'),
                plt.Line2D([0], [0], color='orange', lw=4, label='Natural Gas'),
                plt.Rectangle((0, 0), 1, 1, facecolor=self.colors['cooler'], label='Cooling Equipment'),
                plt.Rectangle((0, 0), 1, 1, facecolor=self.colors['heater'], label='Heating Equipment')
            ]
            ax.legend(handles=legend_elements, loc='upper right', bbox_to_anchor=(0.45, 0.9))
            
            # Add timestamp
            ax.text(0.02, 0.02, f'Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}',
                   transform=ax.transAxes, fontsize=8, alpha=0.7)
            
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
            ax.set_aspect('equal')
            ax.axis('off')
            
            filename = os.path.join(self.output_dir, 'energy_flow_diagram.png')
            plt.savefig(filename, dpi=300, bbox_inches='tight',
                       facecolor=self.colors['background'])
            plt.close()
            return filename
            
        except Exception as e:
            print(f"Error generating energy flow diagram: {e}")
            plt.close()
            return None
    
    def generate_sensor_network(self) -> str:
        """Generate sensor network diagram"""
        try:
            fig, ax = plt.subplots(1, 1, figsize=(14, 10))
            fig.patch.set_facecolor(self.colors['background'])
            
            ax.text(0.5, 0.95, 'SENSOR NETWORK DIAGRAM', 
                   horizontalalignment='center', fontsize=18, fontweight='bold',
                   transform=ax.transAxes)
            
            # Central PLC/Data Acquisition System
            plc_system = FancyBboxPatch((0.4, 0.4), 0.2, 0.15,
                                      boxstyle="round,pad=0.01",
                                      facecolor=self.colors['control'],
                                      edgecolor=self.colors['border'], linewidth=3)
            ax.add_patch(plc_system)
            ax.text(0.5, 0.475, 'PLC SYSTEM\nData Acquisition\nEthernet/Modbus', 
                   ha='center', va='center', fontweight='bold', fontsize=11, color='white')
            
            # Sensor Categories and Locations
            sensor_groups = [
                {
                    'name': 'Temperature Sensors',
                    'sensors': [
                        {'id': 'T01', 'location': 'Zone 1 Supply', 'pos': (0.15, 0.8)},
                        {'id': 'T02', 'location': 'Zone 1 Return', 'pos': (0.15, 0.7)},
                        {'id': 'T03', 'location': 'Zone 2 Supply', 'pos': (0.25, 0.8)},
                        {'id': 'T04', 'location': 'Zone 2 Return', 'pos': (0.25, 0.7)},
                        {'id': 'T05', 'location': 'Outdoor Air', 'pos': (0.1, 0.6)},
                        {'id': 'T06', 'location': 'Chilled Water Supply', 'pos': (0.8, 0.8)},
                        {'id': 'T07', 'location': 'Chilled Water Return', 'pos': (0.85, 0.8)},
                        {'id': 'T08', 'location': 'Hot Water Supply', 'pos': (0.8, 0.7)},
                    ],
                    'color': self.colors['sensor'],
                    'symbol': 'T'
                },
                {
                    'name': 'Pressure Sensors',
                    'sensors': [
                        {'id': 'P01', 'location': 'Supply Fan', 'pos': (0.3, 0.6)},
                        {'id': 'P02', 'location': 'Return Fan', 'pos': (0.35, 0.6)},
                        {'id': 'P03', 'location': 'Filter Differential', 'pos': (0.25, 0.5)},
                        {'id': 'P04', 'location': 'Chilled Water', 'pos': (0.75, 0.6)},
                        {'id': 'P05', 'location': 'Hot Water', 'pos': (0.8, 0.6)},
                    ],
                    'color': self.colors['info'],
                    'symbol': 'P'
                },
                {
                    'name': 'Flow Sensors',
                    'sensors': [
                        {'id': 'F01', 'location': 'Main Supply Air', 'pos': (0.4, 0.8)},
                        {'id': 'F02', 'location': 'Outdoor Air', 'pos': (0.15, 0.5)},
                        {'id': 'F03', 'location': 'Chilled Water', 'pos': (0.75, 0.8)},
                        {'id': 'F04', 'location': 'Hot Water', 'pos': (0.75, 0.7)},
                    ],
                    'color': self.colors['success'],
                    'symbol': 'F'
                },
                {
                    'name': 'Humidity Sensors',
                    'sensors': [
                        {'id': 'H01', 'location': 'Zone 1', 'pos': (0.2, 0.3)},
                        {'id': 'H02', 'location': 'Zone 2', 'pos': (0.3, 0.3)},
                        {'id': 'H03', 'location': 'Outdoor Air', 'pos': (0.1, 0.4)},
                        {'id': 'H04', 'location': 'Mixed Air', 'pos': (0.2, 0.4)},
                    ],
                    'color': self.colors['warning'],
                    'symbol': 'H'
                }
            ]
            
            # Draw sensors and connections
            for group in sensor_groups:
                for sensor in group['sensors']:
                    # Sensor symbol
                    sensor_circle = Circle(sensor['pos'], 0.02, 
                                         facecolor=group['color'],
                                         edgecolor=self.colors['border'], linewidth=1)
                    ax.add_patch(sensor_circle)
                    ax.text(sensor['pos'][0], sensor['pos'][1], group['symbol'], 
                           ha='center', va='center', fontweight='bold', fontsize=8, color='white')
                    
                    # Sensor ID
                    ax.text(sensor['pos'][0], sensor['pos'][1]-0.04, sensor['id'],
                           ha='center', va='top', fontsize=7, fontweight='bold')
                    
                    # Connection line to PLC
                    ax.plot([sensor['pos'][0], 0.4], [sensor['pos'][1], 0.475],
                           color=group['color'], linewidth=1, alpha=0.6, linestyle='--')
            
            # Communication Networks
            # Ethernet backbone
            ethernet_points = [(0.1, 0.2), (0.3, 0.2), (0.5, 0.2), (0.7, 0.2), (0.9, 0.2)]
            for i in range(len(ethernet_points)-1):
                ax.plot([ethernet_points[i][0], ethernet_points[i+1][0]], 
                       [ethernet_points[i][1], ethernet_points[i+1][1]],
                       color=self.colors['control'], linewidth=4, alpha=0.8)
            
            # Network nodes
            for i, point in enumerate(ethernet_points):
                node = Rectangle((point[0]-0.02, point[1]-0.01), 0.04, 0.02,
                               facecolor=self.colors['equipment'],
                               edgecolor=self.colors['border'])
                ax.add_patch(node)
                ax.text(point[0], point[1], f'N{i+1}', ha='center', va='center', 
                       fontsize=7, fontweight='bold')
            
            # PLC connection to network
            ax.plot([0.5, 0.5], [0.4, 0.22], color=self.colors['control'], linewidth=4)
            
            # Wireless sensors
            wireless_sensors = [
                {'id': 'W01', 'location': 'Remote Zone', 'pos': (0.85, 0.3)},
                {'id': 'W02', 'location': 'Rooftop Unit', 'pos': (0.9, 0.5)},
                {'id': 'W03', 'location': 'Parking Garage', 'pos': (0.85, 0.4)}
            ]
            
            for wsensor in wireless_sensors:
                # Wireless sensor
                ws_circle = Circle(wsensor['pos'], 0.025, 
                                 facecolor=self.colors['highlight'],
                                 edgecolor=self.colors['border'], linewidth=2)
                ax.add_patch(ws_circle)
                ax.text(wsensor['pos'][0], wsensor['pos'][1], 'W', 
                       ha='center', va='center', fontweight='bold', fontsize=9, color='white')
                ax.text(wsensor['pos'][0], wsensor['pos'][1]-0.05, wsensor['id'],
                       ha='center', va='top', fontsize=7, fontweight='bold')
                
                # Wireless connection (wavy line)
                import math
                x_vals = [wsensor['pos'][0] - 0.1 + i*0.01 for i in range(11)]
                y_vals = [wsensor['pos'][1] + 0.02*math.sin(i*2) for i in range(11)]
                ax.plot(x_vals, y_vals, color=self.colors['highlight'], 
                       linewidth=2, alpha=0.7)
            
            # Wireless gateway
            gateway = FancyBboxPatch((0.7, 0.35), 0.08, 0.05,
                                   boxstyle="round,pad=0.005",
                                   facecolor=self.colors['highlight'],
                                   edgecolor=self.colors['border'], linewidth=2)
            ax.add_patch(gateway)
            ax.text(0.74, 0.375, 'WiFi\nGateway', ha='center', va='center', 
                   fontsize=8, fontweight='bold', color='white')
            
            # Gateway connection to network
            ax.plot([0.7, 0.7], [0.375, 0.22], color=self.colors['control'], linewidth=3)
            
            # Legend
            legend_elements = []
            for group in sensor_groups:
                legend_elements.append(
                    plt.Line2D([0], [0], marker='o', color='w', 
                              markerfacecolor=group['color'], markersize=8, 
                              label=group['name'])
                )
            legend_elements.extend([
                plt.Line2D([0], [0], marker='o', color='w', 
                          markerfacecolor=self.colors['highlight'], markersize=8, 
                          label='Wireless Sensors'),
                plt.Line2D([0], [0], color=self.colors['control'], lw=3, 
                          label='Ethernet Network'),
                plt.Rectangle((0, 0), 1, 1, facecolor=self.colors['equipment'], 
                            label='Network Nodes')
            ])
            ax.legend(handles=legend_elements, loc='upper left', bbox_to_anchor=(0, 0.9))
            
            # System specifications
            specs = """
NETWORK SPECIFICATIONS:
• Protocol: Modbus TCP/IP over Ethernet
• Network Speed: 100 Mbps
• Wireless: 802.11n WiFi
• Total Sensors: 24 Wired + 3 Wireless
• Scan Rate: 1 second
• Data Storage: 30 days local, 1 year cloud
            """
            ax.text(0.02, 0.4, specs, transform=ax.transAxes, fontsize=9,
                   bbox=dict(boxstyle="round,pad=0.5", facecolor='white', alpha=0.9))
            
            # Sensor status indicators
            status_info = """
SENSOR STATUS:
🟢 Online: 25 sensors
🟡 Warning: 2 sensors
🔴 Offline: 0 sensors
📊 Data Quality: 98.5%
            """
            ax.text(0.75, 0.15, status_info, transform=ax.transAxes, fontsize=9,
                   bbox=dict(boxstyle="round,pad=0.5", facecolor='lightgreen', alpha=0.9))
            
            # Add timestamp
            ax.text(0.98, 0.02, f'Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}',
                   transform=ax.transAxes, fontsize=8, alpha=0.7, ha='right')
            
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
            ax.set_aspect('equal')
            ax.axis('off')
            
            filename = os.path.join(self.output_dir, 'sensor_network.png')
            plt.savefig(filename, dpi=300, bbox_inches='tight',
                       facecolor=self.colors['background'])
            plt.close()
            return filename
            
        except Exception as e:
            print(f"Error generating sensor network: {e}")
            plt.close()
            return None
    
    def generate_safety_systems(self) -> str:
        """Generate safety systems diagram"""
        try:
            fig, ax = plt.subplots(1, 1, figsize=(14, 10))
            fig.patch.set_facecolor(self.colors['background'])
            
            ax.text(0.5, 0.95, 'SAFETY SYSTEMS DIAGRAM', 
                   horizontalalignment='center', fontsize=18, fontweight='bold',
                   transform=ax.transAxes)
            
            # Central Safety Control Panel
            safety_panel = FancyBboxPatch((0.4, 0.7), 0.2, 0.15,
                                        boxstyle="round,pad=0.01",
                                        facecolor=self.colors['danger'],
                                        edgecolor=self.colors['border'], linewidth=3)
            ax.add_patch(safety_panel)
            ax.text(0.5, 0.775, 'SAFETY CONTROL\nPANEL\nEmergency Override', 
                   ha='center', va='center', fontweight='bold', fontsize=11, color='white')
            
            # Emergency Stop Buttons
            estop_locations = [
                {'name': 'Main Control Room', 'pos': (0.1, 0.8)},
                {'name': 'Equipment Room', 'pos': (0.9, 0.8)},
                {'name': 'Zone 1 Exit', 'pos': (0.1, 0.5)},
                {'name': 'Zone 2 Exit', 'pos': (0.9, 0.5)},
                {'name': 'Mechanical Room', 'pos': (0.5, 0.3)}
            ]
            
            for estop in estop_locations:
                # Emergency stop button
                button = Circle(estop['pos'], 0.03, facecolor=self.colors['danger'],
                              edgecolor='darkred', linewidth=3)
                ax.add_patch(button)
                ax.text(estop['pos'][0], estop['pos'][1], 'E-STOP', ha='center', va='center', 
                       fontweight='bold', fontsize=7, color='white')
                ax.text(estop['pos'][0], estop['pos'][1]-0.06, estop['name'],
                       ha='center', va='top', fontsize=8, fontweight='bold')
                
                # Connection to safety panel
                ax.plot([estop['pos'][0], 0.5], [estop['pos'][1], 0.7],
                       color=self.colors['danger'], linewidth=2, alpha=0.7, linestyle='--')
            
            # Fire Safety Systems
            fire_detectors = [
                {'name': 'Smoke Detector\nZone 1', 'pos': (0.2, 0.6), 'type': 'smoke'},
                {'name': 'Smoke Detector\nZone 2', 'pos': (0.3, 0.6), 'type': 'smoke'},
                {'name': 'Heat Detector\nEquipment Room', 'pos': (0.7, 0.6), 'type': 'heat'},
                {'name': 'Flame Detector\nBoiler Room', 'pos': (0.8, 0.6), 'type': 'flame'}
            ]
            
            detector_colors = {
                'smoke': self.colors['equipment'],
                'heat': self.colors['warning'],
                'flame': self.colors['heater']
            }
            
            for detector in fire_detectors:
                det_color = detector_colors[detector['type']]
                detector_box = FancyBboxPatch((detector['pos'][0]-0.04, detector['pos'][1]-0.03), 
                                            0.08, 0.06, boxstyle="round,pad=0.005",
                                            facecolor=det_color,
                                            edgecolor=self.colors['border'], linewidth=1)
                ax.add_patch(detector_box)
                ax.text(detector['pos'][0], detector['pos'][1], detector['name'],
                       ha='center', va='center', fontsize=8, fontweight='bold')
                
                # Connection to fire panel
                ax.plot([detector['pos'][0], 0.4], [detector['pos'][1], 0.775],
                       color='orange', linewidth=2, alpha=0.7, linestyle=':')
            
            # Fire Suppression Panel
            fire_panel = FancyBboxPatch((0.15, 0.75), 0.15, 0.1,
                                      boxstyle="round,pad=0.01",
                                      facecolor='orange',
                                      edgecolor=self.colors['border'], linewidth=2)
            ax.add_patch(fire_panel)
            ax.text(0.225, 0.8, 'FIRE ALARM\nPANEL', ha='center', va='center', 
                   fontweight='bold', fontsize=10)
            
            # Gas Leak Detection
            gas_detectors = [
                {'name': 'Gas Detector\nBoiler Room', 'pos': (0.75, 0.4)},
                {'name': 'Gas Detector\nMechanical Room', 'pos': (0.65, 0.35)}
            ]
            
            for gas_det in gas_detectors:
                gas_circle = Circle(gas_det['pos'], 0.025, facecolor='yellow',
                                  edgecolor=self.colors['border'], linewidth=2)
                ax.add_patch(gas_circle)
                ax.text(gas_det['pos'][0], gas_det['pos'][1], 'GAS', ha='center', va='center', 
                       fontweight='bold', fontsize=7)
                ax.text(gas_det['pos'][0], gas_det['pos'][1]-0.05, gas_det['name'],
                       ha='center', va='top', fontsize=7, fontweight='bold')
                
                # Connection to safety panel
                ax.plot([gas_det['pos'][0], 0.5], [gas_det['pos'][1], 0.7],
                       color='yellow', linewidth=2, alpha=0.7, linestyle='-.')
            
            # Pressure Relief Systems
            relief_valves = [
                {'name': 'PRV-1\nChilled Water', 'pos': (0.2, 0.4)},
                {'name': 'PRV-2\nHot Water', 'pos': (0.35, 0.4)},
                {'name': 'PRV-3\nSteam', 'pos': (0.5, 0.4)}
            ]
            
            for valve in relief_valves:
                valve_triangle = Polygon([(valve['pos'][0]-0.02, valve['pos'][1]-0.02),
                                        (valve['pos'][0]+0.02, valve['pos'][1]-0.02),
                                        (valve['pos'][0], valve['pos'][1]+0.02)],
                                       facecolor=self.colors['valve'],
                                       edgecolor=self.colors['border'])
                ax.add_patch(valve_triangle)
                ax.text(valve['pos'][0], valve['pos'][1]-0.05, valve['name'],
                       ha='center', va='top', fontsize=8, fontweight='bold')
            
            # Ventilation Override System
            ventilation_override = FancyBboxPatch((0.7, 0.75), 0.15, 0.1,
                                                boxstyle="round,pad=0.01",
                                                facecolor=self.colors['fan'],
                                                edgecolor=self.colors['border'], linewidth=2)
            ax.add_patch(ventilation_override)
            ax.text(0.775, 0.8, 'SMOKE\nEVACUATION\nFANS', ha='center', va='center', 
                   fontweight='bold', fontsize=10)
            
            # Emergency Power Systems
            ups_system = FancyBboxPatch((0.1, 0.2), 0.15, 0.08,
                                      boxstyle="round,pad=0.01",
                                      facecolor=self.colors['warning'],
                                      edgecolor=self.colors['border'], linewidth=2)
            ax.add_patch(ups_system)
            ax.text(0.175, 0.24, 'UPS SYSTEM\n15 min backup', ha='center', va='center', 
                   fontweight='bold', fontsize=9)
            
            generator = FancyBboxPatch((0.3, 0.2), 0.15, 0.08,
                                     boxstyle="round,pad=0.01",
                                     facecolor=self.colors['success'],
                                     edgecolor=self.colors['border'], linewidth=2)
            ax.add_patch(generator)
            ax.text(0.375, 0.24, 'GENERATOR\n24 hr backup', ha='center', va='center', 
                   fontweight='bold', fontsize=9)
            
            # Safety Interlocks
            interlock_info = """
SAFETY INTERLOCKS:
• Equipment shutdown on E-Stop
• Fire suppression system activation
• Emergency ventilation mode
• Gas leak isolation valves
• Pressure relief activation
• Emergency lighting activation
            """
            ax.text(0.52, 0.35, interlock_info, transform=ax.transAxes, fontsize=9,
                   bbox=dict(boxstyle="round,pad=0.5", facecolor='lightcoral', alpha=0.9))
            
            # Emergency Procedures
            procedures = """
EMERGENCY PROCEDURES:
1. Activate E-Stop if unsafe conditions
2. Evacuate personnel from affected areas
3. Call emergency services if required
4. Check gas leak detectors regularly
5. Test fire suppression systems monthly
6. Verify emergency power systems
            """
            ax.text(0.02, 0.35, procedures, transform=ax.transAxes, fontsize=9,
                   bbox=dict(boxstyle="round,pad=0.5", facecolor='lightyellow', alpha=0.9))
            
            # System Status Indicators
            status_lights = [
                {'name': 'System Normal', 'pos': (0.85, 0.3), 'color': 'green'},
                {'name': 'Warning', 'pos': (0.85, 0.25), 'color': 'yellow'},
                {'name': 'Emergency', 'pos': (0.85, 0.2), 'color': 'red'}
            ]
            
            for light in status_lights:
                light_circle = Circle(light['pos'], 0.015, facecolor=light['color'],
                                    edgecolor='black', linewidth=1)
                ax.add_patch(light_circle)
                ax.text(light['pos'][0]+0.03, light['pos'][1], light['name'],
                       ha='left', va='center', fontsize=8, fontweight='bold')
            
            # Legend
            legend_elements = [
                plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=self.colors['danger'],
                          markersize=10, label='Emergency Stop'),
                plt.Rectangle((0, 0), 1, 1, facecolor='orange', label='Fire Detection'),
                plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='yellow',
                          markersize=8, label='Gas Detection'),
                plt.Rectangle((0, 0), 1, 1, facecolor=self.colors['valve'], label='Relief Valves'),
                plt.Rectangle((0, 0), 1, 1, facecolor=self.colors['warning'], label='Emergency Power')
            ]
            ax.legend(handles=legend_elements, loc='upper right', bbox_to_anchor=(0.98, 0.7))
            
            # Add timestamp
            ax.text(0.98, 0.02, f'Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}',
                   transform=ax.transAxes, fontsize=8, alpha=0.7, ha='right')
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
            ax.set_aspect('equal')
            ax.axis('off')
            
            filename = os.path.join(self.output_dir, 'safety_systems.png')
            plt.savefig(filename, dpi=300, bbox_inches='tight',
                       facecolor=self.colors['background'])
            plt.close()
            
            return filename
            
        except Exception as e:
            print(f"Error generating safety systems: {e}")
            plt.close()
            return None

    def generate_maintenance_diagram(self) -> str:
        """Generate maintenance points diagram"""
        try:
            fig, ax = plt.subplots(1, 1, figsize=(14, 10))
            fig.patch.set_facecolor(self.colors['background'])
            
            ax.text(0.5, 0.95, 'MAINTENANCE POINTS DIAGRAM', 
                   horizontalalignment='center', fontsize=18, fontweight='bold',
                   transform=ax.transAxes)
            
            # Equipment Layout with Maintenance Points
            equipment_layout = [
                {'name': 'AHU-1', 'pos': (0.15, 0.7), 'type': 'ahu', 'maintenance': 'monthly'},
                {'name': 'Chiller', 'pos': (0.4, 0.8), 'type': 'chiller', 'maintenance': 'quarterly'},
                {'name': 'Boiler', 'pos': (0.6, 0.8), 'type': 'boiler', 'maintenance': 'monthly'},
                {'name': 'Cooling Tower', 'pos': (0.8, 0.7), 'type': 'tower', 'maintenance': 'weekly'},
                {'name': 'Pump P-1', 'pos': (0.3, 0.6), 'type': 'pump', 'maintenance': 'quarterly'},
                {'name': 'Pump P-2', 'pos': (0.7, 0.6), 'type': 'pump', 'maintenance': 'quarterly'},
                {'name': 'Control Panel', 'pos': (0.5, 0.5), 'type': 'control', 'maintenance': 'monthly'}
            ]
            
            maintenance_colors = {
                'weekly': self.colors['danger'],
                'monthly': self.colors['warning'],
                'quarterly': self.colors['success'],
                'annually': self.colors['info']
            }
            
            equipment_colors = {
                'ahu': self.colors['equipment'],
                'chiller': self.colors['cooler'],
                'boiler': self.colors['heater'],
                'tower': self.colors['fan'],
                'pump': self.colors['chilled_water'],
                'control': self.colors['control']
            }
            
            # Draw equipment with maintenance indicators
            for equipment in equipment_layout:
                # Equipment box
                eq_color = equipment_colors.get(equipment['type'], self.colors['equipment'])
                eq_box = FancyBboxPatch((equipment['pos'][0]-0.06, equipment['pos'][1]-0.04), 
                                      0.12, 0.08, boxstyle="round,pad=0.005",
                                      facecolor=eq_color,
                                      edgecolor=self.colors['border'], linewidth=2)
                ax.add_patch(eq_box)
                ax.text(equipment['pos'][0], equipment['pos'][1], equipment['name'],
                       ha='center', va='center', fontsize=10, fontweight='bold')
                
                # Maintenance frequency indicator
                maint_color = maintenance_colors.get(equipment['maintenance'], self.colors['equipment'])
                maint_circle = Circle((equipment['pos'][0]+0.05, equipment['pos'][1]+0.03), 0.02,
                                    facecolor=maint_color, edgecolor='black', linewidth=1)
                ax.add_patch(maint_circle)
                ax.text(equipment['pos'][0]+0.05, equipment['pos'][1]+0.03, 'M',
                       ha='center', va='center', fontsize=8, fontweight='bold', color='white')
                
                # Maintenance interval label
                ax.text(equipment['pos'][0], equipment['pos'][1]-0.07, equipment['maintenance'],
                       ha='center', va='top', fontsize=8, style='italic')
            
            # Maintenance Access Points
            access_points = [
                {'name': 'Filter Access\nPanel', 'pos': (0.1, 0.4), 'tool': 'screwdriver'},
                {'name': 'Belt Inspection\nDoor', 'pos': (0.25, 0.4), 'tool': 'flashlight'},
                {'name': 'Refrigerant\nService Port', 'pos': (0.4, 0.4), 'tool': 'gauges'},
                {'name': 'Drain Pan\nAccess', 'pos': (0.55, 0.4), 'tool': 'wrench'},
                {'name': 'Motor\nLubrication', 'pos': (0.7, 0.4), 'tool': 'grease gun'},
                {'name': 'Control\nCabinet', 'pos': (0.85, 0.4), 'tool': 'multimeter'}
            ]
            
            for access in access_points:
                # Access point box
                access_box = Rectangle((access['pos'][0]-0.04, access['pos'][1]-0.03), 
                                     0.08, 0.06, facecolor=self.colors['zone'],
                                     edgecolor=self.colors['border'], linewidth=1)
                ax.add_patch(access_box)
                ax.text(access['pos'][0], access['pos'][1], access['name'],
                       ha='center', va='center', fontsize=8, fontweight='bold')
                
                # Tool requirement
                ax.text(access['pos'][0], access['pos'][1]-0.05, f"Tool: {access['tool']}",
                       ha='center', va='top', fontsize=7, style='italic')
            
            # Maintenance Schedule Calendar
            calendar_data = """
MAINTENANCE SCHEDULE:

WEEKLY:
• Cooling tower inspection
• Visual equipment check
• Log readings

MONTHLY:
• Filter replacement
• Belt tension check
• Lubrication points
• Control calibration

QUARTERLY:
• Pump maintenance
• Chiller service
• Electrical connections
• Safety system test

ANNUALLY:
• Complete system overhaul
• Efficiency testing
• Pressure testing
• Documentation update
            """
            ax.text(0.02, 0.35, calendar_data, transform=ax.transAxes, fontsize=9,
                   bbox=dict(boxstyle="round,pad=0.5", facecolor='lightyellow', alpha=0.9))
            
            # Maintenance Tools Required
            tools_info = """
REQUIRED TOOLS:
🔧 Basic hand tools
🔩 Socket set (metric & imperial)
⚡ Multimeter & electrical tools
🌡️ Temperature measurement
📏 Pressure gauges
🔦 Flashlight/headlamp
🧤 Safety equipment (PPE)
📋 Maintenance logs
            """
            ax.text(0.52, 0.35, tools_info, transform=ax.transAxes, fontsize=9,
                   bbox=dict(boxstyle="round,pad=0.5", facecolor='lightblue', alpha=0.9))
            
            # Critical Maintenance Points
            critical_points = [
                {'name': 'Emergency Stop\nTest', 'pos': (0.2, 0.2), 'priority': 'critical'},
                {'name': 'Safety Valve\nCheck', 'pos': (0.4, 0.2), 'priority': 'critical'},
                {'name': 'Fire System\nTest', 'pos': (0.6, 0.2), 'priority': 'critical'},
                {'name': 'Backup Power\nTest', 'pos': (0.8, 0.2), 'priority': 'critical'}
            ]
            
            for critical in critical_points:
                # Critical maintenance point
                crit_diamond = Polygon([(critical['pos'][0]-0.03, critical['pos'][1]),
                                      (critical['pos'][0], critical['pos'][1]+0.03),
                                      (critical['pos'][0]+0.03, critical['pos'][1]),
                                      (critical['pos'][0], critical['pos'][1]-0.03)],
                                     facecolor=self.colors['danger'],
                                     edgecolor='darkred', linewidth=2)
                ax.add_patch(crit_diamond)
                ax.text(critical['pos'][0], critical['pos'][1], '!', ha='center', va='center',
                       fontsize=12, fontweight='bold', color='white')
                ax.text(critical['pos'][0], critical['pos'][1]-0.06, critical['name'],
                       ha='center', va='top', fontsize=8, fontweight='bold')
            
            # Maintenance Status Tracking
            status_tracking = """
MAINTENANCE STATUS:
🟢 Up to Date: 85%
🟡 Due Soon: 10%
🔴 Overdue: 5%

NEXT SCHEDULED:
• Filter Change: 3 days
• Pump Service: 1 week
• Safety Test: 2 weeks
            """
            ax.text(0.75, 0.15, status_tracking, transform=ax.transAxes, fontsize=9,
                   bbox=dict(boxstyle="round,pad=0.5", facecolor='lightgreen', alpha=0.9))
            
            # Spare Parts Inventory
            spare_parts = [
                {'name': 'Filters', 'qty': '12', 'pos': (0.1, 0.1)},
                {'name': 'Belts', 'qty': '4', 'pos': (0.25, 0.1)},
                {'name': 'Fuses', 'qty': '20', 'pos': (0.4, 0.1)},
                {'name': 'Gaskets', 'qty': '8', 'pos': (0.55, 0.1)}
            ]
            
            for part in spare_parts:
                part_box = Rectangle((part['pos'][0]-0.03, part['pos'][1]-0.02), 
                                   0.06, 0.04, facecolor=self.colors['equipment'],
                                   edgecolor=self.colors['border'], linewidth=1)
                ax.add_patch(part_box)
                ax.text(part['pos'][0], part['pos'][1], f"{part['name']}\nQty: {part['qty']}",
                       ha='center', va='center', fontsize=7, fontweight='bold')
            
            # Legend
            legend_elements = [
                plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=self.colors['danger'],
                          markersize=8, label='Weekly Maintenance'),
                plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=self.colors['warning'],
                          markersize=8, label='Monthly Maintenance'),
                plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=self.colors['success'],
                          markersize=8, label='Quarterly Maintenance'),
                plt.Line2D([0], [0], marker='D', color='w', markerfacecolor=self.colors['danger'],
                          markersize=8, label='Critical Safety Points'),
                plt.Rectangle((0, 0), 1, 1, facecolor=self.colors['zone'], label='Access Points')
            ]
            ax.legend(handles=legend_elements, loc='upper right', bbox_to_anchor=(0.98, 0.9))
            
            # Add timestamp
            ax.text(0.98, 0.02, f'Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}',
                   transform=ax.transAxes, fontsize=8, alpha=0.7, ha='right')
            
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
            ax.set_aspect('equal')
            ax.axis('off')
            
            filename = os.path.join(self.output_dir, 'maintenance_diagram.png')
            plt.savefig(filename, dpi=300, bbox_inches='tight',
                       facecolor=self.colors['background'])
            plt.close()
            
            return filename
            
        except Exception as e:
            print(f"Error generating maintenance diagram: {e}")
            plt.close()
            return None
    
    def generate_diagram_index(self, generated_files: List[str]):
        """Generate HTML index page for all diagrams"""
        try:
            index_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>HVAC System Diagrams - Index</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #333;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 10px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }
        h1 {
            text-align: center;
            color: #2c3e50;
            margin-bottom: 30px;
            font-size: 2.5em;
        }
        .diagrams-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-top: 30px;
        }
        .diagram-card {
            border: 1px solid #ddd;
            border-radius: 8px;
            padding: 15px;
            text-align: center;
            background: #f8f9fa;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        .diagram-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }
        .diagram-card img {
            max-width: 100%;
            height: auto;
            border-radius: 5px;
            margin-bottom: 10px;
        }
        .diagram-card h3 {
            margin: 10px 0;
            color: #2c3e50;
        }
        .info-box {
            background: #e8f4fd;
            border-left: 4px solid #2196F3;
            padding: 15px;
            margin: 20px 0;
            border-radius: 5px;
        }
        .timestamp {
            text-align: center;
            color: #666;
            margin-top: 30px;
            font-style: italic;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 HVAC Control System - Technical Diagrams</h1>
        
        <div class="info-box">
            <h3>📋 Documentation Overview</h3>
            <p>This collection contains comprehensive technical diagrams for the HVAC control system, 
            including system overviews, zone layouts, piping schematics, electrical diagrams, 
            and control flow charts. Each diagram provides detailed technical information for 
            system understanding, operation, and maintenance.</p>
        </div>
        
        <div class="diagrams-grid">
"""
            
            # Add diagram cards
            diagram_info = {
                'system_overview.png': 'System Overview - Complete HVAC system architecture',
                'zone_layout.png': 'Zone Layout - Building zones and sensor locations',
                'piping_schematic.png': 'Piping Schematic - Hydronic system piping',
                'electrical_diagram.png': 'Electrical Diagram - Power distribution',
                'control_flow.png': 'Control Flow - System control architecture',
                'air_flow_diagram.png': 'Air Flow - Ventilation and air distribution',
                'energy_flow_diagram.png': 'Energy Flow - Energy management system',
                'sensor_network.png': 'Sensor Network - Monitoring infrastructure',
                'safety_systems.png': 'Safety Systems - Emergency and safety controls',
                'maintenance_diagram.png': 'Maintenance Points - Service and maintenance locations'
            }
            
            for filename in generated_files:
                diagram_name = os.path.basename(filename)
                if diagram_name in diagram_info:
                    title = diagram_info[diagram_name]
                    index_content += f"""
            <div class="diagram-card">
                <img src="{diagram_name}" alt="{title}" onclick="window.open('{diagram_name}', '_blank')">
                <h3>{title.split(' - ')[0]}</h3>
                <p>{title.split(' - ')[1] if ' - ' in title else title}</p>
            </div>"""
            
            index_content += f"""
        </div>
        
        <div class="timestamp">
            <p>Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
            <p>Total Diagrams: {len(generated_files)}</p>
        </div>
    </div>
</body>
</html>"""
            
            index_file = os.path.join(self.output_dir, 'index.html')
            with open(index_file, 'w', encoding='utf-8') as f:
                f.write(index_content)
            
            print(f"📄 Diagram index generated: {index_file}")
            
        except Exception as e:
            print(f"Error generating diagram index: {e}")

def main():
    """Main function to generate all diagrams"""
    print("🎨 HVAC System Diagram Generator")
    print("=" * 40)
    
    if not MATPLOTLIB_AVAILABLE:
        print("❌ matplotlib is required for diagram generation")
        print("   Install with: pip install matplotlib")
        return 1
    
    try:
        generator = HVACDiagramGenerator()
        generated_files = generator.generate_all_diagrams()
        
        if generated_files:
            print(f"\n📊 Successfully generated {len(generated_files)} diagrams")
            print(f"📁 Output directory: {generator.output_dir}")
            print("📄 Open 'index.html' to view all diagrams")
        else:
            print("❌ No diagrams were generated")
            return 1
        
    except Exception as e:
        print(f"❌ Error generating diagrams: {e}")
        return 1
        
    return 0

if __name__ == "__main__":
    exit(main())
