# Wastewater Treatment Plant Diagram Generator
# This script generates system diagrams for the Wastewater Treatment Plant control system

import os
import sys
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.path import Path
import numpy as np
import networkx as nx
from datetime import datetime

# Set script directory as working directory
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)
project_root = os.path.abspath(os.path.join(script_dir, '..', '..'))

# Create output directory if it doesn't exist
diagrams_dir = os.path.join(project_root, 'diagrams')
if not os.path.exists(diagrams_dir):
    os.makedirs(diagrams_dir)

# --- Configuration ---
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial', 'Helvetica', 'DejaVu Sans']
plt.rcParams['font.size'] = 12

# Colors
colors = {
    'background': '#f8f9fa',
    'process_block': '#d0e1f9',
    'control_block': '#d6eaf8',
    'signal_line': '#2c3e50',
    'water_line': '#3498db',
    'valve': '#e74c3c',
    'pump': '#2ecc71',
    'sensor': '#f39c12',
    'arrow': '#7f8c8d',
    'text': '#2c3e50',
    'heading': '#2c3e50'
}

# --- Helper Functions ---
def add_pump_symbol(ax, x, y, size=0.5, angle=0, color='#2ecc71'):
    """Add a pump symbol at the specified location"""
    circle = plt.Circle((x, y), size/2, fill=True, color=color, zorder=10)
    ax.add_artist(circle)
    
    # Add triangle inside
    triangle_height = size * 0.7
    triangle_width = size * 0.7
    
    # Calculate triangle points with rotation
    radians = np.deg2rad(angle)
    cos_angle = np.cos(radians)
    sin_angle = np.sin(radians)
    
    # Original points
    triangle_points = [
        [x - triangle_width/2, y - triangle_height/3],
        [x + triangle_width/2, y - triangle_height/3],
        [x, y + triangle_height*2/3]
    ]
    
    # Rotate points around (x,y)
    rotated_points = []
    for px, py in triangle_points:
        dx = px - x
        dy = py - y
        rotated_points.append([
            x + dx * cos_angle - dy * sin_angle,
            y + dx * sin_angle + dy * cos_angle
        ])
    
    triangle = plt.Polygon(rotated_points, fill=True, color='white', zorder=11)
    ax.add_artist(triangle)
    
    return circle

def add_valve_symbol(ax, x, y, size=0.4, angle=0, color='#e74c3c'):
    """Add a valve symbol at the specified location"""
    # Create diamond shape
    diamond = plt.Polygon([
        [x, y + size/2],
        [x + size/2, y],
        [x, y - size/2],
        [x - size/2, y]
    ], fill=True, color=color, zorder=10)
    ax.add_artist(diamond)
    
    # Add line across
    line_length = size * 0.7
    line = plt.Line2D(
        [x - line_length/2, x + line_length/2], 
        [y, y], 
        color='white', 
        linewidth=2,
        zorder=11
    )
    ax.add_artist(line)
    
    return diamond

def add_sensor_symbol(ax, x, y, size=0.3, sensor_type='', color='#f39c12'):
    """Add a sensor symbol with label at the specified location"""
    circle = plt.Circle((x, y), size/2, fill=True, color=color, zorder=10)
    ax.add_artist(circle)
    
    # Add sensor type text
    if sensor_type:
        ax.text(x, y, sensor_type, ha='center', va='center', 
                color='white', fontweight='bold', zorder=11, fontsize=8)
    
    return circle

def draw_flow_arrow(ax, x, y, direction='right', size=0.3, color='#7f8c8d'):
    """Draw a flow direction arrow"""
    if direction == 'right':
        dx, dy = size, 0
    elif direction == 'left':
        dx, dy = -size, 0
    elif direction == 'up':
        dx, dy = 0, size
    else:  # down
        dx, dy = 0, -size
        
    arrow = ax.arrow(x, y, dx, dy, head_width=size*0.6, 
                    head_length=size*0.4, fc=color, ec=color,
                    length_includes_head=True, zorder=9)
    return arrow

def draw_tank(ax, x, y, width, height, fill_percent=0.7, label='', fill_color='#3498db'):
    """Draw a process tank with optional fill level"""
    # Draw tank outline
    tank = plt.Rectangle((x-width/2, y-height/2), width, height, 
                         fill=False, linewidth=2, color='black', zorder=5)
    ax.add_artist(tank)
    
    # Draw fill level
    fill_height = height * fill_percent
    fill = plt.Rectangle((x-width/2, y-height/2), width, fill_height, 
                         fill=True, color=fill_color, alpha=0.5, zorder=4)
    ax.add_artist(fill)
    
    # Add label
    if label:
        ax.text(x, y+height/2+0.2, label, ha='center', va='bottom', 
                color=colors['text'], fontweight='bold')
    
    return tank

def draw_pipe(ax, start, end, width=0.1, color='#3498db', zorder=3):
    """Draw a pipe connecting two points"""
    x1, y1 = start
    x2, y2 = end
    
    # For vertical or horizontal lines
    if x1 == x2 or y1 == y2:
        pipe = plt.Line2D([x1, x2], [y1, y2], linewidth=width*20, 
                         color=color, solid_capstyle='butt', zorder=zorder)
    else:
        # For complex paths, use two segments with a right angle
        mid_x, mid_y = x1, y2  # Create a right angle
        
        # Create path
        verts = [(x1, y1), (mid_x, mid_y), (x2, y2)]
        codes = [Path.MOVETO, Path.LINETO, Path.LINETO]
        path = Path(verts, codes)
        
        pipe = patches.PathPatch(path, linewidth=width*20, 
                                color=color, zorder=zorder)
    
    ax.add_artist(pipe)
    return pipe

# --- Diagram Generation Functions ---

def generate_process_flow_diagram():
    """Generate a process flow diagram for the wastewater treatment plant"""
    print("Generating Process Flow Diagram...")
    
    # Create figure and axis
    fig, ax = plt.subplots(figsize=(16, 10))
    fig.patch.set_facecolor(colors['background'])
    ax.set_facecolor(colors['background'])
    
    # Remove axes
    ax.set_axis_off()
    
    # Set plot limits
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 10)
    
    # Title
    ax.set_title('Wastewater Treatment Plant - Process Flow Diagram', 
                 fontsize=20, fontweight='bold', color=colors['heading'], pad=20)
    
    # Footer with date
    footer_text = f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    fig.text(0.98, 0.02, footer_text, ha='right', va='bottom', 
             fontsize=8, color=colors['text'])
    
    # --- Draw Process Units ---
    
    # 1. Intake/Screening
    intake_x, intake_y = 1.5, 5
    screen_box = plt.Rectangle((intake_x-1, intake_y-0.75), 2, 1.5, 
                               linewidth=2, edgecolor='black', 
                               facecolor=colors['process_block'], zorder=5)
    ax.add_artist(screen_box)
    ax.text(intake_x, intake_y, "Screening", ha='center', va='center', 
            fontweight='bold', color=colors['text'])
    ax.text(intake_x, intake_y-0.4, "Bar Screen", ha='center', va='center', 
            fontsize=10, color=colors['text'])
    
    # Raw sewage inlet
    draw_pipe(ax, (0, intake_y), (intake_x-1, intake_y))
    draw_flow_arrow(ax, 0.5, intake_y)
    ax.text(0.2, intake_y+0.3, "Raw\nInfluent", ha='center', va='bottom', 
            fontsize=10, color=colors['text'])
    
    # 2. Grit Removal
    grit_x, grit_y = 3.5, 5
    draw_tank(ax, grit_x, grit_y, 1.5, 1.5, fill_percent=0.6, label="Grit Chamber")
    
    # Connect screening to grit
    draw_pipe(ax, (intake_x+1, intake_y), (grit_x-0.75, grit_y))
    draw_flow_arrow(ax, intake_x+1.5, intake_y)
    
    # 3. Primary Clarifier
    primary_x, primary_y = 6, 5
    draw_tank(ax, primary_x, primary_y, 2, 2, fill_percent=0.7, label="Primary Clarifier")
    
    # Connect grit to primary
    draw_pipe(ax, (grit_x+0.75, grit_y), (primary_x-1, primary_y))
    draw_flow_arrow(ax, grit_x+1.5, grit_y)
    
    # 4. Aeration Basin
    aeration_x, aeration_y = 9, 5
    aeration_tank = draw_tank(ax, aeration_x, aeration_y, 2, 2.5, 
                              fill_percent=0.8, label="Aeration Basin")
    
    # Draw bubbles in aeration tank
    for i in range(10):
        bubble_x = aeration_x - 0.8 + np.random.rand() * 1.6
        bubble_y = aeration_y - 1 + np.random.rand() * 1.6
        bubble_size = 0.05 + np.random.rand() * 0.08
        bubble = plt.Circle((bubble_x, bubble_y), bubble_size, 
                           color='white', alpha=0.7, zorder=6)
        ax.add_artist(bubble)
    
    # Connect primary to aeration
    draw_pipe(ax, (primary_x+1, primary_y), (aeration_x-1, aeration_y))
    draw_flow_arrow(ax, primary_x+1.8, primary_y)
    
    # 5. Secondary Clarifier
    secondary_x, secondary_y = 12, 5
    draw_tank(ax, secondary_x, secondary_y, 2, 2, 
              fill_percent=0.6, label="Secondary Clarifier")
    
    # Connect aeration to secondary
    draw_pipe(ax, (aeration_x+1, aeration_y), (secondary_x-1, secondary_y))
    draw_flow_arrow(ax, aeration_x+1.8, aeration_y)
    
    # 6. Disinfection
    disinfect_x, disinfect_y = 14.5, 5
    disinfect_box = plt.Rectangle((disinfect_x-1, disinfect_y-0.75), 2, 1.5, 
                                 linewidth=2, edgecolor='black', 
                                 facecolor=colors['process_block'], zorder=5)
    ax.add_artist(disinfect_box)
    ax.text(disinfect_x, disinfect_y, "Disinfection", ha='center', va='center', 
            fontweight='bold', color=colors['text'])
    ax.text(disinfect_x, disinfect_y-0.4, "UV / Chlorine", ha='center', va='center', 
            fontsize=10, color=colors['text'])
    
    # Connect secondary to disinfection
    draw_pipe(ax, (secondary_x+1, secondary_y), (disinfect_x-1, disinfect_y))
    draw_flow_arrow(ax, secondary_x+1.8, secondary_y)
    
    # Effluent outlet
    draw_pipe(ax, (disinfect_x+1, disinfect_y), (16, disinfect_y))
    draw_flow_arrow(ax, disinfect_x+1.5, disinfect_y)
    ax.text(15.8, disinfect_y+0.3, "Treated\nEffluent", ha='center', va='bottom', 
            fontsize=10, color=colors['text'])
    
    # --- Sludge Handling ---
    # Primary sludge
    draw_pipe(ax, (primary_x, primary_y-1), (primary_x, primary_y-2.5), 
             width=0.07, color='#795548')
    draw_flow_arrow(ax, primary_x, primary_y-1.5, direction='down', color='#795548')
    ax.text(primary_x+0.3, primary_y-2, "Primary\nSludge", ha='left', va='center', 
            fontsize=10, color=colors['text'])
    
    # Secondary sludge
    draw_pipe(ax, (secondary_x, secondary_y-1), (secondary_x, secondary_y-2.5), 
             width=0.07, color='#795548')
    draw_flow_arrow(ax, secondary_x, secondary_y-1.5, direction='down', color='#795548')
    ax.text(secondary_x+0.3, secondary_y-2, "Secondary\nSludge", ha='left', va='center', 
            fontsize=10, color=colors['text'])
    
    # RAS - Return Activated Sludge
    draw_pipe(ax, (secondary_x, secondary_y-2.5), (secondary_x-1.5, secondary_y-2.5), 
             width=0.07, color='#795548')
    draw_pipe(ax, (secondary_x-1.5, secondary_y-2.5), (aeration_x, secondary_y-2.5), 
             width=0.07, color='#795548')
    draw_pipe(ax, (aeration_x, secondary_y-2.5), (aeration_x, aeration_y-1.25), 
             width=0.07, color='#795548')
    draw_flow_arrow(ax, aeration_x, aeration_y-2, direction='up', color='#795548')
    add_pump_symbol(ax, secondary_x-1, secondary_y-2.5, size=0.4, color='#795548')
    ax.text(aeration_x-0.3, secondary_y-2.8, "RAS", ha='right', va='center', 
            fontsize=10, color=colors['text'])
    
    # --- Add Equipment and Instrumentation ---
    
    # Influent pump
    add_pump_symbol(ax, 0.8, intake_y, size=0.4)
    
    # Flow meters
    add_sensor_symbol(ax, 0.4, intake_y+0.6, size=0.3, sensor_type='FT')
    add_sensor_symbol(ax, primary_x+1.5, primary_y+0.6, size=0.3, sensor_type='FT')
    add_sensor_symbol(ax, 15.5, disinfect_y+0.6, size=0.3, sensor_type='FT')
    
    # Valves
    add_valve_symbol(ax, grit_x+1.2, grit_y)
    add_valve_symbol(ax, aeration_x+1.2, aeration_y)
    add_valve_symbol(ax, secondary_x+1.2, secondary_y)
    
    # Level sensors
    add_sensor_symbol(ax, primary_x+0.7, primary_y+0.7, size=0.3, sensor_type='LT')
    add_sensor_symbol(ax, aeration_x+0.7, aeration_y+0.7, size=0.3, sensor_type='LT')
    add_sensor_symbol(ax, secondary_x+0.7, secondary_y+0.7, size=0.3, sensor_type='LT')
    
    # Analytical sensors
    add_sensor_symbol(ax, aeration_x+0.7, aeration_y-0.7, size=0.3, sensor_type='DO')
    add_sensor_symbol(ax, secondary_x+0.7, secondary_y-0.7, size=0.3, sensor_type='pH')
    add_sensor_symbol(ax, disinfect_x+0.7, disinfect_y+0.6, size=0.3, sensor_type='Cl')
    
    # Air supply to aeration basin
    air_x, air_y = aeration_x, aeration_y-2
    air_box = plt.Rectangle((air_x-0.75, air_y-0.5), 1.5, 1, 
                           linewidth=2, edgecolor='black', 
                           facecolor=colors['control_block'], zorder=5)
    ax.add_artist(air_box)
    ax.text(air_x, air_y, "Blowers", ha='center', va='center', 
            fontweight='bold', color=colors['text'])
    
    # Air pipes
    draw_pipe(ax, (air_x, air_y+0.5), (air_x, aeration_y-1.25), 
             width=0.08, color='#a9cce3')
    
    # Chemical dosing
    chem_x, chem_y = disinfect_x, disinfect_y-2
    chem_box = plt.Rectangle((chem_x-0.75, chem_y-0.5), 1.5, 1, 
                            linewidth=2, edgecolor='black', 
                            facecolor=colors['control_block'], zorder=5)
    ax.add_artist(chem_box)
    ax.text(chem_x, chem_y, "Chemical\nDosing", ha='center', va='center', 
            fontweight='bold', color=colors['text'])
    
    # Chemical pipes
    draw_pipe(ax, (chem_x, chem_y+0.5), (chem_x, disinfect_y-0.75), 
             width=0.05, color='#f1c40f')
    
    # Legend
    legend_x, legend_y = 8, 1.5
    legend_box = plt.Rectangle((legend_x-3.5, legend_y-1), 7, 2, 
                              linewidth=1, edgecolor='black', 
                              facecolor='white', alpha=0.7, zorder=20)
    ax.add_artist(legend_box)
    ax.text(legend_x, legend_y+0.8, "LEGEND", ha='center', fontweight='bold')
    
    # Legend items
    legend_items = [
        (draw_pipe, (legend_x-3, legend_y+0.4, legend_x-2, legend_y+0.4, 0.1, '#3498db'),
         "Water Flow"),
        (draw_pipe, (legend_x-3, legend_y+0.0, legend_x-2, legend_y+0.0, 0.07, '#795548'),
         "Sludge Flow"),
        (add_pump_symbol, (legend_x-2.5, legend_y-0.4, 0.3),
         "Pump"),
        (add_valve_symbol, (legend_x-2.5, legend_y-0.8, 0.3),
         "Valve"),
        
        (add_sensor_symbol, (legend_x+0.5, legend_y+0.4, 0.3, 'FT'),
         "Flow Transmitter"),
        (add_sensor_symbol, (legend_x+0.5, legend_y+0.0, 0.3, 'LT'),
         "Level Transmitter"),
        (add_sensor_symbol, (legend_x+0.5, legend_y-0.4, 0.3, 'pH'),
         "pH Analyzer"),
        (add_sensor_symbol, (legend_x+0.5, legend_y-0.8, 0.3, 'DO'),
         "DO Analyzer"),
    ]
    
    for i, (func, args, text) in enumerate(legend_items):
        x_pos = legend_x-3 + (i // 4) * 3.5
        y_pos = legend_y+0.4 - (i % 4) * 0.4
        func(ax, *args)
        ax.text(x_pos+0.7, y_pos, text, va='center', fontsize=10)
    
    # Save the diagram
    filepath = os.path.join(diagrams_dir, 'process_flow_diagram.png')
    fig.savefig(filepath, dpi=200, bbox_inches='tight')
    print(f"Process Flow Diagram saved to {filepath}")
    plt.close(fig)
    
    return filepath

def generate_control_system_architecture():
    """Generate a control system architecture diagram"""
    print("Generating Control System Architecture Diagram...")
    
    # Create figure and axis
    fig, ax = plt.subplots(figsize=(14, 10))
    fig.patch.set_facecolor(colors['background'])
    ax.set_facecolor(colors['background'])
    
    # Remove axes
    ax.set_axis_off()
    
    # Set plot limits
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    
    # Title
    ax.set_title('Wastewater Treatment Plant - Control System Architecture', 
                 fontsize=20, fontweight='bold', color=colors['heading'], pad=20)
    
    # Footer with date
    footer_text = f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    fig.text(0.98, 0.02, footer_text, ha='right', va='bottom', 
             fontsize=8, color=colors['text'])
    
    # Define colors for different network levels
    colors_network = {
        'enterprise': '#3498db',
        'control': '#2ecc71',
        'field': '#e67e22',
        'safety': '#e74c3c'
    }
    
    # Create a directed graph
    G = nx.DiGraph()
    
    # Add nodes for devices
    nodes = {
        # Enterprise level
        'reports': {'pos': (2, 9), 'label': 'Reporting\nServer', 'level': 'enterprise'},
        'business': {'pos': (5, 9), 'label': 'Business\nSystems', 'level': 'enterprise'},
        'remote': {'pos': (8, 9), 'label': 'Remote\nAccess', 'level': 'enterprise'},
        
        # Control level
        'scada': {'pos': (2, 7), 'label': 'SCADA\nServers', 'level': 'control'},
        'hmi1': {'pos': (4, 7), 'label': 'Operator\nWorkstation 1', 'level': 'control'},
        'hmi2': {'pos': (6, 7), 'label': 'Operator\nWorkstation 2', 'level': 'control'},
        'engineer': {'pos': (8, 7), 'label': 'Engineering\nWorkstation', 'level': 'control'},
        
        # PLC level
        'main_plc': {'pos': (5, 5), 'label': 'Main Process\nPLC', 'level': 'control'},
        'backup_plc': {'pos': (8, 5), 'label': 'Backup\nPLC', 'level': 'control'},
        'intake_plc': {'pos': (2, 5), 'label': 'Intake\nPLC', 'level': 'control'},
        
        # Remote I/O
        'rio1': {'pos': (1, 3), 'label': 'Remote I/O\nIntake', 'level': 'field'},
        'rio2': {'pos': (3, 3), 'label': 'Remote I/O\nPrimary', 'level': 'field'},
        'rio3': {'pos': (5, 3), 'label': 'Remote I/O\nAeration', 'level': 'field'},
        'rio4': {'pos': (7, 3), 'label': 'Remote I/O\nSecondary', 'level': 'field'},
        'rio5': {'pos': (9, 3), 'label': 'Remote I/O\nDisinfection', 'level': 'field'},
        
        # Field devices (grouped by area)
        'field1': {'pos': (1, 1), 'label': 'Intake\nField Devices', 'level': 'field'},
        'field2': {'pos': (3, 1), 'label': 'Primary\nField Devices', 'level': 'field'},
        'field3': {'pos': (5, 1), 'label': 'Aeration\nField Devices', 'level': 'field'},
        'field4': {'pos': (7, 1), 'label': 'Secondary\nField Devices', 'level': 'field'},
        'field5': {'pos': (9, 1), 'label': 'Disinfection\nField Devices', 'level': 'field'},
    }
    
    # Add nodes to graph
    for node, attrs in nodes.items():
        G.add_node(node, **attrs)
    
    # Add edges (connections)
    # Enterprise connections
    G.add_edge('scada', 'reports')
    G.add_edge('scada', 'business')
    G.add_edge('remote', 'scada')
    
    # Control network
    G.add_edge('scada', 'hmi1')
    G.add_edge('scada', 'hmi2')
    G.add_edge('scada', 'engineer')
    G.add_edge('scada', 'main_plc')
    G.add_edge('main_plc', 'backup_plc')
    G.add_edge('main_plc', 'intake_plc')
    
    # Field network
    G.add_edge('intake_plc', 'rio1')
    G.add_edge('main_plc', 'rio2')
    G.add_edge('main_plc', 'rio3')
    G.add_edge('main_plc', 'rio4')
    G.add_edge('main_plc', 'rio5')
    
    # Field devices
    G.add_edge('rio1', 'field1')
    G.add_edge('rio2', 'field2')
    G.add_edge('rio3', 'field3')
    G.add_edge('rio4', 'field4')
    G.add_edge('rio5', 'field5')
    
    # Draw network zones
    zone_rects = {
        'enterprise': {'y': 8.5, 'height': 1.5, 'color': colors_network['enterprise'], 'label': 'Enterprise Network'},
        'control': {'y': 5.5, 'height': 2.5, 'color': colors_network['control'], 'label': 'Control Network'},
        'field': {'y': 1.5, 'height': 3.0, 'color': colors_network['field'], 'label': 'Field Network'},
    }
    
    for zone, attrs in zone_rects.items():
        rect = plt.Rectangle((0.5, attrs['y']-0.5), 9, attrs['height'], 
                            alpha=0.2, fc=attrs['color'], ec=attrs['color'])
        ax.add_patch(rect)
        ax.text(0.6, attrs['y']+attrs['height']-0.7, attrs['label'], 
                fontsize=12, fontweight='bold', color=attrs['color'])
    
    # Draw nodes
    for node, attrs in nodes.items():
        x, y = attrs['pos']
        level = attrs['level']
        label = attrs['label']
        
        # Create node
        node_width, node_height = 1, 0.8
        rect = plt.Rectangle((x-node_width/2, y-node_height/2), 
                            node_width, node_height,
                            fc='white', ec=colors_network[level], 
                            lw=2, alpha=0.9, zorder=10)
        ax.add_patch(rect)
        
        # Add label
        ax.text(x, y, label, ha='center', va='center', fontsize=9, 
                fontweight='bold', color=colors['text'], zorder=11)
    
    # Draw edges
    for u, v in G.edges():
        x1, y1 = nodes[u]['pos']
        x2, y2 = nodes[v]['pos']
        level1 = nodes[u]['level']
        level2 = nodes[v]['level']
        
        # Color based on source level
        edge_color = colors_network[level1]
        
        # Draw connection
        ax.arrow(x1, y1+0.4, 
                x2-x1, y2-y1-0.4, 
                head_width=0.1, head_length=0.1, 
                fc=edge_color, ec=edge_color, 
                length_includes_head=True,
                linestyle='-', linewidth=1.5,
                zorder=5)
    
    # Add a firewall symbol between enterprise and control network
    firewall_y = 8.5
    firewall_width = 9
    
    # Draw firewall brick pattern
    brick_height = 0.15
    for i in range(int(firewall_width)):
        offset = 0 if i % 2 == 0 else 0.5
        for j in range(2):
            brick_x = 0.5 + i + offset
            if brick_x + 1 <= firewall_width + 0.5:
                brick = plt.Rectangle((brick_x, firewall_y - j*brick_height), 
                                    1, brick_height,
                                    fc='#e74c3c', ec='white', 
                                    lw=1, alpha=0.7, zorder=20)
                ax.add_patch(brick)
    
    # Add firewall label
    ax.text(5, firewall_y, 'FIREWALL', ha='center', va='center', 
            color='white', fontweight='bold', zorder=21)
    
    # Add legend
    legend_x, legend_y = 5, 0.5
    # Create legend box
    legend_box = plt.Rectangle((legend_x-4, legend_y-0.3), 8, 0.6, 
                             fc='white', ec='black', alpha=0.7)
    ax.add_patch(legend_box)
    
    # Legend items
    legend_items = [
        (colors_network['enterprise'], 'Enterprise Network'),
        (colors_network['control'], 'Control Network'),
        (colors_network['field'], 'Field Network'),
    ]
    
    # Add legend items
    for i, (color, label) in enumerate(legend_items):
        x_offset = i * 2.5
        rect = plt.Rectangle((legend_x-3.5+x_offset, legend_y), 0.3, 0.3, 
                           fc=color, ec=color)
        ax.add_patch(rect)
        ax.text(legend_x-3.0+x_offset, legend_y+0.15, label, 
                va='center', fontsize=10)
    
    # Save the diagram
    filepath = os.path.join(diagrams_dir, 'control_system_architecture.png')
    fig.savefig(filepath, dpi=200, bbox_inches='tight')
    print(f"Control System Architecture Diagram saved to {filepath}")
    plt.close(fig)
    
    return filepath

def generate_io_diagram():
    """Generate an I/O connection diagram"""
    print("Generating I/O Connection Diagram...")
    
    # Create figure and axis
    fig, ax = plt.subplots(figsize=(14, 10))
    fig.patch.set_facecolor(colors['background'])
    ax.set_facecolor(colors['background'])
    
    # Remove axes
    ax.set_axis_off()
    
    # Set plot limits
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    
    # Title
    ax.set_title('Wastewater Treatment Plant - I/O Connection Diagram', 
                 fontsize=20, fontweight='bold', color=colors['heading'], pad=20)
    
    # Footer with date
    footer_text = f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    fig.text(0.98, 0.02, footer_text, ha='right', va='bottom', 
             fontsize=8, color=colors['text'])
    
    # Draw PLC
    plc_x, plc_y = 5, 8
    plc_width, plc_height = 4, 1.5
    plc = plt.Rectangle((plc_x-plc_width/2, plc_y-plc_height/2), 
                        plc_width, plc_height,
                        linewidth=2, edgecolor='black', 
                        facecolor='#d6eaf8', zorder=10)
    ax.add_artist(plc)
    
    # PLC label
    ax.text(plc_x, plc_y+0.1, "Main Process PLC", ha='center', va='center', 
            fontweight='bold', fontsize=14, color=colors['text'])
    ax.text(plc_x, plc_y-0.3, "Siemens S7-1500", ha='center', va='center', 
            fontsize=12, color=colors['text'])
    
    # Draw I/O racks
    io_modules = [
        {"x": 1.5, "y": 6, "type": "DI", "channels": 32, "label": "Digital Inputs"},
        {"x": 3.0, "y": 6, "type": "DO", "channels": 32, "label": "Digital Outputs"},
        {"x": 4.5, "y": 6, "type": "AI", "channels": 16, "label": "Analog Inputs"},
        {"x": 6.0, "y": 6, "type": "AO", "channels": 8, "label": "Analog Outputs"},
        {"x": 7.5, "y": 6, "type": "COM", "channels": 0, "label": "Communication"}
    ]
    
    for module in io_modules:
        mod_x, mod_y = module["x"], module["y"]
        mod_type = module["type"]
        mod_width, mod_height = 1.0, 1.5
        
        # Color based on module type
        if mod_type == "DI":
            color = "#3498db"
        elif mod_type == "DO":
            color = "#2ecc71"
        elif mod_type == "AI":
            color = "#e67e22"
        elif mod_type == "AO":
            color = "#9b59b6"
        else:
            color = "#7f8c8d"
        
        # Draw module
        mod = plt.Rectangle((mod_x-mod_width/2, mod_y-mod_height/2), 
                           mod_width, mod_height,
                           linewidth=2, edgecolor='black', 
                           facecolor=color, alpha=0.7, zorder=10)
        ax.add_artist(mod)
        
        # Module label
        ax.text(mod_x, mod_y+0.4, module["type"], ha='center', va='center', 
                fontweight='bold', fontsize=12, color='white')
        
        # Channel count
        if module["channels"] > 0:
            ax.text(mod_x, mod_y, f"{module['channels']} ch", ha='center', va='center', 
                    fontsize=11, color='white')
        
        # Module name
        ax.text(mod_x, mod_y-0.6, module["label"], ha='center', va='top', 
                fontsize=10, color='white')
    
    # Connect PLC to modules
    for module in io_modules:
        mod_x, mod_y = module["x"], module["y"]
        # Draw connection line
        plt.plot([mod_x, mod_x], [mod_y+0.75, plc_y-0.75], 
                color='black', linestyle='--', linewidth=1, zorder=5)
    
    # Draw field devices
    field_devices = [
        {"x": 1.0, "y": 4, "type": "Limit Switch", "signal": "DI", "tag": "ZS-101", "desc": "Screen Upper Limit"},
        {"x": 1.5, "y": 4, "type": "Limit Switch", "signal": "DI", "tag": "ZS-102", "desc": "Screen Lower Limit"},
        {"x": 2.0, "y": 4, "type": "Motor Status", "signal": "DI", "tag": "HS-103", "desc": "Screen Motor Running"},
        
        {"x": 2.5, "y": 3, "type": "Solenoid Valve", "signal": "DO", "tag": "XV-101", "desc": "Grit Valve"},
        {"x": 3.0, "y": 3, "type": "Motor Control", "signal": "DO", "tag": "HS-201", "desc": "Primary Sludge Pump"},
        {"x": 3.5, "y": 3, "type": "Alarm Light", "signal": "DO", "tag": "XA-301", "desc": "High Level Alarm"},
        
        {"x": 4.0, "y": 4, "type": "Level Transmitter", "signal": "AI", "tag": "LIT-101", "desc": "Primary Tank Level"},
        {"x": 4.5, "y": 4, "type": "Flow Meter", "signal": "AI", "tag": "FIT-201", "desc": "Influent Flow"},
        {"x": 5.0, "y": 4, "type": "pH Analyzer", "signal": "AI", "tag": "AIT-301", "desc": "Aeration pH"},
        
        {"x": 5.5, "y": 3, "type": "Control Valve", "signal": "AO", "tag": "FCV-101", "desc": "Chemical Dosing"},
        {"x": 6.0, "y": 3, "type": "VFD Control", "signal": "AO", "tag": "SIC-201", "desc": "Blower Speed"},
        
        {"x": 6.5, "y": 4, "type": "Radar Level", "signal": "AI", "tag": "LIT-401", "desc": "Secondary Tank Level"},
        {"x": 7.0, "y": 4, "type": "DO Analyzer", "signal": "AI", "tag": "AIT-401", "desc": "Dissolved Oxygen"},
        
        {"x": 7.5, "y": 3, "type": "Modbus Device", "signal": "COM", "tag": "UV-101", "desc": "UV Disinfection System"},
        {"x": 8.0, "y": 3, "type": "Profibus Device", "signal": "COM", "tag": "MCT-201", "desc": "Motor Control Center"}
    ]
    
    # Draw field devices
    for device in field_devices:
        dev_x, dev_y = device["x"], device["y"]
        dev_type = device["type"]
        dev_signal = device["signal"]
        
        # Color based on signal type
        if dev_signal == "DI":
            color = "#3498db"
        elif dev_signal == "DO":
            color = "#2ecc71"
        elif dev_signal == "AI":
            color = "#e67e22"
        elif dev_signal == "AO":
            color = "#9b59b6"
        else:
            color = "#7f8c8d"
        
        # Draw device
        dev_width, dev_height = 0.8, 0.6
        dev = plt.Rectangle((dev_x-dev_width/2, dev_y-dev_height/2), 
                           dev_width, dev_height,
                           linewidth=1, edgecolor='black', 
                           facecolor=color, alpha=0.5, zorder=10)
        ax.add_artist(dev)
        
        # Device tag
        ax.text(dev_x, dev_y, device["tag"], ha='center', va='center', 
                fontsize=9, color=colors['text'])
        
        # Device description
        ax.text(dev_x, dev_y-0.5, device["type"], ha='center', va='top', 
                fontsize=8, color=colors['text'])
        
        # Connect to appropriate module
        if dev_signal == "DI":
            target_x = 1.5
        elif dev_signal == "DO":
            target_x = 3.0
        elif dev_signal == "AI":
            target_x = 4.5
        elif dev_signal == "AO":
            target_x = 6.0
        else:
            target_x = 7.5
        
        # Draw connection line
        plt.plot([dev_x, target_x], [dev_y+0.3, 6-0.75], 
                color=color, linestyle='-', linewidth=0.5, alpha=0.5, zorder=5)
    
    # Add terminal blocks
    term_y = 5
    for x in [1.5, 3.0, 4.5, 6.0, 7.5]:
        term_width, term_height = 0.8, 0.3
        term = plt.Rectangle((x-term_width/2, term_y-term_height/2), 
                            term_width, term_height,
                            linewidth=1, edgecolor='black', 
                            facecolor='#f8f9fa', zorder=10)
        ax.add_artist(term)
        
        # Terminal block label
        ax.text(x, term_y, "TB-"+str(int(x*10)), ha='center', va='center', 
                fontsize=8, color=colors['text'])
        
        # Connect to I/O module
        plt.plot([x, x], [term_y+term_height/2, 6-0.75], 
                color='black', linestyle='-', linewidth=1, zorder=6)
    
    # Add a field junction box
    jb_x, jb_y = 8, 4
    jb_width, jb_height = 1.2, 0.8
    jb = plt.Rectangle((jb_x-jb_width/2, jb_y-jb_height/2), 
                      jb_width, jb_height,
                      linewidth=2, edgecolor='black', 
                      facecolor='#d6eaf8', zorder=10)
    ax.add_artist(jb)
    
    # Junction box label
    ax.text(jb_x, jb_y, "Junction Box\nJB-101", ha='center', va='center', 
            fontsize=10, color=colors['text'])
    
    # Connect to I/O module
    plt.plot([jb_x, 7.5], [jb_y, 6-0.75], 
            color='black', linestyle='-', linewidth=1, zorder=6)
    
    # Add power supply
    ps_x, ps_y = 9, 6
    ps_width, ps_height = 1.0, 1.5
    ps = plt.Rectangle((ps_x-ps_width/2, ps_y-ps_height/2), 
                      ps_width, ps_height,
                      linewidth=2, edgecolor='black', 
                      facecolor='#f1c40f', alpha=0.7, zorder=10)
    ax.add_artist(ps)
    
    # Power supply label
    ax.text(ps_x, ps_y+0.4, "24VDC", ha='center', va='center', 
            fontweight='bold', fontsize=12, color=colors['text'])
    ax.text(ps_x, ps_y, "Power Supply", ha='center', va='center', 
            fontsize=10, color=colors['text'])
    
    # Connect power supply to PLC
    plt.plot([ps_x, plc_x+plc_width/2], [ps_y, ps_y], 
            color='red', linestyle='-', linewidth=2, zorder=6)
    
    # Add field cable tray
    tray_y = 2.5
    tray = plt.Rectangle((0.5, tray_y-0.1), 
                        9, 0.2,
                        linewidth=2, edgecolor='gray', 
                        facecolor='lightgray', zorder=5)
    ax.add_artist(tray)
    
    # Field cable tray label
    ax.text(5, tray_y-0.3, "Field Cable Tray", ha='center', va='top', 
            fontsize=10, color=colors['text'])
    
    # Add legend
    legend_x, legend_y = 5, 1.5
    # Create legend box
    legend_box = plt.Rectangle((legend_x-4, legend_y-0.8), 8, 1.6, 
                             fc='white', ec='black', alpha=0.7)
    ax.add_patch(legend_box)
    
    ax.text(legend_x, legend_y+0.6, "I/O WIRING LEGEND", ha='center', 
            fontweight='bold', fontsize=12)
    
    # Legend items
    legend_items = [
        (plt.Rectangle((0, 0), 1, 1, fc="#3498db", alpha=0.7), "Digital Input (DI)"),
        (plt.Rectangle((0, 0), 1, 1, fc="#2ecc71", alpha=0.7), "Digital Output (DO)"),
        (plt.Rectangle((0, 0), 1, 1, fc="#e67e22", alpha=0.7), "Analog Input (AI)"),
        (plt.Rectangle((0, 0), 1, 1, fc="#9b59b6", alpha=0.7), "Analog Output (AO)"),
        (plt.Rectangle((0, 0), 1, 1, fc="#7f8c8d", alpha=0.7), "Communication")
    ]
    
    # Add legend items in a grid (3x2)
    for i, (patch, label) in enumerate(legend_items):
        row, col = divmod(i, 3)
        x_pos = legend_x - 3 + col * 2.5
        y_pos = legend_y + 0.2 - row * 0.5
        
        legend_patch = plt.Rectangle((x_pos, y_pos), 0.3, 0.3, 
                                   fc=patch.get_facecolor(), 
                                   ec=patch.get_edgecolor(),
                                   alpha=patch.get_alpha())
        ax.add_patch(legend_patch)
        ax.text(x_pos + 0.4, y_pos + 0.15, label, va='center', fontsize=10)
    
    # Add notes
    ax.text(1, 9, "Notes:", ha='left', fontweight='bold', fontsize=10)
    ax.text(1, 8.7, "1. All field wiring to be 18AWG minimum.", ha='left', fontsize=9)
    ax.text(1, 8.5, "2. Analog signals: 4-20mA unless specified otherwise.", ha='left', fontsize=9)
    ax.text(1, 8.3, "3. All shielded cables to be grounded at PLC end only.", ha='left', fontsize=9)
    
    # Save the diagram
    filepath = os.path.join(diagrams_dir, 'io_connection_diagram.png')
    fig.savefig(filepath, dpi=200, bbox_inches='tight')
    print(f"I/O Connection Diagram saved to {filepath}")
    plt.close(fig)
    
    return filepath

def main():
    """Main function to generate all diagrams"""
    # Ensure output directory exists
    if not os.path.exists(diagrams_dir):
        os.makedirs(diagrams_dir)
    
    # Generate diagrams
    process_diagram_path = generate_process_flow_diagram()
    architecture_diagram_path = generate_control_system_architecture()
    io_diagram_path = generate_io_diagram()
    
    # Print summary
    print("\nDiagram Generation Complete!")
    print(f"Process Flow Diagram: {process_diagram_path}")
    print(f"Control System Architecture: {architecture_diagram_path}")
    print(f"I/O Connection Diagram: {io_diagram_path}")

if __name__ == "__main__":
    main()
