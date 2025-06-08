PROGRAM main
VAR
    FirstScan : BOOL := TRUE;
    OperatingMode : INT := 0; (* 0: Stopped, 1: Auto, 2: Storm, 3: Maintenance *)
    SystemState : INT := 0;   (* 0: Init, 1: Running, 2: Warning, 3: Alarm, 4: Emergency *)
    StartupSequenceComplete : BOOL := FALSE;
    SystemInitTimer : TON;
    HeartbeatTimer : TON;
    HeartbeatPulse : BOOL := FALSE;
    PulseTimer : TON;
END_VAR

(* Main control program for Wastewater Treatment Plant *)
(* This program coordinates all subsystems and manages overall plant operations *)

(* System Initialization *)
IF FirstScan THEN
    SystemInitTimer(IN := TRUE, PT := T#10S);
    HeartbeatTimer(IN := TRUE, PT := T#1S);
    PulseTimer(IN := TRUE, PT := T#500MS);
    FirstScan := FALSE;
    SystemRunning := FALSE;
    SystemFault := FALSE;
    AlarmActive := FALSE;
    
    (* Reset all outputs to safe state *)
    PUMP_P101_START := FALSE;
    PUMP_P102_START := FALSE;
    MIXER_M101_START := FALSE;
    MIXER_M102_START := FALSE;
    SCREEN_FORWARD := FALSE;
    SCREEN_REVERSE := FALSE;
    BLOWER_START := FALSE;
    UV_SYSTEM_START := FALSE;
    ACID_DOSING_PUMP := FALSE;
    BASE_DOSING_PUMP := FALSE;
    CHLORINE_DOSING := FALSE;
    SLUDGE_PUMP_START := FALSE;
    ALARM_BEACON := FALSE;
    ALARM_HORN := FALSE;
    BACKWASH_VALVE := FALSE;
    OUTLET_VALVE := FALSE;
    
    (* Initialize analog outputs *)
    PUMP_P101_SPEED := 0;
    PUMP_P102_SPEED := 0;
    BLOWER_SPEED := 0;
    ACID_DOSING_RATE := 0;
    BASE_DOSING_RATE := 0;
    CHLORINE_DOSING_RATE := 0;
    MIXER_M101_SPEED := 0;
    MIXER_M102_SPEED := 0;
END_IF

(* Determine System State Based on Inputs *)
IF EMERGENCY_STOP THEN
    SystemState := 4; (* Emergency *)
ELSIF GAS_ALARM OR HighPHAlarm OR LowPHAlarm OR HighTurbidityAlarm OR LowOxygenAlarm THEN
    SystemState := 3; (* Alarm *)
ELSIF ChemicalLevelWarning OR SCREEN_CLOG OR FILTER_PRESSURE_HIGH THEN
    SystemState := 2; (* Warning *)
ELSIF StartupSequenceComplete THEN
    SystemState := 1; (* Running *)
ELSE
    SystemState := 0; (* Initializing *)
END_IF

(* System Initialization Sequence *)
IF SystemInitTimer.Q AND NOT StartupSequenceComplete THEN
    (* Initialization complete, system ready to run *)
    StartupSequenceComplete := TRUE;
END_IF

(* Determine Operating Mode *)
IF MAINTENANCE_MODE THEN
    OperatingMode := 3; (* Maintenance *)
ELSIF StormModeActive THEN
    OperatingMode := 2; (* Storm *)
ELSIF AUTO_MODE AND StartupSequenceComplete THEN
    OperatingMode := 1; (* Automatic *)
ELSE
    OperatingMode := 0; (* Stopped *)
END_IF

(* System Heartbeat *)
HeartbeatTimer();
IF HeartbeatTimer.Q THEN
    HeartbeatPulse := NOT HeartbeatPulse;
    HeartbeatTimer(IN := TRUE, PT := T#1S);
END_IF

(* Fast Pulse for Controllers *)
PulseTimer();
IF PulseTimer.Q THEN
    PulseTimer(IN := TRUE, PT := T#500MS);
END_IF

(* Process measurements and scale analog inputs *)
ScaledFlowRate := INT_TO_REAL(INTAKE_FLOW_RATE) * MAX_FLOW_RATE / 27648.0;
ScaledTankLevel1 := INT_TO_REAL(TANK_LEVEL_1) * MAX_TANK_LEVEL / 27648.0;
ScaledTankLevel2 := INT_TO_REAL(TANK_LEVEL_2) * MAX_TANK_LEVEL / 27648.0;
ScaledPHValue := 14.0 * INT_TO_REAL(PH_VALUE) / 27648.0;
ScaledDO := 20.0 * INT_TO_REAL(DISSOLVED_OXYGEN) / 27648.0;
ScaledTurbidity := 1000.0 * INT_TO_REAL(TURBIDITY) / 27648.0;
ScaledChlorineResidual := 10.0 * INT_TO_REAL(CHLORINE_RESIDUAL) / 27648.0;

(* Alarm Evaluation *)
HighPHAlarm := ScaledPHValue > MAX_PH;
LowPHAlarm := ScaledPHValue < MIN_PH AND ScaledPHValue > 0.5; (* Ignore if near zero - likely a sensor fault *)
LowOxygenAlarm := ScaledDO < MIN_DO AND BatchProcessing;
HighTurbidityAlarm := ScaledTurbidity > MAX_TURBIDITY;
ChemicalLevelWarning := CHLORINE_LOW OR ACID_TANK_LOW;
GasDetectionAlarm := GAS_ALARM;
AlarmActive := HighPHAlarm OR LowPHAlarm OR HighTurbidityAlarm OR LowOxygenAlarm OR GasDetectionAlarm;

(* Alarm Indicators *)
ALARM_BEACON := AlarmActive OR SystemState = 4; (* On for Alarms & Emergency *)
ALARM_HORN := SystemState = 4; (* Horn only for Emergency *)

(* System Running Status *)
SystemRunning := (OperatingMode > 0) AND (SystemState < 4);
MaintenanceRequired := (OperatingMode = 3) OR SCREEN_CLOG OR FILTER_PRESSURE_HIGH;

(* Call Subsystem Controllers *)
(* Each controller manages its specific process area *)
intake_controller();
treatment_controller();
dosing_controller();
aeration_controller();
monitoring_controller();

(* Safety Interlocks Override - Emergency Stop *)
IF SystemState = 4 THEN
    (* Emergency Stop - Shutdown all processes *)
    PUMP_P101_START := FALSE;
    PUMP_P102_START := FALSE;
    MIXER_M101_START := FALSE;
    MIXER_M102_START := FALSE;
    BLOWER_START := FALSE;
    ACID_DOSING_PUMP := FALSE;
    BASE_DOSING_PUMP := FALSE;
    CHLORINE_DOSING := FALSE;
    SLUDGE_PUMP_START := FALSE;
    
    (* Set all analog outputs to safe state *)
    PUMP_P101_SPEED := 0;
    PUMP_P102_SPEED := 0;
    BLOWER_SPEED := 0;
    ACID_DOSING_RATE := 0;
    BASE_DOSING_RATE := 0;
    CHLORINE_DOSING_RATE := 0;
    MIXER_M101_SPEED := 0;
    MIXER_M102_SPEED := 0;
    
    (* Ensure outlet valve is closed *)
    OUTLET_VALVE := FALSE;
END_IF

(* Daily totalization calculation *)
IF SystemRunning THEN
    TotalFlowToday := TotalFlowToday + (ScaledFlowRate / 3600.0); (* m³/hr to m³/second *)
    TotalEnergyUsage := TotalEnergyUsage + (INT_TO_REAL(POWER_CONSUMPTION) * 500.0 / 27648.0 / 3600.0); (* kW to kWh *)
END_IF

(* Treatment Efficiency Calculation - simplified approximation *)
IF ScaledFlowRate > 10.0 AND ScaledTurbidity < MAX_TURBIDITY THEN
    TreatmentEfficiency := 100.0 * (1.0 - ScaledTurbidity / 1000.0);
END_IF

END_PROGRAM
