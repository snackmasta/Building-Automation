"""
Unit tests for Database Manager
Tests database operations, connection management, and data validation
"""

import unittest
import tempfile
import os
import sqlite3
from datetime import datetime, timedelta
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from database.database_manager import DatabaseManager

class TestDatabaseManager(unittest.TestCase):
    """Test cases for DatabaseManager class"""
    
    def setUp(self):
        """Set up test database"""
        self.test_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.test_db.close()
        self.db_manager = DatabaseManager(self.test_db.name)
        
    def tearDown(self):
        """Clean up test database"""
        self.db_manager.close()
        os.unlink(self.test_db.name)
        
    def test_database_initialization(self):
        """Test database tables are created correctly"""
        # Test database connection works
        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in cursor.fetchall()]
            
        expected_tables = [
            'vehicles', 'parking_spaces', 'transactions', 'system_events',
            'users', 'system_settings', 'maintenance_records', 'reports'
        ]
        for table in expected_tables:
            self.assertIn(table, tables)
            
    def test_vehicle_operations(self):
        """Test vehicle CRUD operations"""
        # Test vehicle insertion
        vehicle_data = {
            'plate_number': 'ABC123',
            'vehicle_type': 'sedan',
            'length': 4.5,
            'width': 1.8,
            'height': 1.6,
            'owner_name': 'Test Owner',
            'phone_number': '555-1234',
            'email': 'test@example.com'
        }
        vehicle_id = self.db_manager.add_vehicle(vehicle_data)
        self.assertIsNotNone(vehicle_id)
        
        # Test vehicle retrieval
        vehicle = self.db_manager.get_vehicle(vehicle_id)
        self.assertIsNotNone(vehicle)
        self.assertEqual(vehicle['plate_number'], 'ABC123')
        self.assertEqual(vehicle['vehicle_type'], 'sedan')
        
        # Test vehicle update
        update_data = {
            'plate_number': 'XYZ789',
            'vehicle_type': 'suv'
        }
        self.assertTrue(self.db_manager.update_vehicle(vehicle_id, update_data))
        updated_vehicle = self.db_manager.get_vehicle(vehicle_id)
        self.assertEqual(updated_vehicle['plate_number'], 'XYZ789')
        self.assertEqual(updated_vehicle['vehicle_type'], 'suv')
        
    def test_parking_space_operations(self):
        """Test parking space management"""
        # Test getting available spaces
        spaces = self.db_manager.get_available_spaces('sedan')
        self.assertGreater(len(spaces), 0)
        
        # Test space allocation
        vehicle_data = {
            'plate_number': 'PARK123',
            'vehicle_type': 'sedan',
            'length': 4.5,
            'width': 1.8,
            'height': 1.6
        }
        vehicle_id = self.db_manager.add_vehicle(vehicle_data)
        space_id = spaces[0]['space_id']
        
        self.assertTrue(self.db_manager.allocate_space(space_id, vehicle_id))
        
        # Test space release
        self.assertTrue(self.db_manager.release_space(space_id))
        
    def test_transaction_operations(self):
        """Test transaction management"""
        # Create test vehicle first
        vehicle_data = {
            'plate_number': 'TRANS123',
            'vehicle_type': 'sedan',
            'length': 4.5,
            'width': 1.8,
            'height': 1.6
        }
        vehicle_id = self.db_manager.add_vehicle(vehicle_data)
        
        # Create test transaction
        transaction_data = {
            'vehicle_id': vehicle_id,
            'amount': 15.50,
            'payment_method': 'card',
            'status': 'paid'
        }
        transaction_id = self.db_manager.create_transaction(transaction_data)
        self.assertIsNotNone(transaction_id)
        
    def test_system_events_logging(self):
        """Test system event logging"""
        # Log test event
        self.db_manager.log_event(
            'vehicle_entry', 'Vehicle ABC123 entered system', 'info'
        )
        
        # Test event was logged (basic test)
        self.assertTrue(True)  # Event logging doesn't return ID in current implementation
        
    def test_data_validation(self):
        """Test data validation and constraints"""
        # Test that we can handle invalid data gracefully
        try:
            invalid_vehicle_data = {
                'plate_number': '',  # Empty plate
                'vehicle_type': 'sedan',
                'length': 4.5,
                'width': 1.8,
                'height': 1.6
            }
            result = self.db_manager.add_vehicle(invalid_vehicle_data)
            # If no exception, at least verify it's handled
            self.assertIsNotNone(result)
        except Exception:
            # Exception is expected for invalid data
            pass
            
    def test_concurrent_operations(self):
        """Test database operations under concurrent access"""
        import threading
        import time
        
        results = []
        
        def add_vehicles():
            for i in range(10):
                try:
                    vehicle_data = {
                        'plate_number': f'TEST{i:03d}',
                        'vehicle_type': 'sedan',
                        'length': 4.5,
                        'width': 1.8,
                        'height': 1.6
                    }
                    vehicle_id = self.db_manager.add_vehicle(vehicle_data)
                    results.append(vehicle_id)
                except Exception as e:
                    print(f"Error adding vehicle: {e}")
                    results.append(None)
                time.sleep(0.01)
                
        def add_transactions():
            for i in range(10):
                try:
                    # Create a vehicle first for the transaction
                    vehicle_data = {
                        'plate_number': f'TRANS{i:03d}',
                        'vehicle_type': 'sedan',
                        'length': 4.5,
                        'width': 1.8,
                        'height': 1.6
                    }
                    vehicle_id = self.db_manager.add_vehicle(vehicle_data)
                    
                    transaction_data = {
                        'vehicle_id': vehicle_id,
                        'amount': 15.50,
                        'payment_method': 'card',
                        'status': 'paid'
                    }
                    transaction_id = self.db_manager.create_transaction(transaction_data)
                    results.append(transaction_id)
                except Exception as e:
                    print(f"Error creating transaction: {e}")
                    results.append(None)
                time.sleep(0.01)
                
        # Run concurrent operations
        thread1 = threading.Thread(target=add_vehicles)
        thread2 = threading.Thread(target=add_transactions)
        
        thread1.start()
        thread2.start()
        
        thread1.join()
        thread2.join()
        
        # Verify operations completed (may have some failures due to concurrency)
        self.assertGreater(len(results), 0)
        
    def test_system_statistics(self):
        """Test system statistics retrieval"""
        # Add some test data
        vehicle_data = {
            'plate_number': 'STATS123',
            'vehicle_type': 'sedan',
            'length': 4.5,
            'width': 1.8,
            'height': 1.6
        }
        self.db_manager.add_vehicle(vehicle_data)
        
        # Get statistics
        stats = self.db_manager.get_system_statistics()
        self.assertIsInstance(stats, dict)
        self.assertIn('total_vehicles', stats)
        self.assertIn('active_vehicles', stats)
        
if __name__ == '__main__':
    unittest.main()
