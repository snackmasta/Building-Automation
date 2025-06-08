(*
===============================================
GLOBAL VARIABLE DECLARATIONS
===============================================
This file contains all global variables, constants,
and type definitions for the PLC project.
*)

VAR_GLOBAL
    // System status variables
    SystemVersion       : STRING := 'PLC_Control_v1.0';
    SystemStartTime     : TIME;
    TotalRunHours       : REAL := 0.0;
    
    // Production statistics
    TotalCycles         : DINT := 0;
    SuccessfulCycles    : DINT := 0;
    FailedCycles        : DINT := 0;
    ProductionRate      : REAL := 0.0;     // Cycles per hour
    
    // System configuration
    AutoMode            : BOOL := TRUE;     // Auto/Manual mode
    MaintenanceMode     : BOOL := FALSE;    // Maintenance mode flag
    
    // Communication status
    HMI_Connected       : BOOL := FALSE;    // HMI connection status
    SCADA_Connected     : BOOL := FALSE;    // SCADA connection status
END_VAR

VAR_GLOBAL CONSTANT
    // Physical constants
    MAX_TEMPERATURE     : REAL := 120.0;    // Maximum safe temperature (°C)
    MIN_TEMPERATURE     : REAL := 10.0;     // Minimum operating temperature (°C)
    MAX_PRESSURE        : REAL := 10.0;     // Maximum system pressure (bar)
    
    // Timing constants
    STARTUP_DELAY       : TIME := T#5S;     // System startup delay
    SHUTDOWN_DELAY      : TIME := T#3S;     // System shutdown delay
    ALARM_DELAY         : TIME := T#1S;     // Alarm activation delay
    
    // Control parameters
    DEFAULT_TEMP_SP     : REAL := 75.0;     // Default temperature setpoint
    TEMP_DEADBAND       : REAL := 1.0;      // Temperature control deadband
    
    // I/O addresses (symbolic names)
    // Digital inputs
    DI_START_BUTTON     : STRING := '%I0.0';
    DI_STOP_BUTTON      : STRING := '%I0.1';
    DI_EMERGENCY_STOP   : STRING := '%I0.2';
    DI_LEVEL_SENSOR     : STRING := '%I0.3';
    
    // Analog inputs  
    AI_TEMPERATURE      : STRING := '%IW0';
    AI_PRESSURE         : STRING := '%IW2';
    
    // Digital outputs
    DO_PUMP             : STRING := '%Q0.0';
    DO_HEATER           : STRING := '%Q0.1';
    DO_VALVE_1          : STRING := '%Q0.2';
    DO_VALVE_2          : STRING := '%Q0.3';
    DO_ALARM_LIGHT      : STRING := '%Q0.4';
    DO_STATUS_LIGHT     : STRING := '%Q0.5';
END_VAR

(*
===============================================
USER DEFINED TYPES
===============================================
*)

TYPE SystemState : (
    STOPPED := 0,
    STARTING := 1,
    RUNNING := 2,
    STOPPING := 3,
    FAULT := 4,
    MAINTENANCE := 5
);
END_TYPE

TYPE AlarmLevel : (
    NO_ALARM := 0,
    WARNING := 1,
    ALARM := 2,
    CRITICAL := 3
);
END_TYPE

TYPE ProcessData : STRUCT
    Temperature         : REAL;
    Pressure           : REAL;
    FlowRate           : REAL;
    Level              : REAL;
    Timestamp          : DATE_AND_TIME;
END_STRUCT;
END_TYPE
