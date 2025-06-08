# Troubleshooting Guide

## Overview

This comprehensive troubleshooting guide provides systematic approaches to diagnosing and resolving issues across all PLC automation systems in this repository. From simple sensor faults to complex system failures, this guide helps operators and maintenance personnel quickly identify and resolve problems while maintaining safety and system integrity.

## 📚 Table of Contents

1. [Troubleshooting Methodology](#troubleshooting-methodology)
2. [Common System Issues](#common-system-issues)
3. [Hardware Troubleshooting](#hardware-troubleshooting)
4. [Software Troubleshooting](#software-troubleshooting)
5. [Communication Issues](#communication-issues)
6. [Emergency Troubleshooting](#emergency-troubleshooting)
7. [Diagnostic Tools](#diagnostic-tools)

## 🔍 Troubleshooting Methodology

### Systematic Approach Framework

#### The SAFER Method
```
S - SECURE the area and ensure safety
A - ASSESS the situation and gather information
F - FIND the root cause through logical analysis
E - EXECUTE the appropriate corrective action
R - REVIEW and verify the solution effectiveness
```

### Problem Classification Matrix

#### Severity Categories
```
CRITICAL (Red):
├── Safety system failures
├── Complete system shutdown
├── Fire/explosion hazards
├── Environmental releases
└── Personnel injury risks

Response: Immediate action, emergency protocols

HIGH (Orange):
├── Major equipment failures
├── Production stoppage
├── Quality system failures
├── Multiple system faults
└── Backup system activation

Response: Within 15 minutes, escalate if needed

MEDIUM (Yellow):
├── Single equipment malfunctions
├── Performance degradation
├── Intermittent faults
├── Sensor/instrument failures
└── Communication disruptions

Response: Within 1 hour, scheduled maintenance

LOW (Blue):
├── Minor operational issues
├── Cosmetic problems
├── Documentation discrepancies
├── Non-critical warnings
└── Information updates

Response: Next available opportunity
```

### Information Gathering Checklist

#### Initial Assessment Questions
```markdown
## Problem Definition
- [ ] What exactly is the problem? (Be specific)
- [ ] When did the problem first occur?
- [ ] What was happening when the problem started?
- [ ] Has this problem occurred before?
- [ ] What has changed recently in the system?

## System Status
- [ ] Which equipment/systems are affected?
- [ ] What alarms are currently active?
- [ ] Are safety systems functioning normally?
- [ ] What is the current operating mode?
- [ ] Are there any error codes displayed?

## Environmental Conditions
- [ ] Are environmental conditions normal? (temperature, humidity, etc.)
- [ ] Have there been any power disturbances?
- [ ] Are all utility systems operating normally?
- [ ] Has there been any recent maintenance work?
- [ ] Are there any unusual sounds, smells, or vibrations?

## Documentation Check
- [ ] Check recent maintenance logs
- [ ] Review recent alarm history
- [ ] Verify recent configuration changes
- [ ] Check for outstanding work orders
- [ ] Review operator shift logs
```

## ⚠️ Common System Issues

### Motor and Drive Problems

#### Motor Won't Start
```
Possible Causes and Solutions:

1. CONTROL SYSTEM ISSUES:
   Problem: No start signal from PLC
   Check: PLC output status, wiring continuity
   Solution: Verify PLC program logic, check I/O modules
   
2. POWER SUPPLY PROBLEMS:
   Problem: Insufficient voltage or power
   Check: Voltage levels, circuit breakers, fuses
   Solution: Reset breakers, replace fuses, check supply voltage
   
3. MECHANICAL ISSUES:
   Problem: Seized bearings or coupling
   Check: Manual rotation, bearing condition, alignment
   Solution: Lubricate, replace bearings, realign coupling
   
4. PROTECTION SYSTEM ACTIVATION:
   Problem: Overload, thermal protection tripped
   Check: Motor temperature, current draw, protection settings
   Solution: Allow cooling, check load, adjust protection
```

#### Motor Runs But Performance Poor
```pascal
// PLC diagnostic program for motor performance
FUNCTION_BLOCK FB_MotorDiagnostics

VAR_INPUT
    rMotorCurrent : REAL;        // Actual motor current
    rMotorSpeed : REAL;          // Actual motor speed
    rSpeedSetpoint : REAL;       // Commanded speed
    rVibrationLevel : REAL;      // Vibration measurement
END_VAR

VAR_OUTPUT
    bPerformanceWarning : BOOL;
    bMaintenanceRequired : BOOL;
    sDiagnosticMessage : STRING;
END_VAR

VAR_CONSTANT
    rNormalCurrentMin : REAL := 8.0;    // Minimum normal current
    rNormalCurrentMax : REAL := 12.0;   // Maximum normal current
    rSpeedTolerance : REAL := 2.0;      // Speed deviation tolerance
    rVibrationLimit : REAL := 5.0;      // Maximum vibration level
END_VAR

// Performance analysis
IF rMotorCurrent < rNormalCurrentMin THEN
    bPerformanceWarning := TRUE;
    sDiagnosticMessage := 'Low current - possible belt slippage or light load';
    
ELSIF rMotorCurrent > rNormalCurrentMax THEN
    bPerformanceWarning := TRUE;
    sDiagnosticMessage := 'High current - possible overload or bearing issues';
    
ELSIF ABS(rMotorSpeed - rSpeedSetpoint) > rSpeedTolerance THEN
    bPerformanceWarning := TRUE;
    sDiagnosticMessage := 'Speed deviation - check mechanical coupling';
    
ELSIF rVibrationLevel > rVibrationLimit THEN
    bMaintenanceRequired := TRUE;
    sDiagnosticMessage := 'High vibration - bearing or alignment issue';
    
ELSE
    bPerformanceWarning := FALSE;
    bMaintenanceRequired := FALSE;
    sDiagnosticMessage := 'Motor performance normal';
END_IF;
```

### Sensor and Instrument Faults

#### Temperature Sensor Issues
```
FAULT: Erratic temperature readings

DIAGNOSIS STEPS:
1. Check sensor wiring and connections
2. Verify power supply to transmitter
3. Test sensor resistance (RTD) or voltage (thermocouple)
4. Check for electrical interference
5. Verify calibration accuracy

COMMON SOLUTIONS:
├── Tighten loose connections
├── Shield cables from electrical noise
├── Replace damaged sensors
├── Recalibrate instruments
└── Update PLC scaling parameters
```

#### Pressure Sensor Troubleshooting
```python
# Python script for pressure sensor diagnostics
class PressureSensorDiagnostics:
    def __init__(self):
        self.sensor_specs = {
            'range_min': 0.0,      # Minimum pressure range
            'range_max': 100.0,    # Maximum pressure range
            'accuracy': 0.25,      # Accuracy percentage
            'response_time': 1.0   # Response time in seconds
        }
    
    def diagnose_sensor(self, sensor_readings, expected_pressure):
        """Diagnose pressure sensor performance"""
        
        issues = []
        
        # Check for out-of-range readings
        for reading in sensor_readings:
            if reading < self.sensor_specs['range_min'] or reading > self.sensor_specs['range_max']:
                issues.append({
                    'type': 'OUT_OF_RANGE',
                    'description': f'Reading {reading} outside sensor range',
                    'severity': 'HIGH',
                    'action': 'Check sensor wiring and power supply'
                })
        
        # Check accuracy
        if expected_pressure is not None:
            avg_reading = sum(sensor_readings) / len(sensor_readings)
            error_percent = abs(avg_reading - expected_pressure) / expected_pressure * 100
            
            if error_percent > self.sensor_specs['accuracy']:
                issues.append({
                    'type': 'ACCURACY_ERROR',
                    'description': f'Sensor accuracy error: {error_percent:.2f}%',
                    'severity': 'MEDIUM',
                    'action': 'Calibrate sensor or replace if beyond tolerance'
                })
        
        # Check for signal noise
        if len(sensor_readings) > 5:
            std_dev = self.calculate_std_deviation(sensor_readings)
            if std_dev > 1.0:  # Threshold for noise detection
                issues.append({
                    'type': 'SIGNAL_NOISE',
                    'description': f'High signal noise detected: {std_dev:.2f}',
                    'severity': 'MEDIUM',
                    'action': 'Check cable shielding and electrical interference'
                })
        
        # Check for stuck readings
        if len(set(sensor_readings)) == 1 and len(sensor_readings) > 3:
            issues.append({
                'type': 'STUCK_READING',
                'description': 'Sensor appears to be stuck at one value',
                'severity': 'HIGH',
                'action': 'Check sensor operation and replace if necessary'
            })
        
        return self.generate_diagnostic_report(issues)
    
    def calculate_std_deviation(self, readings):
        """Calculate standard deviation of readings"""
        if len(readings) < 2:
            return 0
        
        mean = sum(readings) / len(readings)
        variance = sum((x - mean) ** 2 for x in readings) / len(readings)
        return variance ** 0.5
    
    def generate_diagnostic_report(self, issues):
        """Generate diagnostic report with recommendations"""
        if not issues:
            return {
                'status': 'HEALTHY',
                'message': 'Pressure sensor operating normally',
                'recommendations': []
            }
        
        high_severity = [i for i in issues if i['severity'] == 'HIGH']
        medium_severity = [i for i in issues if i['severity'] == 'MEDIUM']
        
        if high_severity:
            status = 'CRITICAL'
            message = f'{len(high_severity)} critical issues detected'
        elif medium_severity:
            status = 'WARNING'
            message = f'{len(medium_severity)} issues require attention'
        else:
            status = 'INFO'
            message = 'Minor issues detected'
        
        return {
            'status': status,
            'message': message,
            'issues': issues,
            'recommendations': [issue['action'] for issue in issues]
        }
```

### Control Loop Problems

#### PID Control Troubleshooting
```
PROBLEM: Poor PID control performance

SYMPTOMS AND SOLUTIONS:

1. OSCILLATING CONTROL:
   Symptoms: Output swings back and forth around setpoint
   Causes: Proportional gain too high, derivative time too small
   Solutions: Reduce Kp, increase derivative time, check for noise
   
2. SLOW RESPONSE:
   Symptoms: Takes too long to reach setpoint
   Causes: Proportional gain too low, integral time too long
   Solutions: Increase Kp, reduce integral time, check process capacity
   
3. STEADY-STATE ERROR:
   Symptoms: Never quite reaches setpoint
   Causes: No integral action, integral windup, process disturbances
   Solutions: Enable integral action, add anti-windup, increase integral gain
   
4. UNSTABLE CONTROL:
   Symptoms: Continuous oscillation, system becomes unstable
   Causes: Aggressive tuning, process delay, sensor noise
   Solutions: Conservative tuning, add filtering, check loop timing
```

### Valve and Actuator Issues

#### Control Valve Problems
```
FAULT DIAGNOSIS FLOWCHART:

Valve doesn't respond to commands:
├── Check control signal (4-20mA or pneumatic)
├── Verify actuator air supply (pneumatic valves)
├── Check valve position feedback
├── Inspect for mechanical binding
└── Test positioner calibration

Valve position doesn't match command:
├── Calibrate positioner
├── Check linkage adjustment
├── Verify feedback sensor
├── Inspect for wear or damage
└── Adjust travel limits

Valve response is slow:
├── Check air supply pressure and flow
├── Inspect tubing for restrictions
├── Verify positioner response time
├── Check for temperature effects
└── Lubricate moving parts if needed
```

## 🔧 Hardware Troubleshooting

### PLC Hardware Issues

#### I/O Module Failures
```pascal
// PLC program for I/O module diagnostics
FUNCTION_BLOCK FB_IOModuleDiagnostics

VAR_INPUT
    bModulePresent : BOOL;       // Module presence detection
    wModuleStatus : WORD;        // Module status word
    bChannelFault : ARRAY[0..15] OF BOOL;  // Individual channel faults
END_VAR

VAR_OUTPUT
    bModuleHealthy : BOOL;
    sModuleStatus : STRING;
    wFaultChannels : WORD;
END_VAR

VAR
    i : INT;
    iFaultCount : INT;
END_VAR

// Module presence check
IF NOT bModulePresent THEN
    bModuleHealthy := FALSE;
    sModuleStatus := 'Module not detected - check seating and connections';
    RETURN;
END_IF;

// Status word analysis
CASE wModuleStatus OF
    16#0000:
        sModuleStatus := 'Module operating normally';
        bModuleHealthy := TRUE;
        
    16#0001:
        sModuleStatus := 'Configuration error - verify module type';
        bModuleHealthy := FALSE;
        
    16#0002:
        sModuleStatus := 'Power supply fault - check 24V supply';
        bModuleHealthy := FALSE;
        
    16#0004:
        sModuleStatus := 'Communication error - check backplane connection';
        bModuleHealthy := FALSE;
        
    16#0008:
        sModuleStatus := 'Calibration required - schedule maintenance';
        bModuleHealthy := FALSE;
        
    ELSE
        sModuleStatus := 'Unknown fault code - consult manual';
        bModuleHealthy := FALSE;
END_CASE;

// Channel fault analysis
iFaultCount := 0;
wFaultChannels := 0;

FOR i := 0 TO 15 DO
    IF bChannelFault[i] THEN
        iFaultCount := iFaultCount + 1;
        wFaultChannels := wFaultChannels OR SHL(1, i);
    END_IF;
END_FOR;

IF iFaultCount > 0 THEN
    sModuleStatus := sModuleStatus + CONCAT(' - ', INT_TO_STRING(iFaultCount));
    sModuleStatus := sModuleStatus + ' channel faults detected';
    bModuleHealthy := FALSE;
END_IF;
```

#### Communication Network Issues
```
NETWORK TROUBLESHOOTING STEPS:

1. PHYSICAL LAYER CHECK:
   ├── Verify cable connections and terminations
   ├── Check for proper cable types and lengths
   ├── Test cable continuity with multimeter
   ├── Verify network termination resistors
   └── Check for electromagnetic interference

2. DATA LINK LAYER:
   ├── Verify node addresses are unique
   ├── Check baud rate settings match
   ├── Verify communication parameters
   ├── Monitor for data collisions
   └── Check for excessive network traffic

3. APPLICATION LAYER:
   ├── Verify PLC communication settings
   ├── Check HMI tag configuration
   ├── Test individual device responses
   ├── Monitor communication statistics
   └── Check for timeout settings
```

### Power System Problems

#### UPS and Power Supply Issues
```python
# Python script for power system monitoring
class PowerSystemMonitor:
    def __init__(self):
        self.voltage_limits = {
            'nominal': 24.0,
            'min_warning': 21.6,    # 90% of nominal
            'min_critical': 19.2,   # 80% of nominal
            'max_warning': 26.4,    # 110% of nominal
            'max_critical': 28.8    # 120% of nominal
        }
        
        self.power_quality_thresholds = {
            'voltage_ripple_max': 0.5,      # 500mV ripple
            'frequency_tolerance': 0.1,      # ±0.1 Hz
            'harmonic_distortion_max': 5.0   # 5% THD
        }
    
    def analyze_power_quality(self, voltage_readings, frequency_readings):
        """Analyze power quality and identify issues"""
        
        issues = []
        
        # Voltage level analysis
        avg_voltage = sum(voltage_readings) / len(voltage_readings)
        
        if avg_voltage < self.voltage_limits['min_critical']:
            issues.append({
                'type': 'CRITICAL_UNDERVOLTAGE',
                'description': f'Voltage critically low: {avg_voltage:.1f}V',
                'action': 'Check power supply and connections immediately',
                'priority': 'CRITICAL'
            })
        elif avg_voltage < self.voltage_limits['min_warning']:
            issues.append({
                'type': 'LOW_VOLTAGE_WARNING',
                'description': f'Voltage below normal: {avg_voltage:.1f}V',
                'action': 'Monitor closely and check supply capacity',
                'priority': 'HIGH'
            })
        
        if avg_voltage > self.voltage_limits['max_critical']:
            issues.append({
                'type': 'CRITICAL_OVERVOLTAGE',
                'description': f'Voltage critically high: {avg_voltage:.1f}V',
                'action': 'Shut down equipment to prevent damage',
                'priority': 'CRITICAL'
            })
        elif avg_voltage > self.voltage_limits['max_warning']:
            issues.append({
                'type': 'HIGH_VOLTAGE_WARNING',
                'description': f'Voltage above normal: {avg_voltage:.1f}V',
                'action': 'Check voltage regulator settings',
                'priority': 'HIGH'
            })
        
        # Voltage stability analysis
        voltage_range = max(voltage_readings) - min(voltage_readings)
        if voltage_range > self.power_quality_thresholds['voltage_ripple_max']:
            issues.append({
                'type': 'VOLTAGE_INSTABILITY',
                'description': f'High voltage ripple: {voltage_range:.2f}V',
                'action': 'Check power supply filtering and load stability',
                'priority': 'MEDIUM'
            })
        
        # Frequency analysis
        if frequency_readings:
            avg_frequency = sum(frequency_readings) / len(frequency_readings)
            if abs(avg_frequency - 50.0) > self.power_quality_thresholds['frequency_tolerance']:
                issues.append({
                    'type': 'FREQUENCY_DEVIATION',
                    'description': f'Frequency deviation: {avg_frequency:.2f}Hz',
                    'action': 'Check grid connection and generator stability',
                    'priority': 'HIGH'
                })
        
        return self.generate_power_report(issues, avg_voltage, avg_frequency if frequency_readings else None)
    
    def generate_power_report(self, issues, voltage, frequency):
        """Generate comprehensive power system report"""
        
        report = {
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'system_status': 'HEALTHY' if not issues else 'ISSUES_DETECTED',
            'measurements': {
                'voltage': voltage,
                'frequency': frequency
            },
            'issues': issues,
            'recommendations': []
        }
        
        # Generate recommendations based on issues
        critical_issues = [i for i in issues if i['priority'] == 'CRITICAL']
        high_issues = [i for i in issues if i['priority'] == 'HIGH']
        
        if critical_issues:
            report['system_status'] = 'CRITICAL'
            report['recommendations'].append('Immediate shutdown recommended to prevent equipment damage')
        elif high_issues:
            report['system_status'] = 'WARNING'
            report['recommendations'].append('Schedule immediate maintenance to prevent system failure')
        
        # Add preventive recommendations
        if voltage < 23.0:
            report['recommendations'].append('Consider upgrading power supply capacity')
        
        if len(issues) > 3:
            report['recommendations'].append('Comprehensive power system audit recommended')
        
        return report
```

## 💻 Software Troubleshooting

### PLC Program Issues

#### Logic Errors and Debugging
```pascal
// PLC debugging function block
FUNCTION_BLOCK FB_ProgramDebugger

VAR_INPUT
    bEnableDebug : BOOL;
    sDebugLevel : STRING;  // 'INFO', 'WARNING', 'ERROR'
END_VAR

VAR_OUTPUT
    sDebugMessage : STRING;
    bLogMessage : BOOL;
END_VAR

VAR
    arrDebugBuffer : ARRAY[1..100] OF STRING;
    iBufferIndex : INT := 1;
    dtLastMessage : DATE_AND_TIME;
END_VAR

// Debug message logging function
FUNCTION LogDebugMessage : BOOL
VAR_INPUT
    sMessage : STRING;
    sLevel : STRING;
    sLocation : STRING;
END_VAR

VAR
    sTimestamp : STRING;
    sFormattedMessage : STRING;
END_VAR

// Create timestamp
sTimestamp := DT_TO_STRING(dtLastMessage);

// Format debug message
sFormattedMessage := CONCAT(sTimestamp, ' [');
sFormattedMessage := CONCAT(sFormattedMessage, sLevel);
sFormattedMessage := CONCAT(sFormattedMessage, '] ');
sFormattedMessage := CONCAT(sFormattedMessage, sLocation);
sFormattedMessage := CONCAT(sFormattedMessage, ': ');
sFormattedMessage := CONCAT(sFormattedMessage, sMessage);

// Store in buffer
IF iBufferIndex <= 100 THEN
    arrDebugBuffer[iBufferIndex] := sFormattedMessage;
    iBufferIndex := iBufferIndex + 1;
ELSE
    // Buffer full, wrap around
    iBufferIndex := 1;
    arrDebugBuffer[iBufferIndex] := sFormattedMessage;
END_IF;

LogDebugMessage := TRUE;
```

#### Memory and Performance Issues
```
PERFORMANCE TROUBLESHOOTING:

Slow Scan Times:
├── Check for infinite loops in program logic
├── Optimize complex mathematical calculations
├── Reduce unnecessary data movement operations
├── Implement efficient sorting and searching algorithms
└── Use appropriate data types for variables

Memory Usage Problems:
├── Monitor global variable usage
├── Check for memory leaks in function blocks
├── Optimize string operations
├── Use local variables where possible
└── Implement proper variable initialization

Communication Bottlenecks:
├── Optimize network traffic patterns
├── Implement efficient data packaging
├── Use appropriate update rates for different data types
├── Monitor network utilization statistics
└── Implement proper error handling for communication failures
```

## 🔧 Diagnostic Tools

### Built-in Diagnostic Features

#### PLC Diagnostic Capabilities
```pascal
// System diagnostics function block
FUNCTION_BLOCK FB_SystemDiagnostics

VAR_INPUT
    bRunDiagnostics : BOOL;
END_VAR

VAR_OUTPUT
    stDiagnosticResults : stDiagnosticData;
END_VAR

VAR
    stSystemInfo : stSystemInformation;
    arrModuleStatus : ARRAY[1..16] OF stModuleInfo;
    i : INT;
END_VAR

TYPE stDiagnosticData : STRUCT
    rScanTimeMin : REAL;       // Minimum scan time
    rScanTimeMax : REAL;       // Maximum scan time  
    rScanTimeAvg : REAL;       // Average scan time
    iMemoryUsed : INT;         // Memory usage percentage
    iCommErrors : INT;         // Communication error count
    bSystemHealthy : BOOL;     // Overall system health
    sHealthMessage : STRING;   // Health status message
END_STRUCT;
END_TYPE

// Collect diagnostic information
IF bRunDiagnostics THEN
    // Get system information
    GetSystemInfo(stSystemInfo);
    
    // Collect scan time statistics
    stDiagnosticResults.rScanTimeMin := stSystemInfo.rScanTimeMin;
    stDiagnosticResults.rScanTimeMax := stSystemInfo.rScanTimeMax;
    stDiagnosticResults.rScanTimeAvg := stSystemInfo.rScanTimeAvg;
    
    // Check memory usage
    stDiagnosticResults.iMemoryUsed := stSystemInfo.iMemoryUsedPercent;
    
    // Count communication errors
    stDiagnosticResults.iCommErrors := stSystemInfo.iCommunicationErrors;
    
    // Assess overall health
    IF stDiagnosticResults.rScanTimeMax > 50.0 OR
       stDiagnosticResults.iMemoryUsed > 90 OR
       stDiagnosticResults.iCommErrors > 100 THEN
        stDiagnosticResults.bSystemHealthy := FALSE;
        stDiagnosticResults.sHealthMessage := 'System performance issues detected';
    ELSE
        stDiagnosticResults.bSystemHealthy := TRUE;
        stDiagnosticResults.sHealthMessage := 'System operating normally';
    END_IF;
    
    bRunDiagnostics := FALSE;  // Reset trigger
END_IF;
```

### External Diagnostic Tools

#### Network Analysis Tools
```python
# Python script for network diagnostic analysis
import ping3
import socket
import time
from dataclasses import dataclass
from typing import List, Dict

@dataclass
class NetworkNode:
    name: str
    ip_address: str
    device_type: str
    expected_response_time: float

class NetworkDiagnostics:
    def __init__(self):
        self.nodes = []
        self.test_results = []
    
    def add_network_node(self, name: str, ip: str, device_type: str, expected_ms: float):
        """Add a network node for testing"""
        self.nodes.append(NetworkNode(name, ip, device_type, expected_ms))
    
    def ping_test(self, node: NetworkNode, count: int = 5) -> Dict:
        """Perform ping test on network node"""
        
        results = {
            'node_name': node.name,
            'ip_address': node.ip_address,
            'device_type': node.device_type,
            'packets_sent': count,
            'packets_received': 0,
            'packet_loss_percent': 0,
            'response_times': [],
            'avg_response_time': 0,
            'status': 'UNKNOWN'
        }
        
        successful_pings = 0
        response_times = []
        
        for i in range(count):
            try:
                response_time = ping3.ping(node.ip_address, timeout=5)
                if response_time is not None:
                    successful_pings += 1
                    response_times.append(response_time * 1000)  # Convert to ms
                    time.sleep(0.1)  # Small delay between pings
            except Exception as e:
                print(f"Error pinging {node.ip_address}: {e}")
        
        results['packets_received'] = successful_pings
        results['packet_loss_percent'] = ((count - successful_pings) / count) * 100
        results['response_times'] = response_times
        
        if response_times:
            results['avg_response_time'] = sum(response_times) / len(response_times)
        
        # Determine status
        if successful_pings == 0:
            results['status'] = 'OFFLINE'
        elif results['packet_loss_percent'] > 20:
            results['status'] = 'POOR'
        elif results['avg_response_time'] > node.expected_response_time * 2:
            results['status'] = 'SLOW'
        else:
            results['status'] = 'HEALTHY'
        
        return results
    
    def port_scan(self, ip: str, ports: List[int]) -> Dict:
        """Scan specific ports on a device"""
        
        scan_results = {
            'ip_address': ip,
            'scanned_ports': ports,
            'open_ports': [],
            'closed_ports': [],
            'services_detected': {}
        }
        
        for port in ports:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(3)
                result = sock.connect_ex((ip, port))
                
                if result == 0:
                    scan_results['open_ports'].append(port)
                    # Try to identify service
                    service = self.identify_service(port)
                    if service:
                        scan_results['services_detected'][port] = service
                else:
                    scan_results['closed_ports'].append(port)
                
                sock.close()
                
            except Exception as e:
                print(f"Error scanning port {port} on {ip}: {e}")
                scan_results['closed_ports'].append(port)
        
        return scan_results
    
    def identify_service(self, port: int) -> str:
        """Identify common services by port number"""
        common_ports = {
            21: 'FTP',
            22: 'SSH',
            23: 'Telnet',
            25: 'SMTP',
            53: 'DNS',
            80: 'HTTP',
            110: 'POP3',
            143: 'IMAP',
            443: 'HTTPS',
            502: 'Modbus TCP',
            2404: 'IEC 61850',
            44818: 'EtherNet/IP'
        }
        
        return common_ports.get(port, 'Unknown')
    
    def comprehensive_network_test(self) -> Dict:
        """Run comprehensive network diagnostics"""
        
        test_summary = {
            'test_timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'total_nodes': len(self.nodes),
            'healthy_nodes': 0,
            'problematic_nodes': 0,
            'offline_nodes': 0,
            'node_results': [],
            'recommendations': []
        }
        
        # Test each node
        for node in self.nodes:
            ping_result = self.ping_test(node)
            test_summary['node_results'].append(ping_result)
            
            if ping_result['status'] == 'HEALTHY':
                test_summary['healthy_nodes'] += 1
            elif ping_result['status'] == 'OFFLINE':
                test_summary['offline_nodes'] += 1
            else:
                test_summary['problematic_nodes'] += 1
        
        # Generate recommendations
        if test_summary['offline_nodes'] > 0:
            test_summary['recommendations'].append(
                f"{test_summary['offline_nodes']} nodes are offline - check physical connections"
            )
        
        if test_summary['problematic_nodes'] > 0:
            test_summary['recommendations'].append(
                f"{test_summary['problematic_nodes']} nodes have performance issues - investigate network congestion"
            )
        
        overall_health = (test_summary['healthy_nodes'] / test_summary['total_nodes']) * 100
        if overall_health < 90:
            test_summary['recommendations'].append(
                "Network health below 90% - comprehensive network audit recommended"
            )
        
        return test_summary

# Usage example
if __name__ == "__main__":
    diagnostics = NetworkDiagnostics()
    
    # Add network nodes for testing
    diagnostics.add_network_node("Main PLC", "192.168.1.100", "PLC", 10.0)
    diagnostics.add_network_node("HMI Station", "192.168.1.101", "HMI", 15.0)
    diagnostics.add_network_node("I/O Module 1", "192.168.1.110", "Remote I/O", 20.0)
    diagnostics.add_network_node("Drive 1", "192.168.1.120", "VFD", 25.0)
    
    # Run comprehensive test
    results = diagnostics.comprehensive_network_test()
    
    # Display results
    print(f"Network Test Results - {results['test_timestamp']}")
    print(f"Total Nodes: {results['total_nodes']}")
    print(f"Healthy: {results['healthy_nodes']}")
    print(f"Problems: {results['problematic_nodes']}")
    print(f"Offline: {results['offline_nodes']}")
    
    if results['recommendations']:
        print("\nRecommendations:")
        for rec in results['recommendations']:
            print(f"- {rec}")
```

## 📋 Emergency Troubleshooting

### Critical System Failures

#### Complete System Shutdown
```
EMERGENCY RESPONSE PROCEDURE:

IMMEDIATE ACTIONS (First 5 minutes):
1. Ensure personnel safety - evacuate if necessary
2. Check emergency stop status - verify activation
3. Assess for fire, gas, or environmental hazards
4. Contact emergency services if required
5. Notify plant management and technical support

INITIAL ASSESSMENT (5-15 minutes):
1. Check main power supply and distribution
2. Verify PLC power and status indicators
3. Check for obvious physical damage
4. Review alarm history before failure
5. Document failure circumstances

DIAGNOSTIC STEPS (15+ minutes):
1. Test communication to all devices
2. Check individual system components
3. Review recent changes or maintenance
4. Isolate failed components systematically
5. Plan recovery strategy based on findings
```

#### Safety System Failures
```pascal
// Emergency safety system diagnostics
FUNCTION_BLOCK FB_SafetySystemCheck

VAR_INPUT
    bRunEmergencyCheck : BOOL;
END_VAR

VAR_OUTPUT
    bSafetySystemOK : BOOL;
    sSafetyStatus : STRING;
    wFailedSafetySystems : WORD;
END_VAR

VAR
    bEmergencyStopOK : BOOL;
    bSafetyRelaysOK : BOOL;
    bSafetyPLCOK : BOOL;
    bLightCurtainsOK : BOOL;
    bPressureSwitchesOK : BOOL;
END_VAR

// Check all safety systems
IF bRunEmergencyCheck THEN
    
    // Emergency stop circuit test
    bEmergencyStopOK := TestEmergencyStopCircuit();
    
    // Safety relay status
    bSafetyRelaysOK := TestSafetyRelays();
    
    // Safety PLC communication
    bSafetyPLCOK := TestSafetyPLCComm();
    
    // Light curtain functionality
    bLightCurtainsOK := TestLightCurtains();
    
    // Pressure switch status
    bPressureSwitchesOK := TestPressureSwitches();
    
    // Compile results
    wFailedSafetySystems := 0;
    
    IF NOT bEmergencyStopOK THEN
        wFailedSafetySystems := wFailedSafetySystems OR 16#0001;
    END_IF;
    
    IF NOT bSafetyRelaysOK THEN
        wFailedSafetySystems := wFailedSafetySystems OR 16#0002;
    END_IF;
    
    IF NOT bSafetyPLCOK THEN
        wFailedSafetySystems := wFailedSafetySystems OR 16#0004;
    END_IF;
    
    IF NOT bLightCurtainsOK THEN
        wFailedSafetySystems := wFailedSafetySystems OR 16#0008;
    END_IF;
    
    IF NOT bPressureSwitchesOK THEN
        wFailedSafetySystems := wFailedSafetySystems OR 16#0010;
    END_IF;
    
    // Overall assessment
    bSafetySystemOK := (wFailedSafetySystems = 0);
    
    IF bSafetySystemOK THEN
        sSafetyStatus := 'All safety systems operational';
    ELSE
        sSafetyStatus := 'SAFETY SYSTEM FAILURE - DO NOT RESTART';
    END_IF;
    
    bRunEmergencyCheck := FALSE;
END_IF;
```

### Recovery Procedures

#### System Recovery Checklist
```markdown
# System Recovery Procedure

## Phase 1: Safety Verification (Critical)
- [ ] All personnel accounted for and safe
- [ ] Emergency stop systems functional
- [ ] No fire, gas, or environmental hazards
- [ ] Safety systems tested and operational
- [ ] Area secured for restart operations

## Phase 2: Damage Assessment
- [ ] Visual inspection of all equipment completed
- [ ] Electrical systems checked for damage
- [ ] Mechanical systems inspected
- [ ] Instrumentation verified functional
- [ ] Control systems communication tested

## Phase 3: Root Cause Analysis
- [ ] Alarm history reviewed and analyzed
- [ ] Recent changes documented and evaluated
- [ ] Environmental conditions assessed
- [ ] Equipment maintenance history reviewed
- [ ] Failure mode identified and documented

## Phase 4: Repair and Restoration
- [ ] Damaged components identified and replaced
- [ ] System integrity tests completed
- [ ] Calibration verification performed
- [ ] Software/configuration restored if needed
- [ ] Documentation updated with changes

## Phase 5: Restart Authorization
- [ ] Engineering approval for restart
- [ ] Safety coordinator sign-off
- [ ] Operations management approval
- [ ] All test procedures completed successfully
- [ ] Restart procedure reviewed with operators

## Phase 6: Monitored Restart
- [ ] Gradual system startup with close monitoring
- [ ] All parameters within normal ranges
- [ ] No abnormal conditions observed
- [ ] Full operational capability confirmed
- [ ] Incident report completed and filed
```

## 🔗 Related Resources

### Wiki Navigation
- **[Operating Procedures](Operating-Procedures.md)** - Standard operating procedures
- **[Maintenance Guide](Maintenance-Guide.md)** - Preventive maintenance procedures
- **[Safety Procedures](Safety-Procedures.md)** - Safety protocols and emergency response
- **[PLC Programming](../technical/PLC-Programming.md)** - Technical programming details
- **[System Architecture](../technical/System-Architecture.md)** - System design and integration

### External Resources
- **Manufacturer Technical Support**: Contact information for PLC vendors
- **Industry Standards**: IEC 61131, ISA standards for troubleshooting
- **Online Forums**: Automation communities and support groups
- **Training Resources**: Troubleshooting courses and certifications

---

*This troubleshooting guide is part of the Industrial PLC Control Systems Repository wiki system, providing comprehensive diagnostic and repair procedures for maintaining optimal system performance and safety.*
