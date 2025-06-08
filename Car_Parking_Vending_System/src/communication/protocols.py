"""
Communication Protocols for Automated Car Parking System
Handles WebSocket, TCP/IP, Modbus, and OPC UA communication
"""

import asyncio
import websockets
import json
import logging
import threading
import time
import socket
import struct
from typing import Dict, List, Optional, Callable, Any
from datetime import datetime
from dataclasses import dataclass, asdict
import uuid

# Modbus communication
try:
    from pymodbus.client.sync import ModbusTcpClient
    from pymodbus.constants import Endian
    from pymodbus.payload import BinaryPayloadDecoder, BinaryPayloadBuilder
    MODBUS_AVAILABLE = True
except ImportError:
    MODBUS_AVAILABLE = False
    
# OPC UA communication
try:
    from opcua import Client as OPCClient
    from opcua import ua
    OPC_AVAILABLE = True
except ImportError:
    OPC_AVAILABLE = False

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class Message:
    """Communication message structure"""
    id: str
    type: str
    source: str
    destination: str
    timestamp: datetime
    data: Dict
    priority: int = 0

class WebSocketServer:
    """WebSocket server for real-time communication"""
    
    def __init__(self, host: str = "localhost", port: int = 8765):
        self.host = host
        self.port = port
        self.clients = set()
        self.message_handlers = {}
        self.running = False
        
    def register_handler(self, message_type: str, handler: Callable):
        """Register message handler"""
        self.message_handlers[message_type] = handler
        
    async def register_client(self, websocket, path):
        """Register new WebSocket client"""
        self.clients.add(websocket)
        logger.info(f"Client connected: {websocket.remote_address}")
        
        try:
            # Send welcome message
            welcome_msg = {
                "type": "connection_established",
                "timestamp": datetime.now().isoformat(),
                "client_id": str(uuid.uuid4())
            }
            await websocket.send(json.dumps(welcome_msg))
            
            # Handle incoming messages
            async for message in websocket:
                await self.handle_message(websocket, message)
                
        except websockets.exceptions.ConnectionClosed:
            logger.info(f"Client disconnected: {websocket.remote_address}")
        except Exception as e:
            logger.error(f"WebSocket error: {e}")
        finally:
            self.clients.discard(websocket)
            
    async def handle_message(self, websocket, message_str: str):
        """Handle incoming WebSocket message"""
        try:
            message_data = json.loads(message_str)
            message_type = message_data.get('type')
            
            if message_type in self.message_handlers:
                response = await self.message_handlers[message_type](message_data)
                if response:
                    await websocket.send(json.dumps(response))
            else:
                logger.warning(f"Unknown message type: {message_type}")
                
        except json.JSONDecodeError:
            logger.error("Invalid JSON message received")
        except Exception as e:
            logger.error(f"Message handling error: {e}")
            
    async def broadcast(self, message: Dict):
        """Broadcast message to all connected clients"""
        if self.clients:
            message_str = json.dumps(message)
            await asyncio.gather(
                *[client.send(message_str) for client in self.clients],
                return_exceptions=True
            )
            
    async def send_to_client(self, client, message: Dict):
        """Send message to specific client"""
        try:
            await client.send(json.dumps(message))
        except Exception as e:
            logger.error(f"Error sending message to client: {e}")
            
    def start_server(self):
        """Start WebSocket server"""
        self.running = True
        return websockets.serve(self.register_client, self.host, self.port)

class TCPServer:
    """TCP server for PLC communication"""
    
    def __init__(self, host: str = "localhost", port: int = 9001):
        self.host = host
        self.port = port
        self.socket = None
        self.clients = []
        self.running = False
        self.message_handlers = {}
        
    def register_handler(self, command: str, handler: Callable):
        """Register command handler"""
        self.message_handlers[command] = handler
        
    def start_server(self):
        """Start TCP server"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket.bind((self.host, self.port))
            self.socket.listen(5)
            self.running = True
            
            logger.info(f"TCP server started on {self.host}:{self.port}")
            
            while self.running:
                try:
                    client_socket, address = self.socket.accept()
                    logger.info(f"TCP client connected: {address}")
                    
                    # Handle client in separate thread
                    client_thread = threading.Thread(
                        target=self.handle_client,
                        args=(client_socket, address)
                    )
                    client_thread.daemon = True
                    client_thread.start()
                    
                except Exception as e:
                    if self.running:
                        logger.error(f"TCP server error: {e}")
                        
        except Exception as e:
            logger.error(f"Failed to start TCP server: {e}")
            
    def handle_client(self, client_socket, address):
        """Handle TCP client connection"""
        try:
            self.clients.append(client_socket)
            
            while self.running:
                # Receive data
                data = client_socket.recv(1024)
                if not data:
                    break
                    
                # Process message
                try:
                    message = json.loads(data.decode('utf-8'))
                    response = self.process_message(message)
                    
                    if response:
                        client_socket.send(json.dumps(response).encode('utf-8'))
                        
                except json.JSONDecodeError:
                    logger.error("Invalid JSON received from TCP client")
                except Exception as e:
                    logger.error(f"TCP message processing error: {e}")
                    
        except Exception as e:
            logger.error(f"TCP client error: {e}")
        finally:
            self.clients.remove(client_socket)
            client_socket.close()
            logger.info(f"TCP client disconnected: {address}")
            
    def process_message(self, message: Dict) -> Optional[Dict]:
        """Process incoming TCP message"""
        command = message.get('command')
        
        if command in self.message_handlers:
            return self.message_handlers[command](message)
        else:
            logger.warning(f"Unknown TCP command: {command}")
            return {"status": "error", "message": f"Unknown command: {command}"}
            
    def broadcast(self, message: Dict):
        """Broadcast message to all TCP clients"""
        message_str = json.dumps(message).encode('utf-8')
        
        for client in self.clients[:]:  # Copy list to avoid modification during iteration
            try:
                client.send(message_str)
            except Exception as e:
                logger.error(f"Error broadcasting to TCP client: {e}")
                self.clients.remove(client)
                
    def stop_server(self):
        """Stop TCP server"""
        self.running = False
        if self.socket:
            self.socket.close()

class ModbusClient:
    """Modbus TCP client for PLC communication"""
    
    def __init__(self, host: str = "192.168.1.100", port: int = 502, unit_id: int = 1):
        if not MODBUS_AVAILABLE:
            raise ImportError("pymodbus library not available")
            
        self.host = host
        self.port = port
        self.unit_id = unit_id
        self.client = None
        self.connected = False
        
    def connect(self) -> bool:
        """Connect to Modbus server"""
        try:
            self.client = ModbusTcpClient(self.host, port=self.port)
            self.connected = self.client.connect()
            
            if self.connected:
                logger.info(f"Connected to Modbus server: {self.host}:{self.port}")
            else:
                logger.error("Failed to connect to Modbus server")
                
            return self.connected
            
        except Exception as e:
            logger.error(f"Modbus connection error: {e}")
            return False
            
    def disconnect(self):
        """Disconnect from Modbus server"""
        if self.client and self.connected:
            self.client.close()
            self.connected = False
            logger.info("Disconnected from Modbus server")
            
    def read_coils(self, address: int, count: int = 1) -> Optional[List[bool]]:
        """Read coil registers"""
        if not self.connected:
            return None
            
        try:
            result = self.client.read_coils(address, count, unit=self.unit_id)
            if result.isError():
                logger.error(f"Modbus read coils error: {result}")
                return None
            return result.bits[:count]
            
        except Exception as e:
            logger.error(f"Error reading coils: {e}")
            return None
            
    def write_coil(self, address: int, value: bool) -> bool:
        """Write single coil"""
        if not self.connected:
            return False
            
        try:
            result = self.client.write_coil(address, value, unit=self.unit_id)
            return not result.isError()
            
        except Exception as e:
            logger.error(f"Error writing coil: {e}")
            return False
            
    def read_holding_registers(self, address: int, count: int = 1) -> Optional[List[int]]:
        """Read holding registers"""
        if not self.connected:
            return None
            
        try:
            result = self.client.read_holding_registers(address, count, unit=self.unit_id)
            if result.isError():
                logger.error(f"Modbus read registers error: {result}")
                return None
            return result.registers
            
        except Exception as e:
            logger.error(f"Error reading holding registers: {e}")
            return None
            
    def write_register(self, address: int, value: int) -> bool:
        """Write single holding register"""
        if not self.connected:
            return False
            
        try:
            result = self.client.write_register(address, value, unit=self.unit_id)
            return not result.isError()
            
        except Exception as e:
            logger.error(f"Error writing register: {e}")
            return False
            
    def read_float(self, address: int) -> Optional[float]:
        """Read float value from two consecutive registers"""
        registers = self.read_holding_registers(address, 2)
        if registers:
            decoder = BinaryPayloadDecoder.fromRegisters(registers, byteorder=Endian.Big)
            return decoder.decode_32bit_float()
        return None
        
    def write_float(self, address: int, value: float) -> bool:
        """Write float value to two consecutive registers"""
        if not self.connected:
            return False
            
        try:
            builder = BinaryPayloadBuilder(byteorder=Endian.Big)
            builder.add_32bit_float(value)
            payload = builder.to_registers()
            
            result = self.client.write_registers(address, payload, unit=self.unit_id)
            return not result.isError()
            
        except Exception as e:
            logger.error(f"Error writing float: {e}")
            return False

class OPCUAClient:
    """OPC UA client for industrial communication"""
    
    def __init__(self, endpoint: str = "opc.tcp://localhost:4840"):
        if not OPC_AVAILABLE:
            raise ImportError("opcua library not available")
            
        self.endpoint = endpoint
        self.client = None
        self.connected = False
        self.subscription = None
        self.node_handlers = {}
        
    def connect(self) -> bool:
        """Connect to OPC UA server"""
        try:
            self.client = OPCClient(self.endpoint)
            self.client.connect()
            self.connected = True
            
            logger.info(f"Connected to OPC UA server: {self.endpoint}")
            return True
            
        except Exception as e:
            logger.error(f"OPC UA connection error: {e}")
            return False
            
    def disconnect(self):
        """Disconnect from OPC UA server"""
        if self.client and self.connected:
            if self.subscription:
                self.subscription.delete()
            self.client.disconnect()
            self.connected = False
            logger.info("Disconnected from OPC UA server")
            
    def read_node(self, node_id: str) -> Any:
        """Read node value"""
        if not self.connected:
            return None
            
        try:
            node = self.client.get_node(node_id)
            return node.get_value()
            
        except Exception as e:
            logger.error(f"Error reading OPC UA node: {e}")
            return None
            
    def write_node(self, node_id: str, value: Any) -> bool:
        """Write node value"""
        if not self.connected:
            return False
            
        try:
            node = self.client.get_node(node_id)
            node.set_value(value)
            return True
            
        except Exception as e:
            logger.error(f"Error writing OPC UA node: {e}")
            return False
            
    def subscribe_node(self, node_id: str, handler: Callable):
        """Subscribe to node value changes"""
        if not self.connected:
            return False
            
        try:
            if not self.subscription:
                self.subscription = self.client.create_subscription(1000, self)
                
            node = self.client.get_node(node_id)
            self.subscription.subscribe_data_change(node, handler)
            self.node_handlers[node_id] = handler
            
            return True
            
        except Exception as e:
            logger.error(f"Error subscribing to OPC UA node: {e}")
            return False

class CommunicationManager:
    """Central communication manager"""
    
    def __init__(self):
        self.websocket_server = None
        self.tcp_server = None
        self.modbus_client = None
        self.opcua_client = None
        
        self.message_queue = []
        self.running = False
        
        # Message routing table
        self.routes = {
            'hmi': [],
            'plc': [],
            'database': [],
            'external': []
        }
        
    def setup_websocket_server(self, host: str = "localhost", port: int = 8765):
        """Setup WebSocket server"""
        self.websocket_server = WebSocketServer(host, port)
        
        # Register standard handlers
        self.websocket_server.register_handler('system_status', self.handle_system_status)
        self.websocket_server.register_handler('parking_command', self.handle_parking_command)
        self.websocket_server.register_handler('elevator_command', self.handle_elevator_command)
        self.websocket_server.register_handler('emergency_stop', self.handle_emergency_stop)
        
    def setup_tcp_server(self, host: str = "localhost", port: int = 9001):
        """Setup TCP server"""
        self.tcp_server = TCPServer(host, port)
        
        # Register standard handlers
        self.tcp_server.register_handler('READ_STATUS', self.handle_plc_read_status)
        self.tcp_server.register_handler('WRITE_OUTPUT', self.handle_plc_write_output)
        self.tcp_server.register_handler('EMERGENCY_STOP', self.handle_plc_emergency)
        
    def setup_modbus_client(self, host: str = "192.168.1.100", port: int = 502):
        """Setup Modbus client"""
        if MODBUS_AVAILABLE:
            self.modbus_client = ModbusClient(host, port)
        else:
            logger.warning("Modbus client not available - pymodbus not installed")
            
    def setup_opcua_client(self, endpoint: str = "opc.tcp://localhost:4840"):
        """Setup OPC UA client"""
        if OPC_AVAILABLE:
            self.opcua_client = OPCUAClient(endpoint)
        else:
            logger.warning("OPC UA client not available - opcua not installed")
            
    def start_all_services(self):
        """Start all communication services"""
        self.running = True
        
        # Start WebSocket server
        if self.websocket_server:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            websocket_thread = threading.Thread(
                target=self.run_websocket_server,
                args=(loop,)
            )
            websocket_thread.daemon = True
            websocket_thread.start()
            
        # Start TCP server
        if self.tcp_server:
            tcp_thread = threading.Thread(target=self.tcp_server.start_server)
            tcp_thread.daemon = True
            tcp_thread.start()
            
        # Connect Modbus client
        if self.modbus_client:
            self.modbus_client.connect()
            
        # Connect OPC UA client
        if self.opcua_client:
            self.opcua_client.connect()
            
        logger.info("All communication services started")
        
    def run_websocket_server(self, loop):
        """Run WebSocket server in event loop"""
        asyncio.set_event_loop(loop)
        start_server = self.websocket_server.start_server()
        loop.run_until_complete(start_server)
        loop.run_forever()
        
    def stop_all_services(self):
        """Stop all communication services"""
        self.running = False
        
        if self.tcp_server:
            self.tcp_server.stop_server()
            
        if self.modbus_client:
            self.modbus_client.disconnect()
            
        if self.opcua_client:
            self.opcua_client.disconnect()
            
        logger.info("All communication services stopped")
        
    # Message Handlers
    async def handle_system_status(self, message: Dict) -> Dict:
        """Handle system status request"""
        return {
            "type": "system_status_response",
            "timestamp": datetime.now().isoformat(),
            "status": "operational",
            "services": {
                "websocket": self.websocket_server is not None,
                "tcp": self.tcp_server is not None and self.tcp_server.running,
                "modbus": self.modbus_client is not None and self.modbus_client.connected,
                "opcua": self.opcua_client is not None and self.opcua_client.connected
            }
        }
        
    async def handle_parking_command(self, message: Dict) -> Dict:
        """Handle parking command"""
        command = message.get('command')
        params = message.get('params', {})
        
        # Forward to PLC via Modbus/TCP
        if self.modbus_client and self.modbus_client.connected:
            # Example: Write command to PLC
            if command == 'park_vehicle':
                success = self.modbus_client.write_register(1000, 1)  # Park command
                return {"status": "success" if success else "error"}
                
        return {"status": "error", "message": "PLC not connected"}
        
    async def handle_elevator_command(self, message: Dict) -> Dict:
        """Handle elevator command"""
        elevator_id = message.get('elevator_id')
        command = message.get('command')
        level = message.get('level')
        
        # Forward to PLC
        if self.modbus_client and self.modbus_client.connected:
            # Write elevator command
            register_base = 2000 + (elevator_id * 10)
            
            if command == 'move_to_level':
                success = self.modbus_client.write_register(register_base, level)
                return {"status": "success" if success else "error"}
                
        return {"status": "error", "message": "PLC not connected"}
        
    async def handle_emergency_stop(self, message: Dict) -> Dict:
        """Handle emergency stop"""
        # Set emergency stop flag
        if self.modbus_client and self.modbus_client.connected:
            success = self.modbus_client.write_coil(0, True)  # Emergency stop coil
            
            # Broadcast emergency stop to all clients
            emergency_msg = {
                "type": "emergency_alert",
                "timestamp": datetime.now().isoformat(),
                "message": "Emergency stop activated"
            }
            
            if self.websocket_server:
                await self.websocket_server.broadcast(emergency_msg)
                
            if self.tcp_server:
                self.tcp_server.broadcast(emergency_msg)
                
            return {"status": "success" if success else "error"}
            
        return {"status": "error", "message": "PLC not connected"}
        
    def handle_plc_read_status(self, message: Dict) -> Dict:
        """Handle PLC status read request"""
        if self.modbus_client and self.modbus_client.connected:
            try:
                # Read system status registers
                status_registers = self.modbus_client.read_holding_registers(0, 10)
                
                if status_registers:
                    return {
                        "command": "READ_STATUS_RESPONSE",
                        "status": "success",
                        "data": status_registers
                    }
                    
            except Exception as e:
                logger.error(f"Error reading PLC status: {e}")
                
        return {"command": "READ_STATUS_RESPONSE", "status": "error"}
        
    def handle_plc_write_output(self, message: Dict) -> Dict:
        """Handle PLC output write request"""
        address = message.get('address')
        value = message.get('value')
        
        if self.modbus_client and self.modbus_client.connected:
            success = self.modbus_client.write_register(address, value)
            return {
                "command": "WRITE_OUTPUT_RESPONSE",
                "status": "success" if success else "error"
            }
            
        return {"command": "WRITE_OUTPUT_RESPONSE", "status": "error"}
        
    def handle_plc_emergency(self, message: Dict) -> Dict:
        """Handle PLC emergency request"""
        if self.modbus_client and self.modbus_client.connected:
            success = self.modbus_client.write_coil(0, True)
            return {
                "command": "EMERGENCY_RESPONSE",
                "status": "success" if success else "error"
            }
            
        return {"command": "EMERGENCY_RESPONSE", "status": "error"}
        
    def send_system_update(self, update_data: Dict):
        """Send system update to all connected clients"""
        message = {
            "type": "system_update",
            "timestamp": datetime.now().isoformat(),
            "data": update_data
        }
        
        # Send via WebSocket
        if self.websocket_server:
            asyncio.create_task(self.websocket_server.broadcast(message))
            
        # Send via TCP
        if self.tcp_server:
            self.tcp_server.broadcast(message)

if __name__ == "__main__":
    # Test communication manager
    comm_manager = CommunicationManager()
    
    # Setup services
    comm_manager.setup_websocket_server()
    comm_manager.setup_tcp_server()
    comm_manager.setup_modbus_client()
    
    try:
        # Start services
        comm_manager.start_all_services()
        
        # Keep running
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\nStopping communication services...")
        comm_manager.stop_all_services()
