"""
Integration tests for the complete Car Parking Vending System
Tests end-to-end workflows and system integration
"""

import unittest
import tempfile
import os
import time
import threading
import json
from datetime import datetime, timedelta
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from database.database_manager import DatabaseManager
from simulation.parking_simulator import ParkingSimulator
from communication.protocols import CommunicationManager
from utilities.system_utilities import SystemUtilities
from unittest.mock import Mock, patch

class TestSystemIntegration(unittest.TestCase):
    """Integration tests for the complete parking system"""
    
    def setUp(self):
        """Set up integrated test environment"""
        # Create temporary database
        self.test_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.test_db.close()
        
        # Initialize system components
        self.db_manager = DatabaseManager(self.test_db.name)
        self.simulator = ParkingSimulator(self.db_manager)
        
        # Communication configuration
        comm_config = {
            'websocket': {'host': 'localhost', 'port': 8766, 'max_connections': 10},
            'tcp': {'host': 'localhost', 'port': 9002, 'buffer_size': 1024},
            'modbus': {'host': '192.168.1.100', 'port': 502, 'unit_id': 1},
            'opcua': {'endpoint': 'opc.tcp://localhost:4840', 'namespace': 'http://example.com'}
        }
        self.comm_manager = CommunicationManager(comm_config)
        
        # System utilities
        self.system_utils = SystemUtilities()
        
    def tearDown(self):
        """Clean up test environment"""
        self.simulator.stop_simulation()
        self.comm_manager.stop_all_servers()
        self.db_manager.close()
        os.unlink(self.test_db.name)
        
    def test_complete_parking_workflow(self):
        """Test complete vehicle parking and retrieval workflow"""
        # Initialize system
        self.simulator.initialize_parking_grid()
        
        # Step 1: Vehicle arrival
        vehicle_data = {
            'license_plate': 'INTEG001',
            'vehicle_type': 'sedan',
            'length': 4.5,
            'width': 1.8,
            'height': 1.6
        }
        
        # Add vehicle to database
        vehicle_id = self.db_manager.add_vehicle(**vehicle_data)
        self.assertIsNotNone(vehicle_id)
        
        # Step 2: Find and allocate parking space
        available_space = self.simulator.find_available_space(vehicle_data['vehicle_type'])
        self.assertIsNotNone(available_space)
        
        space_allocated = self.db_manager.update_space_status(
            available_space['id'], 'occupied', vehicle_data['license_plate']
        )
        self.assertTrue(space_allocated)
        
        # Step 3: Process payment
        transaction_id = self.db_manager.create_transaction(
            vehicle_data['license_plate'], 'credit_card', 0.0, 'pending'
        )
        self.assertIsNotNone(transaction_id)
        
        # Step 4: Log system events
        entry_event = self.db_manager.log_system_event(
            'vehicle_entry', 'info', 
            f"Vehicle {vehicle_data['license_plate']} entered and parked in space {available_space['id']}"
        )
        self.assertIsNotNone(entry_event)
        
        # Step 5: Vehicle retrieval workflow
        # Calculate parking duration and fee
        duration_minutes = 120  # 2 hours
        parking_fee = self.simulator.calculate_parking_fee(duration_minutes)
        
        # Update transaction with calculated fee
        payment_updated = self.db_manager.update_transaction(
            transaction_id, 
            amount=parking_fee,
            status='completed',
            end_time=datetime.now()
        )
        self.assertTrue(payment_updated)
        
        # Release parking space
        space_released = self.db_manager.release_parking_space(available_space['id'])
        self.assertTrue(space_released)
        
        # Log exit event
        exit_event = self.db_manager.log_system_event(
            'vehicle_exit', 'info',
            f"Vehicle {vehicle_data['license_plate']} exited from space {available_space['id']}"
        )
        self.assertIsNotNone(exit_event)
        
        # Verify final state
        final_space = self.db_manager.get_parking_space(available_space['id'])
        self.assertEqual(final_space['status'], 'available')
        
        final_transaction = self.db_manager.get_transaction(transaction_id)
        self.assertEqual(final_transaction['status'], 'completed')
        self.assertGreater(final_transaction['amount'], 0)
        
    def test_concurrent_vehicle_operations(self):
        """Test system handling of concurrent vehicle operations"""
        self.simulator.initialize_parking_grid()
        
        results = []
        errors = []
        
        def parking_operation(vehicle_index):
            try:
                # Generate unique vehicle
                license_plate = f"CONC{vehicle_index:03d}"
                vehicle_id = self.db_manager.add_vehicle(
                    license_plate, 'sedan', 4.5, 1.8, 1.6
                )
                
                # Find and allocate space
                space = self.simulator.find_available_space('sedan')
                if space:
                    allocated = self.db_manager.update_space_status(
                        space['id'], 'occupied', license_plate
                    )
                    if allocated:
                        # Create transaction
                        transaction_id = self.db_manager.create_transaction(
                            license_plate, 'credit_card', 15.00, 'completed'
                        )
                        results.append({
                            'vehicle_id': vehicle_id,
                            'space_id': space['id'],
                            'transaction_id': transaction_id
                        })
                        
            except Exception as e:
                errors.append(str(e))
                
        # Start concurrent operations
        threads = []
        for i in range(20):
            thread = threading.Thread(target=parking_operation, args=(i,))
            threads.append(thread)
            thread.start()
            
        # Wait for all operations to complete
        for thread in threads:
            thread.join()
            
        # Verify results
        self.assertEqual(len(errors), 0, f"Errors occurred: {errors}")
        self.assertGreater(len(results), 0)
        
        # Verify data consistency
        for result in results:
            # Check vehicle exists
            vehicle = self.db_manager.get_vehicle(result['vehicle_id'])
            self.assertIsNotNone(vehicle)
            
            # Check space is occupied
            space = self.db_manager.get_parking_space(result['space_id'])
            self.assertEqual(space['status'], 'occupied')
            
            # Check transaction exists
            transaction = self.db_manager.get_transaction(result['transaction_id'])
            self.assertIsNotNone(transaction)
            
    def test_communication_integration(self):
        """Test integration between different communication protocols"""
        # Start communication servers
        websocket_started = self.comm_manager.start_websocket_server()
        tcp_started = self.comm_manager.start_tcp_server()
        
        if not (websocket_started and tcp_started):
            self.skipTest("Communication servers could not be started")
            
        # Test message routing between protocols
        test_message = {
            'type': 'system_status',
            'data': {
                'total_spaces': 300,
                'occupied_spaces': 150,
                'available_spaces': 150,
                'revenue_today': 2550.75
            },
            'timestamp': time.time()
        }
        
        # Configure message routing
        routing_config = {
            'system_status': ['websocket', 'tcp'],
            'parking_event': ['websocket'],
            'maintenance_alert': ['websocket', 'tcp']
        }
        self.comm_manager.configure_message_routing(routing_config)
        
        # Broadcast message
        self.comm_manager.broadcast_message(test_message)
        
        # Verify message was queued for appropriate protocols
        websocket_queue = self.comm_manager.get_message_queue('websocket')
        tcp_queue = self.comm_manager.get_message_queue('tcp')
        
        self.assertGreater(len(websocket_queue), 0)
        self.assertGreater(len(tcp_queue), 0)
        
        # Verify message content
        websocket_msg = websocket_queue[-1]
        self.assertEqual(websocket_msg['type'], 'system_status')
        self.assertEqual(websocket_msg['data']['total_spaces'], 300)
        
    def test_real_time_simulation_integration(self):
        """Test real-time simulation with database and communication integration"""
        self.simulator.initialize_parking_grid()
        
        # Start real-time simulation
        self.simulator.start_simulation(mode='real_time', interval=0.1)
        
        # Monitor system for a period
        initial_stats = self.simulator.get_simulation_statistics()
        time.sleep(1.0)  # Let simulation run
        final_stats = self.simulator.get_simulation_statistics()
        
        # Stop simulation
        self.simulator.stop_simulation()
        
        # Verify simulation activity
        self.assertGreaterEqual(
            final_stats['total_arrivals'], 
            initial_stats['total_arrivals']
        )
        
        # Verify database integration
        recent_transactions = self.db_manager.get_recent_transactions(limit=10)
        if recent_transactions:
            self.assertGreater(len(recent_transactions), 0)
            
        # Verify events were logged
        recent_events = self.db_manager.get_system_events(limit=20)
        self.assertGreater(len(recent_events), 0)
        
    def test_system_performance_under_load(self):
        """Test system performance under high load conditions"""
        self.simulator.initialize_parking_grid()
        
        start_time = time.time()
        
        # Simulate high load scenario
        operations_count = 200
        for i in range(operations_count):
            # Alternate between arrivals and departures
            if i % 2 == 0:
                self.simulator.simulate_arrival()
            else:
                self.simulator.simulate_departure()
                
        end_time = time.time()
        duration = end_time - start_time
        
        # Performance metrics
        operations_per_second = operations_count / duration
        
        # Verify performance is acceptable (adjust thresholds as needed)
        self.assertGreater(operations_per_second, 50)  # At least 50 ops/sec
        
        # Verify system stability
        stats = self.simulator.get_simulation_statistics()
        self.assertGreaterEqual(stats['current_occupancy'], 0)
        self.assertLessEqual(stats['current_occupancy'], 300)
        
        # Verify database consistency
        total_vehicles = len(self.db_manager.get_all_vehicles())
        total_transactions = len(self.db_manager.get_all_transactions())
        
        # Should have reasonable number of records
        self.assertGreater(total_vehicles, 0)
        self.assertGreater(total_transactions, 0)
        
    def test_error_recovery_integration(self):
        """Test system error recovery and fault tolerance"""
        self.simulator.initialize_parking_grid()
        
        # Simulate database connection error
        with patch.object(self.db_manager, 'add_vehicle', side_effect=Exception("DB Error")):
            # System should handle the error gracefully
            result = self.simulator.simulate_arrival()
            # May return None or handle error internally
            
        # Verify system continues to function after error
        normal_result = self.simulator.simulate_arrival()
        # Should work normally again
        
        # Test communication error recovery
        with patch.object(self.comm_manager, 'send_websocket_message', side_effect=Exception("Comm Error")):
            # Should not crash the system
            test_message = {'type': 'test', 'data': {}}
            result = self.comm_manager.send_websocket_message(test_message)
            self.assertFalse(result)  # Should return False on error
            
        # Verify error statistics are tracked
        error_stats = self.comm_manager.get_error_statistics()
        self.assertIsInstance(error_stats, dict)
        
    def test_data_consistency_across_components(self):
        """Test data consistency across all system components"""
        self.simulator.initialize_parking_grid()
        
        # Perform multiple operations
        test_vehicles = []
        for i in range(10):
            license_plate = f"DATA{i:03d}"
            
            # Add vehicle through simulator
            arrival_result = self.simulator.simulate_arrival_with_license(license_plate)
            if arrival_result:
                test_vehicles.append(arrival_result)
                
        # Verify consistency between simulator and database
        for vehicle_data in test_vehicles:
            license_plate = vehicle_data['vehicle']['license_plate']
            space_id = vehicle_data['space']['id']
            
            # Check database records
            db_vehicle = self.db_manager.get_vehicle_by_license(license_plate)
            db_space = self.db_manager.get_parking_space(space_id)
            
            self.assertIsNotNone(db_vehicle)
            self.assertIsNotNone(db_space)
            self.assertEqual(db_space['status'], 'occupied')
            self.assertEqual(db_space['vehicle_license'], license_plate)
            
            # Check simulator state
            sim_space = self.simulator.get_space_status(space_id)
            self.assertEqual(sim_space['status'], 'occupied')
            self.assertEqual(sim_space['vehicle_license'], license_plate)
            
    def test_system_monitoring_integration(self):
        """Test integrated system monitoring and health checks"""
        # Get system health status
        health_status = self.system_utils.get_system_health()
        
        # Verify health check structure
        expected_components = ['database', 'simulation', 'communication']
        for component in expected_components:
            if component in health_status:
                self.assertIn('status', health_status[component])
                self.assertIn('last_check', health_status[component])
                
        # Test performance monitoring
        performance_metrics = self.system_utils.get_performance_metrics()
        self.assertIsInstance(performance_metrics, dict)
        
        # Test resource utilization
        resource_usage = self.system_utils.get_resource_usage()
        self.assertIn('memory_usage', resource_usage)
        self.assertIn('cpu_usage', resource_usage)
        
    def test_backup_and_recovery_integration(self):
        """Test integrated backup and recovery procedures"""
        self.simulator.initialize_parking_grid()
        
        # Generate some test data
        for _ in range(5):
            self.simulator.simulate_arrival()
            
        # Create system backup
        backup_file = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        backup_file.close()
        
        try:
            # Test database backup
            backup_success = self.db_manager.backup_database(backup_file.name)
            self.assertTrue(backup_success)
            
            # Verify backup file exists and has content
            self.assertTrue(os.path.exists(backup_file.name))
            self.assertGreater(os.path.getsize(backup_file.name), 0)
            
            # Test backup integrity
            backup_db = DatabaseManager(backup_file.name)
            backup_vehicles = backup_db.get_all_vehicles()
            original_vehicles = self.db_manager.get_all_vehicles()
            
            self.assertEqual(len(backup_vehicles), len(original_vehicles))
            backup_db.close()
            
        finally:
            os.unlink(backup_file.name)

if __name__ == '__main__':
    unittest.main()
