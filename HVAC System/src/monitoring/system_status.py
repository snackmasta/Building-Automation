#!/usr/bin/env python3
"""
HVAC Control System - System Status Monitor
============================================

This module provides comprehensive system monitoring and status reporting
for the HVAC control system. It monitors PLC connectivity, system health,
performance metrics, and generates status reports.

Author: HVAC Control System Team
Version: 1.0
Date: 2024
"""

import os
import sys
import time
import json
import logging
import psutil
import socket
import subprocess
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
import configparser

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

@dataclass
class SystemStatus:
    """Data class for system status information"""
    timestamp: str
    plc_connected: bool
    hmi_running: bool
    simulator_running: bool
    monitor_running: bool
    cpu_usage: float
    memory_usage: float
    disk_usage: float
    network_status: bool
    active_alarms: int
    system_uptime: str
    last_backup: str
    system_mode: str
    energy_efficiency: float
    zone_count_active: int
    temperature_range: Dict[str, float]
    air_quality_status: str
    maintenance_due: List[str]

class HVACSystemMonitor:
    """HVAC System Status Monitor"""
    
    def __init__(self, config_file: str = None):
        """Initialize the system monitor"""
        self.config_file = config_file or os.path.join(project_root, 'config', 'plc_config.ini')
        self.config = self._load_config()
        self.logger = self._setup_logging()
        self.processes = {}
        self.last_check = None
        self.status_history = []
        
        # System thresholds
        self.cpu_threshold = 80.0
        self.memory_threshold = 85.0
        self.disk_threshold = 90.0
        
        self.logger.info("HVAC System Monitor initialized")
    
    def _load_config(self) -> configparser.ConfigParser:
        """Load system configuration"""
        config = configparser.ConfigParser()
        if os.path.exists(self.config_file):
            config.read(self.config_file)
        else:
            # Create default config
            config['PLC'] = {
                'host': '192.168.1.100',
                'port': '502',
                'timeout': '5'
            }
            config['SYSTEM'] = {
                'zone_count': '8',
                'update_interval': '5',
                'log_level': 'INFO'
            }
            config['MONITORING'] = {
                'cpu_threshold': '80',
                'memory_threshold': '85',
                'disk_threshold': '90'
            }
        return config
    
    def _setup_logging(self) -> logging.Logger:
        """Setup logging configuration"""
        logger = logging.getLogger('HVACMonitor')
        logger.setLevel(logging.INFO)
        
        # Create logs directory if it doesn't exist
        log_dir = os.path.join(project_root, 'logs')
        os.makedirs(log_dir, exist_ok=True)
        
        # File handler
        log_file = os.path.join(log_dir, f'system_monitor_{datetime.now().strftime("%Y%m%d")}.log')
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.INFO)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # Formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        
        return logger
    
    def check_plc_connectivity(self) -> bool:
        """Check PLC connectivity"""
        try:
            host = self.config.get('PLC', 'host', fallback='192.168.1.100')
            port = int(self.config.get('PLC', 'port', fallback='502'))
            timeout = int(self.config.get('PLC', 'timeout', fallback='5'))
            
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            result = sock.connect_ex((host, port))
            sock.close()
            
            is_connected = result == 0
            if is_connected:
                self.logger.debug(f"PLC connectivity OK: {host}:{port}")
            else:
                self.logger.warning(f"PLC connectivity failed: {host}:{port}")
            
            return is_connected
            
        except Exception as e:
            self.logger.error(f"Error checking PLC connectivity: {e}")
            return False
    
    def check_process_status(self) -> Dict[str, bool]:
        """Check status of HVAC system processes"""
        processes = {
            'hmi_running': False,
            'simulator_running': False,
            'monitor_running': False
        }
        
        try:
            for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                try:
                    pinfo = proc.info
                    cmdline = ' '.join(pinfo['cmdline']) if pinfo['cmdline'] else ''
                    
                    if 'hmi_interface.py' in cmdline:
                        processes['hmi_running'] = True
                        self.processes['hmi'] = pinfo['pid']
                    elif 'plc_simulator.py' in cmdline:
                        processes['simulator_running'] = True
                        self.processes['simulator'] = pinfo['pid']
                    elif 'system_monitor.py' in cmdline:
                        processes['monitor_running'] = True
                        self.processes['monitor'] = pinfo['pid']
                        
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
                    
        except Exception as e:
            self.logger.error(f"Error checking process status: {e}")
        
        return processes
    
    def get_system_resources(self) -> Dict[str, float]:
        """Get system resource usage"""
        try:
            cpu_usage = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            return {
                'cpu_usage': cpu_usage,
                'memory_usage': memory.percent,
                'disk_usage': disk.percent
            }
        except Exception as e:
            self.logger.error(f"Error getting system resources: {e}")
            return {
                'cpu_usage': 0.0,
                'memory_usage': 0.0,
                'disk_usage': 0.0
            }
    
    def check_network_status(self) -> bool:
        """Check network connectivity"""
        try:
            # Try to connect to a reliable host
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            result = sock.connect_ex(('8.8.8.8', 53))
            sock.close()
            return result == 0
        except Exception:
            return False
    
    def get_system_uptime(self) -> str:
        """Get system uptime"""
        try:
            uptime_seconds = time.time() - psutil.boot_time()
            uptime_delta = timedelta(seconds=uptime_seconds)
            
            days = uptime_delta.days
            hours, remainder = divmod(uptime_delta.seconds, 3600)
            minutes, _ = divmod(remainder, 60)
            
            return f"{days}d {hours}h {minutes}m"
        except Exception as e:
            self.logger.error(f"Error getting system uptime: {e}")
            return "Unknown"
    
    def check_maintenance_status(self) -> List[str]:
        """Check for maintenance tasks due"""
        maintenance_due = []
        
        try:
            # Check for maintenance schedule file
            maintenance_file = os.path.join(project_root, 'data', 'maintenance_schedule.json')
            if os.path.exists(maintenance_file):
                with open(maintenance_file, 'r') as f:
                    schedule = json.load(f)
                
                current_date = datetime.now()
                for task in schedule.get('tasks', []):
                    due_date = datetime.strptime(task['due_date'], '%Y-%m-%d')
                    if due_date <= current_date:
                        maintenance_due.append(task['name'])
            else:
                # Default maintenance items
                maintenance_due = ['Filter replacement check', 'System calibration review']
                
        except Exception as e:
            self.logger.error(f"Error checking maintenance status: {e}")
            maintenance_due = ['Maintenance status check failed']
        
        return maintenance_due
    
    def simulate_zone_data(self) -> Dict[str, Any]:
        """Simulate zone data for demonstration"""
        import random
        
        zone_count = int(self.config.get('SYSTEM', 'zone_count', fallback='8'))
        active_zones = random.randint(5, zone_count)
        
        temps = [18 + random.uniform(0, 8) for _ in range(zone_count)]
        
        return {
            'zone_count_active': active_zones,
            'temperature_range': {
                'min': min(temps),
                'max': max(temps),
                'avg': sum(temps) / len(temps)
            }
        }
    
    def simulate_air_quality(self) -> str:
        """Simulate air quality status"""
        import random
        statuses = ['Excellent', 'Good', 'Fair', 'Poor']
        weights = [0.4, 0.3, 0.2, 0.1]
        return random.choices(statuses, weights=weights)[0]
    
    def get_comprehensive_status(self) -> SystemStatus:
        """Get comprehensive system status"""
        self.logger.info("Collecting comprehensive system status...")
        
        # Get basic system info
        process_status = self.check_process_status()
        resources = self.get_system_resources()
        zone_data = self.simulate_zone_data()
        
        # Create status object
        status = SystemStatus(
            timestamp=datetime.now().isoformat(),
            plc_connected=self.check_plc_connectivity(),
            hmi_running=process_status['hmi_running'],
            simulator_running=process_status['simulator_running'],
            monitor_running=process_status['monitor_running'],
            cpu_usage=resources['cpu_usage'],
            memory_usage=resources['memory_usage'],
            disk_usage=resources['disk_usage'],
            network_status=self.check_network_status(),
            active_alarms=0,  # Would be populated from alarm system
            system_uptime=self.get_system_uptime(),
            last_backup="2024-01-15 02:00:00",  # Would be read from backup log
            system_mode="AUTO",
            energy_efficiency=85.5,  # Would be calculated from energy data
            zone_count_active=zone_data['zone_count_active'],
            temperature_range=zone_data['temperature_range'],
            air_quality_status=self.simulate_air_quality(),
            maintenance_due=self.check_maintenance_status()
        )
        
        self.last_check = datetime.now()
        self.status_history.append(status)
        
        # Keep only last 100 status records
        if len(self.status_history) > 100:
            self.status_history.pop(0)
        
        return status
    
    def check_system_health(self, status: SystemStatus) -> List[str]:
        """Check system health and return warnings/errors"""
        issues = []
        
        # Check PLC connectivity
        if not status.plc_connected:
            issues.append("❌ CRITICAL: PLC not connected")
        
        # Check essential processes
        if not status.hmi_running:
            issues.append("⚠️  WARNING: HMI interface not running")
        
        if not status.simulator_running:
            issues.append("ℹ️  INFO: PLC simulator not running")
        
        # Check resource usage
        if status.cpu_usage > self.cpu_threshold:
            issues.append(f"⚠️  WARNING: High CPU usage ({status.cpu_usage:.1f}%)")
        
        if status.memory_usage > self.memory_threshold:
            issues.append(f"⚠️  WARNING: High memory usage ({status.memory_usage:.1f}%)")
        
        if status.disk_usage > self.disk_threshold:
            issues.append(f"❌ CRITICAL: Low disk space ({status.disk_usage:.1f}% used)")
        
        # Check network
        if not status.network_status:
            issues.append("⚠️  WARNING: Network connectivity issues")
        
        # Check maintenance
        if status.maintenance_due:
            issues.append(f"ℹ️  INFO: Maintenance due: {', '.join(status.maintenance_due)}")
        
        return issues
    
    def print_status_report(self, status: SystemStatus):
        """Print formatted status report"""
        print("\n" + "="*80)
        print("                HVAC CONTROL SYSTEM - STATUS REPORT")
        print("="*80)
        print(f"📅 Timestamp: {status.timestamp}")
        print(f"⏱️  System Uptime: {status.system_uptime}")
        print(f"🔧 System Mode: {status.system_mode}")
        print()
        
        # Connection Status
        print("🔗 CONNECTION STATUS:")
        print(f"   PLC Connected: {'✅ YES' if status.plc_connected else '❌ NO'}")
        print(f"   Network Status: {'✅ ONLINE' if status.network_status else '❌ OFFLINE'}")
        print()
        
        # Process Status
        print("⚙️  PROCESS STATUS:")
        print(f"   HMI Interface: {'✅ RUNNING' if status.hmi_running else '❌ STOPPED'}")
        print(f"   PLC Simulator: {'✅ RUNNING' if status.simulator_running else '❌ STOPPED'}")
        print(f"   System Monitor: {'✅ RUNNING' if status.monitor_running else '❌ STOPPED'}")
        print()
        
        # System Resources
        print("💻 SYSTEM RESOURCES:")
        print(f"   CPU Usage: {status.cpu_usage:.1f}%")
        print(f"   Memory Usage: {status.memory_usage:.1f}%")
        print(f"   Disk Usage: {status.disk_usage:.1f}%")
        print()
        
        # HVAC Status
        print("🌡️  HVAC SYSTEM:")
        print(f"   Active Zones: {status.zone_count_active}/8")
        print(f"   Temperature Range: {status.temperature_range['min']:.1f}°C - {status.temperature_range['max']:.1f}°C")
        print(f"   Average Temperature: {status.temperature_range['avg']:.1f}°C")
        print(f"   Air Quality: {status.air_quality_status}")
        print(f"   Energy Efficiency: {status.energy_efficiency:.1f}%")
        print()
        
        # Alarms and Maintenance
        print("🚨 ALARMS & MAINTENANCE:")
        print(f"   Active Alarms: {status.active_alarms}")
        print(f"   Maintenance Due: {len(status.maintenance_due)} items")
        if status.maintenance_due:
            for item in status.maintenance_due:
                print(f"      - {item}")
        print()
        
        # Health Check
        issues = self.check_system_health(status)
        print("🏥 SYSTEM HEALTH:")
        if not issues:
            print("   ✅ All systems operating normally")
        else:
            for issue in issues:
                print(f"   {issue}")
        
        print("="*80)
    
    def save_status_json(self, status: SystemStatus, filename: str = None):
        """Save status to JSON file"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = os.path.join(project_root, 'data', f'system_status_{timestamp}.json')
        
        # Create data directory if it doesn't exist
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        try:
            with open(filename, 'w') as f:
                json.dump(asdict(status), f, indent=2)
            self.logger.info(f"Status saved to {filename}")
        except Exception as e:
            self.logger.error(f"Error saving status to JSON: {e}")
    
    def run_continuous_monitoring(self, interval: int = 60):
        """Run continuous monitoring with specified interval"""
        print(f"Starting continuous monitoring (interval: {interval}s)")
        print("Press Ctrl+C to stop...")
        
        try:
            while True:
                status = self.get_comprehensive_status()
                self.print_status_report(status)
                
                # Save status every 10 minutes
                if len(self.status_history) % 10 == 0:
                    self.save_status_json(status)
                
                time.sleep(interval)
                
        except KeyboardInterrupt:
            print("\n\nMonitoring stopped by user")
            self.logger.info("Continuous monitoring stopped")
    
    def generate_health_report(self) -> str:
        """Generate a comprehensive health report"""
        status = self.get_comprehensive_status()
        issues = self.check_system_health(status)
        
        report = []
        report.append("HVAC SYSTEM HEALTH REPORT")
        report.append("=" * 50)
        report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")
        
        # Overall health score
        total_checks = 10
        passed_checks = total_checks - len([i for i in issues if "CRITICAL" in i or "WARNING" in i])
        health_score = (passed_checks / total_checks) * 100
        
        report.append(f"Overall Health Score: {health_score:.1f}%")
        report.append("")
        
        if health_score >= 90:
            report.append("🟢 System Status: EXCELLENT")
        elif health_score >= 75:
            report.append("🟡 System Status: GOOD")
        elif health_score >= 50:
            report.append("🟠 System Status: FAIR")
        else:
            report.append("🔴 System Status: POOR")
        
        report.append("")
        report.append("Issues Found:")
        if not issues:
            report.append("   ✅ No issues detected")
        else:
            for issue in issues:
                report.append(f"   {issue}")
        
        return "\n".join(report)

def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(description='HVAC System Status Monitor')
    parser.add_argument('--continuous', '-c', action='store_true', 
                       help='Run continuous monitoring')
    parser.add_argument('--interval', '-i', type=int, default=60,
                       help='Monitoring interval in seconds (default: 60)')
    parser.add_argument('--json', '-j', action='store_true',
                       help='Save status to JSON file')
    parser.add_argument('--health', '-h', action='store_true',
                       help='Generate health report only')
    parser.add_argument('--config', '-cfg', type=str,
                       help='Path to configuration file')
    
    args = parser.parse_args()
    
    # Create monitor instance
    monitor = HVACSystemMonitor(config_file=args.config)
    
    try:
        if args.health:
            # Generate health report only
            report = monitor.generate_health_report()
            print(report)
            
        elif args.continuous:
            # Run continuous monitoring
            monitor.run_continuous_monitoring(args.interval)
            
        else:
            # Single status check
            status = monitor.get_comprehensive_status()
            monitor.print_status_report(status)
            
            if args.json:
                monitor.save_status_json(status)
    
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
