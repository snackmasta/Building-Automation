# Wastewater Treatment Plant System Documentation

**Document Number:** WWTP-SD-001  
**Revision:** 1.0  
**Date:** June 8, 2025  

## Table of Contents
1. [System Overview](#system-overview)
2. [Hardware Architecture](#hardware-architecture)
3. [Software Architecture](#software-architecture)
4. [Control Systems](#control-systems)
5. [Communication Networks](#communication-networks)
6. [Data Management](#data-management)
7. [Security](#security)
8. [Integration Points](#integration-points)
9. [Technical Specifications](#technical-specifications)
10. [Revision History](#revision-history)

## System Overview

The Wastewater Treatment Plant (WWTP) automation system provides comprehensive monitoring and control for all aspects of the wastewater treatment process. The system is designed to optimize treatment efficiency, ensure regulatory compliance, minimize energy consumption, and provide operators with clear visibility into all process parameters.

### System Purpose
- Automate routine operations of the wastewater treatment plant
- Monitor all critical process parameters in real-time
- Control treatment processes to meet effluent quality requirements
- Detect and respond to abnormal conditions
- Collect and store operational data for reporting and analysis
- Provide operators with intuitive interfaces for process supervision
- Support remote monitoring and operation

### System Scope
The automation system covers the following treatment processes:
- Intake and preliminary treatment (screening, grit removal)
- Primary treatment (sedimentation)
- Secondary treatment (biological processing)
- Chemical treatment (pH adjustment, nutrient removal)
- Disinfection (UV or chemical)
- Sludge handling
- Support systems (blowers, pumps, chemical dosing)

## Hardware Architecture

### Control Hardware

#### Programmable Logic Controllers (PLCs)
- **Main Process PLC**
  - Model: Siemens S7-1500
  - CPU: 1516-3 PN/DP
  - Memory: 5 MB work memory
  - Location: Main Control Panel (MCP-001)
  - Function: Primary process control, coordination of all subsystems

- **Intake System PLC**
  - Model: Siemens S7-1200
  - CPU: 1214C DC/DC/DC
  - Memory: 100 KB work memory
  - Location: Intake Building Panel (IBP-001)
  - Function: Control of screening and grit removal

- **Chemical Treatment PLC**
  - Model: Siemens S7-1200
  - CPU: 1215C DC/DC/DC
  - Memory: 125 KB work memory
  - Location: Chemical Building Panel (CBP-001)
  - Function: Chemical dosing and monitoring

#### I/O Modules
Total I/O Count: 
- Digital Inputs: 256
- Digital Outputs: 128
- Analog Inputs: 64
- Analog Outputs: 32

| Module Location | Module Type | Inputs/Outputs | Signals |
|-----------------|-------------|----------------|---------|
| MCP-001 Rack 0 | DI 32xDC 24V | 32 DI | Emergency stops, equipment status, valve positions |
| MCP-001 Rack 0 | DO 32xDC 24V | 32 DO | Valve actuators, motor starters, alarm outputs |
| MCP-001 Rack 0 | AI 8xRTD/TC | 8 AI | Temperature sensors |
| MCP-001 Rack 0 | AI 8x13bit | 8 AI | Level transmitters, pressure transmitters |
| MCP-001 Rack 0 | AO 4x13bit | 4 AO | Variable frequency drives, modulating valves |
| MCP-001 Rack 1 | DI 32xDC 24V | 32 DI | Equipment status, valve positions |
| MCP-001 Rack 1 | DO 16xDC 24V | 16 DO | Motor starters, indication lights |
| IBP-001 Rack 0 | DI 16xDC 24V | 16 DI | Screen status, grit pump status |
| IBP-001 Rack 0 | DO 16xDC 24V | 16 DO | Screen controls, grit pump controls |
| IBP-001 Rack 0 | AI 8x13bit | 8 AI | Flow transmitters, level transmitters |
| CBP-001 Rack 0 | DI 16xDC 24V | 16 DI | Tank levels, pump status |
| CBP-001 Rack 0 | DO 16xDC 24V | 16 DO | Dosing pump controls, mixer controls |
| CBP-001 Rack 0 | AI 8x13bit | 8 AI | pH, flow, level transmitters |
| CBP-001 Rack 0 | AO 4x13bit | 4 AO | Chemical dosing pumps |

#### Network Hardware
- **Industrial Ethernet Switches**
  - Model: Cisco IE-4000-8GT4G-E
  - Quantity: 4
  - Locations: MCP-001, IBP-001, CBP-001, Admin Building
  - Function: Network backbone for control system

- **Wireless Access Points**
  - Model: Cisco IW3702-2E-UXK9
  - Quantity: 2
  - Locations: Main Process Building, Outdoor Tank Farm
  - Function: Tablet access for operators, maintenance staff

#### Servers and Workstations
- **SCADA Server**
  - Hardware: Dell PowerEdge R740, redundant power supplies
  - Processor: Intel Xeon Gold 6248R, 24 cores
  - Memory: 64GB RAM
  - Storage: 4TB RAID 5 configuration (6x 1TB SSD)
  - OS: Windows Server 2022
  - Location: Server Room (climate controlled)

- **Historian Server**
  - Hardware: Dell PowerEdge R740, redundant power supplies
  - Processor: Intel Xeon Gold 6242R, 20 cores
  - Memory: 64GB RAM
  - Storage: 12TB RAID 5 configuration (6x 4TB SSD)
  - OS: Windows Server 2022
  - Location: Server Room (climate controlled)

- **Operator Workstations**
  - Hardware: Dell Precision 3660
  - Processor: Intel Core i7-12700
  - Memory: 32GB RAM
  - Storage: 1TB SSD
  - OS: Windows 11 Professional
  - Monitors: Dual 24" 1920x1080
  - Quantity: 3
  - Locations: Control Room (2), Supervisor Office (1)

### Field Instrumentation

#### Flow Measurement
- **Raw Wastewater Flow**
  - Instrument: Magnetic Flow Meter
  - Model: Endress+Hauser Proline Promag W400
  - Quantity: 1
  - Range: 0-500 m³/hr
  - Output: 4-20mA HART
  - Location: Intake Structure

- **Process Flow Meters**
  - Instrument: Magnetic Flow Meter
  - Model: Endress+Hauser Proline Promag W300
  - Quantity: 5
  - Ranges: Various (50-300 m³/hr)
  - Output: 4-20mA HART
  - Locations: Primary effluent, RAS, WAS, Final effluent

#### Level Measurement
- **Tank Level Transmitters**
  - Instrument: Ultrasonic Level Transmitter
  - Model: Endress+Hauser Prosonic FMU90
  - Quantity: 8
  - Range: 0-10m
  - Output: 4-20mA HART
  - Locations: Various tanks and basins

- **Wet Well Level**
  - Instrument: Radar Level Transmitter
  - Model: Endress+Hauser Micropilot FMR20
  - Quantity: 2
  - Range: 0-8m
  - Output: 4-20mA HART
  - Locations: Influent wet well, effluent wet well

#### Analytical Instrumentation
- **pH Analyzers**
  - Model: Endress+Hauser Liquiline CM442
  - Sensor: Orbisint CPS11D
  - Quantity: 4
  - Range: 0-14 pH
  - Output: 4-20mA HART + Modbus TCP
  - Locations: Influent, chemical treatment, aeration basin, effluent

- **Dissolved Oxygen**
  - Model: Endress+Hauser Liquiline CM442
  - Sensor: Oxymax COS51D
  - Quantity: 3
  - Range: 0-20 mg/L
  - Output: 4-20mA HART + Modbus TCP
  - Locations: Aeration basins (3 zones)

- **Turbidity**
  - Model: Hach TU5300sc
  - Quantity: 2
  - Range: 0-1000 NTU
  - Output: 4-20mA + Modbus RTU
  - Locations: Primary effluent, final effluent

- **Ammonia Analyzer**
  - Model: Hach Amtax sc
  - Quantity: 2
  - Range: 0.05-20 mg/L NH₄-N
  - Output: 4-20mA + Modbus RTU
  - Locations: Aeration basin effluent, final effluent

- **Chlorine Residual Analyzer**
  - Model: Hach CL17sc
  - Quantity: 1
  - Range: 0-5 mg/L
  - Output: 4-20mA + Modbus RTU
  - Location: Effluent channel

#### Process Actuation
- **Large Valve Actuators**
  - Model: AUMA SA .2 with AC controls
  - Quantity: 12
  - Communication: Profibus DP
  - Sizes: DN100-DN300
  - Locations: Various process areas

- **Small Valve Actuators**
  - Model: AUMA SQ .2 with AC controls
  - Quantity: 24
  - Communication: 24VDC control
  - Sizes: DN25-DN80
  - Locations: Various process areas

- **Variable Frequency Drives**
  - Model: ABB ACS880
  - Quantity: 18
  - Communication: Profinet
  - Power Ranges: 5.5kW to 75kW
  - Locations: Various pump and blower applications

## Software Architecture

### SCADA System
- **Software Platform:** Wonderware System Platform 2023
- **Components:**
  - InTouch HMI
  - Application Server
  - Historian
  - Information Server
  - Alarm Provider
  - Recipe Manager
- **Number of Tags:** Approximately 2,500
- **Clients:**
  - 3 Operator Workstations
  - 2 Engineering Workstations
  - 1 Remote Web Client Server

### PLC Software
- **Programming Software:** Siemens TIA Portal V17
- **Programming Languages:**
  - Structured Text (ST) - Primary language
  - Function Block Diagram (FBD) - For control loops
  - Ladder Diagram (LD) - For interlocks and discrete logic
- **Program Structure:**
  - Global variable definitions
  - Main control program
  - Subsystem-specific controllers (intake, treatment, dosing, aeration, monitoring)
  - Standardized function blocks for common equipment
  - Alarm handling routines
  - Communication interfaces

### Database System
- **Platform:** Microsoft SQL Server 2022
- **Databases:**
  - Process Historian Database
  - Laboratory Information Management System (LIMS)
  - Maintenance Management Database
  - Reporting Database
- **Integration:** ETL processes for data consolidation

### HMI Design
- **Standards:** ISA-101 HMI Design
- **Color Scheme:** Grey background with color highlighting for alarms and status
- **Screen Hierarchy:**
  - Level 1: Plant Overview
  - Level 2: Process Area Overviews
  - Level 3: Equipment Detail Screens
  - Level 4: Diagnostic and Configuration Screens
- **Navigation:** Tab-based system with persistent alarm banner

### Custom Applications
- **Report Generator**
  - Platform: .NET C#
  - Function: Automated regulatory and operational reports
  - Data Source: SQL Server databases

- **Trend Viewer**
  - Platform: HTML5/JavaScript
  - Function: Advanced analysis of historical process data
  - Features: Multi-pen plotting, statistical analysis, export capabilities

- **Mobile Operator Interface**
  - Platform: HTML5 Responsive Web Application
  - Function: Limited monitoring and control via tablets
  - Security: Role-based access control, secure authentication

## Control Systems

### Control Philosophy
The WWTP control system follows a hierarchical structure:
1. **Safety Interlocks** - Highest priority, implemented in hardware and software
2. **Equipment Protection** - Prevents damage to machinery and infrastructure
3. **Process Control** - Maintains setpoints for optimal treatment
4. **Process Optimization** - Adjusts parameters for efficiency and cost savings
5. **Monitoring and Reporting** - Records performance data for analysis and compliance

### Control Loop Details

#### Flow Control Loops

| Loop ID | Description | Process Variable | Control Element | Control Strategy |
|---------|-------------|------------------|-----------------|------------------|
| FC-101 | Influent Flow Control | FT-101 | VFD-101/102 (Influent Pumps) | PID with rate limiting |
| FC-201 | RAS Flow Control | FT-201 | VFD-201/202 (RAS Pumps) | Ratio control based on influent flow |
| FC-202 | WAS Flow Control | FT-202 | VFD-203 (WAS Pump) | Time-based operation with flow totalization |

#### Level Control Loops

| Loop ID | Description | Process Variable | Control Element | Control Strategy |
|---------|-------------|------------------|-----------------|------------------|
| LC-101 | Wet Well Level Control | LT-101 | Influent Pumps | PID with multiple setpoints based on conditions |
| LC-201 | Primary Clarifier Level | LT-201 | CV-201 (Effluent Valve) | On/Off control with deadband |
| LC-301 | Aeration Basin Level | LT-301 | CV-301 (Effluent Valve) | PID with anti-windup |

#### Analytical Control Loops

| Loop ID | Description | Process Variable | Control Element | Control Strategy |
|---------|-------------|------------------|-----------------|------------------|
| AC-101 | pH Control | AT-101 (pH) | Acid/Base Dosing Pumps | PID with deadband |
| AC-201 | Dissolved Oxygen Control | AT-201/202/203 (DO) | Blower Speed + Air Valves | Cascaded PID with multi-zone control |
| AC-301 | Chemical Phosphorus Removal | AT-301 (Phosphorus) | Chemical Dosing Pumps | Flow-paced with trim |

### Interlocks and Permissives

#### Equipment Interlocks
- Pumps will not run if suction/discharge valves closed
- Blowers require minimum speed for cooling
- Chemical pumps will not operate without flow verification
- UV system requires flow verification before activation

#### Safety Interlocks
- High level switches trigger alarm and pump activation
- Low level switches prevent pump dry-running
- High pressure switches shut down affected systems
- Gas detection triggers ventilation and alarms
- Emergency stop halts all non-critical equipment

### Control Modes

#### Auto Mode
The standard operating mode where the PLC controls all processes according to programmed setpoints and algorithms.

#### Manual Mode
Operators can directly command equipment while safety interlocks remain active. Used for maintenance and testing.

#### Maintenance Mode
Special operating mode that allows bypassing of certain process interlocks while maintaining basic safety interlocks. Requires supervisor authorization.

#### Storm Mode
Activated during high flow events, implementing alternate control strategies to handle excessive flows while maintaining critical treatment steps.

## Communication Networks

### Network Architecture
The system utilizes a hierarchical network structure with segmentation for security and reliability:

1. **Control Network (Layer 1)**
   - Protocol: Industrial Ethernet (PROFINET)
   - Speed: 1 Gbps
   - Devices: PLCs, Remote I/O, VFDs, Intelligent Field Devices
   - Topology: Ring structure with redundancy
   - Security: Physically isolated, no direct external access

2. **Supervisory Network (Layer 2)**
   - Protocol: Ethernet TCP/IP
   - Speed: 1 Gbps
   - Devices: SCADA Servers, Operator Workstations, Engineering Workstations
   - Topology: Star with redundant switches
   - Security: Firewall protected, limited external access

3. **Business Network (Layer 3)**
   - Protocol: Ethernet TCP/IP
   - Speed: 10 Gbps
   - Devices: Report Servers, Management Workstations, Business Systems
   - Topology: Enterprise IT infrastructure
   - Security: Standard IT security measures

4. **Wireless Network**
   - Protocol: IEEE 802.11ac
   - Speed: Up to 1.3 Gbps
   - Devices: Operator Tablets, Maintenance Devices
   - Security: WPA3-Enterprise, RADIUS authentication

### Protocols

- **PROFINET** - Primary fieldbus for PLC and I/O communication
- **Modbus TCP** - Secondary protocol for certain field devices
- **HART-IP** - For advanced diagnostics from smart transmitters
- **OPC UA** - Interface between control and supervisory layers
- **MQTT** - For IoT device integration and lightweight messaging
- **SQL** - Database access and integration
- **HTTPS** - Secure web services for reporting and remote access

### Field Device Networks
- **PROFIBUS DP** - Legacy valve actuators
- **HART** - Smart transmitters with 4-20mA + digital
- **Foundation Fieldbus** - Analytical instruments

## Data Management

### Historian Configuration
- **Tag Count:** Approximately 2,500
- **Collection Rate:** 
  - Critical process variables: 1 second
  - Standard process variables: 5 seconds
  - Slow-changing values: 60 seconds
- **Storage Policy:**
  - Full resolution for 90 days
  - 5-minute averages for 1 year
  - Hourly averages for 5 years
  - Daily averages permanently archived
- **Compression Settings:** Swinging door compression algorithm, 0.5% deviation

### Data Flows
1. **Process Data Collection**
   - From: Field instruments → PLCs → SCADA
   - To: Real-time displays, Historian
   - Frequency: Real-time (1-60 seconds depending on criticality)

2. **Laboratory Data**
   - From: LIMS
   - To: SCADA, Reporting Database
   - Frequency: As tests are completed (typically daily)

3. **Compliance Reporting**
   - From: Historian, LIMS
   - To: Regulatory reporting system
   - Frequency: Monthly automated reports, additional ad-hoc

4. **Energy Monitoring**
   - From: Power monitors, VFDs, equipment runtime
   - To: Energy management system
   - Frequency: 15-minute intervals

### Data Backup Strategy
- **SCADA and Historian:**
  - Daily incremental backups
  - Weekly full backups
  - Monthly archives to offsite storage
  - Retention: 7 years

- **PLC Programs:**
  - Version-controlled repository
  - Backup after any change
  - Monthly verification against running program
  - Offsite storage of critical versions

- **Configuration Files:**
  - Version-controlled repository
  - Documentation of all changes
  - Backup of working configurations before modifications

## Security

### Access Control

#### Physical Access
- **Control Room:** Card access + PIN
- **PLC Panels:** Keyed locks, tamper switches
- **Server Room:** Card access + biometric
- **Network Equipment:** Locked cabinets

#### System Access
- **Role-Based Security:**
  - Viewer: Read-only access to displays
  - Operator: Control capabilities within normal parameters
  - Supervisor: Extended control capabilities, setpoint adjustments
  - Engineer: Configuration changes, program modifications
  - Administrator: Full system access

- **Authentication:**
  - Individual user accounts (no shared logins)
  - Complex password requirements
  - Multi-factor authentication for remote access
  - Automatic logout after inactivity

### Network Security
- **Segmentation:** Network separation via VLANs and firewalls
- **Firewall Rules:** Explicit allow-list approach, deny by default
- **VPN:** Encrypted connections for all remote access
- **Intrusion Detection:** Monitoring for unauthorized access attempts
- **Traffic Filtering:** Deep packet inspection for control protocols

### Update Management
- **Security Patches:**
  - Tested in development environment
  - Applied during scheduled maintenance windows
  - Documented approval process
  - Rollback capability

- **Antivirus/Endpoint Protection:**
  - Whitelisting approach for control systems
  - Regular signature updates
  - Scheduled scans during off-peak hours

### Security Monitoring
- **Audit Logging:**
  - All user actions tracked
  - System configuration changes logged
  - Access attempts recorded
  - Logs stored for 1 year

- **Incident Response:**
  - Documented procedures for security events
  - Escalation paths defined
  - Recovery strategies prepared

## Integration Points

### Laboratory Information Management System (LIMS)
- **Integration Type:** Web Services (REST API)
- **Data Exchange:**
  - Sample schedules from SCADA to LIMS
  - Test results from LIMS to SCADA
  - Compliance calculations and alerts
- **Frequency:** Hourly synchronization

### Maintenance Management System
- **Integration Type:** Database link
- **Data Exchange:**
  - Equipment runtime from SCADA to Maintenance System
  - Equipment status and alarms to trigger work orders
  - Maintenance schedules to SCADA for operator notification
- **Frequency:** Daily synchronization, immediate for critical alarms

### Weather Monitoring System
- **Integration Type:** Web Services (REST API)
- **Data Exchange:**
  - Current conditions and forecasts
  - Rainfall data for flow prediction
  - Storm warnings for operational preparation
- **Frequency:** 15-minute updates

### Energy Management System
- **Integration Type:** OPC UA
- **Data Exchange:**
  - Power consumption by equipment and area
  - Demand response signals
  - Energy optimization recommendations
- **Frequency:** Real-time for critical equipment, 15-minute intervals for trends

### Regulatory Reporting System
- **Integration Type:** Database extract and file transfer
- **Data Exchange:**
  - Compliance data formatted for regulatory submissions
  - Violation notifications and alerts
  - Historical compliance records
- **Frequency:** Monthly automated reports, immediate notifications for exceedances

## Technical Specifications

### Performance Requirements
- **System Response Time:** < 2 seconds for operator commands
- **Screen Update Rate:** ≤ 1 second
- **Control Loop Execution:** ≤ 100ms for critical loops
- **Alarm Response:** < 1 second from event to display
- **Historian Storage Capacity:** Minimum 5 years of full data
- **System Availability:** 99.9% uptime (less than 9 hours downtime per year)

### Redundancy Features
- **SCADA Servers:** Hot standby configuration with automatic failover
- **Networks:** Redundant paths with rapid spanning tree recovery
- **Controllers:** Primary PLC with hot standby for critical process areas
- **Power:** UPS for all control system components, backup generator for facility

### Regulatory Compliance
- **Environmental:**
  - EPA Clean Water Act requirements
  - State-specific discharge permits
  - Local watershed protection ordinances

- **Technical Standards:**
  - ISA-18.2 for alarm management
  - ISA-101 for HMI design
  - ISA-99/IEC 62443 for security
  - 21 CFR Part 11 for electronic records (where applicable)

## Revision History
| Revision | Date | Description | Approved By |
|----------|------|-------------|------------|
| 1.0 | June 8, 2025 | Initial release | [Name] |
