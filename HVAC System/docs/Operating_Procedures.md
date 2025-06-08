# HVAC System Operating Procedures

## Table of Contents
1. [Daily Operations](#daily-operations)
2. [Startup Procedures](#startup-procedures)
3. [Shutdown Procedures](#shutdown-procedures)
4. [Zone Control Operations](#zone-control-operations)
5. [Energy Management](#energy-management)
6. [Maintenance Operations](#maintenance-operations)
7. [Emergency Procedures](#emergency-procedures)
8. [Alarm Response](#alarm-response)

## Daily Operations

### Morning Startup Checklist
1. **System Status Check**
   - Run system verification: `utils\verification\verify_system.py`
   - Check all zones are operational
   - Verify temperature setpoints are appropriate
   - Confirm air quality sensors are functioning

2. **Equipment Inspection**
   - Check all fans are running normally
   - Verify compressor operation
   - Inspect heating/cooling coils
   - Check damper positions

3. **Data Review**
   - Review overnight alarm log
   - Check energy consumption trends
   - Verify occupancy schedule accuracy
   - Confirm setpoint schedules

### Zone Control Operations

#### Temperature Control
1. **Manual Setpoint Adjustment**
   ```
   Zone 1-8: Normal range 68-76°F (20-24°C)
   Unoccupied: 60-80°F (15-27°C) setback
   ```

2. **Occupancy Override**
   - Use HMI interface to override schedules
   - Maximum override: 4 hours
   - System returns to schedule automatically

3. **Seasonal Transitions**
   - Spring: Gradually reduce heating, increase fresh air
   - Summer: Optimize cooling efficiency, monitor humidity
   - Fall: Prepare heating systems, check dampers
   - Winter: Minimize fresh air, maximize heat recovery

#### Air Quality Management
1. **CO2 Control**
   - Target: <1000 ppm during occupied hours
   - Alert level: 1200 ppm
   - Action level: 1500 ppm (increase fresh air)

2. **Humidity Control**
   - Target range: 30-60% RH
   - Dehumidification: >70% RH
   - Humidification: <20% RH

## Energy Management

### Daily Energy Optimization
1. **Load Shedding Schedule**
   - Peak hours: 12:00-18:00 weekdays
   - Shed non-critical loads first
   - Monitor demand charges

2. **Equipment Scheduling**
   - Pre-cool before peak hours
   - Use thermal mass for energy storage
   - Optimize start/stop times

3. **Efficiency Monitoring**
   - Track kW/ton ratios
   - Monitor fan efficiency
   - Check economizer operation

### Demand Response Events
1. **Event Notification**
   - Monitor utility signals
   - Prepare load shedding plan
   - Notify facility management

2. **Response Actions**
   - Raise cooling setpoints 2-4°F
   - Reduce fresh air to minimums
   - Shed non-critical equipment

## Startup Procedures

### System Cold Start
1. **Pre-Startup Checks**
   ```
   □ Power supply verified
   □ Water systems primed
   □ Filters checked/replaced
   □ Safety systems tested
   ```

2. **Sequential Startup**
   ```
   1. Start building management system
   2. Initialize PLC controllers
   3. Start air handling units
   4. Enable zone controls
   5. Activate safety systems
   ```

3. **Verification Steps**
   - Run system diagnostics
   - Check all I/O points
   - Verify communication links
   - Test emergency stops

### Zone-by-Zone Startup
1. **Zone Preparation**
   - Set initial setpoints
   - Check damper positions
   - Verify sensor readings

2. **Equipment Activation**
   - Start fans at minimum speed
   - Enable temperature control
   - Activate air quality monitoring

## Shutdown Procedures

### Normal Shutdown
1. **Preparation Phase**
   - Notify occupants (if applicable)
   - Complete current control cycles
   - Save system data

2. **Equipment Shutdown Sequence**
   ```
   1. Disable heating/cooling
   2. Run fans for purge cycle (10 minutes)
   3. Close dampers to minimum position
   4. Stop fans
   5. Disable pumps
   6. Shutdown compressors
   ```

### Emergency Shutdown
1. **Immediate Actions**
   - Activate emergency stop
   - Shut down all equipment
   - Close all dampers
   - Notify emergency services if required

2. **Post-Emergency**
   - Document incident
   - Inspect equipment
   - Reset systems only after clearance

## Maintenance Operations

### Daily Maintenance
- **Visual Inspections**
  - Equipment operation status
  - Unusual noises or vibrations
  - Leak detection
  - Display readings verification

- **Data Collection**
  - Energy consumption logging
  - Temperature/humidity trends
  - Equipment runtime hours
  - Alarm history review

### Weekly Maintenance
- **Filter Inspection**
  - Check pressure drops
  - Visual contamination assessment
  - Replace if necessary

- **Calibration Checks**
  - Temperature sensor verification
  - Pressure transducer checks
  - Flow measurement validation

### Monthly Maintenance
- **Comprehensive Testing**
  - Safety system functional tests
  - Emergency shutdown procedures
  - Backup system verification
  - Control loop tuning

## Emergency Procedures

### Fire Emergency
1. **Automatic Response**
   - System switches to fire mode
   - Smoke dampers close
   - Supply fans stop
   - Exhaust fans continue

2. **Manual Actions**
   - Verify fire alarm activation
   - Coordinate with fire department
   - Do not reset until clearance given

### Freeze Protection
1. **Automatic Protection**
   - Low temperature alarms activate
   - Heating stages energize
   - Anti-freeze valves open
   - Pumps maintain circulation

2. **Manual Response**
   - Check for equipment damage
   - Verify heating operation
   - Monitor temperatures closely

### Power Failure
1. **Immediate Actions**
   - Emergency lighting activated
   - Critical systems on UPS
   - Generator startup (if available)

2. **Recovery Procedures**
   - Gradual equipment restart
   - System verification
   - Resume normal operations

## Alarm Response

### Temperature Alarms
- **High Temperature**
  - Check cooling system operation
  - Verify thermostat settings
  - Inspect for equipment failures

- **Low Temperature**
  - Activate freeze protection
  - Check heating systems
  - Verify damper positions

### Equipment Alarms
- **Fan Failure**
  - Check motor status
  - Verify power supply
  - Inspect mechanical components

- **Compressor Failure**
  - Check refrigerant levels
  - Verify electrical connections
  - Inspect for mechanical issues

### Air Quality Alarms
- **High CO2**
  - Increase fresh air intake
  - Check occupancy levels
  - Verify sensor calibration

- **Humidity Alarms**
  - Adjust humidity control settings
  - Check for water leaks
  - Verify dehumidification operation

## Documentation Requirements

### Daily Logs
- System status reports
- Energy consumption data
- Alarm logs and responses
- Maintenance activities

### Incident Reports
- Equipment failures
- Emergency activations
- Unusual conditions
- Corrective actions taken

### Performance Records
- Energy efficiency metrics
- Temperature control accuracy
- Air quality measurements
- Equipment runtime data

## Training Requirements

### Operator Certification
- Basic HVAC principles
- System operation procedures
- Emergency response training
- Safety protocols

### Ongoing Education
- Monthly safety meetings
- Quarterly system updates
- Annual certification renewal
- New technology training

---

**Document Version:** 1.0  
**Last Updated:** June 8, 2025  
**Next Review:** December 8, 2025  
**Approved By:** HVAC System Administrator
