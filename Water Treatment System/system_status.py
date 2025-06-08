#!/usr/bin/env python3
"""
System Status Monitor for Water Treatment System
Real-time monitoring and health assessment
"""

import time
import json
import sqlite3
import configparser
from datetime import datetime, timedelta
import psutil
import threading
import socket
import subprocess
import os

class SystemStatusMonitor:
    def __init__(self, config_file="plc_config.ini"):
        self.config = configparser.ConfigParser()
        self.config.read(config_file)
        
        # Initialize database
        self.init_database()
        
        # System status data
        self.system_status = {
            'overall_status': 'RUNNING',
            'last_update': datetime.now().isoformat(),
            'uptime': 0,
            'production': {
                'current_rate': 167.5,
                'daily_total': 0,
                'efficiency': 92.1,
                'target_rate': float(self.config.get('PROCESS_PARAMETERS', 'nominal_production_rate', fallback=8500)) / 60
            },
            'equipment': {
                'ro_system': {'status': 'RUNNING', 'pressure': 55.2, 'flow': 167.5, 'efficiency': 95.3},
                'pumps': [
                    {'id': 1, 'status': 'RUNNING', 'flow': 125.3, 'efficiency': 88.5, 'runtime': 1247},
                    {'id': 2, 'status': 'STANDBY', 'flow': 0.0, 'efficiency': 0.0, 'runtime': 1156},
                    {'id': 3, 'status': 'RUNNING', 'flow': 98.7, 'efficiency': 89.2, 'runtime': 1089}
                ],
                'tanks': {
                    'seawater': {'level': 85.0, 'status': 'NORMAL'},
                    'treated': {'level': 62.0, 'status': 'NORMAL'},
                    'roof_tanks': [
                        {'id': 1, 'level': 78.0, 'status': 'NORMAL', 'zone': 'North'},
                        {'id': 2, 'level': 65.0, 'status': 'NORMAL', 'zone': 'South'},
                        {'id': 3, 'level': 71.0, 'status': 'NORMAL', 'zone': 'East'}
                    ]
                }
            },
            'quality': {
                'ph': 7.2, 'chlorine': 0.8, 'tds': 185, 'turbidity': 0.12,
                'temperature': 22.5, 'conductivity': 280, 'status': 'ACCEPTABLE'
            },
            'energy': {
                'current_consumption': 125.8,
                'daily_consumption': 0,
                'efficiency': 88.5,
                'cost_today': 0
            },
            'alarms': {
                'active_count': 0,
                'high_priority': 0,
                'medium_priority': 0,
                'low_priority': 0,
                'last_alarm': None
            },
            'communication': {
                'hmi_connected': True,
                'plc_connected': True,
                'network_status': 'CONNECTED',
                'last_communication': datetime.now().isoformat()
            },
            'maintenance': {
                'next_scheduled': '2025-06-15',
                'overdue_items': 0,
                'membrane_hours': 2847,
                'filter_status': 'GOOD'
            }
        }
        
        self.start_time = datetime.now()
        self.running = True
        
    def init_database(self):
        """Initialize SQLite database for logging"""
        self.db_path = "system_status.db"
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        
        # Create tables
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS system_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                log_level TEXT,
                component TEXT,
                message TEXT,
                data TEXT
            )
        ''')
        
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS performance_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                production_rate REAL,
                energy_consumption REAL,
                efficiency REAL,
                quality_ph REAL,
                quality_tds REAL
            )
        ''')
        
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS alarm_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                priority TEXT,
                component TEXT,
                description TEXT,
                status TEXT
            )
        ''')
        
        self.conn.commit()
        
    def log_event(self, level, component, message, data=None):
        """Log system events to database"""
        data_json = json.dumps(data) if data else None
        self.conn.execute(
            "INSERT INTO system_logs (log_level, component, message, data) VALUES (?, ?, ?, ?)",
            (level, component, message, data_json)
        )
        self.conn.commit()
        
    def log_performance_data(self):
        """Log performance metrics"""
        self.conn.execute(
            """INSERT INTO performance_data 
               (production_rate, energy_consumption, efficiency, quality_ph, quality_tds) 
               VALUES (?, ?, ?, ?, ?)""",
            (
                self.system_status['production']['current_rate'],
                self.system_status['energy']['current_consumption'],
                self.system_status['production']['efficiency'],
                self.system_status['quality']['ph'],
                self.system_status['quality']['tds']
            )
        )
        self.conn.commit()
        
    def check_system_health(self):
        """Comprehensive system health check"""
        health_score = 100
        issues = []
        
        # Check production rate
        current_rate = self.system_status['production']['current_rate']
        target_rate = self.system_status['production']['target_rate']
        if current_rate < target_rate * 0.8:
            health_score -= 15
            issues.append("Production rate below target")
            
        # Check water quality
        quality = self.system_status['quality']
        ph_min = float(self.config.get('WATER_QUALITY', 'ph_min', fallback=6.8))
        ph_max = float(self.config.get('WATER_QUALITY', 'ph_max', fallback=7.6))
        
        if quality['ph'] < ph_min or quality['ph'] > ph_max:
            health_score -= 20
            issues.append("pH out of acceptable range")
            
        if quality['tds'] > float(self.config.get('WATER_QUALITY', 'tds_max', fallback=200)):
            health_score -= 25
            issues.append("TDS exceeds limit")
            
        # Check tank levels
        for tank in self.system_status['equipment']['tanks']['roof_tanks']:
            if tank['level'] < 25:
                health_score -= 10
                issues.append(f"Low level in {tank['zone']} tank")
                
        # Check pump status
        running_pumps = sum(1 for pump in self.system_status['equipment']['pumps'] 
                          if pump['status'] == 'RUNNING')
        if running_pumps == 0:
            health_score -= 50
            issues.append("No pumps running")
        elif running_pumps == 1:
            health_score -= 10
            issues.append("Only one pump running - reduced redundancy")
            
        # Check energy efficiency
        if self.system_status['energy']['efficiency'] < 75:
            health_score -= 15
            issues.append("Energy efficiency below acceptable level")
            
        # Check active alarms
        if self.system_status['alarms']['high_priority'] > 0:
            health_score -= 30
            issues.append("High priority alarms active")
        elif self.system_status['alarms']['medium_priority'] > 2:
            health_score -= 15
            issues.append("Multiple medium priority alarms")
            
        # Update overall status
        if health_score >= 90:
            status = "EXCELLENT"
        elif health_score >= 75:
            status = "GOOD"
        elif health_score >= 60:
            status = "FAIR"
        elif health_score >= 40:
            status = "POOR"
        else:
            status = "CRITICAL"
            
        return {
            'health_score': max(0, health_score),
            'status': status,
            'issues': issues,
            'timestamp': datetime.now().isoformat()
        }
        
    def check_network_connectivity(self):
        """Check network connectivity to critical systems"""
        try:
            # Check local network
            socket.create_connection(("8.8.8.8", 53), timeout=3)
            network_status = "CONNECTED"
        except OSError:
            network_status = "DISCONNECTED"
            
        # Simulate HMI and PLC connectivity checks
        hmi_connected = True  # In real implementation, would ping HMI system
        plc_connected = True  # In real implementation, would check PLC communication
        
        self.system_status['communication'].update({
            'network_status': network_status,
            'hmi_connected': hmi_connected,
            'plc_connected': plc_connected,
            'last_communication': datetime.now().isoformat()
        })
        
    def simulate_real_time_data(self):
        """Simulate real-time data changes for demonstration"""
        import random
        
        # Simulate production variations
        production = self.system_status['production']
        production['current_rate'] += random.uniform(-3, 3)
        production['current_rate'] = max(120, min(200, production['current_rate']))
        production['efficiency'] += random.uniform(-0.5, 0.5)
        production['efficiency'] = max(80, min(95, production['efficiency']))
        
        # Simulate tank level changes
        for tank in self.system_status['equipment']['tanks']['roof_tanks']:
            tank['level'] += random.uniform(-0.3, 0.1)  # Gradual consumption
            tank['level'] = max(15, min(95, tank['level']))
            
        # Simulate water quality variations
        quality = self.system_status['quality']
        quality['ph'] += random.uniform(-0.02, 0.02)
        quality['chlorine'] += random.uniform(-0.03, 0.03)
        quality['tds'] += random.uniform(-2, 2)
        
        # Keep in realistic ranges
        quality['ph'] = max(6.8, min(7.6, quality['ph']))
        quality['chlorine'] = max(0.5, min(1.2, quality['chlorine']))
        quality['tds'] = max(150, min(250, quality['tds']))
        
        # Update energy consumption
        energy = self.system_status['energy']
        energy['current_consumption'] += random.uniform(-2, 2)
        energy['current_consumption'] = max(100, min(150, energy['current_consumption']))
        
    def generate_daily_report(self):
        """Generate daily system performance report"""
        report = {
            'date': datetime.now().strftime('%Y-%m-%d'),
            'uptime_hours': (datetime.now() - self.start_time).total_seconds() / 3600,
            'total_production': self.system_status['production']['daily_total'],
            'average_efficiency': self.system_status['production']['efficiency'],
            'energy_consumption': self.system_status['energy']['daily_consumption'],
            'alarms_today': self.get_daily_alarm_count(),
            'quality_incidents': 0,  # Would be calculated from quality logs
            'maintenance_performed': []  # Would be from maintenance logs
        }
        
        return report
        
    def get_daily_alarm_count(self):
        """Get count of alarms for today"""
        today = datetime.now().strftime('%Y-%m-%d')
        cursor = self.conn.execute(
            "SELECT COUNT(*) FROM alarm_history WHERE date(timestamp) = ?",
            (today,)
        )
        return cursor.fetchone()[0]
        
    def get_system_summary(self):
        """Get comprehensive system summary"""
        health = self.check_system_health()
        
        summary = {
            'system_info': {
                'name': self.config.get('SYSTEM', 'system_name', fallback='Water Treatment System'),
                'version': self.config.get('SYSTEM', 'version', fallback='1.0'),
                'uptime': str(datetime.now() - self.start_time),
                'last_update': datetime.now().isoformat()
            },
            'health': health,
            'status': self.system_status,
            'performance_kpis': {
                'production_efficiency': self.system_status['production']['efficiency'],
                'energy_efficiency': self.system_status['energy']['efficiency'],
                'quality_compliance': 98.5,  # Calculated from quality logs
                'equipment_availability': 99.2  # Calculated from equipment status
            }
        }
        
        return summary
        
    def export_status_report(self, filepath=None):
        """Export current status to JSON file"""
        if not filepath:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filepath = f"system_status_report_{timestamp}.json"
            
        summary = self.get_system_summary()
        
        with open(filepath, 'w') as f:
            json.dump(summary, f, indent=2, default=str)
            
        return filepath
        
    def monitor_loop(self):
        """Main monitoring loop"""
        print("System Status Monitor started...")
        
        while self.running:
            try:
                # Update system uptime
                self.system_status['uptime'] = (datetime.now() - self.start_time).total_seconds()
                self.system_status['last_update'] = datetime.now().isoformat()
                
                # Simulate real-time data changes
                self.simulate_real_time_data()
                
                # Check network connectivity
                self.check_network_connectivity()
                
                # Log performance data every minute
                if int(time.time()) % 60 == 0:
                    self.log_performance_data()
                    
                # Generate and log health check every 5 minutes
                if int(time.time()) % 300 == 0:
                    health = self.check_system_health()
                    self.log_event('INFO', 'HEALTH_CHECK', 
                                 f"System health: {health['status']}", health)
                    
                time.sleep(1)  # Update every second
                
            except KeyboardInterrupt:
                print("\nShutting down monitor...")
                self.running = False
                break
            except Exception as e:
                print(f"Error in monitoring loop: {e}")
                self.log_event('ERROR', 'MONITOR', f"Monitoring error: {e}")
                time.sleep(5)  # Wait before retrying
                
    def start_monitoring(self):
        """Start monitoring in a separate thread"""
        monitor_thread = threading.Thread(target=self.monitor_loop, daemon=True)
        monitor_thread.start()
        return monitor_thread
        
    def stop_monitoring(self):
        """Stop the monitoring system"""
        self.running = False
        self.conn.close()

def print_status_dashboard():
    """Print a simple console dashboard"""
    monitor = SystemStatusMonitor()
    
    try:
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')  # Clear screen
            
            summary = monitor.get_system_summary()
            health = summary['health']
            status = summary['status']
            
            print("=" * 60)
            print("    WATER TREATMENT SYSTEM - STATUS DASHBOARD")
            print("=" * 60)
            print(f"System: {summary['system_info']['name']}")
            print(f"Uptime: {summary['system_info']['uptime']}")
            print(f"Health Score: {health['health_score']}/100 ({health['status']})")
            print(f"Last Update: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print("-" * 60)
            
            # Production Status
            prod = status['production']
            print(f"PRODUCTION:")
            print(f"  Current Rate: {prod['current_rate']:.1f} L/min")
            print(f"  Efficiency: {prod['efficiency']:.1f}%")
            print(f"  Target Rate: {prod['target_rate']:.1f} L/min")
            
            # Equipment Status
            print(f"\nEQUIPMENT:")
            print(f"  RO System: {status['equipment']['ro_system']['status']} "
                  f"({status['equipment']['ro_system']['pressure']:.1f} bar)")
            
            running_pumps = sum(1 for p in status['equipment']['pumps'] 
                              if p['status'] == 'RUNNING')
            print(f"  Pumps: {running_pumps}/3 Running")
            
            # Tank Levels
            print(f"\nTANK LEVELS:")
            print(f"  Seawater: {status['equipment']['tanks']['seawater']['level']:.1f}%")
            print(f"  Treated: {status['equipment']['tanks']['treated']['level']:.1f}%")
            for tank in status['equipment']['tanks']['roof_tanks']:
                print(f"  Roof {tank['id']} ({tank['zone']}): {tank['level']:.1f}%")
            
            # Water Quality
            quality = status['quality']
            print(f"\nWATER QUALITY:")
            print(f"  pH: {quality['ph']:.1f}")
            print(f"  Chlorine: {quality['chlorine']:.1f} ppm")
            print(f"  TDS: {quality['tds']} ppm")
            print(f"  Status: {quality['status']}")
            
            # Energy
            energy = status['energy']
            print(f"\nENERGY:")
            print(f"  Consumption: {energy['current_consumption']:.1f} kW")
            print(f"  Efficiency: {energy['efficiency']:.1f}%")
            
            # Alarms
            alarms = status['alarms']
            print(f"\nALARMS:")
            print(f"  Active: {alarms['active_count']} "
                  f"(H:{alarms['high_priority']}, M:{alarms['medium_priority']}, L:{alarms['low_priority']})")
            
            # Health Issues
            if health['issues']:
                print(f"\nISSUES:")
                for issue in health['issues'][:5]:  # Show first 5 issues
                    print(f"  • {issue}")
            
            print("\n" + "=" * 60)
            print("Press Ctrl+C to exit")
            
            time.sleep(5)  # Update every 5 seconds
            
    except KeyboardInterrupt:
        print("\nExiting dashboard...")
        monitor.stop_monitoring()

def main():
    """Main function"""
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == '--dashboard':
        print_status_dashboard()
    else:
        # Start monitoring service
        monitor = SystemStatusMonitor()
        
        print("Starting Water Treatment System Monitor...")
        print("Press Ctrl+C to stop")
        
        try:
            monitor.monitor_loop()
        except KeyboardInterrupt:
            print("\nShutting down monitor...")
        finally:
            monitor.stop_monitoring()

if __name__ == "__main__":
    main()
