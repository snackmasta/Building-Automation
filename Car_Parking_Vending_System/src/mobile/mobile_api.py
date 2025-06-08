# filepath: c:\Users\Legion\Desktop\PLC\Car_Parking_Vending_System\src\mobile\mobile_api.py
"""
Mobile Application API for Car Parking Vending System
RESTful API designed for mobile app integration
"""

from flask import Flask, request, jsonify, abort
from flask_cors import CORS
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import qrcode
from io import BytesIO
import base64
from PIL import Image
import sqlite3
import os

class MobileAPI:
    """Mobile API server for parking system"""
    
    def __init__(self, db_path: str, security_manager, parking_simulator):
        self.app = Flask(__name__)
        CORS(self.app)
        
        self.db_path = db_path
        self.security = security_manager
        self.parking_sim = parking_simulator
        
        # Set up logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        # Initialize routes
        self._init_routes()
        
    def _init_routes(self):
        """Initialize API routes"""
        
        @self.app.route('/api/v1/auth/login', methods=['POST'])
        def login():
            """User authentication"""
            data = request.get_json()
            username = data.get('username')
            password = data.get('password')
            
            if not username or not password:
                return jsonify({'error': 'Username and password required'}), 400
                
            auth_result = self.security.authenticate_user(
                username, password, 
                request.remote_addr, 
                request.headers.get('User-Agent')
            )
            
            if auth_result:
                # Generate JWT token for mobile
                jwt_token = self.security.generate_jwt_token(auth_result)
                
                return jsonify({
                    'success': True,
                    'user': {
                        'id': auth_result['user_id'],
                        'username': auth_result['username'],
                        'email': auth_result['email'],
                        'role': auth_result['role']
                    },
                    'tokens': {
                        'access_token': jwt_token,
                        'session_token': auth_result['session_token']
                    }
                })
            else:
                return jsonify({'error': 'Invalid credentials'}), 401
                
        @self.app.route('/api/v1/auth/logout', methods=['POST'])
        def logout():
            """User logout"""
            token = request.headers.get('Authorization', '').replace('Bearer ', '')
            if self.security.logout_user(token):
                return jsonify({'success': True})
            return jsonify({'error': 'Invalid session'}), 401
            
        @self.app.route('/api/v1/parking/availability', methods=['GET'])
        def get_availability():
            """Get real-time parking availability"""
            try:
                with sqlite3.connect(self.db_path) as conn:
                    conn.row_factory = sqlite3.Row
                    cursor = conn.cursor()
                    
                    # Get current availability
                    cursor.execute("""
                        SELECT 
                            COUNT(*) as total_spaces,
                            COUNT(CASE WHEN is_occupied = 0 THEN 1 END) as available_spaces,
                            COUNT(CASE WHEN is_occupied = 1 THEN 1 END) as occupied_spaces
                        FROM parking_spaces 
                        WHERE is_active = 1
                    """)
                    
                    stats = dict(cursor.fetchone())
                    
                    # Get availability by level
                    cursor.execute("""
                        SELECT 
                            level,
                            COUNT(*) as total_spaces,
                            COUNT(CASE WHEN is_occupied = 0 THEN 1 END) as available_spaces
                        FROM parking_spaces 
                        WHERE is_active = 1
                        GROUP BY level
                        ORDER BY level
                    """)
                    
                    levels = [dict(row) for row in cursor.fetchall()]
                    
                return jsonify({
                    'success': True,
                    'data': {
                        'overall': stats,
                        'by_level': levels,
                        'last_updated': datetime.now().isoformat()
                    }
                })
                
            except Exception as e:
                self.logger.error(f"Error getting availability: {e}")
                return jsonify({'error': 'Internal server error'}), 500
                
        @self.app.route('/api/v1/parking/reserve', methods=['POST'])
        def reserve_space():
            """Reserve a parking space"""
            # Verify authentication
            user = self._verify_token()
            if not user:
                return jsonify({'error': 'Authentication required'}), 401
                
            data = request.get_json()
            vehicle_info = data.get('vehicle_info', {})
            preferred_level = data.get('preferred_level')
            duration_hours = data.get('duration_hours', 2)
            
            try:
                # Find available space
                space = self._find_available_space(preferred_level, vehicle_info)
                if not space:
                    return jsonify({'error': 'No available spaces'}), 409
                    
                # Create reservation
                reservation_id = self._create_reservation(
                    user['user_id'], space['id'], vehicle_info, duration_hours
                )
                
                # Generate QR code for entry
                qr_code = self._generate_qr_code(reservation_id)
                
                return jsonify({
                    'success': True,
                    'data': {
                        'reservation_id': reservation_id,
                        'space': space,
                        'qr_code': qr_code,
                        'expires_at': (datetime.now() + timedelta(minutes=15)).isoformat(),
                        'estimated_cost': self._calculate_cost(duration_hours)
                    }
                })
                
            except Exception as e:
                self.logger.error(f"Error creating reservation: {e}")
                return jsonify({'error': 'Failed to create reservation'}), 500
                
        @self.app.route('/api/v1/parking/checkin', methods=['POST'])
        def checkin():
            """Check into reserved parking space"""
            user = self._verify_token()
            if not user:
                return jsonify({'error': 'Authentication required'}), 401
                
            data = request.get_json()
            reservation_id = data.get('reservation_id')
            qr_code_data = data.get('qr_code')
            
            try:
                # Verify reservation and QR code
                if not self._verify_reservation(reservation_id, qr_code_data, user['user_id']):
                    return jsonify({'error': 'Invalid reservation'}), 400
                    
                # Process check-in
                parking_session = self._process_checkin(reservation_id)
                
                return jsonify({
                    'success': True,
                    'data': {
                        'session_id': parking_session['id'],
                        'space': parking_session['space'],
                        'checked_in_at': parking_session['checked_in_at'],
                        'checkout_qr': self._generate_checkout_qr(parking_session['id'])
                    }
                })
                
            except Exception as e:
                self.logger.error(f"Error processing checkin: {e}")
                return jsonify({'error': 'Checkin failed'}), 500
                
        @self.app.route('/api/v1/parking/checkout', methods=['POST'])
        def checkout():
            """Check out of parking space"""
            user = self._verify_token()
            if not user:
                return jsonify({'error': 'Authentication required'}), 401
                
            data = request.get_json()
            session_id = data.get('session_id')
            payment_method = data.get('payment_method')
            
            try:
                # Calculate final cost
                cost_info = self._calculate_final_cost(session_id)
                
                # Process payment
                payment_result = self._process_payment(
                    cost_info['amount'], payment_method, user['user_id']
                )
                
                if payment_result['success']:
                    # Complete checkout
                    checkout_info = self._complete_checkout(session_id, payment_result['transaction_id'])
                    
                    return jsonify({
                        'success': True,
                        'data': {
                            'checkout_time': checkout_info['checkout_time'],
                            'total_cost': cost_info['amount'],
                            'duration': cost_info['duration'],
                            'receipt': checkout_info['receipt'],
                            'exit_qr': self._generate_exit_qr(session_id)
                        }
                    })
                else:
                    return jsonify({'error': 'Payment failed'}), 402
                    
            except Exception as e:
                self.logger.error(f"Error processing checkout: {e}")
                return jsonify({'error': 'Checkout failed'}), 500
                
        @self.app.route('/api/v1/user/history', methods=['GET'])
        def get_parking_history():
            """Get user's parking history"""
            user = self._verify_token()
            if not user:
                return jsonify({'error': 'Authentication required'}), 401
                
            try:
                with sqlite3.connect(self.db_path) as conn:
                    conn.row_factory = sqlite3.Row
                    cursor = conn.cursor()
                    
                    cursor.execute("""
                        SELECT 
                            t.id, t.transaction_date, t.amount, t.status,
                            ps.level, ps.space_number,
                            v.license_plate, v.make, v.model
                        FROM transactions t
                        LEFT JOIN parking_spaces ps ON t.space_id = ps.id
                        LEFT JOIN vehicles v ON t.vehicle_id = v.id
                        WHERE t.user_id = ?
                        ORDER BY t.transaction_date DESC
                        LIMIT 50
                    """, (user['user_id'],))
                    
                    history = [dict(row) for row in cursor.fetchall()]
                    
                return jsonify({
                    'success': True,
                    'data': history
                })
                
            except Exception as e:
                self.logger.error(f"Error getting history: {e}")
                return jsonify({'error': 'Failed to get history'}), 500
                
        @self.app.route('/api/v1/user/profile', methods=['GET'])
        def get_profile():
            """Get user profile"""
            user = self._verify_token()
            if not user:
                return jsonify({'error': 'Authentication required'}), 401
                
            try:
                with sqlite3.connect(self.db_path) as conn:
                    conn.row_factory = sqlite3.Row
                    cursor = conn.cursor()
                    
                    cursor.execute("""
                        SELECT username, email, created_at, last_login
                        FROM users WHERE id = ?
                    """, (user['user_id'],))
                    
                    profile = dict(cursor.fetchone())
                    
                    # Get user's vehicles
                    cursor.execute("""
                        SELECT license_plate, make, model, color, vehicle_type
                        FROM vehicles WHERE user_id = ?
                    """, (user['user_id'],))
                    
                    vehicles = [dict(row) for row in cursor.fetchall()]
                    profile['vehicles'] = vehicles
                    
                return jsonify({
                    'success': True,
                    'data': profile
                })
                
            except Exception as e:
                self.logger.error(f"Error getting profile: {e}")
                return jsonify({'error': 'Failed to get profile'}), 500
                
        @self.app.route('/api/v1/user/vehicles', methods=['POST'])
        def add_vehicle():
            """Add vehicle to user profile"""
            user = self._verify_token()
            if not user:
                return jsonify({'error': 'Authentication required'}), 401
                
            data = request.get_json()
            required_fields = ['license_plate', 'make', 'model']
            
            if not all(field in data for field in required_fields):
                return jsonify({'error': 'Missing required vehicle information'}), 400
                
            try:
                with sqlite3.connect(self.db_path) as conn:
                    cursor = conn.cursor()
                    cursor.execute("""
                        INSERT INTO vehicles (user_id, license_plate, make, model, color, vehicle_type)
                        VALUES (?, ?, ?, ?, ?, ?)
                    """, (
                        user['user_id'],
                        data['license_plate'],
                        data['make'],
                        data['model'],
                        data.get('color', ''),
                        data.get('vehicle_type', 'car')
                    ))
                    
                    vehicle_id = cursor.lastrowid
                    conn.commit()
                    
                return jsonify({
                    'success': True,
                    'data': {'vehicle_id': vehicle_id}
                })
                
            except sqlite3.IntegrityError:
                return jsonify({'error': 'License plate already registered'}), 409
            except Exception as e:
                self.logger.error(f"Error adding vehicle: {e}")
                return jsonify({'error': 'Failed to add vehicle'}), 500
                
        @self.app.route('/api/v1/notifications', methods=['GET'])
        def get_notifications():
            """Get user notifications"""
            user = self._verify_token()
            if not user:
                return jsonify({'error': 'Authentication required'}), 401
                
            try:
                # This would typically get notifications from a notifications service
                # For now, return simulated notifications
                notifications = [
                    {
                        'id': 1,
                        'type': 'reminder',
                        'title': 'Parking expires soon',
                        'message': 'Your parking session expires in 30 minutes',
                        'timestamp': datetime.now().isoformat(),
                        'read': False
                    },
                    {
                        'id': 2,
                        'type': 'promotion',
                        'title': 'Special offer',
                        'message': 'Get 20% off your next parking session',
                        'timestamp': (datetime.now() - timedelta(hours=2)).isoformat(),
                        'read': True
                    }
                ]
                
                return jsonify({
                    'success': True,
                    'data': notifications
                })
                
            except Exception as e:
                self.logger.error(f"Error getting notifications: {e}")
                return jsonify({'error': 'Failed to get notifications'}), 500
                
        @self.app.route('/api/v1/support/report', methods=['POST'])
        def report_issue():
            """Report an issue or request support"""
            user = self._verify_token()
            if not user:
                return jsonify({'error': 'Authentication required'}), 401
                
            data = request.get_json()
            issue_type = data.get('type')
            description = data.get('description')
            location = data.get('location')
            
            if not issue_type or not description:
                return jsonify({'error': 'Issue type and description required'}), 400
                
            try:
                with sqlite3.connect(self.db_path) as conn:
                    cursor = conn.cursor()
                    cursor.execute("""
                        INSERT INTO support_tickets (user_id, issue_type, description, location, status)
                        VALUES (?, ?, ?, ?, 'open')
                    """, (user['user_id'], issue_type, description, location))
                    
                    ticket_id = cursor.lastrowid
                    conn.commit()
                    
                return jsonify({
                    'success': True,
                    'data': {
                        'ticket_id': ticket_id,
                        'estimated_response_time': '2-4 hours'
                    }
                })
                
            except Exception as e:
                self.logger.error(f"Error creating support ticket: {e}")
                return jsonify({'error': 'Failed to create ticket'}), 500
                
    def _verify_token(self) -> Optional[Dict]:
        """Verify JWT token from request"""
        auth_header = request.headers.get('Authorization', '')
        if not auth_header.startswith('Bearer '):
            return None
            
        token = auth_header.replace('Bearer ', '')
        return self.security.verify_jwt_token(token)
        
    def _find_available_space(self, preferred_level: Optional[int], vehicle_info: Dict) -> Optional[Dict]:
        """Find available parking space"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            # Build query based on preferences
            where_clause = "WHERE is_occupied = 0 AND is_active = 1"
            params = []
            
            if preferred_level:
                where_clause += " AND level = ?"
                params.append(preferred_level)
                
            # Consider vehicle size if provided
            vehicle_type = vehicle_info.get('vehicle_type', 'car')
            if vehicle_type == 'truck':
                where_clause += " AND space_type IN ('large', 'truck')"
            elif vehicle_type == 'motorcycle':
                where_clause += " AND space_type = 'motorcycle'"
                
            cursor.execute(f"""
                SELECT id, level, space_number, space_type
                FROM parking_spaces 
                {where_clause}
                ORDER BY level, space_number
                LIMIT 1
            """, params)
            
            result = cursor.fetchone()
            return dict(result) if result else None
            
    def _create_reservation(self, user_id: int, space_id: int, vehicle_info: Dict, duration_hours: int) -> str:
        """Create parking reservation"""
        reservation_id = f"RES-{datetime.now().strftime('%Y%m%d')}-{secrets.token_hex(4).upper()}"
        expires_at = datetime.now() + timedelta(minutes=15)  # 15 minute reservation window
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO reservations (
                    reservation_id, user_id, space_id, vehicle_info, 
                    duration_hours, expires_at, status
                ) VALUES (?, ?, ?, ?, ?, ?, 'active')
            """, (
                reservation_id, user_id, space_id, 
                json.dumps(vehicle_info), duration_hours, expires_at.isoformat()
            ))
            conn.commit()
            
        return reservation_id
        
    def _generate_qr_code(self, data: str) -> str:
        """Generate QR code as base64 string"""
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(data)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Convert to base64
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)
        
        return base64.b64encode(buffer.getvalue()).decode()
        
    def _calculate_cost(self, duration_hours: int) -> float:
        """Calculate parking cost"""
        # Simple pricing: $2/hour for first 4 hours, $1.50/hour after
        if duration_hours <= 4:
            return duration_hours * 2.0
        else:
            return (4 * 2.0) + ((duration_hours - 4) * 1.5)
            
    def run(self, host='0.0.0.0', port=5001, debug=False):
        """Run the mobile API server"""
        self.app.run(host=host, port=port, debug=debug)


def main():
    """Main function for running mobile API"""
    from src.security.authentication import SecurityManager
    from src.simulation.parking_simulator import ParkingSimulator
    
    db_path = "data/parking_system.db"
    
    # Initialize dependencies
    security = SecurityManager(db_path)
    parking_sim = ParkingSimulator(db_path)
    
    # Create mobile API
    mobile_api = MobileAPI(db_path, security, parking_sim)
    
    print("Starting Mobile API server on port 5001...")
    mobile_api.run(debug=True)

if __name__ == "__main__":
    main()
