"""
System Diagram Generator for Car Parking Vending System
Generates architectural diagrams, flowcharts, and system schematics
"""

import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Rectangle, Circle, Arrow
import numpy as np
from datetime import datetime

class SystemDiagramGenerator:
    """Generates various system diagrams and flowcharts"""
    
    def __init__(self, output_dir):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
        # Set up plotting style
        plt.style.use('default')
        self.colors = {
            'primary': '#2c3e50',
            'secondary': '#3498db',
            'success': '#27ae60',
            'warning': '#f39c12',
            'danger': '#e74c3c',
            'light': '#ecf0f1',
            'dark': '#34495e'
        }
        
    def generate_system_architecture(self):
        """Generate system architecture diagram"""
        fig, ax = plt.subplots(1, 1, figsize=(16, 12))
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        ax.set_aspect('equal')
        
        # Title
        ax.text(5, 9.5, 'Car Parking Vending System - Architecture', 
                fontsize=20, fontweight='bold', ha='center')
        
        # Physical Infrastructure Layer
        infrastructure = FancyBboxPatch((0.5, 7.5), 9, 1.2, 
                                      boxstyle="round,pad=0.1",
                                      facecolor=self.colors['light'],
                                      edgecolor=self.colors['primary'],
                                      linewidth=2)
        ax.add_patch(infrastructure)
        ax.text(5, 8.1, 'Physical Infrastructure Layer', 
                fontsize=14, fontweight='bold', ha='center')
        
        # Infrastructure components
        components = [
            ('Elevators (3x)', 1.5, 7.8),
            ('Robotic Platforms', 3.5, 7.8),
            ('Sensors & Cameras', 5.5, 7.8),
            ('Payment Kiosks', 7.5, 7.8)
        ]
        
        for comp, x, y in components:
            comp_box = Rectangle((x-0.4, y-0.15), 0.8, 0.3,
                               facecolor=self.colors['secondary'],
                               edgecolor='white')
            ax.add_patch(comp_box)
            ax.text(x, y, comp, fontsize=9, ha='center', va='center', color='white')
            
        # Control Layer
        control = FancyBboxPatch((0.5, 5.8), 9, 1.2,
                               boxstyle="round,pad=0.1",
                               facecolor=self.colors['success'],
                               edgecolor=self.colors['primary'],
                               linewidth=2)
        ax.add_patch(control)
        ax.text(5, 6.4, 'Control Layer', 
                fontsize=14, fontweight='bold', ha='center', color='white')
        
        # Control components
        control_components = [
            ('Main PLC', 1.5, 6.1),
            ('Safety PLC', 2.8, 6.1),
            ('Elevator Controllers', 4.5, 6.1),
            ('Payment Controller', 6.2, 6.1),
            ('Parking Controller', 7.8, 6.1)
        ]
        
        for comp, x, y in control_components:
            comp_box = Rectangle((x-0.35, y-0.15), 0.7, 0.3,
                               facecolor='white',
                               edgecolor=self.colors['dark'])
            ax.add_patch(comp_box)
            ax.text(x, y, comp, fontsize=8, ha='center', va='center')
            
        # Communication Layer
        comm = FancyBboxPatch((0.5, 4.1), 9, 1.2,
                            boxstyle="round,pad=0.1",
                            facecolor=self.colors['warning'],
                            edgecolor=self.colors['primary'],
                            linewidth=2)
        ax.add_patch(comm)
        ax.text(5, 4.7, 'Communication Layer', 
                fontsize=14, fontweight='bold', ha='center')
        
        # Communication protocols
        comm_protocols = [
            ('WebSocket', 1.5, 4.4),
            ('TCP/IP', 2.8, 4.4),
            ('Modbus TCP', 4.2, 4.4),
            ('OPC UA', 5.5, 4.4),
            ('Ethernet', 6.8, 4.4),
            ('WiFi', 8.1, 4.4)
        ]
        
        for prot, x, y in comm_protocols:
            prot_box = Rectangle((x-0.3, y-0.15), 0.6, 0.3,
                               facecolor='white',
                               edgecolor=self.colors['dark'])
            ax.add_patch(prot_box)
            ax.text(x, y, prot, fontsize=8, ha='center', va='center')
            
        # Application Layer
        app = FancyBboxPatch((0.5, 2.4), 9, 1.2,
                           boxstyle="round,pad=0.1",
                           facecolor=self.colors['secondary'],
                           edgecolor=self.colors['primary'],
                           linewidth=2)
        ax.add_patch(app)
        ax.text(5, 3.0, 'Application Layer', 
                fontsize=14, fontweight='bold', ha='center', color='white')
        
        # Application components
        app_components = [
            ('Database\nManager', 1.5, 2.7),
            ('Simulation\nEngine', 2.8, 2.7),
            ('Communication\nManager', 4.2, 2.7),
            ('System\nUtilities', 5.5, 2.7),
            ('Config\nManager', 6.8, 2.7),
            ('Monitoring\nSystem', 8.1, 2.7)
        ]
        
        for comp, x, y in app_components:
            comp_box = Rectangle((x-0.35, y-0.25), 0.7, 0.5,
                               facecolor='white',
                               edgecolor=self.colors['dark'])
            ax.add_patch(comp_box)
            ax.text(x, y, comp, fontsize=8, ha='center', va='center')
            
        # User Interface Layer
        ui = FancyBboxPatch((0.5, 0.7), 9, 1.2,
                          boxstyle="round,pad=0.1",
                          facecolor=self.colors['danger'],
                          edgecolor=self.colors['primary'],
                          linewidth=2)
        ax.add_patch(ui)
        ax.text(5, 1.3, 'User Interface Layer', 
                fontsize=14, fontweight='bold', ha='center', color='white')
        
        # UI components
        ui_components = [
            ('Desktop HMI', 2, 1.0),
            ('Web HMI', 3.5, 1.0),
            ('Mobile App', 5, 1.0),
            ('Customer Kiosk', 6.5, 1.0),
            ('Admin Portal', 8, 1.0)
        ]
        
        for comp, x, y in ui_components:
            comp_box = Rectangle((x-0.4, y-0.15), 0.8, 0.3,
                               facecolor='white',
                               edgecolor=self.colors['dark'])
            ax.add_patch(comp_box)
            ax.text(x, y, comp, fontsize=8, ha='center', va='center')
            
        # Add connection arrows
        arrow_props = dict(arrowstyle='->', lw=2, color=self.colors['dark'])
        
        # Infrastructure to Control
        ax.annotate('', xy=(5, 5.8), xytext=(5, 7.5), arrowprops=arrow_props)
        
        # Control to Communication
        ax.annotate('', xy=(5, 4.1), xytext=(5, 5.8), arrowprops=arrow_props)
        
        # Communication to Application
        ax.annotate('', xy=(5, 2.4), xytext=(5, 4.1), arrowprops=arrow_props)
        
        # Application to UI
        ax.annotate('', xy=(5, 0.7), xytext=(5, 2.4), arrowprops=arrow_props)
        
        ax.set_xticks([])
        ax.set_yticks([])
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)
        
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, 'system_architecture.png'), 
                   dpi=300, bbox_inches='tight')
        plt.close()
        
    def generate_parking_layout(self):
        """Generate 3D parking structure layout"""
        fig = plt.figure(figsize=(16, 12))
        ax = fig.add_subplot(111, projection='3d')
        
        # Parameters
        levels = 15
        spaces_per_level = 20
        space_width = 2.5
        space_length = 5.0
        level_height = 3.0
        
        # Generate parking spaces
        for level in range(levels):
            z = level * level_height
            
            # Create parking spaces in two rows
            for i in range(spaces_per_level):
                if i < 10:  # First row
                    x = i * space_length
                    y = 0
                else:  # Second row
                    x = (i - 10) * space_length
                    y = space_width + 5  # Driving lane
                    
                # Draw parking space
                space_vertices = [
                    [x, y, z],
                    [x + space_length, y, z],
                    [x + space_length, y + space_width, z],
                    [x, y + space_width, z]
                ]
                
                # Color coding: occupied vs available
                import random
                color = 'red' if random.random() < 0.6 else 'green'
                
                ax.plot([v[0] for v in space_vertices] + [space_vertices[0][0]],
                       [v[1] for v in space_vertices] + [space_vertices[0][1]],
                       [v[2] for v in space_vertices] + [space_vertices[0][2]],
                       color=color, linewidth=1)
                       
        # Add elevators
        elevator_positions = [(25, 7.5), (50, 7.5), (75, 7.5)]
        for i, (x, y) in enumerate(elevator_positions):
            # Draw elevator shaft
            ax.plot([x, x], [y, y], [0, levels * level_height], 
                   color='blue', linewidth=5, label='Elevator' if i == 0 else '')
                   
            # Draw elevator car (random position)
            car_z = random.randint(0, levels-1) * level_height
            ax.scatter([x], [y], [car_z], color='blue', s=100, marker='s')
            
        # Add labels and title
        ax.set_xlabel('Length (m)')
        ax.set_ylabel('Width (m)')
        ax.set_zlabel('Height (m)')
        ax.set_title('Car Parking Vending System - 3D Layout\n15 Levels × 20 Spaces = 300 Total Spaces')
        
        # Legend
        ax.plot([], [], color='red', linewidth=2, label='Occupied Space')
        ax.plot([], [], color='green', linewidth=2, label='Available Space')
        ax.legend()
        
        plt.savefig(os.path.join(self.output_dir, 'parking_layout_3d.png'), 
                   dpi=300, bbox_inches='tight')
        plt.close()
        
    def generate_state_machine_diagram(self):
        """Generate PLC state machine diagram"""
        fig, ax = plt.subplots(1, 1, figsize=(14, 10))
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        
        # Title
        ax.text(5, 9.5, 'PLC Main Controller - State Machine', 
                fontsize=16, fontweight='bold', ha='center')
        
        # Define states and positions
        states = {
            'INIT': (2, 8),
            'IDLE': (5, 8),
            'PAYMENT': (8, 8),
            'ENTRY': (2, 6),
            'PARKING': (5, 6),
            'PARKED': (8, 6),
            'RETRIEVAL': (2, 4),
            'EXIT_SEQUENCE': (5, 4),
            'MAINTENANCE': (8, 4),
            'EMERGENCY': (5, 2)
        }
        
        # Draw states
        for state, (x, y) in states.items():
            if state == 'EMERGENCY':
                color = self.colors['danger']
                text_color = 'white'
            elif state == 'MAINTENANCE':
                color = self.colors['warning']
                text_color = 'black'
            elif state in ['PARKED', 'IDLE']:
                color = self.colors['success']
                text_color = 'white'
            else:
                color = self.colors['secondary']
                text_color = 'white'
                
            circle = Circle((x, y), 0.6, facecolor=color, edgecolor='black', linewidth=2)
            ax.add_patch(circle)
            ax.text(x, y, state, fontsize=10, ha='center', va='center', 
                   color=text_color, fontweight='bold')
        
        # Define transitions
        transitions = [
            ('INIT', 'IDLE', 'System Ready'),
            ('IDLE', 'PAYMENT', 'Vehicle Detected'),
            ('PAYMENT', 'ENTRY', 'Payment OK'),
            ('PAYMENT', 'IDLE', 'Payment Failed'),
            ('ENTRY', 'PARKING', 'Vehicle Entered'),
            ('PARKING', 'PARKED', 'Parking Complete'),
            ('PARKED', 'RETRIEVAL', 'Retrieval Request'),
            ('RETRIEVAL', 'EXIT_SEQUENCE', 'Vehicle Retrieved'),
            ('EXIT_SEQUENCE', 'IDLE', 'Vehicle Exited'),
            ('IDLE', 'MAINTENANCE', 'Maintenance Mode'),
            ('MAINTENANCE', 'IDLE', 'Maintenance Complete'),
            ('*', 'EMERGENCY', 'Emergency Stop')
        ]
        
        # Draw transitions
        arrow_props = dict(arrowstyle='->', lw=1.5, color='black')
        
        for start, end, label in transitions:
            if start == '*':  # Emergency transitions
                for state in ['IDLE', 'PAYMENT', 'ENTRY', 'PARKING', 'RETRIEVAL']:
                    start_pos = states[state]
                    end_pos = states[end]
                    ax.annotate('', xy=end_pos, xytext=start_pos, 
                               arrowprops=dict(arrowstyle='->', lw=1, color='red', alpha=0.7))
            else:
                start_pos = states[start]
                end_pos = states[end]
                
                # Calculate arrow position
                dx = end_pos[0] - start_pos[0]
                dy = end_pos[1] - start_pos[1]
                distance = np.sqrt(dx**2 + dy**2)
                
                if distance > 0:
                    # Start and end points on circle edges
                    start_edge = (start_pos[0] + 0.6 * dx/distance, 
                                start_pos[1] + 0.6 * dy/distance)
                    end_edge = (end_pos[0] - 0.6 * dx/distance, 
                              end_pos[1] - 0.6 * dy/distance)
                    
                    ax.annotate('', xy=end_edge, xytext=start_edge, arrowprops=arrow_props)
                    
                    # Add transition label
                    mid_x = (start_edge[0] + end_edge[0]) / 2
                    mid_y = (start_edge[1] + end_edge[1]) / 2
                    ax.text(mid_x, mid_y + 0.2, label, fontsize=8, ha='center', 
                           bbox=dict(boxstyle="round,pad=0.2", facecolor='white', alpha=0.8))
        
        ax.set_xticks([])
        ax.set_yticks([])
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)
        
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, 'state_machine_diagram.png'), 
                   dpi=300, bbox_inches='tight')
        plt.close()
        
    def generate_data_flow_diagram(self):
        """Generate system data flow diagram"""
        fig, ax = plt.subplots(1, 1, figsize=(16, 12))
        ax.set_xlim(0, 12)
        ax.set_ylim(0, 10)
        
        # Title
        ax.text(6, 9.5, 'Car Parking System - Data Flow Diagram', 
                fontsize=16, fontweight='bold', ha='center')
        
        # External entities
        entities = [
            ('Customer', 1, 8, self.colors['primary']),
            ('Administrator', 11, 8, self.colors['primary']),
            ('Payment Gateway', 1, 2, self.colors['warning']),
            ('Maintenance System', 11, 2, self.colors['warning'])
        ]
        
        for name, x, y, color in entities:
            rect = Rectangle((x-0.8, y-0.4), 1.6, 0.8, 
                           facecolor=color, edgecolor='black')
            ax.add_patch(rect)
            ax.text(x, y, name, fontsize=10, ha='center', va='center', 
                   color='white', fontweight='bold')
        
        # Processes
        processes = [
            ('1\nVehicle\nEntry', 3, 7, self.colors['secondary']),
            ('2\nPayment\nProcessing', 3, 5, self.colors['secondary']),
            ('3\nParking\nManagement', 6, 6, self.colors['secondary']),
            ('4\nVehicle\nRetrieval', 9, 7, self.colors['secondary']),
            ('5\nSystem\nMonitoring', 9, 5, self.colors['secondary']),
            ('6\nMaintenance\nScheduling', 6, 3, self.colors['secondary'])
        ]
        
        for name, x, y, color in processes:
            circle = Circle((x, y), 0.8, facecolor=color, edgecolor='black', linewidth=2)
            ax.add_patch(circle)
            ax.text(x, y, name, fontsize=9, ha='center', va='center', 
                   color='white', fontweight='bold')
        
        # Data stores
        stores = [
            ('D1 | Vehicle Database', 4.5, 8.5),
            ('D2 | Transaction Records', 4.5, 4),
            ('D3 | System Logs', 7.5, 8.5),
            ('D4 | Configuration Data', 7.5, 4)
        ]
        
        for name, x, y in stores:
            rect = Rectangle((x-1.2, y-0.3), 2.4, 0.6, 
                           facecolor='white', edgecolor='black', linewidth=2)
            ax.add_patch(rect)
            ax.text(x, y, name, fontsize=9, ha='center', va='center')
        
        # Data flows
        flows = [
            # From Customer
            ((1.8, 8), (2.2, 7), 'Entry Request'),
            ((2.2, 7), (1.8, 8), 'Entry Confirmation'),
            
            # Payment flows
            ((3, 6.2), (3, 5.8), 'Payment Data'),
            ((2.2, 5), (1.8, 2), 'Payment Info'),
            ((1.8, 2.4), (2.2, 5.4), 'Payment Status'),
            
            # Database interactions
            ((3.8, 7), (4.5, 8.2), 'Vehicle Info'),
            ((4.5, 8.2), (3.8, 7), 'Space Assignment'),
            ((3.8, 5), (4.5, 4.3), 'Transaction Data'),
            
            # Parking management
            ((5.2, 6), (6.8, 6), 'Parking Commands'),
            ((6.8, 6), (5.2, 6), 'Status Updates'),
            
            # Retrieval
            ((8.2, 7), (9.8, 7), 'Retrieval Request'),
            ((9.8, 7), (8.2, 7), 'Vehicle Location'),
            
            # Monitoring
            ((9, 5.8), (7.5, 8.2), 'System Status'),
            ((7.5, 8.2), (9, 5.8), 'Alert Data'),
            
            # Maintenance
            ((6, 3.8), (11, 2.4), 'Maintenance Reports'),
            ((11, 2.4), (6, 3.8), 'Maintenance Schedule')
        ]
        
        for (start, end, label) in flows:
            # Draw arrow
            ax.annotate('', xy=end, xytext=start, 
                       arrowprops=dict(arrowstyle='->', lw=1.5, color='blue'))
            
            # Add label
            mid_x = (start[0] + end[0]) / 2
            mid_y = (start[1] + end[1]) / 2
            ax.text(mid_x, mid_y, label, fontsize=8, ha='center', 
                   bbox=dict(boxstyle="round,pad=0.1", facecolor='lightyellow', alpha=0.8))
        
        ax.set_xticks([])
        ax.set_yticks([])
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)
        
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, 'data_flow_diagram.png'), 
                   dpi=300, bbox_inches='tight')
        plt.close()
        
    def generate_network_diagram(self):
        """Generate network architecture diagram"""
        fig, ax = plt.subplots(1, 1, figsize=(16, 10))
        ax.set_xlim(0, 14)
        ax.set_ylim(0, 10)
        
        # Title
        ax.text(7, 9.5, 'Car Parking System - Network Architecture', 
                fontsize=16, fontweight='bold', ha='center')
        
        # Network segments
        segments = [
            ('Control Network\n(192.168.1.0/24)', 2, 8, 3, 1.5, self.colors['secondary']),
            ('Office Network\n(192.168.2.0/24)', 8, 8, 3, 1.5, self.colors['success']),
            ('Customer Network\n(192.168.3.0/24)', 2, 2, 3, 1.5, self.colors['warning']),
            ('External Network\n(Internet)', 8, 2, 3, 1.5, self.colors['danger'])
        ]
        
        for name, x, y, w, h, color in segments:
            rect = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.1",
                                facecolor=color, alpha=0.3, edgecolor=color, linewidth=2)
            ax.add_patch(rect)
            ax.text(x + w/2, y + h - 0.2, name, fontsize=12, fontweight='bold', 
                   ha='center', color=color)
        
        # Network devices
        devices = [
            # Control Network
            ('Main PLC\n192.168.1.10', 2.2, 7.5, 'square'),
            ('Safety PLC\n192.168.1.11', 2.2, 7, 'square'),
            ('Elevator #1\n192.168.1.20', 3.5, 7.5, 'square'),
            ('Elevator #2\n192.168.1.21', 3.5, 7, 'square'),
            ('Elevator #3\n192.168.1.22', 4.3, 7.5, 'square'),
            
            # Office Network
            ('HMI Server\n192.168.2.10', 8.2, 7.5, 'circle'),
            ('Database\n192.168.2.20', 8.2, 7, 'circle'),
            ('Web Server\n192.168.2.30', 9.5, 7.5, 'circle'),
            ('Admin PC\n192.168.2.100', 9.5, 7, 'circle'),
            
            # Customer Network
            ('Kiosk #1\n192.168.3.10', 2.2, 2.5, 'triangle'),
            ('Kiosk #2\n192.168.3.11', 3.2, 2.5, 'triangle'),
            ('WiFi AP\n192.168.3.1', 4.2, 2.5, 'triangle'),
            
            # Core Infrastructure
            ('Core Switch\n192.168.1.1', 6, 5.5, 'diamond'),
            ('Firewall\n192.168.1.254', 6, 4, 'diamond'),
            ('Router\nPublic IP', 8.5, 3, 'diamond')        ]
        
        for name, x, y, shape in devices:
            if shape == 'square':
                rect = Rectangle((x-0.3, y-0.2), 0.6, 0.4, 
                               facecolor=self.colors['secondary'], edgecolor='black')
                ax.add_patch(rect)
            elif shape == 'circle':
                circle = Circle((x, y), 0.25, facecolor=self.colors['success'], edgecolor='black')
                ax.add_patch(circle)
            elif shape == 'triangle':
                triangle = patches.RegularPolygon((x, y), 3, 0.25, 
                                                facecolor=self.colors['warning'], edgecolor='black')
                ax.add_patch(triangle)
            elif shape == 'diamond':
                diamond = patches.RegularPolygon((x, y), 4, 0.3, orientation=np.pi/4,
                                               facecolor=self.colors['primary'], edgecolor='black')
                ax.add_patch(diamond)
                
            ax.text(x, y-0.6, name, fontsize=8, ha='center', va='top')
        
        # Network connections
        connections = [
            # Control network to core switch
            ((3.5, 6.5), (6, 5.8)),
            ((4.5, 6.5), (6, 5.8)),
            
            # Office network to core switch
            ((8.5, 6.5), (6, 5.8)),
            ((9.5, 6.5), (6, 5.8)),
            
            # Customer network to firewall
            ((3.5, 3.5), (6, 4.3)),
            
            # Core connections
            ((6, 5.2), (6, 4.3)),  # Switch to firewall
            ((6.3, 4), (8.2, 3)),   # Firewall to router
        ]
        
        for start, end in connections:
            ax.plot([start[0], end[0]], [start[1], end[1]], 
                   'k-', linewidth=2, alpha=0.7)
          # Add legend
        legend_elements = [
            plt.Rectangle((0, 0), 1, 1, facecolor=self.colors['secondary'], label='PLC/Control'),
            plt.Circle((0, 0), 1, facecolor=self.colors['success'], label='Server/PC'),
            patches.RegularPolygon((0, 0), 3, 1, facecolor=self.colors['warning'], label='Customer Device'),
            patches.RegularPolygon((0, 0), 4, 1, facecolor=self.colors['primary'], label='Network Infrastructure')
        ]
        ax.legend(handles=legend_elements, loc='upper right')
        
        ax.set_xticks([])
        ax.set_yticks([])
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)
        
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, 'network_diagram.png'), 
                   dpi=300, bbox_inches='tight')
        plt.close()
        
    def generate_all_diagrams(self):
        """Generate all system diagrams"""
        print("Generating system diagrams...")
        
        diagrams = [
            ('System Architecture', self.generate_system_architecture),
            ('Parking Layout 3D', self.generate_parking_layout),
            ('State Machine', self.generate_state_machine_diagram),
            ('Data Flow', self.generate_data_flow_diagram),
            ('Network Architecture', self.generate_network_diagram)
        ]
        
        for name, generator in diagrams:
            try:
                print(f"  - {name}...")
                generator()
                print(f"    ✓ Generated successfully")
            except Exception as e:
                print(f"    ✗ Error: {e}")
                
        print(f"\nAll diagrams saved to: {self.output_dir}")

def main():
    """Main function to generate all diagrams"""
    output_dir = os.path.join(os.path.dirname(__file__), '..', 'diagrams')
    generator = SystemDiagramGenerator(output_dir)
    generator.generate_all_diagrams()

if __name__ == '__main__':
    main()
