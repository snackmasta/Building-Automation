// Water Quality Controller Function Block
// Water Quality Monitoring and Treatment Control
// Author: PLC Control System
// Date: June 2025

FUNCTION_BLOCK WaterQualityController
VAR_INPUT
    Enable          : BOOL := FALSE;    // Enable water quality controller
    AutoMode        : BOOL := TRUE;     // Automatic control mode
    Reset           : BOOL := FALSE;    // Reset controller
END_VAR

VAR_OUTPUT
    QualityOK       : BOOL := FALSE;    // Water quality acceptable
    QualityAlarm    : BOOL := FALSE;    // Water quality alarm
    TreatmentActive : BOOL := FALSE;    // Treatment systems active
END_VAR

VAR
    // pH Control
    pHController    : PID;
    pHSetpoint      : REAL := 7.2;      // Target pH
    pHDeadband      : REAL := 0.3;      // pH control deadband
    pHAlarmHigh     : REAL := 8.5;      // High pH alarm
    pHAlarmLow      : REAL := 6.5;      // Low pH alarm
    
    // Chlorine Control
    ChlorineController : PID;
    ChlorineSetpoint   : REAL := 0.5;   // Target chlorine (mg/L)
    ChlorineDeadband   : REAL := 0.1;   // Chlorine control deadband
    ChlorineAlarmHigh  : REAL := 2.0;   // High chlorine alarm
    ChlorineAlarmLow   : REAL := 0.2;   // Low chlorine alarm
    
    // TDS Monitoring
    TDSAlarmLimit   : REAL := 500.0;    // TDS alarm limit (ppm)
    TDSCriticalLimit : REAL := 800.0;   // Critical TDS limit
    
    // Turbidity Monitoring
    TurbidityAlarmLimit : REAL := 1.0;  // Turbidity alarm (NTU)
    TurbidityCriticalLimit : REAL := 4.0; // Critical turbidity
    
    // Conductivity Monitoring
    ConductivityAlarmLimit : REAL := 800.0; // Conductivity alarm (µS/cm)
    
    // Treatment system timers
    pHDoseTimer     : TON;
    ChlorineDoseTimer : TON;
    UVTimer         : TON;
    FlushTimer      : TON;
    
    // Quality monitoring
    QualityCheckTimer : TON;
    QualityCheckInterval : TIME := T#5m;
    
    // Dosing pump control
    pHDoseActive    : BOOL := FALSE;
    ChlorineDoseActive : BOOL := FALSE;
    
    // Historical data for trend analysis
    pHHistory       : ARRAY[1..10] OF REAL;
    ChlorineHistory : ARRAY[1..10] OF REAL;
    TDSHistory      : ARRAY[1..10] OF REAL;
    HistoryIndex    : INT := 1;
    
    // Alarm states
    pHAlarm         : BOOL := FALSE;
    ChlorineAlarm   : BOOL := FALSE;
    TDSAlarm        : BOOL := FALSE;
    TurbidityAlarm  : BOOL := FALSE;
    ConductivityAlarm : BOOL := FALSE;
    
    // Water quality grades
    OverallQuality  : INT := 0;         // 0=Poor, 1=Fair, 2=Good, 3=Excellent
    
END_VAR

// =====================================
// MAIN WATER QUALITY CONTROLLER
// =====================================

IF Reset THEN
    // Reset all controller states
    QualityAlarm := FALSE;
    TreatmentActive := FALSE;
    pHDoseActive := FALSE;
    ChlorineDoseActive := FALSE;
    pHController(bReset := TRUE);
    ChlorineController(bReset := TRUE);
    QualityCheckTimer(IN := FALSE);
END_IF

IF Enable THEN
    // Read and validate sensor data
    ReadWaterQualitySensors();
    
    // Update historical data
    UpdateQualityHistory();
    
    // pH Control System
    ControlpH();
    
    // Chlorine Control System
    ControlChlorine();
    
    // Monitor critical parameters
    MonitorCriticalParameters();
    
    // UV Sterilization Control
    ControlUVSterilization();
    
    // Calculate overall water quality
    CalculateOverallQuality();
    
    // Periodic quality checks
    PeriodicQualityCheck();
    
    TreatmentActive := pHDoseActive OR ChlorineDoseActive OR g_UVSterilizer;
    
ELSE
    // Controller disabled
    StopAllTreatment();
    QualityOK := FALSE;
    TreatmentActive := FALSE;
END_IF

// =====================================
// SENSOR DATA READING AND VALIDATION
// =====================================
FUNCTION ReadWaterQualitySensors : BOOL
VAR_INPUT
END_VAR

    // Read pH sensor with validation
    IF g_ProductpH >= 0.0 AND g_ProductpH <= 14.0 THEN
        g_ProductQuality.pH := g_ProductpH;
    ELSE
        // pH sensor fault - use last known good value
        pHAlarm := TRUE;
    END_IF
    
    // Read TDS sensor with validation
    IF g_ProductTDS >= 0.0 AND g_ProductTDS <= 2000.0 THEN
        g_ProductQuality.TDS := g_ProductTDS;
    ELSE
        // TDS sensor fault
        TDSAlarm := TRUE;
    END_IF
    
    // Read turbidity sensor with validation
    IF g_ProductTurbidity >= 0.0 AND g_ProductTurbidity <= 10.0 THEN
        g_ProductQuality.Turbidity := g_ProductTurbidity;
    ELSE
        // Turbidity sensor fault
        TurbidityAlarm := TRUE;
    END_IF
    
    // Read chlorine sensor with validation
    IF g_ChlorineLevel >= 0.0 AND g_ChlorineLevel <= 5.0 THEN
        g_ProductQuality.Chlorine := g_ChlorineLevel;
    ELSE
        // Chlorine sensor fault
        ChlorineAlarm := TRUE;
    END_IF
    
    // Calculate conductivity from TDS (approximate)
    g_ProductQuality.Conductivity := g_ProductQuality.TDS * 1.8;
    
    ReadWaterQualitySensors := TRUE;
END_FUNCTION

// =====================================
// pH CONTROL SYSTEM
// =====================================
FUNCTION ControlpH : BOOL
VAR_INPUT
END_VAR
VAR
    pHError         : REAL;
    DoseRate        : REAL;
END_VAR

    // Check if pH is within acceptable range
    pHError := ABS(g_ProductQuality.pH - pHSetpoint);
    
    IF pHError > pHDeadband AND AutoMode THEN
        // pH adjustment needed
        pHController(
            bEnable := TRUE,
            fSetpointValue := pHSetpoint,
            fActualValue := g_ProductQuality.pH,
            fKp := 1.5,
            fTn := 300.0,    // 5 minutes integral time
            fTv := 30.0,     // 30 seconds derivative time
            fOutMax := 100.0,
            fOutMin := 0.0
        );
        
        DoseRate := pHController.fOut;
        
        // Determine if acid or base dosing is needed
        IF g_ProductQuality.pH > pHSetpoint + pHDeadband THEN
            // pH too high - dose acid (or stop base dosing)
            g_pHDosingPump := TRUE;
            g_pHDoseRate := DoseRate;
            pHDoseActive := TRUE;
        ELSIF g_ProductQuality.pH < pHSetpoint - pHDeadband THEN
            // pH too low - dose base
            g_pHDosingPump := TRUE;
            g_pHDoseRate := DoseRate;
            pHDoseActive := TRUE;
        ELSE
            // pH within deadband
            g_pHDosingPump := FALSE;
            g_pHDoseRate := 0.0;
            pHDoseActive := FALSE;
        END_IF
        
    ELSE
        // pH within acceptable range or manual mode
        g_pHDosingPump := FALSE;
        g_pHDoseRate := 0.0;
        pHDoseActive := FALSE;
        pHController(bEnable := FALSE);
    END_IF
    
    // pH alarms
    pHAlarm := (g_ProductQuality.pH < pHAlarmLow) OR (g_ProductQuality.pH > pHAlarmHigh);
    
    ControlpH := TRUE;
END_FUNCTION

// =====================================
// CHLORINE CONTROL SYSTEM
// =====================================
FUNCTION ControlChlorine : BOOL
VAR_INPUT
END_VAR
VAR
    ChlorineError   : REAL;
    DoseRate        : REAL;
END_VAR

    // Check chlorine residual level
    ChlorineError := ChlorineSetpoint - g_ProductQuality.Chlorine;
    
    IF ABS(ChlorineError) > ChlorineDeadband AND AutoMode THEN
        // Chlorine adjustment needed
        ChlorineController(
            bEnable := TRUE,
            fSetpointValue := ChlorineSetpoint,
            fActualValue := g_ProductQuality.Chlorine,
            fKp := 2.0,
            fTn := 600.0,    // 10 minutes integral time
            fTv := 60.0,     // 1 minute derivative time
            fOutMax := 100.0,
            fOutMin := 0.0
        );
        
        DoseRate := ChlorineController.fOut;
        
        IF ChlorineError > ChlorineDeadband THEN
            // Chlorine too low - increase dosing
            g_ChlorineDosingPump := TRUE;
            g_ChlorineRate := DoseRate;
            ChlorineDoseActive := TRUE;
            
            // Timer to prevent overdosing
            ChlorineDoseTimer(IN := TRUE, PT := T#2m);
            
        ELSE
            // Chlorine adequate or too high
            g_ChlorineDosingPump := FALSE;
            g_ChlorineRate := 0.0;
            ChlorineDoseActive := FALSE;
            ChlorineDoseTimer(IN := FALSE);
        END_IF
        
    ELSE
        // Chlorine within acceptable range
        g_ChlorineDosingPump := FALSE;
        g_ChlorineRate := 0.0;
        ChlorineDoseActive := FALSE;
        ChlorineController(bEnable := FALSE);
    END_IF
    
    // Chlorine alarms
    ChlorineAlarm := (g_ProductQuality.Chlorine < ChlorineAlarmLow) OR 
                    (g_ProductQuality.Chlorine > ChlorineAlarmHigh);
    
    ControlChlorine := TRUE;
END_FUNCTION

// =====================================
// CRITICAL PARAMETER MONITORING
// =====================================
FUNCTION MonitorCriticalParameters : BOOL
VAR_INPUT
END_VAR

    // TDS Monitoring
    TDSAlarm := g_ProductQuality.TDS > TDSAlarmLimit;
    
    IF g_ProductQuality.TDS > TDSCriticalLimit THEN
        // Critical TDS level - stop production
        TDSAlarm := TRUE;
        QualityAlarm := TRUE;
        // Could trigger RO system cleaning or shutdown
    END_IF
    
    // Turbidity Monitoring
    TurbidityAlarm := g_ProductQuality.Turbidity > TurbidityAlarmLimit;
    
    IF g_ProductQuality.Turbidity > TurbidityCriticalLimit THEN
        // Critical turbidity - stop production
        TurbidityAlarm := TRUE;
        QualityAlarm := TRUE;
        // Could trigger filter backwash or replacement
    END_IF
    
    // Conductivity Monitoring
    ConductivityAlarm := g_ProductQuality.Conductivity > ConductivityAlarmLimit;
    
    // Overall quality alarm
    QualityAlarm := pHAlarm OR ChlorineAlarm OR TDSAlarm OR TurbidityAlarm OR ConductivityAlarm;
    
    // Set global alarm
    g_WaterQualityAlarm := QualityAlarm;
    
    MonitorCriticalParameters := TRUE;
END_FUNCTION

// =====================================
// UV STERILIZATION CONTROL
// =====================================
FUNCTION ControlUVSterilization : BOOL
VAR_INPUT
END_VAR

    // UV sterilizer control based on flow and quality
    IF g_SystemRunning AND g_PermeateFlow > 10.0 THEN
        // Start UV sterilizer when there's flow
        g_UVSterilizer := TRUE;
        
        // Monitor UV lamp performance
        UVTimer(IN := TRUE, PT := T#1h);
        IF UVTimer.Q THEN
            UVTimer(IN := FALSE);
            // Log UV operation time for lamp replacement scheduling
        END_IF
        
    ELSE
        // Stop UV sterilizer when no flow
        g_UVSterilizer := FALSE;
        UVTimer(IN := FALSE);
    END_IF
    
    // Additional UV control based on water quality
    IF TurbidityAlarm OR g_ProductQuality.Turbidity > 0.5 THEN
        // Ensure UV is running for disinfection when turbidity is elevated
        g_UVSterilizer := TRUE;
    END_IF
    
    ControlUVSterilization := TRUE;
END_FUNCTION

// =====================================
// OVERALL QUALITY CALCULATION
// =====================================
FUNCTION CalculateOverallQuality : BOOL
VAR_INPUT
END_VAR
VAR
    QualityScore    : INT := 0;
    ParameterCount  : INT := 0;
END_VAR

    // Reset quality score
    QualityScore := 0;
    ParameterCount := 0;
    
    // pH Quality Assessment
    IF g_ProductQuality.pH >= 6.8 AND g_ProductQuality.pH <= 7.8 THEN
        QualityScore := QualityScore + 3;  // Excellent
    ELSIF g_ProductQuality.pH >= 6.5 AND g_ProductQuality.pH <= 8.5 THEN
        QualityScore := QualityScore + 2;  // Good
    ELSIF g_ProductQuality.pH >= 6.0 AND g_ProductQuality.pH <= 9.0 THEN
        QualityScore := QualityScore + 1;  // Fair
    ELSE
        QualityScore := QualityScore + 0;  // Poor
    END_IF
    ParameterCount := ParameterCount + 1;
    
    // TDS Quality Assessment
    IF g_ProductQuality.TDS <= 200.0 THEN
        QualityScore := QualityScore + 3;  // Excellent
    ELSIF g_ProductQuality.TDS <= 400.0 THEN
        QualityScore := QualityScore + 2;  // Good
    ELSIF g_ProductQuality.TDS <= 600.0 THEN
        QualityScore := QualityScore + 1;  // Fair
    ELSE
        QualityScore := QualityScore + 0;  // Poor
    END_IF
    ParameterCount := ParameterCount + 1;
    
    // Turbidity Quality Assessment
    IF g_ProductQuality.Turbidity <= 0.1 THEN
        QualityScore := QualityScore + 3;  // Excellent
    ELSIF g_ProductQuality.Turbidity <= 0.5 THEN
        QualityScore := QualityScore + 2;  // Good
    ELSIF g_ProductQuality.Turbidity <= 1.0 THEN
        QualityScore := QualityScore + 1;  // Fair
    ELSE
        QualityScore := QualityScore + 0;  // Poor
    END_IF
    ParameterCount := ParameterCount + 1;
    
    // Chlorine Quality Assessment
    IF g_ProductQuality.Chlorine >= 0.3 AND g_ProductQuality.Chlorine <= 0.8 THEN
        QualityScore := QualityScore + 3;  // Excellent
    ELSIF g_ProductQuality.Chlorine >= 0.2 AND g_ProductQuality.Chlorine <= 1.2 THEN
        QualityScore := QualityScore + 2;  // Good
    ELSIF g_ProductQuality.Chlorine >= 0.1 AND g_ProductQuality.Chlorine <= 1.8 THEN
        QualityScore := QualityScore + 1;  // Fair
    ELSE
        QualityScore := QualityScore + 0;  // Poor
    END_IF
    ParameterCount := ParameterCount + 1;
    
    // Calculate average quality
    IF ParameterCount > 0 THEN
        OverallQuality := QualityScore / ParameterCount;
    ELSE
        OverallQuality := 0;
    END_IF
    
    // Determine if quality is acceptable
    QualityOK := (OverallQuality >= 2) AND NOT QualityAlarm;
    
    CalculateOverallQuality := TRUE;
END_FUNCTION

// =====================================
// QUALITY HISTORY TRACKING
// =====================================
FUNCTION UpdateQualityHistory : BOOL
VAR_INPUT
END_VAR

    QualityCheckTimer(IN := TRUE, PT := QualityCheckInterval);
    
    IF QualityCheckTimer.Q THEN
        QualityCheckTimer(IN := FALSE);
        
        // Store current values in history arrays
        pHHistory[HistoryIndex] := g_ProductQuality.pH;
        ChlorineHistory[HistoryIndex] := g_ProductQuality.Chlorine;
        TDSHistory[HistoryIndex] := g_ProductQuality.TDS;
        
        // Move to next history index
        HistoryIndex := HistoryIndex + 1;
        IF HistoryIndex > 10 THEN
            HistoryIndex := 1;
        END_IF
    END_IF
    
    UpdateQualityHistory := TRUE;
END_FUNCTION

// =====================================
// PERIODIC QUALITY CHECK
// =====================================
FUNCTION PeriodicQualityCheck : BOOL
VAR_INPUT
END_VAR
VAR
    i               : INT;
    pHAverage       : REAL := 0.0;
    ChlorineAverage : REAL := 0.0;
    TDSAverage      : REAL := 0.0;
    pHTrend         : REAL := 0.0;
    ChlorineTrend   : REAL := 0.0;
    TDSTrend        : REAL := 0.0;
END_VAR

    // Calculate average values from history
    FOR i := 1 TO 10 DO
        pHAverage := pHAverage + pHHistory[i];
        ChlorineAverage := ChlorineAverage + ChlorineHistory[i];
        TDSAverage := TDSAverage + TDSHistory[i];
    END_FOR
    
    pHAverage := pHAverage / 10.0;
    ChlorineAverage := ChlorineAverage / 10.0;
    TDSAverage := TDSAverage / 10.0;
    
    // Calculate trends (simple slope calculation)
    pHTrend := pHHistory[10] - pHHistory[1];
    ChlorineTrend := ChlorineHistory[10] - ChlorineHistory[1];
    TDSTrend := TDSHistory[10] - TDSHistory[1];
    
    // Trend analysis for predictive maintenance
    IF ABS(pHTrend) > 0.5 THEN
        // pH trending outside normal range
        // Could indicate pH sensor drift or treatment system issues
    END_IF
    
    IF TDSTrend > 50.0 THEN
        // TDS increasing - could indicate membrane fouling
        // Trigger cleaning cycle recommendation
    END_IF
    
    IF ChlorineTrend < -0.2 THEN
        // Chlorine decreasing - could indicate dosing system issues
        // Check chlorine pump and chemical levels
    END_IF
    
    PeriodicQualityCheck := TRUE;
END_FUNCTION

// =====================================
// EMERGENCY TREATMENT SHUTDOWN
// =====================================
FUNCTION StopAllTreatment : BOOL
VAR_INPUT
END_VAR

    // Stop all treatment systems
    g_ChlorineDosingPump := FALSE;
    g_pHDosingPump := FALSE;
    g_UVSterilizer := FALSE;
    
    g_ChlorineRate := 0.0;
    g_pHDoseRate := 0.0;
    
    // Reset active flags
    pHDoseActive := FALSE;
    ChlorineDoseActive := FALSE;
    
    // Stop timers
    pHDoseTimer(IN := FALSE);
    ChlorineDoseTimer(IN := FALSE);
    UVTimer(IN := FALSE);
    
    StopAllTreatment := TRUE;
END_FUNCTION

END_FUNCTION_BLOCK
