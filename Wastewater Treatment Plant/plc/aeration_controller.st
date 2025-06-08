PROGRAM aeration_controller
VAR
    DOPIDParams : PID_PARAMS;
    DOController : PID;
    DOControlOutput : REAL;
    BlowerSpeedOutput : REAL := 0.0;
    AerationCycle : INT := 0;
    AerationTimer : TON;
    AerationPauseTimer : TON;
    CycleActive : BOOL := FALSE;
    MinimumBlowerSpeed : REAL := 20.0;
    MaximumBlowerSpeed : REAL := 95.0;
    BlowerStartupSequence : BOOL := FALSE;
    BlowerStartupTimer : TON;
    BlowerStartupStage : INT := 0;
    BlowerShutdownSequence : BOOL := FALSE;
    BlowerShutdownTimer : TON;
    PreviousDO : REAL := 0.0;
    DOChangeRate : REAL := 0.0;
    DOCalculationTimer : TON;
    AnoxicCycleRequired : BOOL := FALSE;
END_VAR

(* Aeration System Controller *)
(* Manages the aeration blowers and dissolved oxygen control *)

(* Only run when system is operational *)
IF SystemRunning AND SystemState < 4 THEN

    (* Calculate DO change rate every 2 minutes *)
    DOCalculationTimer(IN := TRUE, PT := T#2M);
    IF DOCalculationTimer.Q THEN
        DOChangeRate := (ScaledDO - PreviousDO) / 120.0; (* mg/L per second *)
        PreviousDO := ScaledDO;
        DOCalculationTimer(IN := FALSE);
        DOCalculationTimer(IN := TRUE, PT := T#2M);
    END_IF
    
    (* Check if anoxic cycle is required for nutrient removal *)
    AnoxicCycleRequired := FALSE; (* In real system, this would be based on ammonia and nitrate measurements *)
    
    (* Dissolved Oxygen Control *)
    IF OperatingMode = 1 AND NOT MaintenanceRequired THEN
        (* Configure DO PID controller *)
        DOPIDParams.Kp := 10.0;   (* Proportional gain *)
        DOPIDParams.Ki := 0.1;    (* Integral gain *)
        DOPIDParams.Kd := 1.0;    (* Derivative gain *)
        DOPIDParams.Deadband := 0.1; (* Deadband to prevent oscillations *)
        DOPIDParams.MaxOutput := MaximumBlowerSpeed; (* Output range *)
        DOPIDParams.MinOutput := MinimumBlowerSpeed;
        
        (* Execute DO PID control *)
        DOController.Parameters := DOPIDParams;
        DOController.Setpoint := DissolvedOxygenSetpoint;
        DOController.ProcessValue := ScaledDO;
        DOController.Execute();
        DOControlOutput := DOController.Output;
        
        (* Aeration Control Strategy - Cycle as needed *)
        CASE AerationCycle OF
            0: (* Normal aeration phase *)
                IF NOT AnoxicCycleRequired THEN
                    (* Continuous aeration based on DO control *)
                    BlowerSpeedOutput := DOControlOutput;
                    
                    (* Ensure the blower runs at a reasonable speed *)
                    IF BlowerSpeedOutput < MinimumBlowerSpeed THEN
                        IF ScaledDO < (DissolvedOxygenSetpoint * 1.5) THEN
                            BlowerSpeedOutput := MinimumBlowerSpeed;
                        END_IF
                    END_IF
                    
                    (* Stay in continuous mode *)
                    CycleActive := FALSE;
                ELSE
                    (* Begin cycle operation with aeration phase *)
                    AerationTimer(IN := TRUE, PT := T#30M);
                    CycleActive := TRUE;
                    
                    (* Run blower at calculated speed *)
                    BlowerSpeedOutput := DOControlOutput;
                    
                    (* Move to anoxic phase after timer expires *)
                    IF AerationTimer.Q THEN
                        AerationCycle := 1;
                        AerationTimer(IN := FALSE);
                        AerationPauseTimer(IN := FALSE);
                    END_IF
                END_IF
                
            1: (* Anoxic phase - blower off for denitrification *)
                BlowerSpeedOutput := 0.0;
                AerationPauseTimer(IN := TRUE, PT := T#45M);
                
                (* Emergency override - if DO drops too low, restart aeration *)
                IF ScaledDO < (MIN_DO * 0.5) THEN
                    AerationCycle := 0;
                    AerationPauseTimer(IN := FALSE);
                END_IF
                
                (* Return to aeration phase after timer expires *)
                IF AerationPauseTimer.Q THEN
                    AerationCycle := 0;
                    AerationPauseTimer(IN := FALSE);
                END_IF
        END_CASE
        
        (* Blower Startup Sequence *)
        IF BlowerSpeedOutput > 0.0 AND NOT BLOWER_START THEN
            (* Initialize startup sequence *)
            BlowerStartupSequence := TRUE;
            BlowerShutdownSequence := FALSE;
            BlowerStartupStage := 0;
            BlowerStartupTimer(IN := FALSE);
        END_IF
        
        (* Blower Shutdown Sequence *)
        IF BlowerSpeedOutput = 0.0 AND BLOWER_START THEN
            (* Initialize shutdown sequence *)
            BlowerShutdownSequence := TRUE;
            BlowerStartupSequence := FALSE;
            BlowerShutdownTimer(IN := FALSE);
        END_IF
        
        (* Execute Blower Startup Sequence *)
        IF BlowerStartupSequence THEN
            CASE BlowerStartupStage OF
                0: (* Pre-start checks *)
                    BLOWER_START := FALSE;
                    BLOWER_SPEED := 0;
                    BlowerStartupTimer(IN := TRUE, PT := T#5S);
                    IF BlowerStartupTimer.Q THEN
                        BlowerStartupStage := 1;
                        BlowerStartupTimer(IN := FALSE);
                    END_IF
                    
                1: (* Start motor *)
                    BLOWER_START := TRUE;
                    BLOWER_SPEED := REAL_TO_INT(MinimumBlowerSpeed * 27648.0 / 100.0);
                    BlowerStartupTimer(IN := TRUE, PT := T#10S);
                    IF BlowerStartupTimer.Q THEN
                        BlowerStartupStage := 2;
                        BlowerStartupTimer(IN := FALSE);
                    END_IF
                    
                2: (* Ramp up to target speed *)
                    BLOWER_SPEED := REAL_TO_INT(BlowerSpeedOutput * 27648.0 / 100.0);
                    BlowerStartupSequence := FALSE;
            END_CASE
        END_IF
        
        (* Execute Blower Shutdown Sequence *)
        IF BlowerShutdownSequence THEN
            (* Ramp down speed first *)
            BLOWER_SPEED := REAL_TO_INT(MinimumBlowerSpeed * 27648.0 / 100.0);
            BlowerShutdownTimer(IN := TRUE, PT := T#15S);
            
            IF BlowerShutdownTimer.Q THEN
                (* Safe to stop motor *)
                BLOWER_START := FALSE;
                BLOWER_SPEED := 0;
                BlowerShutdownSequence := FALSE;
                BlowerShutdownTimer(IN := FALSE);
            END_IF
        END_IF
        
        (* Update blower speed if running and not in startup/shutdown sequence *)
        IF BLOWER_START AND NOT BlowerStartupSequence AND NOT BlowerShutdownSequence THEN
            (* Smooth out rapid DO changes to prevent blower hunting *)
            IF ABS(DOChangeRate) > 0.005 THEN
                (* DO changing quickly - apply more gradual change to blower speed *)
                BlowerSpeedOutput := 0.7 * BlowerSpeedOutput + 0.3 * REAL_TO_INT(BLOWER_SPEED) * 100.0 / 27648.0;
            END_IF
            
            (* Apply control output to blower *)
            BLOWER_SPEED := REAL_TO_INT(BlowerSpeedOutput * 27648.0 / 100.0);
        END_IF
    
    ELSIF OperatingMode = 2 THEN
        (* Storm mode - maximum aeration capacity *)
        BLOWER_START := TRUE;
        BLOWER_SPEED := REAL_TO_INT(MaximumBlowerSpeed * 27648.0 / 100.0);
        
    ELSIF OperatingMode = 3 THEN
        (* Maintenance mode - manually controlled from HMI *)
        (* Keep current state - will be controlled by direct PLC writes *)
    ELSE
        (* System stopped or fault - ensure blower is off *)
        BLOWER_START := FALSE;
        BLOWER_SPEED := 0;
    END_IF
    
END_IF

END_PROGRAM
