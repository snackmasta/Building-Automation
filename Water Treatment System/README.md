# Seawater Desalination and Water Distribution System

This is a complete PLC control system for a seawater desalination plant with water treatment and distribution to roof tanks.

## System Overview

The system consists of:
1. **Seawater Intake** - Raw seawater collection and pre-filtration
2. **Pre-Treatment** - Sediment and chemical filtration
3. **Reverse Osmosis (RO)** - Main desalination process
4. **Post-Treatment** - Mineralization and disinfection
5. **Storage System** - Ground and roof tank management
6. **Distribution Network** - Pressurized water distribution

## Files Description

### PLC Program Files
- **main.st** - Main PLC program with complete system control logic
- **desalination_controller.st** - RO process control and monitoring
- **pump_controller.st** - Multi-pump control and sequencing
- **water_quality_controller.st** - Water quality monitoring and treatment
- **global_vars.st** - Global variable declarations and system types
- **plc_config.ini** - PLC configuration and system parameters
- **water_treatment_simulator.py** - Python simulator for testing

### Process Documentation
- **process_diagram.py** - P&ID generator for water treatment system
- **process_diagram.png** - Generated process flow diagram
- **process_diagram.pdf** - Vector format process diagram
- **Water_Treatment_Documentation.md** - Complete system documentation

### HMI and Interface Files
- **hmi_interface.py** - Professional desktop HMI application
- **web_hmi.html** - Web-based monitoring interface
- **system_status.py** - Real-time system status monitoring

### Utility Files
- **run_simulator.bat** - Start the system simulator
- **run_hmi.bat** - Launch desktop HMI
- **generate_diagram.bat** - Generate process diagrams
- **system_launcher.bat** - Start complete system
- **README.md** - This documentation

## System Features

### Desalination Process
- Seawater intake with pre-screening
- Multi-stage pre-filtration (sediment, carbon, softening)
- High-pressure RO membrane system
- Post-treatment mineralization
- UV disinfection system

### Water Quality Control
- TDS (Total Dissolved Solids) monitoring
- pH control and adjustment
- Chlorine residual monitoring
- Turbidity measurement
- Conductivity monitoring

### Storage and Distribution
- Ground storage tank management
- Roof tank level control
- Multi-zone pressure boosting
- Distribution network monitoring
- Water loss detection

### Safety and Monitoring
- Emergency shutdown systems
- Leak detection and alarms
- Equipment protection interlocks
- Energy consumption monitoring
- Remote monitoring capabilities

### Advanced Features
- Variable frequency drive (VFD) control
- Energy optimization algorithms
- Predictive maintenance alerts
- Data logging and reporting
- Mobile notification system

## Quick Start

1. **Run Simulator**: Execute `run_simulator.bat`
2. **Start HMI**: Execute `run_hmi.bat`
3. **Generate Diagrams**: Execute `generate_diagram.bat`
4. **Launch Everything**: Execute `system_launcher.bat`

## System Specifications

- **Production Capacity**: 10,000 L/hour treated water
- **Recovery Rate**: 45% (RO process)
- **Power Consumption**: ~15 kW average
- **Storage Capacity**: 50,000 L ground + 10,000 L roof
- **Distribution Zones**: 4 pressure zones
- **Automation Level**: Fully automated with manual override

## Safety Requirements

- All electrical systems IP65 rated minimum
- Emergency stops at all major equipment
- Leak detection in all pump and valve areas
- Backup power for critical systems
- Regular water quality testing protocols

## 📊 Visual Documentation

The system includes comprehensive visual documentation:

### Process Diagrams
- **Main Process Flow**: Complete system overview from seawater intake to distribution
- **P&ID (Piping & Instrumentation)**: Detailed instrumentation and valve layouts
- **Control System Architecture**: PLC, HMI, and I/O module structure
- **Process Control Flowchart**: Detailed decision tree showing control logic and safety interlocks
- **System State Diagram**: State transitions and operational modes

### Generated Files
All diagrams are automatically generated in both PNG and PDF formats:
- `water_treatment_process_diagram.png` - Main process flow
- `water_treatment_pid.png` - P&ID diagram
- `control_system_architecture.png` - Control system layout
- `process_control_flowchart.png` - **NEW: Comprehensive control logic flowchart**
- `system_states_diagram.png` - **NEW: System state transitions**
- `water_treatment_diagrams.pdf` - Combined PDF with all diagrams

### Flowchart Features
The process control flowchart provides:
- **Decision Points**: Emergency stops, level checks, pressure validation
- **Safety Interlocks**: Multiple safety layers and fail-safe conditions
- **Process Logic**: Step-by-step control sequence from startup to monitoring
- **Alarm Conditions**: Visual representation of alarm triggers and responses
- **Control Loops**: PID control loops for pressure, quality, and flow
- **Maintenance Modes**: Cleaning cycles and maintenance procedures

### Usage
Generate all diagrams using:
```bash
python process_diagram.py
```

Or use the batch file:
```bash
generate_diagrams.bat
```
