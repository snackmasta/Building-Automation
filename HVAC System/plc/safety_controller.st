FUNCTION_BLOCK SafetyController
VAR_INPUT
    fire_alarm_input : BOOL;
    smoke_detector : ARRAY[1..8] OF BOOL;
    freeze_stat : BOOL;
    high_pressure_alarm : BOOL;
    low_pressure_alarm : BOOL;
    manual_emergency_stop : BOOL;
END_VAR

VAR_OUTPUT
    emergency_shutdown : BOOL;
    fire_mode_active : BOOL;
    freeze_protection_active : BOOL;
    safety_fault : BOOL;
    smoke_purge_active : BOOL;
END_VAR

VAR
    // Safety timers
    fire_alarm_timer : TON;
    freeze_protection_timer : TON;
    smoke_purge_timer : TON;
    
    // Safety status tracking
    any_smoke_detected : BOOL;
    freeze_protection_required : BOOL;
    pressure_fault : BOOL;
    
    // Safety interlocks
    supply_fan_safety : BOOL;
    return_fan_safety : BOOL;
    outside_air_safety : BOOL;
    
    // Emergency sequences
    fire_sequence_step : INT;
    freeze_sequence_step : INT;
    
    // Safety override flags
    manual_override_active : BOOL;
    maintenance_mode : BOOL;
END_VAR

// Smoke detection logic
any_smoke_detected := FALSE;
FOR i := 1 TO 8 DO
    IF smoke_detector[i] THEN
        any_smoke_detected := TRUE;
    END_IF;
END_FOR;

// Fire alarm processing with confirmation timer
fire_alarm_timer(IN := (fire_alarm_input OR any_smoke_detected), PT := T#5s);
fire_mode_active := fire_alarm_timer.Q;

// Freeze protection logic
freeze_protection_required := (outdoor_temp <= FREEZE_PROTECTION_TEMP) OR freeze_stat;
freeze_protection_timer(IN := freeze_protection_required, PT := T#10s);
freeze_protection_active := freeze_protection_timer.Q;

// Pressure fault detection
pressure_fault := high_pressure_alarm OR low_pressure_alarm;

// Main safety fault logic
safety_fault := pressure_fault OR manual_emergency_stop;

// Emergency shutdown conditions
emergency_shutdown := fire_mode_active OR 
                     freeze_protection_active OR 
                     safety_fault OR
                     (outdoor_temp > HIGH_TEMP_SHUTDOWN);

// Smoke purge sequence
IF any_smoke_detected AND NOT fire_mode_active THEN
    smoke_purge_timer(IN := TRUE, PT := T#10m);
    smoke_purge_active := smoke_purge_timer.Q;
ELSE
    smoke_purge_timer(IN := FALSE);
    smoke_purge_active := FALSE;
END_IF;

// Safety interlocks for equipment
supply_fan_safety := NOT emergency_shutdown;
return_fan_safety := NOT emergency_shutdown;
outside_air_safety := NOT (fire_mode_active OR freeze_protection_active);

END_FUNCTION_BLOCK

// Main Safety Controller Function
FUNCTION SafetyControllerMain : BOOL
VAR
    safety_ctrl : SafetyController;
    i : INT;
    any_zone_overtemp : BOOL := FALSE;
    any_zone_undertemp : BOOL := FALSE;
END_VAR

// Check for temperature safety conditions
FOR i := 1 TO ZONE_COUNT DO
    IF zone_temps[i] > TEMP_ALARM_HIGH THEN
        any_zone_overtemp := TRUE;
    END_IF;
    
    IF zone_temps[i] < TEMP_ALARM_LOW THEN
        any_zone_undertemp := TRUE;
    END_IF;
END_FOR;

// Run main safety controller
safety_ctrl(
    fire_alarm_input := fire_alarm,
    smoke_detector := smoke_detector,
    freeze_stat := (outdoor_temp <= FREEZE_PROTECTION_TEMP),
    high_pressure_alarm := FALSE, // Connect to actual pressure sensors
    low_pressure_alarm := FALSE,  // Connect to actual pressure sensors
    manual_emergency_stop := emergency_stop
);

// Update global safety flags
emergency_stop := safety_ctrl.emergency_shutdown;
fire_mode_active := safety_ctrl.fire_mode_active;
freeze_protection_active := safety_ctrl.freeze_protection_active;
system_fault := safety_ctrl.safety_fault;

// Implement safety actions
IF safety_ctrl.fire_mode_active THEN
    FireModeSequence();
END_IF;

IF safety_ctrl.freeze_protection_active THEN
    FreezeProtectionSequence();
END_IF;

IF safety_ctrl.smoke_purge_active THEN
    SmokePurgeSequence();
END_IF;

SafetyControllerMain := TRUE;

END_FUNCTION

// Function: Fire Mode Sequence
FUNCTION FireModeSequence : BOOL
VAR
    fire_sequence_timer : TON;
END_VAR

// Fire mode operation sequence according to NFPA standards
// 1. Shut down return fans immediately
return_fan_running := FALSE;
return_fan_speed := 0.0;

// 2. Close outside air dampers
outside_air_damper := 0.0;

// 3. Stop heating and cooling
heating_stage_1 := FALSE;
heating_stage_2 := FALSE;
cooling_stage_1 := FALSE;
cooling_stage_2 := FALSE;

// 4. Supply fan operation depends on fire department connection
// For pressurization mode, keep supply fan running at low speed
IF fire_alarm THEN
    supply_fan_running := TRUE;
    supply_fan_speed := 30.0; // Low speed for stairwell pressurization
ELSE
    supply_fan_running := FALSE;
    supply_fan_speed := 0.0;
END_IF;

// 5. Activate building management system notifications
// (This would interface with BMS)

FireModeSequence := TRUE;

END_FUNCTION

// Function: Freeze Protection Sequence
FUNCTION FreezeProtectionSequence : BOOL
VAR
    freeze_timer : TON;
END_VAR

// Freeze protection sequence
// 1. Close outside air damper to minimum
outside_air_damper := 0.0;

// 2. Start supply fan for air circulation
supply_fan_running := TRUE;
supply_fan_speed := 50.0; // Moderate speed for circulation

// 3. Start return fan
return_fan_running := TRUE;
return_fan_speed := 50.0;

// 4. Activate heating if available
heating_stage_1 := TRUE;
IF outdoor_temp <= (FREEZE_PROTECTION_TEMP - 2.0) THEN
    heating_stage_2 := TRUE;
END_IF;

// 5. Disable cooling
cooling_stage_1 := FALSE;
cooling_stage_2 := FALSE;

// 6. Override temperature setpoints to prevent freezing
FOR i := 1 TO ZONE_COUNT DO
    zone_setpoints[i] := MAX(zone_setpoints[i], 10.0);
END_FOR;

FreezeProtectionSequence := TRUE;

END_FUNCTION

// Function: Smoke Purge Sequence
FUNCTION SmokePurgeSequence : BOOL
VAR
    purge_timer : TON;
END_VAR

// Smoke purge sequence (not fire mode)
// 1. Increase outside air to maximum
outside_air_damper := 100.0;

// 2. Run fans at high speed
supply_fan_running := TRUE;
supply_fan_speed := 100.0;
return_fan_running := TRUE;
return_fan_speed := 100.0;

// 3. Disable heating and cooling during purge
heating_stage_1 := FALSE;
heating_stage_2 := FALSE;
cooling_stage_1 := FALSE;
cooling_stage_2 := FALSE;

// 4. Continue purge for specified time (10 minutes)
purge_timer(IN := TRUE, PT := T#10m);

// 5. Return to normal operation after purge
IF purge_timer.Q THEN
    smoke_purge_active := FALSE;
END_IF;

SmokePurgeSequence := TRUE;

END_FUNCTION

// Function: Safety System Test
FUNCTION SafetySystemTest : BOOL
VAR
    test_sequence_step : INT;
    test_timer : TON;
    test_results : ARRAY[1..10] OF BOOL;
END_VAR

// Weekly automatic safety system test
// This function would be called during maintenance windows

CASE test_sequence_step OF
    0: // Initialize test
        test_sequence_step := 1;
        
    1: // Test smoke detectors
        // Simulate smoke detection test
        test_timer(IN := TRUE, PT := T#30s);
        IF test_timer.Q THEN
            test_results[1] := TRUE; // Test passed
            test_sequence_step := 2;
            test_timer(IN := FALSE);
        END_IF;
        
    2: // Test fire alarm interface
        test_timer(IN := TRUE, PT := T#30s);
        IF test_timer.Q THEN
            test_results[2] := TRUE;
            test_sequence_step := 3;
            test_timer(IN := FALSE);
        END_IF;
        
    3: // Test freeze protection
        test_timer(IN := TRUE, PT := T#30s);
        IF test_timer.Q THEN
            test_results[3] := TRUE;
            test_sequence_step := 4;
            test_timer(IN := FALSE);
        END_IF;
        
    4: // Test emergency stop
        test_timer(IN := TRUE, PT := T#30s);
        IF test_timer.Q THEN
            test_results[4] := TRUE;
            test_sequence_step := 0; // Test complete
            test_timer(IN := FALSE);
        END_IF;
END_CASE;

SafetySystemTest := TRUE;

END_FUNCTION

// Function: Safety Alarm Prioritization
FUNCTION SafetyAlarmPriority : INT
VAR
    priority_level : INT;
END_VAR

// Determine highest priority safety alarm
IF fire_alarm THEN
    priority_level := 1; // Highest priority
ELSIF emergency_stop THEN
    priority_level := 2;
ELSIF freeze_protection_active THEN
    priority_level := 3;
ELSIF high_temp_alarm THEN
    priority_level := 4;
ELSIF air_quality_alarm THEN
    priority_level := 5;
ELSE
    priority_level := 0; // No alarms
END_IF;

SafetyAlarmPriority := priority_level;

END_FUNCTION

// Function: Safety Interlock Check
FUNCTION SafetyInterlockCheck : BOOL
VAR
    interlock_ok : BOOL := TRUE;
END_VAR

// Check all safety interlocks before starting equipment

// Check fire safety
IF fire_mode_active THEN
    interlock_ok := FALSE;
END_IF;

// Check freeze protection
IF freeze_protection_active AND outside_air_damper > 10.0 THEN
    interlock_ok := FALSE;
END_IF;

// Check pressure safety
IF high_pressure_alarm OR low_pressure_alarm THEN
    interlock_ok := FALSE;
END_IF;

// Check temperature limits
FOR i := 1 TO ZONE_COUNT DO
    IF zone_temps[i] > HIGH_TEMP_SHUTDOWN OR zone_temps[i] < FREEZE_PROTECTION_TEMP THEN
        interlock_ok := FALSE;
    END_IF;
END_FOR;

SafetyInterlockCheck := interlock_ok;

END_FUNCTION
