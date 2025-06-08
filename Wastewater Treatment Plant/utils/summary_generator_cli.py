#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Project Summary Generator CLI for Wastewater Treatment Plant
-----------------------------------------------------------
This script provides a command-line interface for the project summary generator
with interactive options to customize the report output.
"""

import os
import sys
import argparse
import time
from datetime import datetime

# Add the parent directory to path for importing the project_summary_generator module
script_dir = os.path.dirname(os.path.abspath(__file__))
utils_dir = os.path.abspath(os.path.join(script_dir, '..'))
if utils_dir not in sys.path:
    sys.path.insert(0, utils_dir)

try:
    from project_summary_generator import ProjectSummaryGenerator
except ImportError:
    print("Error: Could not import ProjectSummaryGenerator. Please check the project structure.")
    sys.exit(1)


def print_header():
    """Print a fancy header for the CLI."""
    header = r"""
    __          __        _                         _            
    \ \        / /       | |                       | |           
     \ \  /\  / /____ ___| |_ _____      ____ _ ___| |_ ___ _ __ 
      \ \/  \/ // _  / __| __/ _ \ \ /\ / / _` / __| __/ _ \ '__|
       \  /\  /|  __/\__ \ |  __/\ V  V / (_| \__ \ |  __/ |   
        \/  \/  \___||___/\__\___| \_/\_/ \__,_|___/\__\___|_|   
                                                                
    ______          _                         _    _____                                           
   |  ____|        | |                       | |  / ____|                                          
   | |__ __ _ _   _| |_ _   _ _ __ ___   ___| | | |  __  ___ _ __   ___ _ __ __ _| |_ ___  _ __  
   |  __/ _` | | | | __| | | | '_ ` _ \ / _ \ | | | |_ |/ _ \ '_ \ / _ \ '__/ _` | __/ _ \| '__| 
   | | | (_| | |_| | |_| |_| | | | | | |  __/ | | |__| |  __/ | | |  __/ | | (_| | || (_) | |    
   |_|  \__,_|\__,_|\__|\__,_|_| |_| |_|\___|_|  \_____|\___|_| |_|\___|_|  \__,_|\__\___/|_|    
                                                                                                  
   """
    print(header)
    print("Project Summary Generator CLI")
    print("=" * 80)


def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')


def interactive_mode(project_root=None):
    """Run the summary generator in interactive mode."""
    clear_screen()
    print_header()
    
    # Get project root
    if not project_root:
        default_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
        project_root = input(f"Enter project root directory [default: {default_root}]: ").strip()
        if not project_root:
            project_root = default_root
    
    # Verify project root exists
    if not os.path.exists(project_root):
        print(f"Error: Project root directory '{project_root}' does not exist.")
        return False
    
    # Get output directory
    default_output_dir = os.path.join(project_root, 'reports')
    output_dir = input(f"Enter output directory [default: {default_output_dir}]: ").strip()
    if not output_dir:
        output_dir = default_output_dir
    
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        try:
            os.makedirs(output_dir)
            print(f"Created output directory: {output_dir}")
        except Exception as e:
            print(f"Error creating output directory: {str(e)}")
            return False
    
    # Get output format
    format_options = {
        '1': 'json',
        '2': 'text',
        '3': 'html'
    }
    
    print("\nSelect output format:")
    for key, value in format_options.items():
        print(f"{key}. {value.upper()}")
    
    format_choice = input("Enter choice [default: 1 (JSON)]: ").strip()
    if not format_choice or format_choice not in format_options:
        format_choice = '1'
    
    output_format = format_options[format_choice]
    
    # Generate timestamp for filename
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    default_filename = f"project_summary_{timestamp}"
    
    filename = input(f"Enter output filename without extension [default: {default_filename}]: ").strip()
    if not filename:
        filename = default_filename
    
    output_path = os.path.join(output_dir, filename)
    
    print("\nGenerating project summary with the following settings:")
    print(f"- Project root: {project_root}")
    print(f"- Output path: {output_path}.{output_format}")
    print(f"- Format: {output_format.upper()}")
    
    # Confirm settings
    confirm = input("\nProceed with these settings? [Y/n]: ").strip().lower()
    if confirm and confirm != 'y':
        print("Operation cancelled.")
        return False
    
    # Show progress
    print("\nGenerating project summary...")
    print("This may take a moment...")
    
    try:
        # Display a simple progress indicator
        print("Analyzing project structure...", end="", flush=True)
        generator = ProjectSummaryGenerator(project_root)
        
        # Simple animation
        for i in range(5):
            time.sleep(0.5)
            print(".", end="", flush=True)
        print(" Done!")
        
        print("Processing configuration files...", end="", flush=True)
        generator.load_configs()
        for i in range(3):
            time.sleep(0.3)
            print(".", end="", flush=True)
        print(" Done!")
        
        print("Analyzing source code...", end="", flush=True)
        generator.analyze_source_code()
        for i in range(8):
            time.sleep(0.4)
            print(".", end="", flush=True)
        print(" Done!")
        
        print("Identifying components...", end="", flush=True)
        generator.identify_components()
        for i in range(3):
            time.sleep(0.3)
            print(".", end="", flush=True)
        print(" Done!")
        
        print("Checking documentation...", end="", flush=True)
        generator.check_documentation_status()
        for i in range(4):
            time.sleep(0.3)
            print(".", end="", flush=True)
        print(" Done!")
        
        print("Generating final report...", end="", flush=True)
        success = generator.save_summary(output_path, output_format)
        for i in range(3):
            time.sleep(0.5)
            print(".", end="", flush=True)
        print(" Done!")
        
        if success:
            print(f"\nProject summary successfully generated: {output_path}.{output_format}")
            
            # Open the file if it's HTML
            if output_format == 'html':
                open_file = input("\nOpen the HTML report now? [Y/n]: ").strip().lower()
                if not open_file or open_file == 'y':
                    try:
                        full_path = f"{output_path}.{output_format}"
                        if os.name == 'nt':
                            os.startfile(full_path)
                        else:
                            import subprocess
                            subprocess.call(['xdg-open', full_path])
                    except Exception as e:
                        print(f"Error opening file: {str(e)}")
            
            return True
        else:
            print("\nError generating project summary.")
            return False
    except Exception as e:
        print(f"\nError: {str(e)}")
        return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Interactive interface for Project Summary Generator')
    parser.add_argument('--project-root', '-p', type=str, default=None,
                       help='Path to project root directory')
    parser.add_argument('--batch', '-b', action='store_true',
                       help='Run in batch mode (non-interactive)')
    parser.add_argument('--output', '-o', type=str, default=None,
                       help='Output file path (without extension)')
    parser.add_argument('--format', '-f', type=str, choices=['json', 'text', 'html'], default='json',
                       help='Output format')
    
    args = parser.parse_args()
    
    if args.batch:
        # Run in batch mode
        project_root = args.project_root or os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
        output = args.output or os.path.join(project_root, 'reports', f"project_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
        
        generator = ProjectSummaryGenerator(project_root)
        success = generator.run(output, args.format)
        
        if success:
            print(f"Project summary generation completed successfully: {output}.{args.format}")
            sys.exit(0)
        else:
            print("Project summary generation failed")
            sys.exit(1)
    else:
        # Run in interactive mode
        success = interactive_mode(args.project_root)
        sys.exit(0 if success else 1)
