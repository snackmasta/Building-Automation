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

## 📋 I/O Table

### Digital Inputs (32 channels)
| Address | Tag Name | Description | Signal Type | Location/Zone |
|---------|----------|-------------|-------------|---------------|
| I0.0 | Fire_Alarm | Fire alarm system input | 24V DC, NC | Building Main |
| I0.1 | Emergency_Stop | Emergency stop button | 24V DC, NC | Control Panel |
| I0.2 | Main_Power_Status | Main power status | 24V DC, NO | Electrical Room |
| I0.3 | Backup_Power_Status | Backup power status | 24V DC, NO | Electrical Room |
| I0.4 | Smoke_Detector_1 | Smoke detector zone 1 | 24V DC, NC | AHU-1 Area |
| I0.5 | Smoke_Detector_2 | Smoke detector zone 2 | 24V DC, NC | AHU-2 Area |
| I0.6 | Filter_Status_AHU1 | Filter differential pressure | 24V DC, NO | AHU-1 |
| I0.7 | Filter_Status_AHU2 | Filter differential pressure | 24V DC, NO | AHU-2 |
| I1.0 | Occupancy_Zone1 | Zone 1 occupancy sensor | 24V DC, NO | Lobby |
| I1.1 | Occupancy_Zone2 | Zone 2 occupancy sensor | 24V DC, NO | Conference Room |
| I1.2 | Occupancy_Zone3 | Zone 3 occupancy sensor | 24V DC, NO | Office Area 1 |
| I1.3 | Occupancy_Zone4 | Zone 4 occupancy sensor | 24V DC, NO | Office Area 2 |
| I1.4 | Occupancy_Zone5 | Zone 5 occupancy sensor | 24V DC, NO | Kitchen |
| I1.5 | Occupancy_Zone6 | Zone 6 occupancy sensor | 24V DC, NO | Server Room |
| I1.6 | Occupancy_Zone7 | Zone 7 occupancy sensor | 24V DC, NO | Storage |
| I1.7 | Occupancy_Zone8 | Zone 8 occupancy sensor | 24V DC, NO | Break Room |
| I2.0 | AHU1_Status | AHU-1 running status | 24V DC, NO | AHU-1 |
| I2.1 | AHU2_Status | AHU-2 running status | 24V DC, NO | AHU-2 |
| I2.2 | Chiller1_Status | Chiller 1 running status | 24V DC, NO | Chiller Plant |
| I2.3 | Chiller2_Status | Chiller 2 running status | 24V DC, NO | Chiller Plant |
| I2.4 | Boiler_Status | Boiler running status | 24V DC, NO | Boiler Room |
| I2.5 | Pump1_Status | Pump 1 running status | 24V DC, NO | Pump Room |
| I2.6 | Pump2_Status | Pump 2 running status | 24V DC, NO | Pump Room |
| I2.7 | Pump3_Status | Pump 3 running status | 24V DC, NO | Pump Room |
| I3.0 | AHU1_Fault | AHU-1 fault alarm | 24V DC, NC | AHU-1 |
| I3.1 | AHU2_Fault | AHU-2 fault alarm | 24V DC, NC | AHU-2 |
| I3.2 | Chiller1_Fault | Chiller 1 fault alarm | 24V DC, NC | Chiller Plant |
| I3.3 | Chiller2_Fault | Chiller 2 fault alarm | 24V DC, NC | Chiller Plant |
| I3.4 | Boiler_Fault | Boiler fault alarm | 24V DC, NC | Boiler Room |
| I3.5 | VFD1_Fault | VFD 1 fault status | 24V DC, NC | AHU-1 |
| I3.6 | VFD2_Fault | VFD 2 fault status | 24V DC, NC | AHU-2 |
| I3.7 | High_Temp_Alarm | High temperature alarm | 24V DC, NO | Building Main |

### Analog Inputs (64 channels)
| Address | Tag Name | Description | Signal Type | Range | Location/Zone |
|---------|----------|-------------|-------------|-------|---------------|
| IW0 | Zone1_Temperature | Zone 1 temperature sensor | 4-20mA | 0-50°C | Lobby |
| IW1 | Zone2_Temperature | Zone 2 temperature sensor | 4-20mA | 0-50°C | Conference Room |
| IW2 | Zone3_Temperature | Zone 3 temperature sensor | 4-20mA | 0-50°C | Office Area 1 |
| IW3 | Zone4_Temperature | Zone 4 temperature sensor | 4-20mA | 0-50°C | Office Area 2 |
| IW4 | Zone5_Temperature | Zone 5 temperature sensor | 4-20mA | 0-50°C | Kitchen |
| IW5 | Zone6_Temperature | Zone 6 temperature sensor | 4-20mA | 0-50°C | Server Room |
| IW6 | Zone7_Temperature | Zone 7 temperature sensor | 4-20mA | 0-50°C | Storage |
| IW7 | Zone8_Temperature | Zone 8 temperature sensor | 4-20mA | 0-50°C | Break Room |
| IW10 | Zone1_Humidity | Zone 1 humidity sensor | 4-20mA | 0-100% RH | Lobby |
| IW11 | Zone2_Humidity | Zone 2 humidity sensor | 4-20mA | 0-100% RH | Conference Room |
| IW12 | Zone3_Humidity | Zone 3 humidity sensor | 4-20mA | 0-100% RH | Office Area 1 |
| IW13 | Zone4_Humidity | Zone 4 humidity sensor | 4-20mA | 0-100% RH | Office Area 2 |
| IW14 | Zone5_Humidity | Zone 5 humidity sensor | 4-20mA | 0-100% RH | Kitchen |
| IW15 | Zone6_Humidity | Zone 6 humidity sensor | 4-20mA | 0-100% RH | Server Room |
| IW16 | Zone7_Humidity | Zone 7 humidity sensor | 4-20mA | 0-100% RH | Storage |
| IW17 | Zone8_Humidity | Zone 8 humidity sensor | 4-20mA | 0-100% RH | Break Room |
| IW20 | Zone1_CO2 | Zone 1 CO2 sensor | 4-20mA | 0-2000 ppm | Lobby |
| IW21 | Zone2_CO2 | Zone 2 CO2 sensor | 4-20mA | 0-2000 ppm | Conference Room |
| IW22 | Zone3_CO2 | Zone 3 CO2 sensor | 4-20mA | 0-2000 ppm | Office Area 1 |
| IW23 | Zone4_CO2 | Zone 4 CO2 sensor | 4-20mA | 0-2000 ppm | Office Area 2 |
| IW30 | Supply_Air_Temp | Supply air temperature | 4-20mA | -20-80°C | AHU-1 |
| IW31 | Return_Air_Temp | Return air temperature | 4-20mA | -20-80°C | AHU-1 |
| IW32 | Outside_Air_Temp | Outside air temperature | 4-20mA | -40-60°C | Roof |
| IW33 | Mixed_Air_Temp | Mixed air temperature | 4-20mA | -20-80°C | AHU-1 |
| IW34 | Supply_Air_Temp_2 | Supply air temperature AHU-2 | 4-20mA | -20-80°C | AHU-2 |
| IW35 | Return_Air_Temp_2 | Return air temperature AHU-2 | 4-20mA | -20-80°C | AHU-2 |
| IW40 | Supply_Pressure | Supply duct pressure | 4-20mA | 0-1000 Pa | Supply Duct |
| IW41 | Return_Pressure | Return duct pressure | 4-20mA | 0-1000 Pa | Return Duct |
| IW42 | Filter_DP_AHU1 | Filter differential pressure | 4-20mA | 0-500 Pa | AHU-1 |
| IW43 | Filter_DP_AHU2 | Filter differential pressure | 4-20mA | 0-500 Pa | AHU-2 |
| IW44 | Static_Pressure | Building static pressure | 4-20mA | -100-100 Pa | Building |
| IW50 | Chilled_Water_Supply | Chilled water supply temp | 4-20mA | 0-50°C | Chiller Plant |
| IW51 | Chilled_Water_Return | Chilled water return temp | 4-20mA | 0-50°C | Chiller Plant |
| IW52 | Hot_Water_Supply | Hot water supply temp | 4-20mA | 0-100°C | Boiler Room |
| IW53 | Hot_Water_Return | Hot water return temp | 4-20mA | 0-100°C | Boiler Room |
| IW54 | CHW_Flow_Rate | Chilled water flow rate | 4-20mA | 0-500 GPM | Pump Room |
| IW55 | HW_Flow_Rate | Hot water flow rate | 4-20mA | 0-200 GPM | Pump Room |
| IW60 | Power_Meter_Total | Total power consumption | 4-20mA | 0-1000 kW | Electrical |
| IW61 | Power_Meter_HVAC | HVAC power consumption | 4-20mA | 0-500 kW | Electrical |
| IW62 | Gas_Meter | Natural gas consumption | 4-20mA | 0-1000 CFH | Gas Meter |
| IW63 | Outside_Humidity | Outside humidity sensor | 4-20mA | 0-100% RH | Roof |

### Digital Outputs (96 channels)
| Address | Tag Name | Description | Signal Type | Equipment |
|---------|----------|-------------|-------------|-----------|
| Q0.0 | AHU1_Start | AHU-1 start command | 24V DC | AHU-1 Starter |
| Q0.1 | AHU2_Start | AHU-2 start command | 24V DC | AHU-2 Starter |
| Q0.2 | Pump1_Start | Pump 1 start command | 24V DC | Pump 1 Starter |
| Q0.3 | Pump2_Start | Pump 2 start command | 24V DC | Pump 2 Starter |
| Q0.4 | Pump3_Start | Pump 3 start command | 24V DC | Pump 3 Starter |
| Q0.5 | Pump4_Start | Pump 4 start command | 24V DC | Pump 4 Starter |
| Q0.6 | Chiller1_Start | Chiller 1 start command | 24V DC | Chiller 1 |
| Q0.7 | Chiller2_Start | Chiller 2 start command | 24V DC | Chiller 2 |
| Q1.0 | Boiler_Start | Boiler start command | 24V DC | Boiler |
| Q1.1 | Exhaust_Fan1_Start | Exhaust fan 1 start | 24V DC | Exhaust Fan 1 |
| Q1.2 | Exhaust_Fan2_Start | Exhaust fan 2 start | 24V DC | Exhaust Fan 2 |
| Q1.3 | Makeup_Air_Fan | Makeup air fan start | 24V DC | Makeup Air Unit |
| Q1.4 | Heat_Recovery_Enable | Heat recovery enable | 24V DC | Heat Recovery |
| Q1.5 | Economizer_Enable | Economizer enable | 24V DC | Economizer |
| Q1.6 | Fire_Alarm_Reset | Fire alarm reset | 24V DC | Fire Panel |
| Q1.7 | System_Alarm | General system alarm | 24V DC | Alarm Horn |
| Q2.0 | Zone1_Damper_Open | Zone 1 damper open | 24V DC | Zone 1 VAV |
| Q2.1 | Zone1_Damper_Close | Zone 1 damper close | 24V DC | Zone 1 VAV |
| Q2.2 | Zone2_Damper_Open | Zone 2 damper open | 24V DC | Zone 2 VAV |
| Q2.3 | Zone2_Damper_Close | Zone 2 damper close | 24V DC | Zone 2 VAV |
| Q2.4 | Zone3_Damper_Open | Zone 3 damper open | 24V DC | Zone 3 VAV |
| Q2.5 | Zone3_Damper_Close | Zone 3 damper close | 24V DC | Zone 3 VAV |
| Q2.6 | Zone4_Damper_Open | Zone 4 damper open | 24V DC | Zone 4 VAV |
| Q2.7 | Zone4_Damper_Close | Zone 4 damper close | 24V DC | Zone 4 VAV |
| Q3.0 | Zone5_Damper_Open | Zone 5 damper open | 24V DC | Zone 5 VAV |
| Q3.1 | Zone5_Damper_Close | Zone 5 damper close | 24V DC | Zone 5 VAV |
| Q3.2 | Zone6_Damper_Open | Zone 6 damper open | 24V DC | Zone 6 VAV |
| Q3.3 | Zone6_Damper_Close | Zone 6 damper close | 24V DC | Zone 6 VAV |
| Q3.4 | Zone7_Damper_Open | Zone 7 damper open | 24V DC | Zone 7 VAV |
| Q3.5 | Zone7_Damper_Close | Zone 7 damper close | 24V DC | Zone 7 VAV |
| Q3.6 | Zone8_Damper_Open | Zone 8 damper open | 24V DC | Zone 8 VAV |
| Q3.7 | Zone8_Damper_Close | Zone 8 damper close | 24V DC | Zone 8 VAV |
| Q4.0 | Outside_Air_Damper_Open | Outside air damper open | 24V DC | OA Damper |
| Q4.1 | Outside_Air_Damper_Close | Outside air damper close | 24V DC | OA Damper |
| Q4.2 | Return_Air_Damper_Open | Return air damper open | 24V DC | RA Damper |
| Q4.3 | Return_Air_Damper_Close | Return air damper close | 24V DC | RA Damper |
| Q4.4 | Exhaust_Damper_Open | Exhaust damper open | 24V DC | Exhaust Damper |
| Q4.5 | Exhaust_Damper_Close | Exhaust damper close | 24V DC | Exhaust Damper |
| Q4.6 | Relief_Damper_Open | Relief damper open | 24V DC | Relief Damper |
| Q4.7 | Relief_Damper_Close | Relief damper close | 24V DC | Relief Damper |
| Q5.0 | Status_Light_Green | System normal status | 24V DC | Status Panel |
| Q5.1 | Status_Light_Yellow | System warning status | 24V DC | Status Panel |
| Q5.2 | Status_Light_Red | System alarm status | 24V DC | Status Panel |
| Q5.3 | Horn_Alarm | Audio alarm | 24V DC | Alarm Horn |
| Q5.4 | Strobe_Light | Visual alarm | 24V DC | Strobe Light |
| Q5.5 | Maintenance_Light | Maintenance required | 24V DC | Maintenance Light |

### Analog Outputs (32 channels)
| Address | Tag Name | Description | Signal Type | Range | Equipment |
|---------|----------|-------------|-------------|-------|-----------|
| QW0 | Zone1_Damper_Position | Zone 1 damper position | 0-10V | 0-100% | Zone 1 VAV |
| QW1 | Zone2_Damper_Position | Zone 2 damper position | 0-10V | 0-100% | Zone 2 VAV |
| QW2 | Zone3_Damper_Position | Zone 3 damper position | 0-10V | 0-100% | Zone 3 VAV |
| QW3 | Zone4_Damper_Position | Zone 4 damper position | 0-10V | 0-100% | Zone 4 VAV |
| QW4 | Zone5_Damper_Position | Zone 5 damper position | 0-10V | 0-100% | Zone 5 VAV |
| QW5 | Zone6_Damper_Position | Zone 6 damper position | 0-10V | 0-100% | Zone 6 VAV |
| QW6 | Zone7_Damper_Position | Zone 7 damper position | 0-10V | 0-100% | Zone 7 VAV |
| QW7 | Zone8_Damper_Position | Zone 8 damper position | 0-10V | 0-100% | Zone 8 VAV |
| QW10 | AHU1_Supply_Fan_Speed | AHU-1 supply fan VFD | 4-20mA | 0-100% | AHU-1 VFD |
| QW11 | AHU1_Return_Fan_Speed | AHU-1 return fan VFD | 4-20mA | 0-100% | AHU-1 VFD |
| QW12 | AHU2_Supply_Fan_Speed | AHU-2 supply fan VFD | 4-20mA | 0-100% | AHU-2 VFD |
| QW13 | AHU2_Return_Fan_Speed | AHU-2 return fan VFD | 4-20mA | 0-100% | AHU-2 VFD |
| QW14 | Pump1_Speed | Pump 1 VFD speed | 4-20mA | 0-100% | Pump 1 VFD |
| QW15 | Pump2_Speed | Pump 2 VFD speed | 4-20mA | 0-100% | Pump 2 VFD |
| QW16 | Pump3_Speed | Pump 3 VFD speed | 4-20mA | 0-100% | Pump 3 VFD |
| QW17 | Pump4_Speed | Pump 4 VFD speed | 4-20mA | 0-100% | Pump 4 VFD |
| QW20 | Outside_Air_Damper | Outside air damper position | 0-10V | 0-100% | OA Damper |
| QW21 | Return_Air_Damper | Return air damper position | 0-10V | 0-100% | RA Damper |
| QW22 | Exhaust_Damper | Exhaust damper position | 0-10V | 0-100% | Exhaust Damper |
| QW23 | Relief_Damper | Relief damper position | 0-10V | 0-100% | Relief Damper |
| QW24 | Zone1_Reheat_Valve | Zone 1 reheat valve | 0-10V | 0-100% | Zone 1 Reheat |
| QW25 | Zone2_Reheat_Valve | Zone 2 reheat valve | 0-10V | 0-100% | Zone 2 Reheat |
| QW26 | Zone3_Reheat_Valve | Zone 3 reheat valve | 0-10V | 0-100% | Zone 3 Reheat |
| QW27 | Zone4_Reheat_Valve | Zone 4 reheat valve | 0-10V | 0-100% | Zone 4 Reheat |
| QW28 | Zone5_Reheat_Valve | Zone 5 reheat valve | 0-10V | 0-100% | Zone 5 Reheat |
| QW29 | Zone6_Reheat_Valve | Zone 6 reheat valve | 0-10V | 0-100% | Zone 6 Reheat |
| QW30 | Zone7_Reheat_Valve | Zone 7 reheat valve | 0-10V | 0-100% | Zone 7 Reheat |
| QW31 | Zone8_Reheat_Valve | Zone 8 reheat valve | 0-10V | 0-100% | Zone 8 Reheat |

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
