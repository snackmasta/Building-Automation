"""
Wastewater Treatment Plant Control System Unit Tests
This module provides unit tests for the Wastewater Treatment Plant control functions.
"""

import unittest
import os
import sys
import configparser
import json
import math

# Add parent directory to path to allow importing modules
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, '..'))
sys.path.append(project_root) # Add project root

# Import mock classes for testing
class MockPLC:
    """Mock PLC class for testing controller logic"""
    def __init__(self):
        self.inputs = {}
        self.outputs = {}
        self.memories = {}
    
    def set_input(self, name, value):
        """Set an input value"""
        self.inputs[name] = value
    
    def get_output(self, name):
        """Get an output value"""
        return self.outputs.get(name, 0)
    
    def set_memory(self, name, value):
        """Set a memory value"""
        self.memories[name] = value
    
    def get_memory(self, name):
        """Get a memory value"""
        return self.memories.get(name, 0)

# Import controller modules if they exist
try:
    from src.core.intake_controller import IntakeController
    from src.core.treatment_controller import TreatmentController
    from src.core.aeration_controller import AerationController
    from src.core.dosing_controller import DosingController
    from src.core.monitoring_controller import MonitoringController
    controllers_imported = True
except ImportError as e:
    print(f"Error importing controllers: {e}") # Add this line for debugging
    controllers_imported = False
    # Create mock controller classes for testing if real ones aren't available
    class IntakeController:
        """Mock intake controller for testing"""
        def __init__(self, plc=None):
            self.plc = plc or MockPLC()
        
        def regulate_flow(self, flow_setpoint, current_flow, tank_level):
            """Regulate the intake flow"""
            if tank_level > 4.5:  # High level alarm
                return 0
            
            # Simple PI control algorithm
            error = flow_setpoint - current_flow
            output = max(0, min(100, 50 + error * 2))
            return output
        
        def screen_control(self, diff_pressure, runtime):
            """Control the screening mechanism"""
            if diff_pressure > 0.2 or runtime > 3600:
                return True
            return False
    
    class TreatmentController:
        """Mock treatment controller for testing"""
        def __init__(self, plc=None):
            self.plc = plc or MockPLC()
        
        def calculate_sludge_removal(self, sludge_blanket, flow_rate):
            """Calculate sludge removal rate"""
            if sludge_blanket > 1.5:
                return max(5, min(20, sludge_blanket * 10))
            return 0
    
    class AerationController:
        """Mock aeration controller for testing"""
        def __init__(self, plc=None):
            self.plc = plc or MockPLC()
        
        def calculate_blower_speed(self, do_setpoint, do_measured, load_factor=1.0):
            """Calculate blower speed based on DO setpoint"""
            error = do_setpoint - do_measured
            output = max(30, min(100, 60 + error * 15 * load_factor))
            return output
    
    class DosingController:
        """Mock dosing controller for testing"""
        def __init__(self, plc=None):
            self.plc = plc or MockPLC()
        
        def calculate_chemical_dose(self, pH_measured, pH_setpoint, flow_rate):
            """Calculate chemical dosing rate"""
            error = pH_setpoint - pH_measured
            base_dose = flow_rate * 0.002  # Base dosing proportional to flow
            adjustment = error * 5  # Adjustment based on pH error
            return max(0, min(100, base_dose + adjustment))
    
    class MonitoringController:
        """Mock monitoring controller for testing"""
        def __init__(self, plc=None):
            self.plc = plc or MockPLC()
        
        def check_alarm_conditions(self, values):
            """Check for alarm conditions"""
            alarms = []
            if values.get('tank_level', 0) > 4.8:
                alarms.append('HIGH_TANK_LEVEL')
            if values.get('do_level', 0) < 1.0:
                alarms.append('LOW_DO')
            if values.get('ph_value', 7.0) < 6.0 or values.get('ph_value', 7.0) > 9.0:
                alarms.append('PH_OUT_OF_RANGE')
            return alarms

class TestIntakeController(unittest.TestCase):
    """Test cases for the Intake Controller"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.plc = MockPLC()
        self.controller = IntakeController(self.plc)
    
    def test_regulate_flow_normal(self):
        """Test flow regulation under normal conditions"""
        flow_setpoint = 300  # m³/hr
        current_flow = 280  # m³/hr
        tank_level = 2.5  # meters
        
        output = self.controller.regulate_flow(flow_setpoint, current_flow, tank_level)
        
        # Output should be higher than 50% due to positive error
        self.assertGreater(output, 50)
        self.assertLessEqual(output, 100)
    
    def test_regulate_flow_high_level(self):
        """Test flow regulation with high tank level"""
        flow_setpoint = 300  # m³/hr
        current_flow = 280  # m³/hr
        tank_level = 5.1  # meters (above max_tank_level of 5.0 in IntakeController)
        
        output = self.controller.regulate_flow(flow_setpoint, current_flow, tank_level)
        
        # Should completely stop flow due to high level
        self.assertEqual(output, 0)
    
    def test_screen_control_normal(self):
        """Test screen control under normal conditions"""
        diff_pressure = 0.1  # bar
        runtime = 1800  # seconds
        
        result = self.controller.screen_control(diff_pressure, runtime)
        
        # Screen should not run under normal conditions
        self.assertFalse(result)
    
    def test_screen_control_high_pressure(self):
        """Test screen control with high differential pressure"""
        diff_pressure = 0.3  # bar
        runtime = 1800  # seconds
        
        result = self.controller.screen_control(diff_pressure, runtime)
        
        # Screen should run due to high pressure
        self.assertTrue(result)

class TestTreatmentController(unittest.TestCase):
    """Test cases for the Treatment Controller"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.plc = MockPLC()
        self.controller = TreatmentController(self.plc)
    
    def test_calculate_sludge_removal_normal(self):
        """Test sludge removal calculation with normal blanket"""
        sludge_blanket = 1.2  # meters
        flow_rate = 300  # m³/hr
        
        # According to TreatmentController.calculate_sludge_removal:
        # if sludge_blanket <= 1.0: return 2
        # elif sludge_blanket <= 1.5: return 5
        # So for 1.2, it should be 5
        output = self.controller.calculate_sludge_removal(sludge_blanket, flow_rate)
        
        self.assertEqual(output, 5)
    
    def test_calculate_sludge_removal_high(self):
        """Test sludge removal calculation with high blanket"""
        sludge_blanket = 1.8  # meters
        flow_rate = 300  # m³/hr
        
        output = self.controller.calculate_sludge_removal(sludge_blanket, flow_rate)
        
        # Should remove sludge with high blanket level
        self.assertGreater(output, 5)
        self.assertLessEqual(output, 20)

class TestAerationController(unittest.TestCase):
    """Test cases for the Aeration Controller"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.plc = MockPLC()
        self.controller = AerationController(self.plc)
    
    def test_calculate_blower_speed_low_do(self):
        """Test blower speed calculation with low DO"""
        do_setpoint = 2.5  # mg/L
        do_measured = 1.5  # mg/L
        
        output = self.controller.calculate_blower_speed(do_setpoint, do_measured)
        
        # Blower speed should increase with low DO
        self.assertGreater(output, 60)
        self.assertLessEqual(output, 100)
    
    def test_calculate_blower_speed_high_do(self):
        """Test blower speed calculation with high DO"""
        do_setpoint = 2.5  # mg/L
        do_measured = 3.5  # mg/L
        
        output = self.controller.calculate_blower_speed(do_setpoint, do_measured)
        
        # Blower speed should decrease with high DO
        self.assertLess(output, 60)
        self.assertGreaterEqual(output, 30)
    
    def test_calculate_blower_speed_load_factor(self):
        """Test blower speed with load factor adjustment"""
        do_setpoint = 2.5  # mg/L
        do_measured = 1.5  # mg/L
        load_factor = 1.5  # High load
        
        normal_output = self.controller.calculate_blower_speed(do_setpoint, do_measured)
        high_load_output = self.controller.calculate_blower_speed(do_setpoint, do_measured, load_factor)
        
        # High load should increase blower speed more
        self.assertGreater(high_load_output, normal_output)

class TestDosingController(unittest.TestCase):
    """Test cases for the Dosing Controller"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.plc = MockPLC()
        self.controller = DosingController(self.plc)
    
    def test_calculate_chemical_dose_low_ph(self):
        """Test chemical dosing with low pH"""
        pH_measured = 6.5
        pH_setpoint = 7.0
        flow_rate = 300  # m³/hr
        alkalinity = 100 # mg/L as CaCO3
        
        # Using ph_control_dosing as the method for pH adjustment
        dosing_command = self.controller.ph_control_dosing(pH_measured, pH_setpoint, flow_rate, alkalinity)
        output = dosing_command['dose_mg_l'] # Get the dose from the returned dict
        
        # Should dose more chemical with low pH
        # Base dose for lime is 10 mg/L when error > 0 and < 0.5
        # Alkalinity factor is 1.0 for alkalinity = 100
        # Expected output should be around 10 mg/L
        self.assertGreater(output, 0) 
        self.assertLessEqual(output, 50) # Max dose for lime
    
    def test_calculate_chemical_dose_high_ph(self):
        """Test chemical dosing with high pH"""
        pH_measured = 7.5
        pH_setpoint = 7.0
        flow_rate = 300  # m³/hr
        alkalinity = 100 # mg/L as CaCO3

        # Using ph_control_dosing as the method for pH adjustment
        dosing_command = self.controller.ph_control_dosing(pH_measured, pH_setpoint, flow_rate, alkalinity)
        output = dosing_command['dose_mg_l'] # Get the dose from the returned dict
        
        # Should dose less or no chemical with high pH (lime is for raising pH)
        # ph_error is -0.5, so lime_dose will be 0
        self.assertEqual(output, 0)

class TestMonitoringController(unittest.TestCase):
    """Test cases for the Monitoring Controller"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.plc = MockPLC()
        self.controller = MonitoringController(self.plc)
        # Initialize with some default sensor data for tests
        self.sensor_data_normal = {
            'intake': {
                'flow_rate': 150.5, 'raw_water_ph': 7.2, 'raw_water_turbidity': 2.5, 
                'raw_water_temperature': 18.5, 'screen_differential_pressure': 0.15, 
                'intake_tank_level': 75.2
            },
            'secondary_treatment': {
                'aeration_tank_do': [2.1, 2.3, 2.0, 2.2],
                'secondary_effluent_bod': 15
            },
            'tertiary_treatment': {
                'final_effluent_tss': 8
            }
        }
        self.sensor_data_high_level = {
            'intake': {
                'flow_rate': 150.5, 'raw_water_ph': 7.2, 'raw_water_turbidity': 2.5, 
                'raw_water_temperature': 18.5, 'screen_differential_pressure': 0.15, 
                'intake_tank_level': 96.0 # Critical High tank level
            },
            'secondary_treatment': {
                'aeration_tank_do': [2.1, 2.3, 2.0, 2.2],
                'secondary_effluent_bod': 15
            },
             'tertiary_treatment': {
                'final_effluent_tss': 8
            }
        }
        self.sensor_data_multiple_alarms = {
            'intake': {
                'flow_rate': 450, # Critical High flow_rate
                'raw_water_ph': 5.0, # Critical Low pH
                'raw_water_turbidity': 12.5, # Critical High turbidity
                'raw_water_temperature': 18.5, 
                'screen_differential_pressure': 0.15, 
                'intake_tank_level': 75.2
            },
            'secondary_treatment': {
                'aeration_tank_do': [0.4, 2.3, 2.0, 2.2], # Critical Low DO in one tank
                 'secondary_effluent_bod': 15
            },
            'tertiary_treatment': {
                'final_effluent_tss': 8
            }
        }

    def test_check_alarm_conditions_normal(self):
        """Test alarm checking with normal values"""
        alarm_results = self.controller.process_alarms(self.sensor_data_normal)
        active_alarms = alarm_results['active_alarms']
        
        # No alarms should be triggered
        self.assertEqual(len(active_alarms), 0)
    
    def test_check_alarm_conditions_high_level(self):
        """Test alarm checking with high tank level"""
        alarm_results = self.controller.process_alarms(self.sensor_data_high_level)
        active_alarms = alarm_results['active_alarms']
        
        # High level alarm should be triggered
        self.assertEqual(len(active_alarms), 1)
        self.assertEqual(active_alarms[0]['parameter'], 'intake.intake_tank_level')
        self.assertEqual(active_alarms[0]['severity'], 'critical') # tank_level > 95 is critical
    
    def test_check_alarm_conditions_multiple(self):
        """Test alarm checking with multiple alarm conditions"""
        alarm_results = self.controller.process_alarms(self.sensor_data_multiple_alarms)
        active_alarms = alarm_results['active_alarms']
        
        # Multiple alarms should be triggered: flow_rate, ph, turbidity, do
        self.assertEqual(len(active_alarms), 4) 
        
        param_names = [alarm['parameter'] for alarm in active_alarms]
        self.assertIn('intake.flow_rate', param_names)
        self.assertIn('intake.raw_water_ph', param_names)
        self.assertIn('intake.raw_water_turbidity', param_names)
        self.assertIn('aeration_tank_1.do', param_names)

class TestControlSystemConfig(unittest.TestCase):
    """Test cases for the control system configuration"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.config_path = os.path.join(project_root, 'config', 'wwtp_config.ini')
        self.config = configparser.ConfigParser()
        
        try:
            self.config.read(self.config_path)
            self.config_exists = True
        except:
            self.config_exists = False
    
    def test_config_file_exists(self):
        """Test that the config file exists"""
        self.assertTrue(os.path.exists(self.config_path), 
                        "Configuration file not found")
    
    @unittest.skipIf(not os.path.exists(os.path.join(project_root, 'config', 'wwtp_config.ini')),
                     "Config file not found")
    def test_config_sections(self):
        """Test that the config file has the required sections"""
        # Updated to match wwtp_config.ini
        required_sections = ['System', 'Process_Parameters', 'Tank_Configuration', 
                             'Retention_Times', 'Chemical_Dosing', 'Control_Strategy', 
                             'PID_Parameters', 'Compliance', 'Sampling', 'Maintenance', 
                             'Storm_Mode', 'Energy_Management']
        for section in required_sections:
            self.assertIn(section, self.config.sections(), 
                          f"Required section {section} not found in config. Found: {self.config.sections()}")
    
    @unittest.skipIf(not os.path.exists(os.path.join(project_root, 'config', 'wwtp_config.ini')),
                     "Config file not found")
    def test_process_parameters(self):
        """Test that the process parameters are within expected ranges"""
        if 'Process_Parameters' in self.config: # Updated section name
            if 'MaxFlowRate' in self.config['Process_Parameters']: # Updated key name
                flow_rate_max = self.config['Process_Parameters'].getfloat('MaxFlowRate')
                self.assertGreater(flow_rate_max, 0, "Flow rate max should be positive")
            
            if 'OptimumPH' in self.config['Process_Parameters']: # Updated key name
                ph_setpoint = self.config['Process_Parameters'].getfloat('OptimumPH')
                self.assertGreaterEqual(ph_setpoint, 6.0, "pH setpoint too low")
                self.assertLessEqual(ph_setpoint, 9.0, "pH setpoint too high")
            
            if 'OptimumDissolvedOxygen' in self.config['Process_Parameters']: # Updated key name
                do_setpoint = self.config['Process_Parameters'].getfloat('OptimumDissolvedOxygen')
                self.assertGreaterEqual(do_setpoint, 0.5, "DO setpoint too low")
                self.assertLessEqual(do_setpoint, 10.0, "DO setpoint too high")

def run_tests():
    """Run the unit tests and generate a report"""
    # Create a test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test cases
    suite.addTests(loader.loadTestsFromTestCase(TestIntakeController))
    suite.addTests(loader.loadTestsFromTestCase(TestTreatmentController))
    suite.addTests(loader.loadTestsFromTestCase(TestAerationController))
    suite.addTests(loader.loadTestsFromTestCase(TestDosingController))
    suite.addTests(loader.loadTestsFromTestCase(TestMonitoringController))
    suite.addTests(loader.loadTestsFromTestCase(TestControlSystemConfig))
    
    # Run the tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Generate a report
    report_path = os.path.join(project_root, 'tests', 'test_results.json')
    report = {
        'total': result.testsRun,
        'failures': len(result.failures),
        'errors': len(result.errors),
        'skipped': len(result.skipped),
        'success': result.testsRun - len(result.failures) - len(result.errors) - len(result.skipped),
        'details': {
            'failures': [{'test': str(test), 'message': msg} for test, msg in result.failures],
            'errors': [{'test': str(test), 'message': msg} for test, msg in result.errors],
            'skipped': [{'test': str(test), 'message': msg} for test, msg in result.skipped]
        }
    }
    
    # Write report to file
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    with open(report_path, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\nTest report saved to {report_path}")
    return result

if __name__ == '__main__':
    # Print header
    print("=" * 80)
    print("Wastewater Treatment Plant Control System Unit Tests")
    print("=" * 80)
    
    # Print status of controller imports
    if controllers_imported:
        print("Using actual controller modules")
    else:
        print("Using mock controller implementations (actual modules not found)")
    
    # Run tests
    print("\nRunning tests...")
    result = run_tests()
    
    # Exit with appropriate status code
    sys.exit(len(result.failures) + len(result.errors))
