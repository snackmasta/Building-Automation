FUNCTION_BLOCK ElevatorController
VAR_INPUT
    ElevatorNumber : INT;               // Elevator number (1, 2, or 3)
    TargetLevel : INT;                  // Target level (1-15)
    Execute : BOOL;                     // Execute movement command
    Stop : BOOL;                        // Emergency stop
    Reset : BOOL;                       // Reset elevator
    ManualMode : BOOL;                  // Manual operation mode
    ManualDirection : BOOL;             // Manual direction (TRUE=up, FALSE=down)
    ManualSpeed : REAL;                 // Manual speed reference
END_VAR

VAR_OUTPUT
    Done : BOOL;                        // Movement completed
    Busy : BOOL;                        // Movement in progress
    Error : BOOL;                       // Error condition
    ErrorID : INT;                      // Error identification code
    CurrentLevel : INT;                 // Current elevator level
    CurrentPosition : REAL;             // Current position (mm)
    AtLevel : BOOL;                     // At target level
    DoorOpen : BOOL;                    // Door open status
    Available : BOOL;                   // Elevator available for use
    LoadWeight : REAL;                  // Current load weight
    MotorSpeed : REAL;                  // Current motor speed
END_VAR

VAR
    // Control state machine
    state : INT := 0;
    previousState : INT;
    stateTimer : TON;
    movementTimer : TON;
    
    // Position and motion control
    currentPos : REAL;                  // Current position in mm
    targetPos : REAL;                   // Target position in mm
    homePosition : REAL := 0.0;         // Ground level position
    levelHeight : REAL := 3000.0;       // Height per level (mm)
    positionTolerance : REAL := 20.0;   // Position tolerance (mm)
    
    // Motion parameters
    maxSpeed : REAL := 2500.0;          // Maximum speed (mm/s)
    acceleration : REAL := 500.0;       // Acceleration (mm/s²)
    deceleration : REAL := 750.0;       // Deceleration (mm/s²)
    currentSpeed : REAL := 0.0;         // Current speed
    targetSpeed : REAL := 0.0;          // Target speed
    
    // Safety and monitoring
    safetyOK : BOOL := TRUE;
    overloadDetected : BOOL := FALSE;
    doorInterlockOK : BOOL := TRUE;
    emergencyStopActive : BOOL := FALSE;
    
    // Door control
    doorState : INT := 0;               // 0=closed, 1=opening, 2=open, 3=closing
    doorTimer : TON;
    doorTimeout : TIME := T#10s;
    
    // Maintenance and diagnostics
    totalOperationTime : TIME;
    totalDistance : REAL := 0.0;
    cycleCount : DINT := 0;
    lastMaintenanceDistance : REAL := 0.0;
    maintenanceRequired : BOOL := FALSE;
    
    // Error handling
    errorHistory : ARRAY[1..10] OF INT;
    errorIndex : INT := 1;
    retryCount : INT := 0;
    maxRetries : INT := 3;
    
    // Performance monitoring
    averageSpeed : REAL;
    lastMovementTime : TIME;
    efficiency : REAL := 100.0;
    
END_VAR

// Input validation
IF ElevatorNumber < 1 OR ElevatorNumber > 3 THEN
    Error := TRUE;
    ErrorID := 5001; // Invalid elevator number
    Available := FALSE;
    RETURN;
END_IF;

IF TargetLevel < 1 OR TargetLevel > MAX_PARKING_LEVELS THEN
    Error := TRUE;
    ErrorID := 5002; // Invalid target level
    RETURN;
END_IF;

// Get current position based on elevator number
CASE ElevatorNumber OF
    1: currentPos := SCALE_INT_TO_REAL(AI_Elevator1_Position, 0.0, 45000.0);
    2: currentPos := SCALE_INT_TO_REAL(AI_Elevator2_Position, 0.0, 45000.0);
    3: currentPos := SCALE_INT_TO_REAL(AI_Elevator3_Position, 0.0, 45000.0);
END_CASE;

CurrentPosition := currentPos;
LoadWeight := SCALE_INT_TO_REAL(AI_LoadCell_PlatformWeight, 0.0, 5000.0);

// Calculate current level
CurrentLevel := REAL_TO_INT((currentPos / levelHeight) + 1);
IF CurrentLevel < 1 THEN CurrentLevel := 1; END_IF;
IF CurrentLevel > MAX_PARKING_LEVELS THEN CurrentLevel := MAX_PARKING_LEVELS; END_IF;

// Safety checks
safetyOK := NOT I_EmergencyStop_Main AND 
            NOT I_EmergencyStop_Level1 AND 
            NOT I_EmergencyStop_Level2 AND
            I_HydraulicSystem_PressureOK AND
            I_UPS_BatteryOK;

overloadDetected := LoadWeight > 4000.0; // 4000kg limit
doorInterlockOK := I_DoorInterlocks_AllClosed;
emergencyStopActive := Stop OR NOT safetyOK;

// Emergency stop handling
IF emergencyStopActive THEN
    state := 90; // Emergency stop state
    targetSpeed := 0.0;
    Error := TRUE;
    ErrorID := 5010;
END_IF;

// Reset handling
IF Reset AND state = 90 THEN
    state := 0; // Reset to idle
    Error := FALSE;
    ErrorID := 0;
    retryCount := 0;
END_IF;

// Calculate target position
targetPos := (TargetLevel - 1) * levelHeight;

// Check if at target level
AtLevel := ABS(currentPos - targetPos) <= positionTolerance;

// Execute movement command
IF Execute AND NOT Busy AND state = 0 AND safetyOK THEN
    IF NOT AtLevel THEN
        Busy := TRUE;
        Done := FALSE;
        state := 10; // Start movement
        movementTimer(IN := TRUE, PT := T#0s);
        cycleCount := cycleCount + 1;
    ELSE
        Done := TRUE; // Already at target
    END_IF;
END_IF;

// Manual mode handling
IF ManualMode AND state = 0 AND safetyOK THEN
    state := 80; // Manual mode
    Busy := TRUE;
END_IF;

// Main state machine
CASE state OF
    
    0: // IDLE
        Busy := FALSE;
        Available := TRUE AND safetyOK AND NOT maintenanceRequired;
        targetSpeed := 0.0;
        
        // Check for maintenance requirements
        IF (totalDistance - lastMaintenanceDistance) > 100000000.0 THEN // 100km
            maintenanceRequired := TRUE;
            Available := FALSE;
        END_IF;
    
    // =============================================================================
    // MOVEMENT SEQUENCE (States 10-49)
    // =============================================================================
    
    10: // PREPARE_FOR_MOVEMENT
        Available := FALSE;
        
        // Ensure doors are closed
        IF NOT doorInterlockOK THEN
            state := 11; // Close doors first
        ELSE
            state := 12; // Doors already closed
        END_IF;
    
    11: // CLOSE_DOORS
        doorState := 3; // Closing
        doorTimer(IN := TRUE, PT := doorTimeout);
        
        IF doorInterlockOK THEN
            doorState := 0; // Closed
            state := 12;
            doorTimer(IN := FALSE);
        ELSIF doorTimer.Q THEN
            Error := TRUE;
            ErrorID := 5011; // Door close timeout
            state := 91;
            doorTimer(IN := FALSE);
        END_IF;
    
    12: // START_MOVEMENT
        // Enable motor based on elevator number
        CASE ElevatorNumber OF
            1: Q_Elevator1_Enable := TRUE;
            2: Q_Elevator2_Enable := TRUE;
            3: Q_Elevator3_Enable := TRUE;
        END_CASE;
        
        // Determine direction
        IF targetPos > currentPos THEN
            // Moving up
            CASE ElevatorNumber OF
                1: Q_Elevator1_Direction := TRUE;
                2: Q_Elevator2_Direction := TRUE;
                3: Q_Elevator3_Direction := TRUE;
            END_CASE;
        ELSE
            // Moving down
            CASE ElevatorNumber OF
                1: Q_Elevator1_Direction := FALSE;
                2: Q_Elevator2_Direction := FALSE;
                3: Q_Elevator3_Direction := FALSE;
            END_CASE;
        END_IF;
        
        state := 13; // Accelerate
    
    13: // ACCELERATE
        // Calculate required speed
        IF ABS(targetPos - currentPos) > 1000.0 THEN
            targetSpeed := maxSpeed; // Full speed for long distances
        ELSE
            targetSpeed := maxSpeed * 0.5; // Half speed for short distances
        END_IF;
        
        // Accelerate to target speed
        IF currentSpeed < targetSpeed THEN
            currentSpeed := currentSpeed + (acceleration * 0.1); // 100ms cycle
            IF currentSpeed > targetSpeed THEN
                currentSpeed := targetSpeed;
            END_IF;
        END_IF;
        
        // Check if close to target for deceleration
        IF ABS(targetPos - currentPos) <= (currentSpeed * currentSpeed) / (2.0 * deceleration) THEN
            state := 14; // Start deceleration
        END_IF;
        
        // Safety check during movement
        IF NOT safetyOK OR overloadDetected THEN
            state := 90; // Emergency stop
        END_IF;
    
    14: // DECELERATE
        // Calculate deceleration distance
        targetSpeed := SQRT(2.0 * deceleration * ABS(targetPos - currentPos));
        
        IF targetSpeed < 100.0 THEN
            targetSpeed := 100.0; // Minimum speed for positioning
        END_IF;
        
        // Decelerate
        IF currentSpeed > targetSpeed THEN
            currentSpeed := currentSpeed - (deceleration * 0.1);
            IF currentSpeed < targetSpeed THEN
                currentSpeed := targetSpeed;
            END_IF;
        END_IF;
        
        // Check if at target position
        IF ABS(targetPos - currentPos) <= positionTolerance THEN
            state := 15; // Stop
        END_IF;
        
        // Timeout check
        IF movementTimer.ET > T#300s THEN
            Error := TRUE;
            ErrorID := 5012; // Movement timeout
            state := 91;
        END_IF;
    
    15: // STOP_AT_TARGET
        targetSpeed := 0.0;
        currentSpeed := 0.0;
        
        // Stop motor
        CASE ElevatorNumber OF
            1: Q_Elevator1_Enable := FALSE;
            2: Q_Elevator2_Enable := FALSE;
            3: Q_Elevator3_Enable := FALSE;
        END_CASE;
        
        stateTimer(IN := TRUE, PT := T#2s);
        
        IF stateTimer.Q THEN
            state := 16; // Final positioning
            stateTimer(IN := FALSE);
        END_IF;
    
    16: // FINE_POSITIONING
        // Fine positioning at very low speed
        IF ABS(targetPos - currentPos) > 5.0 THEN
            CASE ElevatorNumber OF
                1: Q_Elevator1_Enable := TRUE;
                2: Q_Elevator2_Enable := TRUE;
                3: Q_Elevator3_Enable := TRUE;
            END_CASE;
            
            currentSpeed := 50.0; // Very slow speed
            targetSpeed := 50.0;
        ELSE
            state := 17; // Positioning complete
        END_IF;
        
        stateTimer(IN := TRUE, PT := T#30s);
        IF stateTimer.Q THEN
            state := 17; // Timeout - accept current position
            stateTimer(IN := FALSE);
        END_IF;
    
    17: // POSITIONING_COMPLETE
        // Final stop
        targetSpeed := 0.0;
        currentSpeed := 0.0;
        
        CASE ElevatorNumber OF
            1: Q_Elevator1_Enable := FALSE;
            2: Q_Elevator2_Enable := FALSE;
            3: Q_Elevator3_Enable := FALSE;
        END_CASE;
        
        // Update statistics
        lastMovementTime := movementTimer.ET;
        totalDistance := totalDistance + ABS(targetPos - currentPos);
        averageSpeed := ABS(targetPos - currentPos) / TIME_TO_REAL(lastMovementTime);
        
        state := 20; // Open doors
    
    20: // OPEN_DOORS
        doorState := 1; // Opening
        doorTimer(IN := TRUE, PT := doorTimeout);
        
        stateTimer(IN := TRUE, PT := T#2s);
        
        IF stateTimer.Q THEN
            doorState := 2; // Open
            DoorOpen := TRUE;
            state := 30; // Movement complete
            doorTimer(IN := FALSE);
            stateTimer(IN := FALSE);
        ELSIF doorTimer.Q THEN
            // Door open timeout - continue anyway
            DoorOpen := FALSE;
            state := 30;
            doorTimer(IN := FALSE);
        END_IF;
    
    30: // MOVEMENT_COMPLETE
        Done := TRUE;
        Busy := FALSE;
        Available := TRUE;
        AtLevel := TRUE;
        
        // Log successful movement
        LogEvent('ELEVATOR_MOVEMENT', 'Elevator ' + INT_TO_STRING(ElevatorNumber) + 
                 ' moved to level ' + INT_TO_STRING(TargetLevel) + 
                 ' in ' + TIME_TO_STRING(lastMovementTime));
        
        state := 0; // Return to idle
    
    // =============================================================================
    // MANUAL MODE (States 80-89)
    // =============================================================================
    
    80: // MANUAL_OPERATION
        Available := FALSE;
        
        IF NOT ManualMode THEN
            state := 0; // Exit manual mode
            targetSpeed := 0.0;
        ELSE
            // Enable motor
            CASE ElevatorNumber OF
                1: Q_Elevator1_Enable := TRUE;
                   Q_Elevator1_Direction := ManualDirection;
                2: Q_Elevator2_Enable := TRUE;
                   Q_Elevator2_Direction := ManualDirection;
                3: Q_Elevator3_Enable := TRUE;
                   Q_Elevator3_Direction := ManualDirection;
            END_CASE;
            
            targetSpeed := ManualSpeed;
            currentSpeed := ManualSpeed;
            
            // Safety limits in manual mode
            IF currentPos <= 0.0 AND NOT ManualDirection THEN
                targetSpeed := 0.0; // At bottom limit
            ELSIF currentPos >= 45000.0 AND ManualDirection THEN
                targetSpeed := 0.0; // At top limit
            END_IF;
        END_IF;
    
    // =============================================================================
    // ERROR STATES (States 90-99)
    // =============================================================================
    
    90: // EMERGENCY_STOP
        targetSpeed := 0.0;
        currentSpeed := 0.0;
        Available := FALSE;
        Error := TRUE;
        
        // Stop motor immediately
        CASE ElevatorNumber OF
            1: Q_Elevator1_Enable := FALSE;
            2: Q_Elevator2_Enable := FALSE;
            3: Q_Elevator3_Enable := FALSE;
        END_CASE;
        
        // Log emergency stop
        LogError(ErrorID, 'Emergency stop - Elevator ' + INT_TO_STRING(ElevatorNumber));
        
        // Stay in this state until reset
    
    91: // ERROR_WITH_RETRY
        Error := TRUE;
        Available := FALSE;
        targetSpeed := 0.0;
        
        // Stop motor
        CASE ElevatorNumber OF
            1: Q_Elevator1_Enable := FALSE;
            2: Q_Elevator2_Enable := FALSE;
            3: Q_Elevator3_Enable := FALSE;
        END_CASE;
        
        // Record error
        errorHistory[errorIndex] := ErrorID;
        errorIndex := errorIndex + 1;
        IF errorIndex > 10 THEN errorIndex := 1; END_IF;
        
        // Retry logic
        IF retryCount < maxRetries AND safetyOK THEN
            retryCount := retryCount + 1;
            stateTimer(IN := TRUE, PT := T#10s);
            
            IF stateTimer.Q THEN
                state := 10; // Retry movement
                Error := FALSE;
                ErrorID := 0;
                stateTimer(IN := FALSE);
            END_IF;
        ELSE
            state := 90; // Give up, require manual reset
        END_IF;

END_CASE;

// Set speed reference outputs
CASE ElevatorNumber OF
    1: AQ_Elevator1_SpeedRef := REAL_TO_INT(currentSpeed);
    2: AQ_Elevator2_SpeedRef := REAL_TO_INT(currentSpeed);
    3: AQ_Elevator3_SpeedRef := REAL_TO_INT(currentSpeed);
END_CASE;

// Update motor speed output for monitoring
MotorSpeed := currentSpeed;

// Update total operation time
totalOperationTime := totalOperationTime + T#100ms;

// Update elevator data structure
CASE ElevatorNumber OF
    1: Elevator1.CurrentLevel := CurrentLevel;
       Elevator1.CurrentPosition := currentPos;
       Elevator1.TargetLevel := TargetLevel;
       Elevator1.TargetPosition := targetPos;
       Elevator1.Speed := currentSpeed;
       Elevator1.LoadWeight := LoadWeight;
       Elevator1.Available := Available;
       Elevator1.FaultCode := ErrorID;
       Elevator1.OperationHours := totalOperationTime;
       
    2: Elevator2.CurrentLevel := CurrentLevel;
       Elevator2.CurrentPosition := currentPos;
       Elevator2.TargetLevel := TargetLevel;
       Elevator2.TargetPosition := targetPos;
       Elevator2.Speed := currentSpeed;
       Elevator2.LoadWeight := LoadWeight;
       Elevator2.Available := Available;
       Elevator2.FaultCode := ErrorID;
       Elevator2.OperationHours := totalOperationTime;
       
    3: Elevator3.CurrentLevel := CurrentLevel;
       Elevator3.CurrentPosition := currentPos;
       Elevator3.TargetLevel := TargetLevel;
       Elevator3.TargetPosition := targetPos;
       Elevator3.Speed := currentSpeed;
       Elevator3.LoadWeight := LoadWeight;
       Elevator3.Available := Available;
       Elevator3.FaultCode := ErrorID;
       Elevator3.OperationHours := totalOperationTime;
END_CASE;

// Store previous state for debugging
previousState := state;

END_FUNCTION_BLOCK
