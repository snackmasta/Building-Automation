# HMI Development Guide

## Overview

This guide provides comprehensive instructions for developing Human-Machine Interfaces (HMI) for industrial automation systems. From basic operator panels to advanced SCADA systems, learn best practices for creating intuitive, efficient, and safe user interfaces.

## 📚 Table of Contents

1. [HMI Fundamentals](#hmi-fundamentals)
2. [Design Principles](#design-principles)
3. [Development Platforms](#development-platforms)
4. [Screen Design](#screen-design)
5. [Data Integration](#data-integration)
6. [Security & Access Control](#security--access-control)
7. [Testing & Validation](#testing--validation)

## 🖥️ HMI Fundamentals

### Purpose and Function
HMI systems serve as the critical interface between human operators and automated processes, providing:

- **Real-time Process Visualization**: Current status and trends
- **Operator Control**: Manual intervention capabilities
- **Alarm Management**: Fault detection and notification
- **Data Logging**: Historical records and reporting
- **System Configuration**: Parameter adjustment and tuning

### HMI Architecture Levels

#### Level 1: Basic Operator Interface
**Used in**: Project Example
```
Features:
├── Simple start/stop controls
├── Basic status indicators
├── Essential alarm display
└── Manual mode operations
```

#### Level 2: Process Visualization
**Used in**: HVAC System
```
Features:
├── Multi-zone system overview
├── Trend displays for key parameters
├── Recipe management
├── Energy monitoring dashboards
└── Maintenance scheduling
```

#### Level 3: Advanced SCADA
**Used in**: Water Treatment System
```
Features:
├── Plant-wide system integration
├── Advanced analytics and reporting
├── Regulatory compliance tools
├── Remote monitoring capabilities
└── Predictive maintenance features
```

## 🎨 Design Principles

### User Experience (UX) Best Practices

#### Information Hierarchy
```
Priority Level 1: Safety Information
├── Emergency stops
├── Critical alarms
├── Safety system status
└── Lockout/tagout status

Priority Level 2: Process Control
├── Primary process variables
├── Control loop status
├── Equipment operation modes
└── Production targets

Priority Level 3: Supporting Information
├── Historical trends
├── Maintenance data
├── Statistical reports
└── Configuration settings
```

#### Cognitive Load Management
- **7±2 Rule**: Limit screen elements to 5-9 items
- **Consistent Navigation**: Same controls in same locations
- **Progressive Disclosure**: Show details on demand
- **Contextual Information**: Relevant data for current task

### Visual Design Standards

#### Color Coding System
```css
/* Standard Industrial Color Scheme */
Safety Colors:
├── Red: Emergency, danger, stop
├── Yellow: Caution, warning, attention
├── Green: Safe, normal, go
└── Blue: Information, mandatory action

Process Colors:
├── Light Blue: Water, cooling
├── Orange: Heat, steam
├── Purple: Electrical
└── Brown: Raw materials
```

#### Typography Guidelines
- **Primary Text**: 12-14pt for main content
- **Labels**: 10-12pt for field labels
- **Alarms**: 14-16pt bold for critical messages
- **Font Family**: Sans-serif (Arial, Calibri) for readability

### Responsive Design

#### Multiple Screen Sizes
```
Screen Categories:
├── Compact HMI: 7-10 inch (800x480 - 1024x600)
├── Standard Panel: 12-15 inch (1280x800 - 1920x1080)
├── Large Display: 19-24 inch (1920x1080 - 2560x1440)
└── Control Room: Multi-monitor (custom resolutions)
```

## 🛠️ Development Platforms

### Schneider Electric EcoStruxure Machine Expert

#### Project Setup
```
HMI Project Structure:
├── Screens/
│   ├── Main.fhx           # Primary overview
│   ├── Alarms.fhx         # Alarm summary
│   ├── Trends.fhx         # Historical data
│   └── Settings.fhx       # Configuration
├── Graphics/
│   ├── Symbols/           # Custom graphics
│   ├── Backgrounds/       # Screen templates
│   └── Icons/            # Status indicators
└── Scripts/
    ├── Navigation.st      # Screen transitions
    ├── DataLogging.st     # Historical recording
    └── Calculations.st    # Display calculations
```

#### Built-in Features
- **Drag-and-Drop Design**: Visual screen builder
- **Symbol Library**: Pre-built industrial graphics
- **Animation Objects**: Dynamic status indication
- **Recipe Management**: Parameter sets for different products
- **Alarm System**: Built-in alarm handling

### Siemens WinCC Professional

#### Advanced Capabilities
```
WinCC Features:
├── Faceplates: Reusable control elements
├── VB Scripting: Custom functionality
├── OPC Connectivity: Third-party integration
├── Web Publishing: Remote browser access
└── ProcessHistorian: Enterprise data archiving
```

#### Project Architecture
```pascal
// Global script for data calculations
Sub CalculateEfficiency()
    Dim flow As Double
    Dim power As Double
    Dim efficiency As Double
    
    flow = HMIRuntime.Tags("FlowRate").Read
    power = HMIRuntime.Tags("PowerConsumption").Read
    
    If power > 0 Then
        efficiency = (flow * 0.5) / power * 100
        HMIRuntime.Tags("Efficiency").Write efficiency
    End If
End Sub
```

### Open Source Alternatives

#### AdvancedHMI (VB.NET)
- Free development platform
- Visual Studio integration
- Extensive driver library
- Active community support

#### Ignition by Inductive Automation
- Web-based architecture
- Unlimited licensing model
- Built-in historian
- Mobile-responsive design

## 📱 Screen Design

### Main Overview Screen

#### Essential Elements
```
Main Screen Layout:
├── Header: System title, time, user login
├── Navigation: Quick access to major screens
├── Process Overview: High-level system status
├── Key Metrics: Critical process variables
├── Alarm Summary: Active alarm count/priority
└── Footer: System mode, communication status
```

#### Example Implementation
```html
<!-- Main Process Overview -->
<Screen Name="MainOverview" Size="1280x800">
    <!-- Header Section -->
    <Rectangle Fill="DarkBlue" Height="60">
        <Text Content="Water Treatment Plant" Color="White" FontSize="18"/>
        <Text Content="{DateTime}" Color="White" FontSize="12" HAlign="Right"/>
    </Rectangle>
    
    <!-- Process Flow Diagram -->
    <ProcessFlow X="50" Y="100" Width="900" Height="500">
        <Tank Name="RawWater" Level="{RawWaterLevel}" Color="LightBlue"/>
        <Pump Name="FeedPump" Running="{FeedPumpStatus}" Color="Green"/>
        <Filter Name="SandFilter" Backwash="{BackwashActive}" Color="Brown"/>
        <Tank Name="ClearWell" Level="{ClearWellLevel}" Color="Blue"/>
    </ProcessFlow>
    
    <!-- Key Performance Indicators -->
    <KPIPanel X="1000" Y="100" Width="250" Height="300">
        <Metric Label="Flow Rate" Value="{FlowRate}" Units="L/min"/>
        <Metric Label="Turbidity" Value="{Turbidity}" Units="NTU"/>
        <Metric Label="Pressure" Value="{Pressure}" Units="bar"/>
        <Metric Label="Efficiency" Value="{Efficiency}" Units="%"/>
    </KPIPanel>
</Screen>
```

### Alarm Management Screen

#### ISA-18.2 Compliance
```
Alarm Management Features:
├── Priority-based sorting (Critical, High, Medium, Low)
├── Time-stamped event logging
├── Operator acknowledgment tracking
├── Alarm filtering and grouping
└── Statistical analysis and reporting
```

#### Alarm Display Design
```javascript
// JavaScript for alarm handling
function UpdateAlarmList() {
    const alarms = GetActiveAlarms();
    const alarmTable = document.getElementById('alarmTable');
    
    // Clear existing rows
    alarmTable.innerHTML = '';
    
    // Sort by priority and timestamp
    alarms.sort((a, b) => {
        if (a.priority !== b.priority) {
            return a.priority - b.priority; // Higher priority first
        }
        return new Date(b.timestamp) - new Date(a.timestamp);
    });
    
    // Populate alarm table
    alarms.forEach(alarm => {
        const row = alarmTable.insertRow();
        row.className = `alarm-${alarm.priority}`;
        
        row.insertCell(0).textContent = alarm.timestamp;
        row.insertCell(1).textContent = alarm.description;
        row.insertCell(2).textContent = alarm.area;
        row.insertCell(3).innerHTML = `<button onclick="AckAlarm(${alarm.id})">ACK</button>`;
    });
}
```

### Trend Visualization

#### Real-time Trending
```
Trend Display Options:
├── Multiple pen configuration
├── Auto-scaling Y-axis
├── Time range selection
├── Data sampling rates
├── Export capabilities
└── Annotation support
```

#### Implementation Example
```python
# Python script for trend data processing
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime, timedelta

class TrendDisplay:
    def __init__(self):
        self.data_buffer = {}
        self.max_points = 1000
    
    def add_data_point(self, tag_name, value, timestamp=None):
        if timestamp is None:
            timestamp = datetime.now()
        
        if tag_name not in self.data_buffer:
            self.data_buffer[tag_name] = {'time': [], 'value': []}
        
        self.data_buffer[tag_name]['time'].append(timestamp)
        self.data_buffer[tag_name]['value'].append(value)
        
        # Maintain buffer size
        if len(self.data_buffer[tag_name]['time']) > self.max_points:
            self.data_buffer[tag_name]['time'].pop(0)
            self.data_buffer[tag_name]['value'].pop(0)
    
    def generate_trend_chart(self, tag_names, time_range_hours=1):
        plt.figure(figsize=(12, 6))
        
        end_time = datetime.now()
        start_time = end_time - timedelta(hours=time_range_hours)
        
        for tag_name in tag_names:
            if tag_name in self.data_buffer:
                df = pd.DataFrame(self.data_buffer[tag_name])
                df = df[(df['time'] >= start_time) & (df['time'] <= end_time)]
                plt.plot(df['time'], df['value'], label=tag_name)
        
        plt.xlabel('Time')
        plt.ylabel('Value')
        plt.title(f'Process Trends - Last {time_range_hours} Hour(s)')
        plt.legend()
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        return plt
```

## 🔗 Data Integration

### PLC Communication

#### Tag Configuration
```pascal
// PLC tag structure for HMI integration
TYPE HMI_Data_Exchange : STRUCT
    // Process Variables
    Temperature : REAL;
    Pressure : REAL;
    FlowRate : REAL;
    Level : REAL;
    
    // Equipment Status
    PumpRunning : BOOL;
    ValvePosition : REAL;
    MotorSpeed : REAL;
    
    // Alarms and Events
    HighTempAlarm : BOOL;
    LowPressureAlarm : BOOL;
    EquipmentFault : BOOL;
    
    // Commands from HMI
    StartCommand : BOOL;
    StopCommand : BOOL;
    SetpointValue : REAL;
    ModeSelection : INT;
END_STRUCT;

VAR_GLOBAL
    gHMI_Data : HMI_Data_Exchange;
END_VAR
```

#### Data Refresh Strategies
```
Update Frequencies:
├── Critical Data: 100-250ms (safety, alarms)
├── Process Data: 500ms-1s (temperatures, pressures)
├── Status Data: 1-2s (equipment states)
├── Trending Data: 5-30s (historical logging)
└── Configuration: On-demand (setpoints, parameters)
```

### Database Integration

#### Historical Data Storage
```sql
-- SQL table structure for process data
CREATE TABLE ProcessData (
    Timestamp DATETIME PRIMARY KEY,
    TagName VARCHAR(50) NOT NULL,
    Value FLOAT NOT NULL,
    Quality INT DEFAULT 100,
    Units VARCHAR(20),
    Area VARCHAR(30)
);

-- Create indexes for performance
CREATE INDEX IX_ProcessData_Tag_Time ON ProcessData(TagName, Timestamp);
CREATE INDEX IX_ProcessData_Time ON ProcessData(Timestamp);

-- Sample query for trend data
SELECT 
    Timestamp,
    AVG(Value) as AvgValue,
    MIN(Value) as MinValue,
    MAX(Value) as MaxValue
FROM ProcessData 
WHERE TagName = 'Temperature_01' 
    AND Timestamp >= DATEADD(hour, -24, GETDATE())
GROUP BY DATEPART(hour, Timestamp)
ORDER BY Timestamp;
```

### Recipe Management

#### Recipe Data Structure
```json
{
  "recipeId": "BATCH_001",
  "recipeName": "Standard Water Treatment",
  "version": "1.2",
  "created": "2024-01-15T10:30:00Z",
  "parameters": [
    {
      "name": "ChlorineSetpoint",
      "value": 2.5,
      "units": "mg/L",
      "min": 1.0,
      "max": 5.0
    },
    {
      "name": "pHSetpoint",
      "value": 7.2,
      "units": "pH",
      "min": 6.5,
      "max": 8.5
    },
    {
      "name": "FilterBackwashTime",
      "value": 300,
      "units": "seconds",
      "min": 180,
      "max": 600
    }
  ],
  "procedures": [
    {
      "step": 1,
      "description": "Initialize filtration system",
      "duration": 120,
      "actions": ["OpenInletValve", "StartFeedPump"]
    },
    {
      "step": 2,
      "description": "Begin chemical dosing",
      "duration": 0,
      "actions": ["EnableChlorinePump", "EnablePHControl"]
    }
  ]
}
```

## 🔒 Security & Access Control

### User Management

#### Role-Based Access Control (RBAC)
```
User Hierarchy:
├── Operator Level 1: View only, acknowledge alarms
├── Operator Level 2: Manual control, parameter adjustment
├── Supervisor: Recipe changes, system configuration
├── Engineer: Full access, programming changes
└── Administrator: User management, security settings
```

#### Implementation Example
```csharp
// C# example for user authentication
public class UserManager
{
    private Dictionary<string, User> users;
    private User currentUser;
    
    public bool AuthenticateUser(string username, string password)
    {
        if (users.ContainsKey(username))
        {
            var user = users[username];
            if (user.VerifyPassword(password))
            {
                currentUser = user;
                LogUserActivity($"User {username} logged in");
                return true;
            }
        }
        
        LogSecurityEvent($"Failed login attempt for {username}");
        return false;
    }
    
    public bool HasPermission(string action)
    {
        if (currentUser == null) return false;
        
        return currentUser.Role.Permissions.Contains(action);
    }
    
    public void LogUserActivity(string activity)
    {
        var logEntry = new AuditLogEntry
        {
            Timestamp = DateTime.Now,
            UserId = currentUser?.UserId,
            Activity = activity,
            IPAddress = GetClientIPAddress()
        };
        
        SecurityLogger.Log(logEntry);
    }
}

public enum UserRole
{
    Operator = 1,
    Supervisor = 2,
    Engineer = 3,
    Administrator = 4
}
```

### Data Protection

#### Secure Communication
```
Security Measures:
├── Encrypted communication channels (TLS 1.2+)
├── Certificate-based authentication
├── VPN access for remote connections
├── Network segmentation (industrial DMZ)
└── Regular security updates and patches
```

#### Audit Logging
```sql
-- Audit log table structure
CREATE TABLE SecurityAuditLog (
    LogId BIGINT IDENTITY(1,1) PRIMARY KEY,
    Timestamp DATETIME2 DEFAULT GETDATE(),
    UserId VARCHAR(50),
    Action VARCHAR(100),
    TargetObject VARCHAR(100),
    SourceIP VARCHAR(45),
    Success BIT,
    Details NVARCHAR(MAX)
);

-- Example log entries
INSERT INTO SecurityAuditLog (UserId, Action, TargetObject, SourceIP, Success, Details)
VALUES 
    ('operator1', 'LOGIN', 'HMI_System', '192.168.1.100', 1, 'Successful login from operator workstation'),
    ('engineer2', 'SETPOINT_CHANGE', 'Temperature_Controller', '192.168.1.105', 1, 'Changed setpoint from 75°C to 80°C'),
    ('unknown', 'LOGIN_ATTEMPT', 'HMI_System', '10.0.0.50', 0, 'Failed login attempt with invalid credentials');
```

## ✅ Testing & Validation

### Functional Testing

#### Test Case Categories
```
Testing Framework:
├── Unit Tests: Individual screen functionality
├── Integration Tests: PLC-HMI communication
├── User Acceptance Tests: Operator workflow validation
├── Performance Tests: Response time and load testing
└── Security Tests: Access control and data protection
```

#### Test Procedure Example
```yaml
# Test case specification
TestCase: TC_001_Main_Screen_Navigation
Description: Verify main screen navigation buttons work correctly
Preconditions:
  - HMI system powered on
  - Valid user logged in
  - PLC communication established

Steps:
  1. Display main overview screen
  2. Click "Alarms" navigation button
  3. Verify alarm screen displays
  4. Click "Trends" navigation button
  5. Verify trend screen displays
  6. Click "Settings" navigation button
  7. Verify settings screen displays (if user has permission)

Expected Results:
  - All navigation buttons respond within 1 second
  - Correct screens display for each button
  - Access control respected for restricted screens
  - No error messages or system faults
```

### Performance Validation

#### Response Time Testing
```python
# Python script for HMI performance testing
import time
import requests
import statistics

class HMIPerformanceTest:
    def __init__(self, hmi_ip, test_duration=300):
        self.hmi_ip = hmi_ip
        self.test_duration = test_duration
        self.response_times = []
    
    def test_screen_load_time(self, screen_name):
        start_time = time.time()
        
        # Simulate screen request
        response = requests.get(f"http://{self.hmi_ip}/screens/{screen_name}")
        
        end_time = time.time()
        response_time = (end_time - start_time) * 1000  # Convert to milliseconds
        
        self.response_times.append(response_time)
        return response_time
    
    def run_performance_test(self):
        screens = ['main', 'alarms', 'trends', 'settings']
        start_test = time.time()
        
        while (time.time() - start_test) < self.test_duration:
            for screen in screens:
                response_time = self.test_screen_load_time(screen)
                print(f"Screen {screen}: {response_time:.2f}ms")
                time.sleep(1)  # Wait between requests
        
        # Calculate statistics
        avg_response = statistics.mean(self.response_times)
        max_response = max(self.response_times)
        min_response = min(self.response_times)
        
        print(f"\nPerformance Test Results:")
        print(f"Average Response Time: {avg_response:.2f}ms")
        print(f"Maximum Response Time: {max_response:.2f}ms")
        print(f"Minimum Response Time: {min_response:.2f}ms")
        print(f"Total Requests: {len(self.response_times)}")
        
        # Check against requirements
        if avg_response <= 1000:  # 1 second requirement
            print("✅ Performance test PASSED")
        else:
            print("❌ Performance test FAILED")
```

### Usability Testing

#### Operator Feedback Collection
```
Usability Metrics:
├── Task completion time
├── Error rate and frequency
├── User satisfaction ratings
├── Learning curve assessment
└── Accessibility compliance
```

## 📖 Best Practices Summary

### Design Guidelines
1. **Consistency**: Use standard symbols, colors, and layouts
2. **Clarity**: Clear labels, logical grouping, appropriate fonts
3. **Efficiency**: Minimize clicks, provide shortcuts, optimize workflows
4. **Safety**: Prominent emergency controls, clear alarm indication
5. **Accessibility**: Support for different skill levels and physical abilities

### Development Standards
1. **Modular Design**: Reusable components and templates
2. **Version Control**: Track changes and enable rollback
3. **Documentation**: Comprehensive design specifications
4. **Testing**: Thorough validation before deployment
5. **Maintenance**: Regular updates and performance monitoring

## 🔗 Related Resources

### Wiki Navigation
- **[PLC Programming](PLC-Programming.md)** - Control system development
- **[Process Simulation](Process-Simulation.md)** - Virtual commissioning
- **[System Architecture](System-Architecture.md)** - Overall system design
- **[Operating Procedures](../operations/Operating-Procedures.md)** - End-user guidance
- **[Troubleshooting](../operations/Troubleshooting.md)** - Problem resolution

### Standards and Guidelines
- **ISA-101**: Human Machine Interface Design
- **IEC 62264**: Enterprise-Control System Integration
- **NIST Cybersecurity Framework**: Industrial control system security
- **FDA 21 CFR Part 11**: Electronic records compliance

---

*This guide is part of the Industrial PLC Control Systems Repository wiki system, providing comprehensive resources for developing effective human-machine interfaces in industrial automation applications.*
