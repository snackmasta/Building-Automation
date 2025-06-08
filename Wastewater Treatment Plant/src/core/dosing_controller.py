"""
Dosing Controller Module for Wastewater Treatment Plant
Handles chemical dosing for coagulation, pH control, and disinfection
"""

import math
import time
from typing import Dict, Any, List

class DosingController:
    """Controls chemical dosing systems for treatment optimization"""
    
    def __init__(self, plc_interface=None):
        self.plc = plc_interface
        self.chemical_tanks = {
            'coagulant': {'capacity': 5000, 'current_level': 4000, 'concentration': 10},  # L, %
            'flocculant': {'capacity': 2000, 'current_level': 1500, 'concentration': 0.5},
            'lime': {'capacity': 10000, 'current_level': 8000, 'concentration': 20},
            'chlorine': {'capacity': 1000, 'current_level': 800, 'concentration': 12},
            'sodium_hypochlorite': {'capacity': 3000, 'current_level': 2400, 'concentration': 10}
        }
        
    def coagulant_dosing(self, turbidity: float, flow_rate: float, 
                        water_temp: float, ph: float) -> Dict[str, Any]:
        """
        Calculate and control coagulant dosing
        
        Args:
            turbidity: Raw water turbidity (NTU)
            flow_rate: Water flow rate (m³/h)
            water_temp: Water temperature (°C)
            ph: Water pH
            
        Returns:
            Coagulant dosing commands
        """
        # Base dose calculation based on turbidity
        if turbidity < 5:
            base_dose = 2  # mg/L
        elif turbidity < 20:
            base_dose = 5
        elif turbidity < 50:
            base_dose = 10
        elif turbidity < 100:
            base_dose = 20
        else:
            base_dose = 30
        
        # Temperature correction factor
        temp_factor = 1.0 + (20 - water_temp) * 0.02  # Increase dose in cold water
        
        # pH correction factor
        if ph < 6.5:
            ph_factor = 1.2  # Higher dose for low pH
        elif ph > 8.0:
            ph_factor = 1.1  # Slightly higher dose for high pH
        else:
            ph_factor = 1.0  # Optimal pH range
        
        # Calculate final dose
        final_dose = base_dose * temp_factor * ph_factor
        
        # Calculate pump settings
        tank_info = self.chemical_tanks['coagulant']
        concentration = tank_info['concentration']  # %
        required_volume = (final_dose * flow_rate) / (concentration * 10)  # L/h
        
        # Pump capacity check
        max_pump_capacity = 100  # L/h
        pump_speed = min(100, (required_volume / max_pump_capacity) * 100)
        
        dosing_command = {
            'chemical': 'coagulant',
            'dose_mg_l': final_dose,
            'flow_rate_l_h': required_volume,
            'pump_speed': pump_speed,
            'tank_level': tank_info['current_level'],
            'tank_alarm': tank_info['current_level'] < tank_info['capacity'] * 0.1,
            'dosing_active': pump_speed > 5
        }
        
        return dosing_command
    
    def flocculant_dosing(self, turbidity_after_coag: float, flow_rate: float,
                         mixing_intensity: float) -> Dict[str, Any]:
        """
        Calculate and control polymer flocculant dosing
        
        Args:
            turbidity_after_coag: Turbidity after coagulation (NTU)
            flow_rate: Water flow rate (m³/h)
            mixing_intensity: Mixing G-value (1/s)
            
        Returns:
            Flocculant dosing commands
        """
        # Polymer dose based on residual turbidity
        if turbidity_after_coag < 2:
            polymer_dose = 0.1  # mg/L
        elif turbidity_after_coag < 5:
            polymer_dose = 0.3
        elif turbidity_after_coag < 10:
            polymer_dose = 0.5
        else:
            polymer_dose = 1.0
        
        # Mixing intensity correction
        if mixing_intensity > 50:
            mixing_factor = 1.2  # Higher dose for intense mixing
        elif mixing_intensity < 20:
            mixing_factor = 0.8  # Lower dose for gentle mixing
        else:
            mixing_factor = 1.0
        
        final_dose = polymer_dose * mixing_factor
        
        # Calculate pump settings
        tank_info = self.chemical_tanks['flocculant']
        concentration = tank_info['concentration']  # %
        required_volume = (final_dose * flow_rate) / (concentration * 10)  # L/h
        
        max_pump_capacity = 20  # L/h (smaller pump for polymer)
        pump_speed = min(100, (required_volume / max_pump_capacity) * 100)
        
        dosing_command = {
            'chemical': 'flocculant',
            'dose_mg_l': final_dose,
            'flow_rate_l_h': required_volume,
            'pump_speed': pump_speed,
            'tank_level': tank_info['current_level'],
            'tank_alarm': tank_info['current_level'] < tank_info['capacity'] * 0.1,
            'dosing_active': pump_speed > 2
        }
        
        return dosing_command
    
    def ph_control_dosing(self, current_ph: float, target_ph: float, 
                         flow_rate: float, alkalinity: float) -> Dict[str, Any]:
        """
        Calculate lime dosing for pH control
        
        Args:
            current_ph: Current water pH
            target_ph: Target pH value
            flow_rate: Water flow rate (m³/h)
            alkalinity: Water alkalinity (mg/L as CaCO3)
            
        Returns:
            pH control dosing commands
        """
        ph_error = target_ph - current_ph
        
        # Base lime dose calculation
        if abs(ph_error) < 0.1:
            lime_dose = 0  # No adjustment needed
        elif ph_error > 0:  # Need to raise pH
            if ph_error < 0.5:
                lime_dose = 10  # mg/L
            elif ph_error < 1.0:
                lime_dose = 25
            else:
                lime_dose = 50
        else:  # Need to lower pH (use acid instead)
            lime_dose = 0  # Would use acid, not implemented here
        
        # Alkalinity correction
        if alkalinity < 50:
            alkalinity_factor = 1.5  # More lime needed for low alkalinity water
        elif alkalinity > 200:
            alkalinity_factor = 0.8  # Less lime needed for high alkalinity water
        else:
            alkalinity_factor = 1.0
        
        final_dose = lime_dose * alkalinity_factor
        
        # Calculate feeder settings
        tank_info = self.chemical_tanks['lime']
        concentration = tank_info['concentration']  # %
        required_volume = (final_dose * flow_rate) / (concentration * 10)  # L/h
        
        max_feeder_capacity = 200  # L/h
        feeder_speed = min(100, (required_volume / max_feeder_capacity) * 100)
        
        dosing_command = {
            'chemical': 'lime',
            'dose_mg_l': final_dose,
            'flow_rate_l_h': required_volume,
            'feeder_speed': feeder_speed,
            'tank_level': tank_info['current_level'],
            'tank_alarm': tank_info['current_level'] < tank_info['capacity'] * 0.1,
            'dosing_active': feeder_speed > 5,
            'ph_error': ph_error
        }
        
        return dosing_command
    
    def disinfection_dosing(self, flow_rate: float, water_quality: Dict[str, float],
                          contact_time: float, disinfectant_type: str = 'chlorine') -> Dict[str, Any]:
        """
        Calculate disinfectant dosing for pathogen removal
        
        Args:
            flow_rate: Water flow rate (m³/h)
            water_quality: Dictionary with turbidity, pH, temperature
            contact_time: Available contact time (minutes)
            disinfectant_type: Type of disinfectant ('chlorine' or 'sodium_hypochlorite')
            
        Returns:
            Disinfection dosing commands
        """
        turbidity = water_quality.get('turbidity', 1.0)
        ph = water_quality.get('ph', 7.0)
        temperature = water_quality.get('temperature', 20.0)
        
        # Base chlorine dose for 3-log removal
        base_dose = 2.0  # mg/L
        
        # CT (Concentration × Time) requirement
        required_ct = 6.0  # mg·min/L for 3-log Giardia removal at pH 7, 10°C
        
        # pH correction factor
        if ph < 6.5:
            ph_factor = 0.8  # More effective at low pH
        elif ph > 8.0:
            ph_factor = 1.5  # Less effective at high pH
        else:
            ph_factor = 1.0
        
        # Temperature correction factor
        temp_factor = 1.5 ** ((20 - temperature) / 10)  # Q10 = 1.5
        
        # Turbidity factor
        if turbidity > 1.0:
            turbidity_factor = 1 + (turbidity - 1) * 0.1
        else:
            turbidity_factor = 1.0
        
        # Calculate required dose
        required_dose = (required_ct / contact_time) * ph_factor * temp_factor * turbidity_factor
        final_dose = max(base_dose, required_dose)
        
        # Add residual requirement
        residual_dose = 0.5  # mg/L free chlorine residual
        total_dose = final_dose + residual_dose
        
        # Calculate pump settings based on disinfectant type
        tank_info = self.chemical_tanks[disinfectant_type]
        concentration = tank_info['concentration']  # %
        
        if disinfectant_type == 'chlorine':
            # Gas chlorine (100% active)
            required_flow = total_dose * flow_rate / 1000  # kg/h
            max_capacity = 10  # kg/h
        else:
            # Sodium hypochlorite solution
            required_volume = (total_dose * flow_rate) / (concentration * 10)  # L/h
            required_flow = required_volume
            max_capacity = 150  # L/h
        
        pump_speed = min(100, (required_flow / max_capacity) * 100)
        
        dosing_command = {
            'chemical': disinfectant_type,
            'dose_mg_l': total_dose,
            'residual_target': residual_dose,
            'ct_value': total_dose * contact_time,
            'flow_rate': required_flow,
            'pump_speed': pump_speed,
            'tank_level': tank_info['current_level'],
            'tank_alarm': tank_info['current_level'] < tank_info['capacity'] * 0.1,
            'dosing_active': pump_speed > 3
        }
        
        return dosing_command
    
    def chemical_inventory_management(self) -> Dict[str, Any]:
        """
        Monitor chemical inventory and generate reorder alerts
        
        Returns:
            Inventory status and alerts
        """
        inventory_status = {
            'chemicals': [],
            'low_level_alerts': [],
            'emergency_alerts': [],
            'reorder_recommendations': []
        }
        
        for chemical, tank_info in self.chemical_tanks.items():
            level_percent = (tank_info['current_level'] / tank_info['capacity']) * 100
            
            chemical_status = {
                'name': chemical,
                'level_percent': level_percent,
                'level_liters': tank_info['current_level'],
                'capacity': tank_info['capacity'],
                'concentration': tank_info['concentration'],
                'status': 'normal'
            }
            
            # Emergency alert threshold: <= 5%
            if level_percent <= 5.0:  # Changed from < 5 to <= 5.0
                chemical_status['status'] = 'emergency'
                inventory_status['emergency_alerts'].append(
                    f"EMERGENCY: {chemical} level critical at {level_percent:.1f}% ({tank_info['current_level']}L). Immediate action required."
                )
            # Low level alert threshold: < 15% (but not emergency)
            elif level_percent < 15.0: 
                chemical_status['status'] = 'low'
                inventory_status['low_level_alerts'].append(
                    f"LOW LEVEL: {chemical} at {level_percent:.1f}% ({tank_info['current_level']}L). Consider reordering."
                )
                inventory_status['reorder_recommendations'].append(
                    f"Reorder {chemical} soon. Current level: {level_percent:.1f}%"
                )
            
            inventory_status['chemicals'].append(chemical_status)
            
        return inventory_status
    
    def dosing_system_calibration(self, chemical: str, test_duration: int = 300) -> Dict[str, Any]:
        """
        Perform dosing system calibration
        
        Args:
            chemical: Chemical system to calibrate
            test_duration: Calibration test duration (seconds)
            
        Returns:
            Calibration results
        """
        if chemical not in self.chemical_tanks:
            return {'error': 'Chemical not found'}
        
        calibration = {
            'chemical': chemical,
            'test_duration': test_duration,
            'pump_speeds_tested': [25, 50, 75, 100],
            'flow_rates_measured': [],
            'accuracy_percent': 0,
            'calibration_factor': 1.0,
            'status': 'pending'
        }
        
        # Simulate calibration measurements
        for speed in calibration['pump_speeds_tested']:
            # Simulate flow rate measurement with some variability
            expected_flow = speed * 0.5  # L/h per % speed
            measured_flow = expected_flow * (0.95 + 0.1 * (speed / 100))
            calibration['flow_rates_measured'].append(measured_flow)
        
        # Calculate accuracy
        total_error = 0
        for i, speed in enumerate(calibration['pump_speeds_tested']):
            expected = speed * 0.5
            measured = calibration['flow_rates_measured'][i]
            error = abs(expected - measured) / expected
            total_error += error
        
        accuracy = (1 - total_error / len(calibration['pump_speeds_tested'])) * 100
        calibration['accuracy_percent'] = accuracy
        
        # Determine calibration factor
        if accuracy > 95:
            calibration['calibration_factor'] = 1.0
            calibration['status'] = 'passed'
        elif accuracy > 90:
            calibration['calibration_factor'] = 0.98
            calibration['status'] = 'passed_with_adjustment'
        else:
            calibration['calibration_factor'] = 0.95
            calibration['status'] = 'failed'
        
        return calibration
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive dosing system status"""
        return {
            'chemical_tanks': self.chemical_tanks,
            'system_ready': True,
            'dosing_pumps_active': 0,
            'total_chemicals': len(self.chemical_tanks),
            'control_mode': 'automatic'
        }
