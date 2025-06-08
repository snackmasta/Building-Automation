# Car Parking Vending System - Technical Documentation

## Table of Contents
1. [System Overview](#system-overview)
2. [Architecture](#architecture)
3. [Hardware Specifications](#hardware-specifications)
4. [Software Components](#software-components)
5. [PLC Programming](#plc-programming)
6. [Communication Protocols](#communication-protocols)
7. [Database Design](#database-design)
8. [Safety Systems](#safety-systems)
9. [Installation Procedures](#installation-procedures)
10. [Maintenance Guidelines](#maintenance-guidelines)

## System Overview

### Purpose
The Car Parking Vending System is an automated industrial solution that operates like a vending machine for vehicles. It provides fully automated parking and retrieval services using advanced robotics, PLC control systems, and intelligent software management.

### Key Features
- **300 vehicle capacity** (15 levels × 20 spaces per level)
- **3 high-speed elevators** with independent operation
- **Robotic platforms** for vehicle positioning
- **Multi-modal payment processing** (cash, card, mobile, RFID)
- **Real-time monitoring** and management
- **Comprehensive safety systems**
- **Web and desktop HMI interfaces**
- **Advanced simulation capabilities**

### Performance Specifications
- **Vehicle entry time**: < 3 minutes
- **Vehicle retrieval time**: < 5 minutes
- **System availability**: 99.5% uptime
- **Throughput**: 120 vehicles/hour peak capacity
- **Safety integrity level**: SIL 2 compliant

## Architecture

### System Layers

#### 1. Physical Infrastructure Layer
- **Elevators**: 3× high-speed vertical transport systems
- **Robotic Platforms**: Precision vehicle positioning systems
- **Sensors**: Vehicle detection, dimension scanning, occupancy monitoring
- **Payment Kiosks**: Customer interface terminals
- **Safety Systems**: Emergency stops, fire detection, access control

#### 2. Control Layer
- **Main PLC**: Siemens S7-1500 series with redundancy
- **Safety PLC**: Siemens S7-1500F for safety functions
- **Elevator Controllers**: Dedicated motion control systems
- **Payment Controller**: Secure transaction processing unit
- **Parking Controller**: Space allocation and vehicle tracking

#### 3. Communication Layer
- **Ethernet/IP**: Primary industrial communication protocol
- **Modbus TCP**: Secondary PLC communication
- **OPC UA**: SCADA and MES integration
- **WebSocket**: Real-time web interface communication
- **WiFi**: Customer mobile device connectivity

#### 4. Application Layer
- **Database Manager**: SQLite with automatic backup
- **Simulation Engine**: Real-time system simulation
- **Communication Manager**: Protocol handling and message routing
- **System Utilities**: Monitoring, diagnostics, maintenance
- **Configuration Manager**: System parameter management

#### 5. User Interface Layer
- **Desktop HMI**: Python/Tkinter professional interface
- **Web HMI**: HTML5/JavaScript responsive interface
- **Mobile App**: Customer smartphone application
- **Customer Kiosk**: Touch-screen payment terminal
- **Admin Portal**: System administration interface

## Hardware Specifications

### PLC Systems

#### Main Controller
- **Model**: Siemens S7-1500 CPU 1516-3 PN/DP
- **Memory**: 1 MB work memory, 8 MB load memory
- **I/O Capacity**: 8,192 digital I/O, 1,024 analog I/O
- **Communication**: 2× Ethernet, 1× PROFIBUS DP
- **Cycle Time**: < 1 ms typical

#### Safety Controller
- **Model**: Siemens S7-1500F CPU 1516F-3 PN/DP
- **Safety Integrity**: SIL 3 / PL e
- **Safety I/O**: 512 fail-safe digital I/O
- **Reaction Time**: < 10 ms safety shutdown

### Elevator Systems

#### Specifications
- **Type**: Gearless traction elevators
- **Speed**: 2.5 m/s maximum
- **Load Capacity**: 3,000 kg per elevator
- **Travel Height**: 45 meters (15 levels × 3m)
- **Positioning Accuracy**: ±5 mm

#### Drive System
- **Motor**: Permanent magnet synchronous motor
- **Control**: Vector frequency drive with encoder feedback
- **Brake**: Electromagnetic safety brake system
- **Counterweight**: Optimized for vehicle loads

### Robotic Platform Systems

#### Specifications
- **Type**: AGV (Automated Guided Vehicle) platforms
- **Payload**: 3,000 kg maximum vehicle weight
- **Positioning**: Laser-guided navigation system
- **Speed**: 1.0 m/s maximum horizontal movement
- **Battery**: Li-ion with automatic charging stations

### Sensor Systems

#### Vehicle Detection
- **Entry/Exit**: Laser curtain sensors
- **Dimension Scanning**: 3D LIDAR system
- **Position Verification**: Ultrasonic sensors
- **Weight Measurement**: Load cells integrated in platforms

#### Safety Monitoring
- **Emergency Stops**: Category 4 safety circuits
- **Personnel Detection**: Safety laser scanners
- **Fire Detection**: Smoke and heat detectors
- **Environmental**: Temperature, humidity, air quality

## Software Components

### PLC Programming (Structured Text)

#### State Machine Architecture
```
PROGRAM Main_Controller
VAR
    current_state : SystemStates;
    previous_state : SystemStates;
    state_timer : TON;
    error_code : DINT;
END_VAR

CASE current_state OF
    INIT: (* System initialization *)
    IDLE: (* Waiting for vehicle *)
    PAYMENT: (* Processing payment *)
    ENTRY: (* Vehicle entering *)
    PARKING: (* Moving to space *)
    PARKED: (* Vehicle stored *)
    RETRIEVAL: (* Getting vehicle *)
    EXIT_SEQUENCE: (* Vehicle leaving *)
    MAINTENANCE: (* Service mode *)
    EMERGENCY: (* Emergency state *)
END_CASE
```

### Database Schema

#### Core Tables
- **vehicles**: Vehicle information and tracking
- **parking_spaces**: Space status and allocation
- **transactions**: Payment and billing records
- **system_events**: Operational logging
- **maintenance_records**: Service history
- **users**: System user management

### Communication Protocols

#### Protocol Stack
```
Application Layer    │ HMI, Database, Simulation
Presentation Layer   │ JSON, XML, Binary Serialization
Session Layer        │ Authentication, Session Management
Transport Layer      │ TCP, UDP, WebSocket
Network Layer        │ IP, Routing
Data Link Layer      │ Ethernet, WiFi
Physical Layer       │ Cat6 Cable, Fiber Optic
```

## Safety Systems

### Safety Integrity Level (SIL) 2 Compliance

#### Safety Functions
1. **Emergency Stop System**
   - Category 4 safety circuits
   - Redundant monitoring channels
   - Maximum reaction time: 500ms

2. **Personnel Protection**
   - Safety laser scanners at all access points
   - Interlocked access doors
   - Presence detection in vehicle areas

3. **Fire Safety**
   - Automatic sprinkler system
   - Smoke evacuation fans
   - Emergency lighting and egress

4. **Equipment Protection**
   - Overload monitoring
   - Position limit switches
   - Motor thermal protection

### Safety PLC Programming
```
FUNCTION_BLOCK Safety_Monitor
VAR_INPUT
    emergency_stops : ARRAY[1..10] OF BOOL;
    safety_gates : ARRAY[1..6] OF BOOL;
    fire_detectors : ARRAY[1..20] OF BOOL;
END_VAR

VAR_OUTPUT
    safety_ok : BOOL;
    emergency_stop_active : BOOL;
    fire_alarm_active : BOOL;
END_VAR

// Safety logic implementation
safety_ok := NOT (emergency_stop_active OR fire_alarm_active);
```

## Installation Procedures

### Pre-Installation Requirements

#### Site Preparation
1. **Foundation**: Reinforced concrete foundation capable of supporting 500 tons
2. **Electrical**: 480V 3-phase power, 500 kVA capacity
3. **Network**: Fiber optic backbone with redundant paths
4. **Environmental**: Climate-controlled equipment room

#### Utility Requirements
- **Power**: 480V 3-phase, 60Hz, 400A service
- **Network**: Gigabit Ethernet with fiber backbone
- **Compressed Air**: 6 bar, dry air for pneumatic systems
- **Water**: Fire suppression system connection

### Installation Sequence

#### Phase 1: Infrastructure (Weeks 1-4)
1. Install elevator shafts and rails
2. Mount structural steelwork
3. Install electrical distribution panels
4. Run network and communication cables

#### Phase 2: Mechanical Systems (Weeks 5-8)
1. Install elevator motors and drives
2. Mount robotic platform systems
3. Install safety barriers and gates
4. Commission pneumatic systems

#### Phase 3: Control Systems (Weeks 9-10)
1. Install PLC cabinets and I/O modules
2. Connect field devices and sensors
3. Configure network infrastructure
4. Load and test PLC programs

#### Phase 4: Software Integration (Weeks 11-12)
1. Install HMI software and databases
2. Configure communication protocols
3. Integrate payment systems
4. Perform system testing

#### Phase 5: Commissioning (Weeks 13-14)
1. Safety system verification
2. Performance testing
3. Operator training
4. Documentation handover

### Commissioning Checklist

#### Safety Verification
- [ ] Emergency stop system testing
- [ ] Safety interlock verification
- [ ] Fire detection system testing
- [ ] Personnel protection system check

#### Performance Testing
- [ ] Elevator speed and positioning accuracy
- [ ] Robotic platform navigation testing
- [ ] Payment system integration
- [ ] Communication system reliability

#### Software Validation
- [ ] Database integrity verification
- [ ] HMI functionality testing
- [ ] Simulation accuracy validation
- [ ] Backup and recovery procedures

## Maintenance Guidelines

### Preventive Maintenance Schedule

#### Daily Checks
- [ ] Visual inspection of all systems
- [ ] Safety system status verification
- [ ] Review system event logs
- [ ] Check elevator operation

#### Weekly Maintenance
- [ ] Robotic platform battery status
- [ ] Sensor cleaning and calibration
- [ ] Network connectivity testing
- [ ] Database backup verification

#### Monthly Maintenance
- [ ] Elevator inspection and lubrication
- [ ] Safety system functional testing
- [ ] Comprehensive system diagnostics
- [ ] Performance metrics analysis

#### Annual Maintenance
- [ ] Complete safety system recertification
- [ ] Elevator modernization assessment
- [ ] Software updates and patches
- [ ] Hardware lifecycle planning

### Troubleshooting Procedures

#### Common Issues

**Issue**: Vehicle entry timeout
- **Cause**: Sensor malfunction or vehicle positioning
- **Solution**: Check sensor alignment, verify vehicle dimensions
- **Prevention**: Regular sensor calibration

**Issue**: Elevator positioning error
- **Cause**: Encoder drift or mechanical wear
- **Solution**: Recalibrate position feedback, inspect mechanical components
- **Prevention**: Monthly positioning accuracy checks

**Issue**: Communication timeout
- **Cause**: Network congestion or hardware failure
- **Solution**: Check network connectivity, restart communication services
- **Prevention**: Network monitoring and redundant paths

### Spare Parts Inventory

#### Critical Components
- PLC processor modules (2 units)
- I/O modules (10% of installed quantity)
- Elevator drive components (1 complete set)
- Safety relay modules (4 units)
- Network switches (2 units)

#### Consumable Items
- Sensor cleaning supplies
- Lubrication oils and greases
- Elevator brake pads
- UPS batteries
- Cable assemblies

## Performance Optimization

### Key Performance Indicators

#### Operational Metrics
- **Vehicle Throughput**: Target 120 vehicles/hour peak
- **Average Entry Time**: Target < 3 minutes
- **Average Retrieval Time**: Target < 5 minutes
- **System Availability**: Target 99.5% uptime

#### Efficiency Metrics
- **Space Utilization**: Target 95% occupied during peak hours
- **Energy Consumption**: Monitor kWh per vehicle transaction
- **Maintenance Costs**: Track as percentage of revenue
- **Customer Satisfaction**: Survey-based scoring

### Optimization Strategies

#### Traffic Management
- Dynamic space allocation algorithms
- Predictive vehicle retrieval
- Load balancing across elevators
- Queue management during peak times

#### Energy Efficiency
- Regenerative elevator drives
- LED lighting with occupancy sensors
- Variable speed HVAC systems
- Standby mode for idle equipment

---

*Document Version: 1.0*  
*Last Updated: June 8, 2025*  
*Prepared by: PLC Engineering Team*
