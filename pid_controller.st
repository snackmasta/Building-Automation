FUNCTION_BLOCK PID_Controller
VAR_INPUT
    SetPoint    : REAL;     // Desired value
    ProcessVar  : REAL;     // Current process value
    Enable      : BOOL;     // Enable PID control
    Reset       : BOOL;     // Reset integral term
END_VAR

VAR_OUTPUT
    Output      : REAL;     // Control output (0-100%)
    Error       : REAL;     // Current error value
END_VAR

VAR
    // PID parameters
    Kp          : REAL := 1.0;      // Proportional gain
    Ki          : REAL := 0.1;      // Integral gain  
    Kd          : REAL := 0.05;     // Derivative gain
    
    // Internal variables
    LastError   : REAL := 0.0;      // Previous error for derivative
    Integral    : REAL := 0.0;      // Integral accumulator
    Derivative  : REAL := 0.0;      // Derivative term
    
    // Limits
    OutputMin   : REAL := 0.0;      // Minimum output
    OutputMax   : REAL := 100.0;    // Maximum output
    IntegralMax : REAL := 50.0;     // Integral windup limit
    
    FirstScan   : BOOL := TRUE;     // First execution flag
END_VAR

// ===============================================
// PID CONTROLLER IMPLEMENTATION
// ===============================================

IF Enable THEN
    // Calculate error
    Error := SetPoint - ProcessVar;
    
    // Reset integral if requested
    IF Reset THEN
        Integral := 0.0;
        LastError := 0.0;
        FirstScan := TRUE;
    END_IF;
    
    // Proportional term
    // P = Kp * Error
    
    // Integral term with windup protection
    Integral := Integral + (Error * Ki);
    IF Integral > IntegralMax THEN
        Integral := IntegralMax;
    ELSIF Integral < -IntegralMax THEN
        Integral := -IntegralMax;
    END_IF;
    
    // Derivative term (avoid derivative kick on first scan)
    IF NOT FirstScan THEN
        Derivative := Kd * (Error - LastError);
    ELSE
        Derivative := 0.0;
        FirstScan := FALSE;
    END_IF;
    
    // Calculate PID output
    Output := (Kp * Error) + Integral + Derivative;
    
    // Apply output limits
    IF Output > OutputMax THEN
        Output := OutputMax;
    ELSIF Output < OutputMin THEN
        Output := OutputMin;
    END_IF;
    
    // Store error for next cycle
    LastError := Error;
    
ELSE
    // PID disabled - reset all terms
    Output := 0.0;
    Error := 0.0;
    Integral := 0.0;
    Derivative := 0.0;
    LastError := 0.0;
    FirstScan := TRUE;
END_IF;

END_FUNCTION_BLOCK
