PROGRAM dosing_controller
VAR
    PHPIDParams : PID_PARAMS;
    ChlorinePIDParams : PID_PARAMS;
    PHController : PID;
    ChlorineController : PID;
    PHControlOutput : REAL;
    ChlorineControlOutput : REAL;
    AcidDosingActive : BOOL := FALSE;
    BaseDosingActive : BOOL := FALSE;
    ChlorineDosingActive : BOOL := FALSE;
    ChemicalPulseTimer : TON;
    ChemicalPulseActive : BOOL := FALSE;
    DosingDisabled : BOOL := FALSE;
    DosingRate : REAL := 0.0;
    ChlorineDosingRate : REAL := 0.0;
    UrgentPHCorrection : BOOL := FALSE;
    PreviousPHValue : REAL := 7.0;
    PHChangeRate : REAL := 0.0;
    PHCalculationTimer : TON;
END_VAR

(* Chemical Dosing Controller *)
(* Manages chemical dosing for pH control and disinfection *)

(* Only run when system is operational *)
IF SystemRunning AND SystemState < 4 THEN

    (* Calculate pH change rate every minute *)
    PHCalculationTimer(IN := TRUE, PT := T#1M);
    IF PHCalculationTimer.Q THEN
        PHChangeRate := (ScaledPHValue - PreviousPHValue) / 60.0; (* pH units per second *)
        PreviousPHValue := ScaledPHValue;
        PHCalculationTimer(IN := FALSE);
        PHCalculationTimer(IN := TRUE, PT := T#1M);
    END_IF
    
    (* Check if urgent pH correction is needed *)
    UrgentPHCorrection := (ScaledPHValue < MIN_PH - 0.5) OR (ScaledPHValue > MAX_PH + 0.5);
    
    (* Disable dosing during certain conditions *)
    DosingDisabled := (SystemState = 4) OR TANK_HIGH_LEVEL OR MaintenanceRequired OR 
                     (ScaledTankLevel1 < 0.1) OR (ScaledFlowRate < 10.0);
    
    (* pH Control *)
    IF NOT DosingDisabled AND OperatingMode = 1 THEN
        (* Configure pH PID controller *)
        PHPIDParams.Kp := 5.0;   (* Proportional gain *)
        PHPIDParams.Ki := 0.2;   (* Integral gain *)
        PHPIDParams.Kd := 1.0;   (* Derivative gain *)
        PHPIDParams.Deadband := 0.1; (* Deadband to prevent oscillations *)
        PHPIDParams.MaxOutput := 100.0; (* 0-100% output range *)
        PHPIDParams.MinOutput := 0.0;
        
        (* Execute pH PID control *)
        PHController.Parameters := PHPIDParams;
        PHController.Setpoint := PHSetpoint;
        PHController.ProcessValue := ScaledPHValue;
        PHController.Execute();
        PHControlOutput := PHController.Output;
        
        (* Determine if acid or base dosing is needed *)
        IF ScaledPHValue > (PHSetpoint + 0.2) THEN
            (* pH too high - need acid *)
            AcidDosingActive := TRUE;
            BaseDosingActive := FALSE;
            
            (* Calculate acid dosing rate, proportional to deviation *)
            DosingRate := PHControlOutput;
            
            (* Apply limits and safety checks *)
            IF ACID_TANK_LOW THEN
                DosingRate := DosingRate * 0.5; (* Reduce dosing when supply low *)
            END_IF
            
            (* Convert to PLC output format *)
            ACID_DOSING_RATE := REAL_TO_INT(DosingRate * 27648.0 / 100.0);
            BASE_DOSING_RATE := 0;
            
            (* Control dosing pump *)
            ACID_DOSING_PUMP := (DosingRate > 5.0);
            BASE_DOSING_PUMP := FALSE;
            
        ELSIF ScaledPHValue < (PHSetpoint - 0.2) THEN
            (* pH too low - need base *)
            AcidDosingActive := FALSE;
            BaseDosingActive := TRUE;
            
            (* Calculate base dosing rate, proportional to deviation *)
            DosingRate := PHControlOutput;
            
            (* Apply limits and safety checks *)
            IF ABS(PHChangeRate) > 0.01 THEN
                (* pH changing quickly - reduce dosing to prevent overshooting *)
                DosingRate := DosingRate * 0.7;
            END_IF
            
            (* Convert to PLC output format *)
            ACID_DOSING_RATE := 0;
            BASE_DOSING_RATE := REAL_TO_INT(DosingRate * 27648.0 / 100.0);
            
            (* Control dosing pump *)
            ACID_DOSING_PUMP := FALSE;
            BASE_DOSING_PUMP := (DosingRate > 5.0);
            
        ELSE
            (* pH within acceptable range - no dosing needed *)
            AcidDosingActive := FALSE;
            BaseDosingActive := FALSE;
            ACID_DOSING_PUMP := FALSE;
            BASE_DOSING_PUMP := FALSE;
            ACID_DOSING_RATE := 0;
            BASE_DOSING_RATE := 0;
        END_IF
        
        (* Disinfection Control - Chlorine Dosing *)
        IF OUTLET_VALVE AND ScaledFlowRate > 20.0 THEN
            (* Configure chlorine PID controller *)
            ChlorinePIDParams.Kp := 3.0;   (* Proportional gain *)
            ChlorinePIDParams.Ki := 0.1;   (* Integral gain *)
            ChlorinePIDParams.Kd := 0.5;   (* Derivative gain *)
            ChlorinePIDParams.Deadband := 0.05; (* Deadband to prevent oscillations *)
            ChlorinePIDParams.MaxOutput := 100.0; (* 0-100% output range *)
            ChlorinePIDParams.MinOutput := 0.0;
            
            (* Execute chlorine PID control *)
            ChlorineController.Parameters := ChlorinePIDParams;
            ChlorineController.Setpoint := ChlorineDosageSetpoint;
            ChlorineController.ProcessValue := ScaledChlorineResidual;
            ChlorineController.Execute();
            ChlorineControlOutput := ChlorineController.Output;
            
            (* Apply chlorine dosing *)
            ChlorineDosingActive := TRUE;
            
            (* Calculate dosing rate with flow-based adjustment *)
            ChlorineDosingRate := ChlorineControlOutput * (ScaledFlowRate / FlowRateSetpoint);
            
            (* Apply limits and safety checks *)
            IF CHLORINE_LOW THEN
                ChlorineDosingRate := ChlorineDosingRate * 0.5; (* Reduce when supply low *)
            END_IF
            
            (* Convert to PLC output format *)
            CHLORINE_DOSING_RATE := REAL_TO_INT(ChlorineDosingRate * 27648.0 / 100.0);
            
            (* Control dosing pump *)
            CHLORINE_DOSING := (ChlorineDosingRate > 5.0);
            
            (* Track chemical usage *)
            IF CHLORINE_DOSING THEN
                TotalChemicalUsage := TotalChemicalUsage + (ChlorineDosingRate * 0.001); (* L per cycle *)
            END_IF
            
        ELSE
            (* No outlet flow - stop chlorine dosing *)
            ChlorineDosingActive := FALSE;
            CHLORINE_DOSING := FALSE;
            CHLORINE_DOSING_RATE := 0;
        END_IF
        
    ELSE
        (* System in fault or manual mode - disable all chemical dosing *)
        AcidDosingActive := FALSE;
        BaseDosingActive := FALSE;
        ChlorineDosingActive := FALSE;
        ACID_DOSING_PUMP := FALSE;
        BASE_DOSING_PUMP := FALSE;
        CHLORINE_DOSING := FALSE;
        ACID_DOSING_RATE := 0;
        BASE_DOSING_RATE := 0;
        CHLORINE_DOSING_RATE := 0;
    END_IF
    
    (* Pulse-based dosing for more precise chemical control *)
    IF (AcidDosingActive OR BaseDosingActive OR ChlorineDosingActive) AND DosingRate > 0.0 THEN
        ChemicalPulseTimer(IN := TRUE, PT := T#10S);
        IF ChemicalPulseTimer.Q THEN
            ChemicalPulseTimer(IN := FALSE);
            ChemicalPulseActive := NOT ChemicalPulseActive;
            
            (* Modify dosing pattern based on pulse state *)
            IF ChemicalPulseActive THEN
                IF AcidDosingActive THEN
                    ACID_DOSING_PUMP := TRUE;
                END_IF
                IF BaseDosingActive THEN
                    BASE_DOSING_PUMP := TRUE;
                END_IF
                IF ChlorineDosingActive THEN
                    CHLORINE_DOSING := TRUE;
                END_IF
            ELSE
                (* Keep pumps running for high demand, otherwise pulse them *)
                IF AcidDosingActive AND DosingRate < 30.0 AND NOT UrgentPHCorrection THEN
                    ACID_DOSING_PUMP := FALSE;
                END_IF
                IF BaseDosingActive AND DosingRate < 30.0 AND NOT UrgentPHCorrection THEN
                    BASE_DOSING_PUMP := FALSE;
                END_IF
                IF ChlorineDosingActive AND ChlorineDosingRate < 20.0 THEN
                    CHLORINE_DOSING := FALSE;
                END_IF
            END_IF
        END_IF
    ELSE
        ChemicalPulseTimer(IN := FALSE);
    END_IF
    
END_IF

END_PROGRAM
