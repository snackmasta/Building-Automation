#!/usr/bin/env python3
"""
HVAC System - Integration Tests
Tests for the restructured HVAC system components
"""

import sys
import os
import unittest
import importlib.util
import tempfile
import json
from pathlib import Path

# Add the src directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

class TestHVACSystemStructure(unittest.TestCase):
    """Test the restructured HVAC system file organization"""
    
    def setUp(self):
        """Set up test environment"""
        self.base_path = Path(__file__).parent.parent
        self.src_path = self.base_path / 'src'
        self.config_path = self.base_path / 'config'
        self.scripts_path = self.base_path / 'scripts'
        
    def test_folder_structure(self):
        """Test that all required folders exist"""
        required_folders = [
            'src/core',
            'src/gui',
            'src/monitoring',
            'src/simulation',
            'config',
            'scripts/batch',
            'docs',
            'utils',
            'plc',
            'tests'
        ]
        
        for folder in required_folders:
            folder_path = self.base_path / folder
            self.assertTrue(folder_path.exists(), f"Required folder missing: {folder}")
            
    def test_core_files_exist(self):
        """Test that core files are in the correct locations"""
        core_files = [
            'src/core/main_controller.py',
            'src/gui/hmi_interface.py',
            'src/monitoring/system_status.py',
            'src/simulation/hvac_simulator.py'
        ]
        
        for file_path in core_files:
            full_path = self.base_path / file_path
            self.assertTrue(full_path.exists(), f"Core file missing: {file_path}")
            
    def test_batch_scripts_exist(self):
        """Test that all batch scripts exist"""
        batch_scripts = [
            'scripts/batch/system_launcher.bat',
            'scripts/batch/run_main_controller.bat',
            'scripts/batch/run_hmi.bat',
            'scripts/batch/run_simulator.bat',
            'scripts/batch/run_status_monitor.bat',
            'scripts/batch/generate_diagrams.bat'
        ]
        
        for script in batch_scripts:
            script_path = self.base_path / script
            self.assertTrue(script_path.exists(), f"Batch script missing: {script}")
            
    def test_config_files_exist(self):
        """Test that configuration files exist"""
        config_files = [
            'config/plc_config.ini'
        ]
        
        for config_file in config_files:
            config_path = self.base_path / config_file
            self.assertTrue(config_path.exists(), f"Config file missing: {config_file}")

class TestMainController(unittest.TestCase):
    """Test the main HVAC controller"""
    
    def setUp(self):
        """Set up test environment"""
        self.base_path = Path(__file__).parent.parent
        self.main_controller_path = self.base_path / 'src' / 'core' / 'main_controller.py'
        
    def test_main_controller_imports(self):
        """Test that main controller can be imported"""
        try:
            spec = importlib.util.spec_from_file_location(
                "main_controller", 
                self.main_controller_path
            )
            main_controller = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(main_controller)
            
            # Check that HVACController class exists
            self.assertTrue(hasattr(main_controller, 'HVACController'))
            
        except Exception as e:
            self.fail(f"Failed to import main controller: {e}")
            
    def test_hvac_controller_initialization(self):
        """Test HVACController class initialization"""
        try:
            spec = importlib.util.spec_from_file_location(
                "main_controller", 
                self.main_controller_path
            )
            main_controller = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(main_controller)
            
            # Create controller instance
            controller = main_controller.HVACController()
            
            # Test basic attributes
            self.assertIsNotNone(controller.base_path)
            self.assertFalse(controller.running)
            self.assertIsNotNone(controller.zones)
            self.assertIsNotNone(controller.equipment_status)
            self.assertIsNotNone(controller.system_status)
            
        except Exception as e:
            self.fail(f"Failed to initialize HVACController: {e}")

class TestSystemStatus(unittest.TestCase):
    """Test the system status monitoring component"""
    
    def setUp(self):
        """Set up test environment"""
        self.base_path = Path(__file__).parent.parent
        self.status_path = self.base_path / 'src' / 'monitoring' / 'system_status.py'
        
    def test_system_status_file_exists(self):
        """Test that system status file exists and is readable"""
        self.assertTrue(self.status_path.exists())
        
        # Test file is readable with proper encoding handling
        try:
            with open(self.status_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                self.assertGreater(len(content), 0)
        except Exception as e:
            self.fail(f"Could not read system status file: {e}")

class TestSimulator(unittest.TestCase):
    """Test the HVAC simulator component"""
    
    def setUp(self):
        """Set up test environment"""
        self.base_path = Path(__file__).parent.parent
        self.simulator_path = self.base_path / 'src' / 'simulation' / 'hvac_simulator.py'
        
    def test_simulator_file_exists(self):
        """Test that simulator file exists and is readable"""
        self.assertTrue(self.simulator_path.exists())
        
        # Test file is readable with proper encoding handling
        try:
            with open(self.simulator_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                self.assertGreater(len(content), 0)
        except Exception as e:
            self.fail(f"Could not read simulator file: {e}")

class TestConfiguration(unittest.TestCase):
    """Test system configuration"""
    
    def setUp(self):
        """Set up test environment"""
        self.base_path = Path(__file__).parent.parent
        self.config_path = self.base_path / 'config' / 'plc_config.ini'
        
    def test_config_file_readable(self):
        """Test that configuration file is readable"""
        try:
            import configparser
            config = configparser.ConfigParser()
            config.read(self.config_path)
            
            # Basic validation - check for some expected sections
            expected_sections = ['ZONES', 'TEMPERATURE_CONTROL']
            for section in expected_sections:
                if config.has_section(section):
                    self.assertTrue(True)  # At least one expected section found
                    break
            else:
                self.fail("No expected configuration sections found")
                
        except Exception as e:
            self.fail(f"Could not read configuration file: {e}")

class TestBatchScripts(unittest.TestCase):
    """Test batch scripts syntax and structure"""
    
    def setUp(self):
        """Set up test environment"""
        self.base_path = Path(__file__).parent.parent
        self.batch_path = self.base_path / 'scripts' / 'batch'
        
    def test_batch_scripts_syntax(self):
        """Test that batch scripts have basic valid syntax"""
        batch_files = list(self.batch_path.glob('*.bat'))
        self.assertGreater(len(batch_files), 0, "No batch files found")
        
        for batch_file in batch_files:
            with open(batch_file, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                
                # Basic syntax checks
                self.assertIn('@echo off', content, f"Missing @echo off in {batch_file.name}")
                self.assertGreater(len(content), 50, f"Batch file too short: {batch_file.name}")

class TestDocumentation(unittest.TestCase):
    """Test documentation completeness"""
    
    def setUp(self):
        """Set up test environment"""
        self.base_path = Path(__file__).parent.parent
        self.docs_path = self.base_path / 'docs'
        
    def test_documentation_files_exist(self):
        """Test that key documentation files exist"""
        doc_files = [
            'docs/PROJECT_STRUCTURE.md',
            'docs/RESTRUCTURING_COMPLETE.md'
        ]
        
        for doc_file in doc_files:
            doc_path = self.base_path / doc_file
            self.assertTrue(doc_path.exists(), f"Documentation file missing: {doc_file}")

def run_integration_tests():
    """Run all integration tests and return results"""
    test_loader = unittest.TestLoader()
    test_suite = unittest.TestSuite()
    
    # Add all test classes
    test_classes = [
        TestHVACSystemStructure,
        TestMainController,
        TestSystemStatus,
        TestSimulator,
        TestConfiguration,
        TestBatchScripts,
        TestDocumentation
    ]
    
    for test_class in test_classes:
        tests = test_loader.loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    return result

if __name__ == '__main__':
    print("HVAC System - Integration Tests")
    print("=" * 50)
    print()
    
    # Run tests
    result = run_integration_tests()
    
    # Print summary
    print()
    print("=" * 50)
    print("Test Summary:")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    if result.failures:
        print("\nFailures:")
        for test, traceback in result.failures:
            print(f"- {test}: {traceback}")
    
    if result.errors:
        print("\nErrors:")
        for test, traceback in result.errors:
            print(f"- {test}: {traceback}")
    
    if len(result.failures) == 0 and len(result.errors) == 0:
        print("\n✓ All tests passed! HVAC system restructuring successful.")
    else:
        print(f"\n✗ {len(result.failures + result.errors)} test(s) failed.")
    
    print("=" * 50)
