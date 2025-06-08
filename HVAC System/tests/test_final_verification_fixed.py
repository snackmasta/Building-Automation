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
                self.results[test_name] = "PASS"
            else:
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
            return hasattr(simulator, 'run') and hasattr(simulator, 'zones')
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
    
    def test_batch_scripts_validity(self):
        """Test that batch scripts exist and have valid content"""
        try:
            batch_dir = project_root / "scripts" / "batch"
            required_scripts = [
                "run_main_controller.bat",
                "run_status_monitor.bat", 
                "run_tests.bat",
                "system_launcher.bat"
            ]
            
            for script_name in required_scripts:
                script_path = batch_dir / script_name
                if not script_path.exists():
                    print(f"Missing script: {script_name}")
                    return False
                
                content = script_path.read_text(encoding='utf-8', errors='ignore')
                if not content.strip():
                    print(f"Empty script: {script_name}")
                    return False
                
                # Should contain batch file indicators
                if "@echo off" not in content and "echo" not in content:
                    print(f"Invalid batch syntax: {script_name}")
                    return False
            
            return True
        except Exception as e:
            print(f"Batch scripts error: {e}")
            return False
    
    def test_math_import_fix(self):
        """Test that the math import issue has been fixed in HMI interface"""
        try:
            hmi_path = project_root / "src" / "gui" / "hmi_interface.py"
            content = hmi_path.read_text(encoding='utf-8', errors='ignore')
            
            # Check that math is imported at the top
            lines = content.split('\n')
            import_section = lines[:30]  # Check first 30 lines
            
            has_math_import = any('import math' in line for line in import_section)
            
            # Check that math is not imported in main function
            main_function_start = False
            has_math_in_main = False
            
            for line in lines:
                if 'def main():' in line:
                    main_function_start = True
                elif main_function_start and ('def ' in line and 'main' not in line):
                    break
                elif main_function_start and 'import math' in line:
                    has_math_in_main = True
                    break
            
            return has_math_import and not has_math_in_main
        except Exception as e:
            print(f"Math import test error: {e}")
            return False
    
    def test_project_structure_consistency(self):
        """Test that project follows the same structure as Water Treatment System"""
        try:
            required_structure = [
                "src/core/main_controller.py",
                "src/gui/web_hmi.html",
                "src/gui/hmi_interface.py",
                "src/monitoring/system_status.py",
                "src/simulation/hvac_simulator.py",
                "scripts/batch/system_launcher.bat",
                "config/plc_config.ini",
                "docs/PROJECT_STRUCTURE.md"
            ]
            
            for file_path in required_structure:
                full_path = project_root / file_path
                if not full_path.exists():
                    print(f"Missing required file: {file_path}")
                    return False
            
            return True
        except Exception as e:
            print(f"Structure consistency error: {e}")
            return False
    
    def test_documentation_completeness(self):
        """Test that essential documentation exists"""
        try:
            docs_dir = project_root / "docs"
            required_docs = [
                "PROJECT_STRUCTURE.md",
                "RESTRUCTURING_COMPLETE.md"
            ]
            
            for doc in required_docs:
                doc_path = docs_dir / doc
                if not doc_path.exists():
                    print(f"Missing documentation: {doc}")
                    return False
                
                content = doc_path.read_text(encoding='utf-8', errors='ignore')
                if len(content.strip()) < 100:
                    print(f"Insufficient content in: {doc}")
                    return False
            
            return True
        except Exception as e:
            print(f"Documentation error: {e}")
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
        self.run_test("Web HMI Structure", self.test_web_hmi_structure)
        self.run_test("Batch Scripts Validity", self.test_batch_scripts_validity)
        self.run_test("Math Import Fix", self.test_math_import_fix)
        self.run_test("Project Structure Consistency", self.test_project_structure_consistency)
        self.run_test("Documentation Completeness", self.test_documentation_completeness)
        
        # Generate summary
        print("=" * 60)
        print("FINAL VERIFICATION SUMMARY")
        print("=" * 60)
        
        for test_name, result in self.results.items():
            status_icon = "✅" if result == "PASS" else "❌"
            print(f"{test_name:<35} {status_icon} {result}")
        
        print(f"\nTotal: {self.passed_count}/{self.test_count} tests passed")
        
        success_rate = (self.passed_count / self.test_count) * 100
        
        if self.passed_count == self.test_count:
            print("\n🎉 ALL TESTS PASSED - HVAC System restructuring fully successful!")
            print("🎯 The system now follows the same organization pattern as the Water Treatment System.")
            print("✨ All components are working correctly and ready for use.")
            status = "COMPLETE SUCCESS"
        elif success_rate >= 80:
            print(f"\n✅ MOSTLY SUCCESSFUL - {success_rate:.1f}% tests passed")
            print("🔧 Minor issues may need attention but core functionality is working.")
            status = "MOSTLY SUCCESSFUL"
        else:
            print(f"\n⚠️  NEEDS ATTENTION - Only {success_rate:.1f}% tests passed")
            print("🛠️  Several issues need to be resolved.")
            status = "NEEDS WORK"
          # Save detailed report to organized directory
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        reports_dir = project_root / "tests" / "reports" / "final_verification"
        reports_dir.mkdir(parents=True, exist_ok=True)
        report_file = reports_dir / f"final_verification_report_{timestamp}.json"
        
        report_data = {
            "timestamp": datetime.now().isoformat(),
            "total_tests": self.test_count,
            "passed_tests": self.passed_count,
            "success_rate": f"{success_rate:.1f}%",
            "status": status,
            "test_results": self.results,
            "summary": status
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
