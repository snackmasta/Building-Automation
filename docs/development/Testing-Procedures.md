# Testing Procedures Guide

## Overview

This comprehensive guide outlines testing methodologies, procedures, and best practices for all PLC projects in the repository. Our testing approach ensures system reliability, safety, and performance across development, commissioning, and operational phases.

## Testing Philosophy

### Quality Assurance Principles
- **Test-Driven Development**: Write tests before implementation
- **Continuous Testing**: Automated testing throughout development
- **Risk-Based Testing**: Focus on critical system functions
- **Traceability**: Link tests to requirements and specifications
- **Documentation**: Comprehensive test records and reports

### Testing Pyramid
```
┌─────────────────────────────────────┐
│         End-to-End Tests            │ ← Few, expensive, slow
├─────────────────────────────────────┤
│         Integration Tests           │ ← Some, moderate cost
├─────────────────────────────────────┤
│            Unit Tests               │ ← Many, cheap, fast
└─────────────────────────────────────┘
```

## Testing Categories

### 1. Unit Testing

#### PLC Function Block Testing
```structured_text
(* Test function block for PID controller *)
FUNCTION_BLOCK FB_PID_Test
VAR
    pid_controller : FB_PID;
    test_setpoint : REAL := 50.0;
    test_process_value : REAL := 45.0;
    test_output : REAL;
    test_passed : BOOL;
END_VAR

(* Test execution *)
pid_controller(
    setpoint := test_setpoint,
    process_value := test_process_value,
    output => test_output
);

(* Assertions *)
test_passed := (test_output > 0.0) AND (test_output <= 100.0);
```

#### Simulation Unit Tests
```python
import unittest
import numpy as np
from simulation.hvac_model import HVACZone

class TestHVACZone(unittest.TestCase):
    def setUp(self):
        self.zone = HVACZone(
            volume=1000,  # m³
            initial_temperature=20.0  # °C
        )
    
    def test_temperature_response(self):
        """Test zone temperature response to heating"""
        # Apply heating for 1 hour
        for _ in range(3600):
            self.zone.update(heating_input=5000)  # 5kW
        
        # Temperature should increase
        self.assertGreater(self.zone.temperature, 20.0)
        self.assertLess(self.zone.temperature, 30.0)  # Reasonable limit
    
    def test_energy_balance(self):
        """Verify energy conservation"""
        initial_energy = self.zone.thermal_energy
        heat_input = 1000  # 1kW for 1 second
        
        self.zone.update(heating_input=heat_input)
        
        expected_energy = initial_energy + heat_input
        self.assertAlmostEqual(
            self.zone.thermal_energy, 
            expected_energy, 
            delta=0.1
        )

if __name__ == '__main__':
    unittest.main()
```

### 2. Integration Testing

#### Modbus Communication Testing
```python
class TestModbusCommunication(unittest.TestCase):
    def setUp(self):
        self.plc_client = ModbusClient('192.168.1.100', 502)
        self.plc_client.connect()
    
    def test_read_holding_registers(self):
        """Test reading PLC holding registers"""
        result = self.plc_client.read_holding_registers(0, 10)
        self.assertIsNotNone(result)
        self.assertEqual(len(result.registers), 10)
    
    def test_write_read_cycle(self):
        """Test write-then-read consistency"""
        test_values = [1234, 5678, 9012]
        
        # Write test values
        self.plc_client.write_multiple_registers(100, test_values)
        
        # Read back values
        result = self.plc_client.read_holding_registers(100, 3)
        
        # Verify consistency
        self.assertEqual(result.registers, test_values)
    
    def tearDown(self):
        self.plc_client.close()
```

#### HMI-PLC Integration
```python
class TestHMIIntegration(unittest.TestCase):
    def setUp(self):
        self.hmi = HMIInterface()
        self.plc = PLCInterface()
        
    def test_alarm_propagation(self):
        """Test alarm from PLC to HMI"""
        # Trigger alarm in PLC
        self.plc.set_alarm('HIGH_TEMPERATURE', True)
        
        # Wait for propagation
        time.sleep(1)
        
        # Check HMI alarm status
        alarms = self.hmi.get_active_alarms()
        self.assertIn('HIGH_TEMPERATURE', alarms)
    
    def test_setpoint_control(self):
        """Test setpoint change from HMI to PLC"""
        new_setpoint = 75.5
        
        # Change setpoint via HMI
        self.hmi.set_temperature_setpoint(new_setpoint)
        
        # Verify PLC received the change
        plc_setpoint = self.plc.get_temperature_setpoint()
        self.assertAlmostEqual(plc_setpoint, new_setpoint, places=1)
```

### 3. System Testing

#### End-to-End Process Testing
```python
class TestWaterTreatmentProcess(unittest.TestCase):
    def setUp(self):
        self.system = WaterTreatmentSystem()
        self.system.initialize()
    
    def test_complete_treatment_cycle(self):
        """Test full water treatment process"""
        # Set up initial conditions
        self.system.raw_water_tank.level = 90.0  # %
        self.system.raw_water_quality.tds = 500   # ppm
        
        # Start treatment process
        self.system.start_treatment()
        
        # Run for simulated time
        for minute in range(60):  # 1 hour process
            self.system.update()
            time.sleep(0.1)  # 100ms real-time
            
            # Monitor progress
            if minute % 10 == 0:
                self.log_system_status()
        
        # Verify final water quality
        final_quality = self.system.treated_water_quality
        self.assertLess(final_quality.tds, 50)    # <50 ppm TDS
        self.assertGreater(final_quality.ph, 6.5) # pH > 6.5
        self.assertLess(final_quality.ph, 8.5)    # pH < 8.5
    
    def log_system_status(self):
        """Log system status for analysis"""
        status = {
            'timestamp': datetime.now(),
            'raw_water_level': self.system.raw_water_tank.level,
            'treated_water_level': self.system.treated_water_tank.level,
            'ro_pressure': self.system.ro_system.pressure,
            'permeate_flow': self.system.ro_system.permeate_flow,
            'recovery_rate': self.system.ro_system.recovery_rate
        }
        print(f"System Status: {status}")
```

### 4. Performance Testing

#### Control Loop Performance
```python
class TestControlPerformance(unittest.TestCase):
    def test_pid_response_time(self):
        """Test PID controller response characteristics"""
        controller = PIDController(kp=1.0, ki=0.1, kd=0.05)
        process = FirstOrderProcess(gain=1.5, time_constant=60)
        
        # Step input test
        setpoint = 50.0
        process_value = 30.0
        responses = []
        
        for t in range(600):  # 10 minutes
            output = controller.calculate(setpoint, process_value)
            process_value = process.update(output)
            responses.append(process_value)
        
        # Analyze response characteristics
        settling_time = self.calculate_settling_time(responses, setpoint)
        overshoot = self.calculate_overshoot(responses, setpoint)
        steady_state_error = abs(responses[-1] - setpoint)
        
        # Performance criteria
        self.assertLess(settling_time, 300)      # <5 minutes
        self.assertLess(overshoot, 10)           # <10% overshoot
        self.assertLess(steady_state_error, 1.0) # <1.0 unit error
    
    def calculate_settling_time(self, response, setpoint, tolerance=0.02):
        """Calculate 2% settling time"""
        tolerance_band = setpoint * tolerance
        for i in range(len(response)-50, 0, -1):
            if abs(response[i] - setpoint) > tolerance_band:
                return i + 50
        return 0
    
    def calculate_overshoot(self, response, setpoint):
        """Calculate maximum overshoot percentage"""
        max_value = max(response)
        return ((max_value - setpoint) / setpoint) * 100
```

#### Communication Performance
```python
class TestCommunicationPerformance(unittest.TestCase):
    def test_modbus_latency(self):
        """Test Modbus communication latency"""
        client = ModbusClient('192.168.1.100', 502)
        client.connect()
        
        latencies = []
        for _ in range(100):
            start_time = time.perf_counter()
            result = client.read_holding_registers(0, 1)
            end_time = time.perf_counter()
            
            if result:
                latency = (end_time - start_time) * 1000  # ms
                latencies.append(latency)
        
        # Performance metrics
        avg_latency = sum(latencies) / len(latencies)
        max_latency = max(latencies)
        min_latency = min(latencies)
        
        # Requirements
        self.assertLess(avg_latency, 50)   # <50ms average
        self.assertLess(max_latency, 100)  # <100ms maximum
        
        client.close()
    
    def test_data_throughput(self):
        """Test data acquisition throughput"""
        data_collector = DataCollector()
        
        start_time = time.time()
        sample_count = 0
        duration = 60  # 1 minute test
        
        while time.time() - start_time < duration:
            data = data_collector.collect_all_tags()
            if data:
                sample_count += len(data)
            time.sleep(0.1)  # 10 Hz sampling
        
        # Calculate throughput
        throughput = sample_count / duration  # samples/second
        
        # Requirement: >500 samples/second
        self.assertGreater(throughput, 500)
```

### 5. Safety Testing

#### Emergency Stop Testing
```python
class TestSafetyFunctions(unittest.TestCase):
    def test_emergency_stop_response(self):
        """Test emergency stop system response"""
        system = HVACSystem()
        system.start()
        
        # Verify normal operation
        self.assertTrue(system.is_running())
        
        # Trigger emergency stop
        system.emergency_stop()
        
        # Verify immediate shutdown
        self.assertFalse(system.is_running())
        
        # Check all motors stopped
        for motor in system.motors:
            self.assertFalse(motor.is_running)
        
        # Check all valves closed
        for valve in system.safety_valves:
            self.assertEqual(valve.position, 0)  # Fully closed
    
    def test_interlock_logic(self):
        """Test safety interlock logic"""
        system = WaterTreatmentSystem()
        
        # Test low level interlock
        system.raw_water_tank.level = 5.0  # Below minimum
        system.start_ro_pump()
        
        # Pump should not start due to low level
        self.assertFalse(system.ro_pump.is_running)
        
        # Test high pressure interlock
        system.raw_water_tank.level = 80.0  # Adequate level
        system.ro_system.pressure = 85.0    # Above maximum
        system.start_ro_pump()
        
        # Pump should not start due to high pressure
        self.assertFalse(system.ro_pump.is_running)
```

## Automated Testing Framework

### Test Environment Setup
```yaml
# test_config.yaml
test_environment:
  plc_simulator:
    enabled: true
    ip_address: "127.0.0.1"
    port: 502
    
  process_simulator:
    enabled: true
    real_time_factor: 10.0  # 10x faster than real-time
    
  hmi_simulator:
    enabled: true
    headless: true
    
  data_logging:
    enabled: true
    log_level: "DEBUG"
    output_directory: "./test_logs"
```

### Continuous Integration Pipeline
```yaml
# .github/workflows/test.yml
name: PLC System Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.8'
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install -r test-requirements.txt
    
    - name: Start test environment
      run: |
        docker-compose -f docker-compose.test.yml up -d
        sleep 30  # Wait for services to start
    
    - name: Run unit tests
      run: |
        python -m pytest tests/unit/ -v --cov=src/
    
    - name: Run integration tests
      run: |
        python -m pytest tests/integration/ -v
    
    - name: Run system tests
      run: |
        python -m pytest tests/system/ -v --timeout=300
    
    - name: Generate test report
      run: |
        python scripts/generate_test_report.py
    
    - name: Upload test results
      uses: actions/upload-artifact@v2
      with:
        name: test-results
        path: test-results/
```

### Test Data Management
```python
# test_data_generator.py
class TestDataGenerator:
    def generate_sensor_data(self, duration_minutes=60, noise_level=0.1):
        """Generate realistic sensor data for testing"""
        timestamps = []
        values = []
        
        # Base signal with trend and noise
        for minute in range(duration_minutes):
            timestamp = datetime.now() + timedelta(minutes=minute)
            base_value = 50 + 10 * sin(2 * pi * minute / 30)  # 30-min cycle
            noise = random.gauss(0, noise_level)
            value = base_value + noise
            
            timestamps.append(timestamp)
            values.append(value)
        
        return timestamps, values
    
    def generate_alarm_sequence(self):
        """Generate test alarm sequence"""
        alarms = [
            {'time': 0, 'tag': 'TEMP_HIGH', 'state': 'ACTIVE'},
            {'time': 30, 'tag': 'TEMP_HIGH', 'state': 'ACK'},
            {'time': 60, 'tag': 'TEMP_HIGH', 'state': 'CLEAR'},
            {'time': 90, 'tag': 'LEVEL_LOW', 'state': 'ACTIVE'},
        ]
        return alarms
```

## Test Documentation

### Test Case Specification
```markdown
# Test Case: TC_001_Temperature_Control

## Objective
Verify that the temperature control loop maintains setpoint within ±1°C

## Prerequisites
- System initialized and running
- Temperature sensor calibrated
- Heating/cooling actuators functional

## Test Steps
1. Set temperature setpoint to 25°C
2. Monitor temperature for 30 minutes
3. Record temperature every 1 minute
4. Calculate average deviation from setpoint

## Expected Results
- Temperature stays within 24-26°C range
- Average deviation < 0.5°C
- No control oscillation (>0.1 Hz)

## Pass/Fail Criteria
- Pass: All expected results met
- Fail: Any expected result not met

## Test Data
| Time | Temperature | Setpoint | Deviation |
|------|-------------|----------|-----------|
| 0:00 | 24.8       | 25.0     | -0.2      |
| 0:01 | 25.1       | 25.0     | +0.1      |
| ...  | ...        | ...      | ...       |
```

### Test Report Template
```python
# test_report_generator.py
class TestReportGenerator:
    def generate_report(self, test_results):
        """Generate comprehensive test report"""
        report = {
            'summary': {
                'total_tests': len(test_results),
                'passed': sum(1 for r in test_results if r.passed),
                'failed': sum(1 for r in test_results if not r.passed),
                'success_rate': 0.0
            },
            'categories': {
                'unit_tests': [],
                'integration_tests': [],
                'system_tests': [],
                'performance_tests': []
            },
            'detailed_results': test_results,
            'recommendations': []
        }
        
        # Calculate success rate
        if report['summary']['total_tests'] > 0:
            report['summary']['success_rate'] = (
                report['summary']['passed'] / 
                report['summary']['total_tests'] * 100
            )
        
        return report
```

## Best Practices

### Test Design Guidelines
1. **Isolation**: Each test should be independent
2. **Repeatability**: Tests should produce consistent results
3. **Maintainability**: Tests should be easy to update
4. **Coverage**: Aim for >90% code coverage
5. **Documentation**: Clear test objectives and procedures

### Test Environment Management
1. **Version Control**: Track test code and data
2. **Environment Reset**: Clean state between tests
3. **Data Management**: Organize test data and results
4. **Resource Management**: Efficient use of test hardware
5. **Parallel Execution**: Run tests concurrently when possible

### Common Pitfalls
1. **Timing Issues**: Account for system response delays
2. **State Dependencies**: Ensure proper test sequencing
3. **Resource Conflicts**: Avoid hardware contention
4. **Data Corruption**: Validate test data integrity
5. **False Positives**: Verify test assertions are meaningful

## See Also

- [Development Guide](Development-Guide.md)
- [Code Standards](Code-Standards.md)
- [Version Control](Version-Control.md)
- [System Architecture](../technical/System-Architecture.md)
- [Safety Procedures](../operations/Safety-Procedures.md)

---

*Testing Procedures Guide - Part of Industrial PLC Control Systems Repository*
