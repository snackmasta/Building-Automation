FUNCTION_BLOCK TemperatureController
VAR_INPUT
    zone_number : INT;
    current_temp : REAL;
    setpoint_heating : REAL;
    setpoint_cooling : REAL;
    occupancy : BOOL;
    manual_override : BOOL;
END_VAR

VAR_OUTPUT
    heating_demand : BOOL;
    cooling_demand : BOOL;
    demand_level : REAL; // 0.0 to 1.0
    zone_fault : BOOL;
END_VAR

VAR
    pid_heating : PID;
    pid_cooling : PID;
    temp_error : REAL;
    deadband_high : REAL;
    deadband_low : REAL;
    last_temp : REAL;
    temp_change_rate : REAL;
    alarm_timer : TON;
    fault_timer : TON;
    
    // Night setback variables
    effective_setpoint_heating : REAL;
    effective_setpoint_cooling : REAL;
    
    // Alarm conditions
    high_temp_alarm : BOOL;
    low_temp_alarm : BOOL;
    sensor_fault : BOOL;
END_VAR

// Calculate effective setpoints (considering night setback)
IF NOT occupancy AND NOT manual_override THEN
    effective_setpoint_heating := NIGHT_SETBACK_HEATING;
    effective_setpoint_cooling := NIGHT_SETBACK_COOLING;
ELSE
    effective_setpoint_heating := setpoint_heating;
    effective_setpoint_cooling := setpoint_cooling;
END_IF;

// Calculate deadband limits
deadband_low := effective_setpoint_heating - (TEMP_DEADBAND / 2.0);
deadband_high := effective_setpoint_cooling + (TEMP_DEADBAND / 2.0);

// Temperature change rate calculation
temp_change_rate := (current_temp - last_temp) / (TIME_TO_REAL(SCAN_TIME) / 1000.0);
last_temp := current_temp;

// Sensor fault detection
IF current_temp < -50.0 OR current_temp > 80.0 THEN
    sensor_fault := TRUE;
ELSE
    sensor_fault := FALSE;
END_IF;

// Temperature alarm detection
high_temp_alarm := current_temp > TEMP_ALARM_HIGH;
low_temp_alarm := current_temp < TEMP_ALARM_LOW;

// Fault timer for persistent alarms
fault_timer(IN := (high_temp_alarm OR low_temp_alarm OR sensor_fault), PT := T#30s);
zone_fault := fault_timer.Q;

// Main control logic (only if no sensor fault)
IF NOT sensor_fault THEN
    
    // Heating Control
    IF current_temp < deadband_low THEN
        heating_demand := TRUE;
        cooling_demand := FALSE;
        
        // PID control for heating
        pid_heating(
            AUTO := TRUE,
            PV := current_temp,
            SP := effective_setpoint_heating,
            KP := PID_KP,
            TI := T#300s,
            TD := T#60s,
            CYCLE := SCAN_TIME
        );
        
        demand_level := LIMIT(0.0, pid_heating.CV / 100.0, 1.0);
        
    // Cooling Control
    ELSIF current_temp > deadband_high THEN
        cooling_demand := TRUE;
        heating_demand := FALSE;
        
        // PID control for cooling
        pid_cooling(
            AUTO := TRUE,
            PV := current_temp,
            SP := effective_setpoint_cooling,
            KP := PID_KP,
            TI := T#300s,
            TD := T#60s,
            CYCLE := SCAN_TIME
        );
        
        demand_level := LIMIT(0.0, pid_cooling.CV / 100.0, 1.0);
        
    // Dead band - no heating or cooling
    ELSE
        heating_demand := FALSE;
        cooling_demand := FALSE;
        demand_level := 0.0;
        
        // Reset PID controllers
        pid_heating(AUTO := FALSE);
        pid_cooling(AUTO := FALSE);
    END_IF;
    
ELSE
    // Sensor fault - safe mode
    heating_demand := FALSE;
    cooling_demand := FALSE;
    demand_level := 0.0;
END_IF;

END_FUNCTION_BLOCK

// Main Temperature Controller Function
FUNCTION TemperatureControllerMain : BOOL
VAR
    i : INT;
    zone_controller : ARRAY[1..8] OF TemperatureController;
    total_heating_demand : INT := 0;
    total_cooling_demand : INT := 0;
END_VAR

// Process each zone
FOR i := 1 TO ZONE_COUNT DO
    zone_controller[i](
        zone_number := i,
        current_temp := zone_temps[i],
        setpoint_heating := zone_setpoints[i],
        setpoint_cooling := zone_setpoints[i] + 3.0, // 3°C cooling offset
        occupancy := occupancy_detected[i],
        manual_override := FALSE
    );
    
    // Update global arrays
    zone_heating_demand[i] := zone_controller[i].heating_demand;
    zone_cooling_demand[i] := zone_controller[i].cooling_demand;
    
    // Count total demands
    IF zone_controller[i].heating_demand THEN
        total_heating_demand := total_heating_demand + 1;
    END_IF;
    
    IF zone_controller[i].cooling_demand THEN
        total_cooling_demand := total_cooling_demand + 1;
    END_IF;
END_FOR;

// Update system demand indicators
any_heating_demand := total_heating_demand > 0;
any_cooling_demand := total_cooling_demand > 0;

TemperatureControllerMain := TRUE;

END_FUNCTION

// Function: Initialize Zone Setpoints
FUNCTION InitializeZoneSetpoints : BOOL
VAR
    i : INT;
END_VAR

FOR i := 1 TO ZONE_COUNT DO
    CASE i OF
        1: zone_setpoints[i] := 22.0; // Lobby
        2: zone_setpoints[i] := 23.0; // Conference Room
        3, 4: zone_setpoints[i] := 22.0; // Office Areas
        5: zone_setpoints[i] := 21.0; // Kitchen
        6: zone_setpoints[i] := 20.0; // Server Room (cooler)
        7: zone_setpoints[i] := 18.0; // Storage (minimal heating)
        8: zone_setpoints[i] := 22.0; // Break Room
    ELSE
        zone_setpoints[i] := DEFAULT_TEMP_HEATING;
    END_CASE;
END_FOR;

InitializeZoneSetpoints := TRUE;

END_FUNCTION

// Function: Adaptive Temperature Control
FUNCTION AdaptiveTempControl : BOOL
VAR
    i : INT;
    outdoor_temp_factor : REAL;
    occupancy_factor : REAL;
    time_of_day : TIME_OF_DAY;
END_VAR

time_of_day := TIME_OF_DAY();

// Adjust setpoints based on outdoor temperature
IF outdoor_temp < 0.0 THEN
    outdoor_temp_factor := 1.0; // Colder setpoint offset
ELSIF outdoor_temp > 30.0 THEN
    outdoor_temp_factor := -1.0; // Warmer setpoint offset
ELSE
    outdoor_temp_factor := 0.0; // No adjustment
END_IF;

// Adjust setpoints based on time of day and occupancy
FOR i := 1 TO ZONE_COUNT DO
    // Morning warm-up
    IF time_of_day >= TOD#06:00:00 AND time_of_day <= TOD#08:00:00 THEN
        zone_setpoints[i] := zone_setpoints[i] + 1.0;
    END_IF;
    
    // Afternoon adjustment
    IF time_of_day >= TOD#14:00:00 AND time_of_day <= TOD#16:00:00 THEN
        zone_setpoints[i] := zone_setpoints[i] - 0.5;
    END_IF;
    
    // Apply outdoor temperature compensation
    zone_setpoints[i] := zone_setpoints[i] + outdoor_temp_factor;
    
    // Limit setpoint ranges
    zone_setpoints[i] := LIMIT(18.0, zone_setpoints[i], 26.0);
END_FOR;

AdaptiveTempControl := TRUE;

END_FUNCTION
