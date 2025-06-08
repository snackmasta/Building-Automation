FUNCTION_BLOCK PaymentController
VAR_INPUT
    ProcessPayment : BOOL;              // Start payment processing
    CustomerID : STRING[50];            // Customer identification
    RequestedDuration : TIME;           // Requested parking duration
    VehicleType : VehicleSize;          // Vehicle size category
    CancelPayment : BOOL;               // Cancel current transaction
END_VAR

VAR_OUTPUT
    PaymentComplete : BOOL;             // Payment successfully processed
    PaymentAmount : REAL;               // Total amount charged
    PaymentMethod : PaymentMethod;      // Method used for payment
    TransactionID : DINT;               // Unique transaction identifier
    ReceiptPrinted : BOOL;              // Receipt printing status
    Error : BOOL;                       // Payment error occurred
    ErrorCode : INT;                    // Payment error code
    TimeRemaining : TIME;               // Time remaining for payment
END_VAR

VAR
    // Payment state machine
    paymentState : INT := 0;
    stateTimer : TON;
    paymentTimer : TON;
    
    // Payment processing
    calculatedAmount : REAL;
    discountApplied : REAL := 0.0;
    taxAmount : REAL := 0.0;
    totalAmount : REAL;
    
    // Payment methods status
    cashAmount : REAL := 0.0;
    cardTransactionActive : BOOL := FALSE;
    rfidBalance : REAL := 0.0;
    mobilePaymentPending : BOOL := FALSE;
    
    // Customer interface
    displayMessage : STRING[100];
    keypadInput : STRING[20];
    selectedMethod : PaymentMethod := NONE;
    
    // Receipt and ticket data
    ticketData : TicketInfo;
    receiptData : ReceiptInfo;
    
    // Retry and timeout handling
    retryCount : INT := 0;
    maxRetries : INT := 3;
    paymentTimeout : TIME := T#120s;
    
    // Security and validation
    cardValidated : BOOL := FALSE;
    pinVerified : BOOL := FALSE;
    securityCode : STRING[10];
    
END_VAR

// Payment data structures
TYPE TicketInfo :
STRUCT
    TicketNumber : STRING[20];
    IssueTime : DATE_AND_TIME;
    ExpiryTime : DATE_AND_TIME;
    CustomerID : STRING[50];
    VehicleID : STRING[20];
    ParkingLevel : INT;
    ParkingPosition : INT;
    Amount : REAL;
    PaymentMethod : STRING[20];
    QRCode : STRING[100];
END_STRUCT;
END_TYPE;

TYPE ReceiptInfo :
STRUCT
    ReceiptNumber : STRING[20];
    TransactionTime : DATE_AND_TIME;
    MerchantID : STRING[20];
    Amount : REAL;
    Tax : REAL;
    Total : REAL;
    PaymentMethod : STRING[20];
    AuthorizationCode : STRING[20];
END_STRUCT;
END_TYPE;

// Initialize payment processing
IF ProcessPayment AND paymentState = 0 THEN
    paymentState := 10; // Start payment sequence
    paymentTimer(IN := TRUE, PT := paymentTimeout);
    TransactionCounter := TransactionCounter + 1;
    TransactionID := TransactionCounter;
    Error := FALSE;
    ErrorCode := 0;
    PaymentComplete := FALSE;
END_IF;

// Cancel payment if requested
IF CancelPayment THEN
    paymentState := 90; // Cancel state
    PaymentComplete := FALSE;
    Error := TRUE;
    ErrorCode := 4999; // Payment cancelled
END_IF;

// Payment timeout handling
paymentTimer(IN := paymentState > 0 AND paymentState < 80, PT := paymentTimeout);
TimeRemaining := paymentTimeout - paymentTimer.ET;

IF paymentTimer.Q AND paymentState > 0 AND paymentState < 80 THEN
    paymentState := 91; // Timeout state
    Error := TRUE;
    ErrorCode := 4001; // Payment timeout
END_IF;

// Main payment state machine
CASE paymentState OF
    
    0: // IDLE
        PaymentComplete := FALSE;
        Error := FALSE;
        displayMessage := 'System Ready';
    
    // =============================================================================
    // PAYMENT INITIALIZATION (States 10-19)
    // =============================================================================
    
    10: // CALCULATE_AMOUNT
        displayMessage := 'Calculating parking fee...';
        
        // Base calculation on duration and vehicle type
        IF RequestedDuration <= T#1h THEN
            calculatedAmount := HourlyRate;
        ELSIF RequestedDuration <= T#24h THEN
            calculatedAmount := REAL_TO_TIME(RequestedDuration) / 3600000.0 * HourlyRate;
            IF calculatedAmount > DailyRate THEN
                calculatedAmount := DailyRate; // Daily rate cap
            END_IF;
        ELSE
            calculatedAmount := DailyRate * (REAL_TO_TIME(RequestedDuration) / 86400000.0);
            IF calculatedAmount > MonthlyRate THEN
                calculatedAmount := MonthlyRate; // Monthly rate cap
            END_IF;
        END_IF;
        
        // Vehicle type surcharge
        CASE VehicleType OF
            COMPACT: calculatedAmount := calculatedAmount * 0.9; // 10% discount
            STANDARD: ; // No change
            SUV: calculatedAmount := calculatedAmount * 1.2; // 20% surcharge
            MOTORCYCLE: calculatedAmount := calculatedAmount * 0.5; // 50% discount
        END_CASE;
        
        // Apply any customer discounts
        IF CheckCustomerDiscounts(CustomerID) THEN
            discountApplied := calculatedAmount * 0.1; // 10% member discount
            calculatedAmount := calculatedAmount - discountApplied;
        END_IF;
        
        // Calculate tax
        taxAmount := calculatedAmount * 0.08; // 8% tax
        totalAmount := calculatedAmount + taxAmount;
        PaymentAmount := totalAmount;
        
        paymentState := 11;
    
    11: // DISPLAY_AMOUNT_AND_OPTIONS
        displayMessage := 'Amount: $' + REAL_TO_STRING(totalAmount, 2) + 
                         ' - Select payment method';
        
        // Wait for payment method selection
        stateTimer(IN := TRUE, PT := T#30s);
        
        IF I_CashInserted THEN
            selectedMethod := CASH;
            paymentState := 20; // Cash payment
            stateTimer(IN := FALSE);
        ELSIF I_CardInserted THEN
            selectedMethod := CREDIT_CARD;
            paymentState := 30; // Card payment
            stateTimer(IN := FALSE);
        ELSIF I_RFIDCardPresent THEN
            selectedMethod := RFID_CARD;
            paymentState := 40; // RFID payment
            stateTimer(IN := FALSE);
        ELSIF I_QRCodeScanned THEN
            selectedMethod := MOBILE_APP;
            paymentState := 50; // Mobile payment
            stateTimer(IN := FALSE);
        ELSIF stateTimer.Q THEN
            paymentState := 91; // Selection timeout
            ErrorCode := 4002;
            stateTimer(IN := FALSE);
        END_IF;
    
    // =============================================================================
    // CASH PAYMENT (States 20-29)
    // =============================================================================
    
    20: // PROCESS_CASH_PAYMENT
        displayMessage := 'Insert cash: $' + REAL_TO_STRING(totalAmount, 2);
        PaymentMethod := CASH;
        
        stateTimer(IN := TRUE, PT := T#60s);
        
        // Simulate cash counting (in real system, would interface with bill acceptor)
        cashAmount := GetCashAmount();
        
        IF cashAmount >= totalAmount THEN
            paymentState := 21; // Sufficient cash received
            stateTimer(IN := FALSE);
        ELSIF stateTimer.Q THEN
            paymentState := 92; // Cash timeout
            ErrorCode := 4003;
            stateTimer(IN := FALSE);
        END_IF;
    
    21: // CALCULATE_CHANGE
        displayMessage := 'Processing cash payment...';
        
        IF cashAmount > totalAmount THEN
            // Dispense change
            Q_CashDispenser_Enable := TRUE;
            stateTimer(IN := TRUE, PT := T#10s);
            
            IF stateTimer.Q THEN
                displayMessage := 'Change dispensed: $' + 
                                REAL_TO_STRING(cashAmount - totalAmount, 2);
                paymentState := 70; // Payment complete
                stateTimer(IN := FALSE);
            END_IF;
        ELSE
            paymentState := 70; // Exact change
        END_IF;
    
    // =============================================================================
    // CREDIT/DEBIT CARD PAYMENT (States 30-39)
    // =============================================================================
    
    30: // PROCESS_CARD_PAYMENT
        displayMessage := 'Processing card...';
        PaymentMethod := CREDIT_CARD;
        
        Q_CardReader_Enable := TRUE;
        cardTransactionActive := TRUE;
        
        stateTimer(IN := TRUE, PT := T#30s);
        
        // Simulate card validation
        IF ValidateCard() THEN
            paymentState := 31;
            stateTimer(IN := FALSE);
        ELSIF stateTimer.Q THEN
            paymentState := 93; // Card timeout
            ErrorCode := 4004;
            stateTimer(IN := FALSE);
        END_IF;
    
    31: // REQUEST_PIN
        displayMessage := 'Enter PIN';
        
        stateTimer(IN := TRUE, PT := T#60s);
        
        // Get PIN from keypad (simulated)
        IF GetPINInput() THEN
            IF VerifyPIN() THEN
                paymentState := 32;
                stateTimer(IN := FALSE);
            ELSE
                retryCount := retryCount + 1;
                IF retryCount >= maxRetries THEN
                    paymentState := 94; // PIN failed
                    ErrorCode := 4005;
                ELSE
                    displayMessage := 'Incorrect PIN - Try again';
                END_IF;
            END_IF;
        ELSIF stateTimer.Q THEN
            paymentState := 93; // PIN timeout
            ErrorCode := 4006;
            stateTimer(IN := FALSE);
        END_IF;
    
    32: // AUTHORIZE_TRANSACTION
        displayMessage := 'Authorizing transaction...';
        
        stateTimer(IN := TRUE, PT := T#20s);
        
        // Simulate bank authorization
        IF AuthorizeCardTransaction(totalAmount) THEN
            receiptData.AuthorizationCode := GenerateAuthCode();
            paymentState := 70; // Payment approved
            stateTimer(IN := FALSE);
        ELSIF stateTimer.Q THEN
            paymentState := 95; // Authorization failed
            ErrorCode := 4007;
            stateTimer(IN := FALSE);
        END_IF;
    
    // =============================================================================
    // RFID CARD PAYMENT (States 40-49)
    // =============================================================================
    
    40: // PROCESS_RFID_PAYMENT
        displayMessage := 'Reading RFID card...';
        PaymentMethod := RFID_CARD;
        
        stateTimer(IN := TRUE, PT := T#10s);
        
        // Read RFID card balance
        rfidBalance := GetRFIDBalance(CustomerID);
        
        IF rfidBalance >= totalAmount THEN
            paymentState := 41;
            stateTimer(IN := FALSE);
        ELSIF stateTimer.Q THEN
            paymentState := 96; // Insufficient RFID balance
            ErrorCode := 4008;
            stateTimer(IN := FALSE);
        END_IF;
    
    41: // DEDUCT_RFID_BALANCE
        displayMessage := 'Deducting from RFID card...';
        
        stateTimer(IN := TRUE, PT := T#5s);
        
        IF DeductRFIDBalance(CustomerID, totalAmount) THEN
            paymentState := 70; // Payment complete
            stateTimer(IN := FALSE);
        ELSE
            paymentState := 97; // RFID deduction failed
            ErrorCode := 4009;
            stateTimer(IN := FALSE);
        END_IF;
    
    // =============================================================================
    // MOBILE/QR CODE PAYMENT (States 50-59)
    // =============================================================================
    
    50: // PROCESS_MOBILE_PAYMENT
        displayMessage := 'Processing mobile payment...';
        PaymentMethod := MOBILE_APP;
        
        mobilePaymentPending := TRUE;
        stateTimer(IN := TRUE, PT := T#45s);
        
        // Wait for mobile payment confirmation
        IF CheckMobilePaymentStatus() THEN
            paymentState := 70; // Payment confirmed
            stateTimer(IN := FALSE);
        ELSIF stateTimer.Q THEN
            paymentState := 98; // Mobile payment timeout
            ErrorCode := 4010;
            stateTimer(IN := FALSE);
        END_IF;
    
    // =============================================================================
    // PAYMENT COMPLETION (States 70-79)
    // =============================================================================
    
    70: // PAYMENT_SUCCESSFUL
        displayMessage := 'Payment approved - Printing ticket...';
        
        // Generate parking ticket
        GenerateTicket();
        
        // Print ticket
        IF I_TicketPrinter_Ready AND I_TicketPrinter_PaperOK THEN
            Q_TicketPrinter_Print := TRUE;
            paymentState := 71;
        ELSE
            paymentState := 99; // Printer error
            ErrorCode := 4011;
        END_IF;
    
    71: // PRINT_RECEIPT
        displayMessage := 'Printing receipt...';
        
        // Generate receipt
        GenerateReceipt();
        
        stateTimer(IN := TRUE, PT := T#10s);
        
        IF I_ReceiptPrinter_Ready THEN
            Q_ReceiptPrinter_Print := TRUE;
            ReceiptPrinted := TRUE;
            paymentState := 72;
            stateTimer(IN := FALSE);
        ELSIF stateTimer.Q THEN
            // Continue without receipt if printer fails
            ReceiptPrinted := FALSE;
            paymentState := 72;
            stateTimer(IN := FALSE);
        END_IF;
    
    72: // UPDATE_TRANSACTION_RECORD
        displayMessage := 'Transaction complete';
        
        // Update current transaction
        CurrentTransaction.TransactionID := TransactionID;
        CurrentTransaction.Timestamp := GetSystemTime();
        CurrentTransaction.CustomerID := CustomerID;
        CurrentTransaction.PaymentMethod := selectedMethod;
        CurrentTransaction.Amount := totalAmount;
        CurrentTransaction.ParkingDuration := RequestedDuration;
        CurrentTransaction.Status := 'PAID';
        
        // Update system statistics
        SystemStats.TotalRevenue := SystemStats.TotalRevenue + totalAmount;
        
        PaymentComplete := TRUE;
        paymentState := 0; // Return to idle
        
        // Log successful payment
        LogEvent('PAYMENT_SUCCESS', 'Customer: ' + CustomerID + 
                 ', Amount: $' + REAL_TO_STRING(totalAmount, 2) + 
                 ', Method: ' + PaymentMethodToString(selectedMethod));
    
    // =============================================================================
    // ERROR STATES (States 90-99)
    // =============================================================================
    
    90: // PAYMENT_CANCELLED
        displayMessage := 'Payment cancelled';
        Error := TRUE;
        PaymentComplete := FALSE;
        
        // Refund any partial payments
        IF selectedMethod = CASH AND cashAmount > 0 THEN
            Q_CashDispenser_Enable := TRUE; // Return cash
        END_IF;
        
        stateTimer(IN := TRUE, PT := T#5s);
        IF stateTimer.Q THEN
            paymentState := 0; // Return to idle
            stateTimer(IN := FALSE);
        END_IF;
    
    91: // PAYMENT_TIMEOUT
        displayMessage := 'Payment timeout - Please try again';
        Error := TRUE;
        PaymentComplete := FALSE;
        
        stateTimer(IN := TRUE, PT := T#10s);
        IF stateTimer.Q THEN
            paymentState := 0;
            stateTimer(IN := FALSE);
        END_IF;
    
    92: // CASH_TIMEOUT
        displayMessage := 'Cash insertion timeout';
        Error := TRUE;
        
        // Return any inserted cash
        IF cashAmount > 0 THEN
            Q_CashDispenser_Enable := TRUE;
        END_IF;
        
        stateTimer(IN := TRUE, PT := T#10s);
        IF stateTimer.Q THEN
            paymentState := 0;
            stateTimer(IN := FALSE);
        END_IF;
    
    93: // CARD_ERROR
        displayMessage := 'Card error - Please try again';
        Error := TRUE;
        cardTransactionActive := FALSE;
        Q_CardReader_Enable := FALSE;
        
        stateTimer(IN := TRUE, PT := T#10s);
        IF stateTimer.Q THEN
            paymentState := 0;
            stateTimer(IN := FALSE);
        END_IF;
    
    94: // PIN_ERROR
        displayMessage := 'PIN verification failed';
        Error := TRUE;
        cardTransactionActive := FALSE;
        
        stateTimer(IN := TRUE, PT := T#10s);
        IF stateTimer.Q THEN
            paymentState := 0;
            retryCount := 0;
            stateTimer(IN := FALSE);
        END_IF;
    
    95: // AUTHORIZATION_FAILED
        displayMessage := 'Transaction declined';
        Error := TRUE;
        cardTransactionActive := FALSE;
        
        stateTimer(IN := TRUE, PT := T#10s);
        IF stateTimer.Q THEN
            paymentState := 0;
            stateTimer(IN := FALSE);
        END_IF;
    
    96: // INSUFFICIENT_RFID_BALANCE
        displayMessage := 'Insufficient card balance: $' + REAL_TO_STRING(rfidBalance, 2);
        Error := TRUE;
        
        stateTimer(IN := TRUE, PT := T#10s);
        IF stateTimer.Q THEN
            paymentState := 0;
            stateTimer(IN := FALSE);
        END_IF;
    
    97: // RFID_ERROR
        displayMessage := 'RFID card error';
        Error := TRUE;
        
        stateTimer(IN := TRUE, PT := T#10s);
        IF stateTimer.Q THEN
            paymentState := 0;
            stateTimer(IN := FALSE);
        END_IF;
    
    98: // MOBILE_PAYMENT_ERROR
        displayMessage := 'Mobile payment failed';
        Error := TRUE;
        mobilePaymentPending := FALSE;
        
        stateTimer(IN := TRUE, PT := T#10s);
        IF stateTimer.Q THEN
            paymentState := 0;
            stateTimer(IN := FALSE);
        END_IF;
    
    99: // PRINTER_ERROR
        displayMessage := 'Printer error - Payment successful';
        Error := FALSE; // Payment was successful, just printer issue
        PaymentComplete := TRUE;
        
        stateTimer(IN := TRUE, PT := T#5s);
        IF stateTimer.Q THEN
            paymentState := 0;
            stateTimer(IN := FALSE);
        END_IF;

END_CASE;

// ============================================================================
// HELPER FUNCTIONS
// ============================================================================

FUNCTION GenerateTicket : BOOL
ticketData.TicketNumber := 'PKT' + INT_TO_STRING(TransactionID);
ticketData.IssueTime := GetSystemTime();
ticketData.ExpiryTime := ticketData.IssueTime + RequestedDuration;
ticketData.CustomerID := CustomerID;
ticketData.Amount := totalAmount;
ticketData.PaymentMethod := PaymentMethodToString(selectedMethod);
ticketData.QRCode := GenerateQRCode(ticketData.TicketNumber);
GenerateTicket := TRUE;
END_FUNCTION;

FUNCTION GenerateReceipt : BOOL
receiptData.ReceiptNumber := 'RCP' + INT_TO_STRING(TransactionID);
receiptData.TransactionTime := GetSystemTime();
receiptData.MerchantID := 'PARK001';
receiptData.Amount := calculatedAmount;
receiptData.Tax := taxAmount;
receiptData.Total := totalAmount;
receiptData.PaymentMethod := PaymentMethodToString(selectedMethod);
GenerateReceipt := TRUE;
END_FUNCTION;

FUNCTION PaymentMethodToString : STRING
CASE selectedMethod OF
    CASH: PaymentMethodToString := 'CASH';
    CREDIT_CARD: PaymentMethodToString := 'CREDIT CARD';
    RFID_CARD: PaymentMethodToString := 'RFID CARD';
    MOBILE_APP: PaymentMethodToString := 'MOBILE APP';
    QR_CODE: PaymentMethodToString := 'QR CODE';
    ELSE: PaymentMethodToString := 'UNKNOWN';
END_CASE;
END_FUNCTION;

// Clean up on completion
IF paymentState = 0 THEN
    Q_TicketPrinter_Print := FALSE;
    Q_ReceiptPrinter_Print := FALSE;
    Q_CashDispenser_Enable := FALSE;
    Q_CardReader_Enable := FALSE;
    cashAmount := 0.0;
    cardTransactionActive := FALSE;
    mobilePaymentPending := FALSE;
    selectedMethod := NONE;
END_IF;

END_FUNCTION_BLOCK
