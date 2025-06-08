// Water Treatment System Global Variables
// Author: PLC Control System
// Date: June 2025

TYPE
    // System operating modes
    SystemMode : (
        STOPPED,        // System stopped
        STARTUP,        // System starting up
        RUNNING,        // Normal operation
        SHUTDOWN,       // Controlled shutdown
        MAINTENANCE,    // Maintenance mode
        ALARM          // Alarm state
    );
    
    // Water quality structure
    WaterQuality : STRUCT
        TDS         : REAL;     // Total Dissolved Solids (ppm)
        pH          : REAL;     // pH level (0-14)
        Conductivity : REAL;    // Electrical conductivity (µS/cm)
        Turbidity   : REAL;     // Turbidity (NTU)
        Chlorine    : REAL;     // Free chlorine (mg/L)
        Temperature : REAL;     // Water temperature (°C)
        Pressure    : REAL;     // Water pressure (bar)
        FlowRate    : REAL;     // Flow rate (L/min)
    END_STRUCT;
    
    // Tank information structure
    TankInfo : STRUCT
        Level       : REAL;     // Tank level (%)
        Volume      : REAL;     // Current volume (L)
        Capacity    : REAL;     // Tank capacity (L)
        Temperature : REAL;     // Water temperature (°C)
        LowAlarm    : BOOL;     // Low level alarm
        HighAlarm   : BOOL;     // High level alarm
        EmptyAlarm  : BOOL;     // Empty tank alarm
    END_STRUCT;
    
    // Pump status structure
    PumpStatus : STRUCT
        Running     : BOOL;     // Pump running status
        Speed       : REAL;     // Pump speed (%)
        Current     : REAL;     // Motor current (A)
        Pressure    : REAL;     // Discharge pressure (bar)
        FlowRate    : REAL;     // Flow rate (L/min)
        Hours       : REAL;     // Operating hours
        Fault       : BOOL;     // Pump fault status
        Maintenance : BOOL;     // Maintenance required
    END_STRUCT;
    
    // RO membrane status
    ROStatus : STRUCT
        Pressure    : REAL;     // Operating pressure (bar)
        Recovery    : REAL;     // Recovery rate (%)
        Rejection   : REAL;     // Salt rejection rate (%)
        Permeate    : REAL;     // Permeate flow (L/min)
        Concentrate : REAL;     // Concentrate flow (L/min)
        TMP         : REAL;     // Trans-membrane pressure (bar)
        Fouling     : REAL;     // Fouling indicator (%)
        CleanCycle  : INT;      // Cleaning cycles count
    END_STRUCT;
    
END_TYPE

VAR_GLOBAL
    // System control variables
    g_SystemMode        : SystemMode := STOPPED;
    g_SystemRunning     : BOOL := FALSE;
    g_EmergencyStop     : BOOL := FALSE;
    g_MaintenanceMode   : BOOL := FALSE;
    g_AutoMode          : BOOL := TRUE;
    
    // Digital inputs - Field devices
    g_SeawaterIntake    : BOOL := FALSE;    // I0.0 - Seawater intake valve
    g_StartButton       : BOOL := FALSE;    // I0.1 - System start button
    g_StopButton        : BOOL := FALSE;    // I0.2 - System stop button
    g_EmergencyButton   : BOOL := FALSE;    // I0.3 - Emergency stop button
    g_GroundTankLow     : BOOL := FALSE;    // I0.4 - Ground tank low level
    g_GroundTankHigh    : BOOL := FALSE;    // I0.5 - Ground tank high level
    g_RoofTankLow       : BOOL := FALSE;    // I0.6 - Roof tank low level
    g_RoofTankHigh      : BOOL := FALSE;    // I0.7 - Roof tank high level
    g_LeakDetector1     : BOOL := FALSE;    // I1.0 - Leak detector zone 1
    g_LeakDetector2     : BOOL := FALSE;    // I1.1 - Leak detector zone 2
    g_ROHighPressure    : BOOL := FALSE;    // I1.2 - RO high pressure alarm
    g_FilterClogged     : BOOL := FALSE;    // I1.3 - Pre-filter clogged
    
    // Digital outputs - Control devices
    g_IntakePump        : BOOL := FALSE;    // Q0.0 - Seawater intake pump
    g_PreFilterPump     : BOOL := FALSE;    // Q0.1 - Pre-filtration pump
    g_ROPump            : BOOL := FALSE;    // Q0.2 - RO high pressure pump
    g_BoosterPump1      : BOOL := FALSE;    // Q0.3 - Distribution pump 1
    g_BoosterPump2      : BOOL := FALSE;    // Q0.4 - Distribution pump 2
    g_IntakeValve       : BOOL := FALSE;    // Q0.5 - Seawater intake valve
    g_ROPermeateValve   : BOOL := FALSE;    // Q0.6 - RO permeate valve
    g_ConcentrateValve  : BOOL := FALSE;    // Q0.7 - Concentrate discharge valve
    g_GroundTankValve   : BOOL := FALSE;    // Q1.0 - Ground tank inlet valve
    g_RoofTankValve     : BOOL := FALSE;    // Q1.1 - Roof tank inlet valve
    g_ChlorineDosingPump : BOOL := FALSE;   // Q1.2 - Chlorine dosing pump
    g_pHDosingPump      : BOOL := FALSE;    // Q1.3 - pH adjustment pump
    g_UVSterilizer      : BOOL := FALSE;    // Q1.4 - UV sterilizer
    g_SystemAlarm       : BOOL := FALSE;    // Q1.5 - System alarm horn
    g_StatusLight       : BOOL := FALSE;    // Q1.6 - System status light
    g_AlarmLight        : BOOL := FALSE;    // Q1.7 - Alarm indicator light
    
    // Analog inputs - Sensors
    g_SeawaterTDS       : REAL := 35000.0;  // IW0 - Seawater TDS (ppm)
    g_SeawaterTemp      : REAL := 25.0;     // IW1 - Seawater temperature (°C)
    g_GroundTankLevel   : REAL := 0.0;      // IW2 - Ground tank level (%)
    g_RoofTankLevel     : REAL := 0.0;      // IW3 - Roof tank level (%)
    g_ROPressure        : REAL := 0.0;      // IW4 - RO operating pressure (bar)
    g_DistributionPressure : REAL := 0.0;  // IW5 - Distribution pressure (bar)
    g_PermeateFlow      : REAL := 0.0;      // IW6 - RO permeate flow (L/min)
    g_ConcentrateFlow   : REAL := 0.0;      // IW7 - RO concentrate flow (L/min)
    g_ProductTDS        : REAL := 0.0;      // IW8 - Product water TDS (ppm)
    g_ProductpH         : REAL := 7.0;      // IW9 - Product water pH
    g_ProductTurbidity  : REAL := 0.0;      // IW10 - Product turbidity (NTU)
    g_ChlorineLevel     : REAL := 0.0;      // IW11 - Chlorine residual (mg/L)
    
    // Analog outputs - Control signals
    g_IntakePumpSpeed   : REAL := 0.0;      // QW0 - Intake pump VFD (%)
    g_ROPumpSpeed       : REAL := 0.0;      // QW1 - RO pump VFD (%)
    g_BoosterSpeed1     : REAL := 0.0;      // QW2 - Booster pump 1 VFD (%)
    g_BoosterSpeed2     : REAL := 0.0;      // QW3 - Booster pump 2 VFD (%)
    g_ChlorineRate      : REAL := 0.0;      // QW4 - Chlorine dosing rate (%)
    g_pHDoseRate        : REAL := 0.0;      // QW5 - pH dosing rate (%)
    
    // System data structures
    g_SeawaterQuality   : WaterQuality;
    g_ProductQuality    : WaterQuality;
    g_GroundTank        : TankInfo;
    g_RoofTank          : TankInfo;
    g_IntakePumpData    : PumpStatus;
    g_ROPumpData        : PumpStatus;
    g_BoosterPump1Data  : PumpStatus;
    g_BoosterPump2Data  : PumpStatus;
    g_ROSystemData      : ROStatus;
    
    // Process setpoints and limits
    g_ROPressureSetpoint    : REAL := 55.0;     // RO pressure setpoint (bar)
    g_ProductTDSLimit       : REAL := 500.0;    // Max product TDS (ppm)
    g_ProductpHMin          : REAL := 6.5;      // Min product pH
    g_ProductpHMax          : REAL := 8.5;      // Max product pH
    g_ChlorineSetpoint      : REAL := 0.5;      // Chlorine setpoint (mg/L)
    g_GroundTankSetpoint    : REAL := 80.0;     // Ground tank level setpoint (%)
    g_RoofTankSetpoint      : REAL := 90.0;     // Roof tank level setpoint (%)
    g_DistPressureSetpoint  : REAL := 3.5;     // Distribution pressure setpoint (bar)
    
    // System timers and counters
    g_ProductionTime        : TIME := T#0s;     // Total production time
    g_ProductionVolume      : REAL := 0.0;      // Total production volume (L)
    g_DailyProduction       : REAL := 0.0;      // Daily production (L)
    g_SystemUptime          : TIME := T#0s;     // System uptime
    g_LastMaintenanceTime   : TIME := T#0s;     // Last maintenance timestamp
    g_ROCleaningCycles      : INT := 0;         // RO cleaning cycle count
    g_FilterReplacements    : INT := 0;         // Filter replacement count
    
    // Alarm and status flags
    g_WaterQualityAlarm     : BOOL := FALSE;    // Water quality alarm
    g_TankLevelAlarm        : BOOL := FALSE;    // Tank level alarm
    g_PumpFaultAlarm        : BOOL := FALSE;    // Pump fault alarm
    g_ROSystemAlarm         : BOOL := FALSE;    // RO system alarm
    g_LeakageAlarm          : BOOL := FALSE;    // Water leakage alarm
    g_MaintenanceAlarm      : BOOL := FALSE;    // Maintenance required alarm
    g_PowerFailureAlarm     : BOOL := FALSE;    // Power failure alarm
    g_CommunicationAlarm    : BOOL := FALSE;    // Communication alarm
    
    // Energy monitoring
    g_PowerConsumption      : REAL := 0.0;      // Total power consumption (kW)
    g_EnergyToday           : REAL := 0.0;      // Energy consumed today (kWh)
    g_EnergyTotal           : REAL := 0.0;      // Total energy consumed (kWh)
    g_SpecificEnergy        : REAL := 0.0;      // Specific energy (kWh/m³)
    
END_VAR
