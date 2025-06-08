# Project Example - Beginner PLC Tutorial

## Overview

The Project Example is a foundational learning module designed for newcomers to PLC programming and industrial automation. This simple yet comprehensive project introduces core concepts through a basic conveyor belt control system with sorting capabilities.

## 🎯 Learning Objectives

- **Fundamental PLC Programming**: Basic ladder logic, timers, and counters
- **I/O Configuration**: Digital and analog input/output handling
- **HMI Basics**: Simple operator interface design
- **System Integration**: Connecting components in a working system
- **Safety Principles**: Emergency stops and fail-safe operations

## 🔧 System Components

### Hardware Requirements
- **PLC**: Schneider Electric Modicon M221 or equivalent
- **Sensors**: 
  - 3x Proximity sensors (conveyor positions)
  - 1x Color sensor (part sorting)
  - 2x Limit switches (gate positions)
- **Actuators**:
  - 1x Conveyor motor (24V DC)
  - 2x Pneumatic cylinders (sorting gates)
- **HMI**: 7" Touch panel for basic control

### Software Stack
- **Programming**: Schneider Electric EcoStruxure Machine Expert - Basic
- **HMI Development**: Built-in HMI editor
- **Simulation**: Integrated simulator for testing

## 📚 Educational Value

### Beginner Concepts Covered
1. **Basic I/O Operations**
   - Digital input reading (sensors, switches)
   - Digital output control (motors, valves)
   - Understanding PLC scan cycle

2. **Fundamental Logic**
   - Simple start/stop circuits
   - Interlocking and safety logic
   - Basic sequencing operations

3. **Timer Applications**
   - Delay operations
   - Timeout protection
   - Cycle timing control

4. **Counter Functions**
   - Production counting
   - Batch operations
   - Quality tracking

### Project Progression
```
Week 1: Basic I/O and Start/Stop Control
Week 2: Adding Sensors and Feedback
Week 3: Implementing Safety Systems
Week 4: HMI Development and Integration
Week 5: Testing and Documentation
```

## 🚀 Quick Start

### Prerequisites
- Basic electrical knowledge
- Computer with Windows 10/11
- EcoStruxure Machine Expert - Basic (free download)

### Setup Steps
1. **Download Project Files**
   ```
   /Project Example/
   ├── src/
   │   ├── main.st           # Main program logic
   │   ├── safety.st         # Safety interlocks
   │   └── hmi.fhx          # HMI configuration
   ├── docs/
   │   ├── wiring-diagram.pdf
   │   └── io-list.xlsx
   └── simulation/
       └── conveyor-sim.zip
   ```

2. **Import Project**
   - Open EcoStruxure Machine Expert - Basic
   - File → Import → Select project archive
   - Configure PLC connection settings

3. **Run Simulation**
   - Enable simulation mode
   - Download program to virtual PLC
   - Test basic operations

## 💡 Key Learning Features

### Hands-On Exercises
- **Exercise 1**: Manual conveyor control
- **Exercise 2**: Automatic cycle with sensors
- **Exercise 3**: Part sorting logic
- **Exercise 4**: Production counting
- **Exercise 5**: Alarm handling

### Progressive Complexity
1. **Level 1**: Simple on/off control
2. **Level 2**: Sensor integration
3. **Level 3**: Automatic sequencing
4. **Level 4**: Quality control
5. **Level 5**: Data logging

## 🔍 Detailed Components

### Conveyor Control System
```
Process Flow:
Start → Load Part → Transport → Sort → Unload → Repeat
```

**Control Logic Features:**
- Emergency stop functionality
- Manual/Automatic mode selection
- Speed control with variable frequency drive
- Position tracking with encoders
- Fault detection and alarming

### Sorting Mechanism
- **Color Detection**: RGB sensor identifies part types
- **Pneumatic Actuation**: Sorting gates direct parts to correct bins
- **Position Control**: Precise timing for accurate sorting
- **Quality Tracking**: Count good/bad parts for reporting

### Safety Systems
- **Category 1 Safety**: Basic emergency stop circuit
- **Light Curtains**: Operator protection during manual mode
- **Lockout/Tagout**: Proper energy isolation procedures
- **Safety Documentation**: Risk assessment and mitigation

## 📖 Documentation Structure

### Student Materials
- **Lab Manual**: Step-by-step instructions
- **Theory Guide**: Fundamental concepts explained
- **Troubleshooting**: Common issues and solutions
- **Assessment**: Practical evaluation criteria

### Instructor Resources
- **Lesson Plans**: Structured teaching approach
- **Answer Keys**: Solutions to all exercises
- **Equipment Setup**: Hardware configuration guide
- **Assessment Rubrics**: Grading criteria

## 🛠️ Implementation Guide

### Phase 1: Basic Setup (Week 1)
- Install software and configure development environment
- Create new project and set up I/O configuration
- Implement simple start/stop logic
- Test with simulation

### Phase 2: Sensor Integration (Week 2)
- Add proximity sensors for position detection
- Implement conveyor sequencing logic
- Create status indication on HMI
- Test automatic operation

### Phase 3: Sorting Logic (Week 3)
- Integrate color sensor for part detection
- Program pneumatic gate control
- Implement sorting decision logic
- Add production counting

### Phase 4: Advanced Features (Week 4-5)
- Create comprehensive HMI interface
- Add data logging capabilities
- Implement alarm and fault handling
- Perform system testing and validation

## 🎓 Skills Development Path

### Entry Level (Project Example)
- Basic PLC concepts
- Simple ladder logic
- I/O fundamentals
- Safety basics

### Intermediate (HVAC System)
- Advanced control algorithms
- Multi-zone coordination
- Energy management
- System optimization

### Advanced (Water Treatment)
- Process control theory
- Complex state machines
- Data analytics
- Regulatory compliance

## 📋 Assessment Criteria

### Technical Competency
- [ ] Correct I/O configuration
- [ ] Functional ladder logic
- [ ] Proper safety implementation
- [ ] Working HMI interface
- [ ] Complete documentation

### Professional Skills
- [ ] Systematic troubleshooting approach
- [ ] Clear technical communication
- [ ] Adherence to safety procedures
- [ ] Quality documentation practices
- [ ] Continuous improvement mindset

## 🔗 Related Resources

### Wiki Navigation
- **[Repository Overview](../guides/Repository-Overview.md)** - Complete project comparison
- **[Quick Start Guide](../guides/Quick-Start-Guide.md)** - 5-minute setup
- **[PLC Programming Guide](../technical/PLC-Programming.md)** - Advanced concepts
- **[HMI Development](../technical/HMI-Development.md)** - Interface design

### External Learning
- **Schneider Electric University**: Free online courses
- **PLCOpen Standards**: Industry best practices
- **IEC 61131-3**: Programming language standards
- **Safety Standards**: IEC 61508, ISO 13849

---

## 📞 Support

### Getting Help
- **Discord Community**: #plc-beginners channel
- **Office Hours**: Tuesdays 2-4 PM EST
- **Email Support**: plc-help@automation-academy.edu
- **Video Tutorials**: YouTube playlist available

### Contributing
- **Feedback**: Suggest improvements to curriculum
- **Bug Reports**: Report issues with project files
- **Content Creation**: Share additional exercises
- **Peer Support**: Help other students learn

---

*This project is part of the Industrial PLC Control Systems Repository - designed to provide comprehensive, hands-on learning experiences in industrial automation and PLC programming.*
