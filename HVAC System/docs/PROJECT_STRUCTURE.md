# HVAC System - Project Structure

## Folder Organization

This document describes the reorganized folder structure of the HVAC System project, following industry best practices for software organization and maintenance.

### Root Directory Structure

```
HVAC System/
├── plc/                          # PLC Programming
├── src/                          # Source Code
├── config/                       # Configuration
├── docs/                         # Documentation
├── diagrams/                     # Generated Diagrams
├── scripts/                      # Automation Scripts
├── utils/                        # Utilities
├── tests/                        # Unit Tests
├── wiki/                         # Wiki Documentation
└── logs/                         # System Logs
```

### Detailed Folder Contents

#### 1. PLC Programming (`plc/`)
Contains all Structured Text programs for the PLC system:
- `global_vars.st` - Global variable declarations
- `main.st` - Main control program loop
- `temperature_controller.st` - Zone temperature control logic
- `air_quality_controller.st` - Air quality monitoring and control
- `energy_manager.st` - Energy optimization algorithms
- `safety_controller.st` - Safety interlocks and emergency procedures

#### 2. Source Code (`src/`)
Organized by application layer:

**Core Components (`src/core/`)**
- `main_controller.py` - Main HVAC control system

**GUI Layer (`src/gui/`)**
- `hmi_interface.py` - Python tkinter HMI application
- `web_hmi.html` - Web-based monitoring interface

**Simulation Layer (`src/simulation/`)**
- `hvac_simulator.py` - HVAC system physics simulation

**Monitoring Layer (`src/monitoring/`)**
- `system_status.py` - Real-time system monitoring

#### 3. Configuration (`config/`)
- `plc_config.ini` - System configuration parameters
- `hmi_config.ini` - HMI display settings

#### 4. Documentation (`docs/`)
- `Installation_Guide.md` - System installation procedures
- `Maintenance_Manual.md` - Maintenance procedures
- `Operating_Procedures.md` - Daily operation instructions
- `Troubleshooting_Guide.md` - Problem resolution guide

#### 5. Diagrams (`diagrams/`)
Generated visual documentation:
- System architecture diagrams
- Process flow diagrams
- P&ID diagrams
- Control logic flowcharts

#### 6. Scripts (`scripts/`)
Automation and utility scripts:

**Batch Scripts (`scripts/batch/`)**
- `system_launcher.bat` - Main system control center
- `run_main_controller.bat` - Launch main controller
- `run_hmi.bat` - Launch HMI interface
- `run_simulator.bat` - Start HVAC simulator
- `run_status_monitor.bat` - Start monitoring dashboard
- `generate_diagrams.bat` - Generate all diagrams

#### 7. Utilities (`utils/`)
- `hvac_diagram.py` - Diagram generation tools
- `hvac_diagram_new.py` - Updated diagram generator

**Verification (`utils/verification/`)**
- `verify_system.py` - System integrity checker

#### 8. Tests (`tests/`)
Unit tests and integration tests for system components.

#### 9. Wiki (`wiki/`)
Project wiki documentation:
- `Home.md` - Wiki home page
- `pages/` - Individual wiki pages
- `templates/` - Documentation templates
- `assets/` - Wiki assets and images

#### 10. Logs (`logs/`)
System log files generated during operation.

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
- Consistent naming conventions
- Comprehensive documentation

### 4. Industrial Standards
- Follows ISA-88 batch control standards
- Implements IEC 61131-3 PLC programming standards
- Uses industry-standard folder hierarchies
- Maintains audit trails and version control

## File Organization Rules

### Naming Conventions
- Files: `snake_case.py` or `PascalCase.st`
- Folders: `lowercase` with underscores if needed
- Constants: `UPPERCASE_WITH_UNDERSCORES`
- Variables: `camelCase` or `snake_case` consistently

### Import Structure
```python
# Standard library imports
import sys
import time

# Third-party imports
import numpy as np
import matplotlib.pyplot as plt

# Local application imports
from src.core import main_controller
from src.monitoring import system_status
```

### Configuration Management
- All configurable parameters in `config/` folder
- Environment-specific settings separated
- Default values provided for all parameters
- Configuration validation on startup

## Deployment Structure

### Development Environment
- Full source code access
- All debugging tools available
- Comprehensive logging enabled
- Test data and mock services

### Production Environment
- Optimized for performance
- Security hardened
- Minimal logging for efficiency
- Real hardware interfaces

### Testing Environment
- Isolated from production
- Comprehensive test coverage
- Automated testing pipelines
- Performance benchmarking

## Migration Notes

### Files Moved During Restructuring
- `main_controller.py` → `src/core/main_controller.py`
- `system_status.py` → `src/monitoring/system_status.py`
- `web_hmi.html` → `src/gui/web_hmi.html`

### Updated References
- Batch scripts updated to point to new locations
- Import statements adjusted for new structure
- Documentation links updated
- Configuration paths corrected

This structure ensures the HVAC System follows the same organizational principles as the Water Treatment System, promoting consistency across projects and ease of maintenance.
