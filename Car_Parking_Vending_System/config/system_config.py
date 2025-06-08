"""
System Configuration Files for Automated Car Parking System
Central configuration management with validation and defaults
"""

import json
import yaml
import os
import logging
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, asdict
from datetime import datetime
import configparser

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class DatabaseConfig:
    """Database configuration"""
    path: str = "parking_system.db"
    max_connections: int = 10
    backup_enabled: bool = True
    backup_interval_hours: int = 24
    backup_directory: str = "backups"

@dataclass
class PLCConfig:
    """PLC configuration"""
    modbus_host: str = "192.168.1.100"
    modbus_port: int = 502
    modbus_unit_id: int = 1
    connection_timeout: int = 10
    read_timeout: int = 5
    retry_attempts: int = 3

@dataclass
class ElevatorConfig:
    """Elevator configuration"""
    count: int = 3
    max_speed: float = 2.0  # m/s
    acceleration: float = 0.5  # m/s²
    max_load: float = 2000.0  # kg
    level_height: float = 3.0  # meters
    maintenance_interval_hours: int = 168  # 1 week

@dataclass
class ParkingConfig:
    """Parking configuration"""
    total_levels: int = 15
    spaces_per_level: int = 20
    total_spaces: int = 300
    space_dimensions: Dict[str, Dict[str, float]] = None
    rates: Dict[str, float] = None
    max_parking_hours: int = 24
    grace_period_minutes: int = 15

    def __post_init__(self):
        if self.space_dimensions is None:
            self.space_dimensions = {
                "standard": {"length": 5.0, "width": 2.5, "height": 2.2},
                "compact": {"length": 4.5, "width": 2.0, "height": 2.0},
                "large": {"length": 6.0, "width": 3.0, "height": 2.5}
            }
        
        if self.rates is None:
            self.rates = {
                "car": 3.0,
                "suv": 4.0,
                "truck": 6.0,
                "motorcycle": 2.0
            }

@dataclass
class PaymentConfig:
    """Payment system configuration"""
    accepted_methods: List[str] = None
    cash_enabled: bool = True
    card_enabled: bool = True
    mobile_pay_enabled: bool = True
    rfid_enabled: bool = True
    tax_rate: float = 0.08
    discount_rates: Dict[str, float] = None
    currency: str = "USD"

    def __post_init__(self):
        if self.accepted_methods is None:
            self.accepted_methods = ["cash", "credit_card", "debit_card", "mobile_pay", "rfid_card"]
        
        if self.discount_rates is None:
            self.discount_rates = {
                "senior": 0.10,
                "student": 0.15,
                "employee": 0.20,
                "vip": 0.25
            }

@dataclass
class SafetyConfig:
    """Safety system configuration"""
    emergency_contact: str = "911"
    fire_detection_enabled: bool = True
    gas_detection_enabled: bool = True
    earthquake_detection_enabled: bool = True
    emergency_lighting_enabled: bool = True
    evacuation_time_limit: int = 300  # seconds
    safety_check_interval: int = 60  # seconds

@dataclass
class CommunicationConfig:
    """Communication configuration"""
    websocket_host: str = "localhost"
    websocket_port: int = 8765
    tcp_host: str = "localhost"
    tcp_port: int = 9001
    opcua_endpoint: str = "opc.tcp://localhost:4840"
    max_message_size: int = 65536
    heartbeat_interval: int = 30

@dataclass
class LoggingConfig:
    """Logging configuration"""
    level: str = "INFO"
    file_enabled: bool = True
    console_enabled: bool = True
    log_directory: str = "logs"
    max_file_size: int = 10485760  # 10MB
    backup_count: int = 5
    format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

@dataclass
class SimulationConfig:
    """Simulation configuration"""
    enabled: bool = False
    entry_rate: float = 5.0  # vehicles per hour
    exit_rate: float = 3.0   # vehicles per hour
    peak_hours: List[tuple] = None
    peak_multiplier: float = 3.0
    realistic_names: bool = True

    def __post_init__(self):
        if self.peak_hours is None:
            self.peak_hours = [(7, 9), (17, 19)]

@dataclass
class SystemConfig:
    """Complete system configuration"""
    system_name: str = "Automated Car Parking System"
    version: str = "1.0.0"
    timezone: str = "UTC"
    language: str = "en"
    
    database: DatabaseConfig = None
    plc: PLCConfig = None
    elevator: ElevatorConfig = None
    parking: ParkingConfig = None
    payment: PaymentConfig = None
    safety: SafetyConfig = None
    communication: CommunicationConfig = None
    logging: LoggingConfig = None
    simulation: SimulationConfig = None

    def __post_init__(self):
        if self.database is None:
            self.database = DatabaseConfig()
        if self.plc is None:
            self.plc = PLCConfig()
        if self.elevator is None:
            self.elevator = ElevatorConfig()
        if self.parking is None:
            self.parking = ParkingConfig()
        if self.payment is None:
            self.payment = PaymentConfig()
        if self.safety is None:
            self.safety = SafetyConfig()
        if self.communication is None:
            self.communication = CommunicationConfig()
        if self.logging is None:
            self.logging = LoggingConfig()
        if self.simulation is None:
            self.simulation = SimulationConfig()

class ConfigManager:
    """Configuration manager for the parking system"""
    
    def __init__(self, config_file: str = "config/system_config.yaml"):
        self.config_file = config_file
        self.config = SystemConfig()
        self.watchers = {}
        
        # Ensure config directory exists
        os.makedirs(os.path.dirname(config_file), exist_ok=True)
        
        # Load configuration
        self.load_config()
        
    def load_config(self) -> bool:
        """Load configuration from file"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    if self.config_file.endswith('.yaml') or self.config_file.endswith('.yml'):
                        config_data = yaml.safe_load(f)
                    else:
                        config_data = json.load(f)
                
                # Convert dict to SystemConfig
                self.config = self._dict_to_config(config_data)
                logger.info(f"Configuration loaded from {self.config_file}")
                return True
            else:
                # Create default configuration
                self.save_config()
                logger.info(f"Default configuration created at {self.config_file}")
                return True
                
        except Exception as e:
            logger.error(f"Error loading configuration: {e}")
            return False
            
    def save_config(self) -> bool:
        """Save configuration to file"""
        try:
            config_data = asdict(self.config)
            
            with open(self.config_file, 'w') as f:
                if self.config_file.endswith('.yaml') or self.config_file.endswith('.yml'):
                    yaml.dump(config_data, f, default_flow_style=False, indent=2)
                else:
                    json.dump(config_data, f, indent=4, default=str)
            
            logger.info(f"Configuration saved to {self.config_file}")
            return True
            
        except Exception as e:
            logger.error(f"Error saving configuration: {e}")
            return False
            
    def _dict_to_config(self, data: Dict) -> SystemConfig:
        """Convert dictionary to SystemConfig object"""
        try:
            # Create nested configuration objects
            config = SystemConfig()
            
            # Update system-level properties
            for key, value in data.items():
                if hasattr(config, key):
                    if key == 'database' and isinstance(value, dict):
                        config.database = DatabaseConfig(**value)
                    elif key == 'plc' and isinstance(value, dict):
                        config.plc = PLCConfig(**value)
                    elif key == 'elevator' and isinstance(value, dict):
                        config.elevator = ElevatorConfig(**value)
                    elif key == 'parking' and isinstance(value, dict):
                        config.parking = ParkingConfig(**value)
                    elif key == 'payment' and isinstance(value, dict):
                        config.payment = PaymentConfig(**value)
                    elif key == 'safety' and isinstance(value, dict):
                        config.safety = SafetyConfig(**value)
                    elif key == 'communication' and isinstance(value, dict):
                        config.communication = CommunicationConfig(**value)
                    elif key == 'logging' and isinstance(value, dict):
                        config.logging = LoggingConfig(**value)
                    elif key == 'simulation' and isinstance(value, dict):
                        config.simulation = SimulationConfig(**value)
                    else:
                        setattr(config, key, value)
                        
            return config
            
        except Exception as e:
            logger.error(f"Error converting dict to config: {e}")
            return SystemConfig()  # Return default config
            
    def get_config(self) -> SystemConfig:
        """Get current configuration"""
        return self.config
        
    def update_config(self, section: str, key: str, value: Any) -> bool:
        """Update specific configuration value"""
        try:
            if hasattr(self.config, section):
                section_obj = getattr(self.config, section)
                if hasattr(section_obj, key):
                    setattr(section_obj, key, value)
                    
                    # Notify watchers
                    self._notify_watchers(section, key, value)
                    
                    return True
                    
        except Exception as e:
            logger.error(f"Error updating configuration: {e}")
            
        return False
        
    def get_value(self, section: str, key: str, default: Any = None) -> Any:
        """Get configuration value"""
        try:
            if hasattr(self.config, section):
                section_obj = getattr(self.config, section)
                if hasattr(section_obj, key):
                    return getattr(section_obj, key)
                    
        except Exception as e:
            logger.error(f"Error getting configuration value: {e}")
            
        return default
        
    def validate_config(self) -> List[str]:
        """Validate configuration and return list of errors"""
        errors = []
        
        try:
            # Validate parking configuration
            if self.config.parking.total_spaces != (self.config.parking.total_levels * self.config.parking.spaces_per_level):
                errors.append("Total spaces doesn't match levels × spaces_per_level")
                
            # Validate elevator configuration
            if self.config.elevator.count <= 0:
                errors.append("Elevator count must be greater than 0")
                
            if self.config.elevator.max_speed <= 0:
                errors.append("Elevator max speed must be positive")
                
            # Validate payment rates
            for vehicle_type, rate in self.config.payment.discount_rates.items():
                if rate < 0 or rate > 1:
                    errors.append(f"Invalid discount rate for {vehicle_type}: {rate}")
                    
            # Validate communication ports
            if self.config.communication.websocket_port == self.config.communication.tcp_port:
                errors.append("WebSocket and TCP ports cannot be the same")
                
            # Validate database configuration
            if not self.config.database.path:
                errors.append("Database path cannot be empty")
                
        except Exception as e:
            errors.append(f"Configuration validation error: {e}")
            
        return errors
        
    def watch_value(self, section: str, key: str, callback: callable):
        """Watch for changes to a specific configuration value"""
        watch_key = f"{section}.{key}"
        if watch_key not in self.watchers:
            self.watchers[watch_key] = []
        self.watchers[watch_key].append(callback)
        
    def _notify_watchers(self, section: str, key: str, value: Any):
        """Notify watchers of configuration changes"""
        watch_key = f"{section}.{key}"
        if watch_key in self.watchers:
            for callback in self.watchers[watch_key]:
                try:
                    callback(section, key, value)
                except Exception as e:
                    logger.error(f"Error notifying watcher: {e}")
                    
    def export_config(self, format: str = 'yaml') -> str:
        """Export configuration as string"""
        config_data = asdict(self.config)
        
        if format.lower() == 'yaml':
            return yaml.dump(config_data, default_flow_style=False, indent=2)
        elif format.lower() == 'json':
            return json.dumps(config_data, indent=4, default=str)
        else:
            raise ValueError(f"Unsupported format: {format}")
            
    def import_config(self, config_string: str, format: str = 'yaml') -> bool:
        """Import configuration from string"""
        try:
            if format.lower() == 'yaml':
                config_data = yaml.safe_load(config_string)
            elif format.lower() == 'json':
                config_data = json.loads(config_string)
            else:
                raise ValueError(f"Unsupported format: {format}")
                
            self.config = self._dict_to_config(config_data)
            return True
            
        except Exception as e:
            logger.error(f"Error importing configuration: {e}")
            return False
            
    def create_backup(self) -> str:
        """Create configuration backup"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = f"{self.config_file}.backup_{timestamp}"
            
            with open(backup_file, 'w') as f:
                config_data = asdict(self.config)
                yaml.dump(config_data, f, default_flow_style=False, indent=2)
                
            logger.info(f"Configuration backup created: {backup_file}")
            return backup_file
            
        except Exception as e:
            logger.error(f"Error creating configuration backup: {e}")
            return ""
            
    def restore_backup(self, backup_file: str) -> bool:
        """Restore configuration from backup"""
        try:
            if not os.path.exists(backup_file):
                logger.error(f"Backup file not found: {backup_file}")
                return False
                
            with open(backup_file, 'r') as f:
                config_data = yaml.safe_load(f)
                
            self.config = self._dict_to_config(config_data)
            logger.info(f"Configuration restored from backup: {backup_file}")
            return True
            
        except Exception as e:
            logger.error(f"Error restoring configuration backup: {e}")
            return False

class EnvironmentConfig:
    """Environment-specific configuration loader"""
    
    @staticmethod
    def load_environment_config(env: str = "development") -> Dict:
        """Load environment-specific configuration"""
        env_configs = {
            "development": {
                "database": {"path": "dev_parking_system.db"},
                "plc": {"modbus_host": "localhost"},
                "logging": {"level": "DEBUG"},
                "simulation": {"enabled": True}
            },
            "testing": {
                "database": {"path": ":memory:"},
                "plc": {"modbus_host": "localhost"},
                "logging": {"level": "WARNING"},
                "simulation": {"enabled": True, "entry_rate": 10.0}
            },
            "production": {
                "database": {"path": "parking_system.db", "backup_enabled": True},
                "plc": {"modbus_host": "192.168.1.100"},
                "logging": {"level": "INFO"},
                "simulation": {"enabled": False}
            }
        }
        
        return env_configs.get(env, {})

if __name__ == "__main__":
    # Test configuration manager
    config_manager = ConfigManager("config/test_config.yaml")
    
    # Validate configuration
    errors = config_manager.validate_config()
    if errors:
        print("Configuration errors:")
        for error in errors:
            print(f"  - {error}")
    else:
        print("Configuration is valid")
        
    # Print current configuration
    print("\nCurrent configuration:")
    print(config_manager.export_config('yaml'))
    
    # Test configuration updates
    config_manager.update_config('parking', 'total_levels', 20)
    config_manager.save_config()
    
    print("Configuration updated and saved")
