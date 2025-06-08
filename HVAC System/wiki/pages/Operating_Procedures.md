# Operating Procedures

## HVAC Control System Operating Procedures

This document provides comprehensive operating procedures for the HVAC Control System, including normal operations, startup/shutdown procedures, and operational best practices.

---

## Table of Contents

1. [System Overview](#system-overview)
2. [Daily Operations](#daily-operations)
3. [Startup Procedures](#startup-procedures)
4. [Shutdown Procedures](#shutdown-procedures)
5. [Normal Operations](#normal-operations)
6. [Alarm Management](#alarm-management)
7. [Emergency Procedures](#emergency-procedures)
8. [Seasonal Operations](#seasonal-operations)
9. [Performance Monitoring](#performance-monitoring)
10. [Operator Responsibilities](#operator-responsibilities)

---

## System Overview

### System Components

The HVAC Control System consists of:

- **8-Zone Temperature Control**: Individual climate control for each zone
- **Air Quality Management**: CO₂, humidity, and VOC monitoring
- **Energy Management**: Optimized system operation for efficiency
- **Safety Systems**: Fire safety and emergency shutdown capabilities
- **HMI Interface**: Operator control and monitoring interface

### Control Philosophy

The system operates based on:
- **Demand-based control**: Adjusts operation based on occupancy and load
- **Energy optimization**: Minimizes energy consumption while maintaining comfort
- **Safety-first approach**: All safety systems have priority over comfort
- **Predictive control**: Uses weather and occupancy forecasts

---

## Daily Operations

### Morning Startup Routine

#### Pre-Startup Checks (7:00 AM)

1. **Visual Inspection**:
   - [ ] Check all equipment for visible damage
   - [ ] Verify no water leaks or unusual condensation
   - [ ] Ensure all access panels are secure
   - [ ] Check for unusual noises or vibrations

2. **System Status Review**:
   - [ ] Review overnight alarm log
   - [ ] Check system runtime hours
   - [ ] Verify equipment status indicators
   - [ ] Review energy consumption data

3. **Environmental Conditions**:
   - [ ] Check outdoor weather conditions
   - [ ] Review building occupancy schedule
   - [ ] Verify internal heat loads (lighting, equipment)

#### Startup Sequence (7:30 AM)

1. **Launch System Components**:
   ```cmd
   cd "HVAC System"
   scripts\batch\system_launcher.bat
   ```
   Select option 4: "Start Complete System"

2. **Verify System Communication**:
   - PLC connectivity indicator: GREEN
   - All zone sensors reading properly
   - Actuator position feedback normal

3. **Initial System Checks**:
   - All zones in AUTO mode
   - Setpoints at scheduled values
   - No active alarms
   - Energy management system active

### Hourly Monitoring

#### System Performance (Every Hour)

1. **Zone Control Verification**:
   - Check temperature readings vs. setpoints
   - Verify damper positions are reasonable
   - Monitor humidity levels (30-60% RH)
   - Check air quality readings

2. **Equipment Status**:
   - AHU operation status
   - Pump operation and flow rates
   - Chiller/boiler operation (if applicable)
   - Filter pressure drop readings

3. **Energy Monitoring**:
   - Current power consumption
   - Cumulative energy usage
   - Efficiency metrics
   - Cost tracking

### End-of-Day Review (5:00 PM)

1. **Performance Summary**:
   - Review daily energy consumption
   - Check comfort complaints or issues
   - Verify all alarms were addressed
   - Update operational log

2. **Night Mode Preparation**:
   - Switch to unoccupied schedule
   - Verify setback temperatures active
   - Reduce ventilation to minimum
   - Enable enhanced energy savings

---

## Startup Procedures

### Cold Start Procedure

When starting the system after extended shutdown:

#### Step 1: Pre-Start Inspection

1. **Electrical Systems**:
   - [ ] Verify main power available
   - [ ] Check control power circuits
   - [ ] Test emergency stop circuits
   - [ ] Verify UPS systems charged

2. **Mechanical Systems**:
   - [ ] Check all isolation valves open
   - [ ] Verify filter conditions
   - [ ] Check belt tensions and conditions
   - [ ] Ensure all guards in place

3. **Control Systems**:
   - [ ] Boot control servers/PCs
   - [ ] Verify network connectivity
   - [ ] Load current control programs
   - [ ] Test HMI functionality

#### Step 2: System Startup

1. **Start in Manual Mode**:
   ```
   1. Set all zones to MANUAL mode
   2. Set all outputs to 0%
   3. Enable PLC scan
   4. Verify I/O status
   ```

2. **Equipment Sequencing**:
   ```
   1. Start auxiliary equipment (pumps, fans)
   2. Verify flow and pressure readings
   3. Start main AHU units
   4. Check system pressures stabilize
   5. Enable automatic controls
   ```

3. **Zone-by-Zone Activation**:
   ```
   For each zone:
   1. Switch to AUTO mode
   2. Set normal setpoint
   3. Verify control response
   4. Check sensor readings
   5. Test damper operation
   ```

### Warm Start Procedure

For routine daily startup or restart after brief shutdown:

1. **Quick System Check**:
   - Review overnight status
   - Check for any alarms
   - Verify equipment ready status

2. **Automated Startup**:
   - Use system launcher script
   - Monitor startup sequence
   - Verify normal operation achieved

---

## Shutdown Procedures

### Normal Shutdown

#### Planned Shutdown Sequence

1. **Prepare for Shutdown**:
   - [ ] Notify occupants if during occupied hours
   - [ ] Switch all zones to MANUAL mode
   - [ ] Set all outputs to minimum safe position

2. **Equipment Shutdown**:
   ```
   1. Reduce airflow to minimum
   2. Close isolation dampers
   3. Stop AHU units in sequence
   4. Stop pumps and auxiliary equipment
   5. Disable automatic controls
   ```

3. **System Secure**:
   - [ ] Save current configuration
   - [ ] Close HMI applications
   - [ ] Secure control systems
   - [ ] Document shutdown reason and time

### Emergency Shutdown

#### Immediate Shutdown (Emergency)

1. **Emergency Stop Activation**:
   - Press emergency stop button
   - OR activate fire alarm system
   - OR use HMI emergency shutdown

2. **Verify Equipment Stopped**:
   - All fans stopped
   - All dampers closed
   - All pumps stopped
   - Only emergency lighting active

3. **Safety Verification**:
   - Check for gas leaks
   - Verify electrical isolation
   - Ensure access routes clear
   - Contact emergency services if required

---

## Normal Operations

### Zone Control Operations

#### Temperature Control

1. **Setpoint Management**:
   - Occupied hours: 22°C ± 1°C (72°F ± 2°F)
   - Unoccupied hours: 18°C heating / 26°C cooling
   - Special events: Adjust as required

2. **Manual Override**:
   ```
   To override zone temperature:
   1. Select zone on HMI
   2. Switch to MANUAL mode
   3. Adjust setpoint as needed
   4. Set timer for auto return
   5. Document override reason
   ```

3. **Seasonal Adjustments**:
   - Summer: Increase cooling setpoints by 1°C
   - Winter: Decrease heating setpoints by 1°C
   - Transition: Use economizer when beneficial

#### Air Quality Control

1. **CO₂ Management**:
   - Target: < 1000 ppm
   - High alarm: > 1500 ppm
   - Response: Increase outdoor air

2. **Humidity Control**:
   - Target range: 40-60% RH
   - Winter minimum: 30% RH
   - Summer maximum: 65% RH

### Equipment Operations

#### Air Handling Units

1. **Normal Operation**:
   - Monitor supply/return air temperatures
   - Check filter pressure drop daily
   - Verify damper operation
   - Monitor motor current draw

2. **Performance Optimization**:
   - Adjust outdoor air based on occupancy
   - Use economizer when beneficial
   - Optimize supply air temperature
   - Balance airflow quarterly

#### Energy Management

1. **Load Shedding**:
   - Available when utility requests
   - Automatic during peak demand
   - Manual override available
   - Restore after demand reduction

2. **Optimization Strategies**:
   - Night setback operation
   - Optimal start/stop times
   - Demand-based ventilation
   - Free cooling utilization

---

## Alarm Management

### Alarm Categories

#### Priority 1 - Critical Alarms
- Fire alarm activation
- Emergency shutdown triggered
- Loss of control communication
- High temperature safety limit

**Response**: Immediate action required

#### Priority 2 - High Alarms
- Equipment failure
- Sensor malfunction
- High/low temperature alarm
- Air quality alarm

**Response**: Action required within 1 hour

#### Priority 3 - Warning Alarms
- Maintenance due
- Filter change required
- Efficiency degradation
- Minor sensor drift

**Response**: Action required within 24 hours

### Alarm Response Procedures

#### Alarm Acknowledgment

1. **Review Alarm**:
   - Read alarm description
   - Check alarm time and duration
   - Identify affected equipment/zone

2. **Initial Assessment**:
   - Check current system status
   - Verify alarm is valid
   - Assess safety implications

3. **Acknowledge Alarm**:
   - Press ACK button on HMI
   - Document initial assessment
   - Assign response priority

#### Alarm Investigation

1. **Gather Information**:
   - Review system trends
   - Check related equipment
   - Interview operators/occupants

2. **Determine Root Cause**:
   - Analyze failure sequence
   - Check maintenance history
   - Consider environmental factors

3. **Implement Corrective Action**:
   - Make necessary repairs
   - Adjust system settings
   - Schedule follow-up maintenance

---

## Emergency Procedures

### Fire Emergency

#### Detection and Response

1. **Fire Alarm Activation**:
   - Automatic shutdown activated
   - All supply fans stopped
   - Smoke dampers closed
   - Emergency lighting activated

2. **Operator Actions**:
   - [ ] Verify alarm is not false
   - [ ] Contact fire department (911)
   - [ ] Ensure safe evacuation
   - [ ] Remain available for fire department

3. **System Recovery**:
   - Do not restart until cleared by fire department
   - Inspect all equipment before restart
   - Test all safety systems
   - Document incident completely

### Power Failure

#### UPS Operation

1. **Power Loss Detection**:
   - UPS automatically activated
   - Critical systems maintained
   - HMI displays power status

2. **Extended Outage Procedures**:
   - [ ] Switch to essential loads only
   - [ ] Monitor UPS battery status
   - [ ] Prepare for graceful shutdown
   - [ ] Save all current data

3. **Power Restoration**:
   - Wait for stable power (5 minutes)
   - Restart systems in proper sequence
   - Verify all equipment normal
   - Check for any damage

### Equipment Failure

#### Critical Equipment Failure

1. **Immediate Response**:
   - Isolate failed equipment
   - Switch to backup if available
   - Adjust remaining equipment loading
   - Monitor critical parameters

2. **Emergency Operation**:
   - Operate in manual mode if necessary
   - Prioritize life safety systems
   - Maintain minimal comfort levels
   - Contact maintenance immediately

---

## Seasonal Operations

### Summer Operation

#### Cooling Season Preparation

1. **System Changeover**:
   - [ ] Switch heating/cooling mode
   - [ ] Check cooling coil operation
   - [ ] Verify chilled water systems
   - [ ] Test economizer operation

2. **Setpoint Adjustments**:
   - Increase cooling setpoints 1°C
   - Enable humidity control
   - Adjust outdoor air minimums
   - Activate demand limiting

#### Peak Demand Management

1. **Load Shedding Strategy**:
   - Pre-cool building before peak
   - Raise setpoints during peak (3-6 PM)
   - Reduce outdoor air temporarily
   - Cycle non-critical equipment

### Winter Operation

#### Heating Season Preparation

1. **System Changeover**:
   - [ ] Switch cooling/heating mode
   - [ ] Check heating coil operation
   - [ ] Verify hot water systems
   - [ ] Test freeze protection

2. **Cold Weather Operation**:
   - Monitor outdoor air temperature
   - Enable freeze protection
   - Adjust minimum outdoor air
   - Check humidity levels

### Transition Seasons

#### Spring/Fall Operation

1. **Economizer Utilization**:
   - Maximize free cooling/heating
   - Monitor outdoor air quality
   - Adjust based on weather forecasts
   - Optimize mixed air temperature

---

## Performance Monitoring

### Key Performance Indicators

#### Energy Performance

1. **Daily Metrics**:
   - Total energy consumption (kWh)
   - Peak demand (kW)
   - Energy use intensity (kWh/m²)
   - Cost per day

2. **Efficiency Metrics**:
   - COP (Coefficient of Performance)
   - EER (Energy Efficiency Ratio)
   - Fan energy ratio
   - Pump efficiency

#### Comfort Performance

1. **Temperature Performance**:
   - Average zone temperatures
   - Setpoint deviation
   - Comfort complaints
   - Thermal uniformity

2. **Air Quality Performance**:
   - Average CO₂ levels
   - Humidity levels
   - Ventilation effectiveness
   - Outdoor air percentage

### Reporting

#### Daily Reports

Generate daily performance reports including:
- Energy consumption summary
- Comfort metric summary
- Alarm summary
- Equipment runtime hours

#### Weekly Analysis

1. **Trend Analysis**:
   - Week-over-week comparisons
   - Seasonal adjustments needed
   - Equipment performance trends
   - Energy efficiency trends

2. **Maintenance Planning**:
   - Equipment runtime analysis
   - Filter change requirements
   - Calibration scheduling
   - Preventive maintenance planning

---

## Operator Responsibilities

### Primary Operator Duties

#### Daily Responsibilities

1. **System Monitoring**:
   - [ ] Monitor all system alarms
   - [ ] Check equipment status hourly
   - [ ] Review energy consumption
   - [ ] Respond to comfort complaints

2. **Documentation**:
   - [ ] Complete daily log sheets
   - [ ] Document all alarm responses
   - [ ] Record any manual overrides
   - [ ] Note any unusual conditions

3. **Communication**:
   - [ ] Report issues to maintenance
   - [ ] Coordinate with building management
   - [ ] Communicate with occupants
   - [ ] Update shift handover log

#### Weekly Responsibilities

1. **Performance Review**:
   - [ ] Analyze weekly energy reports
   - [ ] Review comfort metrics
   - [ ] Check equipment efficiency
   - [ ] Plan optimization improvements

2. **Maintenance Coordination**:
   - [ ] Schedule routine maintenance
   - [ ] Review maintenance reports
   - [ ] Update equipment logs
   - [ ] Plan equipment upgrades

### Training Requirements

#### Initial Training

1. **System Familiarization**:
   - HVAC system basics
   - Control system operation
   - HMI interface training
   - Safety procedures

2. **Operational Training**:
   - Normal operations
   - Startup/shutdown procedures
   - Alarm response
   - Emergency procedures

#### Ongoing Training

1. **Monthly Topics**:
   - New features or updates
   - Seasonal operation changes
   - Energy efficiency improvements
   - Safety refresher training

2. **Annual Requirements**:
   - Complete system review
   - Emergency drill participation
   - Control system updates
   - Certification maintenance

---

## Quality Assurance

### Operational Verification

#### Weekly Checks

1. **Control Loop Verification**:
   - [ ] Temperature control accuracy
   - [ ] Damper position feedback
   - [ ] Sensor calibration check
   - [ ] Actuator response time

2. **Safety System Testing**:
   - [ ] Fire alarm interface test
   - [ ] Emergency shutdown test
   - [ ] High limit alarm test
   - [ ] Communication backup test

### Documentation Standards

#### Log Keeping

1. **Required Entries**:
   - Time and date of all entries
   - Operator name/initials
   - System status at time of entry
   - Any actions taken

2. **Incident Documentation**:
   - Complete description of event
   - Actions taken to resolve
   - Follow-up requirements
   - Preventive measures implemented

---

## Support Resources

### Quick Reference

#### Emergency Contacts
- **Fire Department**: 911
- **Building Security**: Ext. 5555
- **Maintenance Manager**: Ext. 2345
- **System Vendor**: 1-800-HVAC-HELP

#### System Information
- **PLC IP Address**: 192.168.1.100
- **HMI Server**: HVAC-HMI-01
- **Network Backup**: 192.168.1.200
- **Documentation**: [Wiki Home](../Home.md)

### Related Documents

- [Installation Guide](Installation.md)
- [Troubleshooting Guide](Troubleshooting.md)
- [Maintenance Manual](../docs/Maintenance_Manual.md)
- [Configuration Guide](Configuration.md)

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | June 8, 2025 | Initial operating procedures |

---

*Last Updated: June 8, 2025*
