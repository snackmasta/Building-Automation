#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
I/O Configuration Validator for Wastewater Treatment Plant
----------------------------------------------------------
This utility validates I/O configuration and mapping against actual hardware
and verifies that all required inputs and outputs are properly assigned.
"""

import os
import sys
import configparser
import json
import re
from collections import defaultdict, OrderedDict


class IOValidator:
    """Validates I/O configuration for the WWTP control system."""
    
    def __init__(self, project_root):
        self.project_root = project_root
        self.plc_config = None
        self.io_config = {}
        self.io_tags = {}
        self.errors = []
        self.warnings = []
        
        # Define required I/O by system component
        self.required_io = {
            'intake': {
                'di': ['pump_running', 'pump_fault', 'high_level', 'low_level'],
                'do': ['pump_start', 'pump_stop', 'alarm'],
                'ai': ['flow_rate', 'level'],
                'ao': []
            },
            'treatment': {
                'di': ['mixer_running', 'mixer_fault', 'aerator_running', 'aerator_fault'],
                'do': ['mixer_start', 'mixer_stop', 'aerator_start', 'aerator_stop'],
                'ai': ['level', 'temperature', 'ph', 'dissolvedoxygen'],
                'ao': ['mixer_speed']
            },
            'dosing': {
                'di': ['acid_pump_running', 'base_pump_running', 'chemical_level_low'],
                'do': ['acid_pump_start', 'base_pump_start', 'disinfectant_pump_start'],
                'ai': ['chemical_flow', 'chemical_level'],
                'ao': ['acid_pump_speed', 'base_pump_speed', 'disinfectant_pump_speed']
            },
            'aeration': {
                'di': ['blower_running', 'blower_fault'],
                'do': ['blower_start', 'blower_stop'],
                'ai': ['dissolvedoxygen', 'airflow'],
                'ao': ['blower_speed', 'valve_position']
            },
            'monitoring': {
                'di': ['system_power', 'emergency_stop'],
                'do': ['system_alarm', 'beacon_light'],
                'ai': ['ph', 'dissolvedoxygen', 'turbidity', 'conductivity', 'temperature'],
                'ao': []
            }
        }
    
    def load_configs(self):
        """Load PLC configuration and I/O mapping files."""
        try:
            # Load PLC configuration
            self.plc_config = configparser.ConfigParser()
            self.plc_config.read(os.path.join(self.project_root, 'config', 'plc_config.ini'))
            
            # Look for I/O configuration files
            io_files = [
                os.path.join(self.project_root, 'config', 'io_config.ini'),
                os.path.join(self.project_root, 'plc', 'io_mapping.ini'),
                os.path.join(self.project_root, 'plc', 'io_tags.ini')
            ]
            
            # Try to load any existing I/O configuration
            for file_path in io_files:
                if os.path.exists(file_path):
                    io_config = configparser.ConfigParser()
                    io_config.read(file_path)
                    self.io_config = {s: dict(io_config[s]) for s in io_config.sections()}
                    break
            
            # If no I/O config found, try to extract from PLC code files
            if not self.io_config:
                self._extract_io_from_plc_code()
            
            return bool(self.plc_config.sections())
        except Exception as e:
            self.errors.append(f"Error loading configurations: {str(e)}")
            return False
    
    def _extract_io_from_plc_code(self):
        """Extract I/O tags from PLC code files."""
        try:
            plc_dir = os.path.join(self.project_root, 'plc')
            if not os.path.exists(plc_dir):
                self.warnings.append("PLC directory not found")
                return
                
            # Look for global variables file first
            global_vars_file = os.path.join(plc_dir, 'global_vars.st')
            if os.path.exists(global_vars_file):
                with open(global_vars_file, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    self._parse_io_from_global_vars(content)
            
            # Look in controller files for I/O references
            controller_files = [
                os.path.join(plc_dir, 'intake_controller.st'),
                os.path.join(plc_dir, 'treatment_controller.st'),
                os.path.join(plc_dir, 'dosing_controller.st'),
                os.path.join(plc_dir, 'aeration_controller.st'),
                os.path.join(plc_dir, 'monitoring_controller.st')
            ]
            
            for file_path in controller_files:
                if os.path.exists(file_path):
                    controller_name = os.path.basename(file_path).replace('_controller.st', '')
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        self._parse_io_from_controller(content, controller_name)
        except Exception as e:
            self.warnings.append(f"Error extracting I/O from PLC code: {str(e)}")
    
    def _parse_io_from_global_vars(self, content):
        """Parse I/O tags from global variables file."""
        # Example patterns for different PLC platforms
        # These are simplified and might need adjustment based on actual code
        
        # Look for variable declarations with I/O addresses
        patterns = [
            # Siemens S7 style: %I0.0, %Q0.1, etc.
            r'([\w_]+)\s*AT\s*(%[IQ][\d\.]+)',
            
            # Allen-Bradley style: Local:1:I.Data[0], Local:2:O.Data[1]
            r'([\w_]+)\s*:\s*(Local:\d+:[IO]\.Data\[\d+\])',
            
            # Generic style with comments
            r'([\w_]+)\s*:\s*BOOL\s*;\s*//\s*([IQ][\d\.]+)'
        ]
        
        io_map = defaultdict(dict)
        
        for pattern in patterns:
            matches = re.finditer(pattern, content, re.MULTILINE)
            for match in matches:
                tag_name = match.group(1)
                address = match.group(2)
                
                # Determine I/O type
                io_type = None
                if 'I' in address or 'Input' in address or 'input' in address:
                    if 'Ana' in address or 'AI' in address or '.Data' in address:
                        io_type = 'ai'
                    else:
                        io_type = 'di'
                elif 'Q' in address or 'O' in address or 'Output' in address or 'output' in address:
                    if 'Ana' in address or 'AQ' in address or '.Data' in address:
                        io_type = 'ao'
                    else:
                        io_type = 'do'
                
                if io_type:
                    io_map[io_type][tag_name] = address
        
        # Store parsed I/O mappings
        self.io_tags = dict(io_map)
    
    def _parse_io_from_controller(self, content, controller_name):
        """Parse I/O usage from controller files."""
        # Look for access to variables that might be I/O
        if controller_name not in self.io_config:
            self.io_config[controller_name] = {}
        
        # This is a simplistic approach - in reality would need more sophisticated parsing
        # based on the actual PLC code structure
        io_types = ['di', 'do', 'ai', 'ao']
        
        for io_type in io_types:
            required_tags = self.required_io.get(controller_name, {}).get(io_type, [])
            for tag in required_tags:
                # Simple check for tag usage in the controller code
                # In real implementation, would need to check for actual references to I/O
                pattern = r'\b' + re.escape(tag) + r'\b'
                if re.search(pattern, content, re.IGNORECASE):
                    if io_type not in self.io_config[controller_name]:
                        self.io_config[controller_name][io_type] = []
                    self.io_config[controller_name][io_type].append(tag)
    
    def validate_io_configuration(self):
        """Validate the I/O configuration against hardware and requirements."""
        results = {
            'status': 'passed',
            'errors': [],
            'warnings': [],
            'details': {}
        }
        
        # Get hardware configuration
        hw_di_count = int(self.plc_config.get('IO_Configuration', 'digitalinputs', fallback=0))
        hw_do_count = int(self.plc_config.get('IO_Configuration', 'digitaloutputs', fallback=0))
        hw_ai_count = int(self.plc_config.get('IO_Configuration', 'analoginputs', fallback=0))
        hw_ao_count = int(self.plc_config.get('IO_Configuration', 'analogoutputs', fallback=0))
        
        # Count required I/O
        required_io_counts = {
            'di': 0,
            'do': 0,
            'ai': 0,
            'ao': 0
        }
        
        for component, io_types in self.required_io.items():
            for io_type, tags in io_types.items():
                required_io_counts[io_type] += len(tags)
        
        # Check if hardware has enough I/O
        if required_io_counts['di'] > hw_di_count:
            results['errors'].append(f"Insufficient digital inputs: {hw_di_count} available, {required_io_counts['di']} required")
            results['status'] = 'failed'
        
        if required_io_counts['do'] > hw_do_count:
            results['errors'].append(f"Insufficient digital outputs: {hw_do_count} available, {required_io_counts['do']} required")
            results['status'] = 'failed'
        
        if required_io_counts['ai'] > hw_ai_count:
            results['errors'].append(f"Insufficient analog inputs: {hw_ai_count} available, {required_io_counts['ai']} required")
            results['status'] = 'failed'
        
        if required_io_counts['ao'] > hw_ao_count:
            results['errors'].append(f"Insufficient analog outputs: {hw_ao_count} available, {required_io_counts['ao']} required")
            results['status'] = 'failed'
        
        # Store counts in details
        results['details']['hardware'] = {
            'digital_inputs': hw_di_count,
            'digital_outputs': hw_do_count,
            'analog_inputs': hw_ai_count,
            'analog_outputs': hw_ao_count
        }
        
        results['details']['required'] = required_io_counts
        
        # Check for specific required I/O points
        missing_io = defaultdict(list)
        
        # If we have I/O tags configuration, check against requirements
        if self.io_tags:
            for component, io_types in self.required_io.items():
                for io_type, required_tags in io_types.items():
                    configured_tags = list(self.io_tags.get(io_type, {}).keys())
                    
                    # Check for each required tag if there's a matching configured tag
                    for req_tag in required_tags:
                        found = False
                        for cfg_tag in configured_tags:
                            if req_tag.lower() in cfg_tag.lower():
                                found = True
                                break
                        
                        if not found:
                            missing_io[component].append(f"{io_type.upper()}: {req_tag}")
        else:
            # No detailed I/O config, just note this as a warning
            results['warnings'].append("No detailed I/O tag configuration found. Cannot validate specific I/O points.")
        
        # Add missing I/O details
        if missing_io:
            for component, missing_tags in missing_io.items():
                if missing_tags:
                    results['warnings'].append(f"Component '{component}' is missing I/O tags: {', '.join(missing_tags)}")
            
            results['details']['missing_io'] = dict(missing_io)
        
        # Check for duplicate I/O assignments
        if self.io_tags:
            duplicates = self._check_duplicate_io()
            if duplicates:
                for io_type, dupes in duplicates.items():
                    for address, tags in dupes.items():
                        results['errors'].append(f"Duplicate {io_type.upper()} address {address} used by tags: {', '.join(tags)}")
                
                results['details']['duplicate_io'] = duplicates
                results['status'] = 'failed'
        
        # Add errors and warnings from the class
        results['errors'].extend(self.errors)
        results['warnings'].extend(self.warnings)
        
        if results['errors']:
            results['status'] = 'failed'
        
        return results
    
    def _check_duplicate_io(self):
        """Check for duplicate I/O addresses."""
        duplicates = {}
        
        for io_type, tags in self.io_tags.items():
            address_map = defaultdict(list)
            
            for tag, address in tags.items():
                address_map[address].append(tag)
            
            type_duplicates = {addr: tags for addr, tags in address_map.items() if len(tags) > 1}
            if type_duplicates:
                duplicates[io_type] = type_duplicates
        
        return duplicates
    
    def generate_io_report(self):
        """Generate a comprehensive I/O report."""
        validation_results = self.validate_io_configuration()
        
        # Create a full report with validation results and configuration details
        report = {
            'validation': validation_results,
            'io_configuration': self._format_io_config_for_report(),
            'io_tags': self.io_tags,
            'required_io': self.required_io
        }
        
        return report
    
    def _format_io_config_for_report(self):
        """Format I/O configuration for the report."""
        formatted_config = {}
        
        # Format by controller and I/O type
        for controller, config in self.io_config.items():
            formatted_config[controller] = {}
            
            for io_type in ['di', 'do', 'ai', 'ao']:
                if io_type in config:
                    formatted_config[controller][io_type] = config[io_type]
        
        return formatted_config
    
    def save_report(self, output_file):
        """Save the I/O report to a JSON file."""
        try:
            report = self.generate_io_report()
            
            with open(output_file, 'w') as f:
                json.dump(report, f, indent=2)
            
            return True
        except Exception as e:
            print(f"Error saving report: {str(e)}")
            return False
    
    def generate_io_mapping_file(self, output_file):
        """Generate an I/O mapping configuration file based on requirements."""
        try:
            config = configparser.ConfigParser()
            
            # Add a header section with metadata
            config['METADATA'] = {
                'generated_by': 'IOValidator',
                'date': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'description': 'Generated I/O mapping configuration for WWTP'
            }
            
            # Create sections for each I/O type
            io_types = ['DIGITAL_INPUTS', 'DIGITAL_OUTPUTS', 'ANALOG_INPUTS', 'ANALOG_OUTPUTS']
            for io_type in io_types:
                config[io_type] = {}
            
            # Add required I/O points by component
            address_counter = {
                'di': 0,
                'do': 0,
                'ai': 0,
                'ao': 0
            }
            
            for component, io_types in self.required_io.items():
                for io_type, tags in io_types.items():
                    section_name = {
                        'di': 'DIGITAL_INPUTS',
                        'do': 'DIGITAL_OUTPUTS',
                        'ai': 'ANALOG_INPUTS',
                        'ao': 'ANALOG_OUTPUTS'
                    }[io_type]
                    
                    for tag in tags:
                        tag_name = f"{component}_{tag}"
                        
                        # Generate a placeholder address
                        if io_type in ['di', 'do']:
                            address = f"%{io_type.upper()[0]}{address_counter[io_type]//8}.{address_counter[io_type]%8}"
                        else:
                            address = f"%{io_type.upper()[0]}{address_counter[io_type]}"
                        
                        config[section_name][tag_name] = address
                        address_counter[io_type] += 1
            
            # Write the configuration file
            with open(output_file, 'w') as f:
                config.write(f)
            
            return True
        except Exception as e:
            print(f"Error generating I/O mapping file: {str(e)}")
            return False


if __name__ == "__main__":
    import argparse
    import datetime
    
    parser = argparse.ArgumentParser(description='Validate I/O configuration for WWTP')
    parser.add_argument('--project-root', '-p', type=str, 
                       default=os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')),
                       help='Path to project root directory')
    parser.add_argument('--output', '-o', type=str, default=None,
                       help='Output file path for validation report')
    parser.add_argument('--generate-mapping', '-g', type=str, default=None,
                       help='Generate an I/O mapping file at the specified path')
    
    args = parser.parse_args()
    
    validator = IOValidator(args.project_root)
    
    if not validator.load_configs():
        print("Error: Failed to load configurations")
        sys.exit(1)
    
    results = validator.validate_io_configuration()
    
    # Print summary
    print("\nI/O Configuration Validation Results:")
    print("=" * 40)
    print(f"Status: {results['status'].upper()}")
    
    if results['errors']:
        print("\nErrors:")
        for i, error in enumerate(results['errors'], 1):
            print(f"{i}. {error}")
    
    if results['warnings']:
        print("\nWarnings:")
        for i, warning in enumerate(results['warnings'], 1):
            print(f"{i}. {warning}")
    
    # Print hardware vs. required summary
    if 'details' in results and 'hardware' in results['details'] and 'required' in results['details']:
        hw = results['details']['hardware']
        req = results['details']['required']
        
        print("\nI/O Point Summary:")
        print("-" * 30)
        print(f"Digital Inputs:  {req['di']} required, {hw['digital_inputs']} available")
        print(f"Digital Outputs: {req['do']} required, {hw['digital_outputs']} available")
        print(f"Analog Inputs:   {req['ai']} required, {hw['analog_inputs']} available")
        print(f"Analog Outputs:  {req['ao']} required, {hw['analog_outputs']} available")
    
    # Save report if requested
    if args.output:
        if validator.save_report(args.output):
            print(f"\nReport saved to {args.output}")
        else:
            print(f"\nFailed to save report")
    
    # Generate I/O mapping file if requested
    if args.generate_mapping:
        if validator.generate_io_mapping_file(args.generate_mapping):
            print(f"\nI/O mapping file generated at {args.generate_mapping}")
        else:
            print(f"\nFailed to generate I/O mapping file")
    
    # Exit with appropriate code
    sys.exit(0 if results['status'] == 'passed' else 1)
