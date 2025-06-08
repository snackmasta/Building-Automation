"""
Automated Car Parking System - Parking Simulator
Real-time simulation of parking operations with vehicle generation and database integration
"""

import random
import time
import threading
import json
import sqlite3
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional, Tuple
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class Vehicle:
    """Vehicle data structure"""
    id: str
    plate_number: str
    vehicle_type: str  # 'car', 'suv', 'truck', 'motorcycle'
    length: float
    width: float
    height: float
    owner_name: str
    phone_number: str
    entry_time: datetime
    exit_time: Optional[datetime] = None
    parking_space: Optional[int] = None
    payment_amount: float = 0.0
    payment_method: str = ""
    
class VehicleGenerator:
    """Generates realistic vehicle data"""
    
    VEHICLE_TYPES = {
        'car': {'length': (4.2, 4.8), 'width': (1.7, 1.9), 'height': (1.4, 1.6), 'weight': 0.7},
        'suv': {'length': (4.6, 5.2), 'width': (1.8, 2.0), 'height': (1.6, 1.9), 'weight': 0.2},
        'truck': {'length': (5.0, 6.5), 'width': (1.9, 2.2), 'height': (1.8, 2.2), 'weight': 0.08},
        'motorcycle': {'length': (2.0, 2.5), 'width': (0.7, 0.9), 'height': (1.0, 1.3), 'weight': 0.02}
    }
    
    NAMES = [
        "John Smith", "Sarah Johnson", "Michael Brown", "Emily Davis", "David Wilson",
        "Jessica Garcia", "Robert Miller", "Ashley Martinez", "Christopher Anderson", "Amanda Taylor"
    ]
    
    def __init__(self):
        self.vehicle_counter = 1
        
    def generate_vehicle(self) -> Vehicle:
        """Generate a random vehicle"""
        # Select vehicle type based on weights
        vehicle_type = random.choices(
            list(self.VEHICLE_TYPES.keys()),
            weights=[v['weight'] for v in self.VEHICLE_TYPES.values()]
        )[0]
        
        # Generate dimensions within type ranges
        type_specs = self.VEHICLE_TYPES[vehicle_type]
        length = random.uniform(*type_specs['length'])
        width = random.uniform(*type_specs['width'])
        height = random.uniform(*type_specs['height'])
        
        # Generate vehicle data
        vehicle_id = f"V{self.vehicle_counter:06d}"
        plate_number = f"{random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')}{random.randint(100, 999)}{random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')}{random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')}{random.randint(10, 99)}"
        owner_name = random.choice(self.NAMES)
        phone_number = f"555-{random.randint(100, 999)}-{random.randint(1000, 9999)}"
        
        self.vehicle_counter += 1
        
        return Vehicle(
            id=vehicle_id,
            plate_number=plate_number,
            vehicle_type=vehicle_type,
            length=length,
            width=width,
            height=height,
            owner_name=owner_name,
            phone_number=phone_number,
            entry_time=datetime.now()
        )

class ParkingSimulator:
    """Main parking system simulator"""
    
    def __init__(self, db_path: str = "parking_system.db"):
        self.db_path = db_path
        self.vehicle_generator = VehicleGenerator()
        self.running = False
        self.simulation_thread = None
        
        # Simulation parameters
        self.entry_rate = 5  # vehicles per hour
        self.exit_rate = 3   # vehicles per hour
        self.peak_hours = [(7, 9), (17, 19)]  # Peak traffic hours
        self.peak_multiplier = 3.0
        
        # System state
        self.total_spaces = 300
        self.occupied_spaces = set()
        self.parked_vehicles = {}
        self.waiting_queue = []
        self.statistics = {
            'total_entries': 0,
            'total_exits': 0,
            'total_revenue': 0.0,
            'average_stay_time': 0.0,
            'occupancy_rate': 0.0
        }
        
        # Initialize database
        self._init_database()
        
    def _init_database(self):
        """Initialize SQLite database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Create tables
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS vehicles (
                    id TEXT PRIMARY KEY,
                    plate_number TEXT UNIQUE,
                    vehicle_type TEXT,
                    length REAL,
                    width REAL,
                    height REAL,
                    owner_name TEXT,
                    phone_number TEXT,
                    entry_time TIMESTAMP,
                    exit_time TIMESTAMP,
                    parking_space INTEGER,
                    payment_amount REAL,
                    payment_method TEXT
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS parking_spaces (
                    space_id INTEGER PRIMARY KEY,
                    level INTEGER,
                    position INTEGER,
                    vehicle_id TEXT,
                    occupied BOOLEAN DEFAULT FALSE,
                    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (vehicle_id) REFERENCES vehicles (id)
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS transactions (
                    transaction_id TEXT PRIMARY KEY,
                    vehicle_id TEXT,
                    amount REAL,
                    payment_method TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    status TEXT,
                    FOREIGN KEY (vehicle_id) REFERENCES vehicles (id)
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS system_events (
                    event_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    event_type TEXT,
                    description TEXT,
                    severity TEXT
                )
            """)
            
            # Initialize parking spaces if empty
            cursor.execute("SELECT COUNT(*) FROM parking_spaces")
            if cursor.fetchone()[0] == 0:
                spaces = []
                for level in range(1, 16):  # 15 levels
                    for position in range(1, 21):  # 20 spaces per level
                        space_id = (level - 1) * 20 + position
                        spaces.append((space_id, level, position, None, False))
                
                cursor.executemany(
                    "INSERT INTO parking_spaces (space_id, level, position, vehicle_id, occupied) VALUES (?, ?, ?, ?, ?)",
                    spaces
                )
            
            conn.commit()
            conn.close()
            logger.info("Database initialized successfully")
            
        except Exception as e:
            logger.error(f"Database initialization error: {e}")
            
    def _is_peak_hour(self) -> bool:
        """Check if current time is peak hour"""
        current_hour = datetime.now().hour
        for start, end in self.peak_hours:
            if start <= current_hour <= end:
                return True
        return False
        
    def _get_entry_rate(self) -> float:
        """Get current entry rate based on time"""
        base_rate = self.entry_rate
        if self._is_peak_hour():
            return base_rate * self.peak_multiplier
        return base_rate
        
    def _get_exit_rate(self) -> float:
        """Get current exit rate based on time"""
        base_rate = self.exit_rate
        if self._is_peak_hour():
            return base_rate * self.peak_multiplier
        return base_rate
        
    def _find_available_space(self, vehicle: Vehicle) -> Optional[int]:
        """Find available parking space for vehicle"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get available spaces
            cursor.execute("SELECT space_id FROM parking_spaces WHERE occupied = FALSE ORDER BY space_id")
            available_spaces = [row[0] for row in cursor.fetchall()]
            
            if available_spaces:
                # Simple allocation - first available space
                space_id = available_spaces[0]
                
                # Mark space as occupied
                cursor.execute(
                    "UPDATE parking_spaces SET vehicle_id = ?, occupied = TRUE, last_updated = CURRENT_TIMESTAMP WHERE space_id = ?",
                    (vehicle.id, space_id)
                )
                
                conn.commit()
                conn.close()
                return space_id
            
            conn.close()
            return None
            
        except Exception as e:
            logger.error(f"Error finding parking space: {e}")
            return None
            
    def _release_space(self, space_id: int):
        """Release parking space"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute(
                "UPDATE parking_spaces SET vehicle_id = NULL, occupied = FALSE, last_updated = CURRENT_TIMESTAMP WHERE space_id = ?",
                (space_id,)
            )
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"Error releasing parking space: {e}")
            
    def _calculate_parking_fee(self, vehicle: Vehicle) -> float:
        """Calculate parking fee based on duration and vehicle type"""
        if vehicle.exit_time is None:
            return 0.0
            
        duration = vehicle.exit_time - vehicle.entry_time
        hours = max(1, duration.total_seconds() / 3600)  # Minimum 1 hour
        
        # Base rates by vehicle type
        base_rates = {
            'car': 3.0,
            'suv': 4.0,
            'truck': 6.0,
            'motorcycle': 2.0
        }
        
        base_rate = base_rates.get(vehicle.vehicle_type, 3.0)
        return round(base_rate * hours, 2)
        
    def _process_payment(self, vehicle: Vehicle) -> bool:
        """Simulate payment processing"""
        payment_methods = ['cash', 'credit_card', 'debit_card', 'mobile_pay', 'rfid_card']
        vehicle.payment_method = random.choice(payment_methods)
        
        # 95% success rate
        success = random.random() < 0.95
        
        if success:
            try:
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                
                transaction_id = f"T{int(time.time())}{random.randint(100, 999)}"
                cursor.execute(
                    "INSERT INTO transactions (transaction_id, vehicle_id, amount, payment_method, status) VALUES (?, ?, ?, ?, ?)",
                    (transaction_id, vehicle.id, vehicle.payment_amount, vehicle.payment_method, 'completed')
                )
                
                conn.commit()
                conn.close()
                
                self.statistics['total_revenue'] += vehicle.payment_amount
                logger.info(f"Payment processed: {vehicle.plate_number} - ${vehicle.payment_amount}")
                
            except Exception as e:
                logger.error(f"Payment processing error: {e}")
                return False
                
        return success
        
    def _log_event(self, event_type: str, description: str, severity: str = 'info'):
        """Log system event to database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute(
                "INSERT INTO system_events (event_type, description, severity) VALUES (?, ?, ?)",
                (event_type, description, severity)
            )
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"Event logging error: {e}")
            
    def vehicle_entry(self) -> bool:
        """Simulate vehicle entry"""
        if len(self.occupied_spaces) >= self.total_spaces:
            logger.warning("Parking lot full - vehicle entry denied")
            return False
            
        vehicle = self.vehicle_generator.generate_vehicle()
        
        # Find parking space
        space_id = self._find_available_space(vehicle)
        if space_id is None:
            self.waiting_queue.append(vehicle)
            self._log_event('vehicle_queued', f"Vehicle {vehicle.plate_number} added to waiting queue", 'warning')
            return False
            
        vehicle.parking_space = space_id
        self.occupied_spaces.add(space_id)
        self.parked_vehicles[vehicle.id] = vehicle
        
        # Save to database
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute(
                "INSERT INTO vehicles (id, plate_number, vehicle_type, length, width, height, owner_name, phone_number, entry_time, parking_space) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (vehicle.id, vehicle.plate_number, vehicle.vehicle_type, vehicle.length, vehicle.width, vehicle.height,
                 vehicle.owner_name, vehicle.phone_number, vehicle.entry_time, vehicle.parking_space)
            )
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"Database error during entry: {e}")
            
        self.statistics['total_entries'] += 1
        self._log_event('vehicle_entry', f"Vehicle {vehicle.plate_number} entered - Space {space_id}")
        logger.info(f"Vehicle entry: {vehicle.plate_number} -> Space {space_id}")
        
        return True
        
    def vehicle_exit(self) -> bool:
        """Simulate vehicle exit"""
        if not self.parked_vehicles:
            return False
            
        # Select random parked vehicle
        vehicle_id = random.choice(list(self.parked_vehicles.keys()))
        vehicle = self.parked_vehicles[vehicle_id]
        
        # Set exit time and calculate fee
        vehicle.exit_time = datetime.now()
        vehicle.payment_amount = self._calculate_parking_fee(vehicle)
        
        # Process payment
        if not self._process_payment(vehicle):
            self._log_event('payment_failed', f"Payment failed for vehicle {vehicle.plate_number}", 'error')
            return False
            
        # Release parking space
        if vehicle.parking_space:
            self._release_space(vehicle.parking_space)
            self.occupied_spaces.discard(vehicle.parking_space)
            
        # Update database
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute(
                "UPDATE vehicles SET exit_time = ?, payment_amount = ?, payment_method = ? WHERE id = ?",
                (vehicle.exit_time, vehicle.payment_amount, vehicle.payment_method, vehicle.id)
            )
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"Database error during exit: {e}")
            
        # Remove from parked vehicles
        del self.parked_vehicles[vehicle_id]
        
        # Process waiting queue
        if self.waiting_queue:
            waiting_vehicle = self.waiting_queue.pop(0)
            space_id = self._find_available_space(waiting_vehicle)
            if space_id:
                waiting_vehicle.parking_space = space_id
                self.occupied_spaces.add(space_id)
                self.parked_vehicles[waiting_vehicle.id] = waiting_vehicle
                self._log_event('vehicle_from_queue', f"Vehicle {waiting_vehicle.plate_number} moved from queue to space {space_id}")
                
        self.statistics['total_exits'] += 1
        self._log_event('vehicle_exit', f"Vehicle {vehicle.plate_number} exited - Payment: ${vehicle.payment_amount}")
        logger.info(f"Vehicle exit: {vehicle.plate_number} - Payment: ${vehicle.payment_amount}")
        
        return True
        
    def _update_statistics(self):
        """Update system statistics"""
        if self.statistics['total_exits'] > 0:
            # Calculate average stay time
            try:
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                
                cursor.execute("""
                    SELECT AVG((julianday(exit_time) - julianday(entry_time)) * 24) as avg_hours
                    FROM vehicles 
                    WHERE exit_time IS NOT NULL
                """)
                
                result = cursor.fetchone()
                if result[0]:
                    self.statistics['average_stay_time'] = round(result[0], 2)
                    
                conn.close()
                
            except Exception as e:
                logger.error(f"Statistics calculation error: {e}")
                
        # Calculate occupancy rate
        self.statistics['occupancy_rate'] = round((len(self.occupied_spaces) / self.total_spaces) * 100, 1)
        
    def get_system_status(self) -> Dict:
        """Get current system status"""
        self._update_statistics()
        
        return {
            'timestamp': datetime.now().isoformat(),
            'total_spaces': self.total_spaces,
            'occupied_spaces': len(self.occupied_spaces),
            'available_spaces': self.total_spaces - len(self.occupied_spaces),
            'waiting_queue': len(self.waiting_queue),
            'statistics': self.statistics,
            'is_peak_hour': self._is_peak_hour(),
            'entry_rate': self._get_entry_rate(),
            'exit_rate': self._get_exit_rate()
        }
        
    def get_parking_grid(self) -> List[Dict]:
        """Get parking grid status"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT ps.space_id, ps.level, ps.position, ps.occupied, 
                       v.plate_number, v.vehicle_type, v.entry_time
                FROM parking_spaces ps
                LEFT JOIN vehicles v ON ps.vehicle_id = v.id AND v.exit_time IS NULL
                ORDER BY ps.space_id
            """)
            
            spaces = []
            for row in cursor.fetchall():
                space = {
                    'space_id': row[0],
                    'level': row[1],
                    'position': row[2],
                    'occupied': bool(row[3]),
                    'vehicle': {
                        'plate_number': row[4],
                        'vehicle_type': row[5],
                        'entry_time': row[6]
                    } if row[4] else None
                }
                spaces.append(space)
                
            conn.close()
            return spaces
            
        except Exception as e:
            logger.error(f"Error getting parking grid: {e}")
            return []
            
    def _simulation_loop(self):
        """Main simulation loop"""
        logger.info("Parking simulation started")
        
        while self.running:
            try:
                # Calculate probabilities based on rates
                entry_prob = self._get_entry_rate() / 3600  # Per second
                exit_prob = self._get_exit_rate() / 3600    # Per second
                
                # Vehicle entry
                if random.random() < entry_prob:
                    self.vehicle_entry()
                    
                # Vehicle exit
                if random.random() < exit_prob:
                    self.vehicle_exit()
                    
                # Update statistics periodically
                if int(time.time()) % 60 == 0:  # Every minute
                    self._update_statistics()
                    
                time.sleep(1)  # 1 second simulation step
                
            except Exception as e:
                logger.error(f"Simulation error: {e}")
                time.sleep(1)
                
        logger.info("Parking simulation stopped")
        
    def start_simulation(self):
        """Start the parking simulation"""
        if not self.running:
            self.running = True
            self.simulation_thread = threading.Thread(target=self._simulation_loop)
            self.simulation_thread.daemon = True
            self.simulation_thread.start()
            self._log_event('simulation_start', "Parking simulation started")
            
    def stop_simulation(self):
        """Stop the parking simulation"""
        if self.running:
            self.running = False
            if self.simulation_thread:
                self.simulation_thread.join()
            self._log_event('simulation_stop', "Parking simulation stopped")
            
    def clear_database(self):
        """Clear all simulation data"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("DELETE FROM vehicles")
            cursor.execute("DELETE FROM transactions")
            cursor.execute("DELETE FROM system_events")
            cursor.execute("UPDATE parking_spaces SET vehicle_id = NULL, occupied = FALSE")
            
            conn.commit()
            conn.close()
            
            # Reset simulation state
            self.occupied_spaces.clear()
            self.parked_vehicles.clear()
            self.waiting_queue.clear()
            self.statistics = {
                'total_entries': 0,
                'total_exits': 0,
                'total_revenue': 0.0,
                'average_stay_time': 0.0,
                'occupancy_rate': 0.0
            }
            
            logger.info("Database cleared successfully")
            
        except Exception as e:
            logger.error(f"Error clearing database: {e}")

if __name__ == "__main__":
    # Create and run simulator
    simulator = ParkingSimulator()
    
    try:
        simulator.start_simulation()
        
        # Run for demo
        while True:
            status = simulator.get_system_status()
            print(f"\nSystem Status - {status['timestamp']}")
            print(f"Occupied: {status['occupied_spaces']}/{status['total_spaces']} ({status['statistics']['occupancy_rate']}%)")
            print(f"Queue: {status['waiting_queue']} vehicles")
            print(f"Revenue: ${status['statistics']['total_revenue']}")
            print(f"Entries: {status['statistics']['total_entries']}, Exits: {status['statistics']['total_exits']}")
            
            time.sleep(10)
            
    except KeyboardInterrupt:
        print("\nStopping simulation...")
        simulator.stop_simulation()
