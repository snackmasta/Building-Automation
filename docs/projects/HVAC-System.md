# HVAC Control System

A comprehensive PLC-based HVAC (Heating, Ventilation, and Air Conditioning) control system for building automation and climate management.

## 🏢 System Overview

The HVAC control system provides intelligent climate management for commercial buildings and industrial facilities with advanced energy optimization and safety features.

### Key Capabilities
- **Multi-Zone Control**: 8 independent climate zones with individual setpoints
- **Energy Management**: Variable frequency drive control and demand response
- **Air Quality Monitoring**: CO2, humidity, and particulate monitoring
- **Safety Systems**: Emergency shutdown and equipment protection
- **Predictive Control**: Weather compensation and occupancy scheduling

## 🎯 System Features

### Climate Control
- **Temperature Regulation**: PID control with 0.5°C accuracy
- **Humidity Management**: Dehumidification and humidification control
- **Air Quality Control**: CO2-based fresh air management
- **Zone Scheduling**: Time-based and occupancy-driven operation

### Energy Efficiency
- **Variable Speed Drives**: Optimized fan and pump operation
- **Demand Response**: Peak load management and cost optimization
- **Heat Recovery**: Energy recovery from exhaust air
- **Equipment Optimization**: Automated equipment sequencing

### Safety & Protection
- **Fire Safety Integration**: Smoke detection and emergency ventilation
- **Freeze Protection**: Coil protection and system safeguards
- **Equipment Protection**: Motor protection and fault detection
- **Emergency Procedures**: Automatic emergency shutdown sequences

## 📂 Project Structure

```
HVAC System/
├── README.md                    # System overview and quick start
├── MISSION_COMPLETE.md         # Project completion documentation
├── plc/                        # PLC Programming Files
│   ├── main.st                 # Main control program
│   ├── global_vars.st          # Global variable declarations
│   ├── temperature_controller.st # Zone temperature control
│   ├── air_quality_controller.st # Air quality management
│   ├── energy_manager.st       # Energy optimization
│   └── safety_controller.st    # Safety and emergency systems
├── src/                        # Source Code
│   ├── gui/                    # User Interfaces
│   │   ├── hmi_interface.py    # Desktop HMI application
│   │   └── web_hmi.html        # Web-based interface
│   ├── simulation/             # Process Simulation
│   │   └── hvac_simulator.py   # HVAC system simulator
│   ├── monitoring/             # System Monitoring
│   │   └── system_status.py    # Real-time monitoring
│   └── core/                   # Core Functionality
│       └── hvac_diagram.py     # System diagram generator
├── config/                     # Configuration Files
│   ├── plc_config.ini          # PLC configuration
│   └── hmi_config.ini          # HMI configuration
├── diagrams/                   # System Diagrams
│   ├── system_overview.png     # Overall system layout
│   ├── zone_layout.png         # Building zone configuration
│   ├── control_flow.png        # Control logic flow
│   └── energy_flow_diagram.png # Energy flow visualization
├── docs/                       # Documentation
│   ├── Installation_Guide.md   # Setup procedures
│   ├── Operating_Procedures.md # Operating instructions
│   ├── Maintenance_Manual.md   # Maintenance procedures
│   └── Troubleshooting_Guide.md# Problem resolution
├── scripts/batch/              # Automation Scripts
│   ├── system_launcher.bat     # Main system launcher
│   ├── run_hmi.bat             # HMI launcher
│   ├── run_simulator.bat       # Simulator launcher
│   └── generate_diagrams.bat   # Diagram generation
├── tests/                      # Testing & Verification
│   ├── system_verification.py  # System integrity check
│   └── test_integration.py     # Integration testing
├── utils/                      # Utility Scripts
│   └── verification/           # System verification tools
└── wiki/                       # Project Wiki
    ├── Home.md                 # Wiki homepage
    ├── pages/                  # Wiki content pages
    └── templates/              # Page templates
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+ with required packages
- Modern web browser
- Windows OS (for batch scripts)

### Launch System
```batch
# Navigate to HVAC System directory
cd "HVAC System"

# Launch complete system
scripts\batch\system_launcher.bat
```

### Individual Components
```batch
# Desktop HMI interface
scripts\batch\run_hmi.bat

# Process simulator
scripts\batch\run_simulator.bat

# Web interface (open in browser)
src\gui\web_hmi.html

# System status monitor
python src\monitoring\system_status.py
```

## 🎮 System Operation

### Zone Control
1. **Set Zone Temperatures**: Use HMI to adjust individual zone setpoints
2. **Monitor Conditions**: View real-time temperature, humidity, and air quality
3. **Schedule Operations**: Configure time-based and occupancy schedules
4. **Energy Optimization**: Enable automatic energy-saving modes

### Air Quality Management
1. **CO2 Monitoring**: Track CO2 levels for fresh air requirements
2. **Humidity Control**: Maintain optimal humidity levels
3. **Filter Management**: Monitor filter status and replacement schedules
4. **Ventilation Control**: Automatic fresh air intake adjustment

### Energy Management
1. **Equipment Sequencing**: Optimize equipment operation order
2. **Load Management**: Monitor and control peak demand
3. **Efficiency Tracking**: View energy consumption and efficiency metrics
4. **Demand Response**: Participate in utility demand response programs

## 🔧 Configuration

### Zone Configuration
Edit `config/plc_config.ini`:
```ini
[ZONES]
number_of_zones = 8
zone_names = Conference Room A,Office Area 1,Reception,Server Room,Conference Room B,Office Area 2,Break Room,Storage

[TEMPERATURE_CONTROL]
default_setpoint = 22.0
setpoint_min = 18.0
setpoint_max = 26.0
deadband = 0.5
```

### Equipment Settings
```ini
[EQUIPMENT]
ahu_count = 2
chiller_count = 2
boiler_count = 1
pump_count = 4

[ENERGY_MANAGEMENT]
demand_limit_kw = 500
peak_hours_start = 14:00
peak_hours_end = 18:00
```

## 📊 Technical Specifications

### Control System
- **PLC Programming**: IEC 61131-3 Structured Text
- **I/O Configuration**: 128 digital inputs, 64 analog inputs, 96 digital outputs, 32 analog outputs
- **Communication**: BACnet/IP and Modbus TCP/IP
- **Safety Rating**: SIL 1 compliant with emergency stops
- **Scan Time**: 100ms typical, 200ms maximum

### Process Specifications
| Parameter | Specification | Range |
|-----------|---------------|-------|
| **Zones** | 8 independent zones | Configurable 1-16 |
| **Temperature Control** | ±0.5°C accuracy | 18-26°C |
| **Humidity Control** | ±5% RH accuracy | 30-70% RH |
| **Air Quality** | CO2 monitoring | 400-2000 ppm |
| **Energy Management** | Variable speed control | 0-100% |

### Equipment Capacity
| Equipment | Quantity | Capacity | Control Method |
|-----------|----------|----------|----------------|
| **Air Handling Units** | 2 | 10,000 CFM each | VFD control |
| **Chillers** | 2 | 100 tons each | Staged control |
| **Boilers** | 1 | 500 MBH | Modulating control |
| **Pumps** | 4 | Variable | VFD control |

## 🛡️ Safety Features

### Emergency Systems
- **Emergency Stop**: Plant-wide emergency shutdown capability
- **Fire Safety**: Smoke detection integration and emergency ventilation
- **Freeze Protection**: Coil protection and low temperature alarms
- **Equipment Protection**: Motor overload and fault detection

### Alarm Management
- **Priority Levels**: Critical, High, Medium, Low priority alarms
- **Escalation**: Automatic escalation for unacknowledged alarms
- **Notification**: Email and SMS notification capability
- **Logging**: Complete alarm history and acknowledgment tracking

## 📈 Performance Monitoring

### Key Performance Indicators (KPIs)
- **Energy Efficiency**: kWh per square foot per day
- **Temperature Performance**: Zone temperature deviation from setpoint
- **Equipment Efficiency**: Runtime hours and performance ratios
- **Maintenance Indicators**: Filter change intervals and equipment health

### Trending and Analytics
- **Real-time Trending**: Live data visualization
- **Historical Analysis**: Long-term performance analysis
- **Energy Reports**: Daily, weekly, and monthly energy consumption
- **Maintenance Reports**: Equipment runtime and maintenance schedules

## 🔍 Troubleshooting

### Common Issues
| Issue | Possible Cause | Solution |
|-------|---------------|----------|
| **Zone Not Heating** | Damper closed, valve issue | Check damper position, verify valve operation |
| **High Energy Usage** | Equipment oversized, poor scheduling | Review equipment sequencing, adjust schedules |
| **Poor Air Quality** | Insufficient fresh air, filter dirty | Check fresh air dampers, replace filters |
| **Temperature Swings** | Poor PID tuning, sensor issues | Retune PID parameters, calibrate sensors |

### Diagnostic Procedures
1. **System Status Check**: Review overall system status and alarms
2. **Zone Analysis**: Check individual zone performance and setpoints
3. **Equipment Status**: Verify all equipment operational status
4. **Communication Check**: Ensure all network communications active

## 📚 Documentation

### Available Documentation
- **[Installation Guide](../docs/Installation_Guide.md)**: Complete setup procedures
- **[Operating Procedures](../docs/Operating_Procedures.md)**: Daily operation guidelines
- **[Maintenance Manual](../docs/Maintenance_Manual.md)**: Preventive maintenance
- **[Troubleshooting Guide](../docs/Troubleshooting_Guide.md)**: Problem resolution

### Wiki Resources
- **[Project Wiki](../wiki/Home.md)**: Comprehensive knowledge base
- **[Technical Reference](../wiki/pages/Technical_Reference.md)**: Detailed specifications
- **[Configuration Guide](../wiki/pages/Configuration.md)**: System configuration
- **[Performance Monitoring](../wiki/pages/Performance_Monitoring.md)**: KPI tracking

## 🎓 Learning Objectives

### For Building Automation Professionals
- Multi-zone HVAC control strategies
- Energy management and optimization techniques
- BACnet communication and integration
- Building automation system design

### For Controls Engineers
- Advanced PLC programming techniques
- System integration and communication
- Energy optimization algorithms
- Professional HMI development

### For Facility Managers
- HVAC system operation and optimization
- Energy management and cost control
- Preventive maintenance procedures
- Performance monitoring and analysis

## 🌟 Advanced Features

### Energy Optimization
- **Optimal Start/Stop**: Weather-compensated pre-conditioning
- **Economizer Control**: Free cooling with outside air
- **Demand Limiting**: Automatic load shedding during peak periods
- **Equipment Optimization**: Automatic equipment sequencing for efficiency

### Predictive Control
- **Weather Integration**: Weather forecast-based control adjustments
- **Occupancy Learning**: Adaptive scheduling based on usage patterns
- **Predictive Maintenance**: Equipment health monitoring and prediction
- **Load Forecasting**: Predictive energy demand analysis

## 📞 Support Resources

### Getting Help
1. **Documentation**: Check comprehensive docs in `docs/` folder
2. **Wiki**: Browse project wiki for detailed information
3. **System Verification**: Run `utils/verification/verify_system.py`
4. **Configuration Check**: Verify settings in `config/` files

### Technical Support
- **System Status**: Use built-in monitoring tools
- **Log Analysis**: Check system logs in `logs/` folder
- **Performance Metrics**: Review KPI dashboards
- **Alarm History**: Analyze alarm patterns and trends

---

**Ready to get started?**
- [Quick Start Guide](../guides/Quick-Start-Guide.md) - Get running in minutes
- [Installation Guide](../docs/Installation_Guide.md) - Detailed setup
- [Project Wiki](../wiki/Home.md) - Comprehensive documentation

*Professional building automation made accessible!*
