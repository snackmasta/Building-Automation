# HVAC System Troubleshooting Guide

## Table of Contents
1. [Quick Diagnostic Tools](#quick-diagnostic-tools)
2. [Temperature Control Issues](#temperature-control-issues)
3. [Air Quality Problems](#air-quality-problems)
4. [Equipment Malfunctions](#equipment-malfunctions)
5. [Communication Failures](#communication-failures)
6. [Energy Management Issues](#energy-management-issues)
7. [Safety System Problems](#safety-system-problems)
8. [Common Error Codes](#common-error-codes)
9. [Maintenance-Related Issues](#maintenance-related-issues)

## Quick Diagnostic Tools

### System Status Check
```bash
# Run comprehensive system verification
python utils\verification\verify_system.py

# Check system status monitor
python src\monitoring\system_status.py

# Generate system diagrams for visual inspection
python utils\hvac_diagram.py
```

### HMI Diagnostic Access
1. Open HMI interface: `scripts\batch\run_hmi.bat`
2. Navigate to **Diagnostics** tab
3. Review real-time system status
4. Check alarm history and trends

### Log File Locations
- System logs: `logs\hvac_system.log`
- Alarm logs: `logs\alarms.log`
- Energy logs: `logs\energy_data.log`
- Error logs: `logs\errors.log`

## Temperature Control Issues

### Zone Not Heating

#### Symptoms
- Zone temperature below setpoint
- Heating call active but no response
- Low supply air temperature

#### Diagnostic Steps
1. **Check Setpoints**
   - Verify occupied/unoccupied schedules
   - Confirm setpoint values in HMI
   - Check for manual overrides

2. **Inspect Equipment**
   ```
   □ Heating coil valve position
   □ Supply air temperature sensor
   □ Zone temperature sensor
   □ Damper positions
   ```

3. **Control System Check**
   - PID controller output values
   - Valve/damper control signals
   - Temperature sensor readings

#### Common Solutions
- **Stuck Heating Valve:** Manual exercise or replacement
- **Faulty Sensor:** Calibrate or replace temperature sensor
- **Control Loop Issue:** Retune PID parameters
- **Airflow Problem:** Check dampers and fan operation

### Zone Not Cooling

#### Symptoms
- Zone temperature above setpoint
- Cooling call active but no response
- High supply air temperature

#### Diagnostic Steps
1. **Refrigeration System**
   ```
   □ Compressor operation
   □ Refrigerant pressures
   □ Cooling coil temperature
   □ Condensate drainage
   ```

2. **Air Distribution**
   ```
   □ Supply air flow rates
   □ Damper positions
   □ Return air temperature
   □ Mixing box operation
   ```

#### Common Solutions
- **Low Refrigerant:** Check for leaks, recharge system
- **Dirty Coils:** Clean evaporator and condenser coils
- **Airflow Restrictions:** Clean filters, check ductwork
- **Control Issues:** Verify cooling valve operation

### Temperature Oscillation

#### Symptoms
- Temperature swinging above/below setpoint
- Frequent heating/cooling cycling
- Uncomfortable zone conditions

#### Diagnostic Steps
1. **Control Parameters**
   - PID tuning constants (P, I, D)
   - Deadband settings
   - Cycle timing parameters

2. **System Response**
   - Equipment capacity vs. load
   - Thermal mass considerations
   - External disturbances

#### Solutions
- **Retune Controllers:** Adjust PID parameters
- **Increase Deadband:** Reduce sensitivity
- **Equipment Sizing:** Verify capacity matches load

## Air Quality Problems

### High CO2 Levels

#### Symptoms
- CO2 readings above 1000 ppm
- Stuffy or uncomfortable conditions
- Occupant complaints

#### Diagnostic Steps
1. **Fresh Air System**
   ```
   □ Outside air damper position
   □ Fresh air flow rates
   □ Economizer operation
   □ Air mixing calculations
   ```

2. **Occupancy Factors**
   - Current occupancy vs. design
   - Ventilation requirements
   - Schedule verification

#### Solutions
- **Increase Fresh Air:** Adjust minimum outside air settings
- **Demand Control:** Implement CO2-based ventilation
- **System Capacity:** Verify adequate fresh air capability

### Humidity Problems

#### High Humidity (>70% RH)
1. **Check Dehumidification**
   - Cooling coil condensation
   - Reheat operation
   - Outdoor air conditions

2. **Solutions**
   - Increase cooling coil capacity
   - Add dedicated dehumidification
   - Adjust fresh air ratios

#### Low Humidity (<30% RH)
1. **Check Humidification**
   - Humidifier operation
   - Steam/water supply
   - Distribution system

2. **Solutions**
   - Increase humidification capacity
   - Check for air leaks
   - Adjust heating strategies

## Equipment Malfunctions

### Fan Problems

#### Fan Won't Start
1. **Electrical Checks**
   ```
   □ Power supply voltage
   □ Motor starter condition
   □ Control circuit continuity
   □ Overload protection status
   ```

2. **Mechanical Checks**
   ```
   □ Belt tension and alignment
   □ Bearing condition
   □ Impeller clearance
   □ Shaft alignment
   ```

#### Fan Running but Low Airflow
1. **Airflow Restrictions**
   - Dirty filters
   - Closed dampers
   - Blocked ductwork
   - Obstruction in unit

2. **Mechanical Issues**
   - Belt slippage
   - Wrong rotation direction
   - Damaged impeller
   - Motor speed issues

### Compressor Problems

#### Compressor Won't Start
1. **Safety Lockouts**
   ```
   □ High/low pressure switches
   □ Temperature safeties
   □ Oil pressure protection
   □ Phase protection
   ```

2. **Electrical Issues**
   ```
   □ Contactor operation
   □ Control voltage
   □ Motor windings
   □ Start components
   ```

#### Short Cycling
1. **Pressure Issues**
   - Low refrigerant charge
   - Restricted flow
   - Oversized equipment
   - Control sensitivity

2. **Solutions**
   - Check refrigerant levels
   - Clean coils and filters
   - Adjust time delays
   - Verify sizing calculations

### Valve/Damper Problems

#### Stuck or Slow Operation
1. **Actuator Issues**
   ```
   □ Air pressure (pneumatic)
   □ Control signal (electric)
   □ Linkage mechanical
   □ Calibration settings
   ```

2. **Mechanical Problems**
   ```
   □ Binding or corrosion
   □ Damaged seals
   □ Worn bearings
   □ Improper installation
   ```

## Communication Failures

### Network Connectivity Issues

#### Symptoms
- Controllers offline
- No data updates
- Communication timeouts
- HMI connection lost

#### Diagnostic Steps
1. **Physical Layer**
   ```
   □ Cable connections
   □ Network switch status
   □ Cable integrity
   □ Termination resistors
   ```

2. **Network Layer**
   ```
   □ IP address conflicts
   □ Subnet configuration
   □ Router/gateway settings
   □ Network traffic load
   ```

#### Solutions
- **Cable Issues:** Replace damaged cables
- **Network Config:** Verify IP settings
- **Switch Problems:** Reset or replace switches
- **Traffic Issues:** Optimize communication timing

### PLC Communication Errors

#### Controller Faults
1. **Hardware Diagnostics**
   - CPU status LEDs
   - I/O module indicators
   - Power supply voltage
   - Communication ports

2. **Software Issues**
   - Program corruption
   - Memory errors
   - Configuration mismatches
   - Firmware versions

## Energy Management Issues

### High Energy Consumption

#### Diagnostic Steps
1. **Baseline Comparison**
   - Historical energy data
   - Weather normalization
   - Occupancy adjustments
   - Equipment runtime hours

2. **System Efficiency**
   ```
   □ Equipment staging
   □ Load matching
   □ Economizer operation
   □ Schedule optimization
   ```

#### Solutions
- **Equipment Optimization:** Adjust staging sequences
- **Schedule Review:** Optimize start/stop times
- **Maintenance:** Clean coils, replace filters
- **Control Tuning:** Improve efficiency settings

### Demand Charges

#### Peak Demand Analysis
1. **Load Profiling**
   - Identify peak periods
   - Equipment contribution
   - Load diversity factors
   - Ramp rates

2. **Load Management**
   - Shed non-critical loads
   - Stagger equipment starts
   - Pre-cooling strategies
   - Demand limiting controls

## Safety System Problems

### Fire Mode Issues

#### Fire Alarm Interface
1. **Signal Verification**
   ```
   □ Fire alarm input status
   □ Smoke detector operation
   □ Manual pull stations
   □ System acknowledgment
   ```

2. **Response Actions**
   ```
   □ Supply fan shutdown
   □ Smoke damper closure
   □ Exhaust fan operation
   □ Notification systems
   ```

### Freeze Protection Problems

#### Low Temperature Alarms
1. **Temperature Monitoring**
   ```
   □ Sensor accuracy
   □ Location verification
   □ Calibration status
   □ Wiring integrity
   ```

2. **Protection Strategies**
   ```
   □ Heating activation
   □ Pump operation
   □ Valve positions
   □ Airflow management
   ```

## Common Error Codes

### PLC Error Codes
| Code | Description | Action |
|------|-------------|--------|
| E001 | Temperature sensor fault | Check wiring and calibration |
| E002 | Pressure sensor fault | Verify sensor and connections |
| E003 | Communication timeout | Check network connections |
| E004 | Safety interlock active | Identify and clear interlock |
| E005 | Equipment failure alarm | Inspect equipment operation |

### HMI Error Messages
| Message | Cause | Solution |
|---------|-------|---------|
| "Connection Lost" | Network failure | Check cables and settings |
| "Invalid Parameter" | Configuration error | Verify setpoint ranges |
| "Sensor Fault" | Failed sensor | Replace or recalibrate |
| "Override Active" | Manual override set | Check override settings |

## Maintenance-Related Issues

### Filter Problems

#### High Pressure Drop
1. **Filter Condition**
   - Visual inspection
   - Pressure measurements
   - Airflow impact
   - Replacement schedule

2. **Solutions**
   - Replace filters
   - Check sizing
   - Verify installation
   - Adjust schedule

### Calibration Issues

#### Sensor Drift
1. **Calibration Verification**
   ```
   □ Reference standard comparison
   □ Historical trending
   □ Cross-reference checks
   □ Environmental factors
   ```

2. **Correction Actions**
   - Recalibrate sensors
   - Replace if beyond limits
   - Document adjustments
   - Update schedules

## Emergency Contact Information

### Internal Contacts
- **HVAC Technician:** (555) 123-4567
- **Electrical Contractor:** (555) 234-5678
- **Control System Vendor:** (555) 345-6789
- **Facility Manager:** (555) 456-7890

### External Services
- **Fire Department:** 911
- **Utility Emergency:** (555) 567-8901
- **Refrigeration Service:** (555) 678-9012
- **24/7 HVAC Service:** (555) 789-0123

## Documentation References

### Technical Manuals
- Equipment installation manuals
- Control system programming guides
- Safety system documentation
- Sensor calibration procedures

### Drawings and Schematics
- System layout drawings
- Electrical schematics
- Control logic diagrams
- Piping and instrumentation diagrams

---

**Document Version:** 1.0  
**Last Updated:** June 8, 2025  
**Next Review:** December 8, 2025  
**Approved By:** HVAC System Administrator
