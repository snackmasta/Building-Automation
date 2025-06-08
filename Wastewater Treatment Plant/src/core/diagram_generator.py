#!/usr/bin/env python3
# Wastewater Treatment Plant - Diagram Generator
# Creates professional system diagrams for documentation purposes

import os
import sys
import argparse
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.path as mpath
import numpy as np
from matplotlib.colors import LinearSegmentedColormap
import networkx as nx
from pathlib import Path

# Ensure diagrams directory exists
SCRIPT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DIAGRAMS_DIR = os.path.join(SCRIPT_DIR, "diagrams")
os.makedirs(DIAGRAMS_DIR, exist_ok=True)

# Define diagram generation functions
def generate_treatment_control_flowchart():
    """Generate treatment control logic flowchart"""
    print("Generating Treatment Control Flowchart...")
    
    plt.figure(figsize=(12, 16))
    
    # Create directed graph
    G = nx.DiGraph()
    
    # Define nodes
    nodes = [
        "Start", 
        "System Init", 
        "Check Mode",
        "Auto Mode", 
        "Manual Mode",
        "Storm Mode",
        "Check Sensors",
        "Pre-treatment",
        "Primary Treatment",
        "Secondary Treatment",
        "Tertiary Treatment",
        "Disinfection",
        "Quality Check",
        "Quality OK?",
        "Discharge",
        "Recirculate",
        "End"
    ]
    
    # Add nodes
    for i, node in enumerate(nodes):
        G.add_node(node, pos=(i % 5, -(i // 5)))
    
    # Special node positions
    pos = nx.get_node_attributes(G, 'pos')
    pos["Start"] = (2, 0)
    pos["End"] = (2, -8)
    pos["Quality OK?"] = (2, -6)
    pos["Discharge"] = (3.5, -7)
    pos["Recirculate"] = (0.5, -7)
    
    # Add edges
    G.add_edge("Start", "System Init")
    G.add_edge("System Init", "Check Mode")
    G.add_edge("Check Mode", "Auto Mode")
    G.add_edge("Check Mode", "Manual Mode")
    G.add_edge("Check Mode", "Storm Mode")
    G.add_edge("Auto Mode", "Check Sensors")
    G.add_edge("Manual Mode", "Check Sensors")
    G.add_edge("Storm Mode", "Check Sensors")
    G.add_edge("Check Sensors", "Pre-treatment")
    G.add_edge("Pre-treatment", "Primary Treatment")
    G.add_edge("Primary Treatment", "Secondary Treatment")
    G.add_edge("Secondary Treatment", "Tertiary Treatment")
    G.add_edge("Tertiary Treatment", "Disinfection")
    G.add_edge("Disinfection", "Quality Check")
    G.add_edge("Quality Check", "Quality OK?")
    G.add_edge("Quality OK?", "Discharge")
    G.add_edge("Quality OK?", "Recirculate")
    G.add_edge("Discharge", "End")
    G.add_edge("Recirculate", "Primary Treatment")
    
    # Node colors
    color_map = []
    for node in G:
        if node == "Start" or node == "End":
            color_map.append('#1f78b4')  # Blue
        elif "Mode" in node:
            color_map.append('#33a02c')  # Green
        elif "Check" in node or "Quality" in node:
            color_map.append('#ff7f00')  # Orange
        elif "Treatment" in node or "Disinfection" in node:
            color_map.append('#e31a1c')  # Red
        else:
            color_map.append('#6a3d9a')  # Purple
    
    # Draw the graph
    plt.title("Wastewater Treatment Control Flowchart", fontsize=18, pad=20)
    nx.draw(G, pos, with_labels=True, node_size=3000, node_color=color_map, 
            font_size=10, font_color='white', font_weight='bold', 
            arrowsize=20, edge_color='gray')
    
    # Save diagram
    filepath = os.path.join(DIAGRAMS_DIR, "treatment_control_flowchart.png")
    plt.savefig(filepath, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved flowchart to {filepath}")
    return filepath

def generate_system_layout_diagram():
    """Generate physical layout diagram of the wastewater treatment plant"""
    print("Generating System Layout Diagram...")
    
    plt.figure(figsize=(14, 8))
    plt.grid(False)
    
    # Background color
    ax = plt.gca()
    ax.set_facecolor("#f2f2f2")
    
    # Define equipment colors
    colors = {
        'tank': '#AED6F1',
        'pipe': '#85929E',
        'pump': '#E74C3C',
        'filter': '#F5B041',
        'blower': '#58D68D',
        'chemical': '#BB8FCE',
        'mixing': '#5D6D7E',
        'uv': '#F7DC6F'
    }
    
    # Draw intake system
    plt.fill([0.5, 2, 2, 0.5], [1, 1, 3, 3], color=colors['tank'], alpha=0.7)
    plt.text(1.25, 2, "Inlet\nScreen", ha='center', va='center', fontsize=10)
    
    # Draw primary treatment
    plt.fill([3, 5, 5, 3], [1, 1, 4, 4], color=colors['tank'], alpha=0.9)
    plt.text(4, 2.5, "Primary\nSettling\nTank", ha='center', va='center', fontsize=12)
    
    # Draw aeration tank
    plt.fill([6, 10, 10, 6], [1, 1, 4, 4], color=colors['tank'], alpha=0.8)
    plt.text(8, 2.5, "Aeration\nBasin", ha='center', va='center', fontsize=12)
    
    # Draw secondary clarifier
    circle = plt.Circle((12, 2.5), 1.5, color=colors['tank'], alpha=0.8)
    ax.add_artist(circle)
    plt.text(12, 2.5, "Secondary\nClarifier", ha='center', va='center', fontsize=10)
    
    # Draw tertiary treatment
    plt.fill([14, 16, 16, 14], [2, 2, 3, 3], color=colors['filter'], alpha=0.9)
    plt.text(15, 2.5, "Filters", ha='center', va='center', fontsize=10)
    
    # Draw disinfection
    plt.fill([17, 19, 19, 17], [2, 2, 3, 3], color=colors['uv'], alpha=0.7)
    plt.text(18, 2.5, "UV\nDisinfection", ha='center', va='center', fontsize=10)
    
    # Draw outlet
    plt.fill([20, 21, 21, 20], [2, 2, 3, 3], color='#AED6F1', alpha=0.7)
    plt.text(20.5, 2.5, "Outlet", ha='center', va='center', fontsize=10)
    
    # Draw sludge handling
    plt.fill([3, 5, 5, 3], [6, 6, 7, 7], color='#7F8C8D', alpha=0.7)
    plt.text(4, 6.5, "Sludge\nHandling", ha='center', va='center', fontsize=10)
    
    plt.fill([10, 12, 12, 10], [5, 5, 6, 6], color='#7F8C8D', alpha=0.7)
    plt.text(11, 5.5, "Sludge\nHandling", ha='center', va='center', fontsize=10)
    
    # Draw connecting pipes
    plt.plot([2, 3], [2, 2.5], color=colors['pipe'], linewidth=3)
    plt.plot([5, 6], [2.5, 2.5], color=colors['pipe'], linewidth=3)
    plt.plot([10, 10.5], [2.5, 2.5], color=colors['pipe'], linewidth=3)
    plt.plot([13.5, 14], [2.5, 2.5], color=colors['pipe'], linewidth=3)
    plt.plot([16, 17], [2.5, 2.5], color=colors['pipe'], linewidth=3)
    plt.plot([19, 20], [2.5, 2.5], color=colors['pipe'], linewidth=3)
    
    # Draw sludge pipes
    plt.plot([4, 4], [4, 6], color=colors['pipe'], linewidth=2, linestyle='--')
    plt.plot([12, 11], [1.5, 5], color=colors['pipe'], linewidth=2, linestyle='--')
    
    # Draw pumps
    def draw_pump(x, y):
        circle = plt.Circle((x, y), 0.25, color=colors['pump'])
        ax.add_artist(circle)
        plt.plot([x-0.35, x+0.35], [y-0.35, y+0.35], color='white', linewidth=2)
        plt.plot([x-0.35, x+0.35], [y+0.35, y-0.35], color='white', linewidth=2)
    
    draw_pump(2.5, 2.5)
    draw_pump(5.5, 2.5)
    draw_pump(13, 2.5)
    draw_pump(4, 5)
    draw_pump(11, 4.5)
    
    # Draw blowers for aeration
    def draw_blower(x, y):
        rect = plt.Rectangle((x-0.3, y-0.3), 0.6, 0.6, color=colors['blower'])
        ax.add_artist(rect)
        plt.plot([x, x], [y+0.3, y+0.6], color=colors['pipe'], linewidth=2)
        plt.plot([x-0.3, x+0.3], [y, y], color='white', linewidth=2)
    
    draw_blower(7, 1)
    draw_blower(8, 1)
    draw_blower(9, 1)
    
    # Draw chemical dosing points
    def draw_chemical(x, y):
        triangle = plt.Polygon([[x, y+0.3], [x-0.3, y-0.3], [x+0.3, y-0.3]], 
                               color=colors['chemical'])
        ax.add_artist(triangle)
    
    draw_chemical(4, 0.5)  # pH adjustment
    draw_chemical(19.5, 1.5)  # Chlorine
    
    # Draw legend
    legend_items = [
        mpatches.Patch(color=colors['tank'], label='Tanks/Basins'),
        mpatches.Patch(color=colors['pipe'], label='Piping'),
        mpatches.Patch(color=colors['pump'], label='Pumps'),
        mpatches.Patch(color=colors['filter'], label='Filtration'),
        mpatches.Patch(color=colors['blower'], label='Blowers'),
        mpatches.Patch(color=colors['chemical'], label='Chemical Dosing'),
        mpatches.Patch(color=colors['uv'], label='UV Disinfection'),
        mpatches.Patch(color='#7F8C8D', label='Sludge Handling')
    ]
    
    plt.legend(handles=legend_items, loc='upper center', 
              bbox_to_anchor=(0.5, 1.05), ncol=4)
    
    # Set axis limits and remove ticks
    plt.xlim(0, 22)
    plt.ylim(0, 8)
    plt.axis('off')
    
    plt.title('Wastewater Treatment Plant - System Layout', fontsize=16, pad=20)
    
    # Save diagram
    filepath = os.path.join(DIAGRAMS_DIR, "system_layout_diagram.png")
    plt.savefig(filepath, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved system layout to {filepath}")
    return filepath

def generate_pid_diagram():
    """Generate P&ID (Piping and Instrumentation Diagram)"""
    print("Generating P&ID Diagram...")
    
    plt.figure(figsize=(14, 10))
    
    # Set background color
    ax = plt.gca()
    ax.set_facecolor("#f8f9fa")
    
    # Define equipment colors and styles
    colors = {
        'tank': '#d6eaf8',
        'border': '#2874a6',
        'pipe_main': '#34495e',
        'pipe_secondary': '#7f8c8d',
        'instrument': '#f5b041',
        'valve': '#e74c3c',
        'pump': '#2ecc71',
        'text': '#000000'
    }
    
    # Define P&ID symbols
    def draw_tank(x, y, width, height, name, tag):
        # Draw tank
        rect = plt.Rectangle((x, y), width, height, facecolor=colors['tank'], 
                            edgecolor=colors['border'], linewidth=2)
        ax.add_patch(rect)
        
        # Label
        plt.text(x + width/2, y - 0.2, name, 
                horizontalalignment='center', fontsize=10, color=colors['text'])
        plt.text(x + width/2, y + height + 0.1, tag, 
                horizontalalignment='center', fontsize=8, color=colors['text'])
    
    def draw_pump(x, y, rotation, name, tag):
        # Draw pump symbol (circle with triangle)
        circle = plt.Circle((x, y), 0.3, facecolor='white', 
                           edgecolor=colors['border'], linewidth=2)
        ax.add_patch(circle)
        
        if rotation == 0:  # Horizontal right
            triangle = plt.Polygon([[x+0.3, y], [x-0.1, y+0.2], [x-0.1, y-0.2]], 
                                  facecolor='white', edgecolor=colors['border'], linewidth=2)
        elif rotation == 180:  # Horizontal left
            triangle = plt.Polygon([[x-0.3, y], [x+0.1, y+0.2], [x+0.1, y-0.2]], 
                                  facecolor='white', edgecolor=colors['border'], linewidth=2)
        ax.add_patch(triangle)
        
        # Label
        plt.text(x, y - 0.5, name, horizontalalignment='center', 
                fontsize=8, color=colors['text'])
        plt.text(x, y + 0.5, tag, horizontalalignment='center', 
                fontsize=8, color=colors['text'])
    
    def draw_valve(x, y, rotation, tag):
        # Draw valve symbol
        if rotation == 0:  # Horizontal
            plt.plot([x-0.2, x+0.2], [y, y], color=colors['border'], linewidth=2)
            plt.plot([x, x], [y-0.2, y+0.2], color=colors['border'], linewidth=2)
        else:  # Vertical
            plt.plot([x, x], [y-0.2, y+0.2], color=colors['border'], linewidth=2)
            plt.plot([x-0.2, x+0.2], [y, y], color=colors['border'], linewidth=2)
        
        circle = plt.Circle((x, y), 0.25, facecolor='none', 
                           edgecolor=colors['border'], linewidth=2)
        ax.add_patch(circle)
        
        # Label
        plt.text(x, y - 0.35, tag, horizontalalignment='center', 
                fontsize=7, color=colors['text'])
    
    def draw_instrument(x, y, tag, description=""):
        # Draw instrument circle
        circle = plt.Circle((x, y), 0.25, facecolor='white', 
                           edgecolor=colors['border'], linewidth=1.5)
        ax.add_patch(circle)
        
        # Label inside
        plt.text(x, y, tag, horizontalalignment='center', 
                fontsize=7, color=colors['text'])
        
        # Description
        if description:
            plt.text(x, y - 0.4, description, horizontalalignment='center', 
                    fontsize=6, color=colors['text'])
    
    # Draw main tanks
    draw_tank(1, 2, 1.5, 2, "Inlet Chamber", "T-100")
    draw_tank(4, 2, 2, 3, "Primary Settling", "T-101")
    draw_tank(8, 2, 3, 3, "Aeration Basin", "T-102")
    draw_tank(13, 2, 2, 2, "Secondary Clarifier", "T-103")
    draw_tank(17, 2, 1.5, 1, "Filtration", "F-100")
    draw_tank(20, 2, 1, 1, "Disinfection", "D-100")
    
    # Draw pumps
    draw_pump(3, 3, 0, "Inlet Pump", "P-101")
    draw_pump(7, 3, 0, "Transfer Pump", "P-102")
    draw_pump(16, 3, 0, "Tertiary Pump", "P-103")
    draw_pump(5, 6, 180, "Sludge Pump", "P-104")
    
    # Draw main process line
    plt.plot([2.5, 3, 4], [3, 3, 3], color=colors['pipe_main'], linewidth=3)
    plt.plot([6, 7, 8], [3, 3, 3], color=colors['pipe_main'], linewidth=3)
    plt.plot([11, 13], [3, 3], color=colors['pipe_main'], linewidth=3)
    plt.plot([15, 16, 17], [3, 3, 3], color=colors['pipe_main'], linewidth=3)
    plt.plot([18.5, 20], [3, 3], color=colors['pipe_main'], linewidth=3)
    plt.plot([21, 22], [3, 3], color=colors['pipe_main'], linewidth=3)
    plt.text(22, 3, "→ Outlet", fontsize=10)
    
    # Draw sludge lines
    plt.plot([5, 5, 6], [2, 1, 1], color=colors['pipe_secondary'], 
            linewidth=2, linestyle='--')
    plt.plot([5, 5], [5, 6], color=colors['pipe_secondary'], 
            linewidth=2, linestyle='--')
    plt.plot([14, 14, 6], [2, 1, 1], color=colors['pipe_secondary'], 
            linewidth=2, linestyle='--')
    plt.text(6, 0.7, "To Sludge\nTreatment", fontsize=8, ha='center')
    
    # Draw valves
    draw_valve(2.5, 3, 0, "FV-101")
    draw_valve(4, 1, 90, "FV-102")
    draw_valve(6, 3, 0, "FV-103")
    draw_valve(14, 1, 90, "FV-104")
    draw_valve(18.5, 3, 0, "FV-105")
    draw_valve(21, 3, 0, "FV-106")
    
    # Draw instruments
    draw_instrument(1.5, 4.5, "FIT\n101", "Flow")
    draw_instrument(5, 5.3, "LIT\n101", "Level")
    draw_instrument(9.5, 5.5, "AT\n101", "DO")
    draw_instrument(9.5, 6.3, "AIT\n102", "pH")
    draw_instrument(14, 4.5, "LIT\n102", "Level")
    draw_instrument(21.5, 4.5, "QIT\n101", "Quality")
    
    # Draw chemical dosing points
    def draw_chemical_dosing(x, y, name):
        plt.scatter(x, y, marker='v', s=100, 
                   facecolor='white', edgecolor=colors['border'], linewidth=1.5)
        plt.text(x, y-0.4, name, fontsize=8, ha='center')
    
    draw_chemical_dosing(4.5, 4, "NaOH/HCl")
    draw_chemical_dosing(19.5, 3.5, "Cl₂")
    
    # Draw blowers
    def draw_blower(x, y, tag):
        rect = plt.Rectangle((x-0.3, y-0.3), 0.6, 0.6, facecolor='white', 
                            edgecolor=colors['border'], linewidth=1.5)
        ax.add_patch(rect)
        plt.text(x, y, "M", fontsize=8, ha='center')
        plt.text(x, y-0.5, tag, fontsize=8, ha='center')
    
    draw_blower(9, 1, "B-101")
    draw_blower(10, 1, "B-102")
    
    # Add aerator connections
    for x in range(8, 11):
        plt.plot([x+0.5, x+0.5], [1.3, 2], color=colors['pipe_secondary'], linewidth=1.5)
    
    # Add title and border
    plt.title('Wastewater Treatment Plant - P&ID Diagram', fontsize=16, pad=20)
    plt.grid(False)
    plt.xlim(0, 23)
    plt.ylim(0, 8)
    plt.axis('off')
    
    # Draw border
    border = plt.Rectangle((0.5, 0.5), 22, 7, fill=False, 
                          edgecolor='black', linewidth=1, linestyle='-')
    ax.add_patch(border)
    
    # Add text boxes for project details
    plt.text(1, 7.3, "Wastewater Treatment Plant", fontsize=14, weight='bold')
    plt.text(1, 6.8, "P&ID Diagram", fontsize=12)
    plt.text(22, 7.3, f"Date: June 2025", fontsize=10, ha='right')
    plt.text(22, 6.8, "Rev: 1.0", fontsize=10, ha='right')
    
    # Save diagram
    filepath = os.path.join(DIAGRAMS_DIR, "p_id_diagram.png")
    plt.savefig(filepath, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved P&ID diagram to {filepath}")
    return filepath

def generate_electrical_schematic():
    """Generate electrical schematic diagram"""
    print("Generating Electrical Schematic...")
    
    plt.figure(figsize=(14, 10))
    
    # Set up the plot
    plt.title('Wastewater Treatment Plant - Electrical Schematic', fontsize=16)
    ax = plt.gca()
    ax.set_facecolor("#f8f9fa")
    plt.axis('off')
    
    # Define components
    def draw_line(x1, y1, x2, y2):
        plt.plot([x1, x2], [y1, y2], color='black', linewidth=1.5)
    
    def draw_ground(x, y):
        plt.plot([x, x], [y, y-0.5], color='black', linewidth=1.5)
        plt.plot([x-0.5, x+0.5], [y-0.5, y-0.5], color='black', linewidth=1.5)
        plt.plot([x-0.3, x+0.3], [y-0.7, y-0.7], color='black', linewidth=1.5)
        plt.plot([x-0.1, x+0.1], [y-0.9, y-0.9], color='black', linewidth=1.5)
    
    def draw_power_supply(x, y, label):
        circle = plt.Circle((x, y), 0.5, fill=False, edgecolor='black', linewidth=1.5)
        ax.add_patch(circle)
        plt.text(x, y, label, ha='center', va='center', fontsize=8)
    
    def draw_motor(x, y, label):
        circle = plt.Circle((x, y), 0.7, fill=False, edgecolor='black', linewidth=1.5)
        ax.add_patch(circle)
        plt.text(x, y, "M", ha='center', va='center', fontsize=12)
        plt.text(x, y-0.9, label, ha='center', va='center', fontsize=8)
    
    def draw_contactor(x, y, label):
        plt.plot([x-0.3, x+0.3], [y-0.3, y+0.3], color='black', linewidth=1.5)
        plt.plot([x-0.3, x+0.3], [y+0.3, y-0.3], color='black', linewidth=1.5)
        plt.text(x, y-0.6, label, ha='center', va='center', fontsize=8)
    
    def draw_switch(x, y, state, label):
        if state == "open":
            plt.plot([x-0.4, x+0.4], [y-0.2, y+0.2], color='black', linewidth=1.5)
        else:
            plt.plot([x-0.4, x+0.4], [y, y], color='black', linewidth=1.5)
        plt.scatter([x-0.4, x+0.4], [y-0.2, y+0.2], color='black', s=30)
        plt.text(x, y-0.5, label, ha='center', va='center', fontsize=8)
    
    def draw_plc(x, y, w, h):
        rect = plt.Rectangle((x, y), w, h, fill=False, edgecolor='black', linewidth=1.5)
        ax.add_patch(rect)
        plt.text(x+w/2, y+h+0.3, "PLC Controller", ha='center', va='center', fontsize=10)
        plt.text(x+w/2, y+h/2, "CPU", ha='center', va='center', fontsize=8)
        
        # I/O modules
        for i in range(1, 6):
            module_x = x + i * w/6
            rect = plt.Rectangle((module_x-0.3, y-1), 0.6, 1, fill=False, 
                               edgecolor='black', linewidth=1)
            ax.add_patch(rect)
            if i == 1:
                plt.text(module_x, y-0.5, "DI", ha='center', va='center', fontsize=6)
            elif i == 2:
                plt.text(module_x, y-0.5, "DO", ha='center', va='center', fontsize=6)
            elif i == 3:
                plt.text(module_x, y-0.5, "AI", ha='center', va='center', fontsize=6)
            elif i == 4:
                plt.text(module_x, y-0.5, "AO", ha='center', va='center', fontsize=6)
            elif i == 5:
                plt.text(module_x, y-0.5, "COM", ha='center', va='center', fontsize=6)
    
    def draw_instrument(x, y, label):
        circle = plt.Circle((x, y), 0.4, fill=False, edgecolor='black', linewidth=1.5)
        ax.add_patch(circle)
        plt.text(x, y, label, ha='center', va='center', fontsize=8)
    
    # Draw power distribution
    draw_power_supply(2, 8, "480V\n3Ph")
    draw_ground(2, 7)
    
    # Main bus
    draw_line(2, 8, 12, 8)
    
    # Motor group 1 - Pumps
    y_pos = 6
    for i, label in enumerate(["P-101", "P-102", "P-103", "P-104"]):
        x = 4 + i * 2
        draw_line(x, 8, x, y_pos+1)
        draw_contactor(x, y_pos+1, f"K{i+1}")
        draw_line(x, y_pos+0.5, x, y_pos)
        draw_motor(x, y_pos-0.5, label)
        draw_line(x, y_pos-1.2, x, y_pos-1.5)
        draw_line(x, y_pos-1.5, 2, y_pos-1.5)
    
    # Ground line for motors
    draw_line(2, y_pos-1.5, 2, 7)
    
    # Motor group 2 - Blowers & mixers
    y_pos = 3
    for i, label in enumerate(["B-101", "B-102", "M-101", "M-102"]):
        x = 4 + i * 2
        draw_line(x, 8, x, y_pos+1) 
        draw_contactor(x, y_pos+1, f"K{i+5}")
        draw_line(x, y_pos+0.5, x, y_pos)
        draw_motor(x, y_pos-0.5, label)
        draw_line(x, y_pos-1.2, x, y_pos-1.5)
        draw_line(x, y_pos-1.5, 2, y_pos-1.5)
    
    # Ground line for second group
    draw_line(2, y_pos-1.5, 2, 7)
    
    # PLC section
    draw_plc(13, 5, 3, 2)
    
    # Control power supply
    draw_power_supply(14.5, 8, "24VDC")
    draw_line(14.5, 7.5, 14.5, 7)
    
    # Connect PLC to power
    draw_line(14.5, 8, 14.5, 7)
    draw_ground(14.5, 7)
    
    # Instruments
    instruments = [
        (16, 8, "FIT101"),
        (16, 7, "LIT101"),
        (16, 6, "AT101"),
        (16, 5, "AIT102"),
        (16, 4, "QIT101")
    ]
    
    for x, y, label in instruments:
        draw_instrument(x, y, label)
        draw_line(16.4, y, 17, y)
        draw_line(15.6, y, 15, y)
        if y == 8:
            draw_line(15, y, 15, 6)
            draw_line(15, 6, 14, 6)
    
    # Connect instruments to PLC
    draw_line(14, 6, 13, 6)
    
    # Add legend
    legend_x = 18
    legend_y = 8
    plt.text(legend_x, legend_y+1, "LEGEND:", fontweight='bold', fontsize=10)
    
    draw_motor(legend_x, legend_y, "")
    plt.text(legend_x+1, legend_y, "Motor", fontsize=8, va='center')
    
    draw_contactor(legend_x, legend_y-1, "")
    plt.text(legend_x+1, legend_y-1, "Contactor", fontsize=8, va='center')
    
    draw_switch(legend_x, legend_y-2, "open", "")
    plt.text(legend_x+1, legend_y-2, "Switch", fontsize=8, va='center')
    
    draw_instrument(legend_x, legend_y-3, "")
    plt.text(legend_x+1, legend_y-3, "Instrument", fontsize=8, va='center')
    
    # Draw border
    border = plt.Rectangle((0.5, 0.5), 20, 9, fill=False, 
                          edgecolor='black', linewidth=1, linestyle='-')
    ax.add_patch(border)
    
    # Add text boxes for project details
    plt.text(1, 9.8, "Wastewater Treatment Plant", fontsize=14, weight='bold')
    plt.text(1, 9.3, "Electrical Schematic", fontsize=12)
    plt.text(20, 9.8, f"Date: June 2025", fontsize=10, ha='right')
    plt.text(20, 9.3, "Rev: 1.0", fontsize=10, ha='right')
    
    # Set limits
    plt.xlim(0, 21)
    plt.ylim(0, 10)
    
    # Save diagram
    filepath = os.path.join(DIAGRAMS_DIR, "electrical_schematic.png")
    plt.savefig(filepath, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved electrical schematic to {filepath}")
    return filepath

def combine_diagrams_to_pdf():
    """Combine all diagrams into a single PDF"""
    try:
        from matplotlib.backends.backend_pdf import PdfPages
        import matplotlib.image as mpimg
        
        print("Combining diagrams into PDF...")
        
        # List of diagram files
        diagram_files = [
            os.path.join(DIAGRAMS_DIR, "treatment_control_flowchart.png"),
            os.path.join(DIAGRAMS_DIR, "system_layout_diagram.png"),
            os.path.join(DIAGRAMS_DIR, "p_id_diagram.png"),
            os.path.join(DIAGRAMS_DIR, "electrical_schematic.png")
        ]
        
        # Create PDF
        pdf_path = os.path.join(DIAGRAMS_DIR, "wwtp_system_diagrams.pdf")
        with PdfPages(pdf_path) as pdf:
            # Add title page
            plt.figure(figsize=(8.5, 11))
            plt.text(0.5, 0.7, "Wastewater Treatment Plant", 
                    ha='center', fontsize=24, fontweight='bold')
            plt.text(0.5, 0.6, "System Diagrams", 
                    ha='center', fontsize=20)
            plt.text(0.5, 0.5, "June 2025", 
                    ha='center', fontsize=16)
            plt.text(0.5, 0.4, "Version 1.0", 
                    ha='center', fontsize=16)
            plt.axis('off')
            pdf.savefig()
            plt.close()
            
            # Add each diagram on its own page
            for diagram in diagram_files:
                try:
                    img = mpimg.imread(diagram)
                    plt.figure(figsize=(8.5, 11))
                    plt.imshow(img)
                    plt.axis('off')
                    pdf.savefig(bbox_inches='tight')
                    plt.close()
                except Exception as e:
                    print(f"Error adding {diagram} to PDF: {e}")
        
        print(f"PDF created at {pdf_path}")
        return pdf_path
        
    except ImportError:
        print("Matplotlib PDF backend not available. PDF not created.")
        return None

def main():
    """Main function to generate all diagrams"""
    parser = argparse.ArgumentParser(description='Generate WWTP system diagrams')
    parser.add_argument('--all', action='store_true', help='Generate all diagrams')
    parser.add_argument('--flowchart', action='store_true', help='Generate control flowchart')
    parser.add_argument('--layout', action='store_true', help='Generate system layout')
    parser.add_argument('--pid', action='store_true', help='Generate P&ID diagram')
    parser.add_argument('--electrical', action='store_true', help='Generate electrical schematic')
    parser.add_argument('--pdf', action='store_true', help='Combine diagrams into PDF')
    
    args = parser.parse_args()
    
    # If no specific diagram is selected, generate all
    if not (args.flowchart or args.layout or args.pid or args.electrical or args.pdf):
        args.all = True
    
    if args.all or args.flowchart:
        generate_treatment_control_flowchart()
        
    if args.all or args.layout:
        generate_system_layout_diagram()
        
    if args.all or args.pid:
        generate_pid_diagram()
        
    if args.all or args.electrical:
        generate_electrical_schematic()
        
    if args.all or args.pdf:
        combine_diagrams_to_pdf()
    
    print("Diagram generation complete!")

if __name__ == "__main__":
    main()
