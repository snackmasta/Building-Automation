# HVAC System Wiki - Home

Welcome to the comprehensive HVAC Control System documentation wiki. This wiki serves as the central repository for all system documentation, procedures, and knowledge base articles.

## Quick Navigation

### 📋 [Installation & Setup](pages/Installation.md)
Complete guide for installing and configuring the HVAC control system

### 🔧 [Operating Procedures](pages/Operating_Procedures.md)
Daily operations, startup/shutdown procedures, and zone control operations

### 🛠️ [Maintenance](pages/Maintenance.md)
Preventive maintenance schedules, procedures, and calibration guidelines

### 🚨 [Troubleshooting](pages/Troubleshooting.md)
Diagnostic procedures, common issues, and resolution steps

### ⚙️ [System Configuration](pages/Configuration.md)
PLC programming, parameter settings, and system customization

### 📊 [Performance Monitoring](pages/Performance_Monitoring.md)
KPIs, trending, energy efficiency, and system optimization

### 🔒 [Safety Procedures](pages/Safety.md)
Safety protocols, emergency procedures, and compliance requirements

### 📚 [Technical Reference](pages/Technical_Reference.md)
System specifications, wiring diagrams, and technical documentation

## System Overview

### Architecture
The HVAC control system manages 8 zones with comprehensive control over:
- **Temperature Control:** Multi-stage heating and cooling with PID control
- **Air Quality Management:** CO2 and humidity monitoring with fresh air control
- **Energy Management:** Demand response, load shedding, and optimization
- **Safety Systems:** Fire protection, freeze protection, emergency shutdown

### Key Components
- **PLC Controllers:** Main control logic and equipment management
- **HMI Interface:** Operator interface for monitoring and control
- **Sensors & Actuators:** Temperature, pressure, flow, and air quality monitoring
- **Communication Network:** BACnet/Modbus integration with building systems

### Features
- Real-time monitoring and control
- Historical data logging and trending
- Alarm management and notification
- Energy optimization algorithms
- Comprehensive diagnostics and maintenance tools

## Quick Start Guide

### 1. System Startup
```bash
# Navigate to system directory
cd "C:\Users\Legion\Desktop\PLC\HVAC System"

# Launch system components
scripts\batch\system_launcher.bat
```

### 2. Access Interfaces
- **Desktop HMI:** Run `scripts\batch\run_hmi.bat`
- **Web Interface:** Open `src\gui\web_hmi.html` in browser
- **System Monitor:** Run `python src\monitoring\system_status.py`

### 3. System Verification
```bash
# Run comprehensive system check
python utils\verification\verify_system.py

# Generate system diagrams
python utils\hvac_diagram.py
```

## Recent Updates

### Version 1.0 (June 2025)
- Initial system implementation
- Complete PLC programming suite
- Desktop and web-based HMI interfaces
- Comprehensive simulation engine
- System verification and validation tools
- Complete documentation package

## Support & Contact

### Technical Support
- **System Administrator:** hvac-admin@facility.com
- **Technical Lead:** tech-lead@facility.com
- **Emergency Contact:** (555) 123-4567 (24/7)

### Documentation
- **Installation Guide:** [docs/Installation_Guide.md](../docs/Installation_Guide.md)
- **Operating Procedures:** [docs/Operating_Procedures.md](../docs/Operating_Procedures.md)
- **Maintenance Manual:** [docs/Maintenance_Manual.md](../docs/Maintenance_Manual.md)
- **Troubleshooting Guide:** [docs/Troubleshooting_Guide.md](../docs/Troubleshooting_Guide.md)

## Wiki Guidelines

### Contributing
- Follow the established templates when creating new pages
- Include version control information
- Use consistent formatting and structure
- Add relevant cross-references and links

### Page Organization
- Use clear, descriptive headings
- Include table of contents for long pages
- Add relevant tags and categories
- Maintain current and accurate information

### Templates Available
- [Standard Page Template](templates/Page_Template.md)
- [Procedure Template](templates/Procedure_Template.md)
- [Troubleshooting Template](templates/Troubleshooting_Template.md)
- [Technical Reference Template](templates/Technical_Template.md)

---

**Wiki Version:** 1.0  
**Last Updated:** June 8, 2025  
**Maintained By:** HVAC System Documentation Team
