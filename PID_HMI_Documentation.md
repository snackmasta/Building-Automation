# P&ID and HMI Documentation

## Process & Instrumentation Diagram (P&ID)

The P&ID diagram provides a complete schematic representation of the industrial process control system, showing:

### Equipment Symbols
- **T-001**: Main process tank with heating capability
- **P-001**: Centrifugal pump for product transfer
- **E-001**: Electric heater installed in the tank
- **PV-001**: Inlet control valve (pneumatic)
- **PV-002**: Outlet control valve (pneumatic)

### Instrumentation
- **TT-001**: Temperature transmitter (4-20mA output)
- **TIC-001**: Temperature indicating controller
- **PT-001**: Pressure transmitter (4-20mA output)
- **PI-001**: Pressure indicator
- **LS-001**: Level switch (high/low indication)
- **FT-001**: Flow transmitter (on discharge line)

### Process Description
1. **Feed Material**: Enters through the inlet line and PV-001 valve
2. **Heating Process**: Material is heated in T-001 by electric heater E-001
3. **Temperature Control**: TIC-001 maintains temperature at setpoint via TT-001 feedback
4. **Product Transfer**: When temperature is reached, pump P-001 transfers product
5. **Discharge**: Product exits through PV-002 valve to storage/next process

### Safety Features
- Emergency shutdown capability
- High temperature alarm and shutdown
- High pressure alarm and shutdown
- Low level protection
- Manual emergency stop

## Human Machine Interface (HMI)

The HMI provides comprehensive monitoring and control capabilities:

### Main Screen Layout

#### Process Overview Panel
- **Real-time Process Diagram**: Visual representation of equipment status
- **Dynamic Color Coding**: 
  - Green: Equipment running normally
  - Red: Equipment stopped or in alarm
  - Blue: Tank with liquid present
  - Gray: Equipment offline
- **Live Process Values**: Temperature and pressure displayed on diagram

#### Control Panel
- **System Control Buttons**:
  - START: Initiates automatic process sequence
  - STOP: Safely stops the process
  - E-STOP: Emergency shutdown (red mushroom button style)

- **Operation Mode Selection**:
  - AUTO: Automatic PLC control based on setpoints
  - MANUAL: Direct operator control of individual equipment

- **Setpoint Entry**:
  - Temperature setpoint (20-100°C)
  - Pressure setpoint (0.5-8.0 bar)
  - Real-time setpoint adjustment capability

- **Manual Control Panel** (visible in manual mode):
  - Individual equipment control checkboxes
  - Direct operator override capability
  - Safety interlocks still active

#### Trends & Alarms Panel
- **Real-time Trends**:
  - Temperature trend with setpoint line
  - Pressure trend with setpoint line
  - 100-point rolling history
  - Automatic scaling

- **Active Alarms List**:
  - High temperature alarm (>90°C)
  - High pressure alarm (>5.0 bar)
  - Emergency stop status
  - Low level alarm
  - Time-stamped alarm log

#### Status Bar
- System status display (Running/Stopped/E-Stop)
- Real-time clock
- Connection status indicators

### HMI Features

#### Safety Integration
- **Emergency Stop**: Immediately stops all equipment
- **Alarm Management**: Visual and audible notifications
- **Interlock Monitoring**: Safety conditions continuously checked
- **Operator Permissions**: Mode-based access control

#### Process Control
- **Automatic Sequencing**: PLC-based startup/shutdown procedures
- **Manual Override**: Individual equipment control capability
- **Setpoint Management**: Real-time process parameter adjustment
- **Trend Analysis**: Historical data visualization

#### User Interface Design
- **Professional Industrial Look**: Dark theme with high contrast
- **Intuitive Layout**: Logical grouping of related functions
- **Clear Visual Feedback**: Color coding and status indicators
- **Responsive Design**: Real-time updates without user intervention

### Technical Specifications

#### HMI Software
- **Platform**: Python with Tkinter GUI framework
- **Graphics**: Matplotlib for trends and process graphics
- **Update Rate**: 1-second refresh cycle
- **Data Storage**: In-memory circular buffer (100 points)
- **Display Resolution**: Optimized for 1400x900 minimum

#### Communication Interface
- **Protocol**: Ethernet/IP (simulated)
- **Update Rate**: 100ms PLC scan time
- **Data Tags**: 20+ process variables
- **Alarm Handling**: Real-time event processing

#### Security Features
- **Access Levels**: Operator/Engineer/Maintenance
- **Audit Trail**: All operator actions logged
- **Password Protection**: Mode change restrictions
- **Backup System**: Automatic configuration backup

### Operating Procedures

#### Normal Startup
1. Verify all safety conditions (E-stop reset, level OK)
2. Set desired temperature and pressure setpoints
3. Select AUTO mode
4. Press START button
5. Monitor process through HMI displays
6. System will automatically sequence through startup

#### Normal Shutdown
1. Press STOP button
2. System automatically sequences equipment shutdown
3. Monitor until all equipment stops
4. Verify safe conditions achieved

#### Emergency Procedures
1. **Emergency Stop**: Press E-STOP button immediately
2. **High Temperature**: System auto-shuts down, acknowledge alarm
3. **High Pressure**: System auto-shuts down, acknowledge alarm
4. **Power Failure**: System fails to safe state

### Maintenance Features
- **Equipment Status Monitoring**: Real-time health indicators
- **Trend Analysis**: Historical performance data
- **Alarm History**: Maintenance scheduling support
- **Calibration Reminders**: Scheduled maintenance alerts

### Files Generated
- `pid_diagram.py` - P&ID generator script
- `pid_diagram.png` - High-resolution P&ID image
- `pid_diagram.pdf` - Vector format P&ID
- `hmi_interface.py` - Complete HMI application
- `generate_pid.bat` - P&ID generation script
- `run_hmi.bat` - HMI startup script

### Usage Instructions

#### Running the P&ID Generator
```bash
python pid_diagram.py
# or
generate_pid.bat
```

#### Starting the HMI
```bash
python hmi_interface.py
# or
run_hmi.bat
```

#### HMI Testing Procedure
1. Start HMI application
2. Observe initial STOPPED state
3. Press START to begin simulation
4. Monitor process values and trends
5. Test manual mode operation
6. Simulate alarm conditions
7. Test emergency stop functionality

This complete P&ID and HMI system provides professional-grade visualization and control capabilities for the industrial process control system.
