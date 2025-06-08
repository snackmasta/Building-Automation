# Water Treatment System - Project Structure

## Folder Organization

This document describes the reorganized folder structure of the Water Treatment System project, following industry best practices for software organization and maintenance.

### Root Directory Structure

```
Water Treatment System/
├── plc/                          # PLC Programming
├── src/                          # Source Code
├── config/                       # Configuration
├── docs/                         # Documentation
├── diagrams/                     # Generated Diagrams
├── scripts/                      # Automation Scripts
├── utils/                        # Utilities
└── tests/                        # Unit Tests
```

### Detailed Folder Contents

#### 1. PLC Programming (`plc/`)
Contains all Structured Text programs for the PLC system:
- `global_vars.st` - Global variable declarations
- `main.st` - Main control program loop
- `desalination_controller.st` - RO membrane control logic
- `pump_controller.st` - Pump sequencing and rotation
- `water_quality_controller.st` - Quality monitoring and control

#### 2. Source Code (`src/`)
Organized by application layer:

**GUI Layer (`src/gui/`)**
- `hmi_interface.py` - Python tkinter HMI application
- `web_hmi.html` - Web-based monitoring interface

**Simulation Layer (`src/simulation/`)**
- `water_treatment_simulator.py` - Process physics simulation

**Monitoring Layer (`src/monitoring/`)**
- `system_status.py` - Real-time system monitoring

**Core Components (`src/core/`)**
- `process_diagram.py` - Diagram generation engine

#### 3. Configuration (`config/`)
- `plc_config.ini` - System configuration parameters

#### 4. Documentation (`docs/`)
- `README.md` - Main project documentation
- `System_Documentation.md` - Technical specifications
- `FLOWCHART_IMPLEMENTATION_SUMMARY.md` - Process flow details

#### 5. Diagrams (`diagrams/`)
Generated visual documentation:
- `process_control_flowchart.png` - 24-step decision tree
- `system_states_diagram.png` - State machine visualization
- `control_system_architecture.png` - System architecture
- `water_treatment_process_diagram.png` - Main process flow
- `water_treatment_pid.png` - P&ID diagram
- `water_treatment_diagrams.pdf` - Combined PDF documentation

#### 6. Scripts (`scripts/`)
Automation and utility scripts:

**Batch Scripts (`scripts/batch/`)**
- `system_launcher.bat` - Main system control center
- `run_hmi.bat` - Launch HMI interface
- `run_simulator.bat` - Start process simulator
- `run_status_monitor.bat` - Start monitoring dashboard
- `generate_diagrams.bat` - Generate all diagrams

#### 7. Utilities (`utils/`)
- `final_project_summary.py` - Project report generator
- `flowchart_demo.py` - Flowchart demonstration tool

**Verification (`utils/verification/`)**
- `verify_system.py` - System integrity checker

#### 8. Tests (`tests/`)
Reserved for future unit tests and integration tests.

## Design Principles

### 1. Separation of Concerns
Each folder has a specific responsibility:
- PLC code separate from application code
- GUI separate from business logic
- Documentation separate from implementation
- Scripts separate from core functionality

### 2. Scalability
The structure allows for easy addition of:
- New PLC programs in `plc/`
- New GUI applications in `src/gui/`
- Additional monitoring tools in `src/monitoring/`
- More utility scripts in `utils/`

### 3. Maintainability
- Clear folder names indicate content purpose
- Related files grouped together
- Configuration centralized in `config/`
- Documentation centralized in `docs/`

### 4. Industry Standards
Follows common practices from:
- Industrial automation projects
- Software engineering best practices
- PLC programming standards (IEC 61131-3)
- Process control documentation standards

## Benefits of Restructuring

### Before (Monolithic)
- All 28 files in one directory
- Difficult to navigate and maintain
- No clear separation of concerns
- Hard to locate specific functionality

### After (Structured)
- Logical organization by functionality
- Easy to find and maintain specific components
- Clear separation between different layers
- Professional project structure
- Ready for team collaboration
- Version control friendly

## Usage Guidelines

### For Developers
1. Add new PLC programs to `plc/` folder
2. Place GUI applications in appropriate `src/` subfolder
3. Update documentation in `docs/` when making changes
4. Add utility scripts to `utils/` folder
5. Use `scripts/batch/` for automation tasks

### For Operators
1. Use `scripts/batch/system_launcher.bat` as main entry point
2. Access documentation through `docs/README.md`
3. View diagrams in `diagrams/` folder
4. Check configuration in `config/plc_config.ini`

### For Maintenance
1. Run `utils/verification/verify_system.py` for health checks
2. Generate reports with `utils/final_project_summary.py`
3. Update diagrams with `scripts/batch/generate_diagrams.bat`
4. Monitor system with `scripts/batch/run_status_monitor.bat`

## Migration Notes

All file paths in batch scripts have been updated to work with the new structure:
- Scripts use `cd /d "%~dp0..\.."` to navigate to project root
- Relative paths updated to new folder locations
- Verification scripts updated for new structure
- Documentation references updated

This restructuring maintains full backward compatibility while providing a much more professional and maintainable project organization.
