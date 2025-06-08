"""
Intake Controller Module for Wastewater Treatment Plant
Handles raw water intake, screening, and flow regulation
"""

import math
import time
from typing import Dict, Any, Tuple

class IntakeController:
    """Controls the intake system including pumps, screens, and flow regulation"""
    
    def __init__(self, plc_interface=None):
        self.plc = plc_interface
        self.flow_setpoint = 150.0  # m³/h
        self.max_tank_level = 5.0   # meters
        self.min_tank_level = 1.0   # meters
        self.screen_runtime = 0     # seconds
        self.last_screen_clean = time.time()
        
    def regulate_flow(self, flow_setpoint: float, current_flow: float, tank_level: float) -> float:
        """
        Regulate intake flow using PI control algorithm
        
        Args:
            flow_setpoint: Desired flow rate (m³/h)
            current_flow: Current measured flow (m³/h)
            tank_level: Current tank level (m)
            
        Returns:
            Pump speed percentage (0-100)
        """
        # Safety checks
        if tank_level > self.max_tank_level * 0.95: # Adjusted to 95% of max_tank_level for emergency shutdown
            return 0  # Stop pumps if tank is too full
        
        if tank_level < self.min_tank_level:
            return 100  # Maximum flow if tank is too low
        
        # PI control algorithm
        error = flow_setpoint - current_flow
        kp = 2.0  # Proportional gain
        ki = 0.1  # Integral gain
        
        # Simple PI calculation
        proportional = kp * error
        integral = ki * error  # Simplified integral term
        
        output = 50 + proportional + integral  # Base speed 50%
        
        # Limit output to 0-100%
        return max(0, min(100, output))
    
    def screen_control(self, differential_pressure: float, runtime: int) -> bool:
        """
        Determine if screen cleaning is needed
        
        Args:
            differential_pressure: Pressure difference across screen (bar)
            runtime: Screen runtime since last cleaning (seconds)
            
        Returns:
            True if cleaning is needed
        """
        pressure_threshold = 0.2  # bar
        runtime_threshold = 3600  # 1 hour
        
        return differential_pressure > pressure_threshold or runtime > runtime_threshold
    
    def grit_removal_control(self, grit_level: float, flow_rate: float) -> Dict[str, Any]:
        """
        Control grit removal system
        
        Args:
            grit_level: Grit accumulation level (0-100%)
            flow_rate: Current flow rate (m³/h)
            
        Returns:
            Dictionary with control commands
        """
        commands = {
            'classifier_speed': 0,
            'conveyor_run': False,
            'wash_water_valve': False
        }
        
        if grit_level > 70:  # High grit level
            commands['classifier_speed'] = 80
            commands['conveyor_run'] = True
            commands['wash_water_valve'] = True
        elif grit_level > 40:  # Medium grit level
            commands['classifier_speed'] = 50
            commands['conveyor_run'] = True
            commands['wash_water_valve'] = False
        
        return commands
    
    def pump_control(self, pump_id: str, enable: bool, speed: float) -> Dict[str, Any]:
        """
        Control intake pumps
        
        Args:
            pump_id: Pump identifier (P101, P102, etc.)
            enable: Enable/disable pump
            speed: Pump speed percentage (0-100)
            
        Returns:
            Pump status and commands
        """
        status = {
            'pump_id': pump_id,
            'enabled': enable,
            'speed': max(0, min(100, speed)),
            'current': 0,
            'flow': 0
        }
        
        if enable and speed > 10:
            # Simulate pump performance
            status['current'] = 15 + (speed / 100) * 35  # 15-50 A
            status['flow'] = (speed / 100) * 200  # 0-200 m³/h
        
        return status
    
    def calculate_flow_distribution(self, total_flow: float, num_pumps: int) -> list:
        """
        Calculate optimal flow distribution among available pumps
        
        Args:
            total_flow: Required total flow (m³/h)
            num_pumps: Number of available pumps
            
        Returns:
            List of pump speeds
        """
        if num_pumps == 0:
            return []
        
        # Equal distribution strategy
        flow_per_pump = total_flow / num_pumps
        max_pump_flow = 200  # m³/h per pump
        
        speeds = []
        for i in range(num_pumps):
            speed = min(100, (flow_per_pump / max_pump_flow) * 100)
            speeds.append(speed)
        
        return speeds
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive intake system status"""
        return {
            'flow_setpoint': self.flow_setpoint,
            'tank_levels': {
                'max': self.max_tank_level,
                'min': self.min_tank_level
            },
            'screen_runtime': self.screen_runtime,
            'last_maintenance': self.last_screen_clean,
            'system_ready': True
        }
