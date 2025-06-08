FUNCTION_BLOCK EnergyManager
VAR_INPUT
    current_demand : REAL;     // Current power demand in kW
    peak_limit : REAL;         // Peak demand limit in kW
    utility_signal : INT;      // Demand response signal (0-100)
    time_of_use_rate : REAL;   // Current electricity rate
    outside_temp : REAL;       // Outside temperature
END_VAR

VAR_OUTPUT
    demand_response_active : BOOL;
    load_shed_level : INT;     // 0-5 load shedding levels
    energy_savings_mode : BOOL;
    peak_demand_warning : BOOL;
    estimated_cost : REAL;     // Estimated hourly cost
END_VAR

VAR
    // Demand tracking
    peak_demand_today : REAL;
    peak_demand_month : REAL;
    energy_consumed_today : REAL;
    
    // Load shedding timers
    load_shed_timer : TON;
    recovery_timer : TON;
    
    // Equipment priority arrays
    equipment_priority : ARRAY[1..10] OF INT := [1,2,3,4,5,6,7,8,9,10];
    equipment_shed : ARRAY[1..10] OF BOOL;
    
    // Time-based controls
    current_time : TIME_OF_DAY;
    current_day : INT; // 1=Monday, 7=Sunday
    
    // Economic optimization
    cost_per_kwh : REAL;
    daily_energy_budget : REAL := 500.0; // kWh
    
    // Demand prediction
    predicted_demand : REAL;
    demand_trend : ARRAY[1..24] OF REAL; // Hourly demand history
    trend_hour : INT := 1;
END_VAR

current_time := TIME_OF_DAY();

// Update peak demand tracking
IF current_demand > peak_demand_today THEN
    peak_demand_today := current_demand;
END_IF;

IF current_demand > peak_demand_month THEN
    peak_demand_month := current_demand;
END_IF;

// Update demand trend data
demand_trend[trend_hour] := current_demand;

// Peak demand warning
peak_demand_warning := (current_demand > (peak_limit * 0.9));

// Demand response logic
IF DEMAND_RESPONSE_ENABLED THEN
    // Utility demand response signal processing
    IF utility_signal > 80 THEN
        demand_response_active := TRUE;
        load_shed_level := 4; // High demand response
    ELSIF utility_signal > 60 THEN
        demand_response_active := TRUE;
        load_shed_level := 3; // Medium demand response
    ELSIF utility_signal > 40 THEN
        demand_response_active := TRUE;
        load_shed_level := 2; // Low demand response
    ELSIF current_demand > peak_limit THEN
        demand_response_active := TRUE;
        load_shed_level := 5; // Emergency load shedding
    ELSE
        demand_response_active := FALSE;
        load_shed_level := 0; // Normal operation
    END_IF;
ELSE
    demand_response_active := FALSE;
    load_shed_level := 0;
END_IF;

// Energy savings mode activation
energy_savings_mode := (time_of_use_rate > 0.15) OR // High rate period
                      (energy_consumed_today > (daily_energy_budget * 0.8)); // Approaching budget

// Calculate estimated cost
estimated_cost := current_demand * time_of_use_rate;

// Load shedding implementation
CASE load_shed_level OF
    0: // Normal operation - no load shedding
        FOR i := 1 TO 10 DO
            equipment_shed[i] := FALSE;
        END_FOR;
        
    1: // Minimal load shedding - non-critical loads
        equipment_shed[1] := TRUE;  // Exterior lighting
        equipment_shed[2] := FALSE; // HVAC priority 1
        
    2: // Low load shedding
        equipment_shed[1] := TRUE;  // Exterior lighting
        equipment_shed[2] := TRUE;  // Non-critical HVAC zones
        equipment_shed[3] := FALSE; // Critical HVAC zones
        
    3: // Medium load shedding
        equipment_shed[1] := TRUE;  // Exterior lighting
        equipment_shed[2] := TRUE;  // Non-critical HVAC zones
        equipment_shed[3] := TRUE;  // Some office equipment
        equipment_shed[4] := FALSE; // Critical HVAC zones
        
    4: // High load shedding
        equipment_shed[1] := TRUE;  // Exterior lighting
        equipment_shed[2] := TRUE;  // Non-critical HVAC zones
        equipment_shed[3] := TRUE;  // Office equipment
        equipment_shed[4] := TRUE;  // Partial HVAC operation
        equipment_shed[5] := FALSE; // Emergency systems
        
    5: // Emergency load shedding
        FOR i := 1 TO 8 DO
            equipment_shed[i] := TRUE;
        END_FOR;
        equipment_shed[9] := FALSE;  // Emergency systems
        equipment_shed[10] := FALSE; // Life safety systems
END_CASE;

END_FUNCTION_BLOCK

// Main Energy Manager Function
FUNCTION EnergyManagerMain : BOOL
VAR
    energy_mgr : EnergyManager;
    current_power_demand : REAL;
    utility_dr_signal : INT;
    current_rate : REAL;
    
    // Equipment power consumption estimates (kW)
    supply_fan_power : REAL;
    return_fan_power : REAL;
    cooling_power : REAL;
    heating_power : REAL;
    lighting_power : REAL := 15.0;
    office_equipment_power : REAL := 25.0;
END_VAR

// Calculate equipment power consumption
supply_fan_power := (supply_fan_speed / 100.0) * 7.5; // 7.5kW max fan
return_fan_power := (return_fan_speed / 100.0) * 5.0; // 5kW max fan

IF cooling_stage_1 THEN
    cooling_power := cooling_power + 20.0; // 20kW per stage
END_IF;
IF cooling_stage_2 THEN
    cooling_power := cooling_power + 20.0;
END_IF;

IF heating_stage_1 THEN
    heating_power := heating_power + 15.0; // 15kW per stage
END_IF;
IF heating_stage_2 THEN
    heating_power := heating_power + 15.0;
END_IF;

// Total current demand
current_power_demand := supply_fan_power + return_fan_power + 
                       cooling_power + heating_power + 
                       lighting_power + office_equipment_power;

// Get time-of-use rate (simplified)
IF current_time >= TOD#08:00:00 AND current_time <= TOD#20:00:00 THEN
    current_rate := 0.18; // Peak rate
ELSE
    current_rate := 0.12; // Off-peak rate
END_IF;

// Simulate utility demand response signal
utility_dr_signal := 0; // Normal operation

// Run energy manager
energy_mgr(
    current_demand := current_power_demand,
    peak_limit := PEAK_DEMAND_LIMIT,
    utility_signal := utility_dr_signal,
    time_of_use_rate := current_rate,
    outside_temp := outdoor_temp
);

// Apply load shedding actions
ApplyLoadShedding(energy_mgr.load_shed_level);

// Update global energy management flags
demand_response_active := energy_mgr.demand_response_active;

EnergyManagerMain := TRUE;

END_FUNCTION

// Function: Apply Load Shedding
FUNCTION ApplyLoadShedding : BOOL
VAR_INPUT
    shed_level : INT;
END_VAR
VAR
    temp_setpoint_offset : REAL;
    fan_speed_reduction : REAL;
END_VAR

CASE shed_level OF
    0: // Normal operation
        temp_setpoint_offset := 0.0;
        fan_speed_reduction := 0.0;
        
    1: // Minimal shedding
        temp_setpoint_offset := 0.5; // Slight setpoint adjustment
        fan_speed_reduction := 5.0;  // 5% fan speed reduction
        
    2: // Low shedding
        temp_setpoint_offset := 1.0;
        fan_speed_reduction := 10.0;
        
    3: // Medium shedding
        temp_setpoint_offset := 1.5;
        fan_speed_reduction := 15.0;
        
    4: // High shedding
        temp_setpoint_offset := 2.0;
        fan_speed_reduction := 20.0;
        
    5: // Emergency shedding
        temp_setpoint_offset := 3.0;
        fan_speed_reduction := 30.0;
END_CASE;

// Apply temperature setpoint adjustments
FOR i := 1 TO ZONE_COUNT DO
    IF zone_heating_demand[i] THEN
        zone_setpoints[i] := zone_setpoints[i] - temp_setpoint_offset;
    ELSIF zone_cooling_demand[i] THEN
        zone_setpoints[i] := zone_setpoints[i] + temp_setpoint_offset;
    END_IF;
END_FOR;

// Apply fan speed reduction
supply_fan_speed := supply_fan_speed * (1.0 - fan_speed_reduction / 100.0);
return_fan_speed := return_fan_speed * (1.0 - fan_speed_reduction / 100.0);

// Limit minimum values
supply_fan_speed := MAX(MIN_FAN_SPEED, supply_fan_speed);
return_fan_speed := MAX(MIN_FAN_SPEED, return_fan_speed);

ApplyLoadShedding := TRUE;

END_FUNCTION

// Function: Optimal Start/Stop Control
FUNCTION OptimalStartStop : BOOL
VAR
    building_thermal_mass : REAL := 2.5; // Hours to change 1°C
    preheat_time : TIME;
    precool_time : TIME;
    start_time : TIME_OF_DAY;
    stop_time : TIME_OF_DAY;
    temp_difference : REAL;
END_VAR

// Calculate required pre-conditioning time
IF outdoor_temp < 15.0 THEN
    // Heating season
    temp_difference := DEFAULT_TEMP_HEATING - 18.0; // Night setback difference
    preheat_time := REAL_TO_TIME(REAL_TO_DINT(temp_difference * building_thermal_mass * 3600000.0));
    
    // Adjust start time for optimal pre-heating
    start_time := WEEKDAY_START - TIME_TO_TOD(preheat_time);
    
ELSIF outdoor_temp > 25.0 THEN
    // Cooling season
    temp_difference := 27.0 - DEFAULT_TEMP_COOLING; // Night setback difference
    precool_time := REAL_TO_TIME(REAL_TO_DINT(temp_difference * building_thermal_mass * 3600000.0));
    
    // Adjust start time for optimal pre-cooling
    start_time := WEEKDAY_START - TIME_TO_TOD(precool_time);
ELSE
    // Mild weather - normal start time
    start_time := WEEKDAY_START;
END_IF;

// Optimal stop control with thermal flywheel
stop_time := WEEKDAY_END - T#30m; // Stop 30 minutes early

OptimalStartStop := TRUE;

END_FUNCTION

// Function: Energy Reporting
FUNCTION EnergyReporting : BOOL
VAR
    daily_consumption : REAL;
    monthly_consumption : REAL;
    energy_efficiency_ratio : REAL;
    carbon_footprint : REAL;
    cost_savings : REAL;
END_VAR

// Calculate energy efficiency metrics
energy_efficiency_ratio := daily_consumption / (outdoor_temp * 24.0); // Simplified EER

// Calculate carbon footprint (kg CO2)
carbon_footprint := daily_consumption * 0.45; // 0.45 kg CO2/kWh average

// Calculate cost savings from demand response
cost_savings := 0.0; // Calculate based on load shedding actions

EnergyReporting := TRUE;

END_FUNCTION
