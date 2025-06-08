"""
Unit tests for Communication Protocols
Tests WebSocket, TCP, Modbus, and OPC UA communication
"""

import unittest
import asyncio
import threading
import time
import json
import tempfile
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from communication.protocols import CommunicationManager
from unittest.mock import Mock, patch, MagicMock

class TestCommunicationManager(unittest.TestCase):
    """Test cases for CommunicationManager class"""
    
    def setUp(self):
        """Set up test communication manager"""
        config = {
            'websocket': {
                'host': 'localhost',
                'port': 8765,
                'max_connections': 10
            },
            'tcp': {
                'host': 'localhost',
                'port': 9001,
                'buffer_size': 1024
            },
            'modbus': {
                'host': '192.168.1.100',
                'port': 502,
                'unit_id': 1
            },
            'opcua': {
                'endpoint': 'opc.tcp://localhost:4840',
                'namespace': 'http://example.com'
            }
        }
        self.comm_manager = CommunicationManager(config)
        
    def tearDown(self):
        """Clean up communication manager"""
        self.comm_manager.stop_all_servers()
        
    def test_websocket_server_initialization(self):
        """Test WebSocket server startup and configuration"""
        # Test server configuration
        self.assertEqual(self.comm_manager.websocket_config['host'], 'localhost')
        self.assertEqual(self.comm_manager.websocket_config['port'], 8765)
        
        # Test server startup
        self.assertTrue(self.comm_manager.start_websocket_server())
        self.assertTrue(self.comm_manager.websocket_server_running)
        
        # Test server shutdown
        self.comm_manager.stop_websocket_server()
        self.assertFalse(self.comm_manager.websocket_server_running)
        
    def test_tcp_server_initialization(self):
        """Test TCP server startup and configuration"""
        # Test server configuration
        self.assertEqual(self.comm_manager.tcp_config['host'], 'localhost')
        self.assertEqual(self.comm_manager.tcp_config['port'], 9001)
        
        # Test server startup
        self.assertTrue(self.comm_manager.start_tcp_server())
        self.assertTrue(self.comm_manager.tcp_server_running)
        
        # Test server shutdown
        self.comm_manager.stop_tcp_server()
        self.assertFalse(self.comm_manager.tcp_server_running)
        
    @patch('pymodbus.client.sync.ModbusTcpClient')
    def test_modbus_client_operations(self, mock_modbus_client):
        """Test Modbus TCP client operations"""
        # Mock Modbus client
        mock_client = Mock()
        mock_modbus_client.return_value = mock_client
        mock_client.connect.return_value = True
        mock_client.is_socket_open.return_value = True
        
        # Test connection
        self.assertTrue(self.comm_manager.connect_modbus())
        mock_client.connect.assert_called_once()
        
        # Test read operations
        mock_client.read_holding_registers.return_value = Mock(registers=[100, 200, 300])
        values = self.comm_manager.read_modbus_registers(0, 3)
        self.assertEqual(values, [100, 200, 300])
        
        # Test write operations
        mock_client.write_register.return_value = Mock(isError=lambda: False)
        self.assertTrue(self.comm_manager.write_modbus_register(0, 500))
        
        # Test disconnection
        self.comm_manager.disconnect_modbus()
        mock_client.close.assert_called_once()
        
    @patch('opcua.Client')
    def test_opcua_client_operations(self, mock_opcua_client):
        """Test OPC UA client operations"""
        # Mock OPC UA client
        mock_client = Mock()
        mock_opcua_client.return_value = mock_client
        
        # Test connection
        self.assertTrue(self.comm_manager.connect_opcua())
        mock_client.connect.assert_called_once()
        
        # Test node operations
        mock_node = Mock()
        mock_client.get_node.return_value = mock_node
        mock_node.get_value.return_value = 42.5
        
        value = self.comm_manager.read_opcua_node('ns=2;i=1001')
        self.assertEqual(value, 42.5)
        
        # Test write operations
        self.assertTrue(self.comm_manager.write_opcua_node('ns=2;i=1001', 55.0))
        mock_node.set_value.assert_called_with(55.0)
        
        # Test disconnection
        self.comm_manager.disconnect_opcua()
        mock_client.disconnect.assert_called_once()
        
    def test_message_routing(self):
        """Test message routing between protocols"""
        # Test message queue
        message = {
            'type': 'system_status',
            'data': {'status': 'operational'},
            'timestamp': time.time()
        }
        
        self.comm_manager.add_message_to_queue('websocket', message)
        self.assertEqual(len(self.comm_manager.message_queues['websocket']), 1)
        
        # Test message routing
        routes = {
            'system_status': ['websocket', 'tcp'],
            'alarm': ['websocket', 'tcp', 'modbus']
        }
        self.comm_manager.configure_message_routing(routes)
        
        # Test broadcast message
        alarm_message = {
            'type': 'alarm',
            'data': {'level': 'critical', 'message': 'Fire detected'},
            'timestamp': time.time()
        }
        
        self.comm_manager.broadcast_message(alarm_message)
        
        # Verify message was routed to correct protocols
        self.assertEqual(len(self.comm_manager.message_queues['websocket']), 2)
        self.assertEqual(len(self.comm_manager.message_queues['tcp']), 1)
        
    def test_connection_monitoring(self):
        """Test connection health monitoring"""
        # Test connection status tracking
        self.assertFalse(self.comm_manager.is_modbus_connected())
        self.assertFalse(self.comm_manager.is_opcua_connected())
        
        # Test heartbeat functionality
        with patch.object(self.comm_manager, 'send_heartbeat') as mock_heartbeat:
            self.comm_manager.start_heartbeat_monitoring(interval=0.1)
            time.sleep(0.3)  # Wait for a few heartbeats
            self.comm_manager.stop_heartbeat_monitoring()
            
            # Verify heartbeats were sent
            self.assertGreater(mock_heartbeat.call_count, 1)
            
    def test_automatic_reconnection(self):
        """Test automatic reconnection functionality"""
        with patch.object(self.comm_manager, 'connect_modbus') as mock_connect:
            mock_connect.side_effect = [False, False, True]  # Fail twice, then succeed
            
            # Enable auto-reconnection
            self.comm_manager.enable_auto_reconnection('modbus', max_attempts=3, interval=0.1)
            
            # Trigger reconnection
            success = self.comm_manager.attempt_reconnection('modbus')
            self.assertTrue(success)
            self.assertEqual(mock_connect.call_count, 3)
            
    def test_data_validation(self):
        """Test message data validation"""
        # Test valid message
        valid_message = {
            'type': 'system_status',
            'data': {'status': 'operational'},
            'timestamp': time.time()
        }
        self.assertTrue(self.comm_manager.validate_message(valid_message))
        
        # Test invalid messages
        invalid_messages = [
            {},  # Empty message
            {'type': 'test'},  # Missing data
            {'data': {'test': 'value'}},  # Missing type
            {'type': '', 'data': {}},  # Empty type
            {'type': 'test', 'data': None}  # None data
        ]
        
        for invalid_msg in invalid_messages:
            self.assertFalse(self.comm_manager.validate_message(invalid_msg))
            
    def test_message_serialization(self):
        """Test message serialization and deserialization"""
        original_message = {
            'type': 'parking_status',
            'data': {
                'space_id': 150,
                'status': 'occupied',
                'vehicle': 'ABC123',
                'timestamp': time.time()
            }
        }
        
        # Test JSON serialization
        serialized = self.comm_manager.serialize_message(original_message, 'json')
        self.assertIsInstance(serialized, str)
        
        # Test deserialization
        deserialized = self.comm_manager.deserialize_message(serialized, 'json')
        self.assertEqual(deserialized['type'], original_message['type'])
        self.assertEqual(deserialized['data']['space_id'], original_message['data']['space_id'])
        
        # Test binary serialization
        binary_data = self.comm_manager.serialize_message(original_message, 'binary')
        self.assertIsInstance(binary_data, bytes)
        
        binary_deserialized = self.comm_manager.deserialize_message(binary_data, 'binary')
        self.assertEqual(binary_deserialized['type'], original_message['type'])
        
    def test_error_handling(self):
        """Test error handling and recovery"""
        # Test connection error handling
        with patch.object(self.comm_manager, 'connect_modbus', side_effect=Exception("Connection failed")):
            self.assertFalse(self.comm_manager.connect_modbus())
            
        # Test message sending error handling
        with patch.object(self.comm_manager, 'send_websocket_message', side_effect=Exception("Send failed")):
            result = self.comm_manager.send_websocket_message({'type': 'test', 'data': {}})
            self.assertFalse(result)
            
        # Test protocol-specific error handling
        error_counts = self.comm_manager.get_error_statistics()
        self.assertIsInstance(error_counts, dict)
        
    def test_performance_monitoring(self):
        """Test communication performance monitoring"""
        # Test message throughput tracking
        start_time = time.time()
        for i in range(100):
            message = {
                'type': 'test_message',
                'data': {'counter': i},
                'timestamp': time.time()
            }
            self.comm_manager.track_message_performance(message, 'websocket')
            
        # Get performance statistics
        stats = self.comm_manager.get_performance_statistics()
        self.assertIn('websocket', stats)
        self.assertIn('message_count', stats['websocket'])
        self.assertIn('average_processing_time', stats['websocket'])
        
    def test_security_features(self):
        """Test communication security features"""
        # Test message encryption/decryption
        original_data = "Sensitive parking system data"
        encrypted = self.comm_manager.encrypt_message(original_data)
        self.assertNotEqual(encrypted, original_data)
        
        decrypted = self.comm_manager.decrypt_message(encrypted)
        self.assertEqual(decrypted, original_data)
        
        # Test authentication
        auth_token = self.comm_manager.generate_auth_token('admin_user')
        self.assertIsInstance(auth_token, str)
        self.assertGreater(len(auth_token), 0)
        
        # Test token validation
        self.assertTrue(self.comm_manager.validate_auth_token(auth_token, 'admin_user'))
        self.assertFalse(self.comm_manager.validate_auth_token('invalid_token', 'admin_user'))

if __name__ == '__main__':
    unittest.main()
