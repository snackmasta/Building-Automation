FUNCTION_BLOCK AirQualityController
VAR_INPUT
    zone_number : INT;
    co2_level : INT;           // ppm
    humidity_level : REAL;     // %
    occupancy : BOOL;
    manual_override : BOOL;
END_VAR

VAR_OUTPUT
    fresh_air_demand : REAL;   // 0-100%
    exhaust_demand : REAL;     // 0-100%
    humidity_alarm : BOOL;
    co2_alarm : BOOL;
    air_quality_fault : BOOL;
END_VAR

VAR
    co2_pid : PID;
    humidity_pid : PID;
    co2_error : REAL;
    humidity_error : REAL;
    
    // Alarm timers
    co2_alarm_timer : TON;
    humidity_alarm_timer : TON;
    
    // Demand calculation
    base_fresh_air : REAL;
    occupancy_fresh_air : REAL;
    total_fresh_air_demand : REAL;
    
    // Sensor fault detection
    co2_sensor_fault : BOOL;
    humidity_sensor_fault : BOOL;
    
    // Historical data for trending
    co2_trend : ARRAY[1..10] OF INT;
    humidity_trend : ARRAY[1..10] OF REAL;
    trend_index : INT := 1;
END_VAR

// Sensor fault detection
co2_sensor_fault := (co2_level < 300 OR co2_level > 5000);
humidity_sensor_fault := (humidity_level < 0.0 OR humidity_level > 100.0);
air_quality_fault := co2_sensor_fault OR humidity_sensor_fault;

// Update trending data
co2_trend[trend_index] := co2_level;
humidity_trend[trend_index] := humidity_level;
trend_index := trend_index + 1;
IF trend_index > 10 THEN
    trend_index := 1;
END_IF;

// CO2 Control Logic
IF NOT co2_sensor_fault THEN
    co2_error := REAL(co2_level - CO2_SETPOINT);
    
    // CO2 alarm detection
    co2_alarm_timer(IN := (co2_level > CO2_ALARM_HIGH), PT := T#5m);
    co2_alarm := co2_alarm_timer.Q;
    
    // PID control for CO2
    co2_pid(
        AUTO := TRUE,
        PV := REAL(co2_level),
        SP := REAL(CO2_SETPOINT),
        KP := 0.5,
        TI := T#600s,
        TD := T#30s,
        CYCLE := SCAN_TIME
    );
    
    // Calculate fresh air demand based on CO2
    IF co2_level > CO2_SETPOINT THEN
        fresh_air_demand := LIMIT(FRESH_AIR_MINIMUM, co2_pid.CV, 100.0);
    ELSE
        fresh_air_demand := FRESH_AIR_MINIMUM;
    END_IF;
    
ELSE
    // Sensor fault - use maximum fresh air
    fresh_air_demand := 50.0; // Conservative value
    co2_alarm := TRUE;
END_IF;

// Humidity Control Logic
IF NOT humidity_sensor_fault THEN
    humidity_error := humidity_level - HUMIDITY_SETPOINT;
    
    // Humidity alarm detection (high or low)
    humidity_alarm_timer(
        IN := (humidity_level > (HUMIDITY_SETPOINT + HUMIDITY_TOLERANCE) OR
               humidity_level < (HUMIDITY_SETPOINT - HUMIDITY_TOLERANCE)),
        PT := T#10m
    );
    humidity_alarm := humidity_alarm_timer.Q;
    
    // Humidity control through exhaust
    IF humidity_level > (HUMIDITY_SETPOINT + HUMIDITY_TOLERANCE) THEN
        exhaust_demand := LIMIT(0.0, ABS(humidity_error) * 5.0, 80.0);
    ELSE
        exhaust_demand := 0.0;
    END_IF;
    
ELSE
    // Sensor fault
    exhaust_demand := 0.0;
    humidity_alarm := TRUE;
END_IF;

// Occupancy-based adjustments
IF occupancy THEN
    occupancy_fresh_air := 25.0; // Higher fresh air for occupied zones
ELSE
    occupancy_fresh_air := FRESH_AIR_MINIMUM;
END_IF;

// Final fresh air demand calculation
total_fresh_air_demand := MAX(fresh_air_demand, occupancy_fresh_air);

// Manual override handling
IF manual_override THEN
    // Manual mode - maintain minimum fresh air only
    fresh_air_demand := FRESH_AIR_MINIMUM;
    exhaust_demand := 0.0;
ELSE
    fresh_air_demand := total_fresh_air_demand;
END_IF;

END_FUNCTION_BLOCK

// Main Air Quality Controller Function
FUNCTION AirQualityControllerMain : BOOL
VAR
    i : INT;
    zone_aq_controller : ARRAY[1..8] OF AirQualityController;
    total_fresh_air_demand : REAL;
    total_exhaust_demand : REAL;
    any_co2_alarm : BOOL := FALSE;
    any_humidity_alarm : BOOL := FALSE;
END_VAR

total_fresh_air_demand := 0.0;
total_exhaust_demand := 0.0;

// Process each zone
FOR i := 1 TO ZONE_COUNT DO
    zone_aq_controller[i](
        zone_number := i,
        co2_level := co2_levels[i],
        humidity_level := humidity_levels[i],
        occupancy := occupancy_detected[i],
        manual_override := FALSE
    );
    
    // Accumulate demands
    total_fresh_air_demand := total_fresh_air_demand + zone_aq_controller[i].fresh_air_demand;
    total_exhaust_demand := total_exhaust_demand + zone_aq_controller[i].exhaust_demand;
    
    // Check for any alarms
    IF zone_aq_controller[i].co2_alarm THEN
        any_co2_alarm := TRUE;
    END_IF;
    
    IF zone_aq_controller[i].humidity_alarm THEN
        any_humidity_alarm := TRUE;
    END_IF;
END_FOR;

// Calculate system-wide fresh air demand
outside_air_damper := LIMIT(FRESH_AIR_MINIMUM, total_fresh_air_demand / REAL(ZONE_COUNT), 100.0);

// Set global alarm flag
air_quality_alarm := any_co2_alarm OR any_humidity_alarm;

AirQualityControllerMain := TRUE;

END_FUNCTION

// Function: Air Quality Trending and Analysis
FUNCTION AirQualityTrending : BOOL
VAR
    i, j : INT;
    co2_average : REAL;
    humidity_average : REAL;
    co2_trend_slope : REAL;
    humidity_trend_slope : REAL;
END_VAR

// Calculate averages and trends for predictive control
FOR i := 1 TO ZONE_COUNT DO
    co2_average := 0.0;
    humidity_average := 0.0;
    
    // Calculate zone averages
    FOR j := 1 TO 10 DO
        co2_average := co2_average + REAL(co2_levels[i]);
        humidity_average := humidity_average + humidity_levels[i];
    END_FOR;
    
    co2_average := co2_average / 10.0;
    humidity_average := humidity_average / 10.0;
    
    // Predictive adjustments based on trends
    IF co2_average > (REAL(CO2_SETPOINT) * 0.9) THEN
        // Proactive fresh air increase
        outside_air_damper := outside_air_damper + 5.0;
    END_IF;
END_FOR;

AirQualityTrending := TRUE;

END_FUNCTION

// Function: Contamination Response
FUNCTION ContaminationResponse : BOOL
VAR
    i : INT;
    contamination_detected : BOOL := FALSE;
    purge_mode_active : BOOL := FALSE;
END_VAR

// Check for rapid CO2 increase (possible contamination)
FOR i := 1 TO ZONE_COUNT DO
    IF co2_levels[i] > (CO2_SETPOINT * 1.5) THEN
        contamination_detected := TRUE;
    END_IF;
END_FOR;

// Activate purge mode if contamination detected
IF contamination_detected THEN
    purge_mode_active := TRUE;
    outside_air_damper := 100.0;        // Maximum fresh air
    supply_fan_speed := 100.0;          // Maximum fan speed
    // Extend exhaust operation
END_IF;

ContaminationResponse := TRUE;

END_FUNCTION

// Function: Indoor Air Quality Index Calculation
FUNCTION CalculateIAQIndex : INT
VAR
    i : INT;
    co2_score : REAL;
    humidity_score : REAL;
    overall_score : REAL;
    zone_count_active : INT := 0;
END_VAR

overall_score := 0.0;

FOR i := 1 TO ZONE_COUNT DO
    IF occupancy_detected[i] THEN
        zone_count_active := zone_count_active + 1;
        
        // CO2 scoring (0-50 points)
        IF co2_levels[i] <= CO2_SETPOINT THEN
            co2_score := 50.0;
        ELSIF co2_levels[i] <= CO2_ALARM_HIGH THEN
            co2_score := 50.0 - ((REAL(co2_levels[i] - CO2_SETPOINT) / REAL(CO2_ALARM_HIGH - CO2_SETPOINT)) * 30.0);
        ELSE
            co2_score := 20.0;
        END_IF;
        
        // Humidity scoring (0-50 points)
        IF ABS(humidity_levels[i] - HUMIDITY_SETPOINT) <= HUMIDITY_TOLERANCE THEN
            humidity_score := 50.0;
        ELSE
            humidity_score := 50.0 - (ABS(humidity_levels[i] - HUMIDITY_SETPOINT) * 2.0);
            humidity_score := MAX(10.0, humidity_score);
        END_IF;
        
        overall_score := overall_score + co2_score + humidity_score;
    END_IF;
END_FOR;

IF zone_count_active > 0 THEN
    CalculateIAQIndex := REAL_TO_INT(overall_score / REAL(zone_count_active));
ELSE
    CalculateIAQIndex := 100; // Default excellent rating for unoccupied building
END_IF;

// Ensure result is within 0-100 range
CalculateIAQIndex := LIMIT(0, CalculateIAQIndex, 100);

END_FUNCTION
