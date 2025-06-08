"""
System Utilities for Automated Car Parking System
Helper functions, system monitoring, and maintenance tools
"""

import os
import sys
import time
import psutil
import logging
import threading
import json
import csv
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
import sqlite3
import shutil
import zipfile

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SystemMonitor:
    """System monitoring and health check utilities"""
    
    def __init__(self, db_path: str = "parking_system.db"):
        self.db_path = db_path
        self.monitoring = False
        self.monitor_thread = None
        self.performance_data = []
        
    def start_monitoring(self, interval: int = 30):
        """Start system monitoring"""
        if not self.monitoring:
            self.monitoring = True
            self.monitor_thread = threading.Thread(
                target=self._monitor_loop,
                args=(interval,)
            )
            self.monitor_thread.daemon = True
            self.monitor_thread.start()
            logger.info("System monitoring started")
            
    def stop_monitoring(self):
        """Stop system monitoring"""
        if self.monitoring:
            self.monitoring = False
            if self.monitor_thread:
                self.monitor_thread.join()
            logger.info("System monitoring stopped")
            
    def _monitor_loop(self, interval: int):
        """Main monitoring loop"""
        while self.monitoring:
            try:
                # Collect system metrics
                metrics = self.collect_system_metrics()
                self.performance_data.append(metrics)
                
                # Keep only last 1000 entries
                if len(self.performance_data) > 1000:
                    self.performance_data = self.performance_data[-1000:]
                    
                # Check for issues
                issues = self.check_system_health(metrics)
                for issue in issues:
                    logger.warning(f"System health issue: {issue}")
                    
                time.sleep(interval)
                
            except Exception as e:
                logger.error(f"Monitoring error: {e}")
                time.sleep(interval)
                
    def collect_system_metrics(self) -> Dict:
        """Collect current system metrics"""
        try:
            # CPU and Memory
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('.')
            
            # Database metrics
            db_size = 0
            db_connections = 0
            if os.path.exists(self.db_path):
                db_size = os.path.getsize(self.db_path)
                
            # Process information
            current_process = psutil.Process()
            process_memory = current_process.memory_info().rss
            
            # Network information
            network_io = psutil.net_io_counters()
            
            metrics = {
                'timestamp': datetime.now().isoformat(),
                'cpu_percent': cpu_percent,
                'memory_total': memory.total,
                'memory_used': memory.used,
                'memory_percent': memory.percent,
                'disk_total': disk.total,
                'disk_used': disk.used,
                'disk_percent': disk.percent,
                'db_size': db_size,
                'process_memory': process_memory,
                'network_bytes_sent': network_io.bytes_sent,
                'network_bytes_recv': network_io.bytes_recv
            }
            
            return metrics
            
        except Exception as e:
            logger.error(f"Error collecting metrics: {e}")
            return {}
            
    def check_system_health(self, metrics: Dict) -> List[str]:
        """Check system health and return list of issues"""
        issues = []
        
        try:
            # CPU usage check
            if metrics.get('cpu_percent', 0) > 90:
                issues.append(f"High CPU usage: {metrics['cpu_percent']:.1f}%")
                
            # Memory usage check
            if metrics.get('memory_percent', 0) > 85:
                issues.append(f"High memory usage: {metrics['memory_percent']:.1f}%")
                
            # Disk usage check
            if metrics.get('disk_percent', 0) > 90:
                issues.append(f"High disk usage: {metrics['disk_percent']:.1f}%")
                
            # Database size check (warn if > 1GB)
            if metrics.get('db_size', 0) > 1024 * 1024 * 1024:
                size_gb = metrics['db_size'] / (1024 * 1024 * 1024)
                issues.append(f"Large database size: {size_gb:.2f} GB")
                
            # Process memory check (warn if > 500MB)
            if metrics.get('process_memory', 0) > 500 * 1024 * 1024:
                size_mb = metrics['process_memory'] / (1024 * 1024)
                issues.append(f"High process memory: {size_mb:.1f} MB")
                
        except Exception as e:
            issues.append(f"Health check error: {e}")
            
        return issues
        
    def get_performance_summary(self, hours: int = 24) -> Dict:
        """Get performance summary for specified hours"""
        try:
            cutoff_time = datetime.now() - timedelta(hours=hours)
            
            # Filter recent data
            recent_data = [
                data for data in self.performance_data
                if datetime.fromisoformat(data['timestamp']) > cutoff_time
            ]
            
            if not recent_data:
                return {}
                
            # Calculate averages
            avg_cpu = sum(d.get('cpu_percent', 0) for d in recent_data) / len(recent_data)
            avg_memory = sum(d.get('memory_percent', 0) for d in recent_data) / len(recent_data)
            avg_disk = sum(d.get('disk_percent', 0) for d in recent_data) / len(recent_data)
            
            # Calculate peaks
            max_cpu = max(d.get('cpu_percent', 0) for d in recent_data)
            max_memory = max(d.get('memory_percent', 0) for d in recent_data)
            max_disk = max(d.get('disk_percent', 0) for d in recent_data)
            
            return {
                'period_hours': hours,
                'data_points': len(recent_data),
                'average_cpu': round(avg_cpu, 2),
                'average_memory': round(avg_memory, 2),
                'average_disk': round(avg_disk, 2),
                'peak_cpu': round(max_cpu, 2),
                'peak_memory': round(max_memory, 2),
                'peak_disk': round(max_disk, 2)
            }
            
        except Exception as e:
            logger.error(f"Error calculating performance summary: {e}")
            return {}

class FileManager:
    """File management utilities"""
    
    @staticmethod
    def backup_database(db_path: str, backup_dir: str = "backups") -> str:
        """Create database backup"""
        try:
            os.makedirs(backup_dir, exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_filename = f"parking_system_backup_{timestamp}.db"
            backup_path = os.path.join(backup_dir, backup_filename)
            
            shutil.copy2(db_path, backup_path)
            
            logger.info(f"Database backup created: {backup_path}")
            return backup_path
            
        except Exception as e:
            logger.error(f"Database backup failed: {e}")
            return ""
            
    @staticmethod
    def cleanup_old_backups(backup_dir: str = "backups", keep_days: int = 30):
        """Clean up old backup files"""
        try:
            if not os.path.exists(backup_dir):
                return
                
            cutoff_date = datetime.now() - timedelta(days=keep_days)
            removed_count = 0
            
            for filename in os.listdir(backup_dir):
                filepath = os.path.join(backup_dir, filename)
                
                if os.path.isfile(filepath):
                    file_time = datetime.fromtimestamp(os.path.getmtime(filepath))
                    
                    if file_time < cutoff_date:
                        os.remove(filepath)
                        removed_count += 1
                        
            logger.info(f"Cleaned up {removed_count} old backup files")
            
        except Exception as e:
            logger.error(f"Backup cleanup failed: {e}")
            
    @staticmethod
    def export_data_to_csv(db_path: str, output_dir: str = "exports") -> Dict[str, str]:
        """Export database tables to CSV files"""
        try:
            os.makedirs(output_dir, exist_ok=True)
            
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Get list of tables
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in cursor.fetchall()]
            
            exported_files = {}
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            for table in tables:
                # Export each table
                cursor.execute(f"SELECT * FROM {table}")
                rows = cursor.fetchall()
                
                if rows:
                    # Get column names
                    column_names = [description[0] for description in cursor.description]
                    
                    # Create CSV file
                    csv_filename = f"{table}_{timestamp}.csv"
                    csv_path = os.path.join(output_dir, csv_filename)
                    
                    with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
                        writer = csv.writer(csvfile)
                        writer.writerow(column_names)
                        writer.writerows(rows)
                        
                    exported_files[table] = csv_path
                    
            conn.close()
            
            logger.info(f"Exported {len(exported_files)} tables to CSV")
            return exported_files
            
        except Exception as e:
            logger.error(f"CSV export failed: {e}")
            return {}
            
    @staticmethod
    def create_system_archive(archive_name: str = None) -> str:
        """Create complete system archive"""
        try:
            if archive_name is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                archive_name = f"parking_system_archive_{timestamp}.zip"
                
            # Directories to include
            include_dirs = [
                'config', 'docs', 'hmi', 'plc', 'src', 'scripts'
            ]
            
            # Files to include
            include_files = [
                'README.md', 'requirements.txt', 'parking_system.db'
            ]
            
            with zipfile.ZipFile(archive_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
                # Add directories
                for dir_name in include_dirs:
                    if os.path.exists(dir_name):
                        for root, dirs, files in os.walk(dir_name):
                            for file in files:
                                file_path = os.path.join(root, file)
                                zipf.write(file_path)
                                
                # Add individual files
                for file_name in include_files:
                    if os.path.exists(file_name):
                        zipf.write(file_name)
                        
            logger.info(f"System archive created: {archive_name}")
            return archive_name
            
        except Exception as e:
            logger.error(f"Archive creation failed: {e}")
            return ""

class LogManager:
    """Log file management utilities"""
    
    @staticmethod
    def setup_logging(log_dir: str = "logs", max_size: int = 10485760, backup_count: int = 5):
        """Setup rotating log files"""
        try:
            os.makedirs(log_dir, exist_ok=True)
            
            from logging.handlers import RotatingFileHandler
            
            # Create formatters
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            
            # System log
            system_handler = RotatingFileHandler(
                os.path.join(log_dir, 'system.log'),
                maxBytes=max_size,
                backupCount=backup_count
            )
            system_handler.setFormatter(formatter)
            
            # Error log
            error_handler = RotatingFileHandler(
                os.path.join(log_dir, 'error.log'),
                maxBytes=max_size,
                backupCount=backup_count
            )
            error_handler.setLevel(logging.ERROR)
            error_handler.setFormatter(formatter)
            
            # Configure root logger
            root_logger = logging.getLogger()
            root_logger.addHandler(system_handler)
            root_logger.addHandler(error_handler)
            
            logger.info("Logging setup completed")
            
        except Exception as e:
            logger.error(f"Logging setup failed: {e}")
            
    @staticmethod
    def analyze_logs(log_file: str = "logs/system.log") -> Dict:
        """Analyze log file for patterns and issues"""
        try:
            if not os.path.exists(log_file):
                return {}
                
            error_count = 0
            warning_count = 0
            info_count = 0
            recent_errors = []
            
            with open(log_file, 'r', encoding='utf-8') as f:
                for line in f:
                    if ' - ERROR - ' in line:
                        error_count += 1
                        if len(recent_errors) < 10:
                            recent_errors.append(line.strip())
                    elif ' - WARNING - ' in line:
                        warning_count += 1
                    elif ' - INFO - ' in line:
                        info_count += 1
                        
            return {
                'error_count': error_count,
                'warning_count': warning_count,
                'info_count': info_count,
                'recent_errors': recent_errors
            }
            
        except Exception as e:
            logger.error(f"Log analysis failed: {e}")
            return {}

class DatabaseMaintenance:
    """Database maintenance utilities"""
    
    def __init__(self, db_path: str = "parking_system.db"):
        self.db_path = db_path
        
    def vacuum_database(self) -> bool:
        """Vacuum database to reclaim space"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.execute("VACUUM")
            conn.close()
            
            logger.info("Database vacuum completed")
            return True
            
        except Exception as e:
            logger.error(f"Database vacuum failed: {e}")
            return False
            
    def analyze_database(self) -> bool:
        """Analyze database for optimization"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.execute("ANALYZE")
            conn.close()
            
            logger.info("Database analysis completed")
            return True
            
        except Exception as e:
            logger.error(f"Database analysis failed: {e}")
            return False
            
    def get_database_stats(self) -> Dict:
        """Get database statistics"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            stats = {}
            
            # Get table information
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in cursor.fetchall()]
            
            for table in tables:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                stats[f"{table}_count"] = count
                
            # Database size
            stats['db_size_bytes'] = os.path.getsize(self.db_path)
            stats['db_size_mb'] = round(stats['db_size_bytes'] / (1024 * 1024), 2)
            
            conn.close()
            
            return stats
            
        except Exception as e:
            logger.error(f"Database stats collection failed: {e}")
            return {}
            
    def cleanup_old_data(self, days: int = 30) -> int:
        """Clean up old data from database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cutoff_date = datetime.now() - timedelta(days=days)
            
            # Clean up old vehicles
            cursor.execute(
                "DELETE FROM vehicles WHERE exit_time < ? AND exit_time IS NOT NULL",
                (cutoff_date,)
            )
            vehicles_deleted = cursor.rowcount
            
            # Clean up old events
            cursor.execute(
                "DELETE FROM system_events WHERE timestamp < ?",
                (cutoff_date,)
            )
            events_deleted = cursor.rowcount
            
            # Clean up old transactions
            cursor.execute(
                "DELETE FROM transactions WHERE timestamp < ?",
                (cutoff_date,)
            )
            transactions_deleted = cursor.rowcount
            
            conn.commit()
            conn.close()
            
            total_deleted = vehicles_deleted + events_deleted + transactions_deleted
            logger.info(f"Cleaned up {total_deleted} old records")
            
            return total_deleted
            
        except Exception as e:
            logger.error(f"Data cleanup failed: {e}")
            return 0

class SystemDiagnostics:
    """System diagnostics and troubleshooting"""
    
    @staticmethod
    def run_system_check() -> Dict:
        """Run comprehensive system check"""
        results = {
            'timestamp': datetime.now().isoformat(),
            'overall_status': 'OK',
            'checks': {}
        }
        
        try:
            # Check Python version
            python_version = sys.version_info
            results['checks']['python_version'] = {
                'status': 'OK' if python_version >= (3, 8) else 'WARNING',
                'value': f"{python_version.major}.{python_version.minor}.{python_version.micro}",
                'required': '3.8+'
            }
            
            # Check required directories
            required_dirs = ['config', 'logs', 'backups', 'hmi', 'src', 'plc']
            for dir_name in required_dirs:
                results['checks'][f'directory_{dir_name}'] = {
                    'status': 'OK' if os.path.exists(dir_name) else 'ERROR',
                    'exists': os.path.exists(dir_name)
                }
                
            # Check database
            db_path = 'parking_system.db'
            results['checks']['database'] = {
                'status': 'OK' if os.path.exists(db_path) else 'ERROR',
                'exists': os.path.exists(db_path),
                'size': os.path.getsize(db_path) if os.path.exists(db_path) else 0
            }
            
            # Check configuration file
            config_path = 'config/system_config.yaml'
            results['checks']['configuration'] = {
                'status': 'OK' if os.path.exists(config_path) else 'WARNING',
                'exists': os.path.exists(config_path)
            }
            
            # Check network ports
            import socket
            
            # Check WebSocket port
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.bind(('localhost', 8765))
                sock.close()
                websocket_status = 'OK'
            except OSError:
                websocket_status = 'IN_USE'
                
            results['checks']['websocket_port'] = {
                'status': websocket_status,
                'port': 8765
            }
            
            # Check TCP port
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.bind(('localhost', 9001))
                sock.close()
                tcp_status = 'OK'
            except OSError:
                tcp_status = 'IN_USE'
                
            results['checks']['tcp_port'] = {
                'status': tcp_status,
                'port': 9001
            }
            
            # Determine overall status
            error_count = sum(1 for check in results['checks'].values() if check['status'] == 'ERROR')
            warning_count = sum(1 for check in results['checks'].values() if check['status'] == 'WARNING')
            
            if error_count > 0:
                results['overall_status'] = 'ERROR'
            elif warning_count > 0:
                results['overall_status'] = 'WARNING'
                
            results['summary'] = {
                'total_checks': len(results['checks']),
                'errors': error_count,
                'warnings': warning_count
            }
            
        except Exception as e:
            results['overall_status'] = 'ERROR'
            results['error'] = str(e)
            
        return results
        
    @staticmethod
    def check_dependencies() -> Dict:
        """Check required Python packages"""
        results = {'status': 'OK', 'packages': {}}
        
        required_packages = [
            'tkinter', 'sqlite3', 'websockets', 'yaml', 
            'matplotlib', 'numpy', 'psutil'
        ]
        
        optional_packages = [
            'pymodbus', 'opcua', 'pyserial', 'plotly'
        ]
        
        for package in required_packages:
            try:
                __import__(package)
                results['packages'][package] = {'status': 'OK', 'required': True}
            except ImportError:
                results['packages'][package] = {'status': 'MISSING', 'required': True}
                results['status'] = 'ERROR'
                
        for package in optional_packages:
            try:
                __import__(package)
                results['packages'][package] = {'status': 'OK', 'required': False}
            except ImportError:
                results['packages'][package] = {'status': 'MISSING', 'required': False}
                
        return results

if __name__ == "__main__":
    # Run system diagnostics
    print("=== System Diagnostics ===")
    
    diagnostics = SystemDiagnostics()
    
    # System check
    check_results = diagnostics.run_system_check()
    print(f"Overall Status: {check_results['overall_status']}")
    print(f"Errors: {check_results['summary']['errors']}")
    print(f"Warnings: {check_results['summary']['warnings']}")
    
    # Dependency check
    dep_results = diagnostics.check_dependencies()
    print(f"Dependencies Status: {dep_results['status']}")
    
    # Performance monitoring
    monitor = SystemMonitor()
    monitor.start_monitoring(5)  # 5 second intervals
    
    try:
        time.sleep(30)  # Monitor for 30 seconds
        summary = monitor.get_performance_summary(1)  # Last hour
        print(f"Performance Summary: {summary}")
    finally:
        monitor.stop_monitoring()
