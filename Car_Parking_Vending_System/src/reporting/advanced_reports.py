# filepath: c:\Users\Legion\Desktop\PLC\Car_Parking_Vending_System\src\reporting\advanced_reports.py
"""
Advanced Reporting System for Car Parking Vending System
Generates comprehensive business intelligence and operational reports
"""

import os
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import json
import logging
from typing import Dict, List, Optional, Tuple
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.offline as pyo

class AdvancedReportGenerator:
    """Advanced reporting system with business intelligence capabilities"""
    
    def __init__(self, db_path: str, output_dir: str):
        self.db_path = db_path
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
        # Set up logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        # Configure plotting
        plt.style.use('seaborn-v0_8')
        sns.set_palette("husl")
        
        # Report configuration
        self.report_config = {
            'page_size': (11, 8.5),  # Letter size landscape
            'dpi': 300,
            'font_size': 10,
            'title_size': 16,
            'colors': {
                'primary': '#2c3e50',
                'secondary': '#3498db',
                'success': '#27ae60',
                'warning': '#f39c12',
                'danger': '#e74c3c'
            }
        }
        
    def get_db_connection(self) -> sqlite3.Connection:
        """Get database connection with row factory"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
        
    def generate_executive_summary(self, start_date: str, end_date: str) -> str:
        """Generate executive summary report"""
        self.logger.info(f"Generating executive summary for {start_date} to {end_date}")
        
        with self.get_db_connection() as conn:
            # Key metrics
            total_transactions = self._get_total_transactions(conn, start_date, end_date)
            total_revenue = self._get_total_revenue(conn, start_date, end_date)
            avg_occupancy = self._get_average_occupancy(conn, start_date, end_date)
            customer_satisfaction = self._get_customer_satisfaction(conn, start_date, end_date)
            
            # Peak usage analysis
            peak_hours = self._get_peak_hours(conn, start_date, end_date)
            busiest_days = self._get_busiest_days(conn, start_date, end_date)
            
        # Generate report
        report_path = os.path.join(self.output_dir, f'executive_summary_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf')
        
        with PdfPages(report_path) as pdf:
            # Title page
            fig, ax = plt.subplots(figsize=self.report_config['page_size'])
            ax.text(0.5, 0.8, 'Car Parking System Executive Summary', 
                   fontsize=24, fontweight='bold', ha='center', transform=ax.transAxes)
            ax.text(0.5, 0.7, f'Report Period: {start_date} to {end_date}', 
                   fontsize=16, ha='center', transform=ax.transAxes)
            ax.text(0.5, 0.6, f'Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', 
                   fontsize=12, ha='center', transform=ax.transAxes)
            ax.axis('off')
            pdf.savefig(fig, bbox_inches='tight')
            plt.close()
            
            # Key metrics overview
            self._create_kpi_dashboard(pdf, {
                'Total Transactions': total_transactions,
                'Total Revenue': f"${total_revenue:,.2f}",
                'Average Occupancy': f"{avg_occupancy:.1f}%",
                'Customer Satisfaction': f"{customer_satisfaction:.1f}/5.0"
            })
            
            # Usage patterns
            self._create_usage_patterns_report(pdf, peak_hours, busiest_days)
            
            # Revenue analysis
            self._create_revenue_analysis(pdf, start_date, end_date)
            
            # Operational efficiency
            self._create_efficiency_analysis(pdf, start_date, end_date)
            
        return report_path
        
    def generate_operational_report(self, start_date: str, end_date: str) -> str:
        """Generate detailed operational report"""
        self.logger.info(f"Generating operational report for {start_date} to {end_date}")
        
        report_path = os.path.join(self.output_dir, f'operational_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf')
        
        with PdfPages(report_path) as pdf:
            # Equipment performance
            self._create_equipment_performance_report(pdf, start_date, end_date)
            
            # System uptime analysis
            self._create_uptime_analysis(pdf, start_date, end_date)
            
            # Error and maintenance analysis
            self._create_maintenance_analysis(pdf, start_date, end_date)
            
            # Capacity utilization
            self._create_capacity_analysis(pdf, start_date, end_date)
            
            # Energy consumption
            self._create_energy_analysis(pdf, start_date, end_date)
            
        return report_path
        
    def generate_financial_report(self, start_date: str, end_date: str) -> str:
        """Generate financial analysis report"""
        self.logger.info(f"Generating financial report for {start_date} to {end_date}")
        
        report_path = os.path.join(self.output_dir, f'financial_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf')
        
        with PdfPages(report_path) as pdf:
            # Revenue breakdown
            self._create_revenue_breakdown(pdf, start_date, end_date)
            
            # Payment method analysis
            self._create_payment_analysis(pdf, start_date, end_date)
            
            # Pricing optimization
            self._create_pricing_analysis(pdf, start_date, end_date)
            
            # Profitability analysis
            self._create_profitability_analysis(pdf, start_date, end_date)
            
        return report_path
        
    def generate_customer_analytics(self, start_date: str, end_date: str) -> str:
        """Generate customer behavior analytics report"""
        self.logger.info(f"Generating customer analytics for {start_date} to {end_date}")
        
        report_path = os.path.join(self.output_dir, f'customer_analytics_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf')
        
        with PdfPages(report_path) as pdf:
            # Customer segmentation
            self._create_customer_segmentation(pdf, start_date, end_date)
            
            # Usage patterns
            self._create_customer_usage_patterns(pdf, start_date, end_date)
            
            # Loyalty analysis
            self._create_loyalty_analysis(pdf, start_date, end_date)
            
            # Satisfaction trends
            self._create_satisfaction_trends(pdf, start_date, end_date)
            
        return report_path
        
    def generate_interactive_dashboard(self, start_date: str, end_date: str) -> str:
        """Generate interactive HTML dashboard"""
        self.logger.info(f"Generating interactive dashboard for {start_date} to {end_date}")
        
        with self.get_db_connection() as conn:
            # Get data for dashboard
            revenue_data = self._get_revenue_trend_data(conn, start_date, end_date)
            occupancy_data = self._get_occupancy_data(conn, start_date, end_date)
            equipment_data = self._get_equipment_status_data(conn)
            
        # Create dashboard
        dashboard_path = os.path.join(self.output_dir, f'dashboard_{datetime.now().strftime("%Y%m%d_%H%M%S")}.html')
        
        # Create subplots
        fig = make_subplots(
            rows=3, cols=2,
            subplot_titles=('Revenue Trend', 'Occupancy Rate', 
                          'Payment Methods', 'Equipment Status',
                          'Peak Hours', 'Customer Satisfaction'),
            specs=[[{"secondary_y": True}, {"secondary_y": True}],
                   [{"type": "pie"}, {"type": "bar"}],
                   [{"type": "heatmap"}, {"type": "scatter"}]]
        )
        
        # Revenue trend
        fig.add_trace(
            go.Scatter(x=revenue_data['date'], y=revenue_data['revenue'],
                      name='Daily Revenue', line=dict(color='blue')),
            row=1, col=1
        )
        
        # Occupancy rate
        fig.add_trace(
            go.Scatter(x=occupancy_data['date'], y=occupancy_data['occupancy'],
                      name='Occupancy %', line=dict(color='green')),
            row=1, col=2
        )
        
        # Update layout
        fig.update_layout(
            title_text="Car Parking System Analytics Dashboard",
            showlegend=True,
            height=900
        )
        
        # Save dashboard
        pyo.plot(fig, filename=dashboard_path, auto_open=False)
        
        return dashboard_path
        
    def generate_predictive_analysis(self, start_date: str, end_date: str) -> str:
        """Generate predictive analysis report"""
        self.logger.info(f"Generating predictive analysis for {start_date} to {end_date}")
        
        report_path = os.path.join(self.output_dir, f'predictive_analysis_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf')
        
        with PdfPages(report_path) as pdf:
            # Demand forecasting
            self._create_demand_forecast(pdf, start_date, end_date)
            
            # Revenue prediction
            self._create_revenue_forecast(pdf, start_date, end_date)
            
            # Maintenance prediction
            self._create_maintenance_prediction(pdf, start_date, end_date)
            
            # Capacity planning
            self._create_capacity_planning(pdf, start_date, end_date)
            
        return report_path
        
    def _get_total_transactions(self, conn: sqlite3.Connection, start_date: str, end_date: str) -> int:
        """Get total number of transactions"""
        cursor = conn.execute("""
            SELECT COUNT(*) as total
            FROM transactions 
            WHERE transaction_date BETWEEN ? AND ?
        """, (start_date, end_date))
        return cursor.fetchone()['total']
        
    def _get_total_revenue(self, conn: sqlite3.Connection, start_date: str, end_date: str) -> float:
        """Get total revenue"""
        cursor = conn.execute("""
            SELECT SUM(amount) as total
            FROM transactions 
            WHERE transaction_date BETWEEN ? AND ? AND status = 'completed'
        """, (start_date, end_date))
        result = cursor.fetchone()['total']
        return result if result else 0.0
        
    def _get_average_occupancy(self, conn: sqlite3.Connection, start_date: str, end_date: str) -> float:
        """Get average occupancy rate"""
        cursor = conn.execute("""
            SELECT AVG(occupied_spaces * 100.0 / total_spaces) as avg_occupancy
            FROM system_statistics 
            WHERE timestamp BETWEEN ? AND ?
        """, (start_date, end_date))
        result = cursor.fetchone()['avg_occupancy']
        return result if result else 0.0
        
    def _get_customer_satisfaction(self, conn: sqlite3.Connection, start_date: str, end_date: str) -> float:
        """Get customer satisfaction score"""
        # This would typically come from feedback/survey data
        # For now, calculate based on system performance metrics
        cursor = conn.execute("""
            SELECT AVG(
                CASE 
                    WHEN response_time <= 30 THEN 5.0
                    WHEN response_time <= 60 THEN 4.0
                    WHEN response_time <= 120 THEN 3.0
                    WHEN response_time <= 300 THEN 2.0
                    ELSE 1.0
                END
            ) as satisfaction
            FROM system_events 
            WHERE timestamp BETWEEN ? AND ? AND event_type = 'transaction_completed'
        """, (start_date, end_date))
        result = cursor.fetchone()['satisfaction']
        return result if result else 4.2  # Default satisfaction score
        
    def _get_peak_hours(self, conn: sqlite3.Connection, start_date: str, end_date: str) -> List[Dict]:
        """Get peak usage hours"""
        cursor = conn.execute("""
            SELECT 
                strftime('%H', transaction_date) as hour,
                COUNT(*) as transaction_count
            FROM transactions 
            WHERE transaction_date BETWEEN ? AND ?
            GROUP BY hour
            ORDER BY transaction_count DESC
            LIMIT 5
        """, (start_date, end_date))
        return [dict(row) for row in cursor.fetchall()]
        
    def _get_busiest_days(self, conn: sqlite3.Connection, start_date: str, end_date: str) -> List[Dict]:
        """Get busiest days"""
        cursor = conn.execute("""
            SELECT 
                strftime('%w', transaction_date) as day_of_week,
                COUNT(*) as transaction_count
            FROM transactions 
            WHERE transaction_date BETWEEN ? AND ?
            GROUP BY day_of_week
            ORDER BY transaction_count DESC
        """, (start_date, end_date))
        
        day_names = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
        result = []
        for row in cursor.fetchall():
            result.append({
                'day': day_names[int(row['day_of_week'])],
                'count': row['transaction_count']
            })
        return result
        
    def _create_kpi_dashboard(self, pdf: PdfPages, kpis: Dict):
        """Create KPI dashboard page"""
        fig, axes = plt.subplots(2, 2, figsize=self.report_config['page_size'])
        fig.suptitle('Key Performance Indicators', fontsize=self.report_config['title_size'], fontweight='bold')
        
        colors = list(self.report_config['colors'].values())
        
        for i, (kpi, value) in enumerate(kpis.items()):
            row, col = i // 2, i % 2
            ax = axes[row, col]
            
            # Create KPI box
            ax.text(0.5, 0.6, str(value), fontsize=24, fontweight='bold', 
                   ha='center', va='center', transform=ax.transAxes, color=colors[i])
            ax.text(0.5, 0.3, kpi, fontsize=14, ha='center', va='center', 
                   transform=ax.transAxes)
            
            # Style the box
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
            ax.add_patch(plt.Rectangle((0.1, 0.1), 0.8, 0.8, fill=False, 
                                     edgecolor=colors[i], linewidth=3))
            ax.set_xticks([])
            ax.set_yticks([])
            
        plt.tight_layout()
        pdf.savefig(fig, bbox_inches='tight')
        plt.close()
        
    def _create_usage_patterns_report(self, pdf: PdfPages, peak_hours: List[Dict], busiest_days: List[Dict]):
        """Create usage patterns analysis"""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=self.report_config['page_size'])
        fig.suptitle('Usage Patterns Analysis', fontsize=self.report_config['title_size'], fontweight='bold')
        
        # Peak hours chart
        hours = [f"{h['hour']}:00" for h in peak_hours]
        counts = [h['transaction_count'] for h in peak_hours]
        
        ax1.bar(hours, counts, color=self.report_config['colors']['primary'])
        ax1.set_title('Peak Usage Hours')
        ax1.set_xlabel('Hour of Day')
        ax1.set_ylabel('Number of Transactions')
        ax1.tick_params(axis='x', rotation=45)
        
        # Busiest days chart
        days = [d['day'] for d in busiest_days]
        day_counts = [d['count'] for d in busiest_days]
        
        ax2.pie(day_counts, labels=days, autopct='%1.1f%%', 
               colors=sns.color_palette("husl", len(days)))
        ax2.set_title('Transaction Distribution by Day')
        
        plt.tight_layout()
        pdf.savefig(fig, bbox_inches='tight')
        plt.close()
        
    def _create_revenue_analysis(self, pdf: PdfPages, start_date: str, end_date: str):
        """Create revenue analysis page"""
        with self.get_db_connection() as conn:
            # Daily revenue trend
            cursor = conn.execute("""
                SELECT 
                    DATE(transaction_date) as date,
                    SUM(amount) as daily_revenue
                FROM transactions 
                WHERE transaction_date BETWEEN ? AND ? AND status = 'completed'
                GROUP BY DATE(transaction_date)
                ORDER BY date
            """, (start_date, end_date))
            
            revenue_data = [dict(row) for row in cursor.fetchall()]
            
        if revenue_data:
            dates = [datetime.strptime(r['date'], '%Y-%m-%d') for r in revenue_data]
            revenues = [r['daily_revenue'] for r in revenue_data]
            
            fig, ax = plt.subplots(figsize=self.report_config['page_size'])
            fig.suptitle('Revenue Analysis', fontsize=self.report_config['title_size'], fontweight='bold')
            
            ax.plot(dates, revenues, marker='o', linewidth=2, markersize=4,
                   color=self.report_config['colors']['success'])
            ax.set_title('Daily Revenue Trend')
            ax.set_xlabel('Date')
            ax.set_ylabel('Revenue ($)')
            ax.grid(True, alpha=0.3)
            
            # Add trend line
            if len(dates) > 1:
                z = np.polyfit(range(len(dates)), revenues, 1)
                p = np.poly1d(z)
                ax.plot(dates, p(range(len(dates))), "--", alpha=0.8, 
                       color=self.report_config['colors']['warning'])
            
            plt.xticks(rotation=45)
            plt.tight_layout()
            pdf.savefig(fig, bbox_inches='tight')
            plt.close()
            
    def _create_efficiency_analysis(self, pdf: PdfPages, start_date: str, end_date: str):
        """Create operational efficiency analysis"""
        with self.get_db_connection() as conn:
            # Get efficiency metrics
            cursor = conn.execute("""
                SELECT 
                    AVG(response_time) as avg_response_time,
                    COUNT(CASE WHEN severity = 'error' THEN 1 END) as error_count,
                    COUNT(*) as total_events
                FROM system_events 
                WHERE timestamp BETWEEN ? AND ?
            """, (start_date, end_date))
            
            metrics = dict(cursor.fetchone())
            
        fig, axes = plt.subplots(2, 2, figsize=self.report_config['page_size'])
        fig.suptitle('Operational Efficiency Analysis', fontsize=self.report_config['title_size'], fontweight='bold')
        
        # Response time gauge
        ax = axes[0, 0]
        response_time = metrics['avg_response_time'] or 0
        colors = ['green' if response_time < 30 else 'yellow' if response_time < 60 else 'red']
        ax.pie([response_time, max(0, 120 - response_time)], colors=colors + ['lightgray'], 
               startangle=90, counterclock=False)
        ax.set_title(f'Avg Response Time: {response_time:.1f}s')
        
        # Error rate
        ax = axes[0, 1]
        error_rate = (metrics['error_count'] / max(metrics['total_events'], 1)) * 100
        ax.bar(['Error Rate'], [error_rate], color=self.report_config['colors']['danger'])
        ax.set_title('System Error Rate (%)')
        ax.set_ylabel('Percentage')
        
        # System uptime (simulated)
        ax = axes[1, 0]
        uptime = max(95, 100 - error_rate)  # Simulate uptime based on error rate
        ax.pie([uptime, 100 - uptime], labels=['Uptime', 'Downtime'], 
               colors=[self.report_config['colors']['success'], self.report_config['colors']['danger']])
        ax.set_title(f'System Uptime: {uptime:.1f}%')
        
        # Throughput
        ax = axes[1, 1]
        throughput = metrics['total_events'] / 24  # Events per hour (assuming 24 hour period)
        ax.bar(['Throughput'], [throughput], color=self.report_config['colors']['secondary'])
        ax.set_title('Average Throughput (events/hour)')
        ax.set_ylabel('Events per Hour')
        
        plt.tight_layout()
        pdf.savefig(fig, bbox_inches='tight')
        plt.close()
        
    def _create_equipment_performance_report(self, pdf: PdfPages, start_date: str, end_date: str):
        """Create equipment performance analysis"""
        # This would typically analyze elevator performance, sensor data, etc.
        # For now, create a simulated analysis
        
        fig, axes = plt.subplots(2, 2, figsize=self.report_config['page_size'])
        fig.suptitle('Equipment Performance Analysis', fontsize=self.report_config['title_size'], fontweight='bold')
        
        # Elevator efficiency
        elevators = ['Elevator 1', 'Elevator 2', 'Elevator 3']
        efficiency = [95.2, 92.8, 97.1]  # Simulated data
        
        axes[0, 0].bar(elevators, efficiency, color=self.report_config['colors']['primary'])
        axes[0, 0].set_title('Elevator Efficiency (%)')
        axes[0, 0].set_ylabel('Efficiency %')
        axes[0, 0].set_ylim(80, 100)
        
        # Sensor status
        sensors = ['Entry Sensors', 'Position Sensors', 'Safety Sensors', 'Payment Sensors']
        status = [98, 96, 99, 94]  # Simulated operational status
        
        axes[0, 1].bar(sensors, status, color=self.report_config['colors']['success'])
        axes[0, 1].set_title('Sensor Operational Status (%)')
        axes[0, 1].set_ylabel('Operational %')
        axes[0, 1].tick_params(axis='x', rotation=45)
        
        # Maintenance alerts
        maintenance_data = ['Elevator 1', 'Platform A', 'Sensor Bank 2']
        alert_counts = [2, 1, 3]
        
        axes[1, 0].bar(maintenance_data, alert_counts, color=self.report_config['colors']['warning'])
        axes[1, 0].set_title('Maintenance Alerts')
        axes[1, 0].set_ylabel('Number of Alerts')
        
        # Power consumption
        days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        power = [850, 920, 875, 890, 910, 800, 750]  # kWh simulated
        
        axes[1, 1].plot(days, power, marker='o', color=self.report_config['colors']['secondary'])
        axes[1, 1].set_title('Daily Power Consumption')
        axes[1, 1].set_ylabel('Power (kWh)')
        
        plt.tight_layout()
        pdf.savefig(fig, bbox_inches='tight')
        plt.close()
        
    def _get_revenue_trend_data(self, conn: sqlite3.Connection, start_date: str, end_date: str) -> Dict:
        """Get revenue trend data for dashboard"""
        cursor = conn.execute("""
            SELECT 
                DATE(transaction_date) as date,
                SUM(amount) as revenue
            FROM transactions 
            WHERE transaction_date BETWEEN ? AND ? AND status = 'completed'
            GROUP BY DATE(transaction_date)
            ORDER BY date
        """, (start_date, end_date))
        
        data = [dict(row) for row in cursor.fetchall()]
        return {
            'date': [d['date'] for d in data],
            'revenue': [d['revenue'] for d in data]
        }
        
    def _get_occupancy_data(self, conn: sqlite3.Connection, start_date: str, end_date: str) -> Dict:
        """Get occupancy data for dashboard"""
        cursor = conn.execute("""
            SELECT 
                DATE(timestamp) as date,
                AVG(occupied_spaces * 100.0 / total_spaces) as occupancy
            FROM system_statistics 
            WHERE timestamp BETWEEN ? AND ?
            GROUP BY DATE(timestamp)
            ORDER BY date
        """, (start_date, end_date))
        
        data = [dict(row) for row in cursor.fetchall()]
        return {
            'date': [d['date'] for d in data],
            'occupancy': [d['occupancy'] for d in data]
        }
        
    def _get_equipment_status_data(self, conn: sqlite3.Connection) -> Dict:
        """Get current equipment status"""
        # Simulated equipment status data
        return {
            'elevators': {'operational': 3, 'maintenance': 0, 'offline': 0},
            'sensors': {'operational': 145, 'maintenance': 3, 'offline': 2},
            'platforms': {'operational': 18, 'maintenance': 1, 'offline': 1}
        }
        
    # Additional helper methods would be implemented here for other report types
    # ... (continuing with other analysis methods)


def main():
    """Main function for testing report generation"""
    import sys
    
    db_path = "data/parking_system.db"
    output_dir = "reports"
    
    # Create report generator
    reporter = AdvancedReportGenerator(db_path, output_dir)
    
    # Generate sample reports
    start_date = "2024-01-01"
    end_date = "2024-01-31"
    
    try:
        # Generate executive summary
        exec_report = reporter.generate_executive_summary(start_date, end_date)
        print(f"Executive summary generated: {exec_report}")
        
        # Generate operational report
        ops_report = reporter.generate_operational_report(start_date, end_date)
        print(f"Operational report generated: {ops_report}")
        
        # Generate interactive dashboard
        dashboard = reporter.generate_interactive_dashboard(start_date, end_date)
        print(f"Interactive dashboard generated: {dashboard}")
        
    except Exception as e:
        print(f"Error generating reports: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
