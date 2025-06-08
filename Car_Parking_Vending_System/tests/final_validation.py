"""
Final System Integration Test and Deployment Validation
Complete end-to-end testing and production readiness assessment
"""

import os
import sys
import json
import time
import logging
import tempfile
import threading
from datetime import datetime
from typing import Dict, List, Any, Optional

# Add source paths
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'config'))

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class FinalSystemValidator:
    """Comprehensive final system validation and deployment readiness assessment"""
    
    def __init__(self):
        self.validation_results = {
            'timestamp': datetime.now().isoformat(),
            'system_version': '1.0.0',
            'validation_type': 'Final System Integration Test',
            'components_tested': 0,
            'components_passed': 0,
            'components_failed': 0,
            'deployment_ready': False,
            'test_results': {},
            'performance_metrics': {},
            'security_assessment': {},
            'recommendations': [],
            'next_steps': []
        }
        
    def test_database_integration(self) -> Dict:
        """Comprehensive database integration testing"""
        logger.info("Testing Database Integration...")
        
        test_results = {
            'component': 'Database Management System',
            'tests_run': 0,
            'tests_passed': 0,
            'status': 'UNKNOWN',
            'details': [],
            'performance': {}
        }
        
        try:
            # Create temporary database for testing
            with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as temp_db:
                temp_db_path = temp_db.name
                
            try:
                from database.database_manager import DatabaseManager
                
                # Test 1: Database Initialization
                test_results['tests_run'] += 1
                start_time = time.time()
                db_manager = DatabaseManager(temp_db_path)
                init_time = time.time() - start_time
                test_results['performance']['initialization_time'] = init_time
                test_results['tests_passed'] += 1
                test_results['details'].append(f"✓ Database initialized in {init_time:.3f}s")
                
                # Test 2: Schema Validation
                test_results['tests_run'] += 1
                with db_manager.get_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
                    tables = [row[0] for row in cursor.fetchall()]
                    
                required_tables = ['vehicles', 'parking_spaces', 'transactions', 'system_events', 'users', 'system_settings']
                missing_tables = [table for table in required_tables if table not in tables]
                
                if not missing_tables:
                    test_results['tests_passed'] += 1
                    test_results['details'].append(f"✓ All {len(required_tables)} required tables created")
                else:
                    test_results['details'].append(f"✗ Missing tables: {missing_tables}")
                
                # Test 3: CRUD Operations Performance
                test_results['tests_run'] += 1
                start_time = time.time()
                
                # Add test vehicles
                vehicles_added = 0
                for i in range(10):
                    vehicle_data = {
                        'plate_number': f'TEST{i:03d}',
                        'vehicle_type': 'sedan',
                        'length': 4.5,
                        'width': 1.8,
                        'height': 1.6,
                        'owner_name': f'Test Owner {i}',
                        'phone_number': f'555-{i:04d}',
                        'email': f'test{i}@example.com'
                    }
                    try:
                        vehicle_id = db_manager.add_vehicle(vehicle_data)
                        if vehicle_id:
                            vehicles_added += 1
                    except Exception as e:
                        test_results['details'].append(f"✗ Vehicle addition error: {str(e)}")
                        
                crud_time = time.time() - start_time
                test_results['performance']['crud_operations_time'] = crud_time
                
                if vehicles_added == 10:
                    test_results['tests_passed'] += 1
                    test_results['details'].append(f"✓ Added {vehicles_added} vehicles in {crud_time:.3f}s")
                else:
                    test_results['details'].append(f"✗ Only added {vehicles_added}/10 vehicles")
                
                # Test 4: Concurrent Access
                test_results['tests_run'] += 1
                concurrent_results = []
                
                def concurrent_operation(operation_id):
                    try:
                        vehicle_data = {
                            'plate_number': f'CONC{operation_id:03d}',
                            'vehicle_type': 'suv',
                            'length': 4.8,
                            'width': 1.9,
                            'height': 1.7
                        }
                        vehicle_id = db_manager.add_vehicle(vehicle_data)
                        concurrent_results.append(vehicle_id is not None)
                    except Exception as e:
                        concurrent_results.append(False)
                        
                start_time = time.time()
                threads = []
                for i in range(5):
                    thread = threading.Thread(target=concurrent_operation, args=(i,))
                    threads.append(thread)
                    thread.start()
                    
                for thread in threads:
                    thread.join()
                    
                concurrent_time = time.time() - start_time
                test_results['performance']['concurrent_operations_time'] = concurrent_time
                
                success_count = sum(concurrent_results)
                if success_count == 5:
                    test_results['tests_passed'] += 1
                    test_results['details'].append(f"✓ Concurrent operations successful ({success_count}/5)")
                else:
                    test_results['details'].append(f"✗ Concurrent operations partial success ({success_count}/5)")
                
                # Test 5: Query Performance
                test_results['tests_run'] += 1
                start_time = time.time()
                
                try:
                    available_spaces = db_manager.get_available_spaces('sedan')
                    query_time = time.time() - start_time
                    test_results['performance']['query_time'] = query_time
                    
                    if available_spaces and len(available_spaces) > 0:
                        test_results['tests_passed'] += 1
                        test_results['details'].append(f"✓ Query returned {len(available_spaces)} spaces in {query_time:.3f}s")
                    else:
                        test_results['details'].append("✗ No available spaces found")
                except Exception as e:
                    test_results['details'].append(f"✗ Query error: {str(e)}")
                
                # Cleanup
                db_manager.close()
                
            finally:
                # Remove temporary database
                if os.path.exists(temp_db_path):
                    os.unlink(temp_db_path)
                    
        except ImportError as e:
            test_results['details'].append(f"✗ Database module import error: {str(e)}")
        except Exception as e:
            test_results['details'].append(f"✗ Database test error: {str(e)}")
            
        # Determine status
        if test_results['tests_passed'] == test_results['tests_run']:
            test_results['status'] = 'PASS'
        elif test_results['tests_passed'] > 0:
            test_results['status'] = 'PARTIAL'
        else:
            test_results['status'] = 'FAIL'
            
        return test_results
        
    def test_communication_systems(self) -> Dict:
        """Test communication protocols and interfaces"""
        logger.info("Testing Communication Systems...")
        
        test_results = {
            'component': 'Communication Systems',
            'tests_run': 0,
            'tests_passed': 0,
            'status': 'UNKNOWN',
            'details': [],
            'performance': {}
        }
        
        try:
            from communication.protocols import CommunicationManager
            
            # Test 1: Communication Manager Initialization
            test_results['tests_run'] += 1
            try:
                comm_manager = CommunicationManager()
                test_results['tests_passed'] += 1
                test_results['details'].append("✓ Communication manager initialized")
            except Exception as e:
                test_results['details'].append(f"✗ Communication manager error: {str(e)}")
                
            # Test 2: Protocol Availability Check
            test_results['tests_run'] += 1
            try:
                protocols = ['websocket_server', 'tcp_server', 'modbus_client']
                available_protocols = [p for p in protocols if hasattr(comm_manager, p)]
                
                if len(available_protocols) >= 2:
                    test_results['tests_passed'] += 1
                    test_results['details'].append(f"✓ Protocols available: {available_protocols}")
                else:
                    test_results['details'].append(f"✗ Limited protocols: {available_protocols}")
            except Exception as e:
                test_results['details'].append(f"✗ Protocol check error: {str(e)}")
                
        except ImportError as e:
            test_results['details'].append(f"✗ Communication module import error: {str(e)}")
            
        # Determine status
        if test_results['tests_passed'] == test_results['tests_run']:
            test_results['status'] = 'PASS'
        elif test_results['tests_passed'] > 0:
            test_results['status'] = 'PARTIAL'
        else:
            test_results['status'] = 'FAIL'
            
        return test_results
        
    def test_simulation_engine(self) -> Dict:
        """Test parking simulation capabilities"""
        logger.info("Testing Simulation Engine...")
        
        test_results = {
            'component': 'Simulation Engine',
            'tests_run': 0,
            'tests_passed': 0,
            'status': 'UNKNOWN',
            'details': [],
            'performance': {}
        }
        
        try:
            from simulation.parking_simulator import ParkingSimulator
            
            # Test 1: Simulator Initialization
            test_results['tests_run'] += 1
            try:
                simulator = ParkingSimulator()
                test_results['tests_passed'] += 1
                test_results['details'].append("✓ Parking simulator initialized")
            except Exception as e:
                test_results['details'].append(f"✗ Simulator initialization error: {str(e)}")
                
            # Test 2: Core Methods Availability
            test_results['tests_run'] += 1
            try:
                required_methods = ['start_simulation', 'stop_simulation', 'get_statistics']
                available_methods = [m for m in required_methods if hasattr(simulator, m)]
                
                if len(available_methods) >= 2:
                    test_results['tests_passed'] += 1
                    test_results['details'].append(f"✓ Core methods available: {available_methods}")
                else:
                    test_results['details'].append(f"✗ Missing methods: {set(required_methods) - set(available_methods)}")
            except Exception as e:
                test_results['details'].append(f"✗ Method check error: {str(e)}")
                
        except ImportError as e:
            test_results['details'].append(f"✗ Simulation module import error: {str(e)}")
            
        # Determine status
        if test_results['tests_passed'] == test_results['tests_run']:
            test_results['status'] = 'PASS'
        elif test_results['tests_passed'] > 0:
            test_results['status'] = 'PARTIAL'
        else:
            test_results['status'] = 'FAIL'
            
        return test_results
        
    def test_security_framework(self) -> Dict:
        """Test security and authentication systems"""
        logger.info("Testing Security Framework...")
        
        test_results = {
            'component': 'Security Framework',
            'tests_run': 0,
            'tests_passed': 0,
            'status': 'UNKNOWN',
            'details': [],
            'performance': {}
        }
        
        try:
            from security.authentication import AuthenticationManager
            
            # Test 1: Authentication Manager Initialization
            test_results['tests_run'] += 1
            try:
                auth_manager = AuthenticationManager()
                test_results['tests_passed'] += 1
                test_results['details'].append("✓ Authentication manager initialized")
            except Exception as e:
                test_results['details'].append(f"✗ Authentication manager error: {str(e)}")
                
            # Test 2: Security Methods Check
            test_results['tests_run'] += 1
            try:
                security_methods = ['authenticate_user', 'create_user', 'generate_token', 'validate_token']
                available_methods = [m for m in security_methods if hasattr(auth_manager, m)]
                
                if len(available_methods) >= 3:
                    test_results['tests_passed'] += 1
                    test_results['details'].append(f"✓ Security methods available: {len(available_methods)}/4")
                else:
                    test_results['details'].append(f"✗ Missing security methods: {set(security_methods) - set(available_methods)}")
            except Exception as e:
                test_results['details'].append(f"✗ Security method check error: {str(e)}")
                
        except ImportError as e:
            test_results['details'].append(f"✗ Security module import error: {str(e)}")
            
        # Determine status
        if test_results['tests_passed'] == test_results['tests_run']:
            test_results['status'] = 'PASS'
        elif test_results['tests_passed'] > 0:
            test_results['status'] = 'PARTIAL'
        else:
            test_results['status'] = 'FAIL'
            
        return test_results
        
    def test_system_configuration(self) -> Dict:
        """Test system configuration and settings"""
        logger.info("Testing System Configuration...")
        
        test_results = {
            'component': 'System Configuration',
            'tests_run': 0,
            'tests_passed': 0,
            'status': 'UNKNOWN',
            'details': [],
            'performance': {}
        }
        
        # Test configuration files
        config_files = [
            ('system_config.yaml', os.path.join(os.path.dirname(__file__), '..', 'config', 'system_config.yaml')),
            ('system_config.py', os.path.join(os.path.dirname(__file__), '..', 'config', 'system_config.py')),
            ('requirements.txt', os.path.join(os.path.dirname(__file__), '..', 'requirements.txt'))
        ]
        
        for config_name, config_path in config_files:
            test_results['tests_run'] += 1
            if os.path.exists(config_path):
                test_results['tests_passed'] += 1
                test_results['details'].append(f"✓ Configuration file exists: {config_name}")
            else:
                test_results['details'].append(f"✗ Missing configuration file: {config_name}")
                
        # Test configuration manager
        try:
            from system_config import ConfigManager
            
            test_results['tests_run'] += 1
            try:
                config_manager = ConfigManager()
                test_results['tests_passed'] += 1
                test_results['details'].append("✓ Configuration manager functional")
            except Exception as e:
                test_results['details'].append(f"✗ Configuration manager error: {str(e)}")
                
        except ImportError as e:
            test_results['details'].append(f"✗ Configuration module import error: {str(e)}")
            
        # Determine status
        if test_results['tests_passed'] == test_results['tests_run']:
            test_results['status'] = 'PASS'
        elif test_results['tests_passed'] > 0:
            test_results['status'] = 'PARTIAL'
        else:
            test_results['status'] = 'FAIL'
            
        return test_results
        
    def assess_deployment_readiness(self) -> Dict:
        """Assess overall system deployment readiness"""
        logger.info("Assessing Deployment Readiness...")
        
        # Required files for deployment
        required_files = [
            'README.md',
            'requirements.txt',
            'scripts/install.bat',
            'scripts/start_system.bat',
            'scripts/stop_system.bat',
            'plc/main.st',
            'plc/global_vars.st',
            'hmi/web/index.html',
            'src/database/database_manager.py',
            'src/simulation/parking_simulator.py'
        ]
        
        deployment_assessment = {
            'files_checked': 0,
            'files_present': 0,
            'missing_files': [],
            'deployment_scripts_ready': False,
            'documentation_complete': False,
            'system_components_ready': False
        }
        
        project_root = os.path.join(os.path.dirname(__file__), '..')
        
        for file_path in required_files:
            deployment_assessment['files_checked'] += 1
            full_path = os.path.join(project_root, file_path)
            if os.path.exists(full_path):
                deployment_assessment['files_present'] += 1
            else:
                deployment_assessment['missing_files'].append(file_path)
                
        # Check deployment scripts
        script_files = ['scripts/install.bat', 'scripts/start_system.bat', 'scripts/stop_system.bat']
        scripts_present = all(os.path.exists(os.path.join(project_root, script)) for script in script_files)
        deployment_assessment['deployment_scripts_ready'] = scripts_present
        
        # Check documentation
        doc_files = ['README.md', 'docs/technical/Technical_Documentation.md', 'docs/user/User_Manual.md']
        docs_present = all(os.path.exists(os.path.join(project_root, doc)) for doc in doc_files)
        deployment_assessment['documentation_complete'] = docs_present
        
        # Assess component readiness
        component_statuses = [result['status'] for result in self.validation_results['test_results'].values()]
        passing_components = sum(1 for status in component_statuses if status == 'PASS')
        total_components = len(component_statuses)
        
        deployment_assessment['system_components_ready'] = (passing_components / total_components) >= 0.8 if total_components > 0 else False
        
        return deployment_assessment
        
    def generate_recommendations(self) -> List[str]:
        """Generate deployment and improvement recommendations"""
        recommendations = []
        
        # Check overall component health
        component_statuses = [result['status'] for result in self.validation_results['test_results'].values()]
        failing_components = [name for name, result in self.validation_results['test_results'].items() if result['status'] == 'FAIL']
        partial_components = [name for name, result in self.validation_results['test_results'].items() if result['status'] == 'PARTIAL']
        
        if not failing_components and not partial_components:
            recommendations.append("🎉 All system components are fully functional and ready for production deployment")
        elif failing_components:
            recommendations.append(f"❌ Critical: Fix failing components before deployment: {', '.join(failing_components)}")
        elif partial_components:
            recommendations.append(f"⚠️ Warning: Address partial component issues: {', '.join(partial_components)}")
            
        # Performance recommendations
        db_performance = self.validation_results['test_results'].get('database_integration', {}).get('performance', {})
        if db_performance.get('query_time', 0) > 0.1:
            recommendations.append("🔧 Consider database query optimization for better performance")
            
        # Security recommendations
        if 'security_framework' in self.validation_results['test_results']:
            security_status = self.validation_results['test_results']['security_framework']['status']
            if security_status != 'PASS':
                recommendations.append("🔒 Security framework needs attention before production deployment")
                
        # Documentation recommendations
        recommendations.append("📖 Ensure all user documentation is up-to-date before user training")
        recommendations.append("🔄 Implement regular system health monitoring and maintenance schedules")
        recommendations.append("📊 Set up production logging and monitoring dashboards")
        
        return recommendations
        
    def run_final_validation(self) -> Dict:
        """Execute complete final system validation"""
        logger.info("Starting Final System Validation...")
        start_time = time.time()
        
        # Run all component tests
        test_components = [
            ('database_integration', self.test_database_integration),
            ('communication_systems', self.test_communication_systems),
            ('simulation_engine', self.test_simulation_engine),
            ('security_framework', self.test_security_framework),
            ('system_configuration', self.test_system_configuration)
        ]
        
        for component_name, test_function in test_components:
            try:
                self.validation_results['components_tested'] += 1
                result = test_function()
                self.validation_results['test_results'][component_name] = result
                
                if result['status'] == 'PASS':
                    self.validation_results['components_passed'] += 1
                else:
                    self.validation_results['components_failed'] += 1
                    
            except Exception as e:
                logger.error(f"Error testing {component_name}: {e}")
                self.validation_results['components_failed'] += 1
                
        # Assess deployment readiness
        deployment_assessment = self.assess_deployment_readiness()
        
        # Determine overall deployment readiness
        self.validation_results['deployment_ready'] = (
            self.validation_results['components_passed'] >= 4 and
            deployment_assessment['deployment_scripts_ready'] and
            deployment_assessment['documentation_complete'] and
            deployment_assessment['system_components_ready']
        )
        
        # Generate recommendations
        self.validation_results['recommendations'] = self.generate_recommendations()
        
        # Add next steps
        if self.validation_results['deployment_ready']:
            self.validation_results['next_steps'] = [
                "✅ System is ready for production deployment",
                "🚀 Execute deployment scripts to install the system",
                "📋 Conduct user training sessions",
                "🔍 Perform final acceptance testing with stakeholders",
                "📊 Set up production monitoring and alerting",
                "📝 Schedule regular maintenance and updates"
            ]
        else:
            self.validation_results['next_steps'] = [
                "🔧 Address failing component issues",
                "📋 Complete missing documentation",
                "🧪 Re-run validation tests after fixes",
                "⚡ Optimize performance bottlenecks",
                "🔒 Strengthen security implementations",
                "📖 Update deployment procedures"
            ]
            
        # Calculate execution time
        self.validation_results['execution_time'] = round(time.time() - start_time, 2)
        
        return self.validation_results
        
    def generate_final_report(self) -> str:
        """Generate comprehensive final validation report"""
        report_dir = os.path.join(os.path.dirname(__file__), '..', 'reports')
        os.makedirs(report_dir, exist_ok=True)
        
        # Generate JSON report
        json_file = os.path.join(report_dir, 'final_validation_report.json')
        with open(json_file, 'w') as f:
            json.dump(self.validation_results, f, indent=2)
            
        # Generate detailed text report
        text_file = os.path.join(report_dir, 'final_validation_report.txt')
        with open(text_file, 'w', encoding='utf-8') as f:
            f.write("CAR PARKING VENDING SYSTEM - FINAL VALIDATION REPORT\n")
            f.write("=" * 70 + "\n\n")
            f.write(f"Generated: {self.validation_results['timestamp']}\n")
            f.write(f"System Version: {self.validation_results['system_version']}\n")
            f.write(f"Validation Type: {self.validation_results['validation_type']}\n")
            f.write(f"Execution Time: {self.validation_results['execution_time']} seconds\n\n")
            
            # Executive Summary
            f.write("EXECUTIVE SUMMARY\n")
            f.write("-" * 20 + "\n")
            f.write(f"Components Tested: {self.validation_results['components_tested']}\n")
            f.write(f"Components Passed: {self.validation_results['components_passed']}\n")
            f.write(f"Components Failed: {self.validation_results['components_failed']}\n")
            
            success_rate = (self.validation_results['components_passed'] / self.validation_results['components_tested'] * 100) if self.validation_results['components_tested'] > 0 else 0
            f.write(f"Success Rate: {success_rate:.1f}%\n")
            
            deployment_status = "READY" if self.validation_results['deployment_ready'] else "NOT READY"
            f.write(f"Deployment Status: {deployment_status}\n\n")
            
            # Component Details
            f.write("COMPONENT TEST RESULTS\n")
            f.write("-" * 30 + "\n")
            for component_name, result in self.validation_results['test_results'].items():
                f.write(f"\n{result['component'].upper()}: {result['status']}\n")
                f.write(f"Tests: {result['tests_passed']}/{result['tests_run']} passed\n")
                for detail in result['details']:
                    f.write(f"  {detail}\n")
                    
            # Recommendations
            f.write("\nRECOMMENDATIONS\n")
            f.write("-" * 20 + "\n")
            for recommendation in self.validation_results['recommendations']:
                f.write(f"• {recommendation}\n")
                
            # Next Steps
            f.write("\nNEXT STEPS\n")
            f.write("-" * 15 + "\n")
            for step in self.validation_results['next_steps']:
                f.write(f"• {step}\n")
                
        logger.info(f"Final validation reports generated: {json_file}, {text_file}")
        return text_file

if __name__ == "__main__":
    validator = FinalSystemValidator()
    results = validator.run_final_validation()
    
    # Print executive summary
    print("\n" + "=" * 70)
    print("CAR PARKING VENDING SYSTEM - FINAL VALIDATION SUMMARY")
    print("=" * 70)
    print(f"System Version: {results['system_version']}")
    print(f"Components Tested: {results['components_tested']}")
    print(f"Components Passed: {results['components_passed']}")
    print(f"Components Failed: {results['components_failed']}")
    
    if results['components_tested'] > 0:
        success_rate = (results['components_passed'] / results['components_tested']) * 100
        print(f"Success Rate: {success_rate:.1f}%")
        
    deployment_status = "✅ READY FOR DEPLOYMENT" if results['deployment_ready'] else "❌ NOT READY FOR DEPLOYMENT"
    print(f"Deployment Status: {deployment_status}")
    
    print(f"Execution Time: {results['execution_time']} seconds")
    
    print("\nCOMPONENT STATUS:")
    for component_name, result in results['test_results'].items():
        status_icon = "✅" if result['status'] == 'PASS' else "⚠️" if result['status'] == 'PARTIAL' else "❌"
        print(f"  {status_icon} {result['component']}: {result['status']}")
        
    print("\nRECOMMENDATIONS:")
    for recommendation in results['recommendations']:
        print(f"• {recommendation}")
        
    print("\nNEXT STEPS:")
    for step in results['next_steps']:
        print(f"• {step}")
        
    # Generate detailed report
    report_file = validator.generate_final_report()
    print(f"\nDetailed report generated: {report_file}")
    
    print("\n" + "=" * 70)
    print("FINAL VALIDATION COMPLETE")
    print("=" * 70)
