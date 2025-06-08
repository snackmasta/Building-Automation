#!/usr/bin/env python3
"""
HVAC System Verification Script
Comprehensive system check and validation tool
"""

import os
import sys
import json
import configparser
import platform
from pathlib import Path
from datetime import datetime

class SystemVerification:
    def __init__(self, base_path=None):
        self.base_path = Path(base_path) if base_path else Path(__file__).parent
        self.results = {
            'timestamp': datetime.now().isoformat(),
            'system_info': self._get_system_info(),
            'checks': [],
            'summary': {'pass': 0, 'fail': 0, 'warning': 0, 'total': 0}
        }
        
    def _get_system_info(self):
        """Get system information"""
        return {
            'platform': platform.platform(),
            'python_version': sys.version,
            'base_path': str(self.base_path.absolute()),
            'working_directory': os.getcwd()
        }
    
    def add_check(self, name, status, message, category='General'):
        """Add a check result"""
        check = {
            'name': name,
            'category': category,
            'status': status,
            'message': message
        }
        self.results['checks'].append(check)
        self.results['summary'][status.lower()] += 1
        self.results['summary']['total'] += 1
        
        # Print real-time results
        status_symbol = {'PASS': '✓', 'FAIL': '✗', 'WARNING': '⚠'}.get(status, '?')
        print(f"[{status_symbol}] {category}: {name} - {message}")
        
    def check_directory_structure(self):
        """Verify directory structure"""
        required_dirs = [
            'config', 'scripts', 'scripts/batch', 'scripts/python',
            'docs', 'wiki', 'wiki/pages', 'wiki/templates',
            'logs', 'utils', 'data', 'backup'
        ]
        
        for dir_path in required_dirs:
            full_path = self.base_path / dir_path
            if full_path.exists():
                self.add_check(f"Directory: {dir_path}", 'PASS', 'Directory exists', 'Directory Structure')
            else:
                self.add_check(f"Directory: {dir_path}", 'FAIL', 'Directory missing', 'Directory Structure')
                try:
                    full_path.mkdir(parents=True, exist_ok=True)
                    self.add_check(f"Auto-create: {dir_path}", 'PASS', 'Directory created automatically', 'Directory Structure')
                except Exception as e:
                    self.add_check(f"Auto-create: {dir_path}", 'FAIL', f'Failed to create directory: {e}', 'Directory Structure')
    
    def check_core_files(self):
        """Check for core system files"""
        core_files = {
            'config/plc_config.ini': 'PLC Configuration File',
            'config/hmi_config.ini': 'HMI Configuration File',
            'main_controller.py': 'Main Controller Script',
            'system_status.py': 'System Status Monitor',
            'web_hmi.html': 'Web HMI Interface',
            'docs/Maintenance_Manual.md': 'Maintenance Manual',
            'wiki/Home.md': 'Wiki Home Page'
        }
        
        for file_path, description in core_files.items():
            full_path = self.base_path / file_path
            if full_path.exists():
                file_size = full_path.stat().st_size
                self.add_check(description, 'PASS', f'File exists ({file_size} bytes)', 'Core Files')
            else:
                self.add_check(description, 'FAIL', 'File missing', 'Core Files')
    
    def check_configuration_files(self):
        """Verify configuration files"""
        config_file = self.base_path / 'config' / 'plc_config.ini'
        
        if not config_file.exists():
            self.add_check('PLC Configuration', 'FAIL', 'Configuration file missing', 'Configuration')
            return
            
        try:
            config = configparser.ConfigParser()
            config.read(config_file)
            
            required_sections = [
                'SYSTEM', 'ZONES', 'TEMPERATURE_CONTROL', 'AIR_QUALITY',
                'EQUIPMENT', 'ENERGY_MANAGEMENT', 'SAFETY', 'SCHEDULE',
                'COMMUNICATION', 'ALARMS', 'LOGGING', 'MAINTENANCE', 'CALIBRATION'
            ]
            
            for section in required_sections:
                if config.has_section(section):
                    self.add_check(f'Config Section: {section}', 'PASS', 'Section exists', 'Configuration')
                else:
                    self.add_check(f'Config Section: {section}', 'FAIL', 'Section missing', 'Configuration')
            
            # Check specific critical parameters
            critical_params = [
                ('SYSTEM', 'system_name'),
                ('ZONES', 'zone_count'),
                ('COMMUNICATION', 'hmi_port'),
                ('LOGGING', 'log_file_path')
            ]
            
            for section, param in critical_params:
                if config.has_section(section) and config.has_option(section, param):
                    value = config.get(section, param)
                    self.add_check(f'Config Parameter: {section}.{param}', 'PASS', f'Parameter set to: {value}', 'Configuration')
                else:
                    self.add_check(f'Config Parameter: {section}.{param}', 'FAIL', 'Parameter missing', 'Configuration')
                    
        except Exception as e:
            self.add_check('Configuration File Parse', 'FAIL', f'Error parsing configuration: {e}', 'Configuration')
    
    def run_all_checks(self):
        """Run all verification checks"""
        print("="*60)
        print("HVAC SYSTEM VERIFICATION")
        print("="*60)
        print(f"Base Path: {self.base_path}")
        print(f"Timestamp: {self.results['timestamp']}")
        print(f"Platform: {self.results['system_info']['platform']}")
        print("-"*60)
        
        # Run checks
        self.check_directory_structure()
        self.check_core_files()
        self.check_configuration_files()
        
        # Print summary
        print("-"*60)
        print("VERIFICATION SUMMARY")
        print("-"*60)
        summary = self.results['summary']
        total = summary['total']
        passed = summary['pass']
        failed = summary['fail']
        warnings = summary['warning']
        
        pass_rate = (passed / total * 100) if total > 0 else 0
        
        print(f"Total Checks: {total}")
        print(f"Passed: {passed}")
        print(f"Failed: {failed}")
        print(f"Warnings: {warnings}")
        print(f"Pass Rate: {pass_rate:.1f}%")
        
        if failed > 0:
            print("\nFAILED CHECKS:")
            for check in self.results['checks']:
                if check['status'] == 'FAIL':
                    print(f"  ✗ {check['category']}: {check['name']} - {check['message']}")
        
        return self.results

def main():
    """Main verification function"""
    print("Starting HVAC System Verification...")
    base_path = sys.argv[1] if len(sys.argv) > 1 else None
    print(f"Base path: {base_path}")
    verifier = SystemVerification(base_path)
    results = verifier.run_all_checks()
    
    if results['summary']['fail'] > 0:
        sys.exit(1)
    else:
        sys.exit(0)

if __name__ == "__main__":
    main()
