# filepath: c:\Users\Legion\Desktop\PLC\Car_Parking_Vending_System\src\optimization\performance_optimizer.py
"""
Performance Optimization Module for Car Parking Vending System
Optimizes system performance through various strategies and algorithms
"""

import os
import time
import sqlite3
import threading
import multiprocessing
from queue import Queue, Empty
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import psutil
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
import numpy as np
from collections import deque, defaultdict
import json
import pickle
from dataclasses import dataclass
import asyncio
import cProfile
import pstats
from functools import wraps, lru_cache
import gc

@dataclass
class PerformanceMetrics:
    """Performance metrics data structure"""
    timestamp: datetime
    cpu_usage: float
    memory_usage: float
    disk_usage: float
    response_time: float
    throughput: float
    error_rate: float
    active_connections: int

class PerformanceOptimizer:
    """Main performance optimization system"""
    
    def __init__(self, db_path: str, config: Dict = None):
        self.db_path = db_path
        self.config = config or {}
        
        # Set up logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        # Performance monitoring
        self.metrics_history = deque(maxlen=1000)
        self.metrics_lock = threading.Lock()
        
        # Connection pooling
        self.connection_pool = Queue(maxsize=20)
        self._init_connection_pool()
        
        # Caching system
        self.cache = {}
        self.cache_lock = threading.Lock()
        self.cache_stats = {'hits': 0, 'misses': 0}
        
        # Thread pool for async operations
        self.thread_pool = ThreadPoolExecutor(max_workers=8)
        
        # Optimization strategies
        self.optimization_strategies = {
            'database': DatabaseOptimizer(db_path),
            'memory': MemoryOptimizer(),
            'query': QueryOptimizer(db_path),
            'cache': CacheOptimizer(),
            'concurrent': ConcurrencyOptimizer()
        }
        
        # Performance monitoring
        self.monitoring_active = False
        self.monitoring_thread = None
        
        # Profiling
        self.profiler = None
        self.profiling_active = False
        
    def _init_connection_pool(self):
        """Initialize database connection pool"""
        for _ in range(10):
            conn = sqlite3.connect(self.db_path, check_same_thread=False)
            conn.execute("PRAGMA journal_mode=WAL")
            conn.execute("PRAGMA synchronous=NORMAL")
            conn.execute("PRAGMA cache_size=10000")
            conn.execute("PRAGMA temp_store=MEMORY")
            self.connection_pool.put(conn)
            
    def get_connection(self) -> sqlite3.Connection:
        """Get connection from pool"""
        try:
            return self.connection_pool.get(timeout=5)
        except Empty:
            # Create new connection if pool is empty
            conn = sqlite3.connect(self.db_path, check_same_thread=False)
            conn.execute("PRAGMA journal_mode=WAL")
            conn.execute("PRAGMA synchronous=NORMAL")
            return conn
            
    def return_connection(self, conn: sqlite3.Connection):
        """Return connection to pool"""
        try:
            self.connection_pool.put_nowait(conn)
        except:
            # Pool is full, close connection
            conn.close()
            
    def start_performance_monitoring(self):
        """Start performance monitoring"""
        if not self.monitoring_active:
            self.monitoring_active = True
            self.monitoring_thread = threading.Thread(target=self._monitor_performance, daemon=True)
            self.monitoring_thread.start()
            self.logger.info("Performance monitoring started")
            
    def stop_performance_monitoring(self):
        """Stop performance monitoring"""
        self.monitoring_active = False
        if self.monitoring_thread:
            self.monitoring_thread.join()
        self.logger.info("Performance monitoring stopped")
        
    def _monitor_performance(self):
        """Monitor system performance metrics"""
        while self.monitoring_active:
            try:
                # Collect system metrics
                cpu_percent = psutil.cpu_percent(interval=1)
                memory = psutil.virtual_memory()
                disk = psutil.disk_usage('/')
                
                # Calculate application-specific metrics
                response_time = self._measure_response_time()
                throughput = self._calculate_throughput()
                error_rate = self._calculate_error_rate()
                active_connections = self._count_active_connections()
                
                # Create metrics object
                metrics = PerformanceMetrics(
                    timestamp=datetime.now(),
                    cpu_usage=cpu_percent,
                    memory_usage=memory.percent,
                    disk_usage=disk.percent,
                    response_time=response_time,
                    throughput=throughput,
                    error_rate=error_rate,
                    active_connections=active_connections
                )
                
                # Store metrics
                with self.metrics_lock:
                    self.metrics_history.append(metrics)
                    
                # Check for performance issues
                self._check_performance_thresholds(metrics)
                
                time.sleep(10)  # Monitor every 10 seconds
                
            except Exception as e:
                self.logger.error(f"Performance monitoring error: {e}")
                time.sleep(10)
                
    def _measure_response_time(self) -> float:
        """Measure average response time for database queries"""
        try:
            conn = self.get_connection()
            start_time = time.time()
            
            cursor = conn.execute("SELECT COUNT(*) FROM parking_spaces")
            cursor.fetchone()
            
            response_time = (time.time() - start_time) * 1000  # Convert to milliseconds
            self.return_connection(conn)
            
            return response_time
            
        except Exception as e:
            self.logger.error(f"Response time measurement failed: {e}")
            return 0.0
            
    def _calculate_throughput(self) -> float:
        """Calculate system throughput (operations per second)"""
        try:
            conn = self.get_connection()
            cursor = conn.execute("""
                SELECT COUNT(*) 
                FROM system_events 
                WHERE timestamp >= datetime('now', '-1 minute')
            """)
            
            events_last_minute = cursor.fetchone()[0]
            self.return_connection(conn)
            
            return events_last_minute / 60.0  # Events per second
            
        except Exception as e:
            self.logger.error(f"Throughput calculation failed: {e}")
            return 0.0
            
    def _calculate_error_rate(self) -> float:
        """Calculate error rate percentage"""
        try:
            conn = self.get_connection()
            cursor = conn.execute("""
                SELECT 
                    COUNT(*) as total_events,
                    COUNT(CASE WHEN severity = 'error' THEN 1 END) as error_events
                FROM system_events 
                WHERE timestamp >= datetime('now', '-5 minutes')
            """)
            
            result = cursor.fetchone()
            self.return_connection(conn)
            
            total_events, error_events = result
            
            if total_events > 0:
                return (error_events / total_events) * 100
            return 0.0
            
        except Exception as e:
            self.logger.error(f"Error rate calculation failed: {e}")
            return 0.0
            
    def _count_active_connections(self) -> int:
        """Count active database connections"""
        # This is a simplified version - in reality, would track actual connections
        return self.connection_pool.qsize()
        
    def _check_performance_thresholds(self, metrics: PerformanceMetrics):
        """Check if performance metrics exceed thresholds"""
        thresholds = self.config.get('performance_thresholds', {
            'cpu_usage': 80.0,
            'memory_usage': 85.0,
            'response_time': 1000.0,  # 1 second
            'error_rate': 5.0
        })
        
        alerts = []
        
        if metrics.cpu_usage > thresholds['cpu_usage']:
            alerts.append(f"High CPU usage: {metrics.cpu_usage:.1f}%")
            
        if metrics.memory_usage > thresholds['memory_usage']:
            alerts.append(f"High memory usage: {metrics.memory_usage:.1f}%")
            
        if metrics.response_time > thresholds['response_time']:
            alerts.append(f"High response time: {metrics.response_time:.1f}ms")
            
        if metrics.error_rate > thresholds['error_rate']:
            alerts.append(f"High error rate: {metrics.error_rate:.1f}%")
            
        if alerts:
            self.logger.warning("Performance alerts: " + "; ".join(alerts))
            self._trigger_optimization()
            
    def _trigger_optimization(self):
        """Trigger optimization strategies when performance issues detected"""
        self.logger.info("Triggering performance optimization")
        
        # Run optimization strategies
        self.thread_pool.submit(self.optimization_strategies['memory'].optimize)
        self.thread_pool.submit(self.optimization_strategies['cache'].optimize, self.cache)
        self.thread_pool.submit(self.optimization_strategies['database'].optimize)
        
    @lru_cache(maxsize=1000)
    def cached_query(self, query: str, params: Tuple = ()) -> List[Dict]:
        """Execute cached database query"""
        cache_key = f"{query}:{hash(params)}"
        
        with self.cache_lock:
            if cache_key in self.cache:
                self.cache_stats['hits'] += 1
                return self.cache[cache_key]
                
        # Execute query
        conn = self.get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.execute(query, params)
        results = [dict(row) for row in cursor.fetchall()]
        self.return_connection(conn)
        
        # Cache results
        with self.cache_lock:
            self.cache[cache_key] = results
            self.cache_stats['misses'] += 1
            
        return results
        
    def optimize_query_execution(self, query: str, params: Tuple = ()) -> List[Dict]:
        """Optimize query execution with various strategies"""
        
        # Use query optimizer
        optimized_query = self.optimization_strategies['query'].optimize_query(query)
        
        # Use cached query if appropriate
        if self._is_cacheable_query(query):
            return self.cached_query(optimized_query, params)
            
        # Execute with optimized connection
        conn = self.get_connection()
        conn.row_factory = sqlite3.Row
        
        try:
            cursor = conn.execute(optimized_query, params)
            results = [dict(row) for row in cursor.fetchall()]
            return results
        finally:
            self.return_connection(conn)
            
    def _is_cacheable_query(self, query: str) -> bool:
        """Determine if query results should be cached"""
        # Cache SELECT queries that don't contain NOW(), CURRENT_TIMESTAMP, etc.
        if query.strip().upper().startswith('SELECT'):
            time_functions = ['NOW()', 'CURRENT_TIMESTAMP', 'datetime(\'now\')', 'RANDOM()']
            return not any(func in query.upper() for func in time_functions)
        return False
        
    def start_profiling(self, output_file: str = "performance_profile.prof"):
        """Start code profiling"""
        if not self.profiling_active:
            self.profiler = cProfile.Profile()
            self.profiler.enable()
            self.profiling_active = True
            self.logger.info("Code profiling started")
            
    def stop_profiling(self, output_file: str = "performance_profile.prof"):
        """Stop code profiling and save results"""
        if self.profiling_active and self.profiler:
            self.profiler.disable()
            self.profiling_active = False
            
            # Save profile to file
            self.profiler.dump_stats(output_file)
            
            # Generate readable stats
            stats = pstats.Stats(self.profiler)
            stats.sort_stats('cumulative')
            
            # Save text report
            with open(output_file.replace('.prof', '.txt'), 'w') as f:
                stats.print_stats(20, file=f)  # Top 20 functions
                
            self.logger.info(f"Profiling results saved to {output_file}")
            
    def get_performance_summary(self) -> Dict:
        """Get comprehensive performance summary"""
        with self.metrics_lock:
            if not self.metrics_history:
                return {}
                
            recent_metrics = list(self.metrics_history)[-10:]  # Last 10 measurements
            
        summary = {
            'timestamp': datetime.now().isoformat(),
            'metrics': {
                'cpu_usage': {
                    'current': recent_metrics[-1].cpu_usage,
                    'average': np.mean([m.cpu_usage for m in recent_metrics]),
                    'peak': np.max([m.cpu_usage for m in recent_metrics])
                },
                'memory_usage': {
                    'current': recent_metrics[-1].memory_usage,
                    'average': np.mean([m.memory_usage for m in recent_metrics]),
                    'peak': np.max([m.memory_usage for m in recent_metrics])
                },
                'response_time': {
                    'current': recent_metrics[-1].response_time,
                    'average': np.mean([m.response_time for m in recent_metrics]),
                    'peak': np.max([m.response_time for m in recent_metrics])
                },
                'throughput': {
                    'current': recent_metrics[-1].throughput,
                    'average': np.mean([m.throughput for m in recent_metrics])
                },
                'error_rate': {
                    'current': recent_metrics[-1].error_rate,
                    'average': np.mean([m.error_rate for m in recent_metrics])
                }
            },
            'cache_stats': self.cache_stats.copy(),
            'connection_pool': {
                'available': self.connection_pool.qsize(),
                'total': 20
            },
            'optimization_status': {
                strategy: optimizer.get_status() 
                for strategy, optimizer in self.optimization_strategies.items()
                if hasattr(optimizer, 'get_status')
            }
        }
        
        return summary
        
    def cleanup_resources(self):
        """Clean up system resources"""
        # Clear cache
        with self.cache_lock:
            self.cache.clear()
            
        # Force garbage collection
        gc.collect()
        
        # Close database connections
        while not self.connection_pool.empty():
            try:
                conn = self.connection_pool.get_nowait()
                conn.close()
            except Empty:
                break
                
        self.logger.info("System resources cleaned up")


class DatabaseOptimizer:
    """Database-specific optimization strategies"""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.logger = logging.getLogger(f"{__name__}.DatabaseOptimizer")
        
    def optimize(self):
        """Run database optimization"""
        self.logger.info("Running database optimization")
        
        with sqlite3.connect(self.db_path) as conn:
            # Analyze tables for query optimization
            conn.execute("ANALYZE")
            
            # Vacuum database to reclaim space
            conn.execute("VACUUM")
            
            # Update statistics
            conn.execute("PRAGMA optimize")
            
        self.logger.info("Database optimization completed")
        
    def create_indexes(self):
        """Create performance indexes"""
        indexes = [
            "CREATE INDEX IF NOT EXISTS idx_transactions_date ON transactions(transaction_date)",
            "CREATE INDEX IF NOT EXISTS idx_transactions_user ON transactions(user_id)",
            "CREATE INDEX IF NOT EXISTS idx_transactions_space ON transactions(space_id)",
            "CREATE INDEX IF NOT EXISTS idx_parking_spaces_status ON parking_spaces(is_occupied, is_active)",
            "CREATE INDEX IF NOT EXISTS idx_system_events_timestamp ON system_events(timestamp)",
            "CREATE INDEX IF NOT EXISTS idx_system_events_type ON system_events(event_type)",
        ]
        
        with sqlite3.connect(self.db_path) as conn:
            for index_sql in indexes:
                try:
                    conn.execute(index_sql)
                    self.logger.info(f"Created index: {index_sql}")
                except sqlite3.Error as e:
                    self.logger.warning(f"Index creation failed: {e}")
                    
    def get_status(self) -> Dict:
        """Get database optimization status"""
        with sqlite3.connect(self.db_path) as conn:
            # Get database size
            cursor = conn.execute("SELECT page_count * page_size as size FROM pragma_page_count(), pragma_page_size()")
            db_size = cursor.fetchone()[0]
            
            # Get table counts
            cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in cursor.fetchall()]
            
            table_stats = {}
            for table in tables:
                try:
                    cursor = conn.execute(f"SELECT COUNT(*) FROM {table}")
                    table_stats[table] = cursor.fetchone()[0]
                except sqlite3.Error:
                    table_stats[table] = 0
                    
        return {
            'database_size_bytes': db_size,
            'table_counts': table_stats,
            'last_optimized': datetime.now().isoformat()
        }


class MemoryOptimizer:
    """Memory optimization strategies"""
    
    def __init__(self):
        self.logger = logging.getLogger(f"{__name__}.MemoryOptimizer")
        
    def optimize(self):
        """Run memory optimization"""
        self.logger.info("Running memory optimization")
        
        # Force garbage collection
        gc.collect()
        
        # Get memory usage before and after
        process = psutil.Process()
        memory_info = process.memory_info()
        
        self.logger.info(f"Memory optimization completed. RSS: {memory_info.rss / 1024 / 1024:.1f} MB")
        
    def get_memory_usage(self) -> Dict:
        """Get current memory usage statistics"""
        process = psutil.Process()
        memory_info = process.memory_info()
        
        return {
            'rss_mb': memory_info.rss / 1024 / 1024,
            'vms_mb': memory_info.vms / 1024 / 1024,
            'percent': process.memory_percent(),
            'available_mb': psutil.virtual_memory().available / 1024 / 1024
        }


class QueryOptimizer:
    """SQL query optimization"""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.logger = logging.getLogger(f"{__name__}.QueryOptimizer")
        
    def optimize_query(self, query: str) -> str:
        """Optimize SQL query"""
        # Basic query optimization rules
        optimized = query.strip()
        
        # Add LIMIT if missing from SELECT queries
        if (optimized.upper().startswith('SELECT') and 
            'LIMIT' not in optimized.upper() and 
            'COUNT(' not in optimized.upper()):
            optimized += " LIMIT 1000"
            
        # Use indexes where possible
        optimized = self._suggest_index_usage(optimized)
        
        return optimized
        
    def _suggest_index_usage(self, query: str) -> str:
        """Suggest index usage improvements"""
        # This is a simplified version - real implementation would be more sophisticated
        return query


class CacheOptimizer:
    """Cache optimization strategies"""
    
    def __init__(self):
        self.logger = logging.getLogger(f"{__name__}.CacheOptimizer")
        
    def optimize(self, cache: Dict):
        """Optimize cache performance"""
        # Remove old entries if cache is too large
        max_cache_size = 1000
        
        if len(cache) > max_cache_size:
            # Remove oldest 20% of entries
            entries_to_remove = len(cache) - int(max_cache_size * 0.8)
            keys_to_remove = list(cache.keys())[:entries_to_remove]
            
            for key in keys_to_remove:
                cache.pop(key, None)
                
            self.logger.info(f"Cache optimized: removed {entries_to_remove} entries")


class ConcurrencyOptimizer:
    """Concurrency optimization strategies"""
    
    def __init__(self):
        self.logger = logging.getLogger(f"{__name__}.ConcurrencyOptimizer")
        
    def optimize(self):
        """Optimize concurrency settings"""
        # Adjust thread pool sizes based on system resources
        cpu_count = multiprocessing.cpu_count()
        optimal_threads = min(cpu_count * 2, 16)
        
        self.logger.info(f"Optimal thread count: {optimal_threads}")
        
        return {
            'recommended_thread_count': optimal_threads,
            'cpu_count': cpu_count
        }


def performance_monitor(func):
    """Decorator to monitor function performance"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            result = func(*args, **kwargs)
            execution_time = time.time() - start_time
            
            # Log performance if it's slow
            if execution_time > 1.0:  # More than 1 second
                logger = logging.getLogger(__name__)
                logger.warning(f"Slow function {func.__name__}: {execution_time:.2f}s")
                
            return result
        except Exception as e:
            execution_time = time.time() - start_time
            logger = logging.getLogger(__name__)
            logger.error(f"Function {func.__name__} failed after {execution_time:.2f}s: {e}")
            raise
            
    return wrapper


def main():
    """Main function for testing performance optimization"""
    db_path = "data/parking_system.db"
    
    # Create performance optimizer
    optimizer = PerformanceOptimizer(db_path)
    
    # Start monitoring
    optimizer.start_performance_monitoring()
    
    try:
        # Test query optimization
        result = optimizer.optimize_query_execution(
            "SELECT * FROM parking_spaces WHERE is_active = 1",
            ()
        )
        print(f"Query returned {len(result)} results")
        
        # Get performance summary
        summary = optimizer.get_performance_summary()
        print("Performance Summary:")
        print(json.dumps(summary, indent=2, default=str))
        
        # Wait a bit for metrics collection
        time.sleep(30)
        
    finally:
        # Clean up
        optimizer.stop_performance_monitoring()
        optimizer.cleanup_resources()

if __name__ == "__main__":
    main()
