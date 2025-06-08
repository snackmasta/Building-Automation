"""
System Validator for Car Parking Vending System
Comprehensive validation and testing suite for the complete system
"""

import os
import sys
import json
import time
import logging
from datetime import datetime
from typing import Dict, List, Any

# Add source paths
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SystemValidator:
    """Comprehensive system validation suite"""
    
    def __init__(self):
        self.results = {
            'timestamp': datetime.now().isoformat(),
            'total_tests': 0,
            'passed': 0,
            'failed': 0,
            'errors': 0,
            'components': {},
            'issues': [],
            'recommendations': []
        }
        
    def validate_database_component(self):
        """Validate database management system"""
        logger.info("Validating Database Management System...")
        component_results = {'tests': 0, 'passed': 0, 'failed': 0, 'errors': 0, 'details': []}
        
        try:
            from database.database_manager import DatabaseManager
            
            # Test 1: Database initialization
            try:
                db_manager = DatabaseManager(':memory:')  # Use in-memory database for testing
                component_results['tests'] += 1
                component_results['passed'] += 1
                component_results['details'].append("✓ Database initialization successful")
                
                # Test 2: Table creation validation
                with db_manager.get_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
                    tables = [row[0] for row in cursor.fetchall()]
                    
                expected_tables = ['vehicles', 'parking_spaces', 'transactions', 'system_events', 'users', 'system_settings']
                missing_tables = [table for table in expected_tables if table not in tables]
                
                component_results['tests'] += 1
                if not missing_tables:
                    component_results['passed'] += 1
                    component_results['details'].append("✓ All required tables created")
                else:
                    component_results['failed'] += 1
                    component_results['details'].append(f"✗ Missing tables: {missing_tables}")
                
                # Test 3: Vehicle operations
                vehicle_data = {
                    'plate_number': 'TEST123',
                    'vehicle_type': 'sedan',
                    'length': 4.5,
                    'width': 1.8,
                    'height': 1.6
                }
                
                component_results['tests'] += 1
                try:
                    vehicle_id = db_manager.add_vehicle(vehicle_data)
                    if vehicle_id:
                        component_results['passed'] += 1
                        component_results['details'].append("✓ Vehicle addition successful")
                    else:
                        component_results['failed'] += 1
                        component_results['details'].append("✗ Vehicle addition failed")
                except Exception as e:
                    component_results['errors'] += 1
                    component_results['details'].append(f"✗ Vehicle addition error: {str(e)}")
                
                # Test 4: Parking space operations
                component_results['tests'] += 1
                try:
                    spaces = db_manager.get_available_spaces('sedan')
                    if spaces and len(spaces) > 0:
                        component_results['passed'] += 1
                        component_results['details'].append(f"✓ Available spaces found: {len(spaces)}")
                    else:
                        component_results['failed'] += 1
                        component_results['details'].append("✗ No available spaces found")
                except Exception as e:
                    component_results['errors'] += 1
                    component_results['details'].append(f"✗ Parking space query error: {str(e)}")
                
                db_manager.close()
                
            except Exception as e:
                component_results['errors'] += 1
                component_results['details'].append(f"✗ Database component error: {str(e)}")
                
        except ImportError as e:
            component_results['errors'] += 1
            component_results['details'].append(f"✗ Database module import error: {str(e)}")
            
        self.results['components']['database'] = component_results
        return component_results
        
    def validate_simulation_component(self):
        """Validate parking simulation system"""
        logger.info("Validating Parking Simulation System...")
        component_results = {'tests': 0, 'passed': 0, 'failed': 0, 'errors': 0, 'details': []}
        
        try:
            from simulation.parking_simulator import ParkingSimulator
            
            # Test 1: Simulator initialization
            component_results['tests'] += 1
            try:
                simulator = ParkingSimulator()
                component_results['passed'] += 1
                component_results['details'].append("✓ Simulator initialization successful")
                
                # Test 2: Basic simulation functions
                component_results['tests'] += 1
                try:
                    if hasattr(simulator, 'start_simulation'):
                        component_results['passed'] += 1
                        component_results['details'].append("✓ Simulation methods available")
                    else:
                        component_results['failed'] += 1
                        component_results['details'].append("✗ Missing simulation methods")
                except Exception as e:
                    component_results['errors'] += 1
                    component_results['details'].append(f"✗ Simulation method check error: {str(e)}")
                    
            except Exception as e:
                component_results['errors'] += 1
                component_results['details'].append(f"✗ Simulator initialization error: {str(e)}")
                
        except ImportError as e:
            component_results['errors'] += 1
            component_results['details'].append(f"✗ Simulation module import error: {str(e)}")
            
        self.results['components']['simulation'] = component_results
        return component_results
        
    def validate_communication_component(self):
        """Validate communication protocols"""
        logger.info("Validating Communication Protocols...")
        component_results = {'tests': 0, 'passed': 0, 'failed': 0, 'errors': 0, 'details': []}
        
        try:
            from communication.protocols import CommunicationManager
            
            # Test 1: Communication manager initialization
            component_results['tests'] += 1
            try:
                comm_manager = CommunicationManager()
                component_results['passed'] += 1
                component_results['details'].append("✓ Communication manager initialization successful")
                
                # Test 2: Protocol availability
                component_results['tests'] += 1
                try:
                    if hasattr(comm_manager, 'websocket_server') and hasattr(comm_manager, 'tcp_server'):
                        component_results['passed'] += 1
                        component_results['details'].append("✓ Communication protocols available")
                    else:
                        component_results['failed'] += 1
                        component_results['details'].append("✗ Missing communication protocols")
                except Exception as e:
                    component_results['errors'] += 1
                    component_results['details'].append(f"✗ Protocol check error: {str(e)}")
                    
            except Exception as e:
                component_results['errors'] += 1
                component_results['details'].append(f"✗ Communication manager error: {str(e)}")
                
        except ImportError as e:
            component_results['errors'] += 1
            component_results['details'].append(f"✗ Communication module import error: {str(e)}")
            
        self.results['components']['communication'] = component_results
        return component_results
        
    def validate_security_component(self):
        """Validate security and authentication system"""
        logger.info("Validating Security System...")
        component_results = {'tests': 0, 'passed': 0, 'failed': 0, 'errors': 0, 'details': []}
        
        try:
            from security.authentication import AuthenticationManager
            
            # Test 1: Authentication manager initialization
            component_results['tests'] += 1
            try:
                auth_manager = AuthenticationManager()
                component_results['passed'] += 1
                component_results['details'].append("✓ Authentication manager initialization successful")
                
                # Test 2: Security methods availability
                component_results['tests'] += 1
                try:
                    methods = ['authenticate_user', 'create_user', 'generate_token']
                    missing_methods = [method for method in methods if not hasattr(auth_manager, method)]
                    
                    if not missing_methods:
                        component_results['passed'] += 1
                        component_results['details'].append("✓ All security methods available")
                    else:
                        component_results['failed'] += 1
                        component_results['details'].append(f"✗ Missing security methods: {missing_methods}")
                except Exception as e:
                    component_results['errors'] += 1
                    component_results['details'].append(f"✗ Security method check error: {str(e)}")
                    
            except Exception as e:
                component_results['errors'] += 1
                component_results['details'].append(f"✗ Authentication manager error: {str(e)}")
                
        except ImportError as e:
            component_results['errors'] += 1
            component_results['details'].append(f"✗ Security module import error: {str(e)}")
            
        self.results['components']['security'] = component_results
        return component_results
        
    def validate_configuration_system(self):
        """Validate system configuration management"""
        logger.info("Validating Configuration System...")
        component_results = {'tests': 0, 'passed': 0, 'failed': 0, 'errors': 0, 'details': []}
        
        # Test 1: Configuration files existence
        config_files = [
            os.path.join(os.path.dirname(__file__), '..', 'config', 'system_config.yaml'),
            os.path.join(os.path.dirname(__file__), '..', 'config', 'system_config.py')
        ]
        
        for config_file in config_files:
            component_results['tests'] += 1
            if os.path.exists(config_file):
                component_results['passed'] += 1
                component_results['details'].append(f"✓ Configuration file exists: {os.path.basename(config_file)}")
            else:
                component_results['failed'] += 1
                component_results['details'].append(f"✗ Missing configuration file: {os.path.basename(config_file)}")
        
        # Test 2: Configuration manager
        try:
            sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'config'))
            from system_config import ConfigManager
            
            component_results['tests'] += 1
            try:
                config_manager = ConfigManager()
                component_results['passed'] += 1
                component_results['details'].append("✓ Configuration manager initialization successful")
            except Exception as e:
                component_results['errors'] += 1
                component_results['details'].append(f"✗ Configuration manager error: {str(e)}")
                
        except ImportError as e:
            component_results['errors'] += 1
            component_results['details'].append(f"✗ Configuration module import error: {str(e)}")
            
        self.results['components']['configuration'] = component_results
        return component_results
        
    def validate_file_structure(self):
        """Validate project file structure"""
        logger.info("Validating File Structure...")
        component_results = {'tests': 0, 'passed': 0, 'failed': 0, 'errors': 0, 'details': []}
        
        project_root = os.path.join(os.path.dirname(__file__), '..')
        
        # Required directories
        required_dirs = [
            'src', 'plc', 'hmi', 'docs', 'config', 'tests', 'scripts',
            'src/database', 'src/simulation', 'src/communication', 'src/security',
            'hmi/web', 'docs/technical', 'docs/user'
        ]
        
        for dir_path in required_dirs:
            component_results['tests'] += 1
            full_path = os.path.join(project_root, dir_path)
            if os.path.exists(full_path):
                component_results['passed'] += 1
                component_results['details'].append(f"✓ Directory exists: {dir_path}")
            else:
                component_results['failed'] += 1
                component_results['details'].append(f"✗ Missing directory: {dir_path}")
        
        # Required files
        required_files = [
            'README.md', 'requirements.txt',
            'plc/main.st', 'plc/global_vars.st',
            'hmi/web/index.html', 'hmi/web/styles.css',
            'src/database/database_manager.py',
            'src/simulation/parking_simulator.py'
        ]
        
        for file_path in required_files:
            component_results['tests'] += 1
            full_path = os.path.join(project_root, file_path)
            if os.path.exists(full_path):
                component_results['passed'] += 1
                component_results['details'].append(f"✓ File exists: {file_path}")
            else:
                component_results['failed'] += 1
                component_results['details'].append(f"✗ Missing file: {file_path}")
                
        self.results['components']['file_structure'] = component_results
        return component_results
        
    def run_full_validation(self):
        """Run complete system validation"""
        logger.info("Starting Complete System Validation...")
        start_time = time.time()
        
        # Run all validation components
        validation_components = [
            self.validate_file_structure,
            self.validate_configuration_system,
            self.validate_database_component,
            self.validate_simulation_component,
            self.validate_communication_component,
            self.validate_security_component
        ]
        
        for validator in validation_components:
            try:
                validator()
            except Exception as e:
                logger.error(f"Validation error in {validator.__name__}: {e}")
                
        # Calculate totals
        for component_name, component_results in self.results['components'].items():
            self.results['total_tests'] += component_results['tests']
            self.results['passed'] += component_results['passed']
            self.results['failed'] += component_results['failed']
            self.results['errors'] += component_results['errors']
            
        # Calculate execution time
        self.results['execution_time'] = round(time.time() - start_time, 2)
        
        # Generate recommendations
        self._generate_recommendations()
        
        return self.results
        
    def _generate_recommendations(self):
        """Generate system recommendations based on validation results"""
        recommendations = []
        
        # Check overall success rate
        total_tests = self.results['total_tests']
        passed_tests = self.results['passed']
        
        if total_tests > 0:
            success_rate = (passed_tests / total_tests) * 100
            
            if success_rate >= 90:
                recommendations.append("✅ System validation highly successful - ready for production")
            elif success_rate >= 75:
                recommendations.append("⚠️ System mostly functional - minor issues need attention")
            elif success_rate >= 50:
                recommendations.append("⚠️ System partially functional - significant issues need resolution")
            else:
                recommendations.append("❌ System has major issues - extensive fixes required")
                
        # Component-specific recommendations
        for component_name, component_results in self.results['components'].items():
            if component_results['errors'] > 0:
                recommendations.append(f"🔧 Fix {component_name} component errors")
            if component_results['failed'] > 0:
                recommendations.append(f"📋 Address {component_name} component failures")
                
        # General recommendations
        if self.results['errors'] > 0:
            recommendations.append("🐛 Debug and fix critical errors before deployment")
        if self.results['failed'] > 0:
            recommendations.append("📝 Review and update failing test cases")
            
        self.results['recommendations'] = recommendations
        
    def generate_report(self):
        """Generate validation report"""
        report_dir = os.path.join(os.path.dirname(__file__), '..', 'reports')
        os.makedirs(report_dir, exist_ok=True)
        
        # JSON report
        json_file = os.path.join(report_dir, 'system_validation.json')
        with open(json_file, 'w') as f:
            json.dump(self.results, f, indent=2)
              # Text report
        text_file = os.path.join(report_dir, 'system_validation.txt')
        with open(text_file, 'w', encoding='utf-8') as f:
            f.write("CAR PARKING VENDING SYSTEM - VALIDATION REPORT\n")
            f.write("=" * 60 + "\n\n")
            f.write(f"Generated: {self.results['timestamp']}\n")
            f.write(f"Execution Time: {self.results['execution_time']} seconds\n\n")
            
            f.write("SUMMARY:\n")
            f.write("-" * 20 + "\n")
            f.write(f"Total Tests: {self.results['total_tests']}\n")
            f.write(f"Passed: {self.results['passed']}\n")
            f.write(f"Failed: {self.results['failed']}\n")
            f.write(f"Errors: {self.results['errors']}\n")
            
            if self.results['total_tests'] > 0:
                success_rate = (self.results['passed'] / self.results['total_tests']) * 100
                f.write(f"Success Rate: {success_rate:.1f}%\n\n")
            
            f.write("COMPONENT DETAILS:\n")
            f.write("-" * 30 + "\n")
            for component_name, component_results in self.results['components'].items():
                f.write(f"\n{component_name.upper()}:\n")
                for detail in component_results['details']:
                    f.write(f"  {detail}\n")
                    
            f.write("\nRECOMMENDATIONS:\n")
            f.write("-" * 20 + "\n")
            for recommendation in self.results['recommendations']:
                f.write(f"• {recommendation}\n")
                
        logger.info(f"Validation reports generated: {json_file}, {text_file}")
        return json_file, text_file

if __name__ == "__main__":
    validator = SystemValidator()
    results = validator.run_full_validation()
    
    # Print summary
    print("\n" + "=" * 70)
    print("CAR PARKING VENDING SYSTEM - VALIDATION SUMMARY")
    print("=" * 70)
    print(f"Total Tests: {results['total_tests']}")
    print(f"Passed: {results['passed']}")
    print(f"Failed: {results['failed']}")
    print(f"Errors: {results['errors']}")
    print(f"Execution Time: {results['execution_time']} seconds")
    
    if results['total_tests'] > 0:
        success_rate = (results['passed'] / results['total_tests']) * 100
        print(f"Success Rate: {success_rate:.1f}%")
        
    print("\nRECOMMENDATIONS:")
    for recommendation in results['recommendations']:
        print(f"• {recommendation}")
        
    # Generate detailed reports
    json_file, text_file = validator.generate_report()
    print(f"\nDetailed reports generated:")
    print(f"• JSON: {json_file}")
    print(f"• Text: {text_file}")
