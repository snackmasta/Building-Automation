# Configuration Guide

## HVAC Control System Configuration Guide

This guide provides detailed instructions for configuring all aspects of the HVAC Control System, including PLC settings, zone parameters, safety systems, and optimization features.

---

## Table of Contents

1. [Configuration Overview](#configuration-overview)
2. [PLC Configuration](#plc-configuration)
3. [Zone Configuration](#zone-configuration)
4. [Safety System Configuration](#safety-system-configuration)
5. [Energy Management Settings](#energy-management-settings)
6. [HMI Configuration](#hmi-configuration)
7. [Scheduling Configuration](#scheduling-configuration)
8. [Network and Communication](#network-and-communication)
9. [Advanced Settings](#advanced-settings)
10. [Backup and Restore](#backup-and-restore)

---

## Configuration Overview

### Configuration Files Structure

The HVAC Control System uses a hierarchical configuration structure:

```
config/
├── plc_config.ini          # Main PLC configuration
├── zones_config.ini        # Zone-specific settings
├── safety_config.ini       # Safety system parameters
├── schedule_config.ini     # Operating schedules
└── backup/                 # Configuration backups
    ├── plc_config_backup.ini
    └── system_backup_YYYYMMDD.zip
```

### Configuration Principles

1. **Layered Configuration**: System → Zone → Equipment → Component
2. **Safety First**: Safety parameters override comfort settings
3. **Energy Efficiency**: Default settings optimize energy usage
4. **Flexibility**: Easy adjustment for different building types
5. **Validation**: All settings are validated for safe operation

---

## PLC Configuration

### Main PLC Settings

#### Primary Configuration File: `config/plc_config.ini`

```ini
[PLC]
# Network Configuration
ip_address = 192.168.1.100
port = 44818
timeout = 5
retry_count = 3
protocol = ethernet_ip

# System Timing
scan_interval = 1.0
update_rate = 250
heartbeat_interval = 10

# Data Format
byte_order = little_endian
word_size = 16
float_format = ieee_754
```

#### Communication Parameters

| Parameter | Description | Range | Default |
|-----------|-------------|-------|---------|
| `ip_address` | PLC IP address | Valid IP | 192.168.1.100 |
| `port` | Communication port | 1-65535 | 44818 |
| `timeout` | Response timeout (sec) | 1-30 | 5 |
| `retry_count` | Connection retries | 1-10 | 3 |
| `scan_interval` | Data update rate (sec) | 0.1-10.0 | 1.0 |

#### System Configuration

```ini
[SYSTEM]
# System Identification
system_name = HVAC_Control_System_v1.0
location = Building_A
installation_date = 2025-06-08

# Logging Configuration
log_level = INFO
log_file_size = 10MB
max_log_files = 30
log_directory = logs

# Operating Modes
default_mode = AUTO
startup_mode = MANUAL
emergency_mode = SAFE

# Performance Settings
max_concurrent_operations = 8
buffer_size = 1024
data_retention_days = 90
```

### PLC Tag Mapping

#### Input Tags (from PLC)

```ini
[INPUT_TAGS]
# Temperature Sensors (Analog Inputs)
zone_1_temp = N7:0
zone_2_temp = N7:1
zone_3_temp = N7:2
zone_4_temp = N7:3
zone_5_temp = N7:4
zone_6_temp = N7:5
zone_7_temp = N7:6
zone_8_temp = N7:7

# Humidity Sensors
zone_1_humidity = N7:10
zone_2_humidity = N7:11
zone_3_humidity = N7:12
zone_4_humidity = N7:13
zone_5_humidity = N7:14
zone_6_humidity = N7:15
zone_7_humidity = N7:16
zone_8_humidity = N7:17

# Air Quality Sensors
zone_1_co2 = N7:20
zone_2_co2 = N7:21
zone_3_co2 = N7:22
zone_4_co2 = N7:23

# System Status (Digital Inputs)
fire_alarm = I:0/0
emergency_stop = I:0/1
main_power_status = I:0/2
backup_power_status = I:0/3
```

#### Output Tags (to PLC)

```ini
[OUTPUT_TAGS]
# Damper Controls (Analog Outputs)
zone_1_damper = N7:100
zone_2_damper = N7:101
zone_3_damper = N7:102
zone_4_damper = N7:103
zone_5_damper = N7:104
zone_6_damper = N7:105
zone_7_damper = N7:106
zone_8_damper = N7:107

# Equipment Controls (Digital Outputs)
ahu_1_start = O:0/0
ahu_2_start = O:0/1
pump_1_start = O:0/2
pump_2_start = O:0/3
exhaust_fan_start = O:0/4

# System Controls
system_enable = O:0/10
emergency_shutdown = O:0/11
alarm_horn = O:0/12
status_light = O:0/13
```

---

## Zone Configuration

### Individual Zone Settings

#### Zone Configuration Template

```ini
[ZONE_1]
# Zone Identification
name = Office_Area_North
description = North office area with 12 workstations
area_sqft = 1200
occupancy_max = 15

# Temperature Control
temp_sensor_address = N7:0
temp_setpoint_occupied = 22.0
temp_setpoint_unoccupied = 18.0
temp_deadband = 1.0
temp_alarm_high = 28.0
temp_alarm_low = 16.0

# Humidity Control
humidity_sensor_address = N7:10
humidity_setpoint = 50.0
humidity_deadband = 5.0
humidity_alarm_high = 70.0
humidity_alarm_low = 30.0

# Air Quality Control
co2_sensor_address = N7:20
co2_setpoint = 800
co2_alarm = 1000
voc_sensor_address = N7:30
voc_alarm = 500

# Damper Control
damper_output_address = N7:100
damper_min_position = 10.0
damper_max_position = 100.0
damper_response_time = 60

# Airflow Settings
design_airflow_cfm = 2400
min_airflow_cfm = 480
airflow_per_person = 20
airflow_per_sqft = 2.0

# Control Parameters
control_type = PID
proportional_gain = 2.0
integral_time = 300
derivative_time = 30
control_deadband = 0.5

# Occupancy Settings
occupancy_sensor_address = I:1/0
occupied_schedule = STANDARD_OFFICE
unoccupied_setback = 4.0
warm_up_time = 60
cool_down_time = 30
```

#### Zone Types and Defaults

**Office Zones**:
```ini
temp_setpoint_occupied = 22.0
temp_deadband = 1.0
airflow_per_person = 20
min_outdoor_air_percent = 20
```

**Conference Rooms**:
```ini
temp_setpoint_occupied = 21.0
temp_deadband = 0.5
airflow_per_person = 25
min_outdoor_air_percent = 30
```

**Storage Areas**:
```ini
temp_setpoint_occupied = 20.0
temp_deadband = 2.0
airflow_per_person = 10
min_outdoor_air_percent = 10
```

**Server Rooms**:
```ini
temp_setpoint_occupied = 18.0
temp_deadband = 1.0
humidity_setpoint = 45.0
continuous_operation = true
```

### Global Zone Settings

```ini
[ZONE_DEFAULTS]
# Default Operating Parameters
default_temp_setpoint = 22.0
default_humidity_setpoint = 50.0
default_co2_setpoint = 800

# Control Tuning Defaults
default_proportional_gain = 2.0
default_integral_time = 300
default_derivative_time = 30

# Safety Limits
max_temp_setpoint = 26.0
min_temp_setpoint = 18.0
max_humidity_setpoint = 65.0
min_humidity_setpoint = 35.0

# Energy Management
setback_temperature = 4.0
setup_temperature = 4.0
minimum_runtime = 300
maximum_runtime = 3600
```

---

## Safety System Configuration

### Critical Safety Parameters

#### Fire Safety Integration

```ini
[FIRE_SAFETY]
# Fire Alarm Interface
fire_alarm_input = I:0/0
fire_alarm_type = normally_closed
fire_alarm_response = immediate_shutdown

# Smoke Detection
smoke_detector_1 = I:0/4
smoke_detector_2 = I:0/5
smoke_detector_response = zone_shutdown

# Emergency Shutdown
emergency_stop_input = I:0/1
emergency_stop_type = latching
reset_required = manual

# Fire Mode Operation
fire_mode_airflow = exhaust_only
fire_mode_dampers = full_exhaust
fire_mode_disable_heating = true
fire_mode_override_locks = true
```

#### Temperature Safety Limits

```ini
[TEMPERATURE_SAFETY]
# High Temperature Limits
high_temp_warning = 28.0
high_temp_alarm = 30.0
high_temp_shutdown = 35.0

# Low Temperature Limits
low_temp_warning = 16.0
low_temp_alarm = 14.0
freeze_protection = 2.0

# Safety Actions
high_temp_action = increase_cooling
low_temp_action = increase_heating
freeze_protection_action = emergency_heat

# Safety Overrides
safety_override_comfort = true
safety_override_energy = true
safety_override_schedule = true
```

#### Equipment Protection

```ini
[EQUIPMENT_PROTECTION]
# Motor Protection
motor_overload_trip = I:0/10
high_vibration_alarm = I:0/11
bearing_temperature_high = I:0/12

# System Protection
low_water_pressure = I:0/15
high_water_pressure = I:0/16
filter_pressure_high = I:0/17

# Protection Actions
motor_trip_action = immediate_stop
low_pressure_action = backup_pump_start
high_pressure_action = pressure_relief
filter_alarm_action = maintenance_alert
```

---

## Energy Management Settings

### Optimization Parameters

#### Demand Management

```ini
[DEMAND_MANAGEMENT]
# Peak Demand Settings
peak_demand_limit = 500.0
demand_window = 15
demand_prediction = true

# Load Shedding Strategy
shed_level_1 = 10
shed_level_2 = 20
shed_level_3 = 30
shed_level_4 = 50

# Load Shedding Actions
level_1_action = reduce_airflow_10_percent
level_2_action = raise_cooling_setpoint_1C
level_3_action = reduce_airflow_20_percent
level_4_action = shutdown_non_critical_zones

# Recovery Settings
recovery_delay = 300
gradual_recovery = true
recovery_time = 900
```

#### Economizer Configuration

```ini
[ECONOMIZER]
# Operating Parameters
enable_economizer = true
outdoor_air_high_limit = 24.0
outdoor_air_low_limit = -5.0
enthalpy_control = true

# Damper Settings
minimum_outdoor_air = 20
maximum_outdoor_air = 100
damper_response_time = 120

# Control Logic
economizer_deadband = 2.0
changeover_setpoint = 18.0
lockout_on_humidity = true
humidity_lockout_limit = 70.0
```

#### Energy Optimization

```ini
[ENERGY_OPTIMIZATION]
# Optimal Start/Stop
optimal_start_enable = true
optimal_stop_enable = true
max_preheat_time = 120
max_precool_time = 60

# Night Setback
night_setback_enable = true
heating_setback = 4.0
cooling_setup = 4.0
weekend_setback = 6.0

# Efficiency Settings
part_load_efficiency = true
staging_optimization = true
variable_speed_control = true
```

---

## HMI Configuration

### Display Settings

#### Screen Configuration

```ini
[HMI_DISPLAY]
# Screen Properties
resolution = 1920x1080
color_depth = 32
refresh_rate = 60
fullscreen_mode = false

# Update Rates
screen_update_rate = 1.0
trend_update_rate = 5.0
alarm_update_rate = 0.5

# Color Scheme
background_color = #F0F0F0
normal_color = #000000
alarm_color = #FF0000
warning_color = #FFA500
ok_color = #00FF00
```

#### Graphics Settings

```ini
[HMI_GRAPHICS]
# Chart Settings
trend_points = 1440
trend_duration = 24
auto_scale = true
grid_lines = true

# Gauge Settings
gauge_style = circular
scale_divisions = 10
needle_smoothing = true

# Animation Settings
enable_animations = true
animation_speed = medium
fade_transitions = true
```

### User Interface Configuration

```ini
[USER_INTERFACE]
# Navigation
main_menu_timeout = 300
auto_logout_time = 1800
breadcrumb_navigation = true

# User Levels
operator_level = 1
supervisor_level = 2
administrator_level = 3
maintenance_level = 4

# Security Settings
password_required = true
password_expiry_days = 90
login_attempts_max = 3
lockout_duration = 900
```

---

## Scheduling Configuration

### Operating Schedules

#### Standard Office Schedule

```ini
[SCHEDULE_OFFICE]
# Weekday Schedule
monday_start = 07:00
monday_end = 18:00
tuesday_start = 07:00
tuesday_end = 18:00
wednesday_start = 07:00
wednesday_end = 18:00
thursday_start = 07:00
thursday_end = 18:00
friday_start = 07:00
friday_end = 18:00

# Weekend Schedule
saturday_start = 08:00
saturday_end = 14:00
sunday_occupied = false

# Holiday Schedule
use_holiday_schedule = true
holiday_schedule = UNOCCUPIED
```

#### Custom Schedules

```ini
[SCHEDULE_CONFERENCE]
# Event-Based Scheduling
booking_system_integration = true
pre_event_warmup = 60
post_event_cooldown = 30
override_duration = 240

[SCHEDULE_24_7]
# Continuous Operation
continuous_operation = true
night_setback = 2.0
weekend_setback = 1.0
```

### Holiday Configuration

```ini
[HOLIDAYS]
# 2025 Holidays
new_years_day = 2025-01-01
memorial_day = 2025-05-26
independence_day = 2025-07-04
labor_day = 2025-09-01
thanksgiving = 2025-11-27
christmas = 2025-12-25

# Holiday Behavior
holiday_mode = unoccupied
holiday_setback = 6.0
holiday_override_allowed = true
```

---

## Network and Communication

### Network Configuration

#### Ethernet Settings

```ini
[NETWORK]
# Primary Network Interface
primary_interface = Ethernet
ip_address = 192.168.1.50
subnet_mask = 255.255.255.0
default_gateway = 192.168.1.1
dns_server = 192.168.1.10

# Backup Network Interface
backup_interface = WiFi
backup_ip = 192.168.2.50
backup_subnet = 255.255.255.0
backup_gateway = 192.168.2.1

# Network Timeouts
connection_timeout = 5
read_timeout = 3
write_timeout = 3
keepalive_interval = 30
```

#### Communication Protocols

```ini
[PROTOCOLS]
# Ethernet/IP Configuration
ethernet_ip_enable = true
ethernet_ip_port = 44818
explicit_messaging = true
implicit_messaging = false

# Modbus TCP Configuration
modbus_tcp_enable = false
modbus_tcp_port = 502
modbus_unit_id = 1

# BACnet Configuration
bacnet_enable = false
bacnet_port = 47808
bacnet_device_id = 12345
```

---

## Advanced Settings

### Control Algorithm Parameters

#### PID Controller Tuning

```ini
[PID_TUNING]
# Temperature Control
temp_proportional_gain = 2.0
temp_integral_time = 300
temp_derivative_time = 30
temp_output_min = 0.0
temp_output_max = 100.0

# Pressure Control  
pressure_proportional_gain = 1.5
pressure_integral_time = 180
pressure_derivative_time = 20

# Flow Control
flow_proportional_gain = 3.0
flow_integral_time = 120
flow_derivative_time = 15
```

#### Advanced Control Features

```ini
[ADVANCED_CONTROL]
# Adaptive Control
adaptive_tuning = true
self_tuning_interval = 86400
learning_rate = 0.1

# Predictive Control
model_predictive_control = false
prediction_horizon = 3600
control_horizon = 900

# Fuzzy Logic
fuzzy_control_enable = false
fuzzy_rule_base = standard
membership_functions = triangular
```

### System Diagnostics

```ini
[DIAGNOSTICS]
# Performance Monitoring
performance_logging = true
performance_log_interval = 300
trend_data_retention = 90

# System Health
health_check_interval = 60
auto_diagnostics = true
diagnostic_report_daily = true

# Maintenance Alerts
predictive_maintenance = true
maintenance_alert_days = 7
filter_change_alert = true
calibration_reminder = true
```

---

## Backup and Restore

### Configuration Backup

#### Automatic Backup Settings

```ini
[BACKUP]
# Backup Schedule
automatic_backup = true
backup_interval = daily
backup_time = 02:00
backup_retention_days = 30

# Backup Location
backup_directory = config/backup
remote_backup_enable = false
remote_backup_path = \\server\hvac_backup

# Backup Contents
include_configuration = true
include_trends = true
include_logs = false
include_user_settings = true
```

#### Manual Backup Procedure

1. **Create Backup**:
   ```cmd
   python utils\backup_config.py --create
   ```

2. **Restore from Backup**:
   ```cmd
   python utils\backup_config.py --restore config/backup/system_backup_20250608.zip
   ```

3. **Verify Configuration**:
   ```cmd
   python utils\verification\verify_system.py
   ```

### Configuration Validation

#### Validation Rules

```ini
[VALIDATION]
# Range Checking
enable_range_validation = true
enable_type_validation = true
enable_dependency_validation = true

# Safety Validation
safety_override_validation = true
temperature_limit_validation = true
pressure_limit_validation = true

# Cross-Reference Validation
zone_count_validation = true
sensor_address_validation = true
actuator_address_validation = true
```

---

## Configuration Examples

### Small Office Building (4 zones)

```ini
[SYSTEM]
zone_count = 4
building_type = office
total_area_sqft = 4800

[ZONE_1]
name = Reception
area_sqft = 400
occupancy_max = 4
temp_setpoint_occupied = 22.0

[ZONE_2]
name = Open_Office
area_sqft = 2400  
occupancy_max = 24
temp_setpoint_occupied = 22.0

[ZONE_3]
name = Conference_Room
area_sqft = 600
occupancy_max = 12
temp_setpoint_occupied = 21.0

[ZONE_4]
name = Server_Room
area_sqft = 200
continuous_operation = true
temp_setpoint_occupied = 18.0
```

### Manufacturing Facility (8 zones)

```ini
[SYSTEM]
zone_count = 8
building_type = industrial
total_area_sqft = 24000

[ZONE_1]
name = Production_Floor_A
area_sqft = 8000
occupancy_max = 20
temp_setpoint_occupied = 20.0
high_heat_load = true

[ZONE_2]
name = Assembly_Area
area_sqft = 4000
occupancy_max = 15
temp_setpoint_occupied = 21.0
precision_control = true
```

---

## Best Practices

### Configuration Management

#### Version Control
- Track all configuration changes
- Document change reasons
- Test changes in development environment
- Implement staged rollouts

#### Change Control Process
1. **Planning**: Define change requirements
2. **Testing**: Validate in test environment  
3. **Approval**: Get stakeholder approval
4. **Implementation**: Apply changes carefully
5. **Verification**: Confirm proper operation
6. **Documentation**: Update all documentation

### Performance Optimization

#### Regular Reviews
- Monthly performance analysis
- Quarterly configuration review
- Annual optimization study
- Continuous improvement process

#### Key Performance Indicators
- Energy consumption trends
- Comfort complaint frequency
- Equipment runtime hours
- System availability percentage

---

## Troubleshooting Configuration Issues

### Common Problems

| Issue | Symptoms | Solution |
|-------|----------|----------|
| Invalid configuration syntax | System won't start | Check INI file format |
| Out-of-range values | Alarms at startup | Verify parameter ranges |
| Missing required parameters | Error messages | Add missing configuration |
| Conflicting settings | Erratic operation | Review interdependencies |

### Validation Tools

```cmd
# Check configuration syntax
python utils\validate_config.py

# Test configuration loading
python utils\test_config.py

# Generate configuration report
python utils\config_report.py
```

---

## Support and Documentation

### Configuration Support

- **Online Documentation**: [Wiki Home](../Home.md)
- **Configuration Templates**: Available in `config/templates/`
- **Example Configurations**: Available in `config/examples/`
- **Technical Support**: support@hvac-system.com

### Related Documents

- [Installation Guide](Installation.md)
- [Operating Procedures](Operating_Procedures.md)
- [Troubleshooting Guide](Troubleshooting.md)
- [Maintenance Manual](../docs/Maintenance_Manual.md)

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | June 8, 2025 | Initial configuration guide |

---

*Last Updated: June 8, 2025*
