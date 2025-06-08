# Troubleshooting Guide

## HVAC Control System Troubleshooting Guide

This comprehensive troubleshooting guide provides systematic approaches to diagnosing and resolving common issues with the HVAC Control System.

---

## Table of Contents

1. [General Troubleshooting Approach](#general-troubleshooting-approach)
2. [System Communication Issues](#system-communication-issues)
3. [Temperature Control Problems](#temperature-control-problems)
4. [Equipment Malfunctions](#equipment-malfunctions)
5. [Air Quality Issues](#air-quality-issues)
6. [Energy System Problems](#energy-system-problems)
7. [HMI and Software Issues](#hmi-and-software-issues)
8. [Sensor and Actuator Problems](#sensor-and-actuator-problems)
9. [Alarm Troubleshooting](#alarm-troubleshooting)
10. [Emergency Situations](#emergency-situations)

---

## General Troubleshooting Approach

### Systematic Diagnosis Method

#### Step 1: Information Gathering
1. **Document the Problem**:
   - What exactly is wrong?
   - When did it start?
   - What changed recently?
   - Is it intermittent or constant?

2. **Check System Status**:
   - Review current alarms
   - Check system logs
   - Verify communication status
   - Note any related issues

3. **Gather Evidence**:
   - Take screenshots of errors
   - Record current readings
   - Note environmental conditions
   - Check recent maintenance

#### Step 2: Initial Assessment
1. **Safety Check**:
   - Ensure safe working conditions
   - Check for immediate hazards
   - Verify emergency systems operational
   - Consider occupant safety

2. **Scope Assessment**:
   - Is it system-wide or localized?
   - Which components are affected?
   - What systems are still working?
   - Priority level determination

#### Step 3: Systematic Testing
1. **Start with Basics**:
   - Power supply verification
   - Communication links
   - Basic sensor readings
   - Manual operation test

2. **Work from General to Specific**:
   - System level → Subsystem → Component
   - Check dependencies first
   - Test one variable at a time
   - Document each test result

---

## System Communication Issues

### PLC Communication Failure

#### Symptoms
- "PLC Not Responding" alarms
- Data not updating on HMI
- System status shows offline
- Communication timeout errors

#### Troubleshooting Steps

**Level 1: Basic Connectivity**
1. **Check Physical Connection**:
   ```cmd
   ping 192.168.1.100
   ```
   - ✅ Success: Network path is good
   - ❌ Failure: Check network cables/switches

2. **Verify PLC Status**:
   - Check PLC power indicators
   - Verify CPU status lights
   - Check Ethernet module status
   - Look for fault indicators

3. **Test Network Interface**:
   ```cmd
   ipconfig /all
   netstat -an | findstr :44818
   ```

**Level 2: Protocol Issues**
1. **Check Configuration**:
   - Verify IP address in config file
   - Check port number (44818 for Ethernet/IP)
   - Verify protocol settings
   - Check timeout values

2. **Communication Settings**:
   ```ini
   [PLC]
   ip_address = 192.168.1.100
   port = 44818
   timeout = 5
   protocol = ethernet_ip
   ```

**Level 3: Advanced Diagnostics**
1. **Network Analysis**:
   - Use Wireshark to capture packets
   - Check for network collisions
   - Verify switch configuration
   - Test with different cables

2. **PLC Programming**:
   - Check PLC communication tags
   - Verify Ethernet configuration
   - Test with PLC programming software
   - Check for communication conflicts

#### Resolution Actions

| Problem | Solution |
|---------|----------|
| Network cable disconnected | Reconnect and verify link lights |
| Wrong IP address | Update config file with correct IP |
| PLC in PROGRAM mode | Switch PLC to RUN mode |
| Network switch failure | Replace switch or use direct connection |
| Firewall blocking | Configure firewall exception |

### HMI Connection Issues

#### Symptoms
- HMI displays "Disconnected"
- Data fields show stale values
- Control commands not working
- Error messages on screen

#### Troubleshooting Steps

1. **Check HMI Application**:
   - Restart HMI software
   - Check log files for errors
   - Verify configuration files
   - Test with backup HMI

2. **Verify Communication Path**:
   - HMI → Network → PLC
   - Test each link independently
   - Check intermediate devices
   - Verify network topology

---

## Temperature Control Problems

### Zone Not Maintaining Setpoint

#### Symptoms
- Temperature consistently above/below setpoint
- Large temperature swings
- Slow response to setpoint changes
- Comfort complaints from occupants

#### Diagnostic Procedure

**Step 1: Verify Control Loop**
1. **Check Current Conditions**:
   - Current temperature reading
   - Setpoint value
   - Control output percentage
   - Damper position feedback

2. **Control Logic Verification**:
   ```
   If temp < setpoint → heating output should increase
   If temp > setpoint → cooling output should increase
   Check: Is output responding correctly?
   ```

**Step 2: Sensor Verification**
1. **Temperature Sensor Check**:
   - Compare with portable thermometer
   - Check sensor mounting location
   - Verify wiring connections
   - Test sensor with multimeter

2. **Calibration Check**:
   ```
   Acceptable tolerance: ±0.5°C (±1°F)
   If error > tolerance → recalibrate or replace
   ```

**Step 3: Actuator Testing**
1. **Damper Operation**:
   - Manual override test
   - Full stroke operation
   - Position feedback accuracy
   - Response time measurement

2. **Control Signal Verification**:
   - Measure output signal (0-10V or 4-20mA)
   - Check signal at actuator terminals
   - Verify control signal matches command

#### Common Solutions

| Symptom | Likely Cause | Solution |
|---------|--------------|----------|
| Slow response | Poor airflow | Check ductwork, adjust dampers |
| Overshooting setpoint | Aggressive control tuning | Adjust PID parameters |
| Temperature offset | Sensor calibration drift | Recalibrate or replace sensor |
| No response to commands | Actuator failure | Test/replace actuator |
| Erratic control | Sensor location issue | Relocate sensor to representative area |

### Multiple Zones Affected

#### System-Wide Temperature Issues

**Symptoms**:
- All zones running hot/cold
- Simultaneous control problems
- Supply air temperature issues

**Investigation Steps**:
1. **Check Central Equipment**:
   - Air handler operation
   - Supply air temperature
   - Return air temperature
   - Mixed air temperature

2. **Environmental Factors**:
   - Outdoor air temperature
   - Solar load changes
   - Occupancy levels
   - Internal heat sources

---

## Equipment Malfunctions

### Air Handling Unit Problems

#### AHU Not Starting

**Troubleshooting Checklist**:
1. **Power Supply**:
   - [ ] Main disconnect on
   - [ ] Control power energized  
   - [ ] Motor overloads reset
   - [ ] VFD status normal

2. **Safety Interlocks**:
   - [ ] Emergency stops reset
   - [ ] Fire alarm not active
   - [ ] Smoke detector normal
   - [ ] High temperature limits normal

3. **Control Signals**:
   - [ ] Start command present
   - [ ] Damper end switches made
   - [ ] Pressure switches normal
   - [ ] VFD ready signal

**Step-by-Step Diagnosis**:
```
1. Check main power at disconnect
2. Verify control power at control panel
3. Check status of all safety devices
4. Verify start signal from control system
5. Check motor and VFD status
6. Test manual start at motor starter
```

#### AHU Running But No Airflow

**Possible Causes**:
- Fan belt broken
- Dampers closed
- Ductwork obstruction
- Fan rotation reversed

**Verification Steps**:
1. **Visual Inspection**:
   - Check fan belt condition
   - Verify fan rotation direction
   - Check damper positions
   - Look for obvious obstructions

2. **Measurements**:
   - Check motor current draw
   - Measure supply air flow
   - Check static pressure readings
   - Verify damper positions

### Pump System Issues

#### Pumps Not Providing Flow

**Diagnosis Steps**:
1. **Pump Operation**:
   - Check pump rotation direction
   - Verify impeller condition
   - Check for cavitation
   - Measure pump current

2. **System Checks**:
   - Verify isolation valves open
   - Check for air in system
   - Test pressure sensors
   - Check expansion tank

---

## Air Quality Issues

### High CO₂ Levels

#### Symptoms
- CO₂ readings > 1000 ppm
- Occupant complaints of stuffiness
- Air quality alarms active
- Poor indoor air quality

#### Investigation Process

**Step 1: Verify Readings**
1. **Sensor Verification**:
   - Check sensor calibration date
   - Test with portable CO₂ meter
   - Verify sensor location
   - Check for sensor drift

2. **Reading Analysis**:
   - Compare multiple zones
   - Check time-of-day patterns
   - Correlate with occupancy
   - Review historical trends

**Step 2: Ventilation Assessment**
1. **Outdoor Air Flow**:
   - Measure outdoor air damper position
   - Check outdoor air flow rate
   - Verify economizer operation
   - Test minimum OA controls

2. **System Operation**:
   - Check AHU operation
   - Verify return air flow
   - Check exhaust fan operation
   - Measure building pressure

#### Resolution Steps

| CO₂ Level | Action Required |
|-----------|----------------|
| < 800 ppm | Normal operation |
| 800-1000 ppm | Monitor trends |
| 1000-1500 ppm | Increase outdoor air |
| > 1500 ppm | Maximum ventilation + investigation |

### Humidity Control Problems

#### High Humidity Issues

**Symptoms**:
- Humidity > 65% RH
- Condensation on windows
- Musty odors
- Mold growth potential

**Troubleshooting**:
1. **Dehumidification Capacity**:
   - Check cooling coil operation
   - Verify chilled water temperature
   - Check coil air flow
   - Test humidity sensors

2. **External Factors**:
   - Check for water infiltration
   - Verify building envelope
   - Check occupancy levels
   - Review weather conditions

---

## Energy System Problems

### High Energy Consumption

#### Analysis Approach

**Step 1: Baseline Comparison**
1. **Historical Analysis**:
   - Compare to previous periods
   - Adjust for weather differences
   - Account for occupancy changes
   - Check for system modifications

**Step 2: Component Analysis**
1. **Major Energy Users**:
   - AHU fan energy
   - Pump energy consumption
   - Heating/cooling energy
   - Lighting and plug loads

2. **Efficiency Metrics**:
   - kW/ton for cooling
   - kW/CFM for air handling
   - Overall system efficiency
   - Peak demand patterns

#### Common Energy Issues

| Problem | Symptoms | Investigation |
|---------|----------|---------------|
| Fans running unnecessarily | High fan energy | Check schedules, occupancy sensors |
| Poor economizer operation | High cooling energy | Test outdoor air dampers, controls |
| Simultaneous heating/cooling | High total energy | Check zone controls, setpoints |
| Equipment short cycling | High peak demand | Check control dead bands, staging |

---

## HMI and Software Issues

### HMI Application Errors

#### Application Won't Start

**Common Error Messages**:
```
"Python module not found"
"Configuration file missing"
"Cannot connect to display"
"Permission denied"
```

**Resolution Steps**:
1. **Check Dependencies**:
   ```cmd
   python --version
   pip list | findstr matplotlib
   pip list | findstr numpy
   ```

2. **Configuration Files**:
   - Verify config/plc_config.ini exists
   - Check file permissions
   - Validate configuration syntax

3. **System Resources**:
   - Check available memory
   - Verify disk space
   - Close unnecessary applications

#### HMI Display Issues

**Symptoms**:
- Blank or frozen screens
- Missing graphics elements
- Slow screen updates
- Incorrect data display

**Troubleshooting**:
1. **Display Driver Issues**:
   - Update graphics drivers
   - Check display resolution
   - Test with different monitor
   - Verify graphics card compatibility

2. **Application Performance**:
   - Check CPU usage
   - Monitor memory consumption
   - Close background applications
   - Restart HMI application

---

## Sensor and Actuator Problems

### Temperature Sensor Issues

#### Sensor Reading Errors

**Symptom Analysis**:
```
Reading too high → Check for heat sources, calibration
Reading too low → Check for drafts, wiring issues
Erratic readings → Check connections, interference
No reading → Check power, wiring, sensor failure
```

**Testing Procedures**:
1. **Electrical Testing**:
   ```
   RTD Sensors (Pt100):
   - Resistance at 0°C: 100Ω
   - Resistance at 20°C: 107.79Ω
   - Check all three wires for continuity
   
   4-20mA Transmitters:
   - 4mA = minimum temperature
   - 20mA = maximum temperature
   - Check loop power (24VDC)
   ```

2. **Calibration Verification**:
   - Use certified reference thermometer
   - Check at multiple temperatures
   - Document calibration results
   - Adjust or replace if needed

### Actuator Problems

#### Damper Actuator Issues

**Common Problems**:
- Actuator not responding to control signal
- Incorrect position feedback
- Mechanical binding or sticking
- Slow or erratic operation

**Diagnostic Steps**:
1. **Control Signal Test**:
   ```
   Measure control signal:
   0-10V: Check with voltmeter
   4-20mA: Check with ammeter
   Verify signal matches HMI command
   ```

2. **Mechanical Inspection**:
   - Check linkage connections
   - Verify damper blade movement
   - Look for obstructions
   - Check mounting hardware

3. **Position Feedback**:
   - Test feedback signal accuracy
   - Check feedback potentiometer
   - Verify wiring connections
   - Calibrate if necessary

---

## Alarm Troubleshooting

### False Alarms

#### High Temperature Alarm - Zone 3

**Investigation Process**:
1. **Verify Actual Conditions**:
   - Check with portable thermometer
   - Compare adjacent zones
   - Review recent trends
   - Check time of alarm

2. **Sensor Issues**:
   - Test sensor accuracy
   - Check wiring connections
   - Look for interference sources
   - Verify mounting location

3. **Control Logic**:
   - Check alarm setpoints
   - Verify calculation logic
   - Test alarm delay timers
   - Review recent programming changes

### Persistent Alarms

#### Communication Alarm Won't Clear

**Troubleshooting Steps**:
1. **Verify Problem Resolution**:
   - Confirm communication restored
   - Check all devices responding
   - Test data exchange
   - Verify stable operation

2. **Alarm System Check**:
   - Check alarm acknowledgment
   - Verify alarm reset function
   - Test alarm database
   - Check for software bugs

---

## Emergency Situations

### Total System Failure

#### Immediate Actions
1. **Safety Assessment**:
   - Ensure personnel safety
   - Check for hazardous conditions
   - Verify emergency systems
   - Contact appropriate authorities

2. **Damage Control**:
   - Secure all equipment
   - Protect from further damage
   - Document current conditions
   - Notify management

#### Recovery Procedures
1. **Systematic Restart**:
   - Check for physical damage
   - Verify power systems
   - Test communication links
   - Restart in manual mode first

2. **Verification Testing**:
   - Test each subsystem
   - Verify safety systems
   - Check critical functions
   - Return to automatic mode

### Fire Alarm Integration Issues

#### Fire Alarm Not Shutting Down HVAC

**Critical Steps**:
1. **Manual Shutdown**:
   - Use emergency stop buttons
   - Shut down at main disconnects
   - Close fire/smoke dampers manually
   - Verify shutdown complete

2. **System Investigation**:
   - Check fire alarm interface
   - Verify wiring connections
   - Test contact operation
   - Check control logic

---

## Preventive Measures

### Regular Maintenance

#### Daily Checks
- [ ] Review all active alarms
- [ ] Check critical system parameters
- [ ] Verify backup systems ready
- [ ] Test emergency communications

#### Weekly Checks
- [ ] Sensor calibration verification
- [ ] Actuator position checks
- [ ] Communication system test
- [ ] Backup system test

#### Monthly Checks
- [ ] Complete system performance review
- [ ] Trending analysis
- [ ] Preventive maintenance updates
- [ ] Training refresher sessions

### Documentation

#### Maintain Current Records
- System configuration changes
- Calibration certificates
- Maintenance performed
- Problem resolution history

#### Update Procedures
- Keep troubleshooting guides current
- Document new solutions
- Update contact information
- Review and revise annually

---

## Quick Reference

### Emergency Contacts
- **Fire Department**: 911
- **Building Security**: Ext. 5555
- **Maintenance**: Ext. 2345
- **System Vendor**: 1-800-HVAC-HELP

### Key System Information
- **PLC IP**: 192.168.1.100
- **HMI Server**: HVAC-HMI-01
- **Backup Server**: 192.168.1.200
- **Config File**: config/plc_config.ini

### Diagnostic Tools
- **System Status**: `python system_status.py`
- **Network Test**: `ping 192.168.1.100`
- **Verification**: `python utils\verification\verify_system.py`

---

## Related Documents

- [Installation Guide](Installation.md)
- [Operating Procedures](Operating_Procedures.md)
- [Maintenance Manual](../docs/Maintenance_Manual.md)
- [Configuration Guide](Configuration.md)

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | June 8, 2025 | Initial troubleshooting guide |

---

*Last Updated: June 8, 2025*
