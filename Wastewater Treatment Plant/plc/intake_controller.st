PROGRAM intake_controller
VAR
    ScreenCleaningTimer : TON;
    ScreenCleaningActive : BOOL := FALSE;
    ScreenCleaningCycle : INT := 0;
    IntakeValvePosition : INT := 0;
    FlowSetpoint : REAL := 300.0; (* Default flow setpoint *)
    FlowPIDParams : PID_PARAMS;
    ScreeningActive : BOOL := FALSE;
    FlowControl : PID;
    FlowControlOutput : REAL;
    ManualOverrideActive : BOOL := FALSE;
    ScreenClogDetected : BOOL := FALSE;
    PreviousScreenClog : BOOL := FALSE;
END_VAR

(* Intake Process Controller *)
(* Manages the initial wastewater intake, screening, and flow control *)

(* Only run when system is operational *)
IF SystemRunning AND SystemState < 4 THEN

    (* Screen Clog Detection *)
    ScreenClogDetected := SCREEN_CLOG;
    IF ScreenClogDetected AND NOT PreviousScreenClog THEN
        (* New clog detected - start cleaning cycle *)
        ScreenCleaningTimer(IN := FALSE);
        ScreenCleaningActive := TRUE;
        ScreenCleaningCycle := 0;
    END_IF
    PreviousScreenClog := ScreenClogDetected;
    
    (* Screening System Control *)
    IF ScreenCleaningActive THEN
        (* Screen Cleaning Sequence *)
        CASE ScreenCleaningCycle OF
            0: (* Forward motion *)
                SCREEN_FORWARD := TRUE;
                SCREEN_REVERSE := FALSE;
                ScreenCleaningTimer(IN := TRUE, PT := T#30S);
                IF ScreenCleaningTimer.Q THEN
                    ScreenCleaningTimer(IN := FALSE);
                    ScreenCleaningCycle := 1;
                END_IF
                
            1: (* Stop briefly *)
                SCREEN_FORWARD := FALSE;
                SCREEN_REVERSE := FALSE;
                ScreenCleaningTimer(IN := TRUE, PT := T#5S);
                IF ScreenCleaningTimer.Q THEN
                    ScreenCleaningTimer(IN := FALSE);
                    ScreenCleaningCycle := 2;
                END_IF
                
            2: (* Reverse motion *)
                SCREEN_FORWARD := FALSE;
                SCREEN_REVERSE := TRUE;
                ScreenCleaningTimer(IN := TRUE, PT := T#20S);
                IF ScreenCleaningTimer.Q THEN
                    ScreenCleaningTimer(IN := FALSE);
                    ScreenCleaningCycle := 3;
                END_IF
                
            3: (* Complete cycle *)
                SCREEN_FORWARD := FALSE;
                SCREEN_REVERSE := FALSE;
                ScreenCleaningActive := FALSE;
        END_CASE
    ELSIF OperatingMode = 1 THEN
        (* Normal screening operation *)
        (* Run screen periodically with timer based on flow rate *)
        IF ScaledFlowRate > 100.0 THEN
            SCREEN_FORWARD := TRUE;
            SCREEN_REVERSE := FALSE;
            ScreeningActive := TRUE;
        ELSE
            IF ScreeningActive THEN
                ScreenCleaningTimer(IN := TRUE, PT := T#60S);
                IF ScreenCleaningTimer.Q THEN
                    SCREEN_FORWARD := FALSE;
                    SCREEN_REVERSE := FALSE;
                    ScreeningActive := FALSE;
                    ScreenCleaningTimer(IN := FALSE);
                END_IF
            END_IF
        END_IF
    ELSE
        (* Maintenance mode or storm mode - manual control from HMI *)
        (* Keep current state - will be controlled directly by Q variables *)
    END_IF
    
    (* Flow Control *)
    IF OperatingMode = 1 AND NOT ManualOverrideActive THEN
        (* Auto mode flow control *)
        (* Set flow rate based on current system capacity *)
        IF SystemState = 1 THEN
            (* Normal operation *)
            FlowSetpoint := FlowRateSetpoint; (* From global setpoint *)
        ELSIF SystemState = 2 THEN
            (* Warning state - reduce flow *)
            FlowSetpoint := FlowRateSetpoint * 0.8;
        ELSIF SystemState = 3 THEN
            (* Alarm state - further reduce flow *)
            FlowSetpoint := FlowRateSetpoint * 0.5;
        END_IF
        
        (* Scale back if tanks are getting too full *)
        IF ScaledTankLevel1 > (MAX_TANK_LEVEL * 0.9) THEN
            FlowSetpoint := FlowSetpoint * 0.7;
        END_IF
        
        (* Storm mode override *)
        IF OperatingMode = 2 THEN
            FlowSetpoint := MAX_FLOW_RATE * 0.9; (* Near maximum capacity *)
        END_IF
        
        (* Configure PID controller *)
        FlowPIDParams.Kp := 2.0;   (* Proportional gain *)
        FlowPIDParams.Ki := 0.1;   (* Integral gain *)
        FlowPIDParams.Kd := 0.05;  (* Derivative gain *)
        FlowPIDParams.Deadband := 5.0; (* Deadband to prevent oscillations *)
        FlowPIDParams.MaxOutput := 100.0; (* 0-100% output range *)
        FlowPIDParams.MinOutput := 0.0;
        
        (* Execute PID control *)
        FlowControl.Parameters := FlowPIDParams;
        FlowControl.Setpoint := FlowSetpoint;
        FlowControl.ProcessValue := ScaledFlowRate;
        FlowControl.Execute();
        FlowControlOutput := FlowControl.Output;
        
        (* Apply control output to pump *)
        IF INTAKE_FLOW OR ScaledFlowRate < 10.0 THEN
            PUMP_P101_START := TRUE;
            PUMP_P101_SPEED := REAL_TO_INT(FlowControlOutput * 27648.0 / 100.0);
        ELSE
            (* No flow detected at input - stop pump *)
            PUMP_P101_START := FALSE;
            PUMP_P101_SPEED := 0;
        END_IF
    ELSIF OperatingMode = 3 THEN
        (* Maintenance mode - commands from HMI *)
        (* Keep last state - will be controlled by direct PLC writes *)
    END_IF
    
    (* Valve control based on tank levels *)
    IF ScaledTankLevel1 > MAX_TANK_LEVEL * 0.95 THEN
        (* Close inlet valve to prevent overflow *)
        IntakeValvePosition := 0;
    ELSIF ScaledFlowRate < 20.0 AND PUMP_P101_START THEN
        (* Possible blockage or dry run - reduce valve opening *)
        IntakeValvePosition := 3000; (* ~10% *)
    ELSE
        (* Normal operation - valve position follows flow demand *)
        IntakeValvePosition := 8000 + REAL_TO_INT(FlowControlOutput * 19000.0 / 100.0);
    END_IF
END_IF

END_PROGRAM
