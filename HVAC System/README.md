# HVAC Control System

A comprehensive PLC-based HVAC (Heating, Ventilation, and Air Conditioning) control system for building automation and climate management.

## 🏢 System Overview

This HVAC control system provides:
- **Temperature Control**: Multi-zone heating and cooling management
- **Air Quality Monitoring**: CO2, humidity, and air flow control
- **Energy Management**: Efficient operation and demand response
- **Safety Systems**: Emergency shutdown and fault detection
- **Zone Control**: Individual room/area climate management
- **Scheduled Operations**: Time-based and occupancy-driven control

## 🎯 Key Features

### Climate Control
- Multi-zone temperature regulation
- Humidity control and monitoring
- Air quality management (CO2, VOCs)
- Fresh air intake optimization

### Energy Efficiency
- Variable frequency drive (VFD) control
- Demand-based ventilation
- Heat recovery systems
- Peak demand management

### Safety & Monitoring
- Emergency shutdown procedures
- Filter monitoring and alerts
- Equipment fault detection
- Real-time system diagnostics

### User Interface
- Web-based HMI for system monitoring
- Mobile-responsive design
- Real-time alerts and notifications
- Historical data logging

## 📂 Project Structure

```
HVAC System/
├── README.md                    # This file
├── MISSION_COMPLETE.md         # Project completion summary
├── config/                     # Configuration files
│   └── plc_config.ini         # PLC and system configuration
├── diagrams/                   # System diagrams and schematics
│   ├── hvac_architecture.png  # System architecture diagram
│   ├── control_logic_flow.png # Control logic flowchart
│   └── zone_layout.png        # Building zone layout
├── docs/                       # Documentation
│   ├── System_Documentation.md # Complete system documentation
│   ├── Installation_Guide.md  # Installation procedures
│   └── Maintenance_Guide.md   # Maintenance procedures
├── plc/                        # PLC programming files
│   ├── main.st                # Main program logic
│   ├── global_vars.st         # Global variable definitions
│   ├── temperature_controller.st # Temperature control logic
│   ├── air_quality_controller.st # Air quality management
│   ├── energy_manager.st      # Energy optimization logic
│   └── safety_controller.st   # Safety and emergency systems
├── scripts/                    # Automation scripts
│   └── batch/                 # Windows batch files
│       ├── system_launcher.bat
│       ├── run_hmi.bat
│       ├── run_simulator.bat
│       └── generate_diagrams.bat
├── src/                        # Source code
│   ├── core/                  # Core functionality
│   │   └── hvac_diagram.py    # System diagram generator
│   ├── gui/                   # User interface
│   │   ├── hmi_interface.py   # HMI application
│   │   └── web_hmi.html       # Web-based interface
│   ├── monitoring/            # System monitoring
│   │   └── system_status.py   # Status monitoring
│   └── simulation/            # System simulation
│       └── hvac_simulator.py  # HVAC system simulator
├── tests/                      # Test files
├── utils/                      # Utility scripts
│   └── verification/          # System verification
│       └── verify_system.py   # System verification script
└── wiki/                       # Project documentation wiki
    ├── Home.md                # Wiki home page
    ├── pages/                 # Wiki pages
    └── templates/             # Page templates
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Web browser for HMI interface
- PLC programming environment (optional)

### Installation
1. Clone or download this project
2. Navigate to the project directory
3. Run the system launcher:
   ```cmd
   scripts\batch\system_launcher.bat
   ```

### Running the System
1. **Start the Simulator**: `scripts\batch\run_simulator.bat`
2. **Launch HMI Interface**: `scripts\batch\run_hmi.bat`
3. **Monitor System Status**: `python src\monitoring\system_status.py`

## 🎮 System Control

### Temperature Control
- Set target temperatures for each zone
- Monitor heating/cooling demand
- Adjust system response based on occupancy

### Air Quality Management
- Monitor CO2 levels and humidity
- Control fresh air intake
- Manage air circulation and filtration

### Energy Optimization
- Implement demand response strategies
- Monitor energy consumption
- Optimize equipment scheduling

## 📊 Monitoring & Diagnostics

The system provides comprehensive monitoring capabilities:
- Real-time temperature and humidity readings
- Air quality measurements (CO2, particles)
- Energy consumption tracking
- Equipment status and alarms
- Historical data logging and analysis

## 🔧 Configuration

System configuration is managed through:
- `config/plc_config.ini`: Main system parameters
- Web HMI: Runtime adjustments and setpoints
- PLC program: Core control logic and safety parameters

## 🛡️ Safety Features

- Emergency shutdown capability
- High/low temperature alarms
- Equipment fault detection
- Filter replacement alerts
- Fire safety integration ready

## 📚 Documentation

Comprehensive documentation is available in the `wiki/` directory:
- **System Overview**: Complete system description
- **Installation Guide**: Step-by-step setup instructions
- **Operating Procedures**: Daily operation guidelines
- **Maintenance Guide**: Preventive maintenance procedures
- **Troubleshooting**: Common issues and solutions

## 🤝 Contributing

This project follows industrial automation best practices:
- Structured Text (ST) for PLC programming
- Modular design for easy maintenance
- Comprehensive documentation
- Safety-first approach

## 📄 License

This project is designed for educational and industrial automation purposes.

## 📞 Support

For technical support and questions:
- Check the wiki documentation
- Review troubleshooting guides
- Verify system configuration

---

*HVAC Control System - Building Automation Made Simple*
