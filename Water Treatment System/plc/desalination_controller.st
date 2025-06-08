// Desalination Controller Function Block
// Reverse Osmosis (RO) Process Control
// Author: PLC Control System
// Date: June 2025

FUNCTION_BLOCK DesalinationController
VAR_INPUT
    Enable          : BOOL := FALSE;    // Enable RO controller
    PressureSetpoint : REAL := 55.0;    // RO pressure setpoint (bar)
    RecoverySetpoint : REAL := 45.0;    // Recovery rate setpoint (%)
    Reset           : BOOL := FALSE;    // Reset controller
END_VAR

VAR_OUTPUT
    PumpSpeed       : REAL := 0.0;      // RO pump speed output (%)
    ConcentrateValve : REAL := 50.0;    // Concentrate valve position (%)
    SystemReady     : BOOL := FALSE;    // RO system ready
    SystemFault     : BOOL := FALSE;    // RO system fault
    CleaningRequired : BOOL := FALSE;   // Cleaning cycle required
END_VAR

VAR
    // PID controller for pressure
    PressurePID     : PID;
    PIDOutput       : REAL := 0.0;
    
    // Control parameters
    Kp              : REAL := 2.0;      // Proportional gain
    Ti              : REAL := 10.0;     // Integral time (s)
    Td              : REAL := 1.0;      // Derivative time (s)
    
    // Process variables
    PressureError   : REAL := 0.0;
    RecoveryRate    : REAL := 0.0;
    SaltRejection   : REAL := 0.0;
    
    // Fouling monitoring
    FoulingIndex    : REAL := 0.0;
    BaselinePressure : REAL := 55.0;
    PressureDrop    : REAL := 0.0;
    
    // Timers
    StartupTimer    : TON;
    StabilizeTimer  : TON;
    FaultTimer      : TON;
    
    // State machine
    ControlState    : INT := 0;
    
    // Operating hours for maintenance
    OperatingHours  : REAL := 0.0;
    CleaningCycles  : INT := 0;
    
END_VAR

// =====================================
// MAIN DESALINATION CONTROLLER
// =====================================

IF Reset THEN
    // Reset all controller states
    ControlState := 0;
    SystemFault := FALSE;
    PumpSpeed := 0.0;
    ConcentrateValve := 50.0;
    StartupTimer(IN := FALSE);
    StabilizeTimer(IN := FALSE);
    FaultTimer(IN := FALSE);
END_IF

IF Enable THEN
    // Update operating hours
    OperatingHours := OperatingHours + 0.001;  // Increment operating time
    
    // Calculate process variables
    CalculateProcessVariables();
    
    // RO system state machine
    CASE ControlState OF
        0: // Idle state
            PumpSpeed := 0.0;
            ConcentrateValve := 100.0;  // Fully open for startup
            SystemReady := FALSE;
            
            IF Enable AND NOT SystemFault THEN
                ControlState := 1;  // Move to startup
            END_IF
        
        1: // Startup sequence
            StartupTimer(IN := TRUE, PT := T#30s);
            
            // Gradual pump speed increase
            IF StartupTimer.ET < T#20s THEN
                PumpSpeed := REAL_TO_REAL(TIME_TO_DINT(StartupTimer.ET)) / 20000.0 * 40.0;  // Ramp to 40%
            ELSE
                PumpSpeed := 40.0;
            END_IF
            
            // Adjust concentrate valve during startup
            ConcentrateValve := 80.0;
            
            IF StartupTimer.Q THEN
                StartupTimer(IN := FALSE);
                ControlState := 2;  // Move to pressure control
            END_IF
        
        2: // Pressure control mode
            SystemReady := TRUE;
            
            // PID pressure control
            PressureError := PressureSetpoint - g_ROPressure;
            
            PressurePID(
                bEnable := TRUE,
                fSetpointValue := PressureSetpoint,
                fActualValue := g_ROPressure,
                fKp := Kp,
                fTn := Ti,
                fTv := Td,
                fOutMax := 90.0,
                fOutMin := 20.0
            );
            
            PumpSpeed := PressurePID.fOut;
            
            // Concentrate valve control for recovery optimization
            ControlConcentrateValve();
            
            // Monitor for faults
            MonitorSystemHealth();
            
            // Check for cleaning requirement
            CheckCleaningRequirement();
            
            IF SystemFault THEN
                ControlState := 3;  // Move to fault state
            END_IF
        
        3: // Fault state
            PumpSpeed := 0.0;
            ConcentrateValve := 100.0;
            SystemReady := FALSE;
            
            FaultTimer(IN := TRUE, PT := T#10s);
            IF FaultTimer.Q AND NOT SystemFault THEN
                FaultTimer(IN := FALSE);
                ControlState := 0;  // Return to idle
            END_IF
    END_CASE
    
ELSE
    // Controller disabled
    ControlState := 0;
    PumpSpeed := 0.0;
    ConcentrateValve := 100.0;
    SystemReady := FALSE;
    StartupTimer(IN := FALSE);
    StabilizeTimer(IN := FALSE);
    FaultTimer(IN := FALSE);
END_IF

// =====================================
// PROCESS CALCULATIONS
// =====================================
FUNCTION CalculateProcessVariables : BOOL
VAR_INPUT
END_VAR

    // Calculate recovery rate
    IF (g_PermeateFlow + g_ConcentrateFlow) > 0.0 THEN
        RecoveryRate := g_PermeateFlow / (g_PermeateFlow + g_ConcentrateFlow) * 100.0;
    ELSE
        RecoveryRate := 0.0;
    END_IF
    
    // Calculate salt rejection rate
    IF g_SeawaterQuality.TDS > 0.0 THEN
        SaltRejection := (1.0 - g_ProductQuality.TDS / g_SeawaterQuality.TDS) * 100.0;
    ELSE
        SaltRejection := 0.0;
    END_IF
    
    // Calculate fouling index
    PressureDrop := g_ROPressure - BaselinePressure;
    IF BaselinePressure > 0.0 THEN
        FoulingIndex := ABS(PressureDrop) / BaselinePressure * 100.0;
    END_IF
    
    // Update global RO status
    g_ROSystemData.Pressure := g_ROPressure;
    g_ROSystemData.Recovery := RecoveryRate;
    g_ROSystemData.Rejection := SaltRejection;
    g_ROSystemData.Permeate := g_PermeateFlow;
    g_ROSystemData.Concentrate := g_ConcentrateFlow;
    g_ROSystemData.Fouling := FoulingIndex;
    g_ROSystemData.CleanCycle := CleaningCycles;
    
    CalculateProcessVariables := TRUE;
END_FUNCTION

// =====================================
// CONCENTRATE VALVE CONTROL
// =====================================
FUNCTION ControlConcentrateValve : BOOL
VAR_INPUT
END_VAR
VAR
    RecoveryError   : REAL;
    ValveAdjustment : REAL;
END_VAR

    // Control concentrate valve to maintain recovery rate
    RecoveryError := RecoverySetpoint - RecoveryRate;
    
    // Adjust valve position based on recovery error
    IF ABS(RecoveryError) > 2.0 THEN  // Only adjust if error is significant
        ValveAdjustment := RecoveryError * 0.5;  // Gain factor
        
        ConcentrateValve := ConcentrateValve - ValveAdjustment;
        
        // Limit valve position
        IF ConcentrateValve > 90.0 THEN
            ConcentrateValve := 90.0;
        ELSIF ConcentrateValve < 30.0 THEN
            ConcentrateValve := 30.0;
        END_IF
    END_IF
    
    ControlConcentrateValve := TRUE;
END_FUNCTION

// =====================================
// SYSTEM HEALTH MONITORING
// =====================================
FUNCTION MonitorSystemHealth : BOOL
VAR_INPUT
END_VAR

    SystemFault := FALSE;
    
    // Check pressure limits
    IF g_ROPressure > 65.0 THEN  // Over pressure
        SystemFault := TRUE;
    END_IF
    
    IF g_ROPressure < 30.0 AND PumpSpeed > 50.0 THEN  // Pressure too low
        SystemFault := TRUE;
    END_IF
    
    // Check flow rates
    IF g_PermeateFlow < 50.0 AND PumpSpeed > 60.0 THEN  // Low permeate flow
        SystemFault := TRUE;
    END_IF
    
    // Check salt rejection
    IF SaltRejection < 95.0 THEN  // Poor salt rejection
        SystemFault := TRUE;
    END_IF
    
    // Check for membrane fouling
    IF FoulingIndex > 90.0 THEN  // Severe fouling
        SystemFault := TRUE;
    END_IF
    
    // Update global alarm status
    g_ROSystemAlarm := SystemFault;
    
    MonitorSystemHealth := TRUE;
END_FUNCTION

// =====================================
// CLEANING REQUIREMENT CHECK
// =====================================
FUNCTION CheckCleaningRequirement : BOOL
VAR_INPUT
END_VAR

    CleaningRequired := FALSE;
    
    // Check fouling level
    IF FoulingIndex > 70.0 THEN
        CleaningRequired := TRUE;
    END_IF
    
    // Check operating hours (monthly cleaning)
    IF OperatingHours > 720.0 THEN  // 30 days * 24 hours
        CleaningRequired := TRUE;
    END_IF
    
    // Check salt rejection degradation
    IF SaltRejection < 97.0 THEN
        CleaningRequired := TRUE;
    END_IF
    
    // Check recovery rate drop
    IF RecoveryRate < 40.0 THEN
        CleaningRequired := TRUE;
    END_IF
    
    CheckCleaningRequirement := TRUE;
END_FUNCTION

END_FUNCTION_BLOCK

// =====================================
// PID CONTROLLER FUNCTION BLOCK
// =====================================
FUNCTION_BLOCK PID
VAR_INPUT
    bEnable         : BOOL := FALSE;
    fSetpointValue  : REAL := 0.0;
    fActualValue    : REAL := 0.0;
    fKp             : REAL := 1.0;
    fTn             : REAL := 1.0;
    fTv             : REAL := 0.0;
    fOutMax         : REAL := 100.0;
    fOutMin         : REAL := 0.0;
    bReset          : BOOL := FALSE;
END_VAR

VAR_OUTPUT
    fOut            : REAL := 0.0;
    bARWActive      : BOOL := FALSE;
END_VAR

VAR
    fErrorOld       : REAL := 0.0;
    fIntegral       : REAL := 0.0;
    fDerivative     : REAL := 0.0;
    fError          : REAL := 0.0;
    fProportional   : REAL := 0.0;
    fPIDSum         : REAL := 0.0;
    fCycleTime      : REAL := 0.1;  // Assume 100ms cycle time
END_VAR

IF bReset THEN
    fIntegral := 0.0;
    fErrorOld := 0.0;
    fOut := 0.0;
    bARWActive := FALSE;
END_IF

IF bEnable THEN
    // Calculate error
    fError := fSetpointValue - fActualValue;
    
    // Proportional term
    fProportional := fKp * fError;
    
    // Integral term (if Tn > 0)
    IF fTn > 0.0 AND NOT bARWActive THEN
        fIntegral := fIntegral + (fKp * fError * fCycleTime / fTn);
    END_IF
    
    // Derivative term (if Tv > 0)
    IF fTv > 0.0 THEN
        fDerivative := fKp * fTv * (fError - fErrorOld) / fCycleTime;
    ELSE
        fDerivative := 0.0;
    END_IF
    
    // Sum PID terms
    fPIDSum := fProportional + fIntegral + fDerivative;
    
    // Apply output limits
    IF fPIDSum > fOutMax THEN
        fOut := fOutMax;
        bARWActive := TRUE;  // Anti-reset windup
    ELSIF fPIDSum < fOutMin THEN
        fOut := fOutMin;
        bARWActive := TRUE;  // Anti-reset windup
    ELSE
        fOut := fPIDSum;
        bARWActive := FALSE;
    END_IF
    
    // Store error for next cycle
    fErrorOld := fError;
ELSE
    fOut := 0.0;
    fIntegral := 0.0;
    fErrorOld := 0.0;
    bARWActive := FALSE;
END_IF

END_FUNCTION_BLOCK
