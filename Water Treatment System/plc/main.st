// Main Water Treatment System Control Program
// Seawater Desalination and Distribution System
// Author: PLC Control System
// Date: June 2025

PROGRAM Main
VAR
    // Local control variables
    StartupSequence     : INT := 0;         // Startup sequence step
    ShutdownSequence    : INT := 0;         // Shutdown sequence step
    ProductionCycle     : INT := 0;         // Production cycle step
    
    // Timer variables
    StartupTimer        : TON;              // System startup timer
    ShutdownTimer       : TON;              // System shutdown timer
    MaintenanceTimer    : TON;              // Maintenance interval timer
    ProductionTimer     : TON;              // Production cycle timer
    AlarmTimer          : TON;              // Alarm delay timer
    PumpRotationTimer   : TON;              // Pump rotation timer
    
    // Control flags
    SystemStartRequest  : BOOL := FALSE;    // System start request
    SystemStopRequest   : BOOL := FALSE;    // System stop request
    PumpRotationFlag    : BOOL := FALSE;    // Pump rotation flag
    CleaningCycleActive : BOOL := FALSE;    // RO cleaning cycle active
    
    // Process control variables
    RORecoveryRate      : REAL := 0.0;      // Calculated RO recovery rate
    SystemEfficiency    : REAL := 0.0;      // Overall system efficiency
    WaterLossRate       : REAL := 0.0;      // Water loss rate calculation
    
    // Maintenance tracking
    FilterHours         : ARRAY[1..5] OF REAL; // Filter operating hours
    PumpHours           : ARRAY[1..4] OF REAL; // Pump operating hours
    ROMembraneHours     : REAL := 0.0;      // RO membrane hours
    UVLampHours         : REAL := 0.0;      // UV lamp hours
    
END_VAR

// =====================================
// MAIN PROGRAM EXECUTION
// =====================================

// Read input signals and update system status
ReadInputs();

// Process emergency stop and safety systems
SafetyInterlocks();

// Handle system operating modes
CASE g_SystemMode OF
    STOPPED:
        SystemStoppedMode();
    
    STARTUP:
        SystemStartupMode();
    
    RUNNING:
        SystemRunningMode();
    
    SHUTDOWN:
        SystemShutdownMode();
    
    MAINTENANCE:
        MaintenanceMode();
    
    ALARM:
        AlarmMode();
END_CASE

// Execute water treatment processes
WaterTreatmentControl();

// Monitor and control water quality
WaterQualityControl();

// Tank level and distribution control
TankAndDistributionControl();

// Energy monitoring and optimization
EnergyManagement();

// Maintenance scheduling and alerts
MaintenanceManagement();

// Update outputs and HMI data
UpdateOutputs();

// =====================================
// INPUT PROCESSING
// =====================================
FUNCTION ReadInputs : BOOL
VAR_INPUT
END_VAR

    // Read digital inputs
    g_StartButton := StartButton;
    g_StopButton := StopButton;
    g_EmergencyButton := EmergencyButton;
    
    // Process start/stop requests
    IF g_StartButton AND NOT SystemStartRequest THEN
        SystemStartRequest := TRUE;
    END_IF
    
    IF g_StopButton AND NOT SystemStopRequest THEN
        SystemStopRequest := TRUE;
    END_IF
    
    // Update tank information
    g_GroundTank.Level := g_GroundTankLevel;
    g_GroundTank.Volume := g_GroundTank.Level * g_GroundTank.Capacity / 100.0;
    g_GroundTank.LowAlarm := g_GroundTankLevel < 20.0;
    g_GroundTank.HighAlarm := g_GroundTankLevel > 95.0;
    g_GroundTank.EmptyAlarm := g_GroundTankLevel < 5.0;
    
    g_RoofTank.Level := g_RoofTankLevel;
    g_RoofTank.Volume := g_RoofTank.Level * g_RoofTank.Capacity / 100.0;
    g_RoofTank.LowAlarm := g_RoofTankLevel < 30.0;
    g_RoofTank.HighAlarm := g_RoofTankLevel > 95.0;
    g_RoofTank.EmptyAlarm := g_RoofTankLevel < 10.0;
    
    // Update water quality data
    g_SeawaterQuality.TDS := g_SeawaterTDS;
    g_SeawaterQuality.Temperature := g_SeawaterTemp;
    g_ProductQuality.TDS := g_ProductTDS;
    g_ProductQuality.pH := g_ProductpH;
    g_ProductQuality.Turbidity := g_ProductTurbidity;
    g_ProductQuality.Chlorine := g_ChlorineLevel;
    g_ProductQuality.FlowRate := g_PermeateFlow;
    
    ReadInputs := TRUE;
END_FUNCTION

// =====================================
// SAFETY INTERLOCKS
// =====================================
FUNCTION SafetyInterlocks : BOOL
VAR_INPUT
END_VAR

    // Emergency stop processing
    IF g_EmergencyButton THEN
        g_EmergencyStop := TRUE;
        g_SystemMode := ALARM;
        
        // Stop all pumps immediately
        g_IntakePump := FALSE;
        g_PreFilterPump := FALSE;
        g_ROPump := FALSE;
        g_BoosterPump1 := FALSE;
        g_BoosterPump2 := FALSE;
        
        // Close critical valves
        g_IntakeValve := FALSE;
        g_ROPermeateValve := FALSE;
        
        g_SystemAlarm := TRUE;
        g_AlarmLight := TRUE;
    END_IF
    
    // Leak detection safety
    IF g_LeakDetector1 OR g_LeakDetector2 THEN
        g_LeakageAlarm := TRUE;
        
        // Stop pumps in affected zones
        IF g_LeakDetector1 THEN
            g_IntakePump := FALSE;
            g_PreFilterPump := FALSE;
        END_IF
        
        IF g_LeakDetector2 THEN
            g_ROPump := FALSE;
        END_IF
    END_IF
    
    // High pressure protection
    IF g_ROPressure > 65.0 THEN  // Emergency pressure limit
        g_ROPump := FALSE;
        g_ROSystemAlarm := TRUE;
        g_SystemAlarm := TRUE;
    END_IF
    
    // Tank overflow protection
    IF g_GroundTank.HighAlarm THEN
        g_IntakePump := FALSE;
        g_PreFilterPump := FALSE;
        g_ROPump := FALSE;
        g_GroundTankValve := FALSE;
    END_IF
    
    IF g_RoofTank.HighAlarm THEN
        g_BoosterPump1 := FALSE;
        g_BoosterPump2 := FALSE;
        g_RoofTankValve := FALSE;
    END_IF
    
    SafetyInterlocks := TRUE;
END_FUNCTION

// =====================================
// SYSTEM OPERATING MODES
// =====================================
FUNCTION SystemStoppedMode : BOOL
VAR_INPUT
END_VAR

    // All outputs off in stopped mode
    g_IntakePump := FALSE;
    g_PreFilterPump := FALSE;
    g_ROPump := FALSE;
    g_BoosterPump1 := FALSE;
    g_BoosterPump2 := FALSE;
    
    g_IntakeValve := FALSE;
    g_ROPermeateValve := FALSE;
    g_ConcentrateValve := FALSE;
    
    g_UVSterilizer := FALSE;
    g_ChlorineDosingPump := FALSE;
    g_pHDosingPump := FALSE;
    
    // Reset control variables
    StartupSequence := 0;
    ProductionCycle := 0;
    
    // Check for start request
    IF SystemStartRequest AND NOT g_EmergencyStop THEN
        g_SystemMode := STARTUP;
        SystemStartRequest := FALSE;
        g_StatusLight := TRUE;
    END_IF
    
    SystemStoppedMode := TRUE;
END_FUNCTION

FUNCTION SystemStartupMode : BOOL
VAR_INPUT
END_VAR

    // Startup sequence with proper delays
    CASE StartupSequence OF
        0: // Initialize startup
            StartupTimer(IN := TRUE, PT := T#2s);
            IF StartupTimer.Q THEN
                StartupTimer(IN := FALSE);
                StartupSequence := 1;
            END_IF
        
        1: // Open seawater intake valve
            g_IntakeValve := TRUE;
            StartupTimer(IN := TRUE, PT := T#5s);
            IF StartupTimer.Q THEN
                StartupTimer(IN := FALSE);
                StartupSequence := 2;
            END_IF
        
        2: // Start intake pump
            g_IntakePump := TRUE;
            g_IntakePumpSpeed := 60.0;  // Start at 60% speed
            StartupTimer(IN := TRUE, PT := T#10s);
            IF StartupTimer.Q THEN
                StartupTimer(IN := FALSE);
                StartupSequence := 3;
            END_IF
        
        3: // Start pre-filtration pump
            g_PreFilterPump := TRUE;
            StartupTimer(IN := TRUE, PT := T#15s);
            IF StartupTimer.Q THEN
                StartupTimer(IN := FALSE);
                StartupSequence := 4;
            END_IF
        
        4: // Start RO system
            g_ROPump := TRUE;
            g_ROPumpSpeed := 40.0;  // Start RO pump at low speed
            g_ConcentrateValve := TRUE;
            StartupTimer(IN := TRUE, PT := T#20s);
            IF StartupTimer.Q THEN
                StartupTimer(IN := FALSE);
                StartupSequence := 5;
            END_IF
        
        5: // Ramp up RO pressure gradually
            IF g_ROPressure < g_ROPressureSetpoint THEN
                g_ROPumpSpeed := g_ROPumpSpeed + 2.0;  // Increase speed gradually
                IF g_ROPumpSpeed > 90.0 THEN
                    g_ROPumpSpeed := 90.0;
                END_IF
            ELSE
                g_ROPermeateValve := TRUE;
                StartupSequence := 6;
            END_IF
        
        6: // Start post-treatment systems
            g_UVSterilizer := TRUE;
            g_GroundTankValve := TRUE;
            StartupTimer(IN := TRUE, PT := T#10s);
            IF StartupTimer.Q THEN
                StartupTimer(IN := FALSE);
                g_SystemMode := RUNNING;
                g_SystemRunning := TRUE;
                StartupSequence := 0;
            END_IF
    END_CASE
    
    // Abort startup on stop request or alarm
    IF SystemStopRequest OR g_EmergencyStop THEN
        g_SystemMode := SHUTDOWN;
        SystemStopRequest := FALSE;
        StartupSequence := 0;
    END_IF
    
    SystemStartupMode := TRUE;
END_FUNCTION

FUNCTION SystemRunningMode : BOOL
VAR_INPUT
END_VAR

    // Normal production operation
    g_SystemRunning := TRUE;
    g_StatusLight := TRUE;
    
    // Production cycle control
    CASE ProductionCycle OF
        0: // Normal production
            // Production is handled by other control functions
            ProductionTimer(IN := TRUE, PT := T#1h);  // 1 hour cycles
            IF ProductionTimer.Q THEN
                ProductionTimer(IN := FALSE);
                ProductionCycle := 1;  // Check for cleaning cycle
            END_IF
        
        1: // Check if RO cleaning needed
            IF g_ROSystemData.Fouling > 80.0 OR g_ROCleaningCycles < 1 THEN
                ProductionCycle := 2;  // Start cleaning cycle
                CleaningCycleActive := TRUE;
            ELSE
                ProductionCycle := 0;  // Continue production
            END_IF
        
        2: // RO cleaning cycle
            // Cleaning cycle implementation would go here
            // For now, simulate cleaning delay
            ProductionTimer(IN := TRUE, PT := T#30m);
            IF ProductionTimer.Q THEN
                ProductionTimer(IN := FALSE);
                g_ROCleaningCycles := g_ROCleaningCycles + 1;
                CleaningCycleActive := FALSE;
                ProductionCycle := 0;
            END_IF
    END_CASE
    
    // Check for stop request
    IF SystemStopRequest THEN
        g_SystemMode := SHUTDOWN;
        SystemStopRequest := FALSE;
    END_IF
    
    // Check for alarms that require shutdown
    IF g_EmergencyStop OR g_LeakageAlarm THEN
        g_SystemMode := ALARM;
    END_IF
    
    SystemRunningMode := TRUE;
END_FUNCTION

FUNCTION SystemShutdownMode : BOOL
VAR_INPUT
END_VAR

    // Controlled shutdown sequence
    CASE ShutdownSequence OF
        0: // Stop dosing pumps first
            g_ChlorineDosingPump := FALSE;
            g_pHDosingPump := FALSE;
            ShutdownTimer(IN := TRUE, PT := T#5s);
            IF ShutdownTimer.Q THEN
                ShutdownTimer(IN := FALSE);
                ShutdownSequence := 1;
            END_IF
        
        1: // Close permeate valve and reduce RO pressure
            g_ROPermeateValve := FALSE;
            g_ROPumpSpeed := g_ROPumpSpeed - 10.0;
            IF g_ROPumpSpeed <= 0.0 THEN
                g_ROPump := FALSE;
                ShutdownSequence := 2;
            END_IF
        
        2: // Stop RO pump and close concentrate valve
            g_ROPump := FALSE;
            g_ConcentrateValve := FALSE;
            ShutdownTimer(IN := TRUE, PT := T#10s);
            IF ShutdownTimer.Q THEN
                ShutdownTimer(IN := FALSE);
                ShutdownSequence := 3;
            END_IF
        
        3: // Stop pre-filtration pump
            g_PreFilterPump := FALSE;
            ShutdownTimer(IN := TRUE, PT := T#5s);
            IF ShutdownTimer.Q THEN
                ShutdownTimer(IN := FALSE);
                ShutdownSequence := 4;
            END_IF
        
        4: // Stop intake pump and close intake valve
            g_IntakePump := FALSE;
            g_IntakeValve := FALSE;
            ShutdownTimer(IN := TRUE, PT := T#10s);
            IF ShutdownTimer.Q THEN
                ShutdownTimer(IN := FALSE);
                ShutdownSequence := 5;
            END_IF
        
        5: // Stop remaining systems
            g_UVSterilizer := FALSE;
            g_GroundTankValve := FALSE;
            g_RoofTankValve := FALSE;
            g_SystemMode := STOPPED;
            g_SystemRunning := FALSE;
            g_StatusLight := FALSE;
            ShutdownSequence := 0;
    END_CASE
    
    SystemShutdownMode := TRUE;
END_FUNCTION

// =====================================
// WATER TREATMENT CONTROL
// =====================================
FUNCTION WaterTreatmentControl : BOOL
VAR_INPUT
END_VAR

    IF g_SystemRunning THEN
        // RO pressure control
        DesalinationController();
        
        // Water quality control
        WaterQualityController();
        
        // Pump control and sequencing
        PumpController();
    END_IF
    
    WaterTreatmentControl := TRUE;
END_FUNCTION

FUNCTION WaterQualityControl : BOOL
VAR_INPUT
END_VAR

    IF g_SystemRunning THEN
        // pH control
        IF g_ProductQuality.pH < g_ProductpHMin THEN
            g_pHDosingPump := TRUE;
            g_pHDoseRate := (g_ProductpHMin - g_ProductQuality.pH) * 20.0;
        ELSIF g_ProductQuality.pH > g_ProductpHMax THEN
            g_pHDosingPump := TRUE;
            g_pHDoseRate := (g_ProductQuality.pH - g_ProductpHMax) * 20.0;
        ELSE
            g_pHDosingPump := FALSE;
            g_pHDoseRate := 0.0;
        END_IF
        
        // Chlorine dosing control
        IF g_ProductQuality.Chlorine < g_ChlorineSetpoint THEN
            g_ChlorineDosingPump := TRUE;
            g_ChlorineRate := (g_ChlorineSetpoint - g_ProductQuality.Chlorine) * 50.0;
        ELSE
            g_ChlorineDosingPump := FALSE;
            g_ChlorineRate := 0.0;
        END_IF
        
        // Water quality alarms
        g_WaterQualityAlarm := (g_ProductQuality.TDS > g_ProductTDSLimit) OR
                              (g_ProductQuality.pH < g_ProductpHMin) OR
                              (g_ProductQuality.pH > g_ProductpHMax) OR
                              (g_ProductQuality.Turbidity > 1.0);
    END_IF
    
    WaterQualityControl := TRUE;
END_FUNCTION

FUNCTION TankAndDistributionControl : BOOL
VAR_INPUT
END_VAR

    // Ground tank control
    IF g_GroundTank.Level < 30.0 AND g_SystemRunning THEN
        // Increase production if tank is low
        g_IntakePumpSpeed := 80.0;
    ELSIF g_GroundTank.Level > 90.0 THEN
        // Reduce production if tank is nearly full
        g_IntakePumpSpeed := 40.0;
    ELSE
        g_IntakePumpSpeed := 60.0;  // Normal production rate
    END_IF
    
    // Roof tank filling control
    IF g_RoofTank.Level < 50.0 AND g_GroundTank.Level > 40.0 THEN
        g_BoosterPump1 := TRUE;
        g_RoofTankValve := TRUE;
        g_BoosterSpeed1 := 70.0;
        
        // Use second pump if level is very low
        IF g_RoofTank.Level < 30.0 THEN
            g_BoosterPump2 := TRUE;
            g_BoosterSpeed2 := 70.0;
        END_IF
    ELSIF g_RoofTank.Level > 90.0 THEN
        g_BoosterPump1 := FALSE;
        g_BoosterPump2 := FALSE;
        g_RoofTankValve := FALSE;
    END_IF
    
    // Distribution pressure control
    IF g_DistributionPressure < g_DistPressureSetpoint - 0.5 THEN
        // Increase pump speed to maintain pressure
        IF g_BoosterSpeed1 < 90.0 THEN
            g_BoosterSpeed1 := g_BoosterSpeed1 + 5.0;
        END_IF
        IF g_RoofTank.Level < 70.0 AND g_BoosterSpeed2 < 90.0 THEN
            g_BoosterPump2 := TRUE;
            g_BoosterSpeed2 := g_BoosterSpeed2 + 5.0;
        END_IF
    ELSIF g_DistributionPressure > g_DistPressureSetpoint + 0.5 THEN
        // Reduce pump speed if pressure is too high
        IF g_BoosterSpeed1 > 30.0 THEN
            g_BoosterSpeed1 := g_BoosterSpeed1 - 5.0;
        END_IF
        IF g_BoosterSpeed2 > 30.0 THEN
            g_BoosterSpeed2 := g_BoosterSpeed2 - 5.0;
        ELSIF g_BoosterSpeed2 <= 30.0 THEN
            g_BoosterPump2 := FALSE;
        END_IF
    END_IF
    
    TankAndDistributionControl := TRUE;
END_FUNCTION

FUNCTION EnergyManagement : BOOL
VAR_INPUT
END_VAR

    // Calculate total power consumption
    g_PowerConsumption := 0.0;
    
    // Add pump power consumption (estimated)
    IF g_IntakePump THEN
        g_PowerConsumption := g_PowerConsumption + (g_IntakePumpSpeed / 100.0) * 2.5;  // 2.5 kW max
    END_IF
    
    IF g_ROPump THEN
        g_PowerConsumption := g_PowerConsumption + (g_ROPumpSpeed / 100.0) * 7.5;  // 7.5 kW max
    END_IF
    
    IF g_BoosterPump1 THEN
        g_PowerConsumption := g_PowerConsumption + (g_BoosterSpeed1 / 100.0) * 3.0;  // 3.0 kW max
    END_IF
    
    IF g_BoosterPump2 THEN
        g_PowerConsumption := g_PowerConsumption + (g_BoosterSpeed2 / 100.0) * 3.0;  // 3.0 kW max
    END_IF
    
    // Add auxiliary equipment power
    IF g_UVSterilizer THEN
        g_PowerConsumption := g_PowerConsumption + 1.2;  // UV sterilizer
    END_IF
    
    // Calculate specific energy consumption
    IF g_ProductQuality.FlowRate > 0.0 THEN
        g_SpecificEnergy := g_PowerConsumption / (g_ProductQuality.FlowRate * 0.06);  // kWh/m³
    END_IF
    
    EnergyManagement := TRUE;
END_FUNCTION

FUNCTION MaintenanceManagement : BOOL
VAR_INPUT
END_VAR

    // Track operating hours for maintenance scheduling
    IF g_SystemRunning THEN
        // Update pump operating hours
        IF g_IntakePump THEN
            PumpHours[1] := PumpHours[1] + 0.001;  // Add time increment
        END_IF
        
        IF g_ROPump THEN
            PumpHours[2] := PumpHours[2] + 0.001;
            ROMembraneHours := ROMembraneHours + 0.001;
        END_IF
        
        IF g_BoosterPump1 THEN
            PumpHours[3] := PumpHours[3] + 0.001;
        END_IF
        
        IF g_BoosterPump2 THEN
            PumpHours[4] := PumpHours[4] + 0.001;
        END_IF
        
        IF g_UVSterilizer THEN
            UVLampHours := UVLampHours + 0.001;
        END_IF
    END_IF
    
    // Check maintenance intervals
    g_MaintenanceAlarm := (PumpHours[1] > 8760.0) OR  // Annual maintenance
                         (PumpHours[2] > 8760.0) OR
                         (PumpHours[3] > 8760.0) OR
                         (PumpHours[4] > 8760.0) OR
                         (ROMembraneHours > 17520.0) OR  // 2 years
                         (UVLampHours > 8760.0);  // Annual UV lamp replacement
    
    MaintenanceManagement := TRUE;
END_FUNCTION

FUNCTION AlarmMode : BOOL
VAR_INPUT
END_VAR

    // In alarm mode, maintain safe state
    g_SystemAlarm := TRUE;
    g_AlarmLight := TRUE;
    
    // Allow reset only if emergency stop is cleared and no active alarms
    IF NOT g_EmergencyStop AND NOT g_LeakageAlarm AND NOT g_WaterQualityAlarm THEN
        // Reset emergency stop if button is released
        IF NOT g_EmergencyButton THEN
            g_EmergencyStop := FALSE;
            g_SystemMode := STOPPED;
            g_SystemAlarm := FALSE;
            g_AlarmLight := FALSE;
        END_IF
    END_IF
    
    AlarmMode := TRUE;
END_FUNCTION

FUNCTION UpdateOutputs : BOOL
VAR_INPUT
END_VAR

    // Update all output signals based on control logic
    // Digital outputs are already set by control functions
    
    // Update analog outputs
    IntakePumpSpeed := g_IntakePumpSpeed;
    ROPumpSpeed := g_ROPumpSpeed;
    BoosterSpeed1 := g_BoosterSpeed1;
    BoosterSpeed2 := g_BoosterSpeed2;
    ChlorineRate := g_ChlorineRate;
    pHDoseRate := g_pHDoseRate;
    
    // Update status indicators
    StatusLight := g_StatusLight;
    AlarmLight := g_AlarmLight;
    SystemAlarm := g_SystemAlarm;
    
    UpdateOutputs := TRUE;
END_FUNCTION

END_PROGRAM
