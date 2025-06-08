"""
Database Management System for Automated Car Parking System
Handles all database operations, data integrity, and communication protocols
"""

import sqlite3
import json
import logging
import threading
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from contextlib import contextmanager
import hashlib
import uuid

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatabaseManager:
    """Central database management system"""
    
    def __init__(self, db_path: str = "parking_system.db"):
        self.db_path = db_path
        self.connection_pool = []
        self.max_connections = 10
        self.lock = threading.Lock()
        
        # Initialize database
        self._init_database()
        self._init_connection_pool()
        
    def _init_connection_pool(self):
        """Initialize database connection pool"""
        with self.lock:
            for _ in range(self.max_connections):
                conn = sqlite3.connect(self.db_path, check_same_thread=False)
                conn.row_factory = sqlite3.Row  # Enable dict-like access
                self.connection_pool.append(conn)
                
    @contextmanager
    def get_connection(self):
        """Get database connection from pool"""
        with self.lock:
            if self.connection_pool:
                conn = self.connection_pool.pop()
            else:
                conn = sqlite3.connect(self.db_path, check_same_thread=False)
                conn.row_factory = sqlite3.Row
                
        try:
            yield conn
        finally:
            with self.lock:
                if len(self.connection_pool) < self.max_connections:
                    self.connection_pool.append(conn)
                else:
                    conn.close()
                    
    def _init_database(self):
        """Initialize database schema"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Enable foreign keys
                cursor.execute("PRAGMA foreign_keys = ON")
                
                # Vehicles table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS vehicles (
                        id TEXT PRIMARY KEY,
                        plate_number TEXT UNIQUE NOT NULL,
                        vehicle_type TEXT NOT NULL,
                        length REAL NOT NULL,
                        width REAL NOT NULL,
                        height REAL NOT NULL,
                        owner_name TEXT,
                        phone_number TEXT,
                        email TEXT,
                        entry_time TIMESTAMP NOT NULL,
                        exit_time TIMESTAMP,
                        parking_space INTEGER,
                        payment_amount REAL DEFAULT 0.0,
                        payment_method TEXT,
                        status TEXT DEFAULT 'active',
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                # Parking spaces table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS parking_spaces (
                        space_id INTEGER PRIMARY KEY,
                        level INTEGER NOT NULL,
                        position INTEGER NOT NULL,
                        vehicle_id TEXT,
                        occupied BOOLEAN DEFAULT FALSE,
                        reserved BOOLEAN DEFAULT FALSE,
                        maintenance BOOLEAN DEFAULT FALSE,
                        space_type TEXT DEFAULT 'standard',
                        max_length REAL DEFAULT 5.0,
                        max_width REAL DEFAULT 2.0,
                        max_height REAL DEFAULT 2.2,
                        last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (vehicle_id) REFERENCES vehicles (id)
                    )
                """)
                
                # Transactions table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS transactions (
                        transaction_id TEXT PRIMARY KEY,
                        vehicle_id TEXT NOT NULL,
                        amount REAL NOT NULL,
                        payment_method TEXT NOT NULL,
                        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        status TEXT DEFAULT 'pending',
                        reference_number TEXT,
                        receipt_number TEXT,
                        discount_applied REAL DEFAULT 0.0,
                        tax_amount REAL DEFAULT 0.0,
                        FOREIGN KEY (vehicle_id) REFERENCES vehicles (id)
                    )
                """)
                
                # System events table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS system_events (
                        event_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        event_type TEXT NOT NULL,
                        description TEXT NOT NULL,
                        severity TEXT DEFAULT 'info',
                        source TEXT,
                        user_id TEXT,
                        data TEXT
                    )
                """)
                
                # Users table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                        user_id TEXT PRIMARY KEY,
                        username TEXT UNIQUE NOT NULL,
                        password_hash TEXT NOT NULL,
                        salt TEXT NOT NULL,
                        role TEXT DEFAULT 'operator',
                        full_name TEXT,
                        email TEXT,
                        phone TEXT,
                        active BOOLEAN DEFAULT TRUE,
                        last_login TIMESTAMP,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                # System settings table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS system_settings (
                        setting_key TEXT PRIMARY KEY,
                        setting_value TEXT NOT NULL,
                        data_type TEXT DEFAULT 'string',
                        description TEXT,
                        category TEXT,
                        updated_by TEXT,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                # Maintenance records table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS maintenance_records (
                        record_id TEXT PRIMARY KEY,
                        equipment_type TEXT NOT NULL,
                        equipment_id TEXT NOT NULL,
                        maintenance_type TEXT NOT NULL,
                        description TEXT,
                        scheduled_date DATE,
                        completed_date TIMESTAMP,
                        technician TEXT,
                        cost REAL,
                        status TEXT DEFAULT 'scheduled',
                        notes TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                # Reports table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS reports (
                        report_id TEXT PRIMARY KEY,
                        report_type TEXT NOT NULL,
                        report_name TEXT NOT NULL,
                        parameters TEXT,
                        generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        generated_by TEXT,
                        file_path TEXT,
                        status TEXT DEFAULT 'generated'
                    )
                """)
                
                # Create indexes
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_vehicles_plate ON vehicles(plate_number)")
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_vehicles_entry_time ON vehicles(entry_time)")
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_vehicles_status ON vehicles(status)")
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_parking_spaces_occupied ON parking_spaces(occupied)")
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_transactions_timestamp ON transactions(timestamp)")
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_system_events_timestamp ON system_events(timestamp)")
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_system_events_type ON system_events(event_type)")
                
                # Create triggers for updated_at
                cursor.execute("""
                    CREATE TRIGGER IF NOT EXISTS update_vehicles_timestamp 
                    AFTER UPDATE ON vehicles
                    BEGIN
                        UPDATE vehicles SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
                    END
                """)
                
                cursor.execute("""
                    CREATE TRIGGER IF NOT EXISTS update_users_timestamp 
                    AFTER UPDATE ON users
                    BEGIN
                        UPDATE users SET updated_at = CURRENT_TIMESTAMP WHERE user_id = NEW.user_id;
                    END
                """)
                
                # Initialize default settings
                self._init_default_settings(cursor)
                
                # Initialize parking spaces if empty
                cursor.execute("SELECT COUNT(*) FROM parking_spaces")
                if cursor.fetchone()[0] == 0:
                    self._init_parking_spaces(cursor)
                    
                # Create default admin user if no users exist
                cursor.execute("SELECT COUNT(*) FROM users")
                if cursor.fetchone()[0] == 0:
                    self._create_default_admin(cursor)
                    
                conn.commit()
                logger.info("Database initialized successfully")
                
        except Exception as e:
            logger.error(f"Database initialization error: {e}")
            raise
            
    def _init_default_settings(self, cursor):
        """Initialize default system settings"""
        default_settings = [
            ('parking_rate_car', '3.0', 'float', 'Hourly rate for cars', 'pricing'),
            ('parking_rate_suv', '4.0', 'float', 'Hourly rate for SUVs', 'pricing'),
            ('parking_rate_truck', '6.0', 'float', 'Hourly rate for trucks', 'pricing'),
            ('parking_rate_motorcycle', '2.0', 'float', 'Hourly rate for motorcycles', 'pricing'),
            ('max_parking_duration', '24', 'int', 'Maximum parking duration in hours', 'system'),
            ('grace_period', '15', 'int', 'Grace period in minutes', 'system'),
            ('total_levels', '15', 'int', 'Total number of levels', 'system'),
            ('spaces_per_level', '20', 'int', 'Spaces per level', 'system'),
            ('tax_rate', '0.08', 'float', 'Tax rate percentage', 'pricing'),
            ('currency', 'USD', 'string', 'Currency code', 'system'),
            ('emergency_contact', '911', 'string', 'Emergency contact number', 'safety')
        ]
        
        for setting in default_settings:
            cursor.execute(
                "INSERT OR IGNORE INTO system_settings (setting_key, setting_value, data_type, description, category) VALUES (?, ?, ?, ?, ?)",
                setting
            )
            
    def _init_parking_spaces(self, cursor):
        """Initialize parking spaces"""
        spaces = []
        for level in range(1, 16):  # 15 levels
            for position in range(1, 21):  # 20 spaces per level
                space_id = (level - 1) * 20 + position
                space_type = 'standard'
                
                # Mark some spaces for special vehicles
                if position <= 2:  # First 2 spaces for motorcycles
                    space_type = 'motorcycle'
                elif position >= 19:  # Last 2 spaces for trucks
                    space_type = 'truck'
                    
                spaces.append((space_id, level, position, None, False, False, False, space_type, 5.0, 2.0, 2.2))
                
        cursor.executemany(
            "INSERT INTO parking_spaces (space_id, level, position, vehicle_id, occupied, reserved, maintenance, space_type, max_length, max_width, max_height) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            spaces
        )
        
    def _create_default_admin(self, cursor):
        """Create default admin user"""
        user_id = str(uuid.uuid4())
        username = "admin"
        password = "admin123"  # Should be changed on first login
        salt = str(uuid.uuid4())
        password_hash = hashlib.sha256((password + salt).encode()).hexdigest()
        
        cursor.execute(
            "INSERT INTO users (user_id, username, password_hash, salt, role, full_name, active) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (user_id, username, password_hash, salt, 'admin', 'System Administrator', True)
        )
        
    # Vehicle Management
    def add_vehicle(self, vehicle_data: Dict) -> str:
        """Add new vehicle to database"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                vehicle_id = vehicle_data.get('id', str(uuid.uuid4()))
                
                cursor.execute("""
                    INSERT INTO vehicles (id, plate_number, vehicle_type, length, width, height, 
                                        owner_name, phone_number, email, entry_time, parking_space)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    vehicle_id,
                    vehicle_data['plate_number'],
                    vehicle_data['vehicle_type'],
                    vehicle_data['length'],
                    vehicle_data['width'],
                    vehicle_data['height'],
                    vehicle_data.get('owner_name'),
                    vehicle_data.get('phone_number'),
                    vehicle_data.get('email'),
                    vehicle_data.get('entry_time', datetime.now()),
                    vehicle_data.get('parking_space')
                ))
                
                conn.commit()
                
                # Log event
                self.log_event('vehicle_added', f"Vehicle {vehicle_data['plate_number']} added", 'info', 'database')
                
                return vehicle_id
                
        except Exception as e:
            logger.error(f"Error adding vehicle: {e}")
            raise
            
    def get_vehicle(self, vehicle_id: str = None, plate_number: str = None) -> Optional[Dict]:
        """Get vehicle by ID or plate number"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                if vehicle_id:
                    cursor.execute("SELECT * FROM vehicles WHERE id = ?", (vehicle_id,))
                elif plate_number:
                    cursor.execute("SELECT * FROM vehicles WHERE plate_number = ?", (plate_number,))
                else:
                    return None
                    
                row = cursor.fetchone()
                return dict(row) if row else None
                
        except Exception as e:
            logger.error(f"Error getting vehicle: {e}")
            return None
            
    def update_vehicle(self, vehicle_id: str, update_data: Dict) -> bool:
        """Update vehicle information"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # Build dynamic update query
                set_clauses = []
                values = []
                
                for key, value in update_data.items():
                    if key != 'id':  # Don't update ID
                        set_clauses.append(f"{key} = ?")
                        values.append(value)
                        
                if not set_clauses:
                    return False
                    
                values.append(vehicle_id)
                query = f"UPDATE vehicles SET {', '.join(set_clauses)} WHERE id = ?"
                
                cursor.execute(query, values)
                conn.commit()
                
                return cursor.rowcount > 0
                
        except Exception as e:
            logger.error(f"Error updating vehicle: {e}")
            return False
            
    def get_active_vehicles(self) -> List[Dict]:
        """Get all active (parked) vehicles"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    SELECT v.*, ps.level, ps.position 
                    FROM vehicles v
                    LEFT JOIN parking_spaces ps ON v.parking_space = ps.space_id
                    WHERE v.status = 'active' AND v.exit_time IS NULL
                    ORDER BY v.entry_time
                """)
                
                return [dict(row) for row in cursor.fetchall()]
                
        except Exception as e:
            logger.error(f"Error getting active vehicles: {e}")
            return []
            
    # Parking Space Management
    def get_available_spaces(self, vehicle_type: str = None) -> List[Dict]:
        """Get available parking spaces"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                query = """
                    SELECT * FROM parking_spaces 
                    WHERE occupied = FALSE AND reserved = FALSE AND maintenance = FALSE
                """
                params = []
                
                if vehicle_type:
                    # Filter by compatible space types
                    type_mapping = {
                        'motorcycle': ['motorcycle', 'standard'],
                        'car': ['standard'],
                        'suv': ['standard'],
                        'truck': ['truck', 'standard']
                    }
                    
                    compatible_types = type_mapping.get(vehicle_type, ['standard'])
                    placeholders = ','.join(['?' for _ in compatible_types])
                    query += f" AND space_type IN ({placeholders})"
                    params.extend(compatible_types)
                    
                query += " ORDER BY level, position"
                
                cursor.execute(query, params)
                return [dict(row) for row in cursor.fetchall()]
                
        except Exception as e:
            logger.error(f"Error getting available spaces: {e}")
            return []
            
    def allocate_space(self, space_id: int, vehicle_id: str) -> bool:
        """Allocate parking space to vehicle"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # Check if space is available
                cursor.execute(
                    "SELECT occupied, reserved, maintenance FROM parking_spaces WHERE space_id = ?",
                    (space_id,)
                )
                
                row = cursor.fetchone()
                if not row or row['occupied'] or row['reserved'] or row['maintenance']:
                    return False
                    
                # Allocate space
                cursor.execute(
                    "UPDATE parking_spaces SET vehicle_id = ?, occupied = TRUE, last_updated = CURRENT_TIMESTAMP WHERE space_id = ?",
                    (vehicle_id, space_id)
                )
                
                # Update vehicle record
                cursor.execute(
                    "UPDATE vehicles SET parking_space = ? WHERE id = ?",
                    (space_id, vehicle_id)
                )
                
                conn.commit()
                
                self.log_event('space_allocated', f"Space {space_id} allocated to vehicle {vehicle_id}", 'info', 'database')
                
                return True
                
        except Exception as e:
            logger.error(f"Error allocating space: {e}")
            return False
            
    def release_space(self, space_id: int) -> bool:
        """Release parking space"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                cursor.execute(
                    "UPDATE parking_spaces SET vehicle_id = NULL, occupied = FALSE, last_updated = CURRENT_TIMESTAMP WHERE space_id = ?",
                    (space_id,)
                )
                
                conn.commit()
                
                self.log_event('space_released', f"Space {space_id} released", 'info', 'database')
                
                return cursor.rowcount > 0
                
        except Exception as e:
            logger.error(f"Error releasing space: {e}")
            return False
            
    def get_parking_grid(self) -> List[Dict]:
        """Get complete parking grid status"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    SELECT ps.space_id, ps.level, ps.position, ps.occupied, ps.reserved, ps.maintenance, ps.space_type,
                           v.id as vehicle_id, v.plate_number, v.vehicle_type, v.entry_time, v.owner_name
                    FROM parking_spaces ps
                    LEFT JOIN vehicles v ON ps.vehicle_id = v.id AND v.exit_time IS NULL
                    ORDER BY ps.level, ps.position
                """)
                
                return [dict(row) for row in cursor.fetchall()]
                
        except Exception as e:
            logger.error(f"Error getting parking grid: {e}")
            return []
            
    # Transaction Management
    def create_transaction(self, transaction_data: Dict) -> str:
        """Create new transaction record"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                transaction_id = transaction_data.get('transaction_id', str(uuid.uuid4()))
                
                cursor.execute("""
                    INSERT INTO transactions (transaction_id, vehicle_id, amount, payment_method, 
                                            status, reference_number, receipt_number, discount_applied, tax_amount)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    transaction_id,
                    transaction_data['vehicle_id'],
                    transaction_data['amount'],
                    transaction_data['payment_method'],
                    transaction_data.get('status', 'pending'),
                    transaction_data.get('reference_number'),
                    transaction_data.get('receipt_number'),
                    transaction_data.get('discount_applied', 0.0),
                    transaction_data.get('tax_amount', 0.0)
                ))
                
                conn.commit()
                
                self.log_event('transaction_created', f"Transaction {transaction_id} created", 'info', 'database')
                
                return transaction_id
                
        except Exception as e:
            logger.error(f"Error creating transaction: {e}")
            raise
            
    def update_transaction_status(self, transaction_id: str, status: str, reference_number: str = None) -> bool:
        """Update transaction status"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                if reference_number:
                    cursor.execute(
                        "UPDATE transactions SET status = ?, reference_number = ? WHERE transaction_id = ?",
                        (status, reference_number, transaction_id)
                    )
                else:
                    cursor.execute(
                        "UPDATE transactions SET status = ? WHERE transaction_id = ?",
                        (status, transaction_id)
                    )
                    
                conn.commit()
                
                return cursor.rowcount > 0
                
        except Exception as e:
            logger.error(f"Error updating transaction status: {e}")
            return False
            
    # System Event Logging
    def log_event(self, event_type: str, description: str, severity: str = 'info', source: str = None, user_id: str = None, data: Dict = None):
        """Log system event"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    INSERT INTO system_events (event_type, description, severity, source, user_id, data)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    event_type,
                    description,
                    severity,
                    source,
                    user_id,
                    json.dumps(data) if data else None
                ))
                
                conn.commit()
                
        except Exception as e:
            logger.error(f"Error logging event: {e}")
            
    def get_system_events(self, limit: int = 100, event_type: str = None, severity: str = None) -> List[Dict]:
        """Get system events"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                query = "SELECT * FROM system_events WHERE 1=1"
                params = []
                
                if event_type:
                    query += " AND event_type = ?"
                    params.append(event_type)
                    
                if severity:
                    query += " AND severity = ?"
                    params.append(severity)
                    
                query += " ORDER BY timestamp DESC LIMIT ?"
                params.append(limit)
                
                cursor.execute(query, params)
                
                events = []
                for row in cursor.fetchall():
                    event = dict(row)
                    if event['data']:
                        event['data'] = json.loads(event['data'])
                    events.append(event)
                    
                return events
                
        except Exception as e:
            logger.error(f"Error getting system events: {e}")
            return []
            
    # Statistics and Reports
    def get_system_statistics(self, start_date: datetime = None, end_date: datetime = None) -> Dict:
        """Get system statistics"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # Base query conditions
                where_clause = "WHERE 1=1"
                params = []
                
                if start_date:
                    where_clause += " AND entry_time >= ?"
                    params.append(start_date)
                    
                if end_date:
                    where_clause += " AND entry_time <= ?"
                    params.append(end_date)
                    
                # Total vehicles
                cursor.execute(f"SELECT COUNT(*) FROM vehicles {where_clause}", params)
                total_vehicles = cursor.fetchone()[0]
                
                # Active vehicles
                cursor.execute("SELECT COUNT(*) FROM vehicles WHERE status = 'active' AND exit_time IS NULL")
                active_vehicles = cursor.fetchone()[0]
                
                # Total revenue
                cursor.execute(f"SELECT COALESCE(SUM(amount), 0) FROM transactions WHERE status = 'completed' AND timestamp >= ? AND timestamp <= ?",
                              (start_date or datetime.min, end_date or datetime.now()))
                total_revenue = cursor.fetchone()[0]
                
                # Average stay time
                cursor.execute(f"""
                    SELECT AVG((julianday(exit_time) - julianday(entry_time)) * 24) 
                    FROM vehicles 
                    {where_clause} AND exit_time IS NOT NULL
                """, params)
                avg_stay_result = cursor.fetchone()[0]
                avg_stay_time = round(avg_stay_result, 2) if avg_stay_result else 0.0
                
                # Occupancy rate
                cursor.execute("SELECT COUNT(*) FROM parking_spaces WHERE occupied = TRUE")
                occupied_spaces = cursor.fetchone()[0]
                
                cursor.execute("SELECT COUNT(*) FROM parking_spaces WHERE maintenance = FALSE")
                available_total = cursor.fetchone()[0]
                
                occupancy_rate = round((occupied_spaces / available_total) * 100, 1) if available_total > 0 else 0.0
                
                # Peak hours analysis
                cursor.execute(f"""
                    SELECT strftime('%H', entry_time) as hour, COUNT(*) as count
                    FROM vehicles 
                    {where_clause}
                    GROUP BY hour
                    ORDER BY count DESC
                    LIMIT 3
                """, params)
                peak_hours = [{'hour': int(row[0]), 'count': row[1]} for row in cursor.fetchall()]
                
                return {
                    'total_vehicles': total_vehicles,
                    'active_vehicles': active_vehicles,
                    'total_revenue': round(total_revenue, 2),
                    'average_stay_time': avg_stay_time,
                    'occupancy_rate': occupancy_rate,
                    'occupied_spaces': occupied_spaces,
                    'available_spaces': available_total - occupied_spaces,
                    'peak_hours': peak_hours
                }
                
        except Exception as e:
            logger.error(f"Error getting statistics: {e}")
            return {}
            
    # Settings Management
    def get_setting(self, key: str) -> Any:
        """Get system setting value"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                cursor.execute("SELECT setting_value, data_type FROM system_settings WHERE setting_key = ?", (key,))
                row = cursor.fetchone()
                
                if not row:
                    return None
                    
                value, data_type = row
                
                # Convert to appropriate type
                if data_type == 'int':
                    return int(value)
                elif data_type == 'float':
                    return float(value)
                elif data_type == 'bool':
                    return value.lower() in ('true', '1', 'yes')
                else:
                    return value
                    
        except Exception as e:
            logger.error(f"Error getting setting: {e}")
            return None
            
    def set_setting(self, key: str, value: Any, data_type: str = None) -> bool:
        """Set system setting value"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # Auto-detect data type if not provided
                if data_type is None:
                    if isinstance(value, bool):
                        data_type = 'bool'
                    elif isinstance(value, int):
                        data_type = 'int'
                    elif isinstance(value, float):
                        data_type = 'float'
                    else:
                        data_type = 'string'
                        
                cursor.execute("""
                    INSERT OR REPLACE INTO system_settings (setting_key, setting_value, data_type, updated_at)
                    VALUES (?, ?, ?, CURRENT_TIMESTAMP)
                """, (key, str(value), data_type))
                
                conn.commit()
                
                self.log_event('setting_updated', f"Setting {key} updated to {value}", 'info', 'database')
                
                return True
                
        except Exception as e:
            logger.error(f"Error setting value: {e}")
            return False
            
    def close(self):
        """Close all database connections"""
        with self.lock:
            for conn in self.connection_pool:
                conn.close()
            self.connection_pool.clear()

if __name__ == "__main__":
    # Test database manager
    db = DatabaseManager()
    
    # Test statistics
    stats = db.get_system_statistics()
    print("System Statistics:")
    for key, value in stats.items():
        print(f"  {key}: {value}")
        
    # Test settings
    print(f"\nParking rate for cars: ${db.get_setting('parking_rate_car')}")
    
    db.close()
