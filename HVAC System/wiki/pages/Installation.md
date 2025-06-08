# Installation Guide

## HVAC Control System Installation

This guide provides step-by-step instructions for installing and configuring the HVAC Control System.

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [System Requirements](#system-requirements)
3. [Software Installation](#software-installation)
4. [Hardware Setup](#hardware-setup)
5. [Configuration](#configuration)
6. [Verification](#verification)
7. [First Start](#first-start)
8. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Hardware Requirements

- **PLC**: Compatible Allen-Bradley, Siemens, or ModiconPLC
- **PC/HMI Station**: Windows 10/11 with minimum 4GB RAM
- **Network**: Ethernet connectivity for PLC communication
- **HVAC Equipment**: Properly commissioned HVAC system
- **Sensors**: Temperature, humidity, pressure, and air quality sensors
- **Actuators**: Dampers, valves, and variable frequency drives

### Software Requirements

- **Python 3.8+**: Required for all system components
- **Git**: For version control and updates
- **Text Editor**: VS Code, Notepad++, or similar

---

## System Requirements

### Minimum Requirements

| Component | Requirement |
|-----------|-------------|
| Operating System | Windows 10 (64-bit) |
| Processor | Intel Core i3 or equivalent |
| Memory | 4 GB RAM |
| Storage | 2 GB available space |
| Network | Ethernet adapter |
| Display | 1024x768 resolution |

### Recommended Requirements

| Component | Requirement |
|-----------|-------------|
| Operating System | Windows 11 (64-bit) |
| Processor | Intel Core i5 or equivalent |
| Memory | 8 GB RAM |
| Storage | 10 GB available space (SSD preferred) |
| Network | Gigabit Ethernet |
| Display | 1920x1080 resolution |

---

## Software Installation

### Step 1: Install Python

1. Download Python 3.8+ from [python.org](https://python.org)
2. Run the installer with **"Add Python to PATH"** checked
3. Verify installation:
   ```cmd
   python --version
   pip --version
   ```

### Step 2: Install Required Packages

```cmd
pip install numpy matplotlib tkinter configparser pathlib
```

### Step 3: Download System Files

1. Download the HVAC Control System package
2. Extract to desired location (e.g., `C:\HVAC_System\`)
3. Verify all files are present using the verification script

---

## Hardware Setup

### PLC Configuration

1. **Network Setup**:
   - Configure PLC IP address (default: 192.168.1.100)
   - Set subnet mask: 255.255.255.0
   - Configure gateway if required

2. **I/O Mapping**:
   - Map temperature sensors to analog inputs
   - Map humidity sensors to analog inputs
   - Map pressure sensors to analog inputs
   - Map damper actuators to analog outputs
   - Map valve actuators to analog outputs

3. **Communication Settings**:
   - Protocol: Ethernet/IP or Modbus TCP
   - Port: 44818 (Ethernet/IP) or 502 (Modbus)
   - Scan rate: 100ms recommended

### Sensor Wiring

#### Temperature Sensors
- **Type**: RTD (Pt100) or 4-20mA transmitters
- **Range**: 0-50°C (32-122°F)
- **Accuracy**: ±0.5°C
- **Wiring**: 3-wire for RTD, 2-wire for 4-20mA

#### Humidity Sensors
- **Type**: Capacitive or resistive
- **Range**: 0-100% RH
- **Output**: 4-20mA or 0-10V
- **Calibration**: Annual calibration recommended

#### Pressure Sensors
- **Type**: Piezoresistive or capacitive
- **Range**: -500 to +500 Pa (typical)
- **Output**: 4-20mA
- **Installation**: Mount in representative locations

### Actuator Setup

#### Damper Actuators
- **Type**: Electric or pneumatic
- **Control Signal**: 0-10V or 4-20mA
- **Feedback**: Position feedback recommended
- **Calibration**: Full stroke calibration required

#### Valve Actuators
- **Type**: Electric or pneumatic
- **Control Signal**: 0-10V or 4-20mA
- **Sizing**: Properly sized for system flow
- **Installation**: Accessible for maintenance

---

## Configuration

### Step 1: PLC Configuration

Edit `config/plc_config.ini`:

```ini
[PLC]
ip_address = 192.168.1.100
port = 44818
timeout = 5
protocol = ethernet_ip

[SYSTEM]
scan_interval = 1.0
log_level = INFO
max_log_files = 30

[ZONES]
zone_count = 8
default_setpoint = 22.0
temp_tolerance = 0.5
```

### Step 2: Zone Configuration

Configure each zone in the `[ZONES]` section:

```ini
[ZONE_1]
name = Office Area
temp_sensor_address = N7:0
humidity_sensor_address = N7:1
damper_output_address = N7:10
setpoint_min = 18.0
setpoint_max = 26.0

[ZONE_2]
name = Conference Room
temp_sensor_address = N7:2
humidity_sensor_address = N7:3
damper_output_address = N7:11
setpoint_min = 20.0
setpoint_max = 24.0
```

### Step 3: Safety Configuration

```ini
[SAFETY]
high_temp_alarm = 30.0
low_temp_alarm = 10.0
high_humidity_alarm = 80.0
emergency_shutdown_temp = 35.0
fire_alarm_input = I:0/0
```

---

## Verification

### Automated Verification

Run the system verification script:

```cmd
cd "HVAC System"
python utils\verification\verify_system.py
```

This will check:
- ✅ File structure
- ✅ Configuration files
- ✅ Python dependencies
- ✅ PLC programs
- ✅ Documentation
- ✅ System integration

### Manual Verification Checklist

- [ ] All required files present
- [ ] Python 3.8+ installed
- [ ] Required packages installed
- [ ] PLC communication configured
- [ ] Sensor wiring completed
- [ ] Actuator calibration completed
- [ ] Safety systems configured
- [ ] Network connectivity verified

---

## First Start

### Step 1: Start System Components

Use the system launcher:

```cmd
cd "HVAC System"
scripts\batch\system_launcher.bat
```

Select option 4: "Start Complete System"

### Step 2: Verify Operation

1. **Check PLC Communication**:
   - Monitor system status
   - Verify data exchange
   - Check for communication errors

2. **Test Zone Control**:
   - Adjust setpoints
   - Verify damper response
   - Monitor temperature control

3. **Verify Safety Systems**:
   - Test alarm conditions
   - Verify emergency shutdown
   - Check safety interlocks

### Step 3: Calibration

1. **Temperature Sensors**:
   - Compare readings to reference
   - Adjust offsets if necessary
   - Document calibration

2. **Actuators**:
   - Verify full stroke operation
   - Check position feedback
   - Calibrate control loops

---

## Troubleshooting

### Common Issues

#### Python Import Errors
```
ERROR: ModuleNotFoundError: No module named 'numpy'
```
**Solution**: Install missing packages with `pip install numpy matplotlib`

#### PLC Communication Errors
```
ERROR: Unable to connect to PLC at 192.168.1.100
```
**Solution**: 
- Check network connectivity
- Verify PLC IP address
- Check firewall settings

#### Configuration File Errors
```
ERROR: Configuration section [PLC] not found
```
**Solution**: Verify `config/plc_config.ini` exists and is properly formatted

### Diagnostic Tools

1. **Network Connectivity**:
   ```cmd
   ping 192.168.1.100
   telnet 192.168.1.100 44818
   ```

2. **System Status**:
   ```cmd
   python system_status.py
   ```

3. **Log Files**:
   - Check `logs/hvac_system.log`
   - Review error messages
   - Monitor performance metrics

---

## Support

### Documentation
- [Operating Procedures](Operating_Procedures.md)
- [Troubleshooting Guide](Troubleshooting.md)
- [Maintenance Manual](../docs/Maintenance_Manual.md)

### Contact Information
- **Technical Support**: support@hvac-system.com
- **Emergency Contact**: 1-800-HVAC-911
- **Documentation**: [Wiki Home](Home.md)

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | June 8, 2025 | Initial installation guide |

---

*Last Updated: June 8, 2025*
