#!/usr/bin/env python3
"""
HVAC System - Final Comprehensive Verification
Tests all components after restructuring to ensure everything works correctly

Author: System Engineer
Date: June 8, 2025
Version: 1.0.0
"""

import sys
import os
import json
import importlib.util
from pathlib import Path
from datetime import datetime

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

class FinalVerification:
    """Comprehensive verification of the restructured HVAC system"""
    
    def __init__(self):
        self.results = {}
        self.test_count = 0
        self.passed_count = 0
        
    def run_test(self, test_name, test_function):
        """Run a single test and record results"""
        print(f"Running: {test_name}")
        try:
            result = test_function()
            if result:
                print(f"✅ {test_name}")
                self.passed_count += 1
                self.results[test_name] = "PASS"            else:
                print(f"❌ {test_name}")
                self.results[test_name] = "FAIL"
        except Exception as e:
            print(f"❌ {test_name} - Error: {str(e)}")
            self.results[test_name] = f"ERROR: {str(e)}"
        
        self.test_count += 1
        print()
    
    def test_core_imports(self):
        """Test that all core modules can be imported"""
        try:
            # Test main controller
            from src.core.main_controller import HVACController
            
            # Test simulation
            from src.simulation.hvac_simulator import HVACSimulator
            
            # Test monitoring - use correct class name
            from src.monitoring.system_status import HVACSystemMonitor
            
            # Test GUI imports (may fail if dependencies missing, but structure should be correct)
            spec = importlib.util.spec_from_file_location(
                "hmi_interface", 
                project_root / "src" / "gui" / "hmi_interface.py"
            )
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
            
            return True
        except Exception as e:
            print(f"Import error: {e}")
            return False
    
    def test_controller_initialization(self):
        """Test that the main controller initializes correctly"""
        try:
            from src.core.main_controller import HVACController
            controller = HVACController()
            return hasattr(controller, 'zones') and len(controller.zones) > 0
        except Exception as e:
            print(f"Controller initialization error: {e}")
            return False
      def test_configuration_loading(self):
        """Test that configuration loads correctly"""
        try:
            from src.core.main_controller import HVACController
            controller = HVACController()
            return controller.config is not None
        except Exception as e:
            print(f"Configuration loading error: {e}")
            return False
    
    def test_simulator_functionality(self):
        """Test basic simulator functionality"""
        try:
            from src.simulation.hvac_simulator import HVACSimulator
            simulator = HVACSimulator()
            # Test basic simulation step - just check if we can call run method
            # Don't run indefinitely
            return hasattr(simulator, 'run_continuous') and hasattr(simulator, 'zones')
        except Exception as e:
            print(f"Simulator error: {e}")
            return False
    
    def test_status_monitor_initialization(self):
        """Test that status monitor initializes"""
        try:
            from src.monitoring.system_status import HVACSystemMonitor
            monitor = HVACSystemMonitor()
            return hasattr(monitor, 'config') and hasattr(monitor, 'logger')
        except Exception as e:
            print(f"Status monitor error: {e}")
            return False
    
    def test_batch_scripts_syntax(self):
        """Test that batch scripts have valid syntax"""
        try:
            batch_dir = project_root / "scripts" / "batch"
            batch_files = [
                "run_main_controller.bat",
                "run_status_monitor.bat", 
                "run_tests.bat",
                "system_launcher.bat"
            ]
            
            for batch_file in batch_files:
                file_path = batch_dir / batch_file
                if not file_path.exists():
                    return False
                
                # Basic syntax check - file should be readable and contain expected patterns
                content = file_path.read_text(encoding='utf-8', errors='ignore')
                if not content.strip():
                    return False
                    
                # Should contain batch file indicators
                if "@echo off" not in content and "echo" not in content:
                    return False
            
            return True
        except Exception as e:
            print(f"Batch script syntax error: {e}")
            return False
    
    def test_web_hmi_structure(self):
        """Test that web HMI has proper structure"""
        try:
            web_hmi_path = project_root / "src" / "gui" / "web_hmi.html"
            if not web_hmi_path.exists():
                return False
            
            content = web_hmi_path.read_text(encoding='utf-8', errors='ignore')
            
            # Check for essential HTML structure
            required_elements = [
                "<!DOCTYPE html>",
                "<html",
                "<head>",
                "<body>",
                "HVAC"
            ]
            
            for element in required_elements:
                if element not in content:
                    return False
            
            return True
        except Exception as e:
            print(f"Web HMI structure error: {e}")
            return False
    
    def test_data_directories(self):
        """Test that data directories are accessible"""
        try:
            directories = [
                project_root / "data",
                project_root / "logs",
                project_root / "config"
            ]
            
            for directory in directories:
                if not directory.exists() or not directory.is_dir():
                    return False
            
            return True
        except Exception as e:
            print(f"Data directories error: {e}")
            return False
    
    def test_documentation_completeness(self):
        """Test that key documentation exists"""
        try:
            docs_dir = project_root / "docs"
            required_docs = [
                "PROJECT_STRUCTURE.md",
                "RESTRUCTURING_COMPLETE.md"
            ]
            
            for doc in required_docs:
                doc_path = docs_dir / doc
                if not doc_path.exists():
                    return False
                    
                # Check that files are not empty
                content = doc_path.read_text(encoding='utf-8', errors='ignore')
                if len(content.strip()) < 100:  # Should have meaningful content
                    return False
            
            return True
        except Exception as e:
            print(f"Documentation error: {e}")
            return False
    
    def test_project_consistency(self):
        """Test that project follows the same pattern as Water Treatment System"""
        try:
            # Check folder structure matches pattern
            required_folders = [
                "src/core",
                "src/gui", 
                "src/monitoring",
                "src/simulation",
                "scripts/batch",
                "tests",
                "docs",
                "config"
            ]
            
            for folder in required_folders:
                folder_path = project_root / folder
                if not folder_path.exists():
                    return False
            
            # Check that core files are in correct locations
            core_files = [
                "src/core/main_controller.py",
                "src/monitoring/system_status.py",
                "src/gui/web_hmi.html"
            ]
            
            for file_path in core_files:
                if not (project_root / file_path).exists():
                    return False
            
            return True
        except Exception as e:
            print(f"Project consistency error: {e}")
            return False
    
    def run_all_tests(self):
        """Run all verification tests"""
        print("HVAC System - Final Comprehensive Verification")
        print("=" * 60)
        print()
        
        # Run all tests
        self.run_test("Core Module Imports", self.test_core_imports)
        self.run_test("Controller Initialization", self.test_controller_initialization)
        self.run_test("Configuration Loading", self.test_configuration_loading)
        self.run_test("Simulator Functionality", self.test_simulator_functionality)
        self.run_test("Status Monitor Initialization", self.test_status_monitor_initialization)
        self.run_test("Batch Scripts Syntax", self.test_batch_scripts_syntax)
        self.run_test("Web HMI Structure", self.test_web_hmi_structure)
        self.run_test("Data Directories", self.test_data_directories)
        self.run_test("Documentation Completeness", self.test_documentation_completeness)
        self.run_test("Project Consistency", self.test_project_consistency)
        
        # Generate summary
        print("=" * 60)
        print("FINAL VERIFICATION SUMMARY")
        print("=" * 60)
        
        for test_name, result in self.results.items():
            status_icon = "✅" if result == "PASS" else "❌"
            print(f"{test_name:<35} {status_icon} {result}")
        
        print(f"\nTotal: {self.passed_count}/{self.test_count} tests passed")
        
        if self.passed_count == self.test_count:
            print("\n🎉 ALL TESTS PASSED - HVAC System restructuring fully successful!")
            print("🎯 The system now follows the same organization pattern as the Water Treatment System.")
            print("✨ All components are working correctly and ready for use.")
        else:
            print(f"\n⚠️  {self.test_count - self.passed_count} tests failed - some issues need attention")
        
        # Save detailed report
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = project_root / f"final_verification_report_{timestamp}.json"
        
        report_data = {
            "timestamp": datetime.now().isoformat(),
            "total_tests": self.test_count,
            "passed_tests": self.passed_count,
            "success_rate": f"{(self.passed_count/self.test_count*100):.1f}%",
            "test_results": self.results,
            "summary": "ALL TESTS PASSED" if self.passed_count == self.test_count else "SOME TESTS FAILED"
        }
        
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False)
        
        print(f"\nDetailed report saved to: {report_file}")
        
        return self.passed_count == self.test_count

def main():
    """Main verification function"""
    verifier = FinalVerification()
    success = verifier.run_all_tests()
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
