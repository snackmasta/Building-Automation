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
        
        # Create combined PDF
        print("Creating combined PDF...")
        pdf_path = os.path.join(output_dir, "water_treatment_diagrams.pdf")
        with PdfPages(pdf_path) as pdf:
            pdf.savefig(fig1, bbox_inches='tight', facecolor='white')
            pdf.savefig(fig2, bbox_inches='tight', facecolor='white')
            pdf.savefig(fig3, bbox_inches='tight', facecolor='white')
        print(f"Saved: {pdf_path}")
        
        plt.close('all')
        print("All diagrams generated successfully!")
        
        return [png_path1, png_path2, png_path3, pdf_path]

def main():
    """Main function to generate all process diagrams"""
    print("Water Treatment System - Process Diagram Generator")
    print("=" * 50)
    
    generator = ProcessDiagramGenerator()
    
    # Generate diagrams in current directory
    output_files = generator.generate_all_diagrams()
    
    print("\nGenerated files:")
    for file_path in output_files:
        print(f"  • {file_path}")
    
    print("\nDiagram generation complete!")

if __name__ == "__main__":
    main()
