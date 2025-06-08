# Wastewater Treatment Plant Operating Procedures

**Document Number:** WWTP-OP-001  
**Revision:** 1.0  
**Date:** June 8, 2025  

## Table of Contents
1. [Introduction](#introduction)
2. [System Overview](#system-overview)
3. [Normal Operations](#normal-operations)
4. [Startup Procedures](#startup-procedures)
5. [Shutdown Procedures](#shutdown-procedures)
6. [Emergency Procedures](#emergency-procedures)
7. [Maintenance Procedures](#maintenance-procedures)
8. [Special Operating Conditions](#special-operating-conditions)
9. [Process Control Parameters](#process-control-parameters)
10. [Quality Management](#quality-management)
11. [Health, Safety, and Environmental Considerations](#health-safety-and-environmental-considerations)
12. [Reporting and Documentation](#reporting-and-documentation)

## Introduction

This operating procedure document provides comprehensive guidance for the safe and effective operation of the automated Wastewater Treatment Plant (WWTP). The document covers normal operations, startup and shutdown procedures, emergency responses, maintenance activities, and special operating conditions.

All plant operators, maintenance personnel, and supervisors must be familiar with these procedures and follow them diligently to ensure:
- Compliance with regulatory requirements
- Protection of public health and the environment
- Efficient operation of treatment processes
- Worker safety
- Proper equipment functioning and longevity

## System Overview

The Wastewater Treatment Plant consists of the following main subsystems:

1. **Intake and Screening**
   - Bar screens for large debris removal
   - Grit chambers for sand/grit removal
   - Flow measurement instrumentation
   - Influent pumping station

2. **Primary Treatment**
   - Primary clarifiers/sedimentation tanks
   - Sludge collection mechanisms
   - Primary sludge pumping

3. **Secondary Treatment**
   - Aeration basins with diffused air system
   - Blowers for oxygen supply
   - Return activated sludge (RAS) pumping
   - Waste activated sludge (WAS) pumping
   - Secondary clarifiers

4. **Chemical Treatment**
   - pH adjustment system
   - Phosphorus removal (if applicable)
   - Chemical storage and dosing systems

5. **Disinfection**
   - UV disinfection system
   - Chlorine contact chamber (if applicable)
   - Dechlorination system (if applicable)

6. **Monitoring and Control**
   - Process instrumentation (flow, level, pH, DO, turbidity)
   - PLC control system
   - SCADA/HMI interfaces
   - Sampling points and laboratory analysis

## Normal Operations

### Daily Operator Tasks

#### Beginning of Shift
1. Review the previous shift's logs and notes
2. Check the SCADA system for alarms or abnormal conditions
3. Perform visual inspection of equipment and processes
4. Collect and analyze routine samples or verify automatic sampling
5. Check chemical inventory levels
6. Verify all critical equipment is operational

#### During Shift
1. Monitor process parameters through HMI/SCADA:
   - Flow rates (influent, effluent, RAS, WAS)
   - Tank levels
   - DO levels in aeration basins
   - pH values
   - Turbidity measurements
   - Chemical dosing rates
   - Equipment status

2. Respond to any alarms or abnormal conditions
3. Make process adjustments as needed:
   - Adjust blower output to maintain DO setpoints
   - Modify chemical dosing rates based on lab results
   - Adjust RAS/WAS rates to maintain proper sludge age
   - Modify flow distribution as needed

4. Perform scheduled sampling and testing
5. Maintain accurate logs of all activities and observations

#### End of Shift
1. Brief incoming operators on current plant status
2. Document any issues requiring follow-up
3. Complete all required logs and reports
4. Ensure control systems are left in the appropriate mode (auto/manual)

## Startup Procedures

### System Startup from Complete Shutdown

1. **Pre-startup Checks**
   - Verify electrical systems are operational
   - Check that all valves are in their correct positions
   - Ensure adequate chemical supplies are available
   - Confirm all safety systems are functioning
   - Verify communication networks are operational

2. **Control System Initialization**
   - Power up the control panels and HMI workstations
   - Login to the SCADA system
   - Acknowledge any standing alarms
   - Set the system to "Manual" mode initially

3. **Subsystem Startup Sequence**
   
   a. **Intake System**
      - Start bar screen cleaning mechanisms
      - Open influent valves
      - Start grit removal systems
      - Start influent pumps at minimum speed
      - Verify flow measurement instrumentation is working

   b. **Primary Treatment**
      - Start sludge scraper mechanisms
      - Open influent valves to primary clarifiers
      - Start primary sludge pumps on timed operation

   c. **Secondary Treatment**
      - Start aeration blowers at minimum speed
      - Verify proper airflow distribution to aeration basins
      - Start RAS pumps at minimum speed
      - Start WAS pumps based on solids management requirements
      - Verify secondary clarifier mechanisms are operational

   d. **Disinfection System**
      - Power up UV system (if applicable)
      - Start chlorine dosing system at minimum rate (if applicable)
      - Start dechlorination system (if applicable)

   e. **Chemical Systems**
      - Start chemical metering pumps
      - Verify proper chemical feed rates

4. **Transition to Automatic Control**
   - Once all systems are stable, transition from "Manual" to "Auto" mode
   - Verify all control loops are functioning properly
   - Monitor system closely for the first hour after full startup

## Shutdown Procedures

### Planned Full System Shutdown

1. **Preparation**
   - Notify appropriate regulatory agencies if required
   - Create a shutdown schedule
   - Notify downstream systems or users

2. **Control System Transition**
   - Switch from "Auto" to "Manual" mode
   - Reduce all process rates gradually

3. **Subsystem Shutdown Sequence**

   a. **Chemical Systems**
      - Reduce chemical dosing gradually to minimum
      - Stop chemical metering pumps
      - Close chemical supply valves

   b. **Disinfection System**
      - Reduce UV intensity gradually (if applicable)
      - Stop chlorine dosing system (if applicable)
      - Allow sufficient contact time before stopping flow

   c. **Secondary Treatment**
      - Reduce aeration blower output gradually
      - Stop WAS pumping
      - Reduce and then stop RAS pumping
      - Allow secondary clarifiers to continue operating

   d. **Primary Treatment**
      - Stop primary sludge pumps after final cycle
      - Allow primary clarifiers to continue operating

   e. **Intake System**
      - Stop influent pumps
      - Close influent valves
      - Stop grit removal systems
      - Stop bar screen mechanisms

4. **Final Steps**
   - Complete final sampling if required
   - Document shutdown in logs
   - Secure facility if shutdown will be extended

### Emergency Shutdown

See [Emergency Procedures](#emergency-procedures) section.

## Emergency Procedures

### Emergency Shutdown Procedure

1. Press the "EMERGENCY STOP" button on any HMI or physical control panel
2. The automated emergency shutdown sequence will:
   - Stop all pumps immediately
   - Close critical motorized valves
   - Switch aeration to minimum settings
   - Maintain power to monitoring systems
   - Trigger alarms and notifications

3. Immediately notify the plant supervisor and appropriate authorities
4. Document the cause of the emergency shutdown
5. Follow recovery procedures once the emergency is resolved

### Specific Emergency Situations

#### Power Failure
1. Verify backup generators have started (if installed)
2. If no backup power is available:
   - Verify critical valves fail to their safe positions
   - Prepare for manual operation of critical systems
   - Contact utility provider to get restoration estimate

#### Chemical Spill
1. Follow the facility's Hazardous Materials Response Plan
2. Evacuate affected areas if necessary
3. Use appropriate PPE before approaching spill area
4. Contain the spill using available spill kits
5. Prevent chemicals from entering waterways or drainage systems
6. Report the spill to appropriate authorities if required

#### Flooding
1. Shut down electrical equipment in affected areas
2. Deploy pumps to remove water if safe to do so
3. Protect critical electrical and control components
4. Evaluate structural integrity before restart

#### High Influent Flow (Storm Event)
1. Activate "Storm Mode" in the control system
2. Monitor levels in all tanks
3. Ensure bypass systems are ready if needed
4. Increase sampling frequency to monitor treatment effectiveness

#### Equipment Failure
1. Identify the failed equipment and its impact on the process
2. Switch to redundant equipment if available
3. If no redundancy exists, implement contingency operations
4. Contact maintenance personnel for repairs

## Maintenance Procedures

### Routine Maintenance

1. **Daily Maintenance Tasks**
   - Visual inspection of all accessible equipment
   - Greasing of specified bearings
   - Cleaning of sensor probes
   - Debris removal from screens

2. **Weekly Maintenance Tasks**
   - Check oil levels in gear boxes
   - Inspect belt drives for wear and tension
   - Test emergency backup systems
   - Calibrate critical instruments

3. **Monthly Maintenance Tasks**
   - Complete motor insulation tests
   - Check valve actuators for proper operation
   - Inspect diffusers for fouling
   - Test chemical pumps for accurate delivery

### Planned Maintenance Shutdowns

1. **Preparation**
   - Schedule during periods of low flow when possible
   - Ensure all replacement parts and tools are available
   - Brief all personnel on the maintenance plan
   - Have contingency plans ready

2. **Shutdown Process**
   - Follow the appropriate shutdown procedure for the system
   - Isolate the equipment with lock-out/tag-out procedures
   - Verify zero energy state before work begins
   - Complete maintenance tasks according to specifications
   - Test equipment before returning to service

3. **Restart Process**
   - Remove all lock-out/tag-out devices
   - Follow appropriate startup procedures
   - Monitor closely during initial operation
   - Document maintenance and any issues encountered

## Special Operating Conditions

### Storm Mode

1. **Activation Criteria**
   - Influent flow exceeds 150% of average daily flow
   - Sudden increase in flow rate exceeding 10% per minute
   - Weather service warnings for heavy precipitation
   - Operator judgment based on local conditions

2. **Storm Mode Operations**
   - Increase screening cleaning frequency
   - Maximize primary treatment capacity
   - Adjust chemical dosing rates for higher flows
   - Increase monitoring frequency
   - Prepare equalization basins if available

3. **Deactivation Criteria**
   - Flow returns to within 110% of average daily flow
   - Stable influent flow patterns for at least 2 hours
   - Weather event has passed

### Low Flow Operations

1. **Activation Criteria**
   - Influent flow falls below 50% of average daily flow
   - Extended dry weather periods
   - Scheduled upstream maintenance

2. **Low Flow Operations**
   - Reduce number of units in service
   - Adjust air supply to match reduced oxygen demand
   - Modify chemical dosing rates
   - Implement energy conservation measures
   - Consider batch operation of certain processes

### Cold Weather Operations

1. **Preparation**
   - Inspect and activate all heating systems
   - Ensure insulation is intact on exposed pipes
   - Check antifreeze protection in critical systems

2. **Operations Adjustments**
   - Monitor biological activity more closely (typically reduced in cold)
   - Adjust sludge age to compensate for slower biological activity
   - Ensure adequate mixing to prevent freezing
   - Keep critical valves and actuators moving regularly

### Hot Weather Operations

1. **Preparation**
   - Check cooling systems for all equipment
   - Ensure adequate ventilation in enclosed spaces
   - Verify chemical storage conditions are appropriate

2. **Operations Adjustments**
   - Monitor for increased biological activity
   - Be alert for algae growth in clarifiers
   - Adjust chemical dosing (chemical reactions often faster in heat)
   - Implement odor control measures (odors typically worse in heat)

## Process Control Parameters

### Critical Control Parameters and Targets

| Parameter | Target Range | Critical Limits | Monitoring Frequency |
|-----------|--------------|----------------|---------------------|
| **Primary Treatment** |
| Influent Flow | 200-400 m³/hr | <100 or >500 m³/hr | Continuous |
| Primary Tank Level | 2.0-3.0 m | <1.0 or >4.0 m | Continuous |
| Retention Time | 2.0-3.0 hours | <1.5 hours | Calculated daily |
| **Aeration Process** |
| Dissolved Oxygen | 2.0-4.0 mg/L | <1.0 or >6.0 mg/L | Continuous |
| MLSS | 2500-3500 mg/L | <2000 or >4000 mg/L | Daily testing |
| F/M Ratio | 0.15-0.25 | <0.10 or >0.50 | Calculated weekly |
| Sludge Age | 10-15 days | <8 or >20 days | Calculated weekly |
| **Chemical Treatment** |
| pH | 6.8-7.5 | <6.0 or >8.5 | Continuous |
| Phosphorus | <1.0 mg/L | >2.0 mg/L | Daily testing |
| Chemical Dosage | Process specific | Process specific | Continuous |
| **Disinfection** |
| UV Intensity | >30 mJ/cm² | <25 mJ/cm² | Continuous |
| Chlorine Residual | 0.5-1.5 mg/L | <0.2 or >2.0 mg/L | Continuous |
| Contact Time | >30 minutes | <25 minutes | Calculated daily |
| **Effluent Quality** |
| TSS | <30 mg/L | >45 mg/L | Daily testing |
| BOD₅ | <25 mg/L | >40 mg/L | Weekly testing |
| Turbidity | <10 NTU | >15 NTU | Continuous |
| E. coli | <200 cfu/100mL | >400 cfu/100mL | Daily testing |

### Process Control Adjustments

#### DO Control Loop
- **Setpoint:** 2.5 mg/L (adjustable based on load)
- **Control Method:** PID control of blower speed
- **Adjustment Triggers:**
  - High ammonia in effluent: Increase DO setpoint by 0.5 mg/L
  - Low DO recovery after loading: Increase minimum blower speed
  - Excessive DO overshooting: Tune PID parameters

#### Chemical Dosing Control
- **pH Control:**
  - Target: 7.0 pH
  - Control Method: PID control of acid/base dosing pumps
  - Maximum Rate of Change: 0.1 pH units per 15 minutes
  
- **Phosphorus Removal:**
  - Dosing ratio: 1.5-2.5 moles metal salt per mole of phosphorus
  - Control Method: Flow-paced with trim based on lab results
  - Adjustment frequency: Weekly based on effluent results

## Quality Management

### Sampling and Analysis

#### Sampling Locations
1. **Influent Channel**
   - Parameters: Flow, pH, Temperature, TSS, BOD₅
   - Frequency: Daily composite samples

2. **Primary Effluent**
   - Parameters: TSS, BOD₅
   - Frequency: Weekly composite samples

3. **Aeration Basin**
   - Parameters: MLSS, DO, Temperature
   - Frequency: Daily grab samples

4. **Secondary Effluent**
   - Parameters: TSS, BOD₅, Ammonia, Phosphorus
   - Frequency: Weekly composite samples

5. **Final Effluent**
   - Parameters: TSS, BOD₅, pH, Ammonia, Phosphorus, E. coli
   - Frequency: Daily composite samples

### Laboratory Testing Procedures
- All testing must follow approved Standard Methods
- QA/QC procedures must be followed including:
  - Regular calibration of lab equipment
  - Analysis of blank and duplicate samples
  - Use of control standards
  - Documentation of all results

### Record Keeping Requirements
- Daily operational logs
- Laboratory test results
- Calibration records
- Maintenance activities
- Non-compliance incidents
- Equipment failures
- Operator certifications

## Health, Safety, and Environmental Considerations

### Safety Requirements

#### Personal Protective Equipment (PPE)
- Required at all times in process areas:
  - Safety glasses
  - Steel-toed boots
  - Hard hat
  
- Required for specific tasks:
  - Chemical handling: Face shield, chemical-resistant gloves, apron
  - Confined space entry: Appropriate respiratory protection, harness, gas detector
  - High noise areas: Hearing protection

#### Hazardous Areas
- Chemical storage rooms: Verify ventilation before entry
- Confined spaces: Follow confined space entry procedures
- Electrical rooms: Only qualified personnel allowed entry

### Environmental Protection Measures

- Spill containment systems must be maintained and inspected regularly
- All chemical deliveries must be supervised
- Secondary containment must be in place for all chemical storage
- Stormwater runoff must be monitored for contamination
- Air emissions (including odors) must be controlled

## Reporting and Documentation

### Required Reports

#### Daily Reports
- Operational data summary
- Flow volumes (total and peak)
- Key process parameters
- Chemical usage
- Energy consumption
- Alarm events
- Maintenance activities performed

#### Monthly Reports
- Compliance with permit requirements
- Process performance statistics
- Chemical and energy consumption totals
- Maintenance summary
- Unusual events or conditions

#### Annual Reports
- Annual performance summary
- Major maintenance activities
- Capital improvements
- Staff training completed
- Compliance history

### Compliance Notifications
- Any permit exceedances must be reported to regulatory agencies within required timeframes
- Bypass or overflow events must be reported immediately
- Follow the facility's Regulatory Notification Protocol for all reportable events

## Appendices

### Contact Information
- Plant Manager: [Name], Phone: [Phone Number]
- Operations Supervisor: [Name], Phone: [Phone Number]
- Maintenance Supervisor: [Name], Phone: [Phone Number]
- Laboratory Manager: [Name], Phone: [Phone Number]
- Regulatory Agency: [Name], Phone: [Phone Number]
- Emergency Response: [Phone Number]

### Reference Documents
- Equipment manuals (located in control room)
- P&ID drawings (located in control room and engineering office)
- Facility NPDES permit
- Safety Data Sheets (located in laboratory and at chemical storage areas)
- Emergency Response Plan
- Standard Operating Procedures for specific equipment

### Revision History
| Revision | Date | Description | Approved By |
|----------|------|-------------|------------|
| 1.0 | June 8, 2025 | Initial release | [Name] |
