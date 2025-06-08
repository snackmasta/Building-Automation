PROGRAM monitoring_controller
VAR
    MonitoringCycleTimer : TON;
    DataLogTimer : TON;
    SampleCollectionTimer : TON;
    SampleInterval : TIME := T#4H;
    LastSampleTime : TIME;
    SampleNeeded : BOOL := FALSE;
    ComplianceCheckTimer : TON;
    ComplianceStatus : BOOL := TRUE;
    OutOfSpecCount : INT := 0;
    AlarmHistoryIndex : INT := 0;
    AlarmHistoryTime : ARRAY[0..9] OF TIME;
    AlarmHistoryCode : ARRAY[0..9] OF INT;
    LimitsExceeded : BOOL := FALSE;
    WaterQualityStatus : INT := 0; (* 0=Good, 1=Marginal, 2=Poor *)
    FirstScan : BOOL := TRUE;
    ParameterCheckCycle : INT := 0;
END_VAR

(* Monitoring and Reporting Controller *)
(* Handles monitoring, data logging, and compliance reporting *)

(* Initialize data structures on first scan *)
IF FirstScan THEN
    ComplianceStatus := TRUE;
    OutOfSpecCount := 0;
    ParameterCheckCycle := 0;
    FirstScan := FALSE;
END_IF

(* Run monitoring even when system is not in automatic mode *)
(* This ensures critical parameters are always monitored *)

(* Cyclic monitoring of parameters *)
MonitoringCycleTimer(IN := TRUE, PT := T#10S);
IF MonitoringCycleTimer.Q THEN
    (* Reset timer for next cycle *)
    MonitoringCycleTimer(IN := FALSE);
    MonitoringCycleTimer(IN := TRUE, PT := T#10S);
    
    (* Cycle through parameter checks to distribute processing *)
    CASE ParameterCheckCycle OF
        0: (* pH monitoring *)
            (* Check pH is within limits *)
            IF ScaledPHValue < MIN_PH OR ScaledPHValue > MAX_PH THEN
                IF NOT (HighPHAlarm OR LowPHAlarm) THEN
                    (* New pH alarm - log it *)
                    LogAlarm(10); (* Code 10 = pH out of range *)
                END_IF
            END_IF
            ParameterCheckCycle := 1;
            
        1: (* Dissolved oxygen monitoring *)
            (* Check DO level *)
            IF ScaledDO < MIN_DO AND BatchProcessing THEN
                IF NOT LowOxygenAlarm THEN
                    (* New DO alarm - log it *)
                    LogAlarm(20); (* Code 20 = Low oxygen *)
                END_IF
            END_IF
            ParameterCheckCycle := 2;
            
        2: (* Turbidity monitoring *)
            (* Check turbidity *)
            IF ScaledTurbidity > MAX_TURBIDITY THEN
                IF NOT HighTurbidityAlarm THEN
                    (* New turbidity alarm - log it *)
                    LogAlarm(30); (* Code 30 = High turbidity *)
                END_IF
                
                (* Adjust water quality status *)
                WaterQualityStatus := 2; (* Poor *)
            ELSIF ScaledTurbidity > (MAX_TURBIDITY * 0.7) THEN
                (* Marginal water quality *)
                WaterQualityStatus := 1; (* Marginal *)
            ELSE
                (* Good water quality *)
                WaterQualityStatus := 0; (* Good *)
            END_IF
            ParameterCheckCycle := 3;
            
        3: (* Gas detection *)
            IF GAS_ALARM AND NOT GasDetectionAlarm THEN
                (* New gas alarm - log it *)
                LogAlarm(40); (* Code 40 = Dangerous gas detected *)
            END_IF
            ParameterCheckCycle := 4;
            
        4: (* Flow monitoring *)
            (* Check for abnormal flow conditions *)
            IF PUMP_P101_RUNNING AND ScaledFlowRate < 10.0 THEN
                (* Pump running but no flow - potential blockage *)
                LogAlarm(50); (* Code 50 = Flow anomaly *)
            END_IF
            ParameterCheckCycle := 5;
            
        5: (* System status *)
            (* Check overall system status *)
            IF SystemState = 3 THEN
                (* System in alarm state *)
                ComplianceStatus := FALSE;
                OutOfSpecCount := OutOfSpecCount + 1;
            ELSIF SystemState = 1 AND OutOfSpecCount > 0 THEN
                (* System back to normal - decrement counter *)
                OutOfSpecCount := OutOfSpecCount - 1;
                IF OutOfSpecCount = 0 THEN
                    ComplianceStatus := TRUE;
                END_IF
            END_IF
            ParameterCheckCycle := 0; (* Restart cycle *)
    END_CASE
END_IF

(* Data Logging Functionality *)
DataLogTimer(IN := TRUE, PT := T#15M);
IF DataLogTimer.Q THEN
    (* Time to log process data *)
    DataLogTimer(IN := FALSE);
    DataLogTimer(IN := TRUE, PT := T#15M);
    
    (* Log key process parameters - these would typically be stored
       in a database or data historian. Here we just set a flag. *)
    LogProcessData();
END_IF

(* Sample Collection Scheduling *)
SampleCollectionTimer(IN := TRUE, PT := SampleInterval);
IF SampleCollectionTimer.Q THEN
    (* Time for routine sample *)
    SampleNeeded := TRUE;
    LastSampleTime := 0; (* Would be current time in real system *)
    SampleCollectionTimer(IN := FALSE);
    SampleCollectionTimer(IN := TRUE, PT := SampleInterval);
END_IF

(* Compliance Checking *)
ComplianceCheckTimer(IN := TRUE, PT := T#1H);
IF ComplianceCheckTimer.Q THEN
    (* Hourly compliance check *)
    ComplianceCheckTimer(IN := FALSE);
    ComplianceCheckTimer(IN := TRUE, PT := T#1H);
    
    (* Check discharge parameters against regulatory limits *)
    IF OUTLET_VALVE AND (
       ScaledTurbidity > MAX_TURBIDITY OR
       ScaledPHValue < MIN_PH OR 
       ScaledPHValue > MAX_PH OR
       ScaledChlorineResidual > 10.0) THEN
        (* Parameters outside regulatory limits *)
        LimitsExceeded := TRUE;
        
        (* Log compliance issue *)
        LogAlarm(100); (* Code 100 = Compliance violation *)
        
        (* In a real system, this would trigger automated reporting
           to operators and potentially regulatory agencies *)
    ELSE
        LimitsExceeded := FALSE;
    END_IF
END_IF

(* Maintenance Requirements Check *)
(* Based on runtime or specific conditions *)
MaintenanceCounter();
IF MaintenanceCounter.CV > 720 THEN (* 720 hours = 30 days *)
    (* Monthly maintenance check *)
    MaintenanceRequired := TRUE;
    
    (* This would typically trigger work orders or maintenance alarms *)
END_IF

(* Performance Metrics Calculation *)
(* Calculate efficiency metrics based on inlet and outlet measurements *)
IF ScaledFlowRate > 10.0 AND OUTPUT_FLOW_RATE > 0 THEN
    (* Basic efficiency calculation based on turbidity reduction *)
    (* In a real system this would include multiple parameters *)
    TreatmentEfficiency := 100.0 * (1.0 - (ScaledTurbidity / 1000.0));
END_IF

(* Define the alarm logging function *)
FUNCTION LogAlarm : VOID
VAR_INPUT
    AlarmCode : INT;
END_VAR
    (* Store alarm in history array *)
    AlarmHistoryCode[AlarmHistoryIndex] := AlarmCode;
    (* In a real system, we would store the current time *)
    AlarmHistoryIndex := (AlarmHistoryIndex + 1) MOD 10;
END_FUNCTION

(* Define the data logging function *)
FUNCTION LogProcessData : VOID
    (* In a real system, this would write to a database or data historian *)
    (* For this example, we're just creating a placeholder function *)
END_FUNCTION

END_PROGRAM
