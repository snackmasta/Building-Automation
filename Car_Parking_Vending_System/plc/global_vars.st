// Global Variables for Car Parking Vending System
// Version: 2.1.0
// Compatible with: Siemens S7-1200/1500, TIA Portal V17+

// =============================================================================
// SYSTEM ENUMERATIONS
// =============================================================================

TYPE SystemState :
(
    INIT := 0,              // System initialization
    IDLE := 1,              // Ready for operation
    PAYMENT := 2,           // Processing payment
    ENTRY := 3,             // Vehicle entry sequence
    PARKING := 4,           // Automated parking
    PARKED := 5,            // Vehicle stored
    RETRIEVAL := 6,         // Vehicle retrieval
    EXIT_SEQUENCE := 7,     // Vehicle exit
    MAINTENANCE := 8,       // Maintenance mode
    EMERGENCY := 9          // Emergency stop
);
END_TYPE;

TYPE ElevatorState :
(
    IDLE := 0,              // Elevator at rest
    MOVING_UP := 1,         // Moving upward
    MOVING_DOWN := 2,       // Moving downward
    POSITIONING := 3,       // Fine positioning
    LOADING := 4,           // Loading vehicle
    UNLOADING := 5,         // Unloading vehicle
    ERROR := 6              // Error state
);
END_TYPE;

TYPE PlatformState :
(
    HOME := 0,              // Home position
    MOVING_X := 1,          // Moving X axis
    MOVING_Y := 2,          // Moving Y axis
    POSITIONING := 3,       // Final positioning
    PICKING_UP := 4,        // Picking up vehicle
    DROPPING_OFF := 5,      // Dropping off vehicle
    ERROR := 6              // Error state
);
END_TYPE;

TYPE PaymentMethod :
(
    NONE := 0,              // No payment
    CASH := 1,              // Cash payment
    CREDIT_CARD := 2,       // Credit/Debit card
    RFID_CARD := 3,         // RFID membership card
    MOBILE_APP := 4,        // Mobile application
    QR_CODE := 5            // QR code payment
);
END_TYPE;

TYPE VehicleSize :
(
    COMPACT := 1,           // Small cars
    STANDARD := 2,          // Standard size
    SUV := 3,               // SUV/Large cars
    MOTORCYCLE := 4         // Motorcycles
);
END_TYPE;

// =============================================================================
// DIGITAL INPUTS (24V DC)
// =============================================================================

VAR_GLOBAL
    // Emergency stops and safety
    I_EmergencyStop_Main        AT %I0.0 : BOOL;   // Main emergency stop
    I_EmergencyStop_Level1      AT %I0.1 : BOOL;   // Level 1 emergency stop
    I_EmergencyStop_Level2      AT %I0.2 : BOOL;   // Level 2 emergency stop
    I_FireDetection_Zone1       AT %I0.3 : BOOL;   // Fire detector zone 1
    I_FireDetection_Zone2       AT %I0.4 : BOOL;   // Fire detector zone 2
    I_FireDetection_Zone3       AT %I0.5 : BOOL;   // Fire detector zone 3
    
    // Barrier positions
    I_EntryBarrier_OpenLimit    AT %I0.6 : BOOL;   // Entry barrier open
    I_EntryBarrier_CloseLimit   AT %I0.7 : BOOL;   // Entry barrier closed
    I_ExitBarrier_OpenLimit     AT %I1.0 : BOOL;   // Exit barrier open
    I_ExitBarrier_CloseLimit    AT %I1.1 : BOOL;   // Exit barrier closed
    
    // Vehicle detection
    I_VehiclePresent_Entry      AT %I1.2 : BOOL;   // Vehicle at entry
    I_VehiclePresent_Exit       AT %I1.3 : BOOL;   // Vehicle at exit
    I_VehiclePresent_Platform   AT %I1.4 : BOOL;   // Vehicle on platform
    I_VehiclePresent_Queue      AT %I1.5 : BOOL;   // Vehicle in queue
    
    // System positions
    I_Elevator1_Home            AT %I1.6 : BOOL;   // Elevator 1 home
    I_Elevator2_Home            AT %I1.7 : BOOL;   // Elevator 2 home
    I_Elevator3_Home            AT %I2.0 : BOOL;   // Elevator 3 home
    I_Platform_Home             AT %I2.1 : BOOL;   // Platform home position
    
    // System status
    I_DoorInterlocks_AllClosed  AT %I2.2 : BOOL;   // All doors closed
    I_HydraulicSystem_PressureOK AT %I2.3 : BOOL;  // Hydraulic pressure OK
    I_UPS_BatteryOK            AT %I2.4 : BOOL;   // UPS battery status
    I_Ventilation_StatusOK     AT %I2.5 : BOOL;   // Ventilation system OK
    I_MainPower_OK             AT %I2.6 : BOOL;   // Main power status
    I_NetworkConnection_OK     AT %I2.7 : BOOL;   // Network connectivity
    
    // Payment system inputs
    I_PaymentKiosk_Ready       AT %I3.0 : BOOL;   // Payment kiosk ready
    I_CashInserted             AT %I3.1 : BOOL;   // Cash payment received
    I_CardInserted             AT %I3.2 : BOOL;   // Card inserted
    I_RFIDCardPresent          AT %I3.3 : BOOL;   // RFID card detected
    I_QRCodeScanned            AT %I3.4 : BOOL;   // QR code scanned
    I_TicketPrinter_Ready      AT %I3.5 : BOOL;   // Ticket printer ready
    I_TicketPrinter_PaperOK    AT %I3.6 : BOOL;   // Printer paper OK
    I_ReceiptPrinter_Ready     AT %I3.7 : BOOL;   // Receipt printer ready
    
END_VAR;

// =============================================================================
// ANALOG INPUTS (4-20mA / 0-10V)
// =============================================================================

VAR_GLOBAL
    // Position feedback
    AI_Elevator1_Position       AT %IW0 : INT;     // Elevator 1 position (mm)
    AI_Elevator2_Position       AT %IW2 : INT;     // Elevator 2 position (mm)
    AI_Elevator3_Position       AT %IW4 : INT;     // Elevator 3 position (mm)
    AI_Platform_XPosition       AT %IW6 : INT;     // Platform X position (mm)
    AI_Platform_YPosition       AT %IW8 : INT;     // Platform Y position (mm)
    AI_Platform_ZPosition       AT %IW10 : INT;    // Platform Z position (mm)
    
    // System monitoring
    AI_HydraulicPressure        AT %IW12 : INT;    // Hydraulic pressure (bar)
    AI_Temperature_ControlRoom  AT %IW14 : INT;    // Control room temp (°C)
    AI_Humidity_ControlRoom     AT %IW16 : INT;    // Control room humidity (%)
    AI_LoadCell_PlatformWeight  AT %IW18 : INT;    // Platform load (kg)
    AI_PowerConsumption         AT %IW20 : INT;    // Power consumption (kW)
    AI_VibrationLevel          AT %IW22 : INT;    // Vibration level
    
    // Vehicle dimensions (from laser scanners)
    AI_VehicleLength           AT %IW24 : INT;    // Vehicle length (mm)
    AI_VehicleWidth            AT %IW26 : INT;    // Vehicle width (mm)
    AI_VehicleHeight           AT %IW28 : INT;    // Vehicle height (mm)
    AI_VehicleWeight           AT %IW30 : INT;    // Vehicle weight (kg)
    
END_VAR;

// =============================================================================
// DIGITAL OUTPUTS (24V DC)
// =============================================================================

VAR_GLOBAL
    // Barrier controls
    Q_EntryBarrier_Open         AT %Q0.0 : BOOL;   // Open entry barrier
    Q_EntryBarrier_Close        AT %Q0.1 : BOOL;   // Close entry barrier
    Q_ExitBarrier_Open          AT %Q0.2 : BOOL;   // Open exit barrier
    Q_ExitBarrier_Close         AT %Q0.3 : BOOL;   // Close exit barrier
    
    // Elevator controls
    Q_Elevator1_Enable          AT %Q0.4 : BOOL;   // Elevator 1 motor enable
    Q_Elevator2_Enable          AT %Q0.5 : BOOL;   // Elevator 2 motor enable
    Q_Elevator3_Enable          AT %Q0.6 : BOOL;   // Elevator 3 motor enable
    Q_Elevator1_Direction       AT %Q0.7 : BOOL;   // Elevator 1 direction
    Q_Elevator2_Direction       AT %Q1.0 : BOOL;   // Elevator 2 direction
    Q_Elevator3_Direction       AT %Q1.1 : BOOL;   // Elevator 3 direction
    
    // Platform controls
    Q_Platform_XEnable          AT %Q1.2 : BOOL;   // Platform X axis enable
    Q_Platform_YEnable          AT %Q1.3 : BOOL;   // Platform Y axis enable
    Q_Platform_ZEnable          AT %Q1.4 : BOOL;   // Platform Z axis enable
    Q_Platform_XDirection       AT %Q1.5 : BOOL;   // Platform X direction
    Q_Platform_YDirection       AT %Q1.6 : BOOL;   // Platform Y direction
    Q_Platform_ZDirection       AT %Q1.7 : BOOL;   // Platform Z direction
    
    // System controls
    Q_HydraulicPump            AT %Q2.0 : BOOL;   // Hydraulic pump start
    Q_VentilationFan           AT %Q2.1 : BOOL;   // Ventilation fan start
    Q_EmergencyLighting        AT %Q2.2 : BOOL;   // Emergency lighting
    Q_MainLighting             AT %Q2.3 : BOOL;   // Main lighting
    
    // Status indicators
    Q_StatusLight_Green        AT %Q2.4 : BOOL;   // Green status light
    Q_StatusLight_Yellow       AT %Q2.5 : BOOL;   // Yellow status light
    Q_StatusLight_Red          AT %Q2.6 : BOOL;   // Red status light
    Q_AlarmHorn               AT %Q2.7 : BOOL;   // Alarm horn
    
    // Door locks and safety
    Q_DoorLock_Entry          AT %Q3.0 : BOOL;   // Entry door lock
    Q_DoorLock_Exit           AT %Q3.1 : BOOL;   // Exit door lock
    Q_SafetyReset             AT %Q3.2 : BOOL;   // Safety system reset
    
    // Payment and printing
    Q_TicketPrinter_Print     AT %Q3.3 : BOOL;   // Print parking ticket
    Q_ReceiptPrinter_Print    AT %Q3.4 : BOOL;   // Print payment receipt
    Q_CashDispenser_Enable    AT %Q3.5 : BOOL;   // Cash change dispenser
    Q_CardReader_Enable       AT %Q3.6 : BOOL;   // Card reader enable
    Q_Display_Enable          AT %Q3.7 : BOOL;   // Customer display enable
    
    // System status outputs
    Q_SystemReady             AT %Q4.0 : BOOL;   // System ready indicator
    Q_SystemEnabled           AT %Q4.1 : BOOL;   // System enabled
    Q_MaintenanceMode         AT %Q4.2 : BOOL;   // Maintenance mode active
    Q_EmergencyActive         AT %Q4.3 : BOOL;   // Emergency mode active
    
END_VAR;

// =============================================================================
// ANALOG OUTPUTS (4-20mA / 0-10V)
// =============================================================================

VAR_GLOBAL
    // Speed references
    AQ_Elevator1_SpeedRef       AT %QW0 : INT;     // Elevator 1 speed ref
    AQ_Elevator2_SpeedRef       AT %QW2 : INT;     // Elevator 2 speed ref
    AQ_Elevator3_SpeedRef       AT %QW4 : INT;     // Elevator 3 speed ref
    AQ_Platform_XSpeedRef       AT %QW6 : INT;     // Platform X speed ref
    AQ_Platform_YSpeedRef       AT %QW8 : INT;     // Platform Y speed ref
    AQ_Platform_ZSpeedRef       AT %QW10 : INT;    // Platform Z speed ref
    
    // System controls
    AQ_HydraulicPressureRef     AT %QW12 : INT;    // Hydraulic pressure ref
    AQ_VentilationSpeedRef      AT %QW14 : INT;    // Ventilation speed ref
    AQ_LightingLevel           AT %QW16 : INT;    // Lighting level control
    
END_VAR;

// =============================================================================
// DATA STRUCTURES
// =============================================================================

TYPE ParkingSpace :
STRUCT
    Level : INT;                // Parking level (1-15)
    Position : INT;             // Position on level (1-20)
    Occupied : BOOL;            // Space occupied flag
    VehicleID : STRING[20];     // Vehicle identification
    ParkingTime : DATE_AND_TIME; // Time when parked
    VehicleType : VehicleSize;   // Vehicle size category
    ReservedFor : STRING[50];    // Reserved for specific customer
    MaintenanceRequired : BOOL;  // Maintenance flag
END_STRUCT;
END_TYPE;

TYPE Transaction :
STRUCT
    TransactionID : DINT;       // Unique transaction ID
    Timestamp : DATE_AND_TIME;  // Transaction timestamp
    CustomerID : STRING[50];    // Customer identification
    VehicleID : STRING[20];     // Vehicle license plate
    PaymentMethod : PaymentMethod; // Payment type used
    Amount : REAL;              // Payment amount
    ParkingDuration : TIME;     // Requested parking duration
    SpaceAssigned : ParkingSpace; // Assigned parking space
    Status : STRING[20];        // Transaction status
END_STRUCT;
END_TYPE;

TYPE SystemStatistics :
STRUCT
    TotalVehiclesParked : DINT;     // Total vehicles parked
    TotalVehiclesRetrieved : DINT;  // Total vehicles retrieved
    TotalRevenue : REAL;            // Total revenue generated
    AverageParkingTime : TIME;      // Average parking operation time
    AverageRetrievalTime : TIME;    // Average retrieval operation time
    SystemUptime : TIME;            // Total system uptime
    MaintenanceHours : TIME;        // Total maintenance time
    EmergencyStops : INT;           // Number of emergency stops
    PowerFailures : INT;            // Number of power failures
    LastMaintenanceDate : DATE;     // Last maintenance date
END_STRUCT;
END_TYPE;

TYPE ElevatorData :
STRUCT
    CurrentLevel : INT;         // Current elevator level
    TargetLevel : INT;          // Target level
    CurrentPosition : REAL;     // Current position (mm)
    TargetPosition : REAL;      // Target position (mm)
    Speed : REAL;               // Current speed (mm/s)
    State : ElevatorState;      // Current state
    LoadWeight : REAL;          // Current load weight (kg)
    LastService : DATE;         // Last service date
    OperationHours : TIME;      // Total operation hours
    FaultCode : INT;            // Current fault code
    Available : BOOL;           // Elevator available
END_STRUCT;
END_TYPE;

TYPE PlatformData :
STRUCT
    XPosition : REAL;           // Current X position (mm)
    YPosition : REAL;           // Current Y position (mm)
    ZPosition : REAL;           // Current Z position (mm)
    XTarget : REAL;             // Target X position
    YTarget : REAL;             // Target Y position
    ZTarget : REAL;             // Target Z position
    State : PlatformState;      // Current platform state
    LoadWeight : REAL;          // Current load weight (kg)
    VehicleSecured : BOOL;      // Vehicle properly secured
    LastCalibration : DATE_AND_TIME; // Last calibration
    FaultCode : INT;            // Current fault code
    Available : BOOL;           // Platform available
END_STRUCT;
END_TYPE;

// =============================================================================
// GLOBAL SYSTEM VARIABLES
// =============================================================================

VAR_GLOBAL
    // Parking space array (15 levels × 20 spaces = 300 total)
    ParkingSpaces : ARRAY[1..15, 1..20] OF ParkingSpace;
    
    // System statistics and monitoring
    SystemStats : SystemStatistics;
    
    // Equipment data
    Elevator1 : ElevatorData;
    Elevator2 : ElevatorData;
    Elevator3 : ElevatorData;
    Platform : PlatformData;
    
    // Current transaction
    CurrentTransaction : Transaction;
    TransactionCounter : DINT := 0;
    
    // System configuration
    MaxVehicleLength : REAL := 5200.0;     // mm
    MaxVehicleWidth : REAL := 2100.0;      // mm
    MaxVehicleHeight : REAL := 1800.0;     // mm
    MaxVehicleWeight : REAL := 3500.0;     // kg
    
    // Pricing structure
    HourlyRate : REAL := 2.50;             // Currency per hour
    DailyRate : REAL := 15.00;             // Currency per day
    MonthlyRate : REAL := 150.00;          // Currency per month
    
    // Operating parameters
    ElevatorSpeed : REAL := 2500.0;        // mm/s
    PlatformSpeed : REAL := 1500.0;        // mm/s
    PositioningTolerance : REAL := 5.0;    // mm
    
    // System timers and counters
    SystemStartTime : DATE_AND_TIME;
    LastTransactionTime : DATE_AND_TIME;
    NextMaintenanceTime : DATE_AND_TIME;
    
    // Queue management
    WaitingVehicles : INT := 0;
    MaxQueueLength : INT := 10;
    EstimatedWaitTime : TIME;
    
    // Performance monitoring
    SystemEfficiency : REAL;               // 0-100%
    EnergyConsumption : REAL;              // kWh
    ThroughputPerHour : REAL;              // vehicles/hour
    
    // Alarm and event logging
    AlarmBuffer : ARRAY[1..100] OF STRING[200];
    EventBuffer : ARRAY[1..1000] OF STRING[200];
    AlarmIndex : INT := 0;
    EventIndex : INT := 0;
    
    // Communication and networking
    HMI_Connected : BOOL := FALSE;
    Database_Connected : BOOL := FALSE;
    PaymentGateway_Connected : BOOL := FALSE;
    RemoteMonitoring_Connected : BOOL := FALSE;
    
    // Weather and environmental
    OutdoorTemperature : REAL;
    WindSpeed : REAL;
    RainIntensity : REAL;
    
END_VAR;

// =============================================================================
// SYSTEM CONSTANTS
// =============================================================================

VAR_GLOBAL CONSTANT
    SYSTEM_VERSION : STRING := '2.1.0';
    MAX_PARKING_LEVELS : INT := 15;
    SPACES_PER_LEVEL : INT := 20;
    TOTAL_PARKING_SPACES : INT := 300;
    
    // Safety limits
    MAX_ELEVATOR_SPEED : REAL := 3000.0;   // mm/s
    MAX_PLATFORM_SPEED : REAL := 2000.0;   // mm/s
    EMERGENCY_STOP_TIME : TIME := T#2s;
    
    // Operational timeouts
    PAYMENT_TIMEOUT : TIME := T#120s;
    ENTRY_TIMEOUT : TIME := T#60s;
    PARKING_TIMEOUT : TIME := T#300s;
    RETRIEVAL_TIMEOUT : TIME := T#300s;
    EXIT_TIMEOUT : TIME := T#90s;
    
    // Communication timeouts
    HMI_TIMEOUT : TIME := T#10s;
    DATABASE_TIMEOUT : TIME := T#30s;
    NETWORK_TIMEOUT : TIME := T#15s;
    
END_VAR;
