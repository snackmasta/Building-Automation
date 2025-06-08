# Specifications

## 📊 System Performance Specifications

### Production Capacity
| Parameter | Specification | Units |
|-----------|---------------|-------|
| **Nominal Capacity** | 10,000 | L/hour |
| **Peak Capacity** | 12,000 | L/hour |
| **Minimum Operating Rate** | 6,000 | L/hour |
| **Daily Production** | 240,000 | L/day |
| **Annual Production** | 87.6 | ML/year |

### Water Quality Parameters
| Parameter | Feed Water | Product Water | Units |
|-----------|------------|---------------|-------|
| **Total Dissolved Solids (TDS)** | 35,000 | <250 | mg/L |
| **Conductivity** | 50,000 | <400 | µS/cm |
| **Chloride** | 19,000 | <50 | mg/L |
| **Sodium** | 10,500 | <20 | mg/L |
| **Sulfate** | 2,700 | <25 | mg/L |
| **pH** | 7.8-8.2 | 6.5-8.5 | pH units |
| **Turbidity** | <1.0 | <0.1 | NTU |
| **Total Hardness** | 6,000 | <50 | mg/L CaCO₃ |

### Process Performance
| Parameter | Specification | Units |
|-----------|---------------|-------|
| **Recovery Rate** | 45% (±2%) | % |
| **Salt Rejection** | >99.3% | % |
| **Energy Consumption** | 4.2 | kWh/m³ |
| **Specific Energy (SEC)** | 3.8 | kWh/m³ product |
| **Operating Pressure** | 50-60 | bar |
| **Feed Pressure** | 4-6 | bar |
| **System Availability** | >95% | % |

## ⚙️ Equipment Specifications

### Reverse Osmosis System
| Component | Specification |
|-----------|---------------|
| **Membrane Type** | Spiral wound polyamide |
| **Membrane Elements** | 8" × 40" (203mm × 1016mm) |
| **Number of Elements** | 24 elements (3 vessels × 8 elements) |
| **Membrane Area** | 37 m² per element |
| **Total Membrane Area** | 888 m² |
| **Pressure Vessels** | 8" FRP, 8-element configuration |
| **Design Pressure** | 83 bar |
| **Test Pressure** | 95 bar |

### High Pressure Pumps
| Parameter | Specification |
|-----------|---------------|
| **Type** | Centrifugal multistage |
| **Number of Pumps** | 2 (1 duty + 1 standby) |
| **Flow Rate** | 22 m³/h per pump |
| **Discharge Pressure** | 60 bar |
| **Motor Power** | 37 kW |
| **Motor Type** | 3-phase induction, IE3 efficiency |
| **Speed Control** | Variable Frequency Drive (VFD) |
| **Materials** | 316 stainless steel |

### Pre-Treatment System
| Component | Specification |
|-----------|---------------|
| **Raw Water Intake Pump** | 25 m³/h @ 6 bar, 11 kW |
| **Multimedia Filter** | 2.0m diameter × 2.5m height |
| **Filter Media** | Anthracite, sand, gravel layers |
| **Cartridge Filters** | 5µm polypropylene, 40" length |
| **Number of Cartridges** | 20 cartridges in parallel |
| **Chemical Dosing Pumps** | Diaphragm type, 0-20 L/h |

### Post-Treatment System
| Component | Specification |
|-----------|---------------|
| **Product Water Tank** | 50,000 L capacity, 316 SS |
| **Distribution Pump** | 15 m³/h @ 4 bar, 5.5 kW |
| **UV Disinfection** | 40 mJ/cm² minimum dose |
| **Chlorination System** | Sodium hypochlorite, 0-5 mg/L |
| **Final Polishing Filter** | 1µm absolute rating |

## 🔌 Electrical Specifications

### Power Requirements
| Parameter | Specification |
|-----------|---------------|
| **Total Connected Load** | 85 kW |
| **Operating Load** | 65 kW average |
| **Supply Voltage** | 400V, 3-phase, 50 Hz |
| **Power Factor** | >0.95 (with correction) |
| **Main Breaker** | 200A, 4-pole MCB |
| **Emergency Power** | UPS for controls (30 min backup) |

### Control System
| Component | Specification |
|-----------|---------------|
| **PLC** | Allen-Bradley CompactLogix 5370 |
| **CPU Module** | 1769-L33ER (2MB memory) |
| **I/O Modules** | 64 DI, 32 DO, 16 AI, 8 AO |
| **Communication** | Ethernet/IP, RS-485 |
| **HMI** | 15" color touchscreen × 2 units |
| **Remote Access** | VPN-enabled for remote monitoring |

### Instrumentation
| Instrument Type | Quantity | Specification |
|-----------------|----------|---------------|
| **Pressure Transmitters** | 12 | 4-20mA, 0-100 bar range |
| **Flow Meters** | 8 | Electromagnetic, ±0.5% accuracy |
| **Conductivity Analyzers** | 4 | 0-50,000 µS/cm range |
| **pH Analyzers** | 2 | 0-14 pH, ±0.1 pH accuracy |
| **Temperature Sensors** | 6 | RTD Pt100, ±0.2°C accuracy |
| **Level Transmitters** | 4 | Ultrasonic, 4-20mA output |

## 🏗️ Mechanical Specifications

### Piping and Valves
| Component | Material | Size | Rating |
|-----------|----------|------|---------|
| **High Pressure Piping** | 316 SS | DN50-DN100 | PN100 |
| **Low Pressure Piping** | 316 SS | DN80-DN150 | PN16 |
| **Feed Water Piping** | GRP/PVC | DN150-DN200 | PN10 |
| **Control Valves** | 316 SS trim | DN25-DN80 | PN100 |
| **Isolation Valves** | Ball valves, 316 SS | DN25-DN150 | PN16-PN100 |

### Structural Requirements
| Parameter | Specification |
|-----------|---------------|
| **Foundation** | Reinforced concrete, 200mm minimum |
| **Floor Loading** | 5 kN/m² minimum |
| **Seismic Design** | Zone 2 seismic resistance |
| **Corrosion Protection** | All exposed steel hot-dip galvanized |
| **Access Platforms** | Non-slip grating, safety railings |

## 🌡️ Environmental Specifications

### Operating Conditions
| Parameter | Range | Units |
|-----------|-------|-------|
| **Ambient Temperature** | 10-40 | °C |
| **Relative Humidity** | 20-80 | % |
| **Maximum Elevation** | 1000 | m above sea level |
| **Noise Level** | <75 | dB(A) at 1m |
| **Vibration** | <2.5 | mm/s RMS |

### Feed Water Quality Limits
| Parameter | Maximum | Units |
|-----------|---------|-------|
| **Temperature** | 35 | °C |
| **pH** | 6.5-8.5 | pH units |
| **SDI (15 min)** | 3.0 | - |
| **Turbidity** | 1.0 | NTU |
| **Free Chlorine** | 0.1 | mg/L |
| **Iron** | 0.3 | mg/L |
| **Manganese** | 0.1 | mg/L |
| **Hydrogen Sulfide** | 0.1 | mg/L |

## 🧪 Chemical Specifications

### Chemical Consumption
| Chemical | Purpose | Dosage | Annual Consumption |
|----------|---------|--------|-------------------|
| **Antiscalant** | Scale prevention | 2-4 mg/L | 200 kg/year |
| **Sodium Bisulfite** | Dechlorination | 2-3 mg/L per mg/L Cl₂ | 150 kg/year |
| **Citric Acid** | Membrane cleaning | 2% solution | 500 kg/year |
| **Sodium Hydroxide** | pH adjustment/cleaning | 0.1-0.5% solution | 300 kg/year |
| **Sodium Hypochlorite** | Disinfection | 1-2 mg/L | 100 kg/year |

### Storage Requirements
| Chemical | Storage Capacity | Material | Safety Features |
|----------|------------------|----------|-----------------|
| **Antiscalant** | 1000 L | HDPE | Spill containment |
| **Sodium Bisulfite** | 500 L | HDPE | Ventilation system |
| **Citric Acid** | 500 kg | Dry storage | Moisture protection |
| **Sodium Hydroxide** | 1000 L | HDPE | Emergency shower |
| **Sodium Hypochlorite** | 500 L | HDPE | Scrubber system |

## 📏 Physical Dimensions

### Equipment Layout
| Equipment | Length | Width | Height | Weight |
|-----------|--------|-------|--------|--------|
| **RO Skid** | 8.0 m | 3.0 m | 3.5 m | 12,000 kg |
| **Pre-treatment Skid** | 6.0 m | 2.5 m | 4.0 m | 8,000 kg |
| **Chemical Dosing Skid** | 2.0 m | 1.5 m | 2.5 m | 1,500 kg |
| **Control Panel** | 2.0 m | 0.8 m | 2.2 m | 500 kg |
| **Product Tank** | 4.0 m dia | 4.0 m dia | 5.0 m | 2,000 kg empty |

### Facility Requirements
| Parameter | Specification |
|-----------|---------------|
| **Total Floor Area** | 150 m² minimum |
| **Ceiling Height** | 6.0 m minimum |
| **Overhead Crane** | 5-ton capacity recommended |
| **Truck Access** | 4.0 m wide × 4.5 m high |
| **Drainage** | Floor drains every 25 m² |

---
*Document ID: SPEC-WTS-2024-v1.0*  
*Last Updated: June 8, 2025*  
*Specification Revision: Rev. C*
