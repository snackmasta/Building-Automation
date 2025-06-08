# Quick Start Guide

Get your Water Treatment System up and running in minutes with this step-by-step guide.

## 🚀 Prerequisites

### System Requirements
- Windows 10/11 operating system
- Python 3.7 or higher installed
- Minimum 4GB RAM, 8GB recommended
- 2GB free disk space

### Required Python Packages
```bash
pip install tkinter matplotlib numpy sqlite3 configparser psutil
```

## ⚡ 5-Minute Startup

### Step 1: Launch the System
```batch
# Navigate to the project directory
cd "c:\Users\Legion\Desktop\PLC\Water Treatment System"

# Run the main system launcher
scripts\batch\system_launcher.bat
```

### Step 2: System Menu Options
When the launcher starts, you'll see:
```
================================================================
            WATER TREATMENT SYSTEM - CONTROL CENTER
================================================================

  1. Launch System Simulator      ← Start here for demo
  2. Launch HMI Interface         ← Main operator interface
  3. Open Web HMI (Browser)       ← Modern web interface
  4. System Status Monitor        ← Real-time monitoring
  5. Generate Process Diagrams    ← Visual documentation
  6. View System Documentation    ← Technical manuals
  7. Open Configuration File      ← System settings
  8. System Health Check          ← Verify system integrity
  9. Export Status Report         ← Generate system report
  0. Exit
```

### Step 3: First Run Sequence
1. **Option 8** - Run health check to verify all components
2. **Option 1** - Launch simulator to see the system in action
3. **Option 2** - Open HMI interface for hands-on control
4. **Option 5** - Generate diagrams to view system layout

## 🎯 Key Components Overview

### Main Control Interface
- **Location:** `src/gui/hmi_interface.py`
- **Features:** Real-time monitoring, manual control, trending
- **Access:** Option 2 in system launcher

### Web Interface
- **Location:** `src/gui/web_hmi.html`
- **Features:** Mobile-responsive, modern dashboard
- **Access:** Option 3 in system launcher

### Process Simulator
- **Location:** `src/simulation/water_treatment_simulator.py`
- **Features:** Realistic physics modeling, GUI visualization
- **Access:** Option 1 in system launcher

### System Monitor
- **Location:** `src/monitoring/system_status.py`
- **Features:** Performance tracking, health monitoring
- **Access:** Option 4 in system launcher

## 🔧 Basic Operations

### Starting the System
1. Ensure all pumps are in manual mode
2. Check water levels in all tanks
3. Verify pressure settings are within range
4. Start intake pump first
5. Engage pre-treatment sequence
6. Initialize RO system when feed conditions are met

### Normal Operation Monitoring
- **Inlet Pressure:** 2-4 bar
- **RO Pressure:** 50-60 bar
- **Recovery Rate:** 40-50%
- **Product Quality:** <500 ppm TDS
- **Tank Levels:** 20-80% normal range

### Emergency Shutdown
- Press **Emergency Stop** button in any interface
- System will safely shut down all pumps
- Valves will move to safe positions
- Alarms will indicate shutdown reason

## 📊 Understanding the Display

### Status Indicators
- 🟢 **Green:** Normal operation
- 🟡 **Yellow:** Warning condition
- 🔴 **Red:** Alarm condition
- ⚫ **Gray:** Equipment offline

### Main Process Values
- **Flow Rate:** L/hour production rate
- **Pressure:** Bar (inlet, RO, product)
- **Quality:** TDS in ppm
- **Recovery:** Percentage of feed water recovered

### Alarm Priorities
1. **Critical:** Immediate action required
2. **High:** Urgent attention needed
3. **Medium:** Monitor closely
4. **Low:** Information only

## 🛠️ Troubleshooting Quick Reference

### Common Issues

**Low Production Rate**
- Check membrane fouling level
- Verify feed pressure is adequate
- Review recovery rate settings

**High TDS in Product**
- Inspect RO membranes for damage
- Check system for leaks
- Verify post-treatment operation

**Pump Won't Start**
- Check electrical connections
- Verify pump is in automatic mode
- Review safety interlocks

**System Won't Start**
- Run system health check (Option 8)
- Check configuration file
- Verify all files are present

## 📚 Next Steps

### For Daily Operations
- Review **[Operating Procedures](Operating-Procedures.md)**
- Study **[Process Flow](Process-Flow.md)** details
- Understand **[Safety Procedures](Safety-Procedures.md)**

### For Technical Understanding
- Read **[System Architecture](System-Architecture.md)**
- Study **[PLC Programming](PLC-Programming.md)**
- Review **[Process Control](Process-Control.md)**

### For Maintenance
- Follow **[Maintenance Guide](Maintenance-Guide.md)**
- Check **[Equipment List](Equipment-List.md)**
- Use **[Troubleshooting](Troubleshooting.md)** guide

## 🆘 Emergency Contacts

### System Issues
1. Check **[Troubleshooting](Troubleshooting.md)** first
2. Run system verification tool
3. Contact technical support

### Safety Emergencies
1. Press emergency stop immediately
2. Follow **[Safety Procedures](Safety-Procedures.md)**
3. Contact emergency services if needed

---

*Need more help? Check the [Home](../Home.md) page for complete navigation.*
