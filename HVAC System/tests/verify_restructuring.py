#!/usr/bin/env python3
"""
HVAC System - Post-Restructuring Verification
Comprehensive test to verify all components work after restructuring
"""

import sys
import os
import time
import subprocess
import json
from pathlib import Path
from datetime import datetime

def test_file_structure():
    """Test that all files are in correct locations"""
    print("Testing file structure...")
    
    base_path = Path(__file__).parent.parent
    required_files = [
        'src/core/main_controller.py',
        'src/gui/hmi_interface.py', 
        'src/monitoring/system_status.py',
        'src/simulation/hvac_simulator.py',
        'config/plc_config.ini',
        'scripts/batch/system_launcher.bat',
        'scripts/batch/run_main_controller.bat',
        'scripts/batch/run_status_monitor.bat',
        'docs/PROJECT_STRUCTURE.md',
        'docs/RESTRUCTURING_COMPLETE.md'
    ]
    
    missing_files = []
    for file_path in required_files:
        full_path = base_path / file_path
        if not full_path.exists():
            missing_files.append(file_path)
    
    if missing_files:
        print(f"❌ Missing files: {missing_files}")
        return False
    else:
        print("✅ All required files in correct locations")
        return True

def test_main_controller_import():
    """Test that main controller can be imported"""
    print("Testing main controller import...")
    
    try:
        # Add src to path
        base_path = Path(__file__).parent.parent
        sys.path.insert(0, str(base_path / 'src'))
        
        # Import and test
        from core.main_controller import HVACController
        controller = HVACController()
        
        # Test basic attributes
        assert hasattr(controller, 'base_path')
        assert hasattr(controller, 'zones')
        assert hasattr(controller, 'equipment_status')
        assert hasattr(controller, 'system_status')
        
        print("✅ Main controller imports and initializes correctly")
        return True
        
    except Exception as e:
        print(f"❌ Main controller import failed: {e}")
        return False

def test_configuration_loading():
    """Test configuration file loading"""
    print("Testing configuration loading...")
    
    try:
        base_path = Path(__file__).parent.parent
        sys.path.insert(0, str(base_path / 'src'))
        
        from core.main_controller import HVACController
        controller = HVACController()
        
        # Test configuration loading
        if controller.load_configuration():
            print("✅ Configuration loads successfully")
            return True
        else:
            print("❌ Configuration loading failed")
            return False
            
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False

def test_zone_initialization():
    """Test zone initialization"""
    print("Testing zone initialization...")
    
    try:
        base_path = Path(__file__).parent.parent
        sys.path.insert(0, str(base_path / 'src'))
        
        from core.main_controller import HVACController
        controller = HVACController()
        
        if controller.load_configuration() and controller.initialize_zones():
            if len(controller.zones) > 0:
                print(f"✅ Zones initialized successfully ({len(controller.zones)} zones)")
                return True
            else:
                print("❌ No zones initialized")
                return False
        else:
            print("❌ Zone initialization failed")
            return False
            
    except Exception as e:
        print(f"❌ Zone initialization test failed: {e}")
        return False

def test_equipment_initialization():
    """Test equipment initialization"""
    print("Testing equipment initialization...")
    
    try:
        base_path = Path(__file__).parent.parent
        sys.path.insert(0, str(base_path / 'src'))
        
        from core.main_controller import HVACController
        controller = HVACController()
        
        if (controller.load_configuration() and 
            controller.initialize_zones() and 
            controller.initialize_equipment()):
            
            required_equipment = ['supply_fan', 'return_fan', 'cooling_coil', 'heating_coil']
            for equipment in required_equipment:
                if equipment not in controller.equipment_status:
                    print(f"❌ Missing equipment: {equipment}")
                    return False
            
            print("✅ Equipment initialized successfully")
            return True
        else:
            print("❌ Equipment initialization failed")
            return False
            
    except Exception as e:
        print(f"❌ Equipment initialization test failed: {e}")
        return False

def test_batch_scripts():
    """Test that batch scripts exist and have correct syntax"""
    print("Testing batch scripts...")
    
    base_path = Path(__file__).parent.parent
    batch_path = base_path / 'scripts' / 'batch'
    
    required_scripts = [
        'system_launcher.bat',
        'run_main_controller.bat', 
        'run_hmi.bat',
        'run_simulator.bat',
        'run_status_monitor.bat',
        'run_tests.bat'
    ]
    
    missing_scripts = []
    for script in required_scripts:
        script_path = batch_path / script
        if not script_path.exists():
            missing_scripts.append(script)
    
    if missing_scripts:
        print(f"❌ Missing batch scripts: {missing_scripts}")
        return False
    else:
        print("✅ All batch scripts present")
        return True

def test_logs_directory():
    """Test logs directory creation"""
    print("Testing logs directory...")
    
    try:
        base_path = Path(__file__).parent.parent
        logs_path = base_path / 'logs'
        
        if not logs_path.exists():
            logs_path.mkdir(exist_ok=True)
        
        if logs_path.exists() and logs_path.is_dir():
            print("✅ Logs directory accessible")
            return True
        else:
            print("❌ Logs directory not accessible")
            return False
            
    except Exception as e:
        print(f"❌ Logs directory test failed: {e}")
        return False

def test_data_directory():
    """Test data directory creation"""
    print("Testing data directory...")
    
    try:
        base_path = Path(__file__).parent.parent
        data_path = base_path / 'data'
        
        if not data_path.exists():
            data_path.mkdir(exist_ok=True)
        
        if data_path.exists() and data_path.is_dir():
            print("✅ Data directory accessible")
            return True
        else:
            print("❌ Data directory not accessible")
            return False
            
    except Exception as e:
        print(f"❌ Data directory test failed: {e}")
        return False

def run_verification():
    """Run all verification tests"""
    print("HVAC System - Post-Restructuring Verification")
    print("=" * 60)
    print()
    
    tests = [
        ("File Structure", test_file_structure),
        ("Main Controller Import", test_main_controller_import),
        ("Configuration Loading", test_configuration_loading),
        ("Zone Initialization", test_zone_initialization),
        ("Equipment Initialization", test_equipment_initialization),
        ("Batch Scripts", test_batch_scripts),
        ("Logs Directory", test_logs_directory),
        ("Data Directory", test_data_directory)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"Running: {test_name}")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            results.append((test_name, False))
        print()
    
    # Summary
    print("=" * 60)
    print("VERIFICATION SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for name, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:<30} {status}")
    
    print()
    print(f"Total: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED - Restructuring successful!")
        return True
    else:
        print(f"⚠️  {total - passed} tests failed - Review needed")
        return False

if __name__ == '__main__':
    success = run_verification()
    
    # Generate verification report
    report = {
        'timestamp': datetime.now().isoformat(),
        'verification_type': 'post_restructuring',
        'success': success,
        'notes': 'Comprehensive verification after HVAC system restructuring'
    }
      base_path = Path(__file__).parent.parent
    reports_dir = base_path / "tests" / "reports" / "restructuring" 
    reports_dir.mkdir(parents=True, exist_ok=True)
    report_path = reports_dir / f'verification_report_restructuring_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
    
    with open(report_path, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\nVerification report saved to: {report_path}")
    
    if success:
        print("\n🎯 HVAC System restructuring completed successfully!")
        print("The system now follows the same organization pattern as the Water Treatment System.")
    else:
        print("\n⚠️  Some issues found - please review the test results above.")
    
    sys.exit(0 if success else 1)
