FUNCTION_BLOCK ParkingController
VAR_INPUT
    Execute : BOOL;                     // Execute parking sequence
    VehicleRetrievalRequest : BOOL;     // Vehicle retrieval request
    CustomerID : STRING[50];            // Customer identification
    VehicleID : STRING[20];             // Vehicle license plate
    PaymentValidated : BOOL;            // Payment validation status
END_VAR

VAR_OUTPUT
    Done : BOOL;                        // Operation completed
    Busy : BOOL;                        // Operation in progress
    Error : BOOL;                       // Error occurred
    ErrorID : INT;                      // Error identification
    AssignedSpace : ParkingSpace;       // Assigned parking space
    EstimatedTime : TIME;               // Estimated completion time
END_VAR

VAR
    // State machine for parking operations
    state : INT := 0;
    stepTimer : TON;
    operationTimer : TON;
    
    // Vehicle handling
    vehicleDimensions : VehicleDimensions;
    optimalSpace : ParkingSpace;
    selectedElevator : INT;
    
    // Position control
    targetLevel : INT;
    targetXPosition : REAL;
    targetYPosition : REAL;
    currentOperation : STRING[50];
    
    // Safety and monitoring
    platformSecure : BOOL;
    elevatorReady : BOOL;
    spaceAvailable : BOOL;
    
    // Performance tracking
    operationStartTime : DATE_AND_TIME;
    parkingSequenceTime : TIME;
    retrievalSequenceTime : TIME;
    
    // Error handling
    retryCount : INT := 0;
    maxRetries : INT := 3;
    lastErrorTime : DATE_AND_TIME;
    
END_VAR

// Vehicle dimensions structure
TYPE VehicleDimensions :
STRUCT
    Length : REAL;
    Width : REAL;
    Height : REAL;
    Weight : REAL;
    VehicleType : VehicleSize;
END_STRUCT;
END_TYPE;

// Main execution logic
IF Execute AND NOT Busy THEN
    Busy := TRUE;
    Done := FALSE;
    Error := FALSE;
    state := 10; // Start parking sequence
    operationStartTime := GetSystemTime();
    operationTimer(IN := TRUE, PT := T#0s);
ELSIF VehicleRetrievalRequest AND NOT Busy THEN
    Busy := TRUE;
    Done := FALSE;
    Error := FALSE;
    state := 50; // Start retrieval sequence
    operationStartTime := GetSystemTime();
    operationTimer(IN := TRUE, PT := T#0s);
END_IF;

// Main state machine
CASE state OF
    
    0: // IDLE
        Busy := FALSE;
        Done := FALSE;
        Error := FALSE;
        currentOperation := 'IDLE';
    
    // =============================================================================
    // PARKING SEQUENCE (States 10-39)
    // =============================================================================
    
    10: // SCAN_VEHICLE_DIMENSIONS
        currentOperation := 'SCANNING_VEHICLE';
        
        // Get vehicle dimensions from laser scanners
        vehicleDimensions.Length := SCALE_INT_TO_REAL(AI_VehicleLength, 0.0, 6000.0);
        vehicleDimensions.Width := SCALE_INT_TO_REAL(AI_VehicleWidth, 0.0, 2500.0);
        vehicleDimensions.Height := SCALE_INT_TO_REAL(AI_VehicleHeight, 0.0, 2000.0);
        vehicleDimensions.Weight := SCALE_INT_TO_REAL(AI_VehicleWeight, 0.0, 5000.0);
        
        // Determine vehicle type
        IF vehicleDimensions.Length <= 4200.0 AND vehicleDimensions.Width <= 1800.0 THEN
            vehicleDimensions.VehicleType := COMPACT;
        ELSIF vehicleDimensions.Length <= 5200.0 AND vehicleDimensions.Width <= 2100.0 THEN
            vehicleDimensions.VehicleType := STANDARD;
        ELSIF vehicleDimensions.Height <= 1200.0 THEN
            vehicleDimensions.VehicleType := MOTORCYCLE;
        ELSE
            vehicleDimensions.VehicleType := SUV;
        END_IF;
        
        // Validate vehicle dimensions
        IF vehicleDimensions.Length > MaxVehicleLength OR
           vehicleDimensions.Width > MaxVehicleWidth OR
           vehicleDimensions.Height > MaxVehicleHeight OR
           vehicleDimensions.Weight > MaxVehicleWeight THEN
            Error := TRUE;
            ErrorID := 2001; // Vehicle too large
            state := 90; // Error handling
        ELSE
            state := 11; // Continue to space finding
        END_IF;
    
    11: // FIND_OPTIMAL_SPACE
        currentOperation := 'FINDING_PARKING_SPACE';
        
        IF FindOptimalParkingSpace() THEN
            state := 12; // Space found
        ELSE
            Error := TRUE;
            ErrorID := 2002; // No available space
            state := 90; // Error handling
        END_IF;
    
    12: // PREPARE_PLATFORM
        currentOperation := 'PREPARING_PLATFORM';
        
        // Ensure platform is at home position
        IF I_Platform_Home THEN
            Q_Platform_XEnable := TRUE;
            Q_Platform_YEnable := TRUE;
            Q_Platform_ZEnable := TRUE;
            state := 13;
        ELSE
            // Move platform to home position
            MovePlatformToHome();
        END_IF;
    
    13: // POSITION_VEHICLE_ON_PLATFORM
        currentOperation := 'POSITIONING_VEHICLE';
        
        stepTimer(IN := TRUE, PT := T#30s);
        
        // Check if vehicle is properly positioned
        IF I_VehiclePresent_Platform AND 
           ABS(AI_Platform_XPosition - 3000) < 50 AND  // Center X position
           ABS(AI_Platform_YPosition - 7500) < 50 THEN // Center Y position
            platformSecure := TRUE;
            state := 14;
            stepTimer(IN := FALSE);
        ELSIF stepTimer.Q THEN
            Error := TRUE;
            ErrorID := 2003; // Vehicle positioning timeout
            state := 90;
            stepTimer(IN := FALSE);
        END_IF;
    
    14: // SECURE_VEHICLE
        currentOperation := 'SECURING_VEHICLE';
        
        // Activate platform securing mechanisms
        Q_Platform_ZEnable := TRUE;
        AQ_Platform_ZSpeedRef := 100; // Slow speed for securing
        
        stepTimer(IN := TRUE, PT := T#10s);
        
        // Check if vehicle is secured (weight on platform)
        IF AI_LoadCell_PlatformWeight > 500 THEN // Minimum 500kg
            Platform.VehicleSecured := TRUE;
            state := 15;
            stepTimer(IN := FALSE);
        ELSIF stepTimer.Q THEN
            Error := TRUE;
            ErrorID := 2004; // Vehicle securing failed
            state := 90;
            stepTimer(IN := FALSE);
        END_IF;
    
    15: // SELECT_ELEVATOR
        currentOperation := 'SELECTING_ELEVATOR';
        
        selectedElevator := SelectOptimalElevator();
        
        IF selectedElevator > 0 THEN
            state := 16;
        ELSE
            Error := TRUE;
            ErrorID := 2005; // No elevator available
            state := 90;
        END_IF;
    
    16: // MOVE_TO_ELEVATOR
        currentOperation := 'MOVING_TO_ELEVATOR';
        
        // Calculate elevator loading position
        CASE selectedElevator OF
            1: targetXPosition := 1500.0; // Elevator 1 position
            2: targetXPosition := 3000.0; // Elevator 2 position
            3: targetXPosition := 4500.0; // Elevator 3 position
        END_CASE;
        
        targetYPosition := 2000.0; // Elevator loading position
        
        MovePlatformToPosition(targetXPosition, targetYPosition, 0.0);
        
        // Check if platform reached elevator
        IF ABS(AI_Platform_XPosition - targetXPosition) < 20 AND
           ABS(AI_Platform_YPosition - targetYPosition) < 20 THEN
            state := 17;
        END_IF;
    
    17: // LOAD_INTO_ELEVATOR
        currentOperation := 'LOADING_INTO_ELEVATOR';
        
        stepTimer(IN := TRUE, PT := T#60s);
        
        // Enable selected elevator
        CASE selectedElevator OF
            1: Q_Elevator1_Enable := TRUE;
            2: Q_Elevator2_Enable := TRUE;
            3: Q_Elevator3_Enable := TRUE;
        END_CASE;
        
        // Transfer vehicle to elevator
        Q_Platform_YEnable := TRUE;
        Q_Platform_YDirection := TRUE; // Move forward into elevator
        AQ_Platform_YSpeedRef := 500; // Slow speed for precision
        
        // Check if loading complete
        IF ABS(AI_Platform_YPosition - 1000.0) < 10 THEN // Inside elevator
            state := 18;
            stepTimer(IN := FALSE);
        ELSIF stepTimer.Q THEN
            Error := TRUE;
            ErrorID := 2006; // Elevator loading timeout
            state := 90;
            stepTimer(IN := FALSE);
        END_IF;
    
    18: // MOVE_TO_PARKING_LEVEL
        currentOperation := 'MOVING_TO_LEVEL';
        
        targetLevel := optimalSpace.Level;
        
        MoveElevatorToLevel(selectedElevator, targetLevel);
        
        // Check if elevator reached target level
        CASE selectedElevator OF
            1: IF ABS(AI_Elevator1_Position - (targetLevel * 3000)) < 50 THEN
                   state := 19;
               END_IF;
            2: IF ABS(AI_Elevator2_Position - (targetLevel * 3000)) < 50 THEN
                   state := 19;
               END_IF;
            3: IF ABS(AI_Elevator3_Position - (targetLevel * 3000)) < 50 THEN
                   state := 19;
               END_IF;
        END_CASE;
    
    19: // UNLOAD_FROM_ELEVATOR
        currentOperation := 'UNLOADING_FROM_ELEVATOR';
        
        stepTimer(IN := TRUE, PT := T#60s);
        
        // Move platform out of elevator to parking level
        Q_Platform_YDirection := FALSE; // Move backward out of elevator
        AQ_Platform_YSpeedRef := 500; // Slow speed
        
        // Calculate target position on parking level
        targetXPosition := optimalSpace.Position * 300.0; // 300mm spacing
        targetYPosition := 7500.0; // Level corridor position
        
        IF ABS(AI_Platform_YPosition - targetYPosition) < 20 THEN
            state := 20;
            stepTimer(IN := FALSE);
        ELSIF stepTimer.Q THEN
            Error := TRUE;
            ErrorID := 2007; // Elevator unloading timeout
            state := 90;
            stepTimer(IN := FALSE);
        END_IF;
    
    20: // MOVE_TO_PARKING_SPACE
        currentOperation := 'MOVING_TO_SPACE';
        
        MovePlatformToPosition(targetXPosition, targetYPosition, 0.0);
        
        // Check if platform reached parking space
        IF ABS(AI_Platform_XPosition - targetXPosition) < 10 AND
           ABS(AI_Platform_YPosition - targetYPosition) < 10 THEN
            state := 21;
        END_IF;
    
    21: // DEPOSIT_VEHICLE
        currentOperation := 'DEPOSITING_VEHICLE';
        
        stepTimer(IN := TRUE, PT := T#30s);
        
        // Lower platform to deposit vehicle
        Q_Platform_ZDirection := FALSE; // Move down
        AQ_Platform_ZSpeedRef := 200; // Very slow for safety
        
        // Check if vehicle deposited (reduced weight on platform)
        IF AI_LoadCell_PlatformWeight < 100 THEN // Most weight removed
            state := 22;
            stepTimer(IN := FALSE);
        ELSIF stepTimer.Q THEN
            Error := TRUE;
            ErrorID := 2008; // Vehicle deposit timeout
            state := 90;
            stepTimer(IN := FALSE);
        END_IF;
    
    22: // UPDATE_PARKING_RECORD
        currentOperation := 'UPDATING_RECORDS';
        
        // Mark space as occupied
        ParkingSpaces[optimalSpace.Level, optimalSpace.Position].Occupied := TRUE;
        ParkingSpaces[optimalSpace.Level, optimalSpace.Position].VehicleID := VehicleID;
        ParkingSpaces[optimalSpace.Level, optimalSpace.Position].ParkingTime := GetSystemTime();
        ParkingSpaces[optimalSpace.Level, optimalSpace.Position].VehicleType := vehicleDimensions.VehicleType;
        
        // Update transaction record
        CurrentTransaction.SpaceAssigned := optimalSpace;
        CurrentTransaction.Status := 'PARKED';
        
        // Update system statistics
        SystemStats.TotalVehiclesParked := SystemStats.TotalVehiclesParked + 1;
        parkingSequenceTime := operationTimer.ET;
        
        // Calculate average parking time
        SystemStats.AverageParkingTime := 
            DINT_TO_TIME((TIME_TO_DINT(SystemStats.AverageParkingTime) * 
                         (SystemStats.TotalVehiclesParked - 1) + 
                         TIME_TO_DINT(parkingSequenceTime)) / 
                         SystemStats.TotalVehiclesParked);
        
        state := 23; // Return platform home
    
    23: // RETURN_PLATFORM_HOME
        currentOperation := 'RETURNING_HOME';
        
        MovePlatformToHome();
        
        IF I_Platform_Home THEN
            state := 30; // Parking sequence complete
        END_IF;
    
    30: // PARKING_COMPLETE
        currentOperation := 'PARKING_COMPLETE';
        AssignedSpace := optimalSpace;
        Done := TRUE;
        Busy := FALSE;
        state := 0; // Return to idle
        
        // Log successful parking
        LogEvent('PARKING_SUCCESS', VehicleID + ' parked at Level ' + 
                 INT_TO_STRING(optimalSpace.Level) + ' Position ' + 
                 INT_TO_STRING(optimalSpace.Position));
    
    // =============================================================================
    // RETRIEVAL SEQUENCE (States 50-89)
    // =============================================================================
    
    50: // FIND_PARKED_VEHICLE
        currentOperation := 'FINDING_VEHICLE';
        
        IF FindParkedVehicle(VehicleID) THEN
            state := 51;
        ELSE
            Error := TRUE;
            ErrorID := 3001; // Vehicle not found
            state := 90;
        END_IF;
    
    51: // PREPARE_FOR_RETRIEVAL
        currentOperation := 'PREPARING_RETRIEVAL';
        
        // Select optimal elevator for retrieval
        selectedElevator := SelectOptimalElevator();
        
        // Ensure platform is at home
        IF I_Platform_Home THEN
            state := 52;
        ELSE
            MovePlatformToHome();
        END_IF;
    
    52: // MOVE_TO_RETRIEVAL_LEVEL
        currentOperation := 'MOVING_TO_LEVEL';
        
        targetLevel := optimalSpace.Level;
        MoveElevatorToLevel(selectedElevator, targetLevel);
        
        // Check if elevator reached target level
        CASE selectedElevator OF
            1: IF ABS(AI_Elevator1_Position - (targetLevel * 3000)) < 50 THEN
                   state := 53;
               END_IF;
            2: IF ABS(AI_Elevator2_Position - (targetLevel * 3000)) < 50 THEN
                   state := 53;
               END_IF;
            3: IF ABS(AI_Elevator3_Position - (targetLevel * 3000)) < 50 THEN
                   state := 53;
               END_IF;
        END_CASE;
    
    53: // MOVE_PLATFORM_TO_VEHICLE
        currentOperation := 'MOVING_TO_VEHICLE';
        
        targetXPosition := optimalSpace.Position * 300.0;
        targetYPosition := 7500.0;
        
        MovePlatformToPosition(targetXPosition, targetYPosition, 0.0);
        
        IF ABS(AI_Platform_XPosition - targetXPosition) < 10 AND
           ABS(AI_Platform_YPosition - targetYPosition) < 10 THEN
            state := 54;
        END_IF;
    
    54: // PICKUP_VEHICLE
        currentOperation := 'PICKING_UP_VEHICLE';
        
        stepTimer(IN := TRUE, PT := T#30s);
        
        // Raise platform to pickup vehicle
        Q_Platform_ZDirection := TRUE; // Move up
        AQ_Platform_ZSpeedRef := 200; // Slow speed for safety
        
        // Check if vehicle picked up (increased weight)
        IF AI_LoadCell_PlatformWeight > 500 THEN
            Platform.VehicleSecured := TRUE;
            state := 55;
            stepTimer(IN := FALSE);
        ELSIF stepTimer.Q THEN
            Error := TRUE;
            ErrorID := 3002; // Vehicle pickup timeout
            state := 90;
            stepTimer(IN := FALSE);
        END_IF;
    
    55: // MOVE_TO_ELEVATOR_FOR_RETRIEVAL
        currentOperation := 'MOVING_TO_ELEVATOR';
        
        // Calculate elevator position
        CASE selectedElevator OF
            1: targetXPosition := 1500.0;
            2: targetXPosition := 3000.0;
            3: targetXPosition := 4500.0;
        END_CASE;
        
        targetYPosition := 2000.0;
        
        MovePlatformToPosition(targetXPosition, targetYPosition, Platform.ZPosition);
        
        IF ABS(AI_Platform_XPosition - targetXPosition) < 20 AND
           ABS(AI_Platform_YPosition - targetYPosition) < 20 THEN
            state := 56;
        END_IF;
    
    56: // LOAD_INTO_ELEVATOR_FOR_RETRIEVAL
        currentOperation := 'LOADING_INTO_ELEVATOR';
        
        stepTimer(IN := TRUE, PT := T#60s);
        
        // Move platform into elevator
        Q_Platform_YDirection := TRUE;
        AQ_Platform_YSpeedRef := 500;
        
        IF ABS(AI_Platform_YPosition - 1000.0) < 10 THEN
            state := 57;
            stepTimer(IN := FALSE);
        ELSIF stepTimer.Q THEN
            Error := TRUE;
            ErrorID := 3003; // Elevator loading timeout
            state := 90;
            stepTimer(IN := FALSE);
        END_IF;
    
    57: // MOVE_TO_GROUND_LEVEL
        currentOperation := 'MOVING_TO_GROUND';
        
        MoveElevatorToLevel(selectedElevator, 1); // Ground level
        
        // Check if elevator reached ground level
        CASE selectedElevator OF
            1: IF ABS(AI_Elevator1_Position) < 50 THEN
                   state := 58;
               END_IF;
            2: IF ABS(AI_Elevator2_Position) < 50 THEN
                   state := 58;
               END_IF;
            3: IF ABS(AI_Elevator3_Position) < 50 THEN
                   state := 58;
               END_IF;
        END_CASE;
    
    58: // UNLOAD_FROM_ELEVATOR_TO_EXIT
        currentOperation := 'UNLOADING_FOR_EXIT';
        
        stepTimer(IN := TRUE, PT := T#60s);
        
        // Move platform out of elevator
        Q_Platform_YDirection := FALSE;
        targetYPosition := 15000.0; // Exit position
        
        IF ABS(AI_Platform_YPosition - targetYPosition) < 20 THEN
            state := 59;
            stepTimer(IN := FALSE);
        ELSIF stepTimer.Q THEN
            Error := TRUE;
            ErrorID := 3004; // Exit positioning timeout
            state := 90;
            stepTimer(IN := FALSE);
        END_IF;
    
    59: // DELIVER_VEHICLE
        currentOperation := 'DELIVERING_VEHICLE';
        
        stepTimer(IN := TRUE, PT := T#30s);
        
        // Lower platform to deliver vehicle
        Q_Platform_ZDirection := FALSE;
        AQ_Platform_ZSpeedRef := 200;
        
        // Check if vehicle delivered
        IF AI_LoadCell_PlatformWeight < 100 THEN
            state := 60;
            stepTimer(IN := FALSE);
        ELSIF stepTimer.Q THEN
            Error := TRUE;
            ErrorID := 3005; // Vehicle delivery timeout
            state := 90;
            stepTimer(IN := FALSE);
        END_IF;
    
    60: // UPDATE_RETRIEVAL_RECORD
        currentOperation := 'UPDATING_RECORDS';
        
        // Mark space as available
        ParkingSpaces[optimalSpace.Level, optimalSpace.Position].Occupied := FALSE;
        ParkingSpaces[optimalSpace.Level, optimalSpace.Position].VehicleID := '';
        
        // Update system statistics
        SystemStats.TotalVehiclesRetrieved := SystemStats.TotalVehiclesRetrieved + 1;
        retrievalSequenceTime := operationTimer.ET;
        
        state := 61; // Return platform home
    
    61: // RETURN_PLATFORM_HOME_AFTER_RETRIEVAL
        currentOperation := 'RETURNING_HOME';
        
        MovePlatformToHome();
        
        IF I_Platform_Home THEN
            state := 70; // Retrieval complete
        END_IF;
    
    70: // RETRIEVAL_COMPLETE
        currentOperation := 'RETRIEVAL_COMPLETE';
        Done := TRUE;
        Busy := FALSE;
        state := 0;
        
        // Log successful retrieval
        LogEvent('RETRIEVAL_SUCCESS', VehicleID + ' retrieved from Level ' + 
                 INT_TO_STRING(optimalSpace.Level) + ' Position ' + 
                 INT_TO_STRING(optimalSpace.Position));
    
    // =============================================================================
    // ERROR HANDLING (States 90-99)
    // =============================================================================
    
    90: // ERROR_STATE
        currentOperation := 'ERROR_HANDLING';
        Error := TRUE;
        Busy := FALSE;
        
        // Log error
        LogError(ErrorID, 'Parking Controller Error: ' + INT_TO_STRING(ErrorID));
        
        // Attempt recovery if retries available
        IF retryCount < maxRetries THEN
            retryCount := retryCount + 1;
            stepTimer(IN := TRUE, PT := T#5s);
            IF stepTimer.Q THEN
                state := 10; // Retry from beginning
                stepTimer(IN := FALSE);
            END_IF;
        ELSE
            state := 0; // Give up and return to idle
            retryCount := 0;
        END_IF;

END_CASE;

// ============================================================================
// HELPER FUNCTIONS
// ============================================================================

// Function to find optimal parking space
FUNCTION FindOptimalParkingSpace : BOOL
VAR
    level, position : INT;
    found : BOOL := FALSE;
    bestLevel, bestPosition : INT;
    minDistance : REAL := 999999.0;
    distance : REAL;
END_VAR

// Search for available space starting from lowest levels
FOR level := 1 TO MAX_PARKING_LEVELS DO
    FOR position := 1 TO SPACES_PER_LEVEL DO
        IF NOT ParkingSpaces[level, position].Occupied AND
           NOT ParkingSpaces[level, position].MaintenanceRequired THEN
            
            // Calculate distance/efficiency score
            distance := level * 100.0 + ABS(position - 10) * 10.0;
            
            IF distance < minDistance THEN
                minDistance := distance;
                bestLevel := level;
                bestPosition := position;
                found := TRUE;
            END_IF;
        END_IF;
    END_FOR;
END_FOR;

IF found THEN
    optimalSpace.Level := bestLevel;
    optimalSpace.Position := bestPosition;
    spaceAvailable := TRUE;
ELSE
    spaceAvailable := FALSE;
END_IF;

FindOptimalParkingSpace := found;
END_FUNCTION;

// Function to select optimal elevator
FUNCTION SelectOptimalElevator : INT
VAR
    selectedElev : INT := 0;
    elev1Distance, elev2Distance, elev3Distance : REAL;
    targetPosition : REAL;
END_VAR

targetPosition := targetLevel * 3000.0;

// Calculate distance for each elevator
elev1Distance := ABS(AI_Elevator1_Position - targetPosition);
elev2Distance := ABS(AI_Elevator2_Position - targetPosition);
elev3Distance := ABS(AI_Elevator3_Position - targetPosition);

// Select closest available elevator
IF Elevator1.Available AND (elev1Distance <= elev2Distance) AND (elev1Distance <= elev3Distance) THEN
    selectedElev := 1;
ELSIF Elevator2.Available AND (elev2Distance <= elev3Distance) THEN
    selectedElev := 2;
ELSIF Elevator3.Available THEN
    selectedElev := 3;
END_IF;

SelectOptimalElevator := selectedElev;
END_FUNCTION;

// Calculate estimated operation time
EstimatedTime := T#90s; // Base time
IF vehicleDimensions.VehicleType = SUV THEN
    EstimatedTime := EstimatedTime + T#30s; // Extra time for larger vehicles
END_IF;
IF targetLevel > 10 THEN
    EstimatedTime := EstimatedTime + T#20s; // Extra time for higher levels
END_IF;

END_FUNCTION_BLOCK
