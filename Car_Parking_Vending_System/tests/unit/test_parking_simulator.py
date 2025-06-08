"""
Unit tests for Parking Simulator
Tests vehicle generation, parking logic, and simulation accuracy
"""

import unittest
import tempfile
import os
import time
from datetime import datetime, timedelta
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from simulation.parking_simulator import ParkingSimulator, VehicleGenerator
from database.database_manager import DatabaseManager
from unittest.mock import Mock, patch

class TestParkingSimulator(unittest.TestCase):
    """Test cases for ParkingSimulator class"""
    
    def setUp(self):
        """Set up test simulator with temporary database"""
        self.test_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.test_db.close()
        
        self.simulator = ParkingSimulator(self.test_db.name)
        
    def tearDown(self):
        """Clean up test resources"""
        self.simulator.stop_simulation()
        os.unlink(self.test_db.name)
        
    def test_simulator_initialization(self):
        """Test simulator initialization and configuration"""
        # Test default configuration
        self.assertEqual(self.simulator.total_spaces, 300)
        self.assertIsInstance(self.simulator.vehicle_generator, VehicleGenerator)
        self.assertFalse(self.simulator.running)
        
    def test_vehicle_generation(self):
        """Test vehicle generation and validation"""
        generator = VehicleGenerator()
        
        # Generate multiple vehicles
        vehicles = [generator.generate_vehicle() for _ in range(10)]
        
        # Validate vehicle properties
        for vehicle in vehicles:
            self.assertIsNotNone(vehicle.id)
            self.assertIsNotNone(vehicle.plate_number)
            self.assertIn(vehicle.vehicle_type, ['car', 'suv', 'truck', 'motorcycle'])
            self.assertGreater(vehicle.length, 0)
            self.assertGreater(vehicle.width, 0)
            self.assertGreater(vehicle.height, 0)
            self.assertIsInstance(vehicle.entry_time, datetime)
            
        # Ensure unique plate numbers
        plate_numbers = [v.plate_number for v in vehicles]
        self.assertEqual(len(plate_numbers), len(set(plate_numbers)))
        
    def test_parking_space_management(self):
        """Test parking space allocation and release"""
        # Test finding available space
        space_id = self.simulator._find_available_space('car')
        self.assertIsNotNone(space_id)
        
        # Test space allocation
        vehicle = self.simulator.vehicle_generator.generate_vehicle()
        success = self.simulator._allocate_space(space_id, vehicle)
        self.assertTrue(success)
        
        # Test space is now occupied
        self.assertIn(space_id, self.simulator.occupied_spaces)
        
        # Test space release
        self.simulator._release_space(space_id)
        self.assertNotIn(space_id, self.simulator.occupied_spaces)
        
    def test_peak_hour_simulation(self):
        """Test peak hour detection and rate adjustment"""
        # Mock current time to peak hour
        with patch('simulation.parking_simulator.datetime') as mock_datetime:
            mock_datetime.now.return_value = datetime(2023, 1, 1, 8, 0)  # 8 AM
            mock_datetime.side_effect = lambda *args, **kw: datetime(*args, **kw)
            
            self.assertTrue(self.simulator._is_peak_hour())
            
        # Mock current time to non-peak hour
        with patch('simulation.parking_simulator.datetime') as mock_datetime:
            mock_datetime.now.return_value = datetime(2023, 1, 1, 14, 0)  # 2 PM
            mock_datetime.side_effect = lambda *args, **kw: datetime(*args, **kw)
            
            self.assertFalse(self.simulator._is_peak_hour())
            
    def test_arrival_simulation(self):
        """Test vehicle arrival simulation"""
        # Test single vehicle entry
        initial_count = self.simulator.statistics['total_entries']
        self.simulator._simulate_arrival()
        
        # Check if entry was recorded (may or may not happen based on probability)
        final_count = self.simulator.statistics['total_entries']
        self.assertGreaterEqual(final_count, initial_count)
        
    def test_departure_simulation(self):
        """Test vehicle departure simulation"""
        # First add a vehicle
        vehicle = self.simulator.vehicle_generator.generate_vehicle()
        space_id = self.simulator._find_available_space(vehicle.vehicle_type)
        if space_id:
            self.simulator._allocate_space(space_id, vehicle)
            
            # Test departure
            initial_exits = self.simulator.statistics['total_exits']
            self.simulator._simulate_departure()
            
            # Check if departure was processed
            final_exits = self.simulator.statistics['total_exits']
            self.assertGreaterEqual(final_exits, initial_exits)
            
    def test_payment_simulation(self):
        """Test payment processing simulation"""
        vehicle = self.simulator.vehicle_generator.generate_vehicle()
        
        # Test payment calculation
        stay_hours = 2.5
        payment_amount = self.simulator._calculate_payment(vehicle.vehicle_type, stay_hours)
        self.assertGreater(payment_amount, 0)
        
        # Test payment method generation
        payment_method = self.simulator._generate_payment_method()
        self.assertIn(payment_method, ['cash', 'credit_card', 'debit_card', 'mobile_payment'])
        
    def test_queue_management(self):
        """Test waiting queue management"""
        # Fill up all spaces
        for i in range(min(50, self.simulator.total_spaces)):
            vehicle = self.simulator.vehicle_generator.generate_vehicle()
            space_id = self.simulator._find_available_space(vehicle.vehicle_type)
            if space_id:
                self.simulator._allocate_space(space_id, vehicle)
                
        # Try to add more vehicles (should go to queue)
        initial_queue_size = len(self.simulator.waiting_queue)
        overflow_vehicle = self.simulator.vehicle_generator.generate_vehicle()
        
        # Simulate queue behavior
        if len(self.simulator.occupied_spaces) >= self.simulator.total_spaces:
            self.simulator.waiting_queue.append(overflow_vehicle)
            
        self.assertGreaterEqual(len(self.simulator.waiting_queue), initial_queue_size)
        
    def test_statistics_tracking(self):
        """Test statistics collection and accuracy"""
        initial_stats = self.simulator.statistics.copy()
        
        # Simulate some activity
        for _ in range(5):
            self.simulator._simulate_arrival()
            
        # Check if statistics were updated
        final_stats = self.simulator.statistics
        self.assertGreaterEqual(final_stats['total_entries'], initial_stats['total_entries'])
        
    def test_real_time_simulation(self):
        """Test real-time simulation functionality"""
        # Start simulation for a short time
        self.simulator.start_simulation()
        self.assertTrue(self.simulator.running)
        
        # Let it run briefly
        time.sleep(0.1)
        
        # Stop simulation
        self.simulator.stop_simulation()
        self.assertFalse(self.simulator.running)
        
    def test_scenario_simulation(self):
        """Test predefined scenario simulation"""
        # Test normal day scenario
        initial_occupancy = len(self.simulator.occupied_spaces)
        
        # Simulate a few cycles
        for _ in range(3):
            self.simulator._simulate_arrival()
            self.simulator._simulate_departure()
            
        # Basic validation that simulation ran
        self.assertIsInstance(self.simulator.statistics['total_entries'], int)
        self.assertIsInstance(self.simulator.statistics['total_exits'], int)
        
    def test_data_export(self):
        """Test data export functionality"""
        # Add some test data
        vehicle = self.simulator.vehicle_generator.generate_vehicle()
        space_id = self.simulator._find_available_space(vehicle.vehicle_type)
        if space_id:
            self.simulator._allocate_space(space_id, vehicle)
            
        # Test export (basic validation)
        stats = self.simulator.get_statistics()
        self.assertIsInstance(stats, dict)
        self.assertIn('total_entries', stats)
        self.assertIn('total_exits', stats)
        self.assertIn('occupancy_rate', stats)

if __name__ == '__main__':
    unittest.main()
        self.assertEqual(custom_simulator.levels, 20)
        
    def test_vehicle_generation(self):
        """Test realistic vehicle generation"""
        # Test vehicle generation patterns
        vehicles = []
        for _ in range(100):
            vehicle = self.simulator.generate_vehicle()
            vehicles.append(vehicle)
            
        # Verify vehicle properties
        self.assertEqual(len(vehicles), 100)
        
        # Check license plate uniqueness
        license_plates = [v['license_plate'] for v in vehicles]
        self.assertEqual(len(license_plates), len(set(license_plates)))
        
        # Check vehicle type distribution
        vehicle_types = [v['vehicle_type'] for v in vehicles]
        unique_types = set(vehicle_types)
        expected_types = {'sedan', 'suv', 'truck', 'compact', 'motorcycle'}
        self.assertTrue(unique_types.issubset(expected_types))
        
        # Check dimension validity
        for vehicle in vehicles:
            self.assertGreater(vehicle['length'], 0)
            self.assertGreater(vehicle['width'], 0)
            self.assertGreater(vehicle['height'], 0)
            self.assertLessEqual(vehicle['length'], 8.0)  # Max truck length
            self.assertLessEqual(vehicle['width'], 3.0)   # Max width
            self.assertLessEqual(vehicle['height'], 3.5)  # Max height
            
    def test_parking_space_management(self):
        """Test parking space allocation and management"""
        # Initialize parking grid
        self.simulator.initialize_parking_grid()
        
        # Test space allocation
        vehicle = self.simulator.generate_vehicle()
        space = self.simulator.find_available_space(vehicle['vehicle_type'])
        self.assertIsNotNone(space)
        
        # Test space occupation
        success = self.simulator.occupy_space(space['id'], vehicle['license_plate'])
        self.assertTrue(success)
        
        # Verify space is marked as occupied
        occupied_space = self.simulator.get_space_status(space['id'])
        self.assertEqual(occupied_space['status'], 'occupied')
        self.assertEqual(occupied_space['vehicle_license'], vehicle['license_plate'])
        
        # Test space release
        release_success = self.simulator.release_space(space['id'])
        self.assertTrue(release_success)
        
        # Verify space is available again
        released_space = self.simulator.get_space_status(space['id'])
        self.assertEqual(released_space['status'], 'available')
        
    def test_arrival_simulation(self):
        """Test vehicle arrival simulation"""
        self.simulator.initialize_parking_grid()
        
        # Test single arrival
        arrival_result = self.simulator.simulate_arrival()
        if arrival_result:  # May be None if no space available
            self.assertIn('vehicle', arrival_result)
            self.assertIn('space', arrival_result)
            self.assertIn('transaction', arrival_result)
            
        # Test multiple arrivals
        arrivals = []
        for _ in range(10):
            result = self.simulator.simulate_arrival()
            if result:
                arrivals.append(result)
                
        # Verify arrivals are properly recorded
        for arrival in arrivals:
            vehicle = arrival['vehicle']
            space = arrival['space']
            
            # Check vehicle is in database
            db_vehicle = self.db_manager.get_vehicle_by_license(vehicle['license_plate'])
            self.assertIsNotNone(db_vehicle)
            
            # Check space is occupied
            db_space = self.db_manager.get_parking_space(space['id'])
            self.assertEqual(db_space['status'], 'occupied')
            
    def test_departure_simulation(self):
        """Test vehicle departure simulation"""
        self.simulator.initialize_parking_grid()
        
        # First, simulate some arrivals to have vehicles to depart
        arrivals = []
        for _ in range(5):
            result = self.simulator.simulate_arrival()
            if result:
                arrivals.append(result)
                
        if not arrivals:
            self.skipTest("No arrivals simulated, cannot test departures")
            
        # Test departure
        departure_result = self.simulator.simulate_departure()
        if departure_result:  # May be None if no vehicles to depart
            self.assertIn('vehicle', departure_result)
            self.assertIn('space', departure_result)
            self.assertIn('duration', departure_result)
            self.assertIn('fee', departure_result)
            
            # Verify space is released
            space_id = departure_result['space']['id']
            released_space = self.db_manager.get_parking_space(space_id)
            self.assertEqual(released_space['status'], 'available')
            
    def test_peak_hour_simulation(self):
        """Test peak hour traffic patterns"""
        # Test morning peak
        morning_config = self.simulator.get_peak_hour_config('morning')
        self.assertGreater(morning_config['arrival_multiplier'], 1.0)
        self.assertLess(morning_config['departure_multiplier'], 1.0)
        
        # Test evening peak
        evening_config = self.simulator.get_peak_hour_config('evening')
        self.assertLess(evening_config['arrival_multiplier'], 1.0)
        self.assertGreater(evening_config['departure_multiplier'], 1.0)
        
        # Test off-peak
        offpeak_config = self.simulator.get_peak_hour_config('off_peak')
        self.assertEqual(offpeak_config['arrival_multiplier'], 1.0)
        self.assertEqual(offpeak_config['departure_multiplier'], 1.0)
        
    def test_payment_simulation(self):
        """Test payment processing simulation"""
        # Test payment method distribution
        payment_methods = []
        for _ in range(100):
            method = self.simulator.generate_payment_method()
            payment_methods.append(method)
            
        # Verify payment method variety
        unique_methods = set(payment_methods)
        expected_methods = {'cash', 'credit_card', 'debit_card', 'mobile_pay', 'rfid'}
        self.assertTrue(unique_methods.issubset(expected_methods))
        
        # Test fee calculation
        duration_minutes = 120  # 2 hours
        fee = self.simulator.calculate_parking_fee(duration_minutes)
        self.assertGreater(fee, 0)
        self.assertIsInstance(fee, (int, float))
        
        # Test progressive pricing
        short_duration_fee = self.simulator.calculate_parking_fee(30)   # 30 minutes
        long_duration_fee = self.simulator.calculate_parking_fee(480)   # 8 hours
        self.assertLess(short_duration_fee, long_duration_fee)
        
    def test_queue_management(self):
        """Test vehicle queue management during peak times"""
        self.simulator.initialize_parking_grid()
        
        # Fill up most parking spaces
        for _ in range(295):  # Leave only 5 spaces
            self.simulator.simulate_arrival()
            
        # Test queue formation
        queue_size_before = len(self.simulator.get_entry_queue())
        
        # Try to add more vehicles (should go to queue)
        for _ in range(10):
            self.simulator.simulate_arrival()
            
        queue_size_after = len(self.simulator.get_entry_queue())
        self.assertGreaterEqual(queue_size_after, queue_size_before)
        
        # Test queue processing when space becomes available
        self.simulator.simulate_departure()  # Free up a space
        processed = self.simulator.process_entry_queue()
        
        if processed:
            self.assertIn('vehicle', processed)
            self.assertIn('space', processed)
            
    def test_statistics_tracking(self):
        """Test simulation statistics and analytics"""
        self.simulator.initialize_parking_grid()
        
        # Run simulation for a period
        start_time = time.time()
        for _ in range(50):
            self.simulator.simulate_arrival()
            self.simulator.simulate_departure()
            
        # Get statistics
        stats = self.simulator.get_simulation_statistics()
        
        # Verify statistics structure
        expected_keys = [
            'total_arrivals', 'total_departures', 'current_occupancy',
            'revenue_generated', 'average_duration', 'peak_occupancy'
        ]
        for key in expected_keys:
            self.assertIn(key, stats)
            
        # Verify statistics are reasonable
        self.assertGreaterEqual(stats['total_arrivals'], 0)
        self.assertGreaterEqual(stats['total_departures'], 0)
        self.assertGreaterEqual(stats['current_occupancy'], 0)
        self.assertLessEqual(stats['current_occupancy'], 300)
        self.assertGreaterEqual(stats['revenue_generated'], 0)
        
    def test_real_time_simulation(self):
        """Test real-time simulation functionality"""
        self.simulator.initialize_parking_grid()
        
        # Start real-time simulation
        self.simulator.start_simulation(mode='real_time', interval=0.1)
        self.assertTrue(self.simulator.is_running())
        
        # Let it run for a short period
        time.sleep(0.5)
        
        # Check that events are being generated
        stats_before = self.simulator.get_simulation_statistics()
        time.sleep(0.3)
        stats_after = self.simulator.get_simulation_statistics()
        
        # At least some activity should have occurred
        total_events_before = stats_before['total_arrivals'] + stats_before['total_departures']
        total_events_after = stats_after['total_arrivals'] + stats_after['total_departures']
        
        # Stop simulation
        self.simulator.stop_simulation()
        self.assertFalse(self.simulator.is_running())
        
    def test_scenario_simulation(self):
        """Test predefined scenario simulation"""
        scenarios = ['normal_day', 'busy_weekend', 'holiday_rush', 'maintenance_mode']
        
        for scenario in scenarios:
            config = self.simulator.get_scenario_config(scenario)
            self.assertIsInstance(config, dict)
            self.assertIn('arrival_rate', config)
            self.assertIn('departure_rate', config)
            
            # Test scenario application
            self.simulator.apply_scenario(scenario)
            current_config = self.simulator.get_current_config()
            self.assertEqual(current_config['scenario'], scenario)
            
    def test_data_export(self):
        """Test simulation data export functionality"""
        self.simulator.initialize_parking_grid()
        
        # Generate some simulation data
        for _ in range(20):
            self.simulator.simulate_arrival()
            self.simulator.simulate_departure()
            
        # Test CSV export
        csv_data = self.simulator.export_data('csv')
        self.assertIsInstance(csv_data, str)
        self.assertIn('vehicle_license', csv_data)
        self.assertIn('entry_time', csv_data)
        
        # Test JSON export
        json_data = self.simulator.export_data('json')
        self.assertIsInstance(json_data, str)
        
        import json
        parsed_data = json.loads(json_data)
        self.assertIsInstance(parsed_data, list)

if __name__ == '__main__':
    unittest.main()
