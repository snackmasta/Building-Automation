// Pump Controller Function Block
// Multi-pump Control and Sequencing for Water Treatment System
// Author: PLC Control System
// Date: June 2025

FUNCTION_BLOCK PumpController
VAR_INPUT
    Enable          : BOOL := FALSE;    // Enable pump controller
    AutoMode        : BOOL := TRUE;     // Automatic mode selection
    ManualOverride  : BOOL := FALSE;    // Manual override mode
    Reset           : BOOL := FALSE;    // Reset controller
END_VAR

VAR_OUTPUT
    SystemReady     : BOOL := FALSE;    // Pump system ready
    SystemFault     : BOOL := FALSE;    // Pump system fault
    MaintenanceReq  : BOOL := FALSE;    // Maintenance required
END_VAR

VAR
    // Pump rotation and sequencing
    PumpRotationTimer   : TON;
    RotationInterval    : TIME := T#24h;    // 24-hour rotation
    ActivePumpIndex     : INT := 1;         // Currently active pump (1-4)
    PumpRunHours        : ARRAY[1..4] OF REAL; // Operating hours per pump
    
    // Pump control state machines
    IntakePumpState     : INT := 0;
    ROPumpState         : INT := 0;
    BoosterPump1State   : INT := 0;
    BoosterPump2State   : INT := 0;
    
    // Pump monitoring
    PumpStartDelay      : TON;
    PumpStopDelay       : TON;
    FaultCheckTimer     : TON;
    
    // Vibration and performance monitoring
    PerformanceCheck    : TON;
    PerformanceInterval : TIME := T#1h;
    
    // Pump efficiency tracking
    IntakeEfficiency    : REAL := 0.0;
    ROEfficiency        : REAL := 0.0;
    BoosterEfficiency1  : REAL := 0.0;
    BoosterEfficiency2  : REAL := 0.0;
    
END_VAR

// =====================================
// MAIN PUMP CONTROLLER
// =====================================

IF Reset THEN
    // Reset all pump states
    IntakePumpState := 0;
    ROPumpState := 0;
    BoosterPump1State := 0;
    BoosterPump2State := 0;
    SystemFault := FALSE;
    PumpRotationTimer(IN := FALSE);
    PumpStartDelay(IN := FALSE);
    PumpStopDelay(IN := FALSE);
END_IF

IF Enable THEN
    // Update pump operating hours
    UpdatePumpHours();
    
    // Pump rotation management
    ManagePumpRotation();
    
    // Individual pump controllers
    ControlIntakePump();
    ControlROPump();
    ControlBoosterPumps();
    
    // Monitor pump performance
    MonitorPumpPerformance();
    
    // Check maintenance requirements
    CheckMaintenanceRequirements();
    
    SystemReady := NOT SystemFault;
    
ELSE
    // Controller disabled - stop all pumps safely
    StopAllPumps();
    SystemReady := FALSE;
END_IF

// =====================================
// PUMP OPERATING HOURS TRACKING
// =====================================
FUNCTION UpdatePumpHours : BOOL
VAR_INPUT
END_VAR

    // Update operating hours for each pump
    IF g_IntakePump THEN
        PumpRunHours[1] := PumpRunHours[1] + 0.001;  // Increment time
        g_IntakePumpData.Hours := PumpRunHours[1];
    END_IF
    
    IF g_ROPump THEN
        PumpRunHours[2] := PumpRunHours[2] + 0.001;
        g_ROPumpData.Hours := PumpRunHours[2];
    END_IF
    
    IF g_BoosterPump1 THEN
        PumpRunHours[3] := PumpRunHours[3] + 0.001;
        g_BoosterPump1Data.Hours := PumpRunHours[3];
    END_IF
    
    IF g_BoosterPump2 THEN
        PumpRunHours[4] := PumpRunHours[4] + 0.001;
        g_BoosterPump2Data.Hours := PumpRunHours[4];
    END_IF
    
    UpdatePumpHours := TRUE;
END_FUNCTION

// =====================================
// PUMP ROTATION MANAGEMENT
// =====================================
FUNCTION ManagePumpRotation : BOOL
VAR_INPUT
END_VAR

    // Automatic pump rotation for equal wear
    PumpRotationTimer(IN := TRUE, PT := RotationInterval);
    
    IF PumpRotationTimer.Q AND AutoMode THEN
        PumpRotationTimer(IN := FALSE);
        
        // Rotate to next pump in sequence
        ActivePumpIndex := ActivePumpIndex + 1;
        IF ActivePumpIndex > 4 THEN
            ActivePumpIndex := 1;
        END_IF
        
        // Apply rotation logic for booster pumps
        RotateBoosterPumps();
    END_IF
    
    ManagePumpRotation := TRUE;
END_FUNCTION

FUNCTION RotateBoosterPumps : BOOL
VAR_INPUT
END_VAR

    // Rotate booster pumps based on operating hours
    IF PumpRunHours[3] > PumpRunHours[4] + 100.0 THEN
        // Pump 1 has significantly more hours, prefer pump 2
        IF g_BoosterPump1 AND NOT g_BoosterPump2 THEN
            g_BoosterPump1 := FALSE;
            PumpStopDelay(IN := TRUE, PT := T#5s);
            IF PumpStopDelay.Q THEN
                g_BoosterPump2 := TRUE;
                g_BoosterSpeed2 := g_BoosterSpeed1;
                g_BoosterSpeed1 := 0.0;
                PumpStopDelay(IN := FALSE);
            END_IF
        END_IF
    ELSIF PumpRunHours[4] > PumpRunHours[3] + 100.0 THEN
        // Pump 2 has significantly more hours, prefer pump 1
        IF g_BoosterPump2 AND NOT g_BoosterPump1 THEN
            g_BoosterPump2 := FALSE;
            PumpStopDelay(IN := TRUE, PT := T#5s);
            IF PumpStopDelay.Q THEN
                g_BoosterPump1 := TRUE;
                g_BoosterSpeed1 := g_BoosterSpeed2;
                g_BoosterSpeed2 := 0.0;
                PumpStopDelay(IN := FALSE);
            END_IF
        END_IF
    END_IF
    
    RotateBoosterPumps := TRUE;
END_FUNCTION

// =====================================
// INTAKE PUMP CONTROL
// =====================================
FUNCTION ControlIntakePump : BOOL
VAR_INPUT
END_VAR

    CASE IntakePumpState OF
        0: // Stopped
            g_IntakePump := FALSE;
            g_IntakePumpSpeed := 0.0;
            g_IntakePumpData.Running := FALSE;
            
            IF g_SystemRunning AND NOT SystemFault THEN
                IntakePumpState := 1;  // Start sequence
            END_IF
        
        1: // Starting
            PumpStartDelay(IN := TRUE, PT := T#3s);
            
            IF PumpStartDelay.Q THEN
                g_IntakePump := TRUE;
                g_IntakePumpSpeed := 30.0;  // Start at low speed
                PumpStartDelay(IN := FALSE);
                IntakePumpState := 2;  // Ramp up
            END_IF
        
        2: // Ramping up
            IF g_IntakePumpSpeed < g_IntakePumpSpeed THEN
                g_IntakePumpSpeed := g_IntakePumpSpeed + 5.0;
            ELSE
                IntakePumpState := 3;  // Normal operation
            END_IF
        
        3: // Normal operation
            g_IntakePumpData.Running := TRUE;
            
            // Monitor pump current and pressure
            MonitorIntakePump();
            
            IF NOT g_SystemRunning OR SystemFault THEN
                IntakePumpState := 4;  // Stop sequence
            END_IF
        
        4: // Stopping
            g_IntakePumpSpeed := g_IntakePumpSpeed - 10.0;
            
            IF g_IntakePumpSpeed <= 0.0 THEN
                g_IntakePump := FALSE;
                g_IntakePumpSpeed := 0.0;
                IntakePumpState := 0;  // Stopped
            END_IF
    END_CASE
    
    ControlIntakePump := TRUE;
END_FUNCTION

// =====================================
// RO PUMP CONTROL
// =====================================
FUNCTION ControlROPump : BOOL
VAR_INPUT
END_VAR

    CASE ROPumpState OF
        0: // Stopped
            g_ROPump := FALSE;
            g_ROPumpSpeed := 0.0;
            g_ROPumpData.Running := FALSE;
            
            IF g_SystemRunning AND NOT SystemFault AND g_IntakePump THEN
                ROPumpState := 1;  // Start sequence
            END_IF
        
        1: // Pre-start delay
            PumpStartDelay(IN := TRUE, PT := T#10s);
            
            IF PumpStartDelay.Q THEN
                g_ROPump := TRUE;
                g_ROPumpSpeed := 20.0;  // Start at very low speed
                PumpStartDelay(IN := FALSE);
                ROPumpState := 2;  // Gradual pressure build
            END_IF
        
        2: // Pressure building
            // Gradual speed increase to build pressure slowly
            IF g_ROPressure < 30.0 AND g_ROPumpSpeed < 50.0 THEN
                g_ROPumpSpeed := g_ROPumpSpeed + 2.0;  // Slow ramp
            ELSIF g_ROPressure >= 30.0 THEN
                ROPumpState := 3;  // Normal operation
            END_IF
            
            // Safety check - don't exceed pressure too quickly
            IF g_ROPressure > 40.0 THEN
                g_ROPumpSpeed := g_ROPumpSpeed - 5.0;
            END_IF
        
        3: // Normal operation
            g_ROPumpData.Running := TRUE;
            
            // Pump speed is controlled by desalination controller
            // Monitor pump performance here
            MonitorROPump();
            
            IF NOT g_SystemRunning OR SystemFault THEN
                ROPumpState := 4;  // Stop sequence
            END_IF
        
        4: // Stopping
            // Gradual pressure reduction
            g_ROPumpSpeed := g_ROPumpSpeed - 5.0;
            
            IF g_ROPumpSpeed <= 0.0 THEN
                g_ROPump := FALSE;
                g_ROPumpSpeed := 0.0;
                ROPumpState := 0;  // Stopped
            END_IF
    END_CASE
    
    ControlROPump := TRUE;
END_FUNCTION

// =====================================
// BOOSTER PUMPS CONTROL
// =====================================
FUNCTION ControlBoosterPumps : BOOL
VAR_INPUT
END_VAR

    // Booster Pump 1 Control
    CASE BoosterPump1State OF
        0: // Stopped
            g_BoosterPump1 := FALSE;
            g_BoosterSpeed1 := 0.0;
            g_BoosterPump1Data.Running := FALSE;
            
            IF g_RoofTank.Level < 70.0 AND g_GroundTank.Level > 30.0 THEN
                BoosterPump1State := 1;  // Start
            END_IF
        
        1: // Starting
            PumpStartDelay(IN := TRUE, PT := T#2s);
            
            IF PumpStartDelay.Q THEN
                g_BoosterPump1 := TRUE;
                g_BoosterSpeed1 := 40.0;  // Start speed
                PumpStartDelay(IN := FALSE);
                BoosterPump1State := 2;  // Running
            END_IF
        
        2: // Running
            g_BoosterPump1Data.Running := TRUE;
            
            // Speed control is handled by tank control logic
            MonitorBoosterPump1();
            
            IF g_RoofTank.Level > 90.0 OR g_GroundTank.Level < 20.0 THEN
                BoosterPump1State := 3;  // Stop
            END_IF
        
        3: // Stopping
            g_BoosterSpeed1 := g_BoosterSpeed1 - 10.0;
            
            IF g_BoosterSpeed1 <= 0.0 THEN
                g_BoosterPump1 := FALSE;
                g_BoosterSpeed1 := 0.0;
                BoosterPump1State := 0;  // Stopped
            END_IF
    END_CASE
    
    // Booster Pump 2 Control (similar logic with different conditions)
    CASE BoosterPump2State OF
        0: // Stopped
            g_BoosterPump2 := FALSE;
            g_BoosterSpeed2 := 0.0;
            g_BoosterPump2Data.Running := FALSE;
            
            // Start pump 2 if pump 1 is running and demand is high
            IF g_RoofTank.Level < 50.0 AND g_BoosterPump1 AND g_GroundTank.Level > 40.0 THEN
                BoosterPump2State := 1;  // Start
            END_IF
        
        1: // Starting
            PumpStartDelay(IN := TRUE, PT := T#2s);
            
            IF PumpStartDelay.Q THEN
                g_BoosterPump2 := TRUE;
                g_BoosterSpeed2 := 40.0;  // Start speed
                PumpStartDelay(IN := FALSE);
                BoosterPump2State := 2;  // Running
            END_IF
        
        2: // Running
            g_BoosterPump2Data.Running := TRUE;
            
            MonitorBoosterPump2();
            
            IF g_RoofTank.Level > 80.0 OR NOT g_BoosterPump1 THEN
                BoosterPump2State := 3;  // Stop
            END_IF
        
        3: // Stopping
            g_BoosterSpeed2 := g_BoosterSpeed2 - 10.0;
            
            IF g_BoosterSpeed2 <= 0.0 THEN
                g_BoosterPump2 := FALSE;
                g_BoosterSpeed2 := 0.0;
                BoosterPump2State := 0;  // Stopped
            END_IF
    END_CASE
    
    ControlBoosterPumps := TRUE;
END_FUNCTION

// =====================================
// PUMP MONITORING FUNCTIONS
// =====================================
FUNCTION MonitorIntakePump : BOOL
VAR_INPUT
END_VAR

    // Calculate pump efficiency (simplified)
    IF g_IntakePumpSpeed > 0.0 THEN
        IntakeEfficiency := (g_SeawaterQuality.FlowRate / g_IntakePumpSpeed) * 100.0;
    ELSE
        IntakeEfficiency := 0.0;
    END_IF
    
    // Update pump data structure
    g_IntakePumpData.Speed := g_IntakePumpSpeed;
    g_IntakePumpData.FlowRate := g_SeawaterQuality.FlowRate;
    g_IntakePumpData.Pressure := g_SeawaterQuality.Pressure;
    
    // Fault detection
    g_IntakePumpData.Fault := (g_IntakePumpData.Current > 15.0) OR  // Overcurrent
                             (IntakeEfficiency < 30.0 AND g_IntakePumpSpeed > 50.0);  // Low efficiency
    
    IF g_IntakePumpData.Fault THEN
        SystemFault := TRUE;
    END_IF
    
    MonitorIntakePump := TRUE;
END_FUNCTION

FUNCTION MonitorROPump : BOOL
VAR_INPUT
END_VAR

    // Calculate RO pump efficiency
    IF g_ROPumpSpeed > 0.0 THEN
        ROEfficiency := (g_ROPressure / g_ROPumpSpeed) * 100.0 / 55.0;  // Normalized to 55 bar
    ELSE
        ROEfficiency := 0.0;
    END_IF
    
    // Update pump data structure
    g_ROPumpData.Speed := g_ROPumpSpeed;
    g_ROPumpData.FlowRate := g_PermeateFlow;
    g_ROPumpData.Pressure := g_ROPressure;
    
    // Fault detection
    g_ROPumpData.Fault := (g_ROPumpData.Current > 25.0) OR  // Overcurrent
                         (g_ROPressure < 20.0 AND g_ROPumpSpeed > 60.0) OR  // Low pressure
                         (ROEfficiency < 40.0 AND g_ROPumpSpeed > 50.0);  // Low efficiency
    
    IF g_ROPumpData.Fault THEN
        SystemFault := TRUE;
    END_IF
    
    MonitorROPump := TRUE;
END_FUNCTION

FUNCTION MonitorBoosterPump1 : BOOL
VAR_INPUT
END_VAR

    // Calculate booster pump efficiency
    IF g_BoosterSpeed1 > 0.0 THEN
        BoosterEfficiency1 := (g_DistributionPressure / g_BoosterSpeed1) * 100.0 / 3.5;  // Normalized
    ELSE
        BoosterEfficiency1 := 0.0;
    END_IF
    
    // Update pump data structure
    g_BoosterPump1Data.Speed := g_BoosterSpeed1;
    g_BoosterPump1Data.Pressure := g_DistributionPressure;
    
    // Fault detection
    g_BoosterPump1Data.Fault := (g_BoosterPump1Data.Current > 12.0) OR  // Overcurrent
                               (BoosterEfficiency1 < 35.0 AND g_BoosterSpeed1 > 50.0);  // Low efficiency
    
    IF g_BoosterPump1Data.Fault THEN
        SystemFault := TRUE;
    END_IF
    
    MonitorBoosterPump1 := TRUE;
END_FUNCTION

FUNCTION MonitorBoosterPump2 : BOOL
VAR_INPUT
END_VAR

    // Calculate booster pump efficiency
    IF g_BoosterSpeed2 > 0.0 THEN
        BoosterEfficiency2 := (g_DistributionPressure / g_BoosterSpeed2) * 100.0 / 3.5;  // Normalized
    ELSE
        BoosterEfficiency2 := 0.0;
    END_IF
    
    // Update pump data structure
    g_BoosterPump2Data.Speed := g_BoosterSpeed2;
    g_BoosterPump2Data.Pressure := g_DistributionPressure;
    
    // Fault detection
    g_BoosterPump2Data.Fault := (g_BoosterPump2Data.Current > 12.0) OR  // Overcurrent
                               (BoosterEfficiency2 < 35.0 AND g_BoosterSpeed2 > 50.0);  // Low efficiency
    
    IF g_BoosterPump2Data.Fault THEN
        SystemFault := TRUE;
    END_IF
    
    MonitorBoosterPump2 := TRUE;
END_FUNCTION

// =====================================
// PERFORMANCE MONITORING
// =====================================
FUNCTION MonitorPumpPerformance : BOOL
VAR_INPUT
END_VAR

    PerformanceCheck(IN := TRUE, PT := PerformanceInterval);
    
    IF PerformanceCheck.Q THEN
        PerformanceCheck(IN := FALSE);
        
        // Log performance data and check trends
        // This would interface with data logging system
        
        // Check for performance degradation
        IF IntakeEfficiency < 40.0 THEN
            g_IntakePumpData.Maintenance := TRUE;
        END_IF
        
        IF ROEfficiency < 50.0 THEN
            g_ROPumpData.Maintenance := TRUE;
        END_IF
        
        IF BoosterEfficiency1 < 45.0 THEN
            g_BoosterPump1Data.Maintenance := TRUE;
        END_IF
        
        IF BoosterEfficiency2 < 45.0 THEN
            g_BoosterPump2Data.Maintenance := TRUE;
        END_IF
    END_IF
    
    MonitorPumpPerformance := TRUE;
END_FUNCTION

// =====================================
// MAINTENANCE REQUIREMENTS
// =====================================
FUNCTION CheckMaintenanceRequirements : BOOL
VAR_INPUT
END_VAR

    MaintenanceReq := FALSE;
    
    // Check operating hours for scheduled maintenance
    IF PumpRunHours[1] > 8760.0 THEN  // Annual maintenance
        g_IntakePumpData.Maintenance := TRUE;
        MaintenanceReq := TRUE;
    END_IF
    
    IF PumpRunHours[2] > 6000.0 THEN  // RO pump needs more frequent maintenance
        g_ROPumpData.Maintenance := TRUE;
        MaintenanceReq := TRUE;
    END_IF
    
    IF PumpRunHours[3] > 8760.0 THEN
        g_BoosterPump1Data.Maintenance := TRUE;
        MaintenanceReq := TRUE;
    END_IF
    
    IF PumpRunHours[4] > 8760.0 THEN
        g_BoosterPump2Data.Maintenance := TRUE;
        MaintenanceReq := TRUE;
    END_IF
    
    // Check for any pump faults
    IF g_IntakePumpData.Fault OR g_ROPumpData.Fault OR 
       g_BoosterPump1Data.Fault OR g_BoosterPump2Data.Fault THEN
        MaintenanceReq := TRUE;
    END_IF
    
    CheckMaintenanceRequirements := TRUE;
END_FUNCTION

// =====================================
// EMERGENCY STOP ALL PUMPS
// =====================================
FUNCTION StopAllPumps : BOOL
VAR_INPUT
END_VAR

    // Immediate stop of all pumps
    g_IntakePump := FALSE;
    g_ROPump := FALSE;
    g_BoosterPump1 := FALSE;
    g_BoosterPump2 := FALSE;
    
    g_IntakePumpSpeed := 0.0;
    g_ROPumpSpeed := 0.0;
    g_BoosterSpeed1 := 0.0;
    g_BoosterSpeed2 := 0.0;
    
    // Reset all pump states
    IntakePumpState := 0;
    ROPumpState := 0;
    BoosterPump1State := 0;
    BoosterPump2State := 0;
    
    StopAllPumps := TRUE;
END_FUNCTION

END_FUNCTION_BLOCK
