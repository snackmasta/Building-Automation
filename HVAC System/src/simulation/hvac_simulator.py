#!/usr/bin/env python3
"""
HVAC System Simulator
Simulates a multi-zone HVAC control system with realistic thermal dynamics
and equipment behavior for testing and demonstration purposes.

Author: System Engineer
Date: June 8, 2025
Version: 1.0.0
"""

import time
import random
import math
import configparser
import json
import logging
from datetime import datetime, timedelta
from dataclasses import dataclass
from typing import Dict, List, Optional

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class ZoneData:
    """Data structure for individual zone information"""
    name: str
    temperature: float = 22.0
    setpoint: float = 22.0
    humidity: float = 50.0
    co2_level: int = 400
    occupancy: bool = False
    heating_demand: bool = False
    cooling_demand: bool = False
    air_flow: float = 100.0  # CFM

@dataclass
class EquipmentStatus:
    """Data structure for equipment status"""
    supply_fan_running: bool = False
    supply_fan_speed: float = 0.0
    return_fan_running: bool = False
    return_fan_speed: float = 0.0
    heating_stage_1: bool = False
    heating_stage_2: bool = False
    cooling_stage_1: bool = False
    cooling_stage_2: bool = False
    outside_air_damper: float = 15.0
    economizer_active: bool = False

class HVACSimulator:
    """Main HVAC system simulator class"""
    
    def __init__(self, config_file: str = "config/plc_config.ini"):
        """Initialize the HVAC simulator"""
        self.config = configparser.ConfigParser()
        self.config.read(config_file)
        
        # Initialize zones
        self.zones: Dict[int, ZoneData] = {}
        self.init_zones()
        
        # Initialize equipment
        self.equipment = EquipmentStatus()
        
        # Environmental conditions
        self.outdoor_temperature = 20.0
        self.outdoor_humidity = 60.0
        self.wind_speed = 5.0  # mph
        
        # System variables
        self.system_running = False
        self.emergency_stop = False
        self.fire_alarm = False
        self.energy_consumed = 0.0  # kWh
        self.peak_demand = 0.0  # kW
        
        # Simulation parameters
        self.simulation_speed = 1.0  # 1.0 = real time
        self.thermal_mass = 2.5  # Hours to change 1°C without HVAC
        
        # Data logging
        self.data_log: List[Dict] = []
        self.start_time = datetime.now()
        
        logger.info("HVAC Simulator initialized successfully")
    
    def init_zones(self):
        """Initialize building zones"""
        zone_count = int(self.config.get('ZONES', 'zone_count', fallback='8'))
        
        zone_configs = {
            1: {"name": "Lobby", "temp": 22.0, "setpoint": 22.0},
            2: {"name": "Conference Room", "temp": 23.0, "setpoint": 23.0},
            3: {"name": "Office Area 1", "temp": 22.5, "setpoint": 22.0},
            4: {"name": "Office Area 2", "temp": 21.8, "setpoint": 22.0},
            5: {"name": "Kitchen", "temp": 24.0, "setpoint": 21.0},
            6: {"name": "Server Room", "temp": 19.5, "setpoint": 20.0},
            7: {"name": "Storage", "temp": 18.0, "setpoint": 18.0},
            8: {"name": "Break Room", "temp": 22.2, "setpoint": 22.0}
        }
        
        for i in range(1, zone_count + 1):
            config = zone_configs.get(i, {"name": f"Zone {i}", "temp": 22.0, "setpoint": 22.0})
            self.zones[i] = ZoneData(
                name=config["name"],
                temperature=config["temp"],
                setpoint=config["setpoint"],
                humidity=50.0 + random.uniform(-5, 5),
                co2_level=400 + random.randint(0, 100)
            )
    
    def update_outdoor_conditions(self):
        """Simulate changing outdoor weather conditions"""
        current_hour = datetime.now().hour
        
        # Simulate daily temperature cycle
        base_temp = 20.0  # Base temperature
        daily_variation = 8.0  # Temperature swing
        
        # Simple sinusoidal temperature variation
        self.outdoor_temperature = base_temp + daily_variation * math.sin((current_hour - 6) * math.pi / 12)
        
        # Add some random variation
        self.outdoor_temperature += random.uniform(-2, 2)
        
        # Limit temperature range
        self.outdoor_temperature = max(-10, min(40, self.outdoor_temperature))
        
        # Humidity varies inversely with temperature (simplified)
        self.outdoor_humidity = 80 - (self.outdoor_temperature - 10) * 1.5
        self.outdoor_humidity = max(20, min(90, self.outdoor_humidity))
        
        # Wind speed variation
        self.wind_speed = 5.0 + random.uniform(-2, 5)
    
    def update_occupancy(self):
        """Simulate building occupancy patterns"""
        current_hour = datetime.now().hour
        current_day = datetime.now().weekday()  # 0=Monday, 6=Sunday
        
        # Business hours: 7 AM to 6 PM on weekdays
        if current_day < 5:  # Weekdays
            if 7 <= current_hour <= 18:
                occupancy_probability = 0.8
            elif 6 <= current_hour <= 19:
                occupancy_probability = 0.4
            else:
                occupancy_probability = 0.1
        else:  # Weekends
            if 9 <= current_hour <= 17:
                occupancy_probability = 0.3
            else:
                occupancy_probability = 0.05
        
        # Update zone occupancy
        for zone_id, zone in self.zones.items():
            # Different zones have different occupancy patterns
            if zone.name == "Server Room":
                zone.occupancy = False  # Always unoccupied
            elif zone.name == "Storage":
                zone.occupancy = random.random() < 0.1  # Rarely occupied
            else:
                zone.occupancy = random.random() < occupancy_probability
    
    def update_zone_loads(self):
        """Update internal loads affecting each zone"""
        for zone_id, zone in self.zones.items():
            # CO2 generation based on occupancy
            if zone.occupancy:
                # People generate CO2
                co2_generation = random.randint(50, 150)  # ppm per hour per person
                zone.co2_level += co2_generation // 12  # Per 5-minute interval
                
                # Heat generation from people and equipment
                internal_heat_gain = random.uniform(0.5, 1.5)  # °C per hour
                zone.temperature += internal_heat_gain / 12
            else:
                # CO2 decay when unoccupied
                zone.co2_level = max(350, zone.co2_level - 10)
            
            # Equipment heat gains (simplified)
            if zone.name == "Server Room":
                zone.temperature += 2.0 / 12  # Servers generate heat
            elif zone.name == "Kitchen":
                zone.temperature += random.uniform(0, 1.0) / 12  # Cooking heat
            
            # Limit CO2 levels
            zone.co2_level = min(5000, max(350, zone.co2_level))
    
    def calculate_thermal_dynamics(self):
        """Calculate heat transfer and thermal dynamics"""
        dt = 1.0 / 12.0  # 5-minute time step in hours
        
        for zone_id, zone in self.zones.items():
            # Heat loss/gain to outdoor air (infiltration)
            infiltration_rate = 0.5  # Air changes per hour
            temp_diff = self.outdoor_temperature - zone.temperature
            infiltration_effect = temp_diff * infiltration_rate * dt / self.thermal_mass
            
            # Heat transfer to adjacent zones (simplified)
            adjacent_temp_avg = sum(z.temperature for z in self.zones.values()) / len(self.zones)
            internal_transfer = (adjacent_temp_avg - zone.temperature) * 0.1 * dt
            
            # Apply thermal effects
            zone.temperature += infiltration_effect + internal_transfer
            
            # HVAC system effects (if running)
            if self.system_running and not self.emergency_stop:
                self.apply_hvac_effects(zone)
    
    def apply_hvac_effects(self, zone: ZoneData):
        """Apply HVAC system effects to zone"""
        dt = 1.0 / 12.0  # 5-minute time step in hours
        
        # Supply air temperature calculation
        supply_air_temp = self.outdoor_temperature
        
        # Heating effects
        if self.equipment.heating_stage_1:
            supply_air_temp += 15.0  # First stage heating
        if self.equipment.heating_stage_2:
            supply_air_temp += 10.0  # Second stage heating
        
        # Cooling effects
        if self.equipment.cooling_stage_1:
            supply_air_temp -= 10.0  # First stage cooling
        if self.equipment.cooling_stage_2:
            supply_air_temp -= 8.0   # Second stage cooling
        
        # Economizer effects
        if self.equipment.economizer_active:
            # Free cooling with outside air
            supply_air_temp = self.outdoor_temperature
        
        # Fan operation effects
        if self.equipment.supply_fan_running:
            air_flow_factor = self.equipment.supply_fan_speed / 100.0
            temp_change_rate = (supply_air_temp - zone.temperature) * air_flow_factor * 0.3
            zone.temperature += temp_change_rate * dt
            
            # Fresh air effects on CO2
            fresh_air_percentage = self.equipment.outside_air_damper / 100.0
            co2_reduction = (zone.co2_level - 400) * fresh_air_percentage * 0.1
            zone.co2_level -= int(co2_reduction)
    
    def determine_equipment_demands(self):
        """Determine heating/cooling demands for each zone"""
        for zone_id, zone in self.zones.items():
            deadband = 1.0  # °C
            
            # Heating demand
            if zone.temperature < (zone.setpoint - deadband / 2):
                zone.heating_demand = True
                zone.cooling_demand = False
            # Cooling demand
            elif zone.temperature > (zone.setpoint + deadband / 2):
                zone.cooling_demand = True
                zone.heating_demand = False
            else:
                # In deadband
                zone.heating_demand = False
                zone.cooling_demand = False
    
    def control_equipment(self):
        """Simulate equipment control logic"""
        if self.emergency_stop or self.fire_alarm:
            # Emergency shutdown
            self.equipment.supply_fan_running = False
            self.equipment.return_fan_running = False
            self.equipment.heating_stage_1 = False
            self.equipment.heating_stage_2 = False
            self.equipment.cooling_stage_1 = False
            self.equipment.cooling_stage_2 = False
            self.equipment.outside_air_damper = 0.0
            return
        
        # Check for any zone demands
        any_heating = any(zone.heating_demand for zone in self.zones.values())
        any_cooling = any(zone.cooling_demand for zone in self.zones.values())
        
        # Fan control
        if any_heating or any_cooling:
            self.equipment.supply_fan_running = True
            self.equipment.return_fan_running = True
            
            # Calculate fan speed based on demand
            heating_zones = sum(1 for zone in self.zones.values() if zone.heating_demand)
            cooling_zones = sum(1 for zone in self.zones.values() if zone.cooling_demand)
            total_demand = (heating_zones + cooling_zones) / len(self.zones)
            
            self.equipment.supply_fan_speed = max(30.0, min(100.0, total_demand * 70.0 + 30.0))
            self.equipment.return_fan_speed = self.equipment.supply_fan_speed * 0.9
        else:
            self.equipment.supply_fan_running = False
            self.equipment.return_fan_running = False
            self.equipment.supply_fan_speed = 0.0
            self.equipment.return_fan_speed = 0.0
        
        # Heating control
        if any_heating:
            self.equipment.heating_stage_1 = True
            heating_count = sum(1 for zone in self.zones.values() if zone.heating_demand)
            if heating_count > len(self.zones) * 0.6:  # High demand
                self.equipment.heating_stage_2 = True
            else:
                self.equipment.heating_stage_2 = False
        else:
            self.equipment.heating_stage_1 = False
            self.equipment.heating_stage_2 = False
        
        # Cooling control
        if any_cooling:
            self.equipment.cooling_stage_1 = True
            cooling_count = sum(1 for zone in self.zones.values() if zone.cooling_demand)
            if cooling_count > len(self.zones) * 0.6:  # High demand
                self.equipment.cooling_stage_2 = True
            else:
                self.equipment.cooling_stage_2 = False
        else:
            self.equipment.cooling_stage_1 = False
            self.equipment.cooling_stage_2 = False
        
        # Economizer control
        if any_cooling and self.outdoor_temperature < 18.0:
            self.equipment.economizer_active = True
            self.equipment.outside_air_damper = min(100.0, 80.0)
        else:
            self.equipment.economizer_active = False
            self.equipment.outside_air_damper = 15.0  # Minimum fresh air
    
    def calculate_energy_consumption(self):
        """Calculate system energy consumption"""
        power_consumption = 0.0
        
        # Fan power consumption
        if self.equipment.supply_fan_running:
            fan_power = 7.5 * (self.equipment.supply_fan_speed / 100.0) ** 3  # kW
            power_consumption += fan_power
        
        if self.equipment.return_fan_running:
            fan_power = 5.0 * (self.equipment.return_fan_speed / 100.0) ** 3  # kW
            power_consumption += fan_power
        
        # Heating power
        if self.equipment.heating_stage_1:
            power_consumption += 15.0  # kW
        if self.equipment.heating_stage_2:
            power_consumption += 15.0  # kW
        
        # Cooling power
        if self.equipment.cooling_stage_1:
            power_consumption += 20.0  # kW
        if self.equipment.cooling_stage_2:
            power_consumption += 20.0  # kW
        
        # Update energy consumption (5-minute intervals)
        energy_increment = power_consumption * (5.0 / 60.0)  # kWh
        self.energy_consumed += energy_increment
        
        # Update peak demand
        if power_consumption > self.peak_demand:
            self.peak_demand = power_consumption
    
    def log_data(self):
        """Log system data for analysis"""
        timestamp = datetime.now()
        
        data_point = {
            'timestamp': timestamp.isoformat(),
            'outdoor_temp': round(self.outdoor_temperature, 1),
            'outdoor_humidity': round(self.outdoor_humidity, 1),
            'system_running': self.system_running,
            'emergency_stop': self.emergency_stop,
            'energy_consumed': round(self.energy_consumed, 2),
            'peak_demand': round(self.peak_demand, 1),
            'equipment': {
                'supply_fan_running': self.equipment.supply_fan_running,
                'supply_fan_speed': round(self.equipment.supply_fan_speed, 1),
                'heating_stage_1': self.equipment.heating_stage_1,
                'heating_stage_2': self.equipment.heating_stage_2,
                'cooling_stage_1': self.equipment.cooling_stage_1,
                'cooling_stage_2': self.equipment.cooling_stage_2,
                'outside_air_damper': round(self.equipment.outside_air_damper, 1)
            },
            'zones': {}
        }
        
        for zone_id, zone in self.zones.items():
            data_point['zones'][zone_id] = {
                'name': zone.name,
                'temperature': round(zone.temperature, 1),
                'setpoint': round(zone.setpoint, 1),
                'humidity': round(zone.humidity, 1),
                'co2_level': zone.co2_level,
                'occupancy': zone.occupancy,
                'heating_demand': zone.heating_demand,
                'cooling_demand': zone.cooling_demand
            }
        
        self.data_log.append(data_point)
        
        # Keep only last 288 data points (24 hours at 5-minute intervals)
        if len(self.data_log) > 288:
            self.data_log.pop(0)
    
    def save_data_log(self, filename: str = None):
        """Save data log to file"""
        if filename is None:
            filename = f"logs/hvac_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        try:
            with open(filename, 'w') as f:
                json.dump(self.data_log, f, indent=2)
            logger.info(f"Data log saved to {filename}")
        except Exception as e:
            logger.error(f"Failed to save data log: {e}")
    
    def get_system_status(self) -> Dict:
        """Get current system status for HMI"""
        return {
            'timestamp': datetime.now().isoformat(),
            'system_running': self.system_running,
            'emergency_stop': self.emergency_stop,
            'fire_alarm': self.fire_alarm,
            'outdoor_conditions': {
                'temperature': round(self.outdoor_temperature, 1),
                'humidity': round(self.outdoor_humidity, 1),
                'wind_speed': round(self.wind_speed, 1)
            },
            'energy': {
                'consumed_today': round(self.energy_consumed, 2),
                'peak_demand': round(self.peak_demand, 1)
            },
            'equipment': self.equipment.__dict__,
            'zones': {zone_id: zone.__dict__ for zone_id, zone in self.zones.items()}
        }
    
    def run_simulation_step(self):
        """Run one simulation time step"""
        # Update environmental conditions
        self.update_outdoor_conditions()
        self.update_occupancy()
        self.update_zone_loads()
        
        # Calculate thermal dynamics
        self.calculate_thermal_dynamics()
        
        # Determine equipment demands
        self.determine_equipment_demands()
        
        # Control equipment
        if self.system_running:
            self.control_equipment()
        
        # Calculate energy consumption
        self.calculate_energy_consumption()
        
        # Log data
        self.log_data()
    
    def run(self, duration_minutes: int = None):
        """Alias for run_continuous method for compatibility"""
        return self.run_continuous(duration_minutes)
    
    def run_continuous(self, duration_minutes: int = None):
        """Run continuous simulation"""
        logger.info("Starting HVAC simulation...")
        self.system_running = True
        
        step_count = 0
        start_time = time.time()
        
        try:
            while True:
                step_start = time.time()
                
                # Run simulation step
                self.run_simulation_step()
                
                step_count += 1
                
                # Print status every 12 steps (1 hour simulation time)
                if step_count % 12 == 0:
                    elapsed_real = time.time() - start_time
                    elapsed_sim = step_count * 5  # minutes
                    logger.info(f"Simulation time: {elapsed_sim} min, Real time: {elapsed_real:.1f}s")
                    self.print_status()
                
                # Check duration limit
                if duration_minutes and step_count * 5 >= duration_minutes:
                    break
                
                # Sleep to maintain simulation timing
                step_time = time.time() - step_start
                sleep_time = (5 * 60 / self.simulation_speed) - step_time  # 5 minutes per step
                if sleep_time > 0:
                    time.sleep(sleep_time)
                
        except KeyboardInterrupt:
            logger.info("Simulation stopped by user")
        finally:
            self.save_data_log()
            logger.info("HVAC simulation ended")
    
    def print_status(self):
        """Print current system status"""
        print("\n" + "="*60)
        print(f"HVAC System Status - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*60)
        print(f"Outdoor: {self.outdoor_temperature:.1f}°C, {self.outdoor_humidity:.1f}% RH")
        print(f"System: {'RUNNING' if self.system_running else 'STOPPED'}")
        print(f"Energy: {self.energy_consumed:.1f} kWh, Peak: {self.peak_demand:.1f} kW")
        print("\nZone Status:")
        for zone_id, zone in self.zones.items():
            status = "🔥" if zone.heating_demand else "❄️" if zone.cooling_demand else "✓"
            occupancy = "👥" if zone.occupancy else "  "
            print(f"  {zone_id}: {zone.name:15} {zone.temperature:5.1f}°C -> {zone.setpoint:4.1f}°C {status} {occupancy}")
        
        print(f"\nEquipment:")
        print(f"  Supply Fan: {'ON' if self.equipment.supply_fan_running else 'OFF':3} ({self.equipment.supply_fan_speed:3.0f}%)")
        print(f"  Heating:    {'ST1' if self.equipment.heating_stage_1 else '   '} {'ST2' if self.equipment.heating_stage_2 else '   '}")
        print(f"  Cooling:    {'ST1' if self.equipment.cooling_stage_1 else '   '} {'ST2' if self.equipment.cooling_stage_2 else '   '}")
        print(f"  Outside Air: {self.equipment.outside_air_damper:3.0f}%")


def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(description='HVAC System Simulator')
    parser.add_argument('--duration', type=int, help='Simulation duration in minutes')
    parser.add_argument('--speed', type=float, default=1.0, help='Simulation speed multiplier')
    parser.add_argument('--config', type=str, default='config/plc_config.ini', help='Configuration file')
    
    args = parser.parse_args()
    
    # Create and run simulator
    simulator = HVACSimulator(args.config)
    simulator.simulation_speed = args.speed
    
    # Initial status
    simulator.print_status()
    
    # Run simulation
    simulator.run_continuous(args.duration)


if __name__ == "__main__":
    main()
