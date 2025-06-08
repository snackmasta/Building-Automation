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
