PROGRAM ParkingVendingSystem
VAR
    // Main system state machine
    currentState : SystemState := INIT;
    previousState : SystemState;
    stateTimer : TON;
    
    // System status and control
    systemEnabled : BOOL := FALSE;
    emergencyStop : BOOL := FALSE;
    systemReady : BOOL := FALSE;
    
    // Customer interface
    customerPresent : BOOL := FALSE;
    paymentReceived : BOOL := FALSE;
    ticketPrinted : BOOL := FALSE;
    
    // Vehicle handling
    vehicleAtEntry : BOOL := FALSE;
    vehicleOnPlatform : BOOL := FALSE;
    vehicleParked : BOOL := FALSE;
    
    // System counters and statistics
    totalVehiclesParked : INT := 0;
    totalVehiclesRetrieved : INT := 0;
    systemOperationTime : TIME;
    
    // Error handling
    errorCode : INT := 0;
    errorMessage : STRING[100] := '';
    
    // Performance metrics
    lastParkingTime : TIME;
    lastRetrievalTime : TIME;
    averageParkingTime : TIME;
    
    // Timers for operations
    entryTimer : TON;
    parkingTimer : TON;
    retrievalTimer : TON;
    exitTimer : TON;
    
    // Safety and monitoring
    allSafetyOK : BOOL := FALSE;
    fireDetected : BOOL := FALSE;
    powerFailure : BOOL := FALSE;
    
END_VAR

// Emergency stop handling
IF I_EmergencyStop_Main OR I_EmergencyStop_Level1 OR I_EmergencyStop_Level2 THEN
    emergencyStop := TRUE;
    currentState := EMERGENCY;
    Q_StatusLight_Red := TRUE;
    Q_StatusLight_Green := FALSE;
    Q_StatusLight_Yellow := FALSE;
    Q_AlarmHorn := TRUE;
    Q_EmergencyLighting := TRUE;
END_IF;

// Fire detection handling
IF I_FireDetection_Zone1 OR I_FireDetection_Zone2 OR I_FireDetection_Zone3 THEN
    fireDetected := TRUE;
    currentState := EMERGENCY;
    Q_StatusLight_Red := TRUE;
    Q_AlarmHorn := TRUE;
    Q_VentilationFan := TRUE; // Start smoke evacuation
END_IF;

// Safety system check
allSafetyOK := I_DoorInterlocks_AllClosed AND 
               I_HydraulicSystem_PressureOK AND 
               I_UPS_BatteryOK AND 
               I_Ventilation_StatusOK AND
               NOT fireDetected AND
               NOT emergencyStop;

// Main state machine
CASE currentState OF
    
    INIT:
        // System initialization
        Q_StatusLight_Yellow := TRUE;
        Q_StatusLight_Green := FALSE;
        Q_StatusLight_Red := FALSE;
        
        // Initialize all outputs
        Q_EntryBarrier_Open := FALSE;
        Q_EntryBarrier_Close := TRUE;
        Q_ExitBarrier_Open := FALSE;
        Q_ExitBarrier_Close := TRUE;
        
        // Reset system variables
        customerPresent := FALSE;
        paymentReceived := FALSE;
        ticketPrinted := FALSE;
        vehicleAtEntry := FALSE;
        vehicleOnPlatform := FALSE;
        
        // Enable subsystems
        Q_HydraulicPump := TRUE;
        Q_VentilationFan := TRUE;
        
        // Check if all systems are ready
        stateTimer(IN := TRUE, PT := T#5s);
        IF stateTimer.Q AND allSafetyOK THEN
            systemReady := TRUE;
            currentState := IDLE;
            stateTimer(IN := FALSE);
        END_IF;
    
    IDLE:
        // System ready for operation
        Q_StatusLight_Green := TRUE;
        Q_StatusLight_Yellow := FALSE;
        Q_StatusLight_Red := FALSE;
        Q_AlarmHorn := FALSE;
        
        systemEnabled := TRUE;
        
        // Check for customer presence
        IF I_VehiclePresent_Entry THEN
            customerPresent := TRUE;
            currentState := PAYMENT;
        END_IF;
        
        // Monitor system health
        IF NOT allSafetyOK THEN
            currentState := EMERGENCY;
        END_IF;
    
    PAYMENT:
        // Payment processing state
        Q_StatusLight_Yellow := TRUE;
        
        // Call payment controller
        paymentReceived := PaymentController.ProcessPayment();
        
        // Payment timeout handling
        stateTimer(IN := TRUE, PT := T#120s);
        IF stateTimer.Q AND NOT paymentReceived THEN
            currentState := IDLE; // Timeout - return to idle
            stateTimer(IN := FALSE);
        ELSIF paymentReceived THEN
            currentState := ENTRY;
            stateTimer(IN := FALSE);
        END_IF;
    
    ENTRY:
        // Vehicle entry sequence
        Q_StatusLight_Yellow := TRUE;
        
        // Open entry barrier
        Q_EntryBarrier_Open := TRUE;
        Q_EntryBarrier_Close := FALSE;
        
        entryTimer(IN := TRUE, PT := T#30s);
        
        // Wait for vehicle to enter
        IF I_VehiclePresent_Entry AND vehicleAtEntry THEN
            vehicleOnPlatform := TRUE;
            Q_EntryBarrier_Open := FALSE;
            Q_EntryBarrier_Close := TRUE;
            currentState := PARKING;
            entryTimer(IN := FALSE);
        ELSIF entryTimer.Q THEN
            // Entry timeout
            Q_EntryBarrier_Open := FALSE;
            Q_EntryBarrier_Close := TRUE;
            currentState := IDLE;
            entryTimer(IN := FALSE);
        END_IF;
    
    PARKING:
        // Automated parking sequence
        Q_StatusLight_Yellow := TRUE;
        parkingTimer(IN := TRUE, PT := T#0s); // Start timing
        
        // Call parking controller
        IF ParkingController.ExecuteParkingSequence() THEN
            vehicleParked := TRUE;
            totalVehiclesParked := totalVehiclesParked + 1;
            lastParkingTime := parkingTimer.ET;
            
            // Update average parking time
            averageParkingTime := DINT_TO_TIME(
                (TIME_TO_DINT(averageParkingTime) * (totalVehiclesParked - 1) + 
                 TIME_TO_DINT(lastParkingTime)) / totalVehiclesParked
            );
            
            // Print parking ticket
            ticketPrinted := TRUE;
            currentState := PARKED;
            parkingTimer(IN := FALSE);
        END_IF;
        
        // Parking timeout (safety)
        IF parkingTimer.ET > T#300s THEN
            errorCode := 1001;
            errorMessage := 'Parking sequence timeout';
            currentState := EMERGENCY;
            parkingTimer(IN := FALSE);
        END_IF;
    
    PARKED:
        // Vehicle successfully parked
        Q_StatusLight_Green := TRUE;
        vehicleOnPlatform := FALSE;
        
        // Reset for next customer
        stateTimer(IN := TRUE, PT := T#10s);
        IF stateTimer.Q THEN
            customerPresent := FALSE;
            paymentReceived := FALSE;
            ticketPrinted := FALSE;
            vehicleAtEntry := FALSE;
            currentState := IDLE;
            stateTimer(IN := FALSE);
        END_IF;
    
    RETRIEVAL:
        // Vehicle retrieval sequence
        Q_StatusLight_Yellow := TRUE;
        retrievalTimer(IN := TRUE, PT := T#0s); // Start timing
        
        // Call parking controller for retrieval
        IF ParkingController.ExecuteRetrievalSequence() THEN
            totalVehiclesRetrieved := totalVehiclesRetrieved + 1;
            lastRetrievalTime := retrievalTimer.ET;
            currentState := EXIT_SEQUENCE;
            retrievalTimer(IN := FALSE);
        END_IF;
        
        // Retrieval timeout (safety)
        IF retrievalTimer.ET > T#300s THEN
            errorCode := 1002;
            errorMessage := 'Retrieval sequence timeout';
            currentState := EMERGENCY;
            retrievalTimer(IN := FALSE);
        END_IF;
    
    EXIT_SEQUENCE:
        // Vehicle exit sequence
        Q_StatusLight_Yellow := TRUE;
        
        // Open exit barrier
        Q_ExitBarrier_Open := TRUE;
        Q_ExitBarrier_Close := FALSE;
        
        exitTimer(IN := TRUE, PT := T#60s);
        
        // Wait for vehicle to exit
        IF NOT I_VehiclePresent_Exit THEN
            Q_ExitBarrier_Open := FALSE;
            Q_ExitBarrier_Close := TRUE;
            currentState := IDLE;
            exitTimer(IN := FALSE);
        ELSIF exitTimer.Q THEN
            // Exit timeout
            Q_ExitBarrier_Open := FALSE;
            Q_ExitBarrier_Close := TRUE;
            currentState := IDLE;
            exitTimer(IN := FALSE);
        END_IF;
    
    MAINTENANCE:
        // Maintenance mode
        Q_StatusLight_Yellow := TRUE;
        Q_StatusLight_Red := TRUE;
        systemEnabled := FALSE;
        
        // Disable all movements
        Q_Elevator1_Enable := FALSE;
        Q_Elevator2_Enable := FALSE;
        Q_Elevator3_Enable := FALSE;
        Q_Platform_XEnable := FALSE;
        Q_Platform_YEnable := FALSE;
        
        // Diagnostics can be run here
        // Manual return to normal operation required
    
    EMERGENCY:
        // Emergency state
        Q_StatusLight_Red := TRUE;
        Q_StatusLight_Green := FALSE;
        Q_StatusLight_Yellow := FALSE;
        Q_AlarmHorn := TRUE;
        Q_EmergencyLighting := TRUE;
        
        systemEnabled := FALSE;
        
        // Stop all movements immediately
        Q_Elevator1_Enable := FALSE;
        Q_Elevator2_Enable := FALSE;
        Q_Elevator3_Enable := FALSE;
        Q_Platform_XEnable := FALSE;
        Q_Platform_YEnable := FALSE;
        
        // Close all barriers
        Q_EntryBarrier_Open := FALSE;
        Q_EntryBarrier_Close := TRUE;
        Q_ExitBarrier_Open := FALSE;
        Q_ExitBarrier_Close := TRUE;
        
        // Keep essential systems running
        Q_HydraulicPump := TRUE;
        Q_VentilationFan := TRUE;
        
        // Emergency reset sequence (manual intervention required)
        IF NOT emergencyStop AND NOT fireDetected AND allSafetyOK THEN
            stateTimer(IN := TRUE, PT := T#10s);
            IF stateTimer.Q THEN
                currentState := INIT;
                emergencyStop := FALSE;
                fireDetected := FALSE;
                errorCode := 0;
                errorMessage := '';
                stateTimer(IN := FALSE);
            END_IF;
        END_IF;

END_CASE;

// Update system operation time
systemOperationTime := systemOperationTime + T#100ms;

// Store previous state for debugging
previousState := currentState;

// Global outputs for system status
Q_SystemReady := systemReady;
Q_SystemEnabled := systemEnabled;

END_PROGRAM
