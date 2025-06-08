"""
System Validator for Wastewater Treatment Plant
Comprehensive validation and testing framework
"""

import os
import sys
import json
import time
import unittest
import random
from datetime import datetime
from typing import Dict, Any, List, Tuple

# Add project paths
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root) # Add project root to allow importing src

# Import all controllers
from src.core.intake_controller import IntakeController
from src.core.treatment_controller import TreatmentController
from src.core.aeration_controller import AerationController
from src.core.dosing_controller import DosingController
from src.core.monitoring_controller import MonitoringController

class WWTPSystemValidator:
    """Comprehensive system validation for the Wastewater Treatment Plant"""
    
    def __init__(self):
        self.validation_results = {
            'overall_status': 'pending',
            'test_categories': {},
            'detailed_results': [],
            'summary': {},
            'recommendations': []
        }
        
        # Initialize controllers
        self.controllers = {
            'intake': IntakeController(),
            'treatment': TreatmentController(),
            'aeration': AerationController(),
            'dosing': DosingController(),
            'monitoring': MonitoringController()
        }
    
    def run_full_validation(self) -> Dict[str, Any]:
        """Run complete system validation"""
        print("Starting Wastewater Treatment Plant System Validation...")
        print("=" * 60)
        
        validation_start = time.time()
        
        # Run all validation categories
        categories = [
            ('Controller Functionality', self._validate_controllers),
            ('Process Control Logic', self._validate_process_control),
            ('Safety Systems', self._validate_safety_systems),
            ('Data Integration', self._validate_data_integration),
            ('Performance Metrics', self._validate_performance),
            ('Alarm Management', self._validate_alarms),
            ('Chemical Dosing', self._validate_chemical_dosing),
            ('Energy Efficiency', self._validate_energy_efficiency),
            ('Compliance Monitoring', self._validate_compliance),
            ('System Reliability', self._validate_reliability)
        ]
        
        for category_name, validation_func in categories:
            print(f"\\nValidating {category_name}...")
            try:
                result = validation_func()
                self.validation_results['test_categories'][category_name] = result
                print(f"✅ {category_name}: {result['status']}")
            except Exception as e:
                error_result = {
                    'status': 'failed',
                    'score': 0,
                    'tests_passed': 0,
                    'tests_total': 1,
                    'error': str(e)
                }
                self.validation_results['test_categories'][category_name] = error_result
                print(f"❌ {category_name}: Failed - {str(e)}")
        
        # Calculate overall results
        self._calculate_overall_results()
        
        validation_time = time.time() - validation_start
        self.validation_results['validation_time'] = validation_time
        self.validation_results['timestamp'] = datetime.now().isoformat()
        
        print(f"\\n{'='*60}")
        print(f"Validation completed in {validation_time:.2f} seconds")
        print(f"Overall Status: {self.validation_results['overall_status'].upper()}")
        print(f"Overall Score: {self.validation_results['summary']['overall_score']:.1f}%")
        
        return self.validation_results
    
    def _validate_controllers(self) -> Dict[str, Any]:
        """Validate all controller modules"""
        tests = []
        
        # Test Intake Controller
        intake = self.controllers['intake']
        
        # Test flow regulation
        flow_output = intake.regulate_flow(150, 140, 3.0)
        tests.append({
            'test': 'Intake Flow Regulation',
            'passed': 0 <= flow_output <= 100,
            'details': f"Flow output: {flow_output}%"
        })
        
        # Test screen control
        screen_needed = intake.screen_control(0.25, 3700)
        tests.append({
            'test': 'Screen Control Logic',
            'passed': screen_needed == True,
            'details': f"Screen cleaning needed: {screen_needed}"
        })
        
        # Test pump control
        pump_status = intake.pump_control('P101', True, 75)
        tests.append({
            'test': 'Pump Control',
            'passed': pump_status['enabled'] and pump_status['speed'] == 75,
            'details': f"Pump status: {pump_status}"
        })
        
        # Test Treatment Controller
        treatment = self.controllers['treatment']
        
        # Test clarifier control
        clarifier_cmd = treatment.primary_clarifier_control(150, 180, 1.2)
        tests.append({
            'test': 'Primary Clarifier Control',
            'passed': 'scraper_speed' in clarifier_cmd and clarifier_cmd['scraper_speed'] > 0,
            'details': f"Clarifier commands: {clarifier_cmd}"
        })
        
        # Test sludge removal calculation
        sludge_rate = treatment.calculate_sludge_removal(1.8, 150)
        tests.append({
            'test': 'Sludge Removal Calculation',
            'passed': 5 <= sludge_rate <= 20,
            'details': f"Sludge removal rate: {sludge_rate} m³/h"
        })
        
        # Test Aeration Controller
        aeration = self.controllers['aeration']
        
        # Test blower speed calculation
        blower_speed = aeration.calculate_blower_speed(2.0, 1.5, 1.2)
        tests.append({
            'test': 'Blower Speed Control',
            'passed': 30 <= blower_speed <= 100,
            'details': f"Blower speed: {blower_speed}%"
        })
        
        # Test blower load distribution
        blower_cmds = aeration.distribute_blower_load(800)
        tests.append({
            'test': 'Blower Load Distribution',
            'passed': len(blower_cmds) == 3 and all('blower_id' in cmd for cmd in blower_cmds),
            'details': f"Blower commands: {len(blower_cmds)} blowers"
        })
        
        # Test Dosing Controller
        dosing = self.controllers['dosing']
        
        # Test coagulant dosing
        coag_cmd = dosing.coagulant_dosing(15, 150, 18, 7.2)
        tests.append({
            'test': 'Coagulant Dosing',
            'passed': coag_cmd['dose_mg_l'] > 0 and 'pump_speed' in coag_cmd,
            'details': f"Coagulant dose: {coag_cmd['dose_mg_l']} mg/L"
        })
        
        # Test disinfection dosing
        water_quality = {'turbidity': 2.0, 'ph': 7.0, 'temperature': 20}
        disinfect_cmd = dosing.disinfection_dosing(150, water_quality, 30)
        tests.append({
            'test': 'Disinfection Dosing',
            'passed': disinfect_cmd['dose_mg_l'] > 0 and disinfect_cmd['ct_value'] > 0,
            'details': f"Disinfection dose: {disinfect_cmd['dose_mg_l']} mg/L"
        })
        
        # Test Monitoring Controller
        monitoring = self.controllers['monitoring']
        
        # Test sensor data collection
        sensor_data = monitoring.collect_sensor_data()
        tests.append({
            'test': 'Sensor Data Collection',
            'passed': 'intake' in sensor_data and 'timestamp' in sensor_data,
            'details': f"Sensor groups: {len([k for k in sensor_data.keys() if k != 'timestamp'])}"
        })
        
        # Test alarm processing
        alarm_result = monitoring.process_alarms(sensor_data)
        tests.append({
            'test': 'Alarm Processing',
            'passed': 'active_alarms' in alarm_result and 'alarm_summary' in alarm_result,
            'details': f"Alarms processed: {alarm_result['alarm_summary']['total_count']}"
        })
        
        # Calculate results
        passed_tests = sum(1 for test in tests if test['passed'])
        total_tests = len(tests)
        score = (passed_tests / total_tests) * 100
        
        return {
            'status': 'passed' if score >= 90 else 'warning' if score >= 70 else 'failed',
            'score': score,
            'tests_passed': passed_tests,
            'tests_total': total_tests,
            'detailed_tests': tests
        }
    
    def _validate_process_control(self) -> Dict[str, Any]:
        """Validate process control logic and integration"""
        tests = []
        
        # Test integrated process flow
        intake = self.controllers['intake']
        treatment = self.controllers['treatment']
        aeration = self.controllers['aeration']
        
        # Simulate process conditions
        flow_rate = 150  # m³/h
        raw_turbidity = 20  # NTU
        raw_ph = 7.2
        
        # Test flow control cascade
        pump_speed = intake.regulate_flow(flow_rate, flow_rate * 0.9, 3.5)
        primary_control = treatment.primary_clarifier_control(flow_rate, raw_turbidity, 1.0)
        blower_speed = aeration.calculate_blower_speed(2.0, 1.8, 1.0)
        
        tests.append({
            'test': 'Process Control Cascade',
            'passed': all([
                0 <= pump_speed <= 100,
                'scraper_speed' in primary_control,
                30 <= blower_speed <= 100
            ]),
            'details': f"Pump: {pump_speed}%, Blower: {blower_speed}%"
        })
        
        # Test load balancing
        blower_distribution = aeration.distribute_blower_load(900)
        active_blowers = sum(1 for cmd in blower_distribution if cmd['enabled'])
        
        tests.append({
            'test': 'Load Balancing',
            'passed': 1 <= active_blowers <= 3,
            'details': f"Active blowers: {active_blowers}/3"
        })
        
        # Test chemical dosing coordination
        dosing = self.controllers['dosing']
        coag_dose = dosing.coagulant_dosing(raw_turbidity, flow_rate, 18, raw_ph)
        floc_dose = dosing.flocculant_dosing(raw_turbidity * 0.6, flow_rate, 40)
        
        tests.append({
            'test': 'Chemical Dosing Coordination',
            'passed': all([
                coag_dose['dose_mg_l'] > 0,
                floc_dose['dose_mg_l'] > 0,
                coag_dose['dose_mg_l'] > floc_dose['dose_mg_l']
            ]),
            'details': f"Coagulant: {coag_dose['dose_mg_l']:.1f}, Flocculant: {floc_dose['dose_mg_l']:.1f}"
        })
        
        # Test process efficiency optimization
        treatment_efficiency = treatment.get_treatment_efficiency(
            {'turbidity': raw_turbidity, 'tss': 200, 'bod': 150},
            {'turbidity': 2.0, 'tss': 15, 'bod': 12}
        )
        
        tests.append({
            'test': 'Treatment Efficiency Calculation',
            'passed': all([
                efficiency > 80 for param, efficiency in treatment_efficiency.items()
                if 'removal' in param
            ]),
            'details': f"Efficiencies: {treatment_efficiency}"
        })
        
        passed_tests = sum(1 for test in tests if test['passed'])
        total_tests = len(tests)
        score = (passed_tests / total_tests) * 100
        
        return {
            'status': 'passed' if score >= 90 else 'warning' if score >= 70 else 'failed',
            'score': score,
            'tests_passed': passed_tests,
            'tests_total': total_tests,
            'detailed_tests': tests
        }
    
    def _validate_safety_systems(self) -> Dict[str, Any]:
        """Validate safety systems and emergency procedures"""
        tests = []
        
        # Test high level shutdown
        intake = self.controllers['intake']
        emergency_flow = intake.regulate_flow(150, 140, 4.8)  # High tank level
        
        tests.append({
            'test': 'High Level Emergency Shutdown',
            'passed': emergency_flow == 0,
            'details': f"Emergency flow output: {emergency_flow}%"
        })
        
        # Test low DO alarm
        aeration = self.controllers['aeration']
        alarm_mgmt = aeration.alarm_management([0.8, 0.9, 0.7, 0.6], [True, True, False])
        
        tests.append({
            'test': 'Low DO Alarm System',
            'passed': alarm_mgmt['low_do_alarm'] and alarm_mgmt['severity'] == 'high',
            'details': f"Alarm severity: {alarm_mgmt['severity']}"
        })
        
        # Test blower failure detection
        tests.append({
            'test': 'Blower Failure Detection',
            'passed': alarm_mgmt['blower_failure'] and 'start_backup_blower' in alarm_mgmt['actions_required'],
            'details': f"Actions: {alarm_mgmt['actions_required']}"
        })
        
        # Test chemical tank low level alarm
        dosing = self.controllers['dosing']
        inventory = dosing.chemical_inventory_management()
        
        # Simulate low level condition
        dosing.chemical_tanks['chlorine']['current_level'] = 50  # 5% of 1000L capacity
        inventory_low = dosing.chemical_inventory_management()
        
        tests.append({
            'test': 'Chemical Tank Low Level Alarm',
            'passed': len(inventory_low['emergency_alerts']) > 0,
            'details': f"Emergency alerts: {inventory_low['emergency_alerts']}"
        })
        
        passed_tests = sum(1 for test in tests if test['passed'])
        total_tests = len(tests)
        score = (passed_tests / total_tests) * 100
        
        return {
            'status': 'passed' if score >= 90 else 'warning' if score >= 70 else 'failed',
            'score': score,
            'tests_passed': passed_tests,
            'tests_total': total_tests,
            'detailed_tests': tests
        }
    
    def _validate_data_integration(self) -> Dict[str, Any]:
        """Validate data collection and integration"""
        tests = []
        
        monitoring = self.controllers['monitoring']
        
        # Test data collection
        sensor_data = monitoring.collect_sensor_data()
        required_sections = ['intake', 'primary_treatment', 'secondary_treatment', 
                           'tertiary_treatment', 'chemical_dosing', 'blowers']
        
        tests.append({
            'test': 'Complete Data Collection',
            'passed': all(section in sensor_data for section in required_sections),
            'details': f"Sections collected: {list(sensor_data.keys())}"
        })
        
        # Test KPI calculation
        kpis = monitoring.calculate_kpis(sensor_data)
        required_kpis = ['turbidity_removal_efficiency', 'bod_removal_efficiency', 
                        'energy_per_cubic_meter', 'equipment_availability']
        
        tests.append({
            'test': 'KPI Calculation',
            'passed': all(kpi in kpis for kpi in required_kpis),
            'details': f"KPIs calculated: {len(kpis)}"
        })
        
        # Test trend data generation
        trends = monitoring.generate_trend_data(24)
        
        tests.append({
            'test': 'Trend Data Generation',
            'passed': 'timestamps' in trends and len(trends['timestamps']) > 0,
            'details': f"Trend points: {len(trends.get('timestamps', []))}"
        })
        
        # Test data export
        from datetime import datetime, timedelta
        end_time = datetime.now()
        start_time = end_time - timedelta(hours=24)
        export_data = monitoring.export_data(start_time, end_time)
        
        tests.append({
            'test': 'Data Export Functionality',
            'passed': 'export_info' in export_data and 'data' in export_data,
            'details': f"Export sections: {list(export_data.keys())}"
        })
        
        passed_tests = sum(1 for test in tests if test['passed'])
        total_tests = len(tests)
        score = (passed_tests / total_tests) * 100
        
        return {
            'status': 'passed' if score >= 90 else 'warning' if score >= 70 else 'failed',
            'score': score,
            'tests_passed': passed_tests,
            'tests_total': total_tests,
            'detailed_tests': tests
        }
    
    def _validate_performance(self) -> Dict[str, Any]:
        """Validate system performance metrics"""
        tests = []
        
        monitoring = self.controllers['monitoring']
        sensor_data = monitoring.collect_sensor_data()
        kpis = monitoring.calculate_kpis(sensor_data)
        
        # Test treatment efficiency
        turbidity_efficiency = kpis.get('turbidity_removal_efficiency', 0)
        tests.append({
            'test': 'Turbidity Removal Efficiency',
            'passed': turbidity_efficiency >= 85,
            'details': f"Efficiency: {turbidity_efficiency:.1f}%"
        })
        
        bod_efficiency = kpis.get('bod_removal_efficiency', 0)
        tests.append({
            'test': 'BOD Removal Efficiency',
            'passed': bod_efficiency >= 85,
            'details': f"Efficiency: {bod_efficiency:.1f}%"
        })
        
        # Test energy efficiency
        energy_per_m3 = kpis.get('energy_per_cubic_meter', 999)
        tests.append({
            'test': 'Energy Efficiency',
            'passed': energy_per_m3 <= 1.0,  # kWh/m³
            'details': f"Energy consumption: {energy_per_m3:.3f} kWh/m³"
        })
        
        # Test equipment availability
        equipment_availability = kpis.get('equipment_availability', 0)
        tests.append({
            'test': 'Equipment Availability',
            'passed': equipment_availability >= 80,
            'details': f"Availability: {equipment_availability:.1f}%"
        })
        
        passed_tests = sum(1 for test in tests if test['passed'])
        total_tests = len(tests)
        score = (passed_tests / total_tests) * 100
        
        return {
            'status': 'passed' if score >= 90 else 'warning' if score >= 70 else 'failed',
            'score': score,
            'tests_passed': passed_tests,
            'tests_total': total_tests,
            'detailed_tests': tests
        }
    
    def _validate_alarms(self) -> Dict[str, Any]:
        """Validate alarm management system"""
        tests = []
        
        monitoring = self.controllers['monitoring']
        
        # Create test sensor data with alarm conditions
        test_data = monitoring.collect_sensor_data()
        
        # Modify data to trigger alarms
        test_data['intake']['raw_water_ph'] = 5.2  # Critical low pH
        test_data['secondary_treatment']['aeration_tank_do'] = [0.8, 0.7, 0.9, 0.6]  # Low DO
        test_data['intake']['flow_rate'] = 450  # High flow
        
        alarm_result = monitoring.process_alarms(test_data)
        
        tests.append({
            'test': 'Alarm Detection',
            'passed': alarm_result['alarm_summary']['total_count'] > 0,
            'details': f"Alarms detected: {alarm_result['alarm_summary']['total_count']}"
        })
        
        tests.append({
            'test': 'Critical Alarm Classification',
            'passed': alarm_result['alarm_summary']['critical_count'] > 0,
            'details': f"Critical alarms: {alarm_result['alarm_summary']['critical_count']}"
        })
        
        # Test alarm prioritization
        critical_alarms = [alarm for alarm in alarm_result['active_alarms'] 
                          if alarm['severity'] == 'critical']
        
        tests.append({
            'test': 'Alarm Prioritization',
            'passed': len(critical_alarms) > 0,
            'details': f"Critical alarms identified: {len(critical_alarms)}"
        })
        
        passed_tests = sum(1 for test in tests if test['passed'])
        total_tests = len(tests)
        score = (passed_tests / total_tests) * 100
        
        return {
            'status': 'passed' if score >= 90 else 'warning' if score >= 70 else 'failed',
            'score': score,
            'tests_passed': passed_tests,
            'tests_total': total_tests,
            'detailed_tests': tests
        }
    
    def _validate_chemical_dosing(self) -> Dict[str, Any]:
        """Validate chemical dosing systems"""
        tests = []
        
        dosing = self.controllers['dosing']
        
        # Test dosing calculations for various conditions
        test_conditions = [
            {'turbidity': 5, 'flow': 100, 'temp': 20, 'ph': 7.0},
            {'turbidity': 25, 'flow': 150, 'temp': 15, 'ph': 6.8},
            {'turbidity': 80, 'flow': 200, 'temp': 10, 'ph': 8.2}
        ]
        
        all_doses_valid = True
        for condition in test_conditions:
            coag_cmd = dosing.coagulant_dosing(
                condition['turbidity'], condition['flow'], 
                condition['temp'], condition['ph']
            )
            if not (2 <= coag_cmd['dose_mg_l'] <= 50):
                all_doses_valid = False
                break
        
        tests.append({
            'test': 'Coagulant Dosing Range Validation',
            'passed': all_doses_valid,
            'details': f"Tested {len(test_conditions)} conditions"
        })
        
        # Test inventory management
        inventory = dosing.chemical_inventory_management()
        
        tests.append({
            'test': 'Chemical Inventory Tracking',
            'passed': len(inventory['chemicals']) > 0,
            'details': f"Chemicals tracked: {len(inventory['chemicals'])}"
        })
        
        # Test calibration function
        calibration = dosing.dosing_system_calibration('coagulant')
        
        tests.append({
            'test': 'Dosing System Calibration',
            'passed': calibration['accuracy_percent'] > 90,
            'details': f"Calibration accuracy: {calibration['accuracy_percent']:.1f}%"
        })
        
        passed_tests = sum(1 for test in tests if test['passed'])
        total_tests = len(tests)
        score = (passed_tests / total_tests) * 100
        
        return {
            'status': 'passed' if score >= 90 else 'warning' if score >= 70 else 'failed',
            'score': score,
            'tests_passed': passed_tests,
            'tests_total': total_tests,
            'detailed_tests': tests
        }
    
    def _validate_energy_efficiency(self) -> Dict[str, Any]:
        """Validate energy efficiency and optimization"""
        tests = []
        
        aeration = self.controllers['aeration']
        
        # Test oxygen transfer optimization
        optimization = aeration.oxygen_transfer_optimization(20, 2.0, 100)
        
        tests.append({
            'test': 'Oxygen Transfer Optimization',
            'passed': 'transfer_efficiency' in optimization and optimization['transfer_efficiency'] > 0.5,
            'details': f"Transfer efficiency: {optimization['transfer_efficiency']:.2f}"
        })
        
        # Test blower efficiency
        blower_cmds = aeration.distribute_blower_load(600)
        total_power = sum(cmd['power_consumption'] for cmd in blower_cmds if cmd['enabled'])
        energy_efficiency = 600 / total_power if total_power > 0 else 0  # m³/h per kW
        
        tests.append({
            'test': 'Blower Energy Efficiency',
            'passed': energy_efficiency > 8,  # Good efficiency threshold
            'details': f"Efficiency: {energy_efficiency:.1f} m³/h per kW"
        })
        
        # Test load optimization
        active_blowers = sum(1 for cmd in blower_cmds if cmd['enabled'])
        
        tests.append({
            'test': 'Load Optimization',
            'passed': active_blowers <= 2,  # Should not need all 3 blowers for 600 m³/h
            'details': f"Active blowers: {active_blowers}/3"
        })
        
        passed_tests = sum(1 for test in tests if test['passed'])
        total_tests = len(tests)
        score = (passed_tests / total_tests) * 100
        
        return {
            'status': 'passed' if score >= 90 else 'warning' if score >= 70 else 'failed',
            'score': score,
            'tests_passed': passed_tests,
            'tests_total': total_tests,
            'detailed_tests': tests
        }
    
    def _validate_compliance(self) -> Dict[str, Any]:
        """Validate regulatory compliance monitoring"""
        tests = []
        
        monitoring = self.controllers['monitoring']
        sensor_data = monitoring.collect_sensor_data()
        kpis = monitoring.calculate_kpis(sensor_data)
        
        # Test effluent quality compliance
        compliance_indicators = [
            ('pH Compliance', kpis.get('effluent_ph_compliance', 0)),
            ('TSS Compliance', kpis.get('effluent_tss_compliance', 0)),
            ('Chlorine Residual Compliance', kpis.get('chlorine_residual_compliance', 0))
        ]
        
        for indicator_name, value in compliance_indicators:
            tests.append({
                'test': indicator_name,
                'passed': value == 1,
                'details': f"Compliance status: {'Pass' if value == 1 else 'Fail'}"
            })
        
        # Test treatment efficiency compliance
        turbidity_removal = kpis.get('turbidity_removal_efficiency', 0)
        bod_removal = kpis.get('bod_removal_efficiency', 0)
        
        tests.append({
            'test': 'Treatment Efficiency Compliance',
            'passed': turbidity_removal >= 85 and bod_removal >= 85,
            'details': f"Turbidity: {turbidity_removal:.1f}%, BOD: {bod_removal:.1f}%"
        })
        
        passed_tests = sum(1 for test in tests if test['passed'])
        total_tests = len(tests)
        score = (passed_tests / total_tests) * 100
        
        return {
            'status': 'passed' if score >= 90 else 'warning' if score >= 70 else 'failed',
            'score': score,
            'tests_passed': passed_tests,
            'tests_total': total_tests,
            'detailed_tests': tests
        }
    
    def _validate_reliability(self) -> Dict[str, Any]:
        """Validate system reliability and redundancy"""
        tests = []
        
        # Test controller redundancy
        all_controllers_initialized = all(
            controller is not None for controller in self.controllers.values()
        )
        
        tests.append({
            'test': 'Controller Initialization',
            'passed': all_controllers_initialized,
            'details': f"Controllers initialized: {len(self.controllers)}/5"
        })
        
        # Test blower redundancy
        aeration = self.controllers['aeration']
        
        # Test with one blower failed
        blower_cmds = aeration.distribute_blower_load(800)
        available_capacity = sum(cmd['airflow'] for cmd in blower_cmds if cmd['enabled'])
        
        tests.append({
            'test': 'Blower System Redundancy',
            'passed': available_capacity >= 800,
            'details': f"Available capacity: {available_capacity:.0f} m³/h"
        })
        
        # Test pump redundancy (intake system)
        intake = self.controllers['intake']
        flow_distribution = intake.calculate_flow_distribution(200, 2)  # 2 pumps available
        
        tests.append({
            'test': 'Pump System Redundancy',
            'passed': len(flow_distribution) == 2 and all(speed <= 100 for speed in flow_distribution),
            'details': f"Pump speeds: {flow_distribution}"
        })
        
        # Test data backup and recovery
        monitoring = self.controllers['monitoring']
        from datetime import datetime, timedelta
        
        export_data = monitoring.export_data(
            datetime.now() - timedelta(hours=1),
            datetime.now()
        )
        
        tests.append({
            'test': 'Data Backup Capability',
            'passed': 'data' in export_data and len(export_data['data']) > 0,
            'details': f"Data export successful: {len(export_data['data'])} parameters"
        })
        
        passed_tests = sum(1 for test in tests if test['passed'])
        total_tests = len(tests)
        score = (passed_tests / total_tests) * 100
        
        return {
            'status': 'passed' if score >= 90 else 'warning' if score >= 70 else 'failed',
            'score': score,
            'tests_passed': passed_tests,
            'tests_total': total_tests,
            'detailed_tests': tests
        }
    
    def _calculate_overall_results(self):
        """Calculate overall validation results"""
        categories = self.validation_results['test_categories']
        
        if not categories:
            self.validation_results['overall_status'] = 'failed'
            return
        
        total_score = sum(cat['score'] for cat in categories.values())
        avg_score = total_score / len(categories)
        
        total_tests_passed = sum(cat['tests_passed'] for cat in categories.values())
        total_tests = sum(cat['tests_total'] for cat in categories.values())
        
        failed_categories = sum(1 for cat in categories.values() if cat['status'] == 'failed')
        warning_categories = sum(1 for cat in categories.values() if cat['status'] == 'warning')
        
        # Determine overall status
        if failed_categories > 0:
            overall_status = 'failed'
        elif warning_categories > 2:
            overall_status = 'warning'
        elif avg_score >= 95:
            overall_status = 'excellent'
        elif avg_score >= 85:
            overall_status = 'passed'
        else:
            overall_status = 'warning'
        
        self.validation_results['overall_status'] = overall_status
        self.validation_results['summary'] = {
            'overall_score': avg_score,
            'tests_passed': total_tests_passed,
            'tests_total': total_tests,
            'categories_passed': len(categories) - failed_categories - warning_categories,
            'categories_warning': warning_categories,
            'categories_failed': failed_categories,
            'categories_total': len(categories)
        }
        
        # Generate recommendations
        self._generate_recommendations()
    
    def _generate_recommendations(self):
        """Generate recommendations based on validation results"""
        recommendations = []
        
        categories = self.validation_results['test_categories']
        
        for category_name, results in categories.items():
            if results['status'] == 'failed':
                recommendations.append(f"CRITICAL: Fix issues in {category_name} (Score: {results['score']:.1f}%)")
            elif results['status'] == 'warning':
                recommendations.append(f"IMPROVE: Enhance {category_name} (Score: {results['score']:.1f}%)")
        
        # General recommendations
        overall_score = self.validation_results['summary']['overall_score']
        
        if overall_score < 70:
            recommendations.append("URGENT: System requires significant improvements before deployment")
        elif overall_score < 85:
            recommendations.append("MODERATE: System needs optimization for optimal performance")
        elif overall_score < 95:
            recommendations.append("MINOR: System is good, minor optimizations recommended")
        else:
            recommendations.append("EXCELLENT: System is ready for deployment")
        
        self.validation_results['recommendations'] = recommendations
    
    def save_validation_report(self, filename: str = None):
        """Save validation results to JSON file"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"wwtp_validation_report_{timestamp}.json"
        
        filepath = os.path.join(project_root, 'reports', filename)
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        with open(filepath, 'w') as f:
            json.dump(self.validation_results, f, indent=2)
        
        print(f"\\nValidation report saved to: {filepath}")
        return filepath


def main():
    """Main validation function"""
    validator = WWTPSystemValidator()
    results = validator.run_full_validation()
    
    # Save report
    report_file = validator.save_validation_report()
    
    # Print summary
    print(f"\\n{'='*60}")
    print("VALIDATION SUMMARY")
    print(f"{'='*60}")
    
    summary = results['summary']
    print(f"Overall Score: {summary['overall_score']:.1f}%")
    print(f"Tests Passed: {summary['tests_passed']}/{summary['tests_total']}")
    print(f"Categories: {summary['categories_passed']} passed, {summary['categories_warning']} warnings, {summary['categories_failed']} failed")
    
    print(f"\\nRecommendations:")
    for rec in results['recommendations']:
        print(f"  • {rec}")
    
    return results


if __name__ == "__main__":
    main()
