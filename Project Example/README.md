# PLC Control System

This is a complete PLC program for an industrial process control system written in Structured Text (ST).

## Files Description

### PLC Program Files
- **main.st** - Main PLC program with process control logic
- **pid_controller.st** - PID controller function block for temperature control
- **global_vars.st** - Global variable declarations and user-defined types
- **plc_config.ini** - PLC configuration settings
- **plc_simulator.py** - Python simulator to test the PLC program

### P&ID and HMI Files
- **pid_diagram.py** - P&ID (Piping & Instrumentation Diagram) generator
- **pid_diagram.png** - Generated P&ID diagram (high resolution)
- **pid_diagram.pdf** - Generated P&ID diagram (vector format)
- **hmi_interface.py** - Professional desktop HMI application
- **web_hmi.html** - Web-based HMI interface
- **PID_HMI_Documentation.md** - Complete P&ID and HMI documentation

### Utility Files
- **run_simulator.bat** - Batch file to run PLC simulator
- **run_hmi.bat** - Batch file to start desktop HMI
- **generate_pid.bat** - Batch file to generate P&ID diagram
- **README.md** - This documentation file

## System Features

### Process Control
- Start/stop control with safety interlocks
- Temperature control with heating element
- Pressure monitoring and control
- Level sensor monitoring
- Two-valve system (inlet/outlet)
- Pump control with sequencing

### Safety Features
- Emergency stop functionality
- Over-temperature protection
- Over-pressure protection
- Level monitoring
- Alarm system with visual indicators

### Advanced Features
- PID temperature controller
- Timer-based sequencing
- Production cycle counting
- System status monitoring
- Configurable setpoints and parameters

## System Operation

### Normal Startup Sequence
1. Check all safety conditions (E-stop, level, pressure)
2. Press START button
3. System performs 2-second startup delay
4. Inlet valve opens
5. Pump starts after 1-second delay
6. Temperature control begins
7. When target temperature reached, outlet valve opens

### Safety Shutdown
The system will automatically shut down if:
- Emergency stop is activated
- Temperature exceeds 100°C
- Pressure exceeds maximum limit
- Level sensor indicates low level while running

## I/O Mapping

### Digital Inputs
| Address | Signal Name | Description | Type | Signal Level | Function |
|---------|-------------|-------------|------|--------------|----------|
| %I0.0 | START_BUTTON | Process start command | NO Contact | 24VDC | Operator start button |
| %I0.1 | STOP_BUTTON | Process stop command | NC Contact | 24VDC | Operator stop button |
| %I0.2 | EMERGENCY_STOP | Emergency shutdown | NC Contact | 24VDC | Safety emergency stop |
| %I0.3 | LEVEL_SENSOR | Tank level monitoring | Reed Switch | 24VDC | Low level detection |

### Analog Inputs
| Address | Signal Name | Description | Range | Signal Type | Calibration | Function |
|---------|-------------|-------------|-------|-------------|-------------|----------|
| %IW0 | TEMPERATURE | Process temperature | 0-120°C | 4-20mA | 4mA=0°C, 20mA=120°C | Temperature monitoring |
| %IW2 | PRESSURE | System pressure | 0-10 bar | 4-20mA | 4mA=0bar, 20mA=10bar | Pressure monitoring |

### Digital Outputs
| Address | Signal Name | Description | Type | Signal Level | Load Current | Function |
|---------|-------------|-------------|------|--------------|--------------|----------|
| %Q0.0 | MAIN_PUMP | Process circulation pump | Relay | 24VDC | 2A max | Fluid circulation |
| %Q0.1 | HEATER | Electric heating element | Relay | 24VDC | 5A max | Temperature control |
| %Q0.2 | INLET_VALVE | Tank inlet solenoid valve | Solenoid | 24VDC | 0.5A | Fluid inlet control |
| %Q0.3 | OUTLET_VALVE | Tank outlet solenoid valve | Solenoid | 24VDC | 0.5A | Fluid outlet control |
| %Q0.4 | ALARM_LIGHT | Red alarm indicator | LED | 24VDC | 0.1A | Fault indication |
| %Q0.5 | STATUS_LIGHT | Green status indicator | LED | 24VDC | 0.1A | Normal operation |

### I/O Summary
- **Total Digital Inputs**: 4 points
- **Total Analog Inputs**: 2 points (4-20mA)
- **Total Digital Outputs**: 6 points
- **Total Analog Outputs**: 0 points
- **Power Consumption**: ~20W total
- **Safety Category**: Basic (SIL 1 equivalent)

## Running the Applications

### PLC Simulator
The Python simulator allows you to test the PLC program logic without actual hardware.

#### Prerequisites
- Python 3.6 or higher

#### Running the Simulator
```bash
python plc_simulator.py
# or double-click
run_simulator.bat
```

### P&ID Diagram Generation
Generate professional P&ID diagrams showing the complete process layout.

#### Running the P&ID Generator
```bash
python pid_diagram.py
# or double-click
generate_pid.bat
```

This creates:
- `pid_diagram.png` (high-resolution image)
- `pid_diagram.pdf` (vector format for printing)

### HMI Interfaces

#### Desktop HMI Application
Professional industrial-style HMI with real-time process visualization.

```bash
python hmi_interface.py
# or double-click
run_hmi.bat
```

Features:
- Real-time process diagram
- Control panel with start/stop buttons
- Auto/Manual mode selection
- Setpoint adjustment
- Live trend plots
- Alarm management
- Professional industrial appearance

#### Web-Based HMI
Modern web interface accessible from any browser.

Simply open `web_hmi.html` in any web browser or use the Simple Browser in VS Code.

Features:
- Responsive design
- Interactive process diagram
- Real-time status updates
- Control capabilities
- Alarm notifications
- Cross-platform compatibility

### Simulator Commands
- `start` - Press start button
- `stop` - Press stop button
- `emergency` - Toggle emergency stop
- `temp <value>` - Set temperature sensor value
- `pressure <value>` - Set pressure sensor value
- `level` - Toggle level sensor
- `status` - Show system status
- `inputs` - Show all input values
- `outputs` - Show all output values
- `help` - Show available commands
- `quit` - Exit simulator

### Example Test Sequence
1. Start the simulator: `python plc_simulator.py`
2. Check status: `status`
3. Start the system: `start`
4. Monitor temperature: `temp 80` (set high temperature)
5. Check outputs: `outputs`
6. Stop the system: `stop`

## Configuration

Edit `plc_config.ini` to modify:
- PLC hardware settings
- Network configuration
- Safety parameters
- Timing settings
- I/O configuration

## Customization

### Adding New Features
1. Add variables to `global_vars.st`
2. Implement logic in `main.st`
3. Update simulator if needed
4. Test with simulator

### Modifying Control Logic
- Edit timing parameters in `main.st`
- Adjust PID parameters in `pid_controller.st`
- Update setpoints and limits as needed

## Technical Specifications

- **Scan Time**: 100ms (configurable)
- **Programming Language**: Structured Text (IEC 61131-3)
- **Target PLC**: Siemens S7-1200 series
- **Memory Usage**: ~2KB for program code
- **I/O Points**: 8 DI, 8 DO, 4 AI, 2 AO

## Safety Notes

⚠️ **WARNING**: This is a demonstration program. For actual industrial use:
- Perform thorough safety analysis
- Implement certified safety functions
- Follow relevant safety standards (ISO 13849, IEC 62061)
- Test extensively before deployment
- Validate all safety interlocks

## Support

For questions about this PLC program:
1. Review the code comments in the .st files
2. Check the simulator output for debugging
3. Refer to your PLC manufacturer's documentation
4. Follow IEC 61131-3 programming standards
