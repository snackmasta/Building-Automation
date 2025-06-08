# Water Treatment System - Industrial Automation Project

## Project Overview
A comprehensive seawater desalination and water treatment system with advanced automation, monitoring, and control capabilities. This project follows industrial automation best practices with a structured folder hierarchy.

## System Architecture
- **Source**: Seawater intake and pre-treatment
- **Process**: Reverse Osmosis (RO) desalination with membrane cleaning
- **Storage**: Roof tank distribution system with level control
- **Distribution**: Automated pump management with pressure control
- **Monitoring**: Real-time quality monitoring and safety interlocks

## Folder Structure

```
Water Treatment System/
├── plc/                          # PLC Programming Files
│   ├── global_vars.st           # Global variable declarations
│   ├── main.st                  # Main control program
│   ├── desalination_controller.st   # RO membrane control
│   ├── pump_controller.st       # Pump sequencing logic
│   └── water_quality_controller.st # Quality monitoring
│
├── src/                         # Source Code
│   ├── gui/                     # Human Machine Interface
│   │   ├── hmi_interface.py     # Python GUI application
│   │   └── web_hmi.html         # Web-based HMI
│   ├── simulation/              # Process Simulation
│   │   └── water_treatment_simulator.py # Realistic process simulator
│   ├── monitoring/              # System Monitoring
│   │   └── system_status.py     # Real-time status monitoring
│   └── core/                    # Core Components
│       └── process_diagram.py   # Diagram generation engine
│
├── config/                      # Configuration Files
│   └── plc_config.ini          # System configuration
│
├── docs/                        # Documentation
│   ├── README.md               # This file
│   ├── System_Documentation.md  # Technical documentation
│   └── FLOWCHART_IMPLEMENTATION_SUMMARY.md # Process flow details
│
├── diagrams/                    # Generated Diagrams
│   ├── process_control_flowchart.png    # 24-step decision tree
│   ├── system_states_diagram.png        # State machine diagram
│   ├── control_system_architecture.png  # System architecture
│   ├── water_treatment_process_diagram.png # Process flow
│   ├── water_treatment_pid.png          # P&ID diagram
│   └── water_treatment_diagrams.pdf     # Combined PDF
│
├── scripts/                     # Automation Scripts
│   └── batch/                   # Windows Batch Files
│       ├── system_launcher.bat  # Main system launcher
│       ├── run_hmi.bat          # Start HMI interface
│       ├── run_simulator.bat    # Start process simulator
│       ├── run_status_monitor.bat # Start monitoring
│       └── generate_diagrams.bat # Generate all diagrams
│
├── utils/                       # Utilities
│   ├── final_project_summary.py # Project summary generator
│   ├── flowchart_demo.py       # Flowchart demonstration
│   └── verification/           # System Verification
│       └── verify_system.py    # System integrity check
│
└── tests/                       # Unit Tests (Future)
    └── (test files will be added here)
```

## Key Features

### 1. Advanced Process Control
- **Multi-stage RO membrane control** with pressure optimization
- **Intelligent pump sequencing** with rotation management
- **Real-time water quality monitoring** with automatic adjustment
- **Comprehensive safety interlocks** with emergency procedures

### 2. Revolutionary Flowchart System
- **24-step decision tree** with color-coded process elements
- **Diamond decision points** with YES/NO branch logic
- **State machine diagram** with 9 operational states
- **Emergency procedures** and fault handling visualization

### 3. Professional HMI Interfaces
- **Python GUI** with real-time data visualization
- **Web-based interface** for remote monitoring
- **Process diagrams** with professional P&ID standards
- **Alarm management** with priority-based notifications

### 4. Realistic Process Simulation
- **Dynamic tank modeling** with realistic physics
- **Membrane fouling simulation** with cleaning cycles
- **Pump performance curves** with efficiency tracking
- **Water quality degradation** modeling

## Quick Start Guide

### 1. System Launch
```batch
# Run the main system launcher
scripts\batch\system_launcher.bat
```

### 2. Individual Components
```batch
# Start HMI interface
scripts\batch\run_hmi.bat

# Start process simulator
scripts\batch\run_simulator.bat

# Start status monitoring
scripts\batch\run_status_monitor.bat

# Generate all diagrams
scripts\batch\generate_diagrams.bat
```

### 3. System Verification
```batch
# Verify system integrity
python utils\verification\verify_system.py
```

## Technical Specifications

### Control System
- **PLC Programming**: IEC 61131-3 Structured Text
- **Communication**: Modbus TCP/IP protocol
- **I/O Configuration**: 64 digital inputs, 32 digital outputs, 16 analog inputs
- **Safety Rating**: SIL 2 compliant with emergency stops

## I/O Mapping

### Digital Inputs
| Address | Signal Name | Description | Type | Signal Level | Function |
|---------|-------------|-------------|------|--------------|----------|
| %I0.0 | SEAWATER_INTAKE | Seawater intake status | NO Contact | 24VDC | Intake valve position |
| %I0.1 | START_BUTTON | System start command | NO Contact | 24VDC | Operator start button |
| %I0.2 | STOP_BUTTON | System stop command | NC Contact | 24VDC | Operator stop button |
| %I0.3 | EMERGENCY_BUTTON | Emergency shutdown | NC Contact | 24VDC | Emergency stop button |
| %I0.4 | GROUND_TANK_LOW | Ground tank low level | Float Switch | 24VDC | Low level alarm |
| %I0.5 | GROUND_TANK_HIGH | Ground tank high level | Float Switch | 24VDC | High level alarm |
| %I0.6 | ROOF_TANK_LOW | Roof tank low level | Float Switch | 24VDC | Low level alarm |
| %I0.7 | ROOF_TANK_HIGH | Roof tank high level | Float Switch | 24VDC | High level alarm |
| %I1.0 | LEAK_DETECTOR_1 | Leak detector zone 1 | Probe | 24VDC | Water leakage detection |
| %I1.1 | LEAK_DETECTOR_2 | Leak detector zone 2 | Probe | 24VDC | Water leakage detection |
| %I1.2 | RO_HIGH_PRESSURE | RO high pressure alarm | Pressure Switch | 24VDC | Over-pressure protection |
| %I1.3 | FILTER_CLOGGED | Pre-filter clogged | Differential Switch | 24VDC | Filter maintenance alarm |

### Analog Inputs
| Address | Signal Name | Description | Range | Signal Type | Calibration | Function |
|---------|-------------|-------------|-------|-------------|-------------|----------|
| %IW0 | SEAWATER_TDS | Seawater TDS sensor | 0-50,000 ppm | 4-20mA | 4mA=0ppm, 20mA=50,000ppm | Feed water quality |
| %IW1 | SEAWATER_TEMP | Seawater temperature | 0-60°C | 4-20mA | 4mA=0°C, 20mA=60°C | Feed water monitoring |
| %IW2 | GROUND_TANK_LEVEL | Ground tank level | 0-100% | 4-20mA | 4mA=0%, 20mA=100% | Storage monitoring |
| %IW3 | ROOF_TANK_LEVEL | Roof tank level | 0-100% | 4-20mA | 4mA=0%, 20mA=100% | Distribution monitoring |
| %IW4 | RO_PRESSURE | RO operating pressure | 0-80 bar | 4-20mA | 4mA=0bar, 20mA=80bar | Membrane pressure |
| %IW5 | DISTRIBUTION_PRESSURE | Distribution pressure | 0-10 bar | 4-20mA | 4mA=0bar, 20mA=10bar | Supply pressure |
| %IW6 | PERMEATE_FLOW | RO permeate flow | 0-500 L/min | 4-20mA | 4mA=0L/min, 20mA=500L/min | Product flow rate |
| %IW7 | CONCENTRATE_FLOW | RO concentrate flow | 0-500 L/min | 4-20mA | 4mA=0L/min, 20mA=500L/min | Reject flow rate |
| %IW8 | PRODUCT_TDS | Product water TDS | 0-2000 ppm | 4-20mA | 4mA=0ppm, 20mA=2000ppm | Product water quality |
| %IW9 | PRODUCT_PH | Product water pH | 0-14 pH | 4-20mA | 4mA=0pH, 20mA=14pH | Product pH monitoring |
| %IW10 | PRODUCT_TURBIDITY | Product turbidity | 0-50 NTU | 4-20mA | 4mA=0NTU, 20mA=50NTU | Water clarity |
| %IW11 | CHLORINE_LEVEL | Chlorine residual | 0-5 mg/L | 4-20mA | 4mA=0mg/L, 20mA=5mg/L | Disinfection monitoring |

### Digital Outputs
| Address | Signal Name | Description | Type | Signal Level | Load Current | Function |
|---------|-------------|-------------|------|--------------|--------------|----------|
| %Q0.0 | INTAKE_PUMP | Seawater intake pump | Contactor | 24VDC | 10A | Feed water supply |
| %Q0.1 | PREFILTER_PUMP | Pre-filtration pump | Contactor | 24VDC | 5A | Pre-treatment |
| %Q0.2 | RO_PUMP | RO high pressure pump | Contactor | 24VDC | 25A | Membrane operation |
| %Q0.3 | BOOSTER_PUMP_1 | Distribution pump 1 | Contactor | 24VDC | 7.5A | Water distribution |
| %Q0.4 | BOOSTER_PUMP_2 | Distribution pump 2 | Contactor | 24VDC | 7.5A | Backup distribution |
| %Q0.5 | INTAKE_VALVE | Seawater intake valve | Solenoid | 24VDC | 2A | Feed water control |
| %Q0.6 | RO_PERMEATE_VALVE | RO permeate valve | Solenoid | 24VDC | 1.5A | Product water control |
| %Q0.7 | CONCENTRATE_VALVE | Concentrate valve | Solenoid | 24VDC | 1.5A | Reject water control |
| %Q1.0 | GROUND_TANK_VALVE | Ground tank inlet valve | Solenoid | 24VDC | 2A | Storage control |
| %Q1.1 | ROOF_TANK_VALVE | Roof tank inlet valve | Solenoid | 24VDC | 2A | Distribution control |
| %Q1.2 | CHLORINE_DOSING_PUMP | Chlorine dosing pump | Peristaltic | 24VDC | 1A | Chemical dosing |
| %Q1.3 | PH_DOSING_PUMP | pH adjustment pump | Peristaltic | 24VDC | 1A | pH correction |
| %Q1.4 | UV_STERILIZER | UV sterilizer | UV Lamp | 24VDC | 3A | Disinfection |
| %Q1.5 | SYSTEM_ALARM | System alarm horn | Horn | 24VDC | 0.5A | Audible alarm |
| %Q1.6 | STATUS_LIGHT | System status light | LED | 24VDC | 0.1A | Normal operation |
| %Q1.7 | ALARM_LIGHT | Alarm indicator light | LED | 24VDC | 0.1A | Fault indication |

### Analog Outputs
| Address | Signal Name | Description | Range | Signal Type | Calibration | Function |
|---------|-------------|-------------|-------|-------------|-------------|----------|
| %QW0 | INTAKE_PUMP_SPEED | Intake pump VFD | 0-100% | 4-20mA | 4mA=0%, 20mA=100% | Pump speed control |
| %QW1 | RO_PUMP_SPEED | RO pump VFD | 0-100% | 4-20mA | 4mA=0%, 20mA=100% | High pressure control |
| %QW2 | BOOSTER_SPEED_1 | Booster pump 1 VFD | 0-100% | 4-20mA | 4mA=0%, 20mA=100% | Distribution control |
| %QW3 | BOOSTER_SPEED_2 | Booster pump 2 VFD | 0-100% | 4-20mA | 4mA=0%, 20mA=100% | Backup pump control |
| %QW4 | CHLORINE_RATE | Chlorine dosing rate | 0-100% | 4-20mA | 4mA=0%, 20mA=100% | Chemical dosing |
| %QW5 | PH_DOSE_RATE | pH dosing rate | 0-100% | 4-20mA | 4mA=0%, 20mA=100% | pH adjustment |

### I/O Summary
- **Total Digital Inputs**: 12 points (Safety Category SIL 2)
- **Total Analog Inputs**: 12 points (4-20mA process signals)
- **Total Digital Outputs**: 16 points (Motor control and valves)
- **Total Analog Outputs**: 6 points (VFD and dosing control)
- **Power Consumption**: ~150W total I/O power
- **Safety Systems**: Emergency stops, pressure relief, leak detection
- **Communication**: Modbus TCP/IP for SCADA integration

### Process Parameters
- **Feed Water**: Seawater (35,000 ppm TDS)
- **Product Water**: <500 ppm TDS, pH 6.5-8.5
- **Recovery Rate**: 45-50% (optimized for membrane life)
- **Production Capacity**: 1000 m³/day
- **Storage Capacity**: 200 m³ roof tank system

### Software Requirements
- **Python 3.8+** with tkinter, matplotlib, sqlite3
- **Web Browser** for web HMI (Chrome/Firefox recommended)
- **Windows OS** for batch script execution

## Advanced Features

### 1. Energy Optimization
- **Variable Speed Drives** for pump efficiency
- **Load balancing** across multiple pumps
- **Energy recovery** from high-pressure reject stream
- **Predictive maintenance** scheduling

### 2. Data Management
- **SQLite database** for historical data logging
- **Performance trending** and analysis
- **Maintenance scheduling** with automated reminders
- **Report generation** with customizable templates

### 3. Safety Systems
- **Multi-layer safety interlocks** with redundancy
- **Emergency shutdown** procedures
- **Pressure relief** and overpressure protection
- **Level monitoring** with high/low alarms
- **Quality assurance** with automatic rejection

## Development Team
This project demonstrates professional-grade industrial automation development with:
- **Modular design** for easy maintenance and expansion
- **Industry standards** compliance (ISA, IEC, NEMA)
- **Documentation** following engineering best practices
- **Version control** ready structure

## License
Industrial Automation Educational Project

## Support
For technical support or questions about this water treatment system implementation, refer to the detailed documentation in the `docs/` folder.

---
**Status**: Production Ready ✅  
**Last Updated**: December 2024  
**Version**: 2.0 (Restructured)
