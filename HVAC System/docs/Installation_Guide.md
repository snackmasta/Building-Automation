# HVAC System Installation Guide

## Overview

This guide provides step-by-step instructions for installing and configuring the HVAC Control System. The system includes PLC programming, HMI interfaces, simulation tools, and comprehensive monitoring capabilities.

## Prerequisites

### Hardware Requirements

- **PLC Controller**: Siemens S7-1200 or compatible
- **HMI Panel**: 10" minimum touch panel or PC-based HMI
- **I/O Modules**: Analog and digital I/O as per system specifications
- **Network Infrastructure**: Ethernet switch, cables
- **Sensors**: Temperature, humidity, CO2, pressure sensors
- **Actuators**: Control valves, VFDs, damper actuators

### Software Requirements

- **Windows 10/11** (for development and HMI)
- **Python 3.8+** with required packages
- **TIA Portal V16+** (for PLC programming)
- **Web Browser** (Chrome, Firefox, Edge for Web HMI)

### Python Packages
```bash
pip install numpy matplotlib tkinter configparser
```

## Installation Steps

### 1. Project Setup

1. **Download/Clone Project**
   ```bash
   git clone <repository_url>
   cd "HVAC System"
   ```

2. **Verify Project Structure**
   ```
   HVAC System/
   ├── config/
   ├── diagrams/
   ├── docs/
   ├── logs/
   ├── plc/
   ├── scripts/batch/
   ├── src/
   ├── tests/
   ├── utils/
   └── wiki/
   ```

3. **Run System Verification**
   ```bash
   python utils/verification/verify_system.py
   ```

### 2. PLC Configuration

1. **Open TIA Portal**
   - Create new project: "HVAC_Control_System"
   - Add S7-1200 CPU (e.g., CPU 1215C DC/DC/DC)

2. **Import PLC Programs**
   - Import `plc/main.st` as main program block
   - Import `plc/global_vars.st` as global data block
   - Import controller programs:
     - `plc/temperature_controller.st`
     - `plc/air_quality_controller.st`
     - `plc/energy_manager.st`
     - `plc/safety_controller.st`

3. **Configure I/O**
   - Add analog input modules for sensors
   - Add analog output modules for control signals
   - Add digital I/O modules for status and alarms
   - Configure network interface

4. **Set Communication**
   - Configure Ethernet settings (IP: 192.168.1.100)
   - Enable MODBUS TCP or OPC UA communication
   - Test network connectivity

### 3. HMI Installation

#### Desktop HMI Setup

1. **Install Python Dependencies**
   ```bash
   cd "HVAC System"
   pip install -r requirements.txt
   ```

2. **Launch HMI Interface**
   ```bash
   scripts/batch/run_hmi.bat
   ```
   or
   ```bash
   python src/gui/hmi_interface.py
   ```

#### Web HMI Setup

1. **Copy Web Files**
   - Place `src/gui/web_hmi.html` on web server
   - Or open directly in browser for testing

2. **Configure Data Source**
   - Update JavaScript data source URLs
   - Configure real-time data polling

### 4. Simulation Setup

1. **Launch Simulator**
   ```bash
   scripts/batch/run_simulator.bat
   ```

2. **Verify Simulation**
   - Check zone temperature simulation
   - Verify equipment behavior
   - Monitor data logging

### 5. System Monitoring

1. **Start System Monitor**
   ```bash
   python src/monitoring/system_status.py
   ```

2. **Configure Logging**
   - Check `logs/` directory creation
   - Verify data file generation
   - Set log retention policies

## Configuration

### PLC Configuration File

Edit `config/plc_config.ini` to match your system:

```ini
[ZONES]
number_of_zones = 8
zone_names = Conference Room A,Office Area 1,Reception,Server Room,Conference Room B,Office Area 2,Break Room,Storage

[TEMPERATURE_CONTROL]
default_setpoint = 22.0
setpoint_min = 18.0
setpoint_max = 26.0
deadband = 0.5

[EQUIPMENT]
ahu_count = 2
chiller_count = 2
boiler_count = 1
pump_count = 4
```

### Network Configuration

1. **PLC Network Settings**
   - IP Address: 192.168.1.100
   - Subnet Mask: 255.255.255.0
   - Gateway: 192.168.1.1

2. **HMI Network Settings**
   - Configure same subnet as PLC
   - Test ping connectivity

### Sensor Calibration

1. **Temperature Sensors**
   - Calibrate using certified reference
   - Set scaling: 4-20mA = 0-50°C
   - Document calibration certificates

2. **Pressure Sensors**
   - Zero and span calibration
   - Set scaling: 4-20mA = 0-100 PSI
   - Verify with calibrated gauge

3. **Flow Sensors**
   - Calibrate flow coefficient
   - Set scaling per manufacturer specs
   - Verify with ultrasonic meter

## Testing

### 1. Individual Component Testing

```bash
# Test PLC communication
python tests/test_plc_communication.py

# Test HMI functionality
python tests/test_hmi_interface.py

# Test simulation accuracy
python tests/test_simulation.py
```

### 2. System Integration Testing

1. **Start All Components**
   ```bash
   scripts/batch/system_launcher.bat
   ```

2. **Verify Data Flow**
   - PLC → HMI data updates
   - HMI → PLC command execution
   - Alarm generation and acknowledgment

3. **Test Emergency Scenarios**
   - Fire alarm simulation
   - Power failure response
   - Communication loss handling

### 3. Performance Testing

1. **Load Testing**
   - Maximum concurrent users
   - Data update frequency
   - Response time measurement

2. **Endurance Testing**
   - 24-hour continuous operation
   - Memory leak detection
   - System stability verification

## Troubleshooting

### Common Issues

1. **PLC Communication Failure**
   - Check Ethernet cable connections
   - Verify IP address settings
   - Test with TIA Portal online diagnostics

2. **HMI Display Issues**
   - Check Python package installations
   - Verify tkinter availability
   - Update graphics drivers

3. **Simulation Not Starting**
   - Check file permissions
   - Verify Python path
   - Install missing dependencies

4. **Data Logging Problems**
   - Check disk space availability
   - Verify folder permissions
   - Check file handle limits

### Diagnostic Tools

1. **System Verification**
   ```bash
   python utils/verification/verify_system.py
   ```

2. **Network Diagnostics**
   ```bash
   ping 192.168.1.100
   telnet 192.168.1.100 502
   ```

3. **Log Analysis**
   ```bash
   python utils/log_analyzer.py logs/system_status.log
   ```

## Security

### Network Security

1. **Firewall Configuration**
   - Allow only required ports (502, 80, 443)
   - Block unnecessary services
   - Enable logging

2. **Access Control**
   - Implement user authentication
   - Role-based permissions
   - Regular password updates

3. **Communication Security**
   - Use encrypted protocols where possible
   - VPN for remote access
   - Certificate-based authentication

### Physical Security

1. **PLC Cabinet Security**
   - Locked electrical enclosures
   - Tamper detection
   - Physical access logging

2. **Network Infrastructure**
   - Secure switch locations
   - Cable protection
   - Port security

## Maintenance

### Daily Checks

- [ ] System status indicators
- [ ] Active alarm count
- [ ] Communication status
- [ ] Data logging verification

### Weekly Checks

- [ ] Backup system data
- [ ] Check disk space usage
- [ ] Review alarm history
- [ ] Test emergency scenarios

### Monthly Checks

- [ ] Sensor calibration verification
- [ ] Software updates
- [ ] Performance analysis
- [ ] Security audit

### Annual Checks

- [ ] Complete system verification
- [ ] Sensor recalibration
- [ ] Network security assessment
- [ ] Disaster recovery testing

## Support

### Documentation

- System diagrams: `diagrams/`
- Technical manuals: `docs/`
- Wiki pages: `wiki/pages/`

### Contact Information

- System Integrator: [Contact Info]
- PLC Vendor Support: [Contact Info]
- Emergency Contact: [24/7 Number]

### Version Information

- System Version: 2.0
- Last Updated: [Current Date]
- Next Scheduled Update: [Future Date]

---

**Note**: This installation guide should be customized for your specific installation requirements and local regulations.
