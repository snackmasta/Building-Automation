PROGRAM Main
VAR
    // Input variables - typically mapped to physical I/O
    StartButton     : BOOL := FALSE;    // I0.0 - Start button
    StopButton      : BOOL := FALSE;    // I0.1 - Stop button  
    EmergencyStop   : BOOL := FALSE;    // I0.2 - Emergency stop
    LevelSensor     : BOOL := FALSE;    // I0.3 - Tank level sensor
    TempSensor      : REAL := 20.0;     // IW0 - Temperature sensor (°C)
    PressureSensor  : REAL := 0.0;      // IW2 - Pressure sensor (bar)
    
    // Output variables - typically mapped to physical outputs
    Pump            : BOOL := FALSE;    // Q0.0 - Main pump
    Heater          : BOOL := FALSE;    // Q0.1 - Heating element
    Valve1          : BOOL := FALSE;    // Q0.2 - Inlet valve
    Valve2          : BOOL := FALSE;    // Q0.3 - Outlet valve
    AlarmLight      : BOOL := FALSE;    // Q0.4 - Red alarm light
    StatusLight     : BOOL := FALSE;    // Q0.5 - Green status light
    
    // Internal variables
    SystemRunning   : BOOL := FALSE;    // System state flag
    SystemReady     : BOOL := FALSE;    // System ready flag
    AlarmActive     : BOOL := FALSE;    // Alarm state
    CycleCount      : INT := 0;         // Production cycle counter
    
    // Setpoints and parameters
    SetTemperature  : REAL := 75.0;     // Temperature setpoint (°C)
    MaxPressure     : REAL := 5.0;      // Maximum pressure limit (bar)
    TempTolerance   : REAL := 2.0;      // Temperature tolerance (°C)
    
    // Timers
    StartupTimer    : TON;              // Startup delay timer
    HeatingTimer    : TON;              // Heating cycle timer
    PumpTimer       : TON;              // Pump run timer
    AlarmTimer      : TON;              // Alarm delay timer
    
    // Function block instances
    TempController  : PID_Controller;   // Temperature PID controller
END_VAR

// ===============================================
// MAIN PROGRAM LOGIC
// ===============================================

// System safety checks
SystemReady := NOT EmergencyStop AND 
               LevelSensor AND 
               (PressureSensor < MaxPressure) AND
               NOT AlarmActive;

// Start/Stop logic
IF StartButton AND SystemReady AND NOT SystemRunning THEN
    SystemRunning := TRUE;
    CycleCount := CycleCount + 1;
END_IF;

IF StopButton OR EmergencyStop OR AlarmActive THEN
    SystemRunning := FALSE;
END_IF;

// ===============================================
// PROCESS CONTROL LOGIC
// ===============================================

IF SystemRunning THEN
    // Startup sequence with delay
    StartupTimer(IN := TRUE, PT := T#2S);
    
    IF StartupTimer.Q THEN
        // Open inlet valve
        Valve1 := TRUE;
        
        // Start pump after valve opens
        PumpTimer(IN := TRUE, PT := T#1S);
        IF PumpTimer.Q THEN
            Pump := TRUE;
        END_IF;
        
        // Temperature control
        IF TempSensor < (SetTemperature - TempTolerance) THEN
            Heater := TRUE;
            HeatingTimer(IN := TRUE, PT := T#30S);
        ELSIF TempSensor > (SetTemperature + TempTolerance) THEN
            Heater := FALSE;
            HeatingTimer(IN := FALSE);
        END_IF;
        
        // Process completion check
        IF TempSensor >= SetTemperature AND HeatingTimer.Q THEN
            Valve2 := TRUE;  // Open outlet valve
        END_IF;
        
    END_IF;
    
ELSE
    // System stopped - reset all outputs
    StartupTimer(IN := FALSE);
    PumpTimer(IN := FALSE);
    HeatingTimer(IN := FALSE);
    Pump := FALSE;
    Heater := FALSE;
    Valve1 := FALSE;
    Valve2 := FALSE;
END_IF;

// ===============================================
// ALARM LOGIC
// ===============================================

// Check for alarm conditions
AlarmActive := (PressureSensor > MaxPressure) OR 
               (TempSensor > 100.0) OR
               (SystemRunning AND NOT LevelSensor);

// Alarm timer for debouncing
AlarmTimer(IN := AlarmActive, PT := T#500MS);

IF AlarmTimer.Q THEN
    AlarmLight := TRUE;
    SystemRunning := FALSE;  // Emergency shutdown
ELSE
    AlarmLight := FALSE;
END_IF;

// ===============================================
// STATUS INDICATORS
// ===============================================

// Status light shows system ready and running
StatusLight := SystemReady AND SystemRunning;

// Reset alarm when conditions clear
IF NOT AlarmActive AND NOT SystemRunning THEN
    AlarmActive := FALSE;
END_IF;

END_PROGRAM
