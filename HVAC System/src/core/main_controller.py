#!/usr/bin/env python3
"""
HVAC Main Controller
Central control system for HVAC operations
"""

import sys
import time
import json
import configparser
import logging
from datetime import datetime
from pathlib import Path

class HVACController:
    def __init__(self, config_path=None):
        self.base_path = Path(__file__).parent.parent.parent  # Go up to project root
        self.config_path = config_path or self.base_path / 'config' / 'plc_config.ini'
        self.running = False
        self.config = None
        self.zones = {}
        self.equipment_status = {}
        self.system_status = {
            'startup_time': None,
            'running': False,
            'error_count': 0,
            'last_update': None
        }
        
        # Setup logging
        self.setup_logging()
        self.logger = logging.getLogger(__name__)
        
    def setup_logging(self):
        """Setup logging configuration"""
        log_dir = self.base_path / 'logs'
        log_dir.mkdir(exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_dir / 'hvac_controller.log'),
                logging.StreamHandler(sys.stdout)
            ]
        )
    
    def load_configuration(self):
        """Load system configuration"""
        try:
            if not self.config_path.exists():
                raise FileNotFoundError(f"Configuration file not found: {self.config_path}")
            
            self.config = configparser.ConfigParser()
            self.config.read(self.config_path)
            
            self.logger.info("Configuration loaded successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to load configuration: {e}")
            return False
    
    def initialize_zones(self):
        """Initialize zone control"""
        try:
            zone_count = int(self.config.get('ZONES', 'zone_count', fallback=8))
            
            for i in range(1, zone_count + 1):
                zone_name = self.config.get('ZONES', f'zone_{i}_name', fallback=f'Zone {i}')
                self.zones[f'zone_{i}'] = {
                    'name': zone_name,
                    'temperature': 22.0,
                    'setpoint_heating': float(self.config.get('TEMPERATURE_CONTROL', 'default_temp_heating', fallback=21.0)),
                    'setpoint_cooling': float(self.config.get('TEMPERATURE_CONTROL', 'default_temp_cooling', fallback=24.0)),
                    'humidity': 45.0,
                    'co2': 400,
                    'occupied': False,
                    'damper_position': 50,
                    'fan_speed': 30
                }
            
            self.logger.info(f"Initialized {zone_count} zones")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to initialize zones: {e}")
            return False
    
    def initialize_equipment(self):
        """Initialize equipment status"""
        try:
            self.equipment_status = {
                'supply_fan': {'running': False, 'speed': 0, 'vfd_enabled': True},
                'return_fan': {'running': False, 'speed': 0, 'vfd_enabled': True},
                'cooling_coil': {'stages': 2, 'active_stages': 0, 'capacity': 0},
                'heating_coil': {'stages': 2, 'active_stages': 0, 'capacity': 0},
                'economizer': {'enabled': True, 'position': 0, 'mode': 'auto'},
                'heat_recovery': {'enabled': True, 'effectiveness': 0.75, 'bypass': False}
            }
            
            self.logger.info("Equipment initialized successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to initialize equipment: {e}")
            return False
    
    def update_system_status(self):
        """Update system status"""
        self.system_status['last_update'] = datetime.now().isoformat()
        self.system_status['running'] = self.running
        
        # Save status to file
        try:
            status_file = self.base_path / 'data' / 'system_status.json'
            status_file.parent.mkdir(exist_ok=True)
            
            with open(status_file, 'w') as f:
                json.dump({
                    'system_status': self.system_status,
                    'zones': self.zones,
                    'equipment': self.equipment_status
                }, f, indent=2)
                
        except Exception as e:
            self.logger.error(f"Failed to save system status: {e}")
    
    def control_loop(self):
        """Main control loop"""
        self.logger.info("Starting control loop")
        
        while self.running:
            try:
                # Simulate temperature control
                for zone_id, zone_data in self.zones.items():
                    # Simple temperature simulation
                    current_temp = zone_data['temperature']
                    heating_sp = zone_data['setpoint_heating']
                    cooling_sp = zone_data['setpoint_cooling']
                    
                    # Basic control logic
                    if current_temp < heating_sp - 0.5:
                        # Need heating
                        zone_data['temperature'] += 0.1
                    elif current_temp > cooling_sp + 0.5:
                        # Need cooling
                        zone_data['temperature'] -= 0.1
                    
                    # Update other parameters
                    zone_data['humidity'] = max(30, min(70, zone_data['humidity'] + (0.5 - 1.0) * 0.1))
                    zone_data['co2'] = max(400, min(1000, zone_data['co2'] + (5 - 10) * 1))
                
                # Update equipment status
                self.equipment_status['supply_fan']['running'] = True
                self.equipment_status['supply_fan']['speed'] = 75
                
                # Update system status
                self.update_system_status()
                
                # Control loop delay
                time.sleep(1)
                
            except KeyboardInterrupt:
                self.logger.info("Shutdown requested by user")
                break
            except Exception as e:
                self.logger.error(f"Error in control loop: {e}")
                self.system_status['error_count'] += 1
                time.sleep(5)  # Wait before retrying
    
    def start(self):
        """Start the HVAC controller"""
        self.logger.info("Starting HVAC Controller")
        
        # Load configuration
        if not self.load_configuration():
            self.logger.error("Failed to load configuration. Exiting.")
            return False
        
        # Initialize subsystems
        if not self.initialize_zones():
            self.logger.error("Failed to initialize zones. Exiting.")
            return False
        
        if not self.initialize_equipment():
            self.logger.error("Failed to initialize equipment. Exiting.")
            return False
        
        # Set running state
        self.running = True
        self.system_status['startup_time'] = datetime.now().isoformat()
        self.system_status['running'] = True
        
        self.logger.info("HVAC Controller started successfully")
        
        # Start control loop
        self.control_loop()
        
        return True
    
    def stop(self):
        """Stop the HVAC controller"""
        self.logger.info("Stopping HVAC Controller")
        self.running = False
        self.system_status['running'] = False
        self.update_system_status()

def main():
    """Main function"""
    print("HVAC Main Controller Starting...")
    
    controller = HVACController()
    
    try:
        controller.start()
    except KeyboardInterrupt:
        print("\nShutdown requested...")
    finally:
        controller.stop()
        print("HVAC Controller stopped.")

if __name__ == "__main__":
    main()
