#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Configuration Validator for Wastewater Treatment Plant
-----------------------------------------------------
This utility validates configuration files and system settings to ensure they
meet requirements and specifications.
"""

import os
import sys
import configparser
import json
import re
from collections import defaultdict


class ConfigValidator:
    """Validates system configurations against specifications and requirements."""
    
    def __init__(self, project_root):
        self.project_root = project_root
        self.config_files = {}
        self.validation_results = {}
        self.errors = []
        self.warnings = []
    
    def load_config_files(self):
        """Load all relevant configuration files."""
        config_dir = os.path.join(self.project_root, 'config')
        
        try:
            # Load PLC config
            plc_config = configparser.ConfigParser()
            plc_config.read(os.path.join(config_dir, 'plc_config.ini'))
            self.config_files['plc_config'] = plc_config
            
            # Load WWTP config
            wwtp_config = configparser.ConfigParser()
            wwtp_config.read(os.path.join(config_dir, 'wwtp_config.ini'))
            self.config_files['wwtp_config'] = wwtp_config
            
            # Check if files were loaded successfully
            if not plc_config.sections() or not wwtp_config.sections():
                self.errors.append("Failed to load one or more configuration files")
                return False
                
            return True
        except Exception as e:
            self.errors.append(f"Error loading configuration files: {str(e)}")
            return False
    
    def validate_plc_config(self):
        """Validate PLC configuration."""
        results = {
            'status': 'passed',
            'errors': [],
            'warnings': []
        }
        
        try:
            config = self.config_files['plc_config']
            
            # Check required sections
            required_sections = ['System', 'PLC', 'Communication', 'IO_Configuration']
            for section in required_sections:
                if not config.has_section(section):
                    results['errors'].append(f"Missing required section: {section}")
                    results['status'] = 'failed'
            
            # Check PLC IP address format
            if config.has_section('PLC') and 'ip' in config['PLC']:
                ip = config['PLC']['ip']
                if not re.match(r'^(\d{1,3}\.){3}\d{1,3}$', ip):
                    results['errors'].append(f"Invalid IP address format: {ip}")
                    results['status'] = 'failed'
            
            # Check IO configuration
            if config.has_section('IO_Configuration'):
                io_section = config['IO_Configuration']
                # Verify digital inputs/outputs are integers
                for io_type in ['digitalinputs', 'digitaloutputs', 'analoginputs', 'analogoutputs']:
                    if io_type in io_section:
                        try:
                            int(io_section[io_type])
                        except ValueError:
                            results['errors'].append(f"Invalid {io_type} value: {io_section[io_type]}")
                            results['status'] = 'failed'
            
            # Check program timing parameters
            if config.has_section('Program'):
                prog_section = config['Program']
                # Verify cycle times are reasonable
                if 'maincycle' in prog_section:
                    try:
                        main_cycle = int(prog_section['maincycle'])
                        if main_cycle < 10 or main_cycle > 1000:
                            results['warnings'].append(
                                f"Main cycle time ({main_cycle}ms) outside recommended range (10-1000ms)"
                            )
                    except ValueError:
                        results['errors'].append(f"Invalid main cycle time: {prog_section['maincycle']}")
                        results['status'] = 'failed'
            
            # Check HMI configuration
            if config.has_section('HMI'):
                hmi_section = config['HMI']
                if 'updaterate' in hmi_section:
                    try:
                        update_rate = int(hmi_section['updaterate'])
                        if update_rate < 100:
                            results['warnings'].append(
                                f"HMI update rate ({update_rate}ms) is very fast"
                            )
                    except ValueError:
                        results['errors'].append(f"Invalid HMI update rate: {hmi_section['updaterate']}")
                        results['status'] = 'failed'
            
            self.validation_results['plc_config'] = results
            return results['status'] == 'passed'
        except Exception as e:
            self.errors.append(f"Error validating PLC configuration: {str(e)}")
            self.validation_results['plc_config'] = {
                'status': 'error',
                'errors': [str(e)],
                'warnings': []
            }
            return False
    
    def validate_wwtp_config(self):
        """Validate WWTP configuration."""
        results = {
            'status': 'passed',
            'errors': [],
            'warnings': []
        }
        
        try:
            config = self.config_files['wwtp_config']
            
            # Check required sections
            required_sections = ['System', 'Process_Parameters', 'Tank_Configuration']
            for section in required_sections:
                if not config.has_section(section):
                    results['errors'].append(f"Missing required section: {section}")
                    results['status'] = 'failed'
            
            # Check system capacity
            if config.has_section('System') and 'capacity' in config['System']:
                try:
                    capacity = float(config['System']['capacity'])
                    if capacity <= 0:
                        results['errors'].append(f"Invalid system capacity: {capacity}")
                        results['status'] = 'failed'
                except ValueError:
                    results['errors'].append(f"Invalid system capacity: {config['System']['capacity']}")
                    results['status'] = 'failed'
            
            # Check process parameters
            if config.has_section('Process_Parameters'):
                params = config['Process_Parameters']
                # Check pH range
                if all(key in params for key in ['minph', 'maxph']):
                    try:
                        min_ph = float(params['minph'])
                        max_ph = float(params['maxph'])
                        
                        if min_ph < 0 or max_ph > 14 or min_ph >= max_ph:
                            results['errors'].append(f"Invalid pH range: {min_ph}-{max_ph}")
                            results['status'] = 'failed'
                    except ValueError:
                        results['errors'].append("Invalid pH values")
                        results['status'] = 'failed'
                
                # Check dissolved oxygen
                if 'minimumdissolvedoxygen' in params:
                    try:
                        min_do = float(params['minimumdissolvedoxygen'])
                        if min_do <= 0:
                            results['warnings'].append(
                                f"Minimum dissolved oxygen ({min_do}) is very low"
                            )
                    except ValueError:
                        results['errors'].append(
                            f"Invalid minimum dissolved oxygen: {params['minimumdissolvedoxygen']}"
                        )
                        results['status'] = 'failed'
            
            # Check tank configuration
            if config.has_section('Tank_Configuration'):
                tank_config = config['Tank_Configuration']
                # Check tank capacities
                for key, value in tank_config.items():
                    if 'capacity' in key.lower():
                        try:
                            capacity = float(value)
                            if capacity <= 0:
                                results['errors'].append(f"Invalid tank capacity ({key}): {capacity}")
                                results['status'] = 'failed'
                        except ValueError:
                            results['errors'].append(f"Invalid tank capacity ({key}): {value}")
                            results['status'] = 'failed'
                
                # Make sure each tank has a corresponding height parameter
                for key in list(tank_config.keys()):
                    if 'capacity' in key.lower() and key.lower().replace('capacity', 'height') not in map(str.lower, tank_config.keys()):
                        results['warnings'].append(f"Missing height parameter for {key}")
            
            # Check PID parameters
            if config.has_section('PID_Parameters'):
                pid_params = config['PID_Parameters']
                for key, value in pid_params.items():
                    try:
                        param_value = float(value)
                        # Check if P terms are negative
                        if '_p' in key.lower() and param_value < 0:
                            results['errors'].append(f"Negative P gain in PID parameter ({key}): {param_value}")
                            results['status'] = 'failed'
                        # Check if I terms are negative
                        elif '_i' in key.lower() and param_value < 0:
                            results['errors'].append(f"Negative I gain in PID parameter ({key}): {param_value}")
                            results['status'] = 'failed'
                    except ValueError:
                        results['errors'].append(f"Invalid PID parameter ({key}): {value}")
                        results['status'] = 'failed'
            
            self.validation_results['wwtp_config'] = results
            return results['status'] == 'passed'
        except Exception as e:
            self.errors.append(f"Error validating WWTP configuration: {str(e)}")
            self.validation_results['wwtp_config'] = {
                'status': 'error',
                'errors': [str(e)],
                'warnings': []
            }
            return False
    
    def cross_validate_configs(self):
        """Perform cross-validation between configurations."""
        results = {
            'status': 'passed',
            'errors': [],
            'warnings': []
        }
        
        try:
            plc_config = self.config_files['plc_config']
            wwtp_config = self.config_files['wwtp_config']
            
            # Check if system names are consistent
            if plc_config.has_section('System') and 'name' in plc_config['System'] and \
               wwtp_config.has_section('System') and 'name' in wwtp_config['System']:
                plc_name = plc_config['System']['name']
                wwtp_name = wwtp_config['System']['name']
                
                if plc_name != wwtp_name and not (plc_name in wwtp_name or wwtp_name in plc_name):
                    results['warnings'].append(
                        f"System name mismatch: '{plc_name}' vs '{wwtp_name}'"
                    )
            
            # Check if IO configuration matches process requirements
            if plc_config.has_section('IO_Configuration') and 'analoginputs' in plc_config['IO_Configuration']:
                try:
                    ai_count = int(plc_config['IO_Configuration']['analoginputs'])
                    
                    # Estimate required analog inputs based on process parameters
                    required_ai = 0
                    if wwtp_config.has_section('Process_Parameters'):
                        # Each parameter that needs monitoring adds a required input
                        for param in ['minph', 'maxph', 'mindissolvedoxygen', 'maxturbidity']:
                            if param in wwtp_config['Process_Parameters']:
                                required_ai += 1
                    
                    # Add inputs for tank level monitoring
                    if wwtp_config.has_section('Tank_Configuration'):
                        for key in wwtp_config['Tank_Configuration']:
                            if 'capacity' in key.lower():
                                required_ai += 1
                    
                    # Check if we have enough analog inputs
                    if ai_count < required_ai:
                        results['warnings'].append(
                            f"Potentially insufficient analog inputs: {ai_count} configured, ~{required_ai} estimated"
                        )
                except ValueError:
                    pass  # Already caught in PLC validation
            
            self.validation_results['cross_validation'] = results
            return results['status'] == 'passed'
        except Exception as e:
            self.errors.append(f"Error in cross-validation: {str(e)}")
            self.validation_results['cross_validation'] = {
                'status': 'error',
                'errors': [str(e)],
                'warnings': []
            }
            return False
    
    def get_overall_result(self):
        """Get the overall validation result."""
        has_errors = False
        
        for category, result in self.validation_results.items():
            if result['status'] in ['failed', 'error']:
                has_errors = True
                self.errors.extend(result['errors'])
            self.warnings.extend(result['warnings'])
        
        return {
            'status': 'failed' if has_errors else 'passed',
            'errors': self.errors,
            'warnings': self.warnings,
            'details': self.validation_results
        }
    
    def validate_all(self):
        """Run all validation checks."""
        if not self.load_config_files():
            return {
                'status': 'error',
                'errors': self.errors,
                'warnings': [],
                'details': {}
            }
        
        self.validate_plc_config()
        self.validate_wwtp_config()
        self.cross_validate_configs()
        
        return self.get_overall_result()


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Validate WWTP configuration files')
    parser.add_argument('--project-root', '-p', type=str, default=os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')),
                        help='Path to project root directory')
    parser.add_argument('--output', '-o', type=str, default=None,
                        help='Output file path for JSON results')
    parser.add_argument('--verbose', '-v', action='store_true',
                        help='Print detailed validation information')
    
    args = parser.parse_args()
    
    validator = ConfigValidator(args.project_root)
    result = validator.validate_all()
    
    # Output results
    if args.verbose:
        print("\nConfiguration Validation Results:")
        print("=" * 40)
        print(f"Status: {result['status'].upper()}")
        
        if result['errors']:
            print("\nErrors:")
            for i, error in enumerate(result['errors'], 1):
                print(f"{i}. {error}")
        
        if result['warnings']:
            print("\nWarnings:")
            for i, warning in enumerate(result['warnings'], 1):
                print(f"{i}. {warning}")
        
        print("\nDetailed Results:")
        for category, details in result['details'].items():
            print(f"\n{category.replace('_', ' ').title()}:")
            print(f"  Status: {details['status'].upper()}")
            
            if details['errors']:
                print("  Errors:")
                for error in details['errors']:
                    print(f"    - {error}")
            
            if details['warnings']:
                print("  Warnings:")
                for warning in details['warnings']:
                    print(f"    - {warning}")
    else:
        print(f"Validation completed: {result['status'].upper()}")
        print(f"Errors: {len(result['errors'])}")
        print(f"Warnings: {len(result['warnings'])}")
    
    # Save results to file if requested
    if args.output:
        try:
            with open(args.output, 'w') as f:
                json.dump(result, f, indent=2)
            print(f"Results saved to {args.output}")
        except Exception as e:
            print(f"Error saving results: {str(e)}")
            sys.exit(1)
    
    sys.exit(0 if result['status'] == 'passed' else 1)
