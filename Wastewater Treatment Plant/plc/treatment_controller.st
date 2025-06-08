PROGRAM treatment_controller
VAR
    MixerControlTimer : TON;
    MixerPulseActive : BOOL := FALSE;
    SettlingPhaseActive : BOOL := FALSE;
    SettlingTimer : TON;
    TankTransferActive : BOOL := FALSE;
    TransferTimer : TON;
    PrimaryTreatmentCycle : INT := 0;
    SecondaryValvePosition : INT := 0;
    MixingIntensity : REAL := 70.0;
    PreviousTankLevel1 : REAL := 0.0;
    TankLevelDelta : REAL := 0.0;
    TankLevelRateOfChange : REAL := 0.0;
    RateCalculationTimer : TON;
    FilterOperationTimer : TON;
    FilterBackwashNeeded : BOOL := FALSE;
END_VAR

(* Treatment Process Controller *)
(* Manages the primary and secondary treatment processes *)

(* Only run when system is operational *)
IF SystemRunning AND SystemState < 4 THEN

    (* Calculate tank level rate of change every 5 minutes *)
    RateCalculationTimer(IN := TRUE, PT := T#5M);
    IF RateCalculationTimer.Q THEN
        TankLevelDelta := ScaledTankLevel1 - PreviousTankLevel1;
        TankLevelRateOfChange := TankLevelDelta / 300.0; (* m per second *)
        PreviousTankLevel1 := ScaledTankLevel1;
        RateCalculationTimer(IN := FALSE);
        RateCalculationTimer(IN := TRUE, PT := T#5M);
    END_IF
    
    (* Primary Treatment Processes *)
    CASE PrimaryTreatmentCycle OF
        0: (* Filling phase - already handled by intake controller *)
            IF ScaledTankLevel1 >= (MAX_TANK_LEVEL * 0.6) THEN
                PrimaryTreatmentCycle := 1;
                MixerControlTimer(IN := FALSE);
            END_IF
            
        1: (* Mixing phase *)
            (* Start mixer for primary tank *)
            MIXER_M101_START := TRUE;
            
            (* Apply variable mixing intensity based on tank level *)
            MixingIntensity := 50.0 + (ScaledTankLevel1 / MAX_TANK_LEVEL) * 50.0;
            MIXER_M101_SPEED := REAL_TO_INT(MixingIntensity * 27648.0 / 100.0);
            
            (* Run mixing for determined time *)
            MixerControlTimer(IN := TRUE, PT := T#20M);
            IF MixerControlTimer.Q THEN
                PrimaryTreatmentCycle := 2;
                MixerControlTimer(IN := FALSE);
                SettlingTimer(IN := FALSE);
            END_IF
            
        2: (* Settling phase *)
            (* Stop mixer to allow settling *)
            MIXER_M101_START := FALSE;
            MIXER_M101_SPEED := 0;
            SettlingPhaseActive := TRUE;
            
            (* Allow suspended solids to settle *)
            SettlingTimer(IN := TRUE, PT := T#45M);
            IF SettlingTimer.Q THEN
                PrimaryTreatmentCycle := 3;
                SettlingTimer(IN := FALSE);
                TransferTimer(IN := FALSE);
            END_IF
            
        3: (* Transfer to secondary treatment *)
            (* Activate transfer pump *)
            PUMP_P102_START := TRUE;
            PUMP_P102_SPEED := 13824; (* 50% speed *)
            TankTransferActive := TRUE;
            
            (* Transfer for specified time or until level drops *)
            TransferTimer(IN := TRUE, PT := T#30M);
            IF TransferTimer.Q OR ScaledTankLevel1 < (MAX_TANK_LEVEL * 0.15) THEN
                PrimaryTreatmentCycle := 0;
                PUMP_P102_START := FALSE;
                PUMP_P102_SPEED := 0;
                TransferTimer(IN := FALSE);
                TankTransferActive := FALSE;
            END_IF
    END_CASE
    
    (* Secondary Treatment Tank Control *)
    IF ScaledTankLevel2 > (MAX_TANK_LEVEL * 0.3) THEN
        (* Start secondary mixing when tank has sufficient level *)
        MIXER_M102_START := TRUE;
        MIXER_M102_SPEED := REAL_TO_INT(60.0 * 27648.0 / 100.0); (* 60% speed *)
    ELSE
        (* Tank too empty for effective mixing *)
        MIXER_M102_START := FALSE;
        MIXER_M102_SPEED := 0;
    END_IF
    
    (* Control outlet valve position based on treatment status *)
    IF ScaledTankLevel2 > (MAX_TANK_LEVEL * 0.5) AND 
       ScaledPHValue >= MIN_PH AND ScaledPHValue <= MAX_PH AND
       ScaledTurbidity < MAX_TURBIDITY * 0.8 THEN
        (* Conditions good for discharge *)
        OUTLET_VALVE := TRUE;
    ELSE
        (* Close outlet if conditions not suitable *)
        OUTLET_VALVE := FALSE;
    END_IF
    
    (* Filter Operation Control *)
    IF NOT FILTER_PRESSURE_HIGH THEN
        (* Normal filter operation *)
        FilterOperationTimer(IN := TRUE, PT := T#8H);
        IF FilterOperationTimer.Q THEN
            (* Time for scheduled backwash *)
            FilterBackwashNeeded := TRUE;
            FilterOperationTimer(IN := FALSE);
        END_IF
    ELSE
        (* High pressure difference - needs immediate backwash *)
        FilterBackwashNeeded := TRUE;
    END_IF
    
    (* Filter Backwash Sequence *)
    IF FilterBackwashNeeded THEN
        (* Close outlet valve during backwash *)
        OUTLET_VALVE := FALSE;
        
        (* Activate backwash valve *)
        BACKWASH_VALVE := TRUE;
        
        (* Run backwash cycle *)
        BackwashTimer(IN := TRUE, PT := T#5M);
        IF BackwashTimer.Q THEN
            BACKWASH_VALVE := FALSE;
            FilterBackwashNeeded := FALSE;
            BackwashTimer(IN := FALSE);
            (* Restart filter operation timer *)
            FilterOperationTimer(IN := TRUE, PT := T#8H);
        END_IF
    END_IF
    
    (* UV System Control - final disinfection *)
    IF OUTLET_VALVE AND ScaledFlowRate > 20.0 THEN
        (* Activate UV when discharging *)
        UV_SYSTEM_START := TRUE;
    ELSE
        (* Turn off UV when not discharging to save energy *)
        UV_SYSTEM_START := FALSE;
    END_IF
    
END_IF

END_PROGRAM
