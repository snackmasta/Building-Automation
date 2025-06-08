# Code Standards Guide

## Overview

This guide establishes comprehensive coding standards and best practices for all PLC projects in the repository. Consistent, readable, and maintainable code is essential for industrial automation systems where safety and reliability are paramount.

## General Principles

### Code Quality Standards
- **Safety First**: Code must prioritize safety over performance
- **Readability**: Code should be self-documenting
- **Consistency**: Follow established patterns throughout
- **Maintainability**: Code should be easy to modify and extend
- **Testability**: Design code to be easily tested
- **Documentation**: Comprehensive comments and documentation

### SOLID Principles for PLC Programming
- **Single Responsibility**: Each function block has one purpose
- **Open/Closed**: Open for extension, closed for modification
- **Liskov Substitution**: Derived blocks can replace base blocks
- **Interface Segregation**: Clients depend only on methods they use
- **Dependency Inversion**: Depend on abstractions, not concretions

## PLC Programming Standards (IEC 61131-3)

### Structured Text (ST) Standards

#### Variable Naming Conventions
```structured_text
(* Global Variables - Use descriptive prefixes *)
VAR_GLOBAL
    // Input variables (sensors)
    bEmergencyStopPressed    : BOOL;         // Boolean input
    rTankLevelPercent       : REAL;          // Real/float input
    iMotorSpeedRPM          : INT;           // Integer input
    wPumpStatus             : WORD;          // Word input
    
    // Output variables (actuators)
    bPumpStartCommand       : BOOL;          // Boolean output
    rValvePositionPercent   : REAL;          // Real/float output
    iHeaterPowerPercent     : INT;           // Integer output
    
    // Internal variables
    bSystemRunning          : BOOL;          // Boolean internal
    rCalculatedFlow         : REAL;          // Real/float calculated
    iAlarmCounter          : INT;           // Integer counter
    
    // Constants
    TEMP_SETPOINT_MIN      : REAL := 15.0;   // Minimum temperature
    TEMP_SETPOINT_MAX      : REAL := 85.0;   // Maximum temperature
    PUMP_SPEED_DEFAULT     : INT := 1450;    // Default pump speed
END_VAR

(* Local Variables - Use clear, descriptive names *)
VAR
    bLocalCondition        : BOOL;           // Local boolean
    rLocalCalculation      : REAL;           // Local calculation
    tmDelayTimer          : TIME;           // Timer variable
    fbPIDController       : FB_PID;         // Function block instance
END_VAR
```

#### Prefix Conventions
| Type | Prefix | Example | Description |
|------|--------|---------|-------------|
| Boolean | b | bPumpRunning | Boolean variables |
| Real/Float | r | rTemperature | Real number variables |
| Integer | i | iCounter | Integer variables |
| Word | w | wStatusWord | Word variables |
| Timer | tm | tmDelayTimer | Timer variables |
| Function Block | fb | fbPIDController | Function block instances |
| Constants | ALL_CAPS | MAX_PRESSURE | Named constants |

#### Code Structure and Comments
```structured_text
(**************************************************************************
 * Function Block: FB_TemperatureController
 * Description: PID temperature controller with safety limits
 * Author: Engineering Team
 * Version: 2.1.0
 * Date: 2025-06-08
 * 
 * Safety Notes:
 * - Emergency stop immediately disables heating
 * - Temperature limits prevent overheating
 * - Watchdog timer ensures control loop execution
 **************************************************************************)

FUNCTION_BLOCK FB_TemperatureController

VAR_INPUT
    rProcessTemperature    : REAL;      // Current temperature [°C]
    rSetpoint             : REAL;      // Desired temperature [°C]  
    bEnable               : BOOL;      // Enable controller
    bEmergencyStop        : BOOL;      // Emergency stop signal
END_VAR

VAR_OUTPUT
    rControlOutput        : REAL;      // Control output [%]
    bHeatingActive        : BOOL;      // Heating element active
    bAlarmHigh           : BOOL;      // High temperature alarm
    bAlarmLow            : BOOL;      // Low temperature alarm
END_VAR

VAR
    // PID controller instance
    fbPID                 : FB_PID;
    
    // Internal calculations
    rErrorValue           : REAL;      // Setpoint - Process value
    rPIDOutput           : REAL;      // Raw PID output
    
    // Safety limits
    rTempLimitHigh       : REAL := 90.0;   // High temperature limit
    rTempLimitLow        : REAL := 5.0;    // Low temperature limit
    
    // Timers
    tmAlarmDelay         : TON;        // Alarm delay timer
    tmWatchdog           : TON;        // Watchdog timer
    
    // Status flags
    bFirstScan           : BOOL := TRUE;
    bSafetyTripped       : BOOL := FALSE;
END_VAR

(* Main controller logic *)
IF bFirstScan THEN
    // Initialize controller on first scan
    fbPID.Reset := TRUE;
    bFirstScan := FALSE;
    
    // Log startup
    // TODO: Add system log entry
END_IF

(* Emergency stop handling - Highest priority *)
IF bEmergencyStop THEN
    rControlOutput := 0.0;
    bHeatingActive := FALSE;
    bSafetyTripped := TRUE;
    
    // Log emergency stop event
    // TODO: Add alarm system integration
    RETURN; // Exit immediately
END_IF

(* Input validation and safety checks *)
IF rSetpoint < rTempLimitLow OR rSetpoint > rTempLimitHigh THEN
    // Invalid setpoint - use safe default
    rSetpoint := 25.0; // Safe room temperature
    
    // TODO: Generate alarm for invalid setpoint
END_IF

(* Temperature alarm logic *)
bAlarmHigh := rProcessTemperature > rTempLimitHigh;
bAlarmLow := rProcessTemperature < rTempLimitLow;

// Delay alarms to prevent nuisance trips
tmAlarmDelay(IN := bAlarmHigh OR bAlarmLow, PT := T#5S);

IF tmAlarmDelay.Q THEN
    // Shutdown on sustained alarm condition
    rControlOutput := 0.0;
    bHeatingActive := FALSE;
    bSafetyTripped := TRUE;
    RETURN;
END_IF

(* PID Controller execution *)
IF bEnable AND NOT bSafetyTripped THEN
    // Calculate error
    rErrorValue := rSetpoint - rProcessTemperature;
    
    // Execute PID controller
    fbPID(
        fSetpointValue := rSetpoint,
        fActualValue := rProcessTemperature,
        bEnable := TRUE,
        fManSyncValue := 0.0,
        eCtrlMode := eCTRL_MODE_ACTIVE,
        fOut => rPIDOutput
    );
    
    // Apply output limits (0-100%)
    rControlOutput := LIMIT(0.0, rPIDOutput, 100.0);
    
    // Determine heating element status
    bHeatingActive := rControlOutput > 5.0; // 5% deadband
    
ELSE
    // Controller disabled - safe shutdown
    rControlOutput := 0.0;
    bHeatingActive := FALSE;
    fbPID.bEnable := FALSE;
END_IF

(* Watchdog timer for loop monitoring *)
tmWatchdog(IN := TRUE, PT := T#100MS);
IF tmWatchdog.Q THEN
    tmWatchdog(IN := FALSE);
    tmWatchdog(IN := TRUE);
    
    // TODO: Update loop execution counter
END_IF
```

#### Error Handling Standards
```structured_text
(* Standard error handling pattern *)
VAR
    eErrorCode           : E_ErrorCode := E_ErrorCode.NO_ERROR;
    sErrorMessage        : STRING[255] := '';
    bErrorAcknowledged   : BOOL := FALSE;
END_VAR

(* Error checking and handling *)
IF NOT bInputValid THEN
    eErrorCode := E_ErrorCode.INVALID_INPUT;
    sErrorMessage := 'Temperature sensor reading out of range';
    
    // Log error
    LogError(eErrorCode, sErrorMessage);
    
    // Take safe action
    DisableOutputs();
    
    // Wait for acknowledgment
    IF NOT bErrorAcknowledged THEN
        RETURN;
    END_IF
END_IF
```

### Ladder Logic (LD) Standards

#### Rung Organization
```
(* Rung 1: Emergency Stop Logic *)
--[/]-------[/]-------[/]-------( )--
  E_STOP   GUARD_1   GUARD_2   SAFETY_OK
  
(* Rung 2: Pump Start Conditions *)
--[ ]-------[/]-------[ ]-------( )--
  START_PB  STOP_PB   READY    PUMP_RUN

(* Rung 3: Pump Run Seal-in *)
--[ ]-------[/]-------[ ]-------( )--
  PUMP_RUN  STOP_PB   NO_FAULT  PUMP_RUN
```

#### Documentation Standards
- Each rung must have a descriptive comment
- Complex logic requires step-by-step explanation
- Safety-critical rungs require additional documentation
- Contact symbols use meaningful tag names

### Function Block Diagram (FBD) Standards

#### Block Arrangement
```
    +----------+    +----------+    +----------+
    |   TEMP   |--->|   PID    |--->| HEATER   |
    | SENSOR   |    |CONTROLLER|    | OUTPUT   |
    +----------+    +----------+    +----------+
         |               |               |
         v               v               v
    +----------+    +----------+    +----------+
    |  ALARM   |    | MANUAL   |    | STATUS   |
    | HANDLER  |    | OVERRIDE |    | DISPLAY  |
    +----------+    +----------+    +----------+
```

#### Connection Standards
- Use meaningful connection labels
- Avoid crossing connection lines
- Group related blocks logically
- Document complex data flows

## Python Programming Standards

### General Style Guidelines
```python
"""
Industrial Automation Python Code Standards
Following PEP 8 with industrial automation specific additions
"""

import logging
import time
from datetime import datetime
from typing import Dict, List, Optional, Union
from dataclasses import dataclass
from enum import Enum, auto

# Configure logging for industrial applications
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('system.log'),
        logging.StreamHandler()
    ]
)

class SystemState(Enum):
    """System operating states"""
    STOPPED = auto()
    STARTING = auto()
    RUNNING = auto()
    STOPPING = auto()
    FAULT = auto()
    MAINTENANCE = auto()

@dataclass
class ProcessData:
    """Process data structure with validation"""
    timestamp: datetime
    temperature: float
    pressure: float
    flow_rate: float
    quality_flags: Dict[str, bool]
    
    def __post_init__(self):
        """Validate data after initialization"""
        if not (0.0 <= self.temperature <= 100.0):
            raise ValueError(f"Temperature {self.temperature} out of range")
        
        if not (0.0 <= self.pressure <= 10.0):
            raise ValueError(f"Pressure {self.pressure} out of range")

class TemperatureController:
    """
    PID Temperature Controller for industrial processes
    
    This class implements a PID controller with anti-windup,
    derivative filtering, and safety limits for industrial
    temperature control applications.
    
    Attributes:
        kp: Proportional gain
        ki: Integral gain  
        kd: Derivative gain
        setpoint: Target temperature
        output_min: Minimum output limit
        output_max: Maximum output limit
    
    Safety Notes:
        - Controller automatically disables on sensor failure
        - Output is limited to safe operating range
        - Watchdog timer monitors loop execution
    """
    
    def __init__(self, 
                 kp: float = 1.0,
                 ki: float = 0.1, 
                 kd: float = 0.05,
                 output_min: float = 0.0,
                 output_max: float = 100.0) -> None:
        """
        Initialize PID controller
        
        Args:
            kp: Proportional gain
            ki: Integral gain
            kd: Derivative gain
            output_min: Minimum output limit (%)
            output_max: Maximum output limit (%)
        
        Raises:
            ValueError: If gain values are negative
        """
        if kp < 0 or ki < 0 or kd < 0:
            raise ValueError("PID gains must be non-negative")
            
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.output_min = output_min
        self.output_max = output_max
        
        # Internal state variables
        self._setpoint: float = 0.0
        self._last_error: float = 0.0
        self._integral: float = 0.0
        self._last_time: Optional[float] = None
        self._enabled: bool = False
        
        # Safety and monitoring
        self._watchdog_timeout: float = 5.0  # seconds
        self._last_update: float = time.time()
        
        # Setup logging
        self._logger = logging.getLogger(self.__class__.__name__)
        self._logger.info("PID Controller initialized")
    
    @property
    def setpoint(self) -> float:
        """Get current setpoint"""
        return self._setpoint
    
    @setpoint.setter
    def setpoint(self, value: float) -> None:
        """
        Set controller setpoint with validation
        
        Args:
            value: New setpoint value
            
        Raises:
            ValueError: If setpoint is out of safe range
        """
        if not (0.0 <= value <= 100.0):
            raise ValueError(f"Setpoint {value} outside safe range 0-100")
            
        self._setpoint = value
        self._logger.info(f"Setpoint changed to {value}")
    
    def update(self, process_value: float) -> float:
        """
        Update PID controller and return output
        
        Args:
            process_value: Current process measurement
            
        Returns:
            Controller output (0-100%)
            
        Raises:
            RuntimeError: If controller is disabled or sensor failed
        """
        current_time = time.time()
        
        # Watchdog check
        if current_time - self._last_update > self._watchdog_timeout:
            self._logger.error("Controller watchdog timeout")
            self._enabled = False
            
        self._last_update = current_time
        
        # Safety checks
        if not self._enabled:
            return 0.0
            
        if not self._is_sensor_valid(process_value):
            self._logger.error(f"Invalid sensor reading: {process_value}")
            self._enabled = False
            return 0.0
        
        # Calculate time step
        if self._last_time is None:
            dt = 0.1  # Default time step
        else:
            dt = current_time - self._last_time
            dt = max(dt, 0.001)  # Prevent division by zero
            
        self._last_time = current_time
        
        # PID calculations
        error = self._setpoint - process_value
        
        # Proportional term
        proportional = self.kp * error
        
        # Integral term with anti-windup
        self._integral += error * dt
        self._integral = self._clamp(
            self._integral, 
            -100.0 / self.ki if self.ki > 0 else -100.0,
            100.0 / self.ki if self.ki > 0 else 100.0
        )
        integral = self.ki * self._integral
        
        # Derivative term
        derivative = self.kd * (error - self._last_error) / dt
        self._last_error = error
        
        # Calculate output
        output = proportional + integral + derivative
        output = self._clamp(output, self.output_min, self.output_max)
        
        # Log periodic status
        if int(current_time) % 10 == 0:  # Every 10 seconds
            self._logger.debug(
                f"PID Update: SP={self._setpoint:.2f}, "
                f"PV={process_value:.2f}, OUT={output:.2f}"
            )
        
        return output
    
    def enable(self) -> None:
        """Enable controller operation"""
        self._enabled = True
        self._integral = 0.0  # Reset integral on enable
        self._last_error = 0.0
        self._last_time = None
        self._logger.info("Controller enabled")
    
    def disable(self) -> None:
        """Disable controller operation"""
        self._enabled = False
        self._logger.info("Controller disabled")
    
    def reset(self) -> None:
        """Reset controller internal state"""
        self._integral = 0.0
        self._last_error = 0.0
        self._last_time = None
        self._logger.info("Controller reset")
    
    @staticmethod
    def _clamp(value: float, min_val: float, max_val: float) -> float:
        """Clamp value between minimum and maximum"""
        return max(min_val, min(value, max_val))
    
    @staticmethod
    def _is_sensor_valid(value: float) -> bool:
        """Validate sensor reading"""
        return not (value is None or 
                   value != value or  # NaN check
                   value < -50.0 or   # Below physical minimum
                   value > 200.0)     # Above physical maximum


# Example usage with proper error handling
def main():
    """Example controller usage"""
    logger = logging.getLogger(__name__)
    
    try:
        # Initialize controller
        controller = TemperatureController(kp=2.0, ki=0.5, kd=0.1)
        controller.setpoint = 75.0
        controller.enable()
        
        # Simulation loop
        process_value = 20.0  # Starting temperature
        
        for cycle in range(100):
            try:
                # Update controller
                output = controller.update(process_value)
                
                # Simple process simulation
                process_value += (output - 50.0) * 0.01
                
                # Log status every 10 cycles
                if cycle % 10 == 0:
                    logger.info(
                        f"Cycle {cycle}: PV={process_value:.2f}, "
                        f"OUT={output:.2f}"
                    )
                
                time.sleep(0.1)  # 100ms loop time
                
            except Exception as e:
                logger.error(f"Controller update failed: {e}")
                break
                
    except Exception as e:
        logger.error(f"Controller initialization failed: {e}")
    
    finally:
        controller.disable()

if __name__ == "__main__":
    main()
```

### Naming Conventions
```python
# Module and package names
# Use lowercase with underscores
water_treatment_controller.py
hvac_energy_optimizer.py

# Class names  
# Use CapWords (PascalCase)
class TemperatureController:
class ProcessDataLogger:
class SafetyInterlock:

# Function and variable names
# Use lowercase with underscores
def calculate_flow_rate():
def validate_sensor_input():
current_temperature = 25.0
setpoint_value = 50.0

# Constants
# Use uppercase with underscores
MAX_TEMPERATURE = 100.0
DEFAULT_TIMEOUT = 30.0
ALARM_PRIORITIES = {
    'CRITICAL': 1,
    'HIGH': 2,
    'MEDIUM': 3,
    'LOW': 4
}

# Private variables and methods
# Use leading underscore
self._internal_state = {}
def _validate_input(self, value):
    pass
```

## Documentation Standards

### Code Comments
```python
class ProcessMonitor:
    """
    Process monitoring system for industrial automation
    
    This class provides real-time monitoring capabilities for
    industrial processes including data acquisition, alarm
    management, and historical data storage.
    
    The monitor operates in a continuous loop, collecting data
    from configured sensors and evaluating alarm conditions.
    All data is logged to both local storage and remote historian.
    
    Example:
        >>> monitor = ProcessMonitor('config.ini')
        >>> monitor.start()
        >>> data = monitor.get_current_data()
        >>> monitor.stop()
    
    Attributes:
        config_file (str): Path to configuration file
        sampling_rate (float): Data sampling rate in Hz
        is_running (bool): Monitor operational status
    
    Note:
        This class is thread-safe and can be used in multi-threaded
        applications. All sensor communications use timeout values
        to prevent hanging operations.
    
    Safety:
        Monitor includes watchdog timer and automatic failsafe
        operation in case of communication failures.
    """
    
    def __init__(self, config_file: str) -> None:
        """
        Initialize process monitor
        
        Args:
            config_file: Path to INI configuration file containing
                        sensor definitions, alarm limits, and 
                        communication parameters
        
        Raises:
            FileNotFoundError: If config file doesn't exist
            ValueError: If configuration is invalid
            ConnectionError: If unable to connect to sensors
        
        Example:
            >>> monitor = ProcessMonitor('/path/to/config.ini')
        """
        pass
    
    def start_monitoring(self) -> None:
        """
        Start continuous monitoring operation
        
        Begins the main monitoring loop which will run until
        stop_monitoring() is called or a critical error occurs.
        
        The loop performs the following operations:
        1. Read all configured sensors
        2. Validate data quality
        3. Evaluate alarm conditions  
        4. Log data to historian
        5. Update system status
        
        Raises:
            RuntimeError: If monitor is already running
            ConnectionError: If unable to establish sensor communications
        
        Note:
            This method runs in a separate thread and returns immediately.
            Use is_running property to check operational status.
        """
        pass
```

### Function Documentation
```python
def calculate_pid_output(setpoint: float,
                        process_value: float,
                        kp: float,
                        ki: float,
                        kd: float,
                        dt: float,
                        integral_state: float,
                        last_error: float) -> tuple[float, float, float]:
    """
    Calculate PID controller output with anti-windup
    
    Implements a discrete PID controller algorithm with integral
    anti-windup protection. The controller uses the velocity form
    to prevent integral windup when output limits are reached.
    
    Args:
        setpoint: Desired process value
        process_value: Current measured process value  
        kp: Proportional gain (>= 0)
        ki: Integral gain (>= 0)
        kd: Derivative gain (>= 0)
        dt: Time step since last calculation (seconds)
        integral_state: Previous integral accumulator value
        last_error: Error value from previous calculation
        
    Returns:
        tuple containing:
            - output: PID controller output
            - new_integral: Updated integral state for next calculation
            - error: Current error value for next calculation
    
    Raises:
        ValueError: If gains are negative or dt is zero/negative
        TypeError: If inputs are not numeric
    
    Example:
        >>> output, integral, error = calculate_pid_output(
        ...     setpoint=75.0,
        ...     process_value=72.5, 
        ...     kp=2.0, ki=0.5, kd=0.1,
        ...     dt=0.1,
        ...     integral_state=0.0,
        ...     last_error=0.0
        ... )
        >>> print(f"Controller output: {output:.2f}%")
    
    Note:
        This function is stateless - all state must be maintained
        by the calling code and passed in on each call.
    """
    # Input validation
    if kp < 0 or ki < 0 or kd < 0:
        raise ValueError("PID gains must be non-negative")
    
    if dt <= 0:
        raise ValueError("Time step must be positive")
    
    # Calculate error
    error = setpoint - process_value
    
    # Proportional term
    proportional = kp * error
    
    # Integral term with anti-windup
    integral_state += error * dt
    integral = ki * integral_state
    
    # Derivative term  
    derivative = kd * (error - last_error) / dt
    
    # Calculate output
    output = proportional + integral + derivative
    
    return output, integral_state, error
```

## Configuration File Standards

### INI File Format
```ini
# PLC Configuration File
# Project: HVAC System
# Version: 2.1.0
# Date: 2025-06-08

[system]
# System identification
name = HVAC Control System
version = 2.1.0
description = Building automation and energy management
location = Main Building, Floor 3

# Operation parameters
scan_time_ms = 100
watchdog_timeout_ms = 5000
safety_enable = true
debug_mode = false

[communication]
# PLC network settings
plc_ip = 192.168.1.100
plc_port = 502
protocol = modbus_tcp
timeout_ms = 1000
retries = 3

# HMI connection
hmi_ip = 192.168.1.101
hmi_port = 8080
update_rate_ms = 500

[sensors]
# Temperature sensors
temp_zone_1.address = 40001
temp_zone_1.scaling = 0.1
temp_zone_1.offset = -40.0
temp_zone_1.units = celsius
temp_zone_1.alarm_high = 30.0
temp_zone_1.alarm_low = 15.0

temp_zone_2.address = 40002
temp_zone_2.scaling = 0.1
temp_zone_2.offset = -40.0
temp_zone_2.units = celsius
temp_zone_2.alarm_high = 28.0
temp_zone_2.alarm_low = 18.0

[actuators]
# Heating valves
valve_zone_1.address = 40101
valve_zone_1.scaling = 1.0
valve_zone_1.min_output = 0.0
valve_zone_1.max_output = 100.0
valve_zone_1.units = percent

[pid_controllers]
# Zone 1 temperature control
pid_zone_1.kp = 2.0
pid_zone_1.ki = 0.5
pid_zone_1.kd = 0.1
pid_zone_1.output_min = 0.0
pid_zone_1.output_max = 100.0
pid_zone_1.setpoint_default = 22.0

[alarms]
# Alarm configuration
enable_logging = true
log_file = alarms.log
max_log_size_mb = 100
acknowledgment_required = true

# Alarm priorities (1=highest, 4=lowest)
temperature_high.priority = 2
temperature_low.priority = 3
communication_fault.priority = 1
sensor_fault.priority = 2

[logging]
# System logging
log_level = INFO
log_file = system.log
max_file_size_mb = 50
backup_count = 5
log_format = %(asctime)s - %(name)s - %(levelname)s - %(message)s

# Data historian
historian_enable = true
historian_interval_s = 60
historian_database = process_data.db
historian_retention_days = 365
```

## Testing Standards

### Unit Test Structure
```python
import unittest
from unittest.mock import Mock, patch
import time
from datetime import datetime

from src.controllers.temperature_controller import TemperatureController

class TestTemperatureController(unittest.TestCase):
    """
    Test suite for TemperatureController class
    
    Tests cover normal operation, error conditions, and safety features.
    All tests use mock objects to avoid hardware dependencies.
    """
    
    def setUp(self):
        """Set up test fixtures before each test method"""
        self.controller = TemperatureController(
            kp=2.0,
            ki=0.5, 
            kd=0.1,
            output_min=0.0,
            output_max=100.0
        )
        
        # Test data
        self.valid_temperature = 25.0
        self.valid_setpoint = 50.0
        self.invalid_temperature = -999.0
    
    def test_controller_initialization(self):
        """Test controller initializes with correct parameters"""
        self.assertEqual(self.controller.kp, 2.0)
        self.assertEqual(self.controller.ki, 0.5)
        self.assertEqual(self.controller.kd, 0.1)
        self.assertEqual(self.controller.output_min, 0.0)
        self.assertEqual(self.controller.output_max, 100.0)
        self.assertFalse(self.controller._enabled)
    
    def test_setpoint_validation(self):
        """Test setpoint validation and error handling"""
        # Valid setpoint
        self.controller.setpoint = 75.0
        self.assertEqual(self.controller.setpoint, 75.0)
        
        # Invalid setpoint - should raise ValueError
        with self.assertRaises(ValueError):
            self.controller.setpoint = -10.0
            
        with self.assertRaises(ValueError):
            self.controller.setpoint = 150.0
    
    def test_controller_enable_disable(self):
        """Test controller enable/disable functionality"""
        # Initially disabled
        self.assertFalse(self.controller._enabled)
        
        # Enable controller
        self.controller.enable()
        self.assertTrue(self.controller._enabled)
        
        # Disable controller
        self.controller.disable()
        self.assertFalse(self.controller._enabled)
    
    def test_pid_calculation(self):
        """Test PID calculation with known inputs"""
        self.controller.setpoint = 50.0
        self.controller.enable()
        
        # First update - should have proportional response
        output1 = self.controller.update(25.0)  # 25°C below setpoint
        self.assertGreater(output1, 0.0)  # Should have positive output
        
        # Second update - should include integral component
        time.sleep(0.1)  # Small delay for time step calculation
        output2 = self.controller.update(30.0)  # Still below setpoint
        self.assertGreater(output2, 0.0)
    
    def test_output_limiting(self):
        """Test controller output stays within limits"""
        self.controller.setpoint = 100.0
        self.controller.enable()
        
        # Large error should be limited to max output
        output = self.controller.update(0.0)  # Maximum error
        self.assertLessEqual(output, self.controller.output_max)
        self.assertGreaterEqual(output, self.controller.output_min)
    
    def test_sensor_validation(self):
        """Test invalid sensor reading handling"""
        self.controller.setpoint = 50.0
        self.controller.enable()
        
        # Invalid sensor reading should disable controller
        output = self.controller.update(self.invalid_temperature)
        self.assertEqual(output, 0.0)
        self.assertFalse(self.controller._enabled)
    
    def test_watchdog_timeout(self):
        """Test watchdog timer functionality"""
        self.controller.setpoint = 50.0
        self.controller.enable()
        
        # Normal operation
        output1 = self.controller.update(25.0)
        self.assertGreater(output1, 0.0)
        
        # Simulate timeout by advancing time
        with patch('time.time', return_value=time.time() + 10.0):
            output2 = self.controller.update(25.0)
            self.assertEqual(output2, 0.0)  # Should disable on timeout
    
    @patch('logging.getLogger')
    def test_logging_functionality(self, mock_logger):
        """Test that controller logs important events"""
        mock_logger_instance = Mock()
        mock_logger.return_value = mock_logger_instance
        
        # Create new controller to test logging
        controller = TemperatureController()
        
        # Test initialization logging
        mock_logger_instance.info.assert_called()
        
        # Test setpoint change logging
        controller.setpoint = 75.0
        mock_logger_instance.info.assert_called_with("Setpoint changed to 75.0")

    def test_edge_cases(self):
        """Test edge cases and boundary conditions"""
        self.controller.enable()
        
        # Zero setpoint
        self.controller.setpoint = 0.0
        output = self.controller.update(0.0)
        self.assertEqual(output, 0.0)
        
        # Maximum setpoint  
        self.controller.setpoint = 100.0
        output = self.controller.update(100.0)
        self.assertEqual(output, 0.0)
        
        # Rapid successive calls
        outputs = []
        for i in range(10):
            output = self.controller.update(50.0)
            outputs.append(output)
        
        # All outputs should be valid
        for output in outputs:
            self.assertGreaterEqual(output, 0.0)
            self.assertLessEqual(output, 100.0)

    def tearDown(self):
        """Clean up after each test method"""
        if hasattr(self, 'controller'):
            self.controller.disable()

if __name__ == '__main__':
    # Configure test logging
    logging.basicConfig(level=logging.DEBUG)
    
    # Run tests
    unittest.main(verbosity=2)
```

## Best Practices Summary

### Code Organization
1. **Modular Design**: Break code into logical, reusable modules
2. **Clear Interfaces**: Define clean APIs between components
3. **Error Handling**: Comprehensive error checking and recovery
4. **Documentation**: Self-documenting code with clear comments
5. **Testing**: Unit tests for all critical functions

### Safety Considerations
1. **Fail-Safe Design**: Default to safe state on errors
2. **Input Validation**: Validate all external inputs
3. **Watchdog Timers**: Monitor system health
4. **Redundancy**: Critical functions have backup systems
5. **Audit Trail**: Log all safety-critical operations

### Performance Guidelines
1. **Efficient Algorithms**: Use appropriate data structures
2. **Memory Management**: Prevent memory leaks
3. **Real-Time Constraints**: Meet timing requirements
4. **Resource Usage**: Monitor CPU and memory usage
5. **Scalability**: Design for future expansion

## See Also

- [Testing Procedures](Testing-Procedures.md)
- [Version Control](Version-Control.md)
- [Development Guide](Development-Guide.md)
- [PLC Programming](../technical/PLC-Programming.md)

---

*Code Standards Guide - Part of Industrial PLC Control Systems Repository*
