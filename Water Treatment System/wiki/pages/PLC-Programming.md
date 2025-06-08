# PLC Programming

## 📋 PLC System Overview

### Hardware Configuration
- **PLC Model:** Allen-Bradley CompactLogix 5370 L3
- **CPU:** 1769-L33ER (Ethernet/IP enabled)
- **I/O Modules:** 1769-IF4XOF2 (Analog), 1769-IQ16 (Digital Input), 1769-OW16 (Digital Output)
- **Communication:** Ethernet/IP, DeviceNet
- **Programming Software:** RSLogix 5000 / Studio 5000

### Program Structure
```
Main Program (Main.st)
├── Global Variables (global_vars.st)
├── Pump Controller (pump_controller.st)
├── Water Quality Controller (water_quality_controller.st)
└── Desalination Controller (desalination_controller.st)
```

## 🔧 Main Control Logic

### Main.st - Primary Control Routine
```iecst
PROGRAM Main
VAR
    system_mode : SYSTEM_MODE := AUTO;
    emergency_stop : BOOL := FALSE;
    startup_complete : BOOL := FALSE;
END_VAR

// System startup sequence
IF NOT emergency_stop AND system_mode = AUTO THEN
    // Call sub-controllers in sequence
    pump_control();
    water_quality_control();
    desalination_control();
    
    // Update HMI status
    hmi_status_update();
    
    startup_complete := TRUE;
ELSE
    // Emergency shutdown sequence
    emergency_shutdown();
    startup_complete := FALSE;
END_IF
```

### Global Variables (global_vars.st)
```iecst
TYPE SYSTEM_MODE :
(
    MANUAL := 0,
    AUTO := 1,
    MAINTENANCE := 2,
    EMERGENCY := 3
);
END_TYPE

VAR_GLOBAL
    // System Status
    system_running : BOOL := FALSE;
    emergency_stop : BOOL := FALSE;
    auto_mode : BOOL := TRUE;
    
    // Process Variables
    feed_pressure : REAL := 0.0;        // bar
    ro_pressure : REAL := 0.0;          // bar
    product_flow : REAL := 0.0;         // m³/h
    reject_flow : REAL := 0.0;          // m³/h
    product_conductivity : REAL := 0.0;  // µS/cm
    
    // Control Setpoints
    feed_pressure_sp : REAL := 4.5;     // bar
    ro_pressure_sp : REAL := 55.0;      // bar
    product_flow_sp : REAL := 10.0;     // m³/h
    conductivity_sp : REAL := 200.0;    // µS/cm
    
    // Safety Limits
    max_ro_pressure : REAL := 65.0;     // bar
    min_feed_pressure : REAL := 2.0;    // bar
    max_conductivity : REAL := 500.0;   // µS/cm
    
    // Equipment Status
    intake_pump_run : BOOL := FALSE;
    hp_pump_run : BOOL := FALSE;
    chemical_dosing_active : BOOL := FALSE;
    
    // Alarms
    high_pressure_alarm : BOOL := FALSE;
    low_pressure_alarm : BOOL := FALSE;
    high_conductivity_alarm : BOOL := FALSE;
    pump_fault_alarm : BOOL := FALSE;
END_VAR
```

## 🚰 Pump Control Logic

### pump_controller.st
```iecst
FUNCTION_BLOCK PumpController
VAR_INPUT
    enable : BOOL;
    pressure_setpoint : REAL;
    flow_setpoint : REAL;
END_VAR

VAR_OUTPUT
    pump_command : BOOL;
    pump_speed : REAL;  // 0-100%
END_VAR

VAR
    pid_pressure : PID_Controller;
    pid_flow : PID_Controller;
    pump_enabled : BOOL := FALSE;
END_VAR

// Pump enable logic
pump_enabled := enable AND 
                NOT emergency_stop AND 
                feed_pressure > min_feed_pressure;

IF pump_enabled THEN
    // PID control for pressure
    pid_pressure.setpoint := pressure_setpoint;
    pid_pressure.process_value := ro_pressure;
    pid_pressure.kp := 2.0;
    pid_pressure.ki := 0.5;
    pid_pressure.kd := 0.1;
    
    pid_pressure();
    
    // Limit pump speed output
    pump_speed := LIMIT(0.0, pid_pressure.output, 100.0);
    pump_command := pump_speed > 10.0;  // Minimum speed threshold
    
    // Safety interlocks
    IF ro_pressure > max_ro_pressure THEN
        pump_command := FALSE;
        high_pressure_alarm := TRUE;
    END_IF;
    
ELSE
    pump_command := FALSE;
    pump_speed := 0.0;
END_IF;
```

## 💧 Water Quality Control

### water_quality_controller.st
```iecst
FUNCTION_BLOCK WaterQualityController
VAR_INPUT
    enable : BOOL;
    conductivity_setpoint : REAL;
END_VAR

VAR_OUTPUT
    reject_valve_position : REAL;  // 0-100%
    chemical_dose_rate : REAL;     // ml/min
    quality_alarm : BOOL;
END_VAR

VAR
    pid_conductivity : PID_Controller;
    flush_timer : TON;
    cleaning_active : BOOL := FALSE;
END_VAR

IF enable AND system_running THEN
    // Conductivity control via reject valve
    pid_conductivity.setpoint := conductivity_setpoint;
    pid_conductivity.process_value := product_conductivity;
    pid_conductivity.kp := 1.5;
    pid_conductivity.ki := 0.3;
    pid_conductivity.kd := 0.05;
    
    pid_conductivity();
    
    // Reject valve positioning (inverse control)
    reject_valve_position := LIMIT(20.0, 50.0 - pid_conductivity.output, 80.0);
    
    // Chemical dosing control
    chemical_dose_rate := calculate_chemical_dose(feed_pressure, product_flow);
    
    // Quality alarm logic
    IF product_conductivity > max_conductivity THEN
        quality_alarm := TRUE;
        // Automatic flush sequence
        flush_timer(IN := TRUE, PT := T#300S);  // 5-minute flush
        IF flush_timer.Q THEN
            cleaning_active := TRUE;
        END_IF;
    ELSE
        quality_alarm := FALSE;
        flush_timer(IN := FALSE);
    END_IF;
    
ELSE
    reject_valve_position := 50.0;  // Default position
    chemical_dose_rate := 0.0;
    quality_alarm := FALSE;
END_IF;
```

## 🏭 Desalination Process Control

### desalination_controller.st
```iecst
FUNCTION_BLOCK DesalinationController
VAR_INPUT
    start_command : BOOL;
    stop_command : BOOL;
END_VAR

VAR_OUTPUT
    process_active : BOOL;
    recovery_rate : REAL;
    energy_consumption : REAL;
END_VAR

VAR
    startup_sequence : INT := 0;
    startup_timer : TON;
    process_timer : TON;
    shutdown_timer : TON;
END_VAR

CASE startup_sequence OF
    0: // Idle state
        IF start_command AND NOT stop_command THEN
            startup_sequence := 1;
        END_IF;
        process_active := FALSE;
        
    1: // Pre-treatment startup
        startup_timer(IN := TRUE, PT := T#30S);
        // Start pre-treatment pumps
        chemical_dosing_active := TRUE;
        IF startup_timer.Q THEN
            startup_sequence := 2;
            startup_timer(IN := FALSE);
        END_IF;
        
    2: // Low pressure flush
        startup_timer(IN := TRUE, PT := T#60S);
        intake_pump_run := TRUE;
        IF startup_timer.Q THEN
            startup_sequence := 3;
            startup_timer(IN := FALSE);
        END_IF;
        
    3: // High pressure ramp-up
        startup_timer(IN := TRUE, PT := T#120S);
        hp_pump_run := TRUE;
        // Gradual pressure increase logic here
        IF startup_timer.Q AND ro_pressure >= (ro_pressure_sp * 0.9) THEN
            startup_sequence := 4;
            startup_timer(IN := FALSE);
        END_IF;
        
    4: // Normal production
        process_active := TRUE;
        process_timer(IN := TRUE, PT := T#0S);  // Continuous operation
        
        // Calculate recovery rate
        IF feed_pressure > 0 AND product_flow > 0 THEN
            recovery_rate := (product_flow / (product_flow + reject_flow)) * 100.0;
        END_IF;
        
        // Calculate energy consumption
        energy_consumption := calculate_energy_usage(ro_pressure, product_flow);
        
        // Check for stop conditions
        IF stop_command OR emergency_stop THEN
            startup_sequence := 5;
            process_timer(IN := FALSE);
        END_IF;
        
    5: // Controlled shutdown
        shutdown_timer(IN := TRUE, PT := T#180S);
        // Gradual pressure reduction
        hp_pump_run := FALSE;
        IF shutdown_timer.Q THEN
            intake_pump_run := FALSE;
            chemical_dosing_active := FALSE;
            startup_sequence := 0;
            shutdown_timer(IN := FALSE);
        END_IF;
        process_active := FALSE;
        
END_CASE;
```

## 🔒 Safety Systems

### Emergency Shutdown Logic
```iecst
FUNCTION EmergencyShutdown : BOOL
VAR_INPUT
    trigger : BOOL;
END_VAR

VAR
    shutdown_active : BOOL := FALSE;
END_VAR

IF trigger OR emergency_stop THEN
    // Immediate pump shutdown
    hp_pump_run := FALSE;
    intake_pump_run := FALSE;
    
    // Close critical valves
    reject_valve_position := 100.0;  // Full open for pressure relief
    
    // Stop chemical dosing
    chemical_dosing_active := FALSE;
    
    // Set alarms
    pump_fault_alarm := TRUE;
    
    shutdown_active := TRUE;
    
    // Log emergency event
    log_emergency_event("Emergency shutdown activated");
END_IF;

EmergencyShutdown := shutdown_active;
```

### Pressure Safety Interlocks
```iecst
FUNCTION PressureSafetyCheck : BOOL
VAR
    pressure_ok : BOOL := TRUE;
END_VAR

// High pressure protection
IF ro_pressure > max_ro_pressure THEN
    pressure_ok := FALSE;
    high_pressure_alarm := TRUE;
    // Trigger emergency shutdown
    EmergencyShutdown(TRUE);
END_IF;

// Low suction pressure protection
IF feed_pressure < min_feed_pressure AND hp_pump_run THEN
    pressure_ok := FALSE;
    low_pressure_alarm := TRUE;
    // Stop high pressure pump to prevent cavitation
    hp_pump_run := FALSE;
END_IF;

PressureSafetyCheck := pressure_ok;
```

## 📊 HMI Interface Functions

### Status Update for HMI
```iecst
FUNCTION HMI_StatusUpdate : BOOL
VAR
    update_complete : BOOL := FALSE;
END_VAR

// Update process values for HMI display
hmi_data.feed_pressure := feed_pressure;
hmi_data.ro_pressure := ro_pressure;
hmi_data.product_flow := product_flow;
hmi_data.product_quality := product_conductivity;
hmi_data.recovery_rate := recovery_rate;

// Update equipment status
hmi_data.intake_pump_status := intake_pump_run;
hmi_data.hp_pump_status := hp_pump_run;
hmi_data.system_mode := system_mode;

// Update alarm status
hmi_data.alarm_count := COUNT_ACTIVE_ALARMS();
hmi_data.emergency_active := emergency_stop;

update_complete := TRUE;
HMI_StatusUpdate := update_complete;
```

---
*Document ID: PLC-WTS-2024-v1.0*  
*Last Updated: June 8, 2025*  
*Software Version: RSLogix 5000 v32.11*
