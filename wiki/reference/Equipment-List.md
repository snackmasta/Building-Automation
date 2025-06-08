# Equipment List

## Overview
This document provides a comprehensive list of all hardware components, software tools, and development equipment used across the three PLC automation projects in this repository.

## Hardware Components

### PLC Hardware
| Component | Model/Type | Project Usage | Specifications | Notes |
|-----------|------------|---------------|----------------|-------|
| **CPU Module** | S7-1200/1500 Series | All Projects | 32-bit processor, 1MB memory | Main control unit |
| **Digital I/O** | SM 1221/1222 | All Projects | 8-16 channels, 24V DC | Discrete inputs/outputs |
| **Analog I/O** | SM 1231/1232 | HVAC, Water Treatment | 4-8 channels, 0-10V/4-20mA | Process variables |
| **Communication** | CM 1241 Ethernet | All Projects | 10/100 Mbps | Network connectivity |
| **Power Supply** | PM 1207 | All Projects | 24V DC, 2.5A | System power |

### Sensors and Instruments
| Sensor Type | Model | Range | Application | Accuracy |
|-------------|-------|-------|-------------|----------|
| **Temperature** | PT100 RTD | -50°C to +200°C | HVAC zones | ±0.1°C |
| **Pressure** | Pressure Transmitter | 0-10 bar | Water treatment | ±0.25% |
| **Flow** | Electromagnetic | 0-100 L/min | Water systems | ±0.5% |
| **pH** | pH Electrode | 0-14 pH | Water treatment | ±0.02 pH |
| **Level** | Ultrasonic | 0-5m | Tank monitoring | ±1mm |
| **Humidity** | Capacitive | 0-100% RH | HVAC control | ±2% RH |
| **Air Quality** | CO2 Sensor | 0-5000 ppm | HVAC monitoring | ±50 ppm |

### Actuators and Control Elements
| Type | Model | Specifications | Application | Control Signal |
|------|-------|----------------|-------------|----------------|
| **Motor Starter** | Contactor + Overload | 0.1-32A | Pump/Fan control | 24V DC |
| **Variable Speed Drive** | VSD | 0.37-22 kW | Motor speed control | 4-20mA |
| **Control Valve** | Pneumatic Actuator | 2"-6" size | Flow control | 4-20mA |
| **Damper Actuator** | Electric Actuator | 0-90° rotation | Air flow control | 0-10V |
| **Solenoid Valve** | 2-way/3-way | 1/2"-2" size | On/off control | 24V DC |

### HMI and Visualization
| Component | Model | Screen Size | Resolution | Interface |
|-----------|-------|-------------|------------|-----------|
| **HMI Panel** | KTP700 Basic | 7" | 800x480 | Ethernet |
| **Industrial PC** | IPC677C | 15" | 1024x768 | Multiple interfaces |
| **Touch Panel** | TP700 Comfort | 7" | 800x480 | PROFINET |

## Software Tools

### Development Environment
| Software | Version | License Type | Purpose | Platform |
|----------|---------|--------------|---------|----------|
| **TIA Portal** | V17/V18 | Commercial | PLC Programming | Windows |
| **Python** | 3.8+ | Open Source | Simulation/HMI | Cross-platform |
| **WinCC** | V17 | Commercial | HMI Development | Windows |
| **Git** | Latest | Open Source | Version Control | Cross-platform |
| **VS Code** | Latest | Free | Code Editor | Cross-platform |

### PLC Programming Libraries
| Library | Standard | Purpose | Projects |
|---------|----------|---------|----------|
| **IEC 61131-3** | International | PLC Programming | All |
| **STEP 7 Basic** | Siemens | Function Blocks | All |
| **Safety Library** | TÜV Certified | Safety Functions | HVAC, Water |
| **Process Library** | Industrial | Process Control | Water Treatment |

### Simulation Tools
| Tool | Type | Capabilities | Integration |
|------|------|--------------|-------------|
| **PLCSIM** | Software | PLC Simulation | TIA Portal |
| **Factory I/O** | 3D Simulation | Process Visualization | Multiple PLCs |
| **Python Simulator** | Custom | Process Modeling | Direct Integration |

## Network Infrastructure

### Communication Protocols
| Protocol | Standard | Speed | Application | Security |
|----------|----------|-------|-------------|----------|
| **PROFINET** | IEC 61158 | 100 Mbps | Real-time I/O | Encrypted |
| **Modbus TCP** | Open Standard | 10/100 Mbps | Device Integration | SSL/TLS |
| **OPC UA** | IEC 62541 | Variable | Data Exchange | Certificate-based |
| **Ethernet/IP** | ODVA | 10/100 Mbps | Industrial Ethernet | Security features |

### Network Components
| Component | Type | Ports | Features | Application |
|-----------|------|-------|----------|-------------|
| **Industrial Switch** | Managed | 8-24 ports | VLAN, QoS | Network backbone |
| **Wireless Access Point** | Industrial | Wi-Fi 6 | Encryption | Mobile devices |
| **Firewall** | Industrial | Multiple | Deep inspection | Security boundary |

## Testing Equipment

### Measurement Instruments
| Instrument | Type | Range | Accuracy | Purpose |
|------------|------|-------|----------|---------|
| **Multimeter** | Digital | 0-1000V, 0-20A | ±0.1% | Electrical testing |
| **Oscilloscope** | Digital | 100 MHz | ±2% | Signal analysis |
| **Loop Calibrator** | Handheld | 4-20mA, 0-10V | ±0.025% | Analog calibration |
| **Network Tester** | Cable/Protocol | Ethernet/PROFINET | - | Network diagnostics |

### Calibration Standards
| Standard | Type | Range | Certification | Calibration Interval |
|----------|------|-------|---------------|---------------------|
| **Temperature** | Reference | -50°C to +200°C | NIST Traceable | 12 months |
| **Pressure** | Dead Weight | 0-100 bar | ISO 17025 | 12 months |
| **Current Source** | Precision | 4-20mA | NIST Traceable | 12 months |
| **Voltage Source** | Precision | 0-10V | NIST Traceable | 12 months |

## Safety Equipment

### Personal Protective Equipment (PPE)
| Equipment | Standard | Application | Replacement |
|-----------|----------|-------------|-------------|
| **Safety Glasses** | ANSI Z87.1 | Eye protection | As needed |
| **Hard Hat** | ANSI Z89.1 | Head protection | 5 years |
| **Safety Shoes** | ASTM F2413 | Foot protection | 1 year |
| **Insulated Gloves** | ASTM D120 | Electrical work | Annual test |

### Emergency Equipment
| Equipment | Type | Location | Inspection |
|-----------|------|----------|------------|
| **Fire Extinguisher** | Class C | Each panel | Monthly |
| **Emergency Stop** | Category 0 | Multiple locations | Weekly |
| **First Aid Kit** | Industrial | Control room | Monthly |
| **Eye Wash Station** | Plumbed | Chemical areas | Weekly |

## Spare Parts Inventory

### Critical Spares
| Component | Part Number | Quantity | Lead Time | Criticality |
|-----------|-------------|----------|-----------|-------------|
| **CPU Module** | 6ES7 214-1AG40 | 1 | 4 weeks | High |
| **I/O Modules** | Various | 2 each | 2 weeks | High |
| **Power Supply** | 6EP1 332-1SH71 | 1 | 1 week | High |
| **HMI Display** | 6AV2 123-2GB03 | 1 | 6 weeks | Medium |
| **Communication Module** | 6GK7 241-1CH30 | 1 | 3 weeks | Medium |

### Consumables
| Item | Usage | Reorder Point | Supplier |
|------|-------|---------------|----------|
| **Fuses** | Protection | 10 pieces | Local |
| **Terminal Blocks** | Wiring | 20 pieces | Local |
| **Cable** | Various sizes | 100m each | Distributor |
| **Labels** | Identification | 1000 pieces | Office supply |

## Vendor Information

### Primary Suppliers
| Vendor | Products | Contact | Support Level |
|--------|----------|---------|---------------|
| **Siemens** | PLC, HMI, Software | +1-800-XXX-XXXX | Premium |
| **Phoenix Contact** | I/O, Terminal blocks | +1-800-XXX-XXXX | Standard |
| **Schneider Electric** | Power, Protection | +1-800-XXX-XXXX | Standard |
| **Endress+Hauser** | Process instruments | +1-800-XXX-XXXX | Premium |

### Local Distributors
| Distributor | Location | Specialization | Delivery |
|-------------|----------|----------------|----------|
| **Industrial Supply Co.** | Local city | General automation | Same day |
| **Control Systems Inc.** | Regional | PLC/HMI systems | Next day |
| **Process Equipment Ltd.** | Regional | Instrumentation | 2-3 days |

## Recommended Procurement

### Minimum Setup (Project Example)
- Basic PLC with 8 I/O
- Simple HMI or PC interface
- Development software licenses
- Basic testing equipment
- **Estimated Cost: $5,000-$8,000**

### Standard Setup (HVAC System)
- Medium PLC with analog I/O
- 7" HMI panel
- Temperature and flow sensors
- Variable speed drives
- **Estimated Cost: $15,000-$25,000**

### Advanced Setup (Water Treatment)
- High-end PLC with safety functions
- Industrial PC with SCADA
- Complete instrumentation package
- Communication infrastructure
- **Estimated Cost: $35,000-$60,000**

## Maintenance Considerations

### Lifecycle Management
- **PLC Hardware**: 10-15 years typical life
- **HMI Displays**: 5-7 years (touchscreen wear)
- **Sensors**: 3-5 years (process dependent)
- **Software**: Annual updates recommended

### Technology Refresh
- Plan for technology updates every 5-7 years
- Maintain backward compatibility where possible
- Consider migration paths for obsolete components
- Budget 10-15% annually for updates and improvements

---

## Related Documentation
- [Technical Specifications](Technical-Specifications.md)
- [Standards Compliance](Standards-Compliance.md)
- [Maintenance Guide](../operations/Maintenance-Guide.md)
- [Safety Procedures](../operations/Safety-Procedures.md)

---
*Last Updated: June 2025*
*Document Version: 1.0*
*Review Cycle: Quarterly*
