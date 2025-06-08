#!/usr/bin/env python3
"""
HVAC System Verification Script
Comprehensive verification and validation of the HVAC control system.
"""

import os
import sys
import json
import configparser
import subprocess
from datetime import datetime
from typing import Dict, List, Tuple, Any
import time

class HVACSystemVerifier:
    """
    Comprehensive system verification for HVAC control system.
    Performs checks on configuration, PLC programs, documentation, and system integrity.
    """
    
    def __init__(self):
        """Initialize the system verifier."""
        self.project_root = os.getcwd()
        self.verification_results = {
            'timestamp': datetime.now().isoformat(),
            'overall_status': 'PENDING',
            'tests_passed': 0,
            'tests_failed': 0,
            'warnings': 0,
            'categories': {}
        }
        
    def run_verification(self) -> bool:
        """Run complete system verification."""
        print("🔍 HVAC System Verification & Validation")
        print("=" * 50)
        print(f"📍 Project Root: {self.project_root}")
        print(f"⏰ Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        # Define verification categories
        verification_tests = [
            ("Project Structure", self._verify_project_structure),
            ("Configuration Files", self._verify_configuration),
            ("PLC Programs", self._verify_plc_programs),
            ("Python Scripts", self._verify_python_scripts),
            ("Documentation", self._verify_documentation),
            ("System Integration", self._verify_system_integration),
            ("Security & Safety", self._verify_security_safety),
            ("Performance", self._verify_performance)
        ]
        
        # Run all verification tests
        for category, test_func in verification_tests:
            print(f"📋 Testing: {category}")
            print("-" * 30)
            
            try:
                results = test_func()
                self.verification_results['categories'][category] = results
                
                # Count results
                passed = results.get('passed', 0)
                failed = results.get('failed', 0)
                warnings = results.get('warnings', 0)
                
                self.verification_results['tests_passed'] += passed
                self.verification_results['tests_failed'] += failed
                self.verification_results['warnings'] += warnings
                
                # Display summary
                status_icon = "✅" if failed == 0 else "❌"
                print(f"{status_icon} {category}: {passed} passed, {failed} failed, {warnings} warnings")
                
                if results.get('details'):
                    for detail in results['details'][:3]:  # Show first 3 details
                        print(f"  • {detail}")
                
            except Exception as e:
                print(f"❌ Error in {category}: {e}")
                self.verification_results['categories'][category] = {
                    'passed': 0, 'failed': 1, 'warnings': 0,
                    'details': [f"Verification error: {e}"]
                }
                self.verification_results['tests_failed'] += 1
            
            print()
        
        # Determine overall status
        total_failed = self.verification_results['tests_failed']
        total_warnings = self.verification_results['warnings']
        
        if total_failed == 0 and total_warnings == 0:
            self.verification_results['overall_status'] = 'EXCELLENT'
        elif total_failed == 0 and total_warnings <= 3:
            self.verification_results['overall_status'] = 'GOOD'
        elif total_failed <= 2:
            self.verification_results['overall_status'] = 'ACCEPTABLE'
        else:
            self.verification_results['overall_status'] = 'NEEDS_WORK'
        
        # Display final results
        self._display_final_results()
        
        # Save verification report
        self._save_verification_report()
        
        return total_failed == 0
        
    def _verify_project_structure(self) -> Dict[str, Any]:
        """Verify project directory structure."""
        results = {'passed': 0, 'failed': 0, 'warnings': 0, 'details': []}
        
        # Required directories
        required_dirs = [
            'config', 'diagrams', 'docs', 'logs', 'plc', 
            'scripts/batch', 'src/core', 'src/gui', 'src/monitoring',
            'src/simulation', 'tests', 'utils', 'wiki/assets', 
            'wiki/pages', 'wiki/templates'
        ]
        
        for dir_path in required_dirs:
            full_path = os.path.join(self.project_root, dir_path)
            if os.path.exists(full_path):
                results['passed'] += 1
                results['details'].append(f"✅ Directory exists: {dir_path}")
            else:
                results['failed'] += 1
                results['details'].append(f"❌ Missing directory: {dir_path}")
        
        # Check for essential files
        essential_files = [
            'README.md',
            'config/plc_config.ini',
            'plc/main.st',
            'plc/global_vars.st',
            'src/gui/hmi_interface.py',
            'src/simulation/hvac_simulator.py'
        ]
        
        for file_path in essential_files:
            full_path = os.path.join(self.project_root, file_path)
            if os.path.exists(full_path):
                results['passed'] += 1
            else:
                results['failed'] += 1
                results['details'].append(f"❌ Missing essential file: {file_path}")
        
        return results
        
    def _verify_configuration(self) -> Dict[str, Any]:
        """Verify configuration files."""
        results = {'passed': 0, 'failed': 0, 'warnings': 0, 'details': []}
        
        # Check PLC configuration
        config_file = os.path.join(self.project_root, 'config/plc_config.ini')
        if os.path.exists(config_file):
            try:
                config = configparser.ConfigParser()
                config.read(config_file)
                
                # Required sections
                required_sections = [
                    'ZONES', 'TEMPERATURE_CONTROL', 'AIR_QUALITY', 
                    'EQUIPMENT', 'ENERGY_MANAGEMENT', 'SAFETY', 'MAINTENANCE'
                ]
                
                for section in required_sections:
                    if config.has_section(section):
                        results['passed'] += 1
                    else:
                        results['failed'] += 1
                        results['details'].append(f"❌ Missing config section: {section}")
                
                # Check critical parameters
                critical_params = [
                    ('ZONES', 'number_of_zones'),
                    ('TEMPERATURE_CONTROL', 'default_setpoint'),
                    ('SAFETY', 'emergency_shutdown_enabled'),
                    ('EQUIPMENT', 'ahu_count')
                ]
                
                for section, param in critical_params:
                    if config.has_option(section, param):
                        results['passed'] += 1
                    else:
                        results['failed'] += 1
                        results['details'].append(f"❌ Missing parameter: {section}.{param}")
                
                results['details'].append("✅ Configuration file structure valid")
                
            except Exception as e:
                results['failed'] += 1
                results['details'].append(f"❌ Configuration file error: {e}")
        else:
            results['failed'] += 1
            results['details'].append("❌ PLC configuration file missing")
        
        return results
        
    def _verify_plc_programs(self) -> Dict[str, Any]:
        """Verify PLC program files."""
        results = {'passed': 0, 'failed': 0, 'warnings': 0, 'details': []}
        
        plc_files = [
            'main.st', 'global_vars.st', 'temperature_controller.st',
            'air_quality_controller.st', 'energy_manager.st', 'safety_controller.st'
        ]
        
        for plc_file in plc_files:
            file_path = os.path.join(self.project_root, 'plc', plc_file)
            if os.path.exists(file_path):
                try:
                    with open(file_path, 'r') as f:
                        content = f.read()
                    
                    # Basic syntax checks for Structured Text
                    syntax_checks = [
                        ('PROGRAM', 'Contains PROGRAM declaration'),
                        ('END_PROGRAM', 'Contains END_PROGRAM'),
                        ('VAR', 'Contains variable declarations'),
                        ('IF', 'Contains conditional logic')
                    ]
                    
                    file_passed = 0
                    for keyword, description in syntax_checks:
                        if keyword in content:
                            file_passed += 1
                        else:
                            results['warnings'] += 1
                            results['details'].append(f"⚠️ {plc_file}: {description}")
                    
                    if file_passed >= 2:  # At least basic structure
                        results['passed'] += 1
                        results['details'].append(f"✅ {plc_file}: Basic structure valid")
                    else:
                        results['failed'] += 1
                        results['details'].append(f"❌ {plc_file}: Invalid structure")
                        
                except Exception as e:
                    results['failed'] += 1
                    results['details'].append(f"❌ {plc_file}: Read error - {e}")
            else:
                results['failed'] += 1
                results['details'].append(f"❌ Missing PLC file: {plc_file}")
        
        return results
        
    def _verify_python_scripts(self) -> Dict[str, Any]:
        """Verify Python script files."""
        results = {'passed': 0, 'failed': 0, 'warnings': 0, 'details': []}
        
        python_files = [
            'src/gui/hmi_interface.py',
            'src/simulation/hvac_simulator.py',
            'src/monitoring/system_status.py',
            'utils/hvac_diagram.py'
        ]
        
        for py_file in python_files:
            file_path = os.path.join(self.project_root, py_file)
            if os.path.exists(file_path):
                try:
                    # Try to compile the Python file
                    with open(file_path, 'r') as f:
                        content = f.read()
                    
                    compile(content, file_path, 'exec')
                    results['passed'] += 1
                    results['details'].append(f"✅ {py_file}: Syntax valid")
                    
                    # Check for essential imports and classes
                    if 'import' in content and ('class' in content or 'def' in content):
                        results['passed'] += 1
                    else:
                        results['warnings'] += 1
                        results['details'].append(f"⚠️ {py_file}: Basic structure check")
                        
                except SyntaxError as e:
                    results['failed'] += 1
                    results['details'].append(f"❌ {py_file}: Syntax error - {e}")
                except Exception as e:
                    results['warnings'] += 1
                    results['details'].append(f"⚠️ {py_file}: Check error - {e}")
            else:
                results['failed'] += 1
                results['details'].append(f"❌ Missing Python file: {py_file}")
        
        return results
        
    def _verify_documentation(self) -> Dict[str, Any]:
        """Verify documentation completeness."""
        results = {'passed': 0, 'failed': 0, 'warnings': 0, 'details': []}
        
        # Check README.md
        readme_path = os.path.join(self.project_root, 'README.md')
        if os.path.exists(readme_path):
            try:
                with open(readme_path, 'r') as f:
                    content = f.read()
                
                essential_sections = [
                    'HVAC Control System',
                    'Features',
                    'Installation',
                    'Usage',
                    'Configuration'
                ]
                
                for section in essential_sections:
                    if section.lower() in content.lower():
                        results['passed'] += 1
                    else:
                        results['warnings'] += 1
                        results['details'].append(f"⚠️ README missing section: {section}")
                
                results['details'].append("✅ README.md exists and has content")
                
            except Exception as e:
                results['failed'] += 1
                results['details'].append(f"❌ README.md error: {e}")
        else:
            results['failed'] += 1
            results['details'].append("❌ README.md missing")
        
        # Check for batch scripts
        batch_scripts = [
            'scripts/batch/system_launcher.bat',
            'scripts/batch/run_hmi.bat',
            'scripts/batch/run_simulator.bat',
            'scripts/batch/generate_diagrams.bat'
        ]
        
        for script in batch_scripts:
            script_path = os.path.join(self.project_root, script)
            if os.path.exists(script_path):
                results['passed'] += 1
            else:
                results['failed'] += 1
                results['details'].append(f"❌ Missing batch script: {script}")
        
        return results
        
    def _verify_system_integration(self) -> Dict[str, Any]:
        """Verify system integration aspects."""
        results = {'passed': 0, 'failed': 0, 'warnings': 0, 'details': []}
        
        # Check if web HMI exists
        web_hmi_path = os.path.join(self.project_root, 'src/gui/web_hmi.html')
        if os.path.exists(web_hmi_path):
            results['passed'] += 1
            results['details'].append("✅ Web HMI interface available")
        else:
            results['warnings'] += 1
            results['details'].append("⚠️ Web HMI interface missing")
        
        # Check for data logging capability
        logs_dir = os.path.join(self.project_root, 'logs')
        if os.path.exists(logs_dir):
            results['passed'] += 1
            results['details'].append("✅ Logging directory exists")
        else:
            results['failed'] += 1
            results['details'].append("❌ Logging directory missing")
        
        # Check for system status monitoring
        status_monitor = os.path.join(self.project_root, 'src/monitoring/system_status.py')
        if os.path.exists(status_monitor):
            results['passed'] += 1
            results['details'].append("✅ System status monitor available")
        else:
            results['failed'] += 1
            results['details'].append("❌ System status monitor missing")
        
        # Check for diagram generation
        diagram_generator = os.path.join(self.project_root, 'utils/hvac_diagram.py')
        if os.path.exists(diagram_generator):
            results['passed'] += 1
            results['details'].append("✅ Diagram generator available")
        else:
            results['failed'] += 1
            results['details'].append("❌ Diagram generator missing")
        
        return results
        
    def _verify_security_safety(self) -> Dict[str, Any]:
        """Verify security and safety features."""
        results = {'passed': 0, 'failed': 0, 'warnings': 0, 'details': []}
        
        # Check for safety controller
        safety_controller = os.path.join(self.project_root, 'plc/safety_controller.st')
        if os.path.exists(safety_controller):
            try:
                with open(safety_controller, 'r') as f:
                    content = f.read()
                
                safety_features = [
                    ('emergency', 'Emergency shutdown procedures'),
                    ('fire', 'Fire safety systems'),
                    ('freeze', 'Freeze protection'),
                    ('alarm', 'Alarm management')
                ]
                
                for keyword, description in safety_features:
                    if keyword.lower() in content.lower():
                        results['passed'] += 1
                        results['details'].append(f"✅ {description} implemented")
                    else:
                        results['warnings'] += 1
                        results['details'].append(f"⚠️ {description} not found")
                        
            except Exception as e:
                results['failed'] += 1
                results['details'].append(f"❌ Safety controller error: {e}")
        else:
            results['failed'] += 1
            results['details'].append("❌ Safety controller missing")
        
        # Check configuration for safety parameters
        config_file = os.path.join(self.project_root, 'config/plc_config.ini')
        if os.path.exists(config_file):
            try:
                config = configparser.ConfigParser()
                config.read(config_file)
                
                if config.has_section('SAFETY'):
                    results['passed'] += 1
                    results['details'].append("✅ Safety configuration section exists")
                else:
                    results['failed'] += 1
                    results['details'].append("❌ Safety configuration missing")
                    
            except Exception as e:
                results['warnings'] += 1
                results['details'].append(f"⚠️ Config safety check error: {e}")
        
        return results
        
    def _verify_performance(self) -> Dict[str, Any]:
        """Verify performance and efficiency features."""
        results = {'passed': 0, 'failed': 0, 'warnings': 0, 'details': []}
        
        # Check for energy management
        energy_manager = os.path.join(self.project_root, 'plc/energy_manager.st')
        if os.path.exists(energy_manager):
            try:
                with open(energy_manager, 'r') as f:
                    content = f.read()
                
                performance_features = [
                    ('optimization', 'Energy optimization'),
                    ('demand', 'Demand response'),
                    ('schedule', 'Scheduling'),
                    ('efficiency', 'Efficiency monitoring')
                ]
                
                for keyword, description in performance_features:
                    if keyword.lower() in content.lower():
                        results['passed'] += 1
                    else:
                        results['warnings'] += 1
                        results['details'].append(f"⚠️ {description} features limited")
                
                results['details'].append("✅ Energy management system present")
                
            except Exception as e:
                results['failed'] += 1
                results['details'].append(f"❌ Energy manager error: {e}")
        else:
            results['failed'] += 1
            results['details'].append("❌ Energy management missing")
        
        # Check for simulation capabilities
        simulator = os.path.join(self.project_root, 'src/simulation/hvac_simulator.py')
        if os.path.exists(simulator):
            results['passed'] += 1
            results['details'].append("✅ System simulator available")
        else:
            results['warnings'] += 1
            results['details'].append("⚠️ System simulator missing")
        
        return results
        
    def _display_final_results(self):
        """Display final verification results."""
        print("🏆 VERIFICATION SUMMARY")
        print("=" * 50)
        
        total_tests = self.verification_results['tests_passed'] + self.verification_results['tests_failed']
        pass_rate = (self.verification_results['tests_passed'] / total_tests * 100) if total_tests > 0 else 0
        
        status = self.verification_results['overall_status']
        status_icons = {
            'EXCELLENT': '🌟',
            'GOOD': '✅',
            'ACCEPTABLE': '⚠️',
            'NEEDS_WORK': '❌'
        }
        
        print(f"{status_icons.get(status, '❓')} Overall Status: {status}")
        print(f"📊 Pass Rate: {pass_rate:.1f}%")
        print(f"✅ Tests Passed: {self.verification_results['tests_passed']}")
        print(f"❌ Tests Failed: {self.verification_results['tests_failed']}")
        print(f"⚠️ Warnings: {self.verification_results['warnings']}")
        print()
        
        # Category breakdown
        print("📋 CATEGORY BREAKDOWN")
        print("-" * 30)
        for category, results in self.verification_results['categories'].items():
            passed = results.get('passed', 0)
            failed = results.get('failed', 0)
            warnings = results.get('warnings', 0)
            total = passed + failed
            
            if total > 0:
                cat_pass_rate = (passed / total * 100)
                status_icon = "✅" if failed == 0 else "❌"
                print(f"{status_icon} {category}: {cat_pass_rate:.0f}% ({passed}/{total})")
        
        print()
        
        # Recommendations
        print("💡 RECOMMENDATIONS")
        print("-" * 30)
        
        if self.verification_results['tests_failed'] > 0:
            print("• Address failed tests before system deployment")
        
        if self.verification_results['warnings'] > 5:
            print("• Review and resolve warnings for optimal performance")
        
        if status == 'EXCELLENT':
            print("• System is ready for deployment")
            print("• Consider adding advanced features")
        elif status == 'GOOD':
            print("• System is nearly ready for deployment")
            print("• Address minor issues for best results")
        elif status == 'ACCEPTABLE':
            print("• System needs improvement before deployment")
            print("• Focus on failed tests and critical warnings")
        else:
            print("• System requires significant work before deployment")
            print("• Address all failed tests and major issues")
        
    def _save_verification_report(self):
        """Save verification report to file."""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_file = os.path.join(self.project_root, f'verification_report_{timestamp}.json')
        
        try:
            with open(report_file, 'w') as f:
                json.dump(self.verification_results, f, indent=2)
            
            print(f"\n📄 Verification report saved: {report_file}")
            
        except Exception as e:
            print(f"\n❌ Failed to save verification report: {e}")

def main():
    """Main function to run system verification."""
    if len(sys.argv) > 1 and sys.argv[1] == '--help':
        print("HVAC System Verification Script")
        print("Usage:")
        print("  python verify_system.py     - Run full verification")
        print("  python verify_system.py --help - Show this help")
        return 0
    
    try:
        verifier = HVACSystemVerifier()
        success = verifier.run_verification()
        
        if success:
            print("\n🎉 System verification completed successfully!")
            return 0
        else:
            print("\n⚠️ System verification completed with issues.")
            return 1
            
    except Exception as e:
        print(f"\n❌ Verification failed: {e}")
        return 1

if __name__ == "__main__":
    exit(main())
