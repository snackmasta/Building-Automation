# filepath: c:\Users\Legion\Desktop\PLC\Car_Parking_Vending_System\src\security\authentication.py
"""
Security and Authentication System for Car Parking Vending System
Provides comprehensive security, user management, and access control
"""

import hashlib
import secrets
import jwt
import bcrypt
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import sqlite3
import json
import hmac
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import os
import time
from functools import wraps

class SecurityManager:
    """Comprehensive security and authentication manager"""
    
    def __init__(self, db_path: str, secret_key: str = None):
        self.db_path = db_path
        self.secret_key = secret_key or secrets.token_urlsafe(32)
        self.session_timeout = 3600  # 1 hour
        self.max_login_attempts = 5
        self.lockout_duration = 900  # 15 minutes
        
        # Set up logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        # Initialize encryption
        self._init_encryption()
        
        # Initialize database
        self._init_security_db()
        
    def _init_encryption(self):
        """Initialize encryption system"""
        # Generate key for sensitive data encryption
        key_material = self.secret_key.encode()
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=b'car_parking_salt',  # In production, use a random salt
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(key_material))
        self.cipher_suite = Fernet(key)
        
    def _init_security_db(self):
        """Initialize security database tables"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Users table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    salt TEXT NOT NULL,
                    role TEXT NOT NULL DEFAULT 'user',
                    is_active BOOLEAN DEFAULT 1,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_login TIMESTAMP,
                    failed_login_attempts INTEGER DEFAULT 0,
                    locked_until TIMESTAMP,
                    two_factor_secret TEXT,
                    two_factor_enabled BOOLEAN DEFAULT 0
                )
            """)
            
            # Sessions table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_sessions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    session_token TEXT UNIQUE NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    expires_at TIMESTAMP NOT NULL,
                    ip_address TEXT,
                    user_agent TEXT,
                    is_active BOOLEAN DEFAULT 1,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            """)
            
            # Audit log table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS security_audit_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    action TEXT NOT NULL,
                    resource TEXT,
                    ip_address TEXT,
                    user_agent TEXT,
                    success BOOLEAN NOT NULL,
                    details TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            """)
            
            # Permissions table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS permissions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    role TEXT NOT NULL,
                    resource TEXT NOT NULL,
                    action TEXT NOT NULL,
                    allowed BOOLEAN DEFAULT 1,
                    UNIQUE(role, resource, action)
                )
            """)
            
            # API keys table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS api_keys (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    key_id TEXT UNIQUE NOT NULL,
                    key_hash TEXT NOT NULL,
                    user_id INTEGER,
                    name TEXT NOT NULL,
                    permissions TEXT,
                    is_active BOOLEAN DEFAULT 1,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    expires_at TIMESTAMP,
                    last_used TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            """)
            
            conn.commit()
            
        # Initialize default roles and permissions
        self._init_default_permissions()
        
    def _init_default_permissions(self):
        """Initialize default role-based permissions"""
        default_permissions = [
            # Admin permissions
            ('admin', 'system', 'read', True),
            ('admin', 'system', 'write', True),
            ('admin', 'system', 'delete', True),
            ('admin', 'users', 'read', True),
            ('admin', 'users', 'write', True),
            ('admin', 'users', 'delete', True),
            ('admin', 'reports', 'read', True),
            ('admin', 'reports', 'write', True),
            ('admin', 'parking', 'read', True),
            ('admin', 'parking', 'write', True),
            
            # Operator permissions
            ('operator', 'system', 'read', True),
            ('operator', 'system', 'write', False),
            ('operator', 'parking', 'read', True),
            ('operator', 'parking', 'write', True),
            ('operator', 'reports', 'read', True),
            ('operator', 'users', 'read', False),
            
            # Maintenance permissions
            ('maintenance', 'system', 'read', True),
            ('maintenance', 'system', 'write', True),
            ('maintenance', 'parking', 'read', True),
            ('maintenance', 'reports', 'read', True),
            ('maintenance', 'equipment', 'read', True),
            ('maintenance', 'equipment', 'write', True),
            
            # User permissions
            ('user', 'parking', 'read', True),
            ('user', 'profile', 'read', True),
            ('user', 'profile', 'write', True),
        ]
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            for role, resource, action, allowed in default_permissions:
                cursor.execute("""
                    INSERT OR IGNORE INTO permissions (role, resource, action, allowed)
                    VALUES (?, ?, ?, ?)
                """, (role, resource, action, allowed))
            conn.commit()
            
    def create_user(self, username: str, email: str, password: str, role: str = 'user') -> bool:
        """Create a new user with secure password hashing"""
        try:
            # Generate salt and hash password
            salt = bcrypt.gensalt()
            password_hash = bcrypt.hashpw(password.encode('utf-8'), salt)
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO users (username, email, password_hash, salt, role)
                    VALUES (?, ?, ?, ?, ?)
                """, (username, email, password_hash.decode('utf-8'), salt.decode('utf-8'), role))
                
                user_id = cursor.lastrowid
                conn.commit()
                
            self._log_security_event(user_id, 'user_created', 'users', True, 
                                   f"User {username} created with role {role}")
            return True
            
        except sqlite3.IntegrityError as e:
            self.logger.error(f"Failed to create user {username}: {e}")
            return False
            
    def authenticate_user(self, username: str, password: str, ip_address: str = None, 
                         user_agent: str = None) -> Optional[Dict]:
        """Authenticate user with rate limiting and lockout protection"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            # Get user data
            cursor.execute("""
                SELECT id, username, email, password_hash, role, is_active, 
                       failed_login_attempts, locked_until
                FROM users WHERE username = ?
            """, (username,))
            
            user = cursor.fetchone()
            
            if not user:
                self._log_security_event(None, 'login_failed', 'authentication', False,
                                       f"Login attempt for non-existent user: {username}",
                                       ip_address, user_agent)
                return None
                
            user_dict = dict(user)
            
            # Check if account is locked
            if user_dict['locked_until']:
                locked_until = datetime.fromisoformat(user_dict['locked_until'])
                if datetime.now() < locked_until:
                    self._log_security_event(user_dict['id'], 'login_failed', 'authentication', False,
                                           "Login attempt on locked account", ip_address, user_agent)
                    return None
                else:
                    # Unlock account
                    cursor.execute("""
                        UPDATE users SET locked_until = NULL, failed_login_attempts = 0
                        WHERE id = ?
                    """, (user_dict['id'],))
                    
            # Check if account is active
            if not user_dict['is_active']:
                self._log_security_event(user_dict['id'], 'login_failed', 'authentication', False,
                                       "Login attempt on inactive account", ip_address, user_agent)
                return None
                
            # Verify password
            if bcrypt.checkpw(password.encode('utf-8'), user_dict['password_hash'].encode('utf-8')):
                # Successful login
                cursor.execute("""
                    UPDATE users SET last_login = CURRENT_TIMESTAMP, failed_login_attempts = 0
                    WHERE id = ?
                """, (user_dict['id'],))
                
                # Create session
                session_token = self._create_session(user_dict['id'], ip_address, user_agent)
                
                self._log_security_event(user_dict['id'], 'login_success', 'authentication', True,
                                       "Successful login", ip_address, user_agent)
                
                return {
                    'user_id': user_dict['id'],
                    'username': user_dict['username'],
                    'email': user_dict['email'],
                    'role': user_dict['role'],
                    'session_token': session_token
                }
            else:
                # Failed login
                failed_attempts = user_dict['failed_login_attempts'] + 1
                
                if failed_attempts >= self.max_login_attempts:
                    # Lock account
                    locked_until = datetime.now() + timedelta(seconds=self.lockout_duration)
                    cursor.execute("""
                        UPDATE users SET failed_login_attempts = ?, locked_until = ?
                        WHERE id = ?
                    """, (failed_attempts, locked_until.isoformat(), user_dict['id']))
                    
                    self._log_security_event(user_dict['id'], 'account_locked', 'authentication', False,
                                           f"Account locked after {failed_attempts} failed attempts",
                                           ip_address, user_agent)
                else:
                    cursor.execute("""
                        UPDATE users SET failed_login_attempts = ?
                        WHERE id = ?
                    """, (failed_attempts, user_dict['id']))
                    
                self._log_security_event(user_dict['id'], 'login_failed', 'authentication', False,
                                       f"Invalid password (attempt {failed_attempts})",
                                       ip_address, user_agent)
                
                conn.commit()
                return None
                
    def validate_session(self, session_token: str) -> Optional[Dict]:
        """Validate user session token"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT s.user_id, s.expires_at, u.username, u.email, u.role, u.is_active
                FROM user_sessions s
                JOIN users u ON s.user_id = u.id
                WHERE s.session_token = ? AND s.is_active = 1
            """, (session_token,))
            
            session = cursor.fetchone()
            
            if not session:
                return None
                
            session_dict = dict(session)
            
            # Check if session has expired
            expires_at = datetime.fromisoformat(session_dict['expires_at'])
            if datetime.now() > expires_at:
                self._invalidate_session(session_token)
                return None
                
            # Check if user is still active
            if not session_dict['is_active']:
                self._invalidate_session(session_token)
                return None
                
            return {
                'user_id': session_dict['user_id'],
                'username': session_dict['username'],
                'email': session_dict['email'],
                'role': session_dict['role']
            }
            
    def check_permission(self, user_role: str, resource: str, action: str) -> bool:
        """Check if user role has permission for resource/action"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT allowed FROM permissions
                WHERE role = ? AND resource = ? AND action = ?
            """, (user_role, resource, action))
            
            result = cursor.fetchone()
            return result[0] if result else False
            
    def _create_session(self, user_id: int, ip_address: str = None, user_agent: str = None) -> str:
        """Create new user session"""
        session_token = secrets.token_urlsafe(32)
        expires_at = datetime.now() + timedelta(seconds=self.session_timeout)
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO user_sessions (user_id, session_token, expires_at, ip_address, user_agent)
                VALUES (?, ?, ?, ?, ?)
            """, (user_id, session_token, expires_at.isoformat(), ip_address, user_agent))
            conn.commit()
            
        return session_token
        
    def _invalidate_session(self, session_token: str):
        """Invalidate user session"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE user_sessions SET is_active = 0 WHERE session_token = ?
            """, (session_token,))
            conn.commit()
            
    def logout_user(self, session_token: str) -> bool:
        """Logout user and invalidate session"""
        session = self.validate_session(session_token)
        if session:
            self._invalidate_session(session_token)
            self._log_security_event(session['user_id'], 'logout', 'authentication', True,
                                   "User logged out")
            return True
        return False
        
    def _log_security_event(self, user_id: Optional[int], action: str, resource: str, 
                           success: bool, details: str = None, ip_address: str = None, 
                           user_agent: str = None):
        """Log security events for audit trail"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO security_audit_log 
                (user_id, action, resource, ip_address, user_agent, success, details)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (user_id, action, resource, ip_address, user_agent, success, details))
            conn.commit()
            
    def create_api_key(self, user_id: int, name: str, permissions: List[str] = None, 
                      expires_days: int = 365) -> Dict:
        """Create API key for programmatic access"""
        key_id = secrets.token_urlsafe(16)
        api_key = secrets.token_urlsafe(32)
        key_hash = hashlib.sha256(api_key.encode()).hexdigest()
        
        expires_at = datetime.now() + timedelta(days=expires_days)
        permissions_json = json.dumps(permissions) if permissions else None
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO api_keys (key_id, key_hash, user_id, name, permissions, expires_at)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (key_id, key_hash, user_id, name, permissions_json, expires_at.isoformat()))
            conn.commit()
            
        self._log_security_event(user_id, 'api_key_created', 'api_keys', True,
                               f"API key '{name}' created")
        
        return {
            'key_id': key_id,
            'api_key': api_key,
            'expires_at': expires_at.isoformat()
        }
        
    def validate_api_key(self, key_id: str, api_key: str) -> Optional[Dict]:
        """Validate API key"""
        key_hash = hashlib.sha256(api_key.encode()).hexdigest()
        
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT ak.user_id, ak.name, ak.permissions, ak.expires_at, u.username, u.role
                FROM api_keys ak
                JOIN users u ON ak.user_id = u.id
                WHERE ak.key_id = ? AND ak.key_hash = ? AND ak.is_active = 1
            """, (key_id, key_hash))
            
            result = cursor.fetchone()
            
            if not result:
                return None
                
            result_dict = dict(result)
            
            # Check expiration
            if result_dict['expires_at']:
                expires_at = datetime.fromisoformat(result_dict['expires_at'])
                if datetime.now() > expires_at:
                    return None
                    
            # Update last used timestamp
            cursor.execute("""
                UPDATE api_keys SET last_used = CURRENT_TIMESTAMP
                WHERE key_id = ?
            """, (key_id,))
            conn.commit()
            
            return {
                'user_id': result_dict['user_id'],
                'username': result_dict['username'],
                'role': result_dict['role'],
                'permissions': json.loads(result_dict['permissions']) if result_dict['permissions'] else []
            }
            
    def encrypt_sensitive_data(self, data: str) -> str:
        """Encrypt sensitive data"""
        return self.cipher_suite.encrypt(data.encode()).decode()
        
    def decrypt_sensitive_data(self, encrypted_data: str) -> str:
        """Decrypt sensitive data"""
        return self.cipher_suite.decrypt(encrypted_data.encode()).decode()
        
    def generate_jwt_token(self, user_data: Dict, expires_hours: int = 24) -> str:
        """Generate JWT token"""
        payload = {
            'user_id': user_data['user_id'],
            'username': user_data['username'],
            'role': user_data['role'],
            'exp': datetime.utcnow() + timedelta(hours=expires_hours),
            'iat': datetime.utcnow()
        }
        return jwt.encode(payload, self.secret_key, algorithm='HS256')
        
    def verify_jwt_token(self, token: str) -> Optional[Dict]:
        """Verify JWT token"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=['HS256'])
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None


def require_auth(security_manager: SecurityManager):
    """Decorator for requiring authentication"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Get session token from request (implementation depends on framework)
            session_token = kwargs.get('session_token')
            if not session_token:
                raise PermissionError("Authentication required")
                
            user = security_manager.validate_session(session_token)
            if not user:
                raise PermissionError("Invalid or expired session")
                
            kwargs['current_user'] = user
            return func(*args, **kwargs)
        return wrapper
    return decorator


def require_permission(security_manager: SecurityManager, resource: str, action: str):
    """Decorator for requiring specific permissions"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            current_user = kwargs.get('current_user')
            if not current_user:
                raise PermissionError("Authentication required")
                
            if not security_manager.check_permission(current_user['role'], resource, action):
                raise PermissionError(f"Permission denied for {action} on {resource}")
                
            return func(*args, **kwargs)
        return wrapper
    return decorator


def main():
    """Main function for testing security system"""
    db_path = "data/parking_system.db"
    
    # Create security manager
    security = SecurityManager(db_path)
    
    # Create test admin user
    if security.create_user("admin", "admin@parking.com", "admin123", "admin"):
        print("Admin user created successfully")
        
    # Test authentication
    auth_result = security.authenticate_user("admin", "admin123", "127.0.0.1", "Test Client")
    if auth_result:
        print(f"Authentication successful: {auth_result['username']}")
        print(f"Session token: {auth_result['session_token']}")
        
        # Test session validation
        user = security.validate_session(auth_result['session_token'])
        if user:
            print(f"Session valid for user: {user['username']}")
            
        # Test permissions
        has_permission = security.check_permission(user['role'], 'system', 'write')
        print(f"Admin has system write permission: {has_permission}")
        
        # Create API key
        api_key_data = security.create_api_key(user['user_id'], "Test API Key")
        print(f"API key created: {api_key_data['key_id']}")
        
    else:
        print("Authentication failed")

if __name__ == "__main__":
    main()
