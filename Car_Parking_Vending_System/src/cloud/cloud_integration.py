# filepath: c:\Users\Legion\Desktop\PLC\Car_Parking_Vending_System\src\cloud\cloud_integration.py
"""
Cloud Integration Module for Car Parking Vending System
Provides integration with cloud services for scalability, backup, and analytics
"""

import os
import json
import logging
import asyncio
import aiohttp
import boto3
from azure.storage.blob import BlobServiceClient
from google.cloud import storage as gcs
from google.cloud import bigquery
import paho.mqtt.client as mqtt
import redis
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import sqlite3
import pandas as pd
import numpy as np
from concurrent.futures import ThreadPoolExecutor
import schedule
import time
from threading import Thread

class CloudIntegrationManager:
    """Manages cloud service integrations"""
    
    def __init__(self, config: Dict):
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # Initialize cloud service clients
        self._init_aws_services()
        self._init_azure_services()
        self._init_gcp_services()
        self._init_mqtt_client()
        self._init_redis_client()
        
        # Set up background tasks
        self.executor = ThreadPoolExecutor(max_workers=4)
        self.scheduler_thread = None
        
    def _init_aws_services(self):
        """Initialize AWS services"""
        if self.config.get('aws', {}).get('enabled'):
            try:
                self.s3_client = boto3.client(
                    's3',
                    aws_access_key_id=self.config['aws']['access_key'],
                    aws_secret_access_key=self.config['aws']['secret_key'],
                    region_name=self.config['aws']['region']
                )
                
                self.dynamodb = boto3.resource(
                    'dynamodb',
                    aws_access_key_id=self.config['aws']['access_key'],
                    aws_secret_access_key=self.config['aws']['secret_key'],
                    region_name=self.config['aws']['region']
                )
                
                self.cloudwatch = boto3.client(
                    'cloudwatch',
                    aws_access_key_id=self.config['aws']['access_key'],
                    aws_secret_access_key=self.config['aws']['secret_key'],
                    region_name=self.config['aws']['region']
                )
                
                self.logger.info("AWS services initialized successfully")
                
            except Exception as e:
                self.logger.error(f"Failed to initialize AWS services: {e}")
                self.s3_client = None
                self.dynamodb = None
                self.cloudwatch = None
        else:
            self.s3_client = None
            self.dynamodb = None
            self.cloudwatch = None
            
    def _init_azure_services(self):
        """Initialize Azure services"""
        if self.config.get('azure', {}).get('enabled'):
            try:
                self.blob_service = BlobServiceClient(
                    account_url=f"https://{self.config['azure']['storage_account']}.blob.core.windows.net",
                    credential=self.config['azure']['storage_key']
                )
                
                self.logger.info("Azure services initialized successfully")
                
            except Exception as e:
                self.logger.error(f"Failed to initialize Azure services: {e}")
                self.blob_service = None
        else:
            self.blob_service = None
            
    def _init_gcp_services(self):
        """Initialize Google Cloud Platform services"""
        if self.config.get('gcp', {}).get('enabled'):
            try:
                # Initialize GCS
                self.gcs_client = gcs.Client.from_service_account_json(
                    self.config['gcp']['credentials_file']
                )
                
                # Initialize BigQuery
                self.bigquery_client = bigquery.Client.from_service_account_json(
                    self.config['gcp']['credentials_file']
                )
                
                self.logger.info("GCP services initialized successfully")
                
            except Exception as e:
                self.logger.error(f"Failed to initialize GCP services: {e}")
                self.gcs_client = None
                self.bigquery_client = None
        else:
            self.gcs_client = None
            self.bigquery_client = None
            
    def _init_mqtt_client(self):
        """Initialize MQTT client for IoT communications"""
        if self.config.get('mqtt', {}).get('enabled'):
            try:
                self.mqtt_client = mqtt.Client()
                
                # Set up callbacks
                self.mqtt_client.on_connect = self._on_mqtt_connect
                self.mqtt_client.on_message = self._on_mqtt_message
                self.mqtt_client.on_disconnect = self._on_mqtt_disconnect
                
                # Connect to MQTT broker
                broker_config = self.config['mqtt']
                if broker_config.get('username'):
                    self.mqtt_client.username_pw_set(
                        broker_config['username'],
                        broker_config['password']
                    )
                    
                self.mqtt_client.connect(
                    broker_config['broker'],
                    broker_config.get('port', 1883),
                    60
                )
                
                self.mqtt_client.loop_start()
                self.logger.info("MQTT client initialized successfully")
                
            except Exception as e:
                self.logger.error(f"Failed to initialize MQTT client: {e}")
                self.mqtt_client = None
        else:
            self.mqtt_client = None
            
    def _init_redis_client(self):
        """Initialize Redis client for caching"""
        if self.config.get('redis', {}).get('enabled'):
            try:
                self.redis_client = redis.Redis(
                    host=self.config['redis']['host'],
                    port=self.config['redis'].get('port', 6379),
                    password=self.config['redis'].get('password'),
                    decode_responses=True
                )
                
                # Test connection
                self.redis_client.ping()
                self.logger.info("Redis client initialized successfully")
                
            except Exception as e:
                self.logger.error(f"Failed to initialize Redis client: {e}")
                self.redis_client = None
        else:
            self.redis_client = None
            
    def _on_mqtt_connect(self, client, userdata, flags, rc):
        """MQTT connection callback"""
        if rc == 0:
            self.logger.info("Connected to MQTT broker")
            # Subscribe to relevant topics
            topics = [
                "parking/sensors/+/status",
                "parking/elevators/+/status",
                "parking/payment/+/transaction",
                "parking/emergency/alert"
            ]
            for topic in topics:
                client.subscribe(topic)
        else:
            self.logger.error(f"Failed to connect to MQTT broker: {rc}")
            
    def _on_mqtt_message(self, client, userdata, msg):
        """MQTT message callback"""
        try:
            topic = msg.topic
            payload = json.loads(msg.payload.decode())
            
            # Process message based on topic
            if "/sensors/" in topic:
                self._process_sensor_data(topic, payload)
            elif "/elevators/" in topic:
                self._process_elevator_data(topic, payload)
            elif "/payment/" in topic:
                self._process_payment_data(topic, payload)
            elif "/emergency/" in topic:
                self._process_emergency_alert(topic, payload)
                
        except Exception as e:
            self.logger.error(f"Error processing MQTT message: {e}")
            
    def _on_mqtt_disconnect(self, client, userdata, rc):
        """MQTT disconnection callback"""
        self.logger.warning("Disconnected from MQTT broker")
        
    def backup_database_to_cloud(self, db_path: str) -> Dict[str, bool]:
        """Backup database to multiple cloud providers"""
        results = {}
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_filename = f"parking_system_backup_{timestamp}.db"
        
        # AWS S3 backup
        if self.s3_client:
            try:
                self.s3_client.upload_file(
                    db_path,
                    self.config['aws']['backup_bucket'],
                    f"database_backups/{backup_filename}"
                )
                results['aws_s3'] = True
                self.logger.info(f"Database backed up to AWS S3: {backup_filename}")
            except Exception as e:
                self.logger.error(f"AWS S3 backup failed: {e}")
                results['aws_s3'] = False
                
        # Azure Blob Storage backup
        if self.blob_service:
            try:
                blob_client = self.blob_service.get_blob_client(
                    container=self.config['azure']['backup_container'],
                    blob=f"database_backups/{backup_filename}"
                )
                
                with open(db_path, 'rb') as data:
                    blob_client.upload_blob(data, overwrite=True)
                    
                results['azure_blob'] = True
                self.logger.info(f"Database backed up to Azure Blob: {backup_filename}")
            except Exception as e:
                self.logger.error(f"Azure Blob backup failed: {e}")
                results['azure_blob'] = False
                
        # Google Cloud Storage backup
        if self.gcs_client:
            try:
                bucket = self.gcs_client.bucket(self.config['gcp']['backup_bucket'])
                blob = bucket.blob(f"database_backups/{backup_filename}")
                
                blob.upload_from_filename(db_path)
                results['gcp_storage'] = True
                self.logger.info(f"Database backed up to GCP Storage: {backup_filename}")
            except Exception as e:
                self.logger.error(f"GCP Storage backup failed: {e}")
                results['gcp_storage'] = False
                
        return results
        
    def sync_data_to_cloud_analytics(self, db_path: str):
        """Sync data to cloud analytics platforms"""
        
        # Export data to BigQuery
        if self.bigquery_client:
            self._sync_to_bigquery(db_path)
            
        # Export metrics to CloudWatch
        if self.cloudwatch:
            self._sync_to_cloudwatch(db_path)
            
    def _sync_to_bigquery(self, db_path: str):
        """Sync data to Google BigQuery for analytics"""
        try:
            with sqlite3.connect(db_path) as conn:
                # Export transactions
                transactions_df = pd.read_sql_query("""
                    SELECT 
                        id, transaction_date, amount, payment_method, status,
                        space_id, user_id, vehicle_id,
                        DATE(transaction_date) as transaction_date_only,
                        strftime('%H', transaction_date) as transaction_hour,
                        strftime('%w', transaction_date) as day_of_week
                    FROM transactions
                    WHERE transaction_date >= date('now', '-7 days')
                """, conn)
                
                # Upload to BigQuery
                dataset_id = self.config['gcp']['bigquery_dataset']
                table_id = 'transactions'
                
                job_config = bigquery.LoadJobConfig(
                    write_disposition="WRITE_APPEND",
                    autodetect=True
                )
                
                job = self.bigquery_client.load_table_from_dataframe(
                    transactions_df, 
                    f"{dataset_id}.{table_id}",
                    job_config=job_config
                )
                
                job.result()  # Wait for completion
                self.logger.info(f"Synced {len(transactions_df)} transactions to BigQuery")
                
                # Export occupancy data
                occupancy_df = pd.read_sql_query("""
                    SELECT 
                        timestamp, total_spaces, occupied_spaces, 
                        (occupied_spaces * 100.0 / total_spaces) as occupancy_rate,
                        DATE(timestamp) as date_only,
                        strftime('%H', timestamp) as hour
                    FROM system_statistics
                    WHERE timestamp >= datetime('now', '-7 days')
                """, conn)
                
                job = self.bigquery_client.load_table_from_dataframe(
                    occupancy_df, 
                    f"{dataset_id}.occupancy_stats",
                    job_config=job_config
                )
                
                job.result()
                self.logger.info(f"Synced {len(occupancy_df)} occupancy records to BigQuery")
                
        except Exception as e:
            self.logger.error(f"BigQuery sync failed: {e}")
            
    def _sync_to_cloudwatch(self, db_path: str):
        """Sync metrics to AWS CloudWatch"""
        try:
            with sqlite3.connect(db_path) as conn:
                cursor = conn.cursor()
                
                # Get current metrics
                cursor.execute("""
                    SELECT 
                        COUNT(*) as total_transactions,
                        SUM(amount) as total_revenue,
                        AVG(amount) as avg_transaction_value
                    FROM transactions 
                    WHERE transaction_date >= datetime('now', '-1 hour')
                """)
                
                metrics = cursor.fetchone()
                
                # Get occupancy metrics
                cursor.execute("""
                    SELECT 
                        AVG(occupied_spaces * 100.0 / total_spaces) as avg_occupancy,
                        MAX(occupied_spaces * 100.0 / total_spaces) as peak_occupancy
                    FROM system_statistics 
                    WHERE timestamp >= datetime('now', '-1 hour')
                """)
                
                occupancy = cursor.fetchone()
                
                # Send metrics to CloudWatch
                namespace = 'ParkingSystem'
                timestamp = datetime.utcnow()
                
                metric_data = [
                    {
                        'MetricName': 'TransactionCount',
                        'Value': metrics[0] or 0,
                        'Unit': 'Count',
                        'Timestamp': timestamp
                    },
                    {
                        'MetricName': 'Revenue',
                        'Value': metrics[1] or 0,
                        'Unit': 'None',
                        'Timestamp': timestamp
                    },
                    {
                        'MetricName': 'AverageOccupancy',
                        'Value': occupancy[0] or 0,
                        'Unit': 'Percent',
                        'Timestamp': timestamp
                    },
                    {
                        'MetricName': 'PeakOccupancy',
                        'Value': occupancy[1] or 0,
                        'Unit': 'Percent',
                        'Timestamp': timestamp
                    }
                ]
                
                self.cloudwatch.put_metric_data(
                    Namespace=namespace,
                    MetricData=metric_data
                )
                
                self.logger.info("Metrics synced to CloudWatch")
                
        except Exception as e:
            self.logger.error(f"CloudWatch sync failed: {e}")
            
    def cache_data(self, key: str, data: Any, expiry_seconds: int = 3600) -> bool:
        """Cache data in Redis"""
        if not self.redis_client:
            return False
            
        try:
            if isinstance(data, (dict, list)):
                data = json.dumps(data)
                
            self.redis_client.setex(key, expiry_seconds, data)
            return True
            
        except Exception as e:
            self.logger.error(f"Cache operation failed: {e}")
            return False
            
    def get_cached_data(self, key: str) -> Optional[Any]:
        """Get cached data from Redis"""
        if not self.redis_client:
            return None
            
        try:
            data = self.redis_client.get(key)
            if data:
                try:
                    return json.loads(data)
                except json.JSONDecodeError:
                    return data
            return None
            
        except Exception as e:
            self.logger.error(f"Cache retrieval failed: {e}")
            return None
            
    def publish_sensor_data(self, sensor_id: str, data: Dict):
        """Publish sensor data via MQTT"""
        if not self.mqtt_client:
            return False
            
        try:
            topic = f"parking/sensors/{sensor_id}/data"
            payload = json.dumps({
                'sensor_id': sensor_id,
                'timestamp': datetime.now().isoformat(),
                'data': data
            })
            
            self.mqtt_client.publish(topic, payload)
            return True
            
        except Exception as e:
            self.logger.error(f"MQTT publish failed: {e}")
            return False
            
    def _process_sensor_data(self, topic: str, payload: Dict):
        """Process incoming sensor data"""
        # Extract sensor ID from topic
        sensor_id = topic.split('/')[2]
        
        # Cache the latest sensor data
        cache_key = f"sensor:{sensor_id}:latest"
        self.cache_data(cache_key, payload, expiry_seconds=300)  # 5 minutes
        
        # Store in time-series database if configured
        if self.config.get('timeseries', {}).get('enabled'):
            self._store_timeseries_data('sensor_data', sensor_id, payload)
            
    def _process_elevator_data(self, topic: str, payload: Dict):
        """Process elevator status data"""
        elevator_id = topic.split('/')[2]
        
        # Cache elevator status
        cache_key = f"elevator:{elevator_id}:status"
        self.cache_data(cache_key, payload, expiry_seconds=60)  # 1 minute
        
    def _process_payment_data(self, topic: str, payload: Dict):
        """Process payment transaction data"""
        # Real-time payment analytics
        self._update_payment_analytics(payload)
        
    def _process_emergency_alert(self, topic: str, payload: Dict):
        """Process emergency alerts"""
        # Immediate notification to monitoring systems
        self._send_emergency_notification(payload)
        
    def start_background_tasks(self):
        """Start background synchronization tasks"""
        
        # Schedule regular backups
        schedule.every(4).hours.do(self._scheduled_backup)
        
        # Schedule data sync
        schedule.every(1).hour.do(self._scheduled_data_sync)
        
        # Schedule cache cleanup
        schedule.every(6).hours.do(self._cleanup_cache)
        
        # Start scheduler thread
        self.scheduler_thread = Thread(target=self._run_scheduler, daemon=True)
        self.scheduler_thread.start()
        
        self.logger.info("Background tasks started")
        
    def _run_scheduler(self):
        """Run the task scheduler"""
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
            
    def _scheduled_backup(self):
        """Scheduled database backup"""
        db_path = self.config.get('database', {}).get('path', 'data/parking_system.db')
        results = self.backup_database_to_cloud(db_path)
        self.logger.info(f"Scheduled backup completed: {results}")
        
    def _scheduled_data_sync(self):
        """Scheduled data synchronization"""
        db_path = self.config.get('database', {}).get('path', 'data/parking_system.db')
        self.sync_data_to_cloud_analytics(db_path)
        self.logger.info("Scheduled data sync completed")
        
    def _cleanup_cache(self):
        """Clean up expired cache entries"""
        if self.redis_client:
            try:
                # Get keys with pattern
                keys = self.redis_client.keys("parking:*:temp")
                if keys:
                    self.redis_client.delete(*keys)
                    self.logger.info(f"Cleaned up {len(keys)} temporary cache entries")
            except Exception as e:
                self.logger.error(f"Cache cleanup failed: {e}")
                
    def get_cloud_status(self) -> Dict[str, bool]:
        """Get status of all cloud services"""
        status = {
            'aws_s3': False,
            'aws_dynamodb': False,
            'aws_cloudwatch': False,
            'azure_blob': False,
            'gcp_storage': False,
            'gcp_bigquery': False,
            'mqtt': False,
            'redis': False
        }
        
        # Test AWS services
        if self.s3_client:
            try:
                self.s3_client.list_buckets()
                status['aws_s3'] = True
            except:
                pass
                
        if self.dynamodb:
            try:
                list(self.dynamodb.tables.all())
                status['aws_dynamodb'] = True
            except:
                pass
                
        if self.cloudwatch:
            try:
                self.cloudwatch.list_metrics(MaxRecords=1)
                status['aws_cloudwatch'] = True
            except:
                pass
                
        # Test Azure services
        if self.blob_service:
            try:
                list(self.blob_service.list_containers(max_results=1))
                status['azure_blob'] = True
            except:
                pass
                
        # Test GCP services
        if self.gcs_client:
            try:
                list(self.gcs_client.list_buckets(max_results=1))
                status['gcp_storage'] = True
            except:
                pass
                
        if self.bigquery_client:
            try:
                list(self.bigquery_client.list_datasets(max_results=1))
                status['gcp_bigquery'] = True
            except:
                pass
                
        # Test MQTT
        if self.mqtt_client and self.mqtt_client.is_connected():
            status['mqtt'] = True
            
        # Test Redis
        if self.redis_client:
            try:
                self.redis_client.ping()
                status['redis'] = True
            except:
                pass
                
        return status
        
    def shutdown(self):
        """Shutdown cloud integration services"""
        if self.mqtt_client:
            self.mqtt_client.loop_stop()
            self.mqtt_client.disconnect()
            
        if self.redis_client:
            self.redis_client.close()
            
        if self.scheduler_thread:
            schedule.clear()
            
        self.logger.info("Cloud integration services shut down")


def main():
    """Main function for testing cloud integration"""
    
    # Sample configuration
    config = {
        'aws': {
            'enabled': False,  # Set to True with valid credentials
            'access_key': 'your_aws_access_key',
            'secret_key': 'your_aws_secret_key',
            'region': 'us-east-1',
            'backup_bucket': 'parking-system-backups'
        },
        'azure': {
            'enabled': False,  # Set to True with valid credentials
            'storage_account': 'your_storage_account',
            'storage_key': 'your_storage_key',
            'backup_container': 'backups'
        },
        'gcp': {
            'enabled': False,  # Set to True with valid credentials
            'credentials_file': 'path/to/service_account.json',
            'backup_bucket': 'parking-system-backups',
            'bigquery_dataset': 'parking_analytics'
        },
        'mqtt': {
            'enabled': False,  # Set to True with valid broker
            'broker': 'mqtt.your-iot-platform.com',
            'port': 1883,
            'username': 'your_username',
            'password': 'your_password'
        },
        'redis': {
            'enabled': False,  # Set to True with valid Redis instance
            'host': 'localhost',
            'port': 6379,
            'password': None
        },
        'database': {
            'path': 'data/parking_system.db'
        }
    }
    
    # Initialize cloud integration
    cloud_mgr = CloudIntegrationManager(config)
    
    # Test cloud service status
    status = cloud_mgr.get_cloud_status()
    print("Cloud service status:", status)
    
    # Start background tasks (if any services are enabled)
    if any(status.values()):
        cloud_mgr.start_background_tasks()
        print("Background tasks started")
    else:
        print("No cloud services enabled - running in local mode")

if __name__ == "__main__":
    main()
