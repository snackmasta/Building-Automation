(*
===============================================================================
SAFETY CONTROLLER
===============================================================================
Purpose: Emergency procedures, safety interlocks, and fail-safe operations
Author: Industrial Automation System
Date: June 8, 2025
Version: 1.0

Safety Requirements:
- Emergency stop activation within 1 second
- Fire suppression system activation
- Elevator emergency brake engagement
- Personnel safety zone monitoring
- Automatic ventilation control
- Emergency lighting activation
- Communication with emergency services
===============================================================================
*)

FUNCTION_BLOCK SafetyController
VAR_INPUT
    Enable : BOOL;                      // Enable safety monitoring
    Reset : BOOL;                       // Reset safety alarms
    TestMode : BOOL;                    // Safety system test mode
END_VAR

VAR_OUTPUT
    SafetyOK : BOOL;                    // Overall safety status
    EmergencyActive : BOOL;             // Emergency condition active
    EvacuationRequired : BOOL;          // Evacuation alarm active
    MaintenanceRequired : BOOL;         // Safety maintenance needed
    SafetyAlarm : BOOL;                 // Safety alarm output
END_VAR

VAR
    // Emergency Stop Processing
    EmergencyStopChain : BOOL;          // Emergency stop chain status
    EmergencyStopTimer : TON;           // Emergency stop response timer
    EmergencyResetTimer : TON;          // Emergency reset delay timer
    
    // Fire Safety System
    FireDetected : BOOL;                // Fire detection status
    FireSuppressionActive : BOOL;       // Fire suppression system active
    EvacuationTimer : TON;              // Evacuation countdown timer
    FireZoneStatus : ARRAY[1..15] OF BOOL; // Fire status per level
    
    // Personnel Safety
    PersonnelInZone : ARRAY[1..10] OF BOOL; // Personnel detection zones
    SafetyZoneViolation : BOOL;         // Safety zone violation detected
    AccessControlActive : BOOL;         // Access control system status
    
    // Equipment Safety Interlocks
    ElevatorSafetyOK : ARRAY[1..3] OF BOOL;  // Elevator safety status
    PlatformSafetyOK : ARRAY[1..20] OF BOOL; // Platform safety status
    MotorSafetyOK : BOOL;               // Motor safety interlocks
    HydraulicSafetyOK : BOOL;           // Hydraulic system safety
    
    // Environmental Safety
    VentilationStatus : BOOL;           // Ventilation system status
    CO_LevelOK : BOOL;                  // Carbon monoxide levels OK
    TemperatureOK : BOOL;               // Temperature within safe limits
    HumidityOK : BOOL;                  // Humidity within safe limits
    
    // Communication Safety
    PLCHeartbeat : BOOL;                // PLC communication heartbeat
    HMIHeartbeat : BOOL;                // HMI communication heartbeat
    NetworkStatus : BOOL;               // Network communication status
    
    // Safety State Machine
    SafetyState : INT;                  // Current safety state
    PreviousState : INT;                // Previous safety state
    StateTimer : TON;                   // State transition timer
    
    // Diagnostic Variables
    SafetyTestResults : ARRAY[1..20] OF BOOL; // Safety test results
    LastTestTime : DATE_AND_TIME;       // Last safety test timestamp
    TestInProgress : BOOL;              // Safety test in progress
    
    // Counters and Statistics
    EmergencyStopCount : DINT;          // Emergency stop activation count
    FireAlarmCount : DINT;              // Fire alarm activation count
    SafetyViolationCount : DINT;        // Safety violation count
    SystemUptimeHours : DINT;           // System uptime in hours
END_VAR

// Safety State Definitions
VAR CONSTANT
    SAFETY_NORMAL : INT := 0;           // Normal operation
    SAFETY_WARNING : INT := 1;          // Warning condition
    SAFETY_ALARM : INT := 2;            // Alarm condition
    SAFETY_EMERGENCY : INT := 3;        // Emergency condition
    SAFETY_EVACUATION : INT := 4;       // Evacuation required
    SAFETY_LOCKDOWN : INT := 5;         // System lockdown
    SAFETY_TEST : INT := 6;             // Safety test mode
    SAFETY_MAINTENANCE : INT := 7;      // Maintenance mode
END_VAR

// Main Safety Controller Logic
IF NOT Enable THEN
    SafetyOK := FALSE;
    SafetyState := SAFETY_LOCKDOWN;
    RETURN;
END_IF

// Emergency Stop Chain Monitoring
EmergencyStopChain := Emergency_Stop_Main AND 
                      Emergency_Stop_Level1 AND 
                      Emergency_Stop_Level2 AND 
                      Emergency_Stop_Maintenance AND
                      Emergency_Stop_HMI;

// Emergency Stop Processing
IF NOT EmergencyStopChain THEN
    EmergencyActive := TRUE;
    SafetyState := SAFETY_EMERGENCY;
    EmergencyStopCount := EmergencyStopCount + 1;
    
    // Activate emergency procedures
    Emergency_Elevator_Stop := TRUE;
    Emergency_Platform_Stop := TRUE;
    Emergency_Motor_Stop := TRUE;
    Emergency_Lighting := TRUE;
    Emergency_Ventilation := TRUE;
    
    // Start emergency response timer
    EmergencyStopTimer(IN := TRUE, PT := T#1S);
END_IF

// Fire Detection and Suppression
FireDetected := Fire_Detector_Level1 OR Fire_Detector_Level2 OR 
                Fire_Detector_Basement OR Smoke_Detector_Main OR
                Heat_Detector_Electrical;

IF FireDetected THEN
    SafetyState := SAFETY_EVACUATION;
    EvacuationRequired := TRUE;
    FireAlarmCount := FireAlarmCount + 1;
    
    // Activate fire suppression sequence
    Fire_Suppression_Activate := TRUE;
    Emergency_Ventilation := TRUE;
    Evacuation_Alarm := TRUE;
    Emergency_Lighting := TRUE;
    
    // Evacuate all vehicles from affected zones
    IF Fire_Detector_Level1 THEN
        Evacuate_Level_1 := TRUE;
    END_IF
    IF Fire_Detector_Level2 THEN
        Evacuate_Level_2 := TRUE;
    END_IF
    
    // Start evacuation timer (10 minutes)
    EvacuationTimer(IN := TRUE, PT := T#10M);
END_IF

// Personnel Safety Zone Monitoring
SafetyZoneViolation := FALSE;
FOR i := 1 TO 10 DO
    IF PersonnelInZone[i] AND Equipment_Operating THEN
        SafetyZoneViolation := TRUE;
        SafetyViolationCount := SafetyViolationCount + 1;
    END_IF
END_FOR

// Equipment Safety Interlocks
FOR i := 1 TO 3 DO
    ElevatorSafetyOK[i] := Elevator_Door_Closed[i] AND 
                           Elevator_Position_Valid[i] AND
                           Elevator_Speed_Safe[i] AND
                           Elevator_Load_Safe[i];
END_FOR

FOR i := 1 TO 20 DO
    PlatformSafetyOK[i] := Platform_Position_Valid[i] AND 
                           Platform_Load_Safe[i] AND
                           Platform_Clear[i];
END_FOR

// Motor Safety Interlocks
MotorSafetyOK := Motor_Temperature_OK AND 
                 Motor_Current_OK AND 
                 Motor_Vibration_OK AND
                 Motor_Overload_OK;

// Hydraulic System Safety
HydraulicSafetyOK := Hydraulic_Pressure_OK AND 
                     Hydraulic_Temperature_OK AND 
                     Hydraulic_Level_OK AND
                     Hydraulic_Filter_OK;

// Environmental Safety Monitoring
VentilationStatus := Ventilation_Fan_1_OK AND 
                     Ventilation_Fan_2_OK AND 
                     Air_Quality_OK;

CO_LevelOK := CO_Level < 35;  // ppm limit
TemperatureOK := (Ambient_Temperature > 5) AND (Ambient_Temperature < 40);
HumidityOK := (Relative_Humidity > 20) AND (Relative_Humidity < 80);

// Communication Safety Heartbeat
PLCHeartbeat := PLC_Status_OK;
HMIHeartbeat := HMI_Status_OK;
NetworkStatus := Network_Status_OK;

// Safety State Machine
CASE SafetyState OF
    SAFETY_NORMAL:
        IF TestMode THEN
            SafetyState := SAFETY_TEST;
        ELSIF FireDetected THEN
            SafetyState := SAFETY_EVACUATION;
        ELSIF NOT EmergencyStopChain THEN
            SafetyState := SAFETY_EMERGENCY;
        ELSIF SafetyZoneViolation THEN
            SafetyState := SAFETY_WARNING;
        END_IF
        
    SAFETY_WARNING:
        SafetyAlarm := TRUE;
        IF NOT SafetyZoneViolation THEN
            SafetyState := SAFETY_NORMAL;
        ELSIF EmergencyStopChain = FALSE THEN
            SafetyState := SAFETY_EMERGENCY;
        END_IF
        
    SAFETY_ALARM:
        SafetyAlarm := TRUE;
        EmergencyActive := TRUE;
        IF Reset AND (NOT FireDetected) AND EmergencyStopChain THEN
            EmergencyResetTimer(IN := TRUE, PT := T#5S);
            IF EmergencyResetTimer.Q THEN
                SafetyState := SAFETY_NORMAL;
                EmergencyResetTimer(IN := FALSE);
            END_IF
        END_IF
        
    SAFETY_EMERGENCY:
        EmergencyActive := TRUE;
        SafetyAlarm := TRUE;
        
        // All equipment emergency stop
        Emergency_All_Stop := TRUE;
        
        IF Reset AND EmergencyStopChain AND (NOT FireDetected) THEN
            EmergencyResetTimer(IN := TRUE, PT := T#10S);
            IF EmergencyResetTimer.Q THEN
                SafetyState := SAFETY_NORMAL;
                EmergencyActive := FALSE;
                Emergency_All_Stop := FALSE;
                EmergencyResetTimer(IN := FALSE);
            END_IF
        END_IF
        
    SAFETY_EVACUATION:
        EvacuationRequired := TRUE;
        EmergencyActive := TRUE;
        SafetyAlarm := TRUE;
        
        // Complete system shutdown
        Emergency_All_Stop := TRUE;
        Evacuation_Alarm := TRUE;
        Emergency_Lighting := TRUE;
        
        // Automatic fire department notification
        Fire_Department_Alert := TRUE;
        
        EvacuationTimer(IN := TRUE, PT := T#30M);
        IF EvacuationTimer.Q AND Reset THEN
            SafetyState := SAFETY_MAINTENANCE;
            EvacuationTimer(IN := FALSE);
        END_IF
        
    SAFETY_LOCKDOWN:
        EmergencyActive := TRUE;
        SafetyAlarm := TRUE;
        Emergency_All_Stop := TRUE;
        
        IF Enable AND Reset THEN
            SafetyState := SAFETY_NORMAL;
            EmergencyActive := FALSE;
            Emergency_All_Stop := FALSE;
        END_IF
        
    SAFETY_TEST:
        TestInProgress := TRUE;
        
        // Perform safety system tests
        SafetyTestResults[1] := Test_Emergency_Stops();
        SafetyTestResults[2] := Test_Fire_Detection();
        SafetyTestResults[3] := Test_Ventilation();
        SafetyTestResults[4] := Test_Emergency_Lighting();
        SafetyTestResults[5] := Test_Communication();
        
        StateTimer(IN := TRUE, PT := T#60S);
        IF StateTimer.Q THEN
            TestInProgress := FALSE;
            LastTestTime := NOW();
            SafetyState := SAFETY_NORMAL;
            StateTimer(IN := FALSE);
        END_IF
        
    SAFETY_MAINTENANCE:
        MaintenanceRequired := TRUE;
        Emergency_All_Stop := TRUE;
        
        IF Reset AND Maintenance_Complete THEN
            SafetyState := SAFETY_NORMAL;
            MaintenanceRequired := FALSE;
            Emergency_All_Stop := FALSE;
        END_IF
END_CASE

// Overall Safety Status
SafetyOK := (SafetyState = SAFETY_NORMAL) AND 
            EmergencyStopChain AND 
            (NOT FireDetected) AND 
            (NOT SafetyZoneViolation) AND
            MotorSafetyOK AND 
            HydraulicSafetyOK AND
            VentilationStatus AND
            CO_LevelOK AND 
            TemperatureOK AND
            PLCHeartbeat AND 
            HMIHeartbeat;

// Safety Output Assignments
Safety_System_OK := SafetyOK;
Emergency_Stop_Output := EmergencyActive;
Fire_Alarm_Output := FireDetected;
Evacuation_Signal := EvacuationRequired;
Maintenance_Signal := MaintenanceRequired;

END_FUNCTION_BLOCK

(*
===============================================================================
SAFETY SYSTEM TEST FUNCTIONS
===============================================================================
*)

FUNCTION Test_Emergency_Stops : BOOL
VAR
    TestResult : BOOL := TRUE;
END_VAR

// Test all emergency stop circuits
TestResult := TestResult AND Emergency_Stop_Main;
TestResult := TestResult AND Emergency_Stop_Level1;
TestResult := TestResult AND Emergency_Stop_Level2;
TestResult := TestResult AND Emergency_Stop_Maintenance;
TestResult := TestResult AND Emergency_Stop_HMI;

Test_Emergency_Stops := TestResult;
END_FUNCTION

FUNCTION Test_Fire_Detection : BOOL
VAR
    TestResult : BOOL := TRUE;
END_VAR

// Test fire detection systems
TestResult := TestResult AND Fire_Detector_Level1_OK;
TestResult := TestResult AND Fire_Detector_Level2_OK;
TestResult := TestResult AND Smoke_Detector_Main_OK;
TestResult := TestResult AND Heat_Detector_Electrical_OK;

Test_Fire_Detection := TestResult;
END_FUNCTION

FUNCTION Test_Ventilation : BOOL
VAR
    TestResult : BOOL := TRUE;
END_VAR

// Test ventilation systems
TestResult := TestResult AND Ventilation_Fan_1_OK;
TestResult := TestResult AND Ventilation_Fan_2_OK;
TestResult := TestResult AND Emergency_Ventilation_OK;

Test_Ventilation := TestResult;
END_FUNCTION

FUNCTION Test_Emergency_Lighting : BOOL
VAR
    TestResult : BOOL := TRUE;
END_VAR

// Test emergency lighting systems
TestResult := TestResult AND Emergency_Light_1_OK;
TestResult := TestResult AND Emergency_Light_2_OK;
TestResult := TestResult AND Exit_Light_1_OK;
TestResult := TestResult AND Exit_Light_2_OK;

Test_Emergency_Lighting := TestResult;
END_FUNCTION

FUNCTION Test_Communication : BOOL
VAR
    TestResult : BOOL := TRUE;
END_VAR

// Test communication systems
TestResult := TestResult AND PLC_Status_OK;
TestResult := TestResult AND HMI_Status_OK;
TestResult := TestResult AND Network_Status_OK;
TestResult := TestResult AND Fire_Department_Comm_OK;

Test_Communication := TestResult;
END_FUNCTION
