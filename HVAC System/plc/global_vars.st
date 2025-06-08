// Global Variables for HVAC Control System
// Date: June 8, 2025
// Version: 1.0.0

VAR_GLOBAL
    // System Configuration
    SYSTEM_NAME : STRING := 'HVAC Control System';
    SYSTEM_VERSION : STRING := '1.0.0';
    SCAN_TIME : TIME := T#100ms;
    
    // Zone Configuration
    ZONE_COUNT : INT := 8;
    ZONE_NAMES : ARRAY[1..8] OF STRING := [
        'Lobby',
        'Conference Room',
        'Office Area 1',
        'Office Area 2',
        'Kitchen',
        'Server Room',
        'Storage',
        'Break Room'
    ];
    
    // Temperature Control Constants
    DEFAULT_TEMP_HEATING : REAL := 21.0;     // °C
    DEFAULT_TEMP_COOLING : REAL := 24.0;     // °C
    TEMP_DEADBAND : REAL := 1.0;             // °C
    TEMP_ALARM_HIGH : REAL := 30.0;          // °C
    TEMP_ALARM_LOW : REAL := 15.0;           // °C
    
    // PID Control Parameters
    PID_KP : REAL := 0.8;    // Proportional gain
    PID_KI : REAL := 0.2;    // Integral gain
    PID_KD : REAL := 0.1;    // Derivative gain
    
    // Air Quality Constants
    CO2_SETPOINT : INT := 800;              // ppm
    CO2_ALARM_HIGH : INT := 1200;           // ppm
    HUMIDITY_SETPOINT : REAL := 50.0;       // %
    HUMIDITY_TOLERANCE : REAL := 10.0;      // %
    FRESH_AIR_MINIMUM : REAL := 15.0;       // %
    
    // Equipment Configuration
    SUPPLY_FAN_VFD : BOOL := TRUE;
    RETURN_FAN_VFD : BOOL := TRUE;
    COOLING_STAGES : INT := 2;
    HEATING_STAGES : INT := 2;
    ECONOMIZER_ENABLED : BOOL := TRUE;
    HEAT_RECOVERY_ENABLED : BOOL := TRUE;
    
    // Energy Management
    DEMAND_RESPONSE_ENABLED : BOOL := TRUE;
    PEAK_DEMAND_LIMIT : REAL := 100.0;      // kW
    OCCUPANCY_CONTROL : BOOL := TRUE;
    NIGHT_SETBACK_HEATING : REAL := 18.0;   // °C
    NIGHT_SETBACK_COOLING : REAL := 27.0;   // °C
    
    // Safety Parameters
    EMERGENCY_SHUTDOWN_ENABLED : BOOL := TRUE;
    FIRE_ALARM_INTEGRATION : BOOL := TRUE;
    FREEZE_PROTECTION_TEMP : REAL := 5.0;   // °C
    HIGH_TEMP_SHUTDOWN : REAL := 35.0;      // °C
    
    // Operating Schedule
    WEEKDAY_START : TIME_OF_DAY := TOD#07:00:00;
    WEEKDAY_END : TIME_OF_DAY := TOD#18:00:00;
    WEEKEND_START : TIME_OF_DAY := TOD#09:00:00;
    WEEKEND_END : TIME_OF_DAY := TOD#17:00:00;
    HOLIDAY_MODE : BOOL := FALSE;
    
    // Communication Settings
    HMI_PORT : INT := 8080;
    SIMULATOR_PORT : INT := 8081;
    MODBUS_PORT : INT := 502;
    UPDATE_INTERVAL : TIME := T#5s;
    
    // Maintenance Intervals
    FILTER_CHANGE_HOURS : REAL := 2160.0;   // 3 months
    BELT_INSPECTION_HOURS : REAL := 4320.0; // 6 months
    ANNUAL_MAINTENANCE_HOURS : REAL := 8760.0; // 1 year
    
    // Sensor Calibration Offsets
    TEMP_SENSOR_OFFSET : REAL := 0.0;
    HUMIDITY_SENSOR_OFFSET : REAL := 0.0;
    CO2_SENSOR_OFFSET : REAL := 0.0;
    PRESSURE_SENSOR_OFFSET : REAL := 0.0;
    
    // Runtime Data
    SYSTEM_START_TIME : DATE_AND_TIME;
    TOTAL_RUNTIME : TIME;
    ENERGY_CONSUMED : REAL;                  // kWh
    
    // Status Flags
    SYSTEM_INITIALIZED : BOOL := FALSE;
    FIRST_SCAN : BOOL := TRUE;
    SIMULATION_MODE : BOOL := FALSE;
    
END_VAR

VAR_GLOBAL CONSTANT
    // Physical Constants
    AIR_DENSITY : REAL := 1.225;           // kg/m³ at 15°C
    SPECIFIC_HEAT_AIR : REAL := 1.006;     // kJ/kg·K
    
    // Conversion Factors
    CFM_TO_M3S : REAL := 0.000471947;      // CFM to m³/s
    INCH_WC_TO_PA : REAL := 248.84;        // Inches of water to Pascals
    BTU_TO_KW : REAL := 0.000293071;       // BTU/hr to kW
    
    // Time Constants
    ONE_HOUR : TIME := T#1h;
    ONE_DAY : TIME := T#24h;
    ONE_WEEK : TIME := T#168h;
    
    // Equipment Limits
    MIN_FAN_SPEED : REAL := 20.0;          // %
    MAX_FAN_SPEED : REAL := 100.0;         // %
    MIN_DAMPER_POSITION : REAL := 0.0;     // %
    MAX_DAMPER_POSITION : REAL := 100.0;   // %
    
END_VAR
