// Charts and Data Visualization for Car Parking Vending System

class ChartManager {
    constructor() {
        this.charts = new Map();
        this.chartOptions = {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'top',
                },
                title: {
                    display: true,
                    font: {
                        size: 16,
                        weight: 'bold'
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    grid: {
                        color: 'rgba(0, 0, 0, 0.1)'
                    }
                },
                x: {
                    grid: {
                        color: 'rgba(0, 0, 0, 0.1)'
                    }
                }
            }
        };
        
        this.colors = {
            primary: '#3498db',
            success: '#27ae60',
            warning: '#f39c12',
            danger: '#e74c3c',
            info: '#17a2b8',
            secondary: '#6c757d'
        };
        
        this.initializeCharts();
    }

    initializeCharts() {
        this.createOccupancyChart();
        this.createRevenueChart();
        this.createOccupancyPatternChart();
        this.createElevatorPerformanceChart();
        this.setupChartUpdateInterval();
    }

    createOccupancyChart() {
        const ctx = document.getElementById('occupancyChart').getContext('2d');
        
        this.charts.set('occupancy', new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: ['Occupied', 'Available', 'Reserved', 'Maintenance'],
                datasets: [{
                    data: [0, 300, 0, 0],
                    backgroundColor: [
                        this.colors.danger,
                        this.colors.success,
                        this.colors.warning,
                        this.colors.secondary
                    ],
                    borderWidth: 2,
                    borderColor: '#ffffff'
                }]
            },
            options: {
                ...this.chartOptions,
                plugins: {
                    ...this.chartOptions.plugins,
                    title: {
                        ...this.chartOptions.plugins.title,
                        text: 'Current Parking Occupancy'
                    },
                    legend: {
                        position: 'bottom'
                    }
                },
                cutout: '60%',
                animation: {
                    animateRotate: true,
                    animateScale: true
                }
            }
        }));
    }

    createRevenueChart() {
        const ctx = document.getElementById('revenueChart').getContext('2d');
        
        // Generate sample data for the last 7 days
        const labels = [];
        const revenueData = [];
        const transactionData = [];
        
        for (let i = 6; i >= 0; i--) {
            const date = new Date();
            date.setDate(date.getDate() - i);
            labels.push(date.toLocaleDateString('en-US', { weekday: 'short' }));
            revenueData.push(Math.random() * 1500 + 500); // Random revenue between $500-$2000
            transactionData.push(Math.floor(Math.random() * 100 + 50)); // Random transactions 50-150
        }
        
        this.charts.set('revenue', new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Revenue ($)',
                    data: revenueData,
                    borderColor: this.colors.success,
                    backgroundColor: this.colors.success + '20',
                    fill: true,
                    tension: 0.4,
                    yAxisID: 'y'
                }, {
                    label: 'Transactions',
                    data: transactionData,
                    borderColor: this.colors.primary,
                    backgroundColor: this.colors.primary + '20',
                    fill: false,
                    tension: 0.4,
                    yAxisID: 'y1'
                }]
            },
            options: {
                ...this.chartOptions,
                plugins: {
                    ...this.chartOptions.plugins,
                    title: {
                        ...this.chartOptions.plugins.title,
                        text: 'Revenue and Transaction Trends (7 Days)'
                    }
                },
                scales: {
                    y: {
                        type: 'linear',
                        display: true,
                        position: 'left',
                        title: {
                            display: true,
                            text: 'Revenue ($)'
                        }
                    },
                    y1: {
                        type: 'linear',
                        display: true,
                        position: 'right',
                        title: {
                            display: true,
                            text: 'Transactions'
                        },
                        grid: {
                            drawOnChartArea: false,
                        }
                    }
                }
            }
        }));
    }

    createOccupancyPatternChart() {
        const ctx = document.getElementById('occupancyPatternChart').getContext('2d');
        
        // Generate sample hourly occupancy data
        const hours = [];
        const occupancyData = [];
        
        for (let i = 0; i < 24; i++) {
            hours.push(`${i.toString().padStart(2, '0')}:00`);
            // Simulate occupancy pattern - higher during business hours
            let occupancy;
            if (i >= 7 && i <= 19) {
                occupancy = 60 + Math.random() * 35; // 60-95% during business hours
            } else {
                occupancy = 20 + Math.random() * 30; // 20-50% during off hours
            }
            occupancyData.push(Math.round(occupancy));
        }
        
        this.charts.set('occupancyPattern', new Chart(ctx, {
            type: 'bar',
            data: {
                labels: hours,
                datasets: [{
                    label: 'Occupancy %',
                    data: occupancyData,
                    backgroundColor: occupancyData.map(value => {
                        if (value >= 80) return this.colors.danger;
                        if (value >= 60) return this.colors.warning;
                        if (value >= 40) return this.colors.primary;
                        return this.colors.success;
                    }),
                    borderWidth: 1,
                    borderRadius: 4
                }]
            },
            options: {
                ...this.chartOptions,
                plugins: {
                    ...this.chartOptions.plugins,
                    title: {
                        ...this.chartOptions.plugins.title,
                        text: 'Hourly Occupancy Pattern (Today)'
                    },
                    legend: {
                        display: false
                    }
                },
                scales: {
                    y: {
                        ...this.chartOptions.scales.y,
                        max: 100,
                        title: {
                            display: true,
                            text: 'Occupancy Percentage'
                        }
                    },
                    x: {
                        title: {
                            display: true,
                            text: 'Hour of Day'
                        }
                    }
                }
            }
        }));
    }

    createElevatorPerformanceChart() {
        const ctx = document.getElementById('elevatorPerformanceChart').getContext('2d');
        
        // Generate sample performance data for 3 elevators
        const timeLabels = [];
        const elevator1Data = [];
        const elevator2Data = [];
        const elevator3Data = [];
        
        for (let i = 11; i >= 0; i--) {
            const time = new Date();
            time.setMinutes(time.getMinutes() - (i * 5));
            timeLabels.push(time.toLocaleTimeString('en-US', { 
                hour: '2-digit', 
                minute: '2-digit' 
            }));
            
            elevator1Data.push(Math.random() * 10 + 5); // 5-15 operations per 5min
            elevator2Data.push(Math.random() * 10 + 5);
            elevator3Data.push(Math.random() * 10 + 5);
        }
        
        this.charts.set('elevatorPerformance', new Chart(ctx, {
            type: 'line',
            data: {
                labels: timeLabels,
                datasets: [{
                    label: 'Elevator 1',
                    data: elevator1Data,
                    borderColor: this.colors.primary,
                    backgroundColor: this.colors.primary + '20',
                    fill: false,
                    tension: 0.4
                }, {
                    label: 'Elevator 2',
                    data: elevator2Data,
                    borderColor: this.colors.success,
                    backgroundColor: this.colors.success + '20',
                    fill: false,
                    tension: 0.4
                }, {
                    label: 'Elevator 3',
                    data: elevator3Data,
                    borderColor: this.colors.warning,
                    backgroundColor: this.colors.warning + '20',
                    fill: false,
                    tension: 0.4
                }]
            },
            options: {
                ...this.chartOptions,
                plugins: {
                    ...this.chartOptions.plugins,
                    title: {
                        ...this.chartOptions.plugins.title,
                        text: 'Elevator Performance (Operations per 5 minutes)'
                    }
                },
                scales: {
                    y: {
                        ...this.chartOptions.scales.y,
                        title: {
                            display: true,
                            text: 'Operations Count'
                        }
                    },
                    x: {
                        title: {
                            display: true,
                            text: 'Time'
                        }
                    }
                }
            }
        }));
    }

    updateOccupancyChart(data) {
        const chart = this.charts.get('occupancy');
        if (chart && data) {
            chart.data.datasets[0].data = [
                data.occupied || 0,
                data.available || 0,
                data.reserved || 0,
                data.maintenance || 0
            ];
            chart.update('none'); // No animation for real-time updates
        }
    }

    updateRevenueChart(data) {
        const chart = this.charts.get('revenue');
        if (chart && data) {
            // Add new data point and remove oldest if more than 7 days
            if (chart.data.labels.length >= 7) {
                chart.data.labels.shift();
                chart.data.datasets[0].data.shift();
                chart.data.datasets[1].data.shift();
            }
            
            const newLabel = new Date().toLocaleDateString('en-US', { weekday: 'short' });
            chart.data.labels.push(newLabel);
            chart.data.datasets[0].data.push(data.revenue || 0);
            chart.data.datasets[1].data.push(data.transactions || 0);
            
            chart.update();
        }
    }

    updateOccupancyPatternChart(hourlyData) {
        const chart = this.charts.get('occupancyPattern');
        if (chart && hourlyData) {
            chart.data.datasets[0].data = hourlyData;
            
            // Update colors based on occupancy levels
            chart.data.datasets[0].backgroundColor = hourlyData.map(value => {
                if (value >= 80) return this.colors.danger;
                if (value >= 60) return this.colors.warning;
                if (value >= 40) return this.colors.primary;
                return this.colors.success;
            });
            
            chart.update();
        }
    }

    updateElevatorPerformanceChart(elevatorData) {
        const chart = this.charts.get('elevatorPerformance');
        if (chart && elevatorData) {
            // Add new time point
            const newTime = new Date().toLocaleTimeString('en-US', { 
                hour: '2-digit', 
                minute: '2-digit' 
            });
            
            // Remove oldest data if more than 12 points (1 hour)
            if (chart.data.labels.length >= 12) {
                chart.data.labels.shift();
                chart.data.datasets.forEach(dataset => dataset.data.shift());
            }
            
            chart.data.labels.push(newTime);
            chart.data.datasets[0].data.push(elevatorData.elevator1 || 0);
            chart.data.datasets[1].data.push(elevatorData.elevator2 || 0);
            chart.data.datasets[2].data.push(elevatorData.elevator3 || 0);
            
            chart.update('none');
        }
    }

    createUsageHeatmap() {
        const heatmapContainer = document.getElementById('usageHeatmap');
        if (!heatmapContainer) return;
        
        heatmapContainer.innerHTML = '';
        
        // Create a simplified heatmap using HTML/CSS
        const heatmapData = this.generateHeatmapData();
        
        const heatmapDiv = document.createElement('div');
        heatmapDiv.className = 'heatmap-grid';
        heatmapDiv.style.cssText = `
            display: grid;
            grid-template-columns: repeat(24, 1fr);
            gap: 2px;
            padding: 20px;
        `;
        
        heatmapData.forEach((value, hour) => {
            const cell = document.createElement('div');
            cell.style.cssText = `
                aspect-ratio: 1;
                background-color: ${this.getHeatmapColor(value)};
                border-radius: 2px;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 10px;
                color: ${value > 0.5 ? 'white' : 'black'};
                cursor: pointer;
            `;
            cell.textContent = hour.toString().padStart(2, '0');
            cell.title = `Hour ${hour}: ${Math.round(value * 100)}% usage`;
            heatmapContainer.appendChild(cell);
        });
        
        // Add legend
        const legend = document.createElement('div');
        legend.style.cssText = `
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 10px;
            margin-top: 15px;
            font-size: 12px;
        `;
        
        legend.innerHTML = `
            <span>Low</span>
            <div style="width: 100px; height: 10px; background: linear-gradient(to right, 
                ${this.getHeatmapColor(0)}, 
                ${this.getHeatmapColor(0.3)}, 
                ${this.getHeatmapColor(0.6)}, 
                ${this.getHeatmapColor(1)}); 
                border-radius: 5px;"></div>
            <span>High</span>
        `;
        
        heatmapContainer.appendChild(legend);
    }

    generateHeatmapData() {
        const data = [];
        for (let hour = 0; hour < 24; hour++) {
            // Simulate usage pattern - higher during business hours
            let usage;
            if (hour >= 7 && hour <= 19) {
                usage = 0.4 + Math.random() * 0.6; // 40-100% during business hours
            } else {
                usage = Math.random() * 0.4; // 0-40% during off hours
            }
            data.push(usage);
        }
        return data;
    }

    getHeatmapColor(value) {
        // Create color gradient from green (low) to red (high)
        const red = Math.round(255 * value);
        const green = Math.round(255 * (1 - value));
        return `rgb(${red}, ${green}, 0)`;
    }

    setupChartUpdateInterval() {
        // Update charts every 30 seconds with simulated data
        setInterval(() => {
            this.updateChartsWithSimulatedData();
        }, 30000);
    }

    updateChartsWithSimulatedData() {
        // Simulate real-time data updates
        const occupancyData = {
            occupied: Math.floor(Math.random() * 150 + 50),
            available: 300 - Math.floor(Math.random() * 150 + 50),
            reserved: Math.floor(Math.random() * 20),
            maintenance: Math.floor(Math.random() * 10)
        };
        occupancyData.available = 300 - occupancyData.occupied - occupancyData.reserved - occupancyData.maintenance;
        
        this.updateOccupancyChart(occupancyData);
        
        // Update elevator performance
        const elevatorData = {
            elevator1: Math.random() * 10 + 5,
            elevator2: Math.random() * 10 + 5,
            elevator3: Math.random() * 10 + 5
        };
        
        this.updateElevatorPerformanceChart(elevatorData);
    }

    resizeCharts() {
        this.charts.forEach(chart => {
            chart.resize();
        });
    }

    refreshCharts() {
        this.charts.forEach(chart => {
            chart.update();
        });
        
        // Refresh heatmap
        this.createUsageHeatmap();
    }

    exportChart(chartName, format = 'png') {
        const chart = this.charts.get(chartName);
        if (chart) {
            const canvas = chart.canvas;
            const url = canvas.toDataURL(`image/${format}`);
            
            const link = document.createElement('a');
            link.download = `${chartName}_${new Date().toISOString().split('T')[0]}.${format}`;
            link.href = url;
            link.click();
        }
    }

    destroyCharts() {
        this.charts.forEach(chart => {
            chart.destroy();
        });
        this.charts.clear();
    }

    getChartData(chartName) {
        const chart = this.charts.get(chartName);
        return chart ? chart.data : null;
    }

    updateChartOptions(chartName, newOptions) {
        const chart = this.charts.get(chartName);
        if (chart) {
            Object.assign(chart.options, newOptions);
            chart.update();
        }
    }

    // Performance metrics visualization
    createPerformanceGauges() {
        const gaugeOptions = {
            type: 'doughnut',
            options: {
                cutout: '75%',
                plugins: {
                    legend: {
                        display: false
                    }
                },
                rotation: -90,
                circumference: 180
            }
        };
        
        // Throughput gauge
        const throughputCtx = document.createElement('canvas');
        throughputCtx.id = 'throughputGauge';
        
        // Efficiency gauge
        const efficiencyCtx = document.createElement('canvas');
        efficiencyCtx.id = 'efficiencyGauge';
        
        // Uptime gauge
        const uptimeCtx = document.createElement('canvas');
        uptimeCtx.id = 'uptimeGauge';
        
        // Implementation would continue with gauge creation...
    }

    // Real-time data streaming
    startRealTimeUpdates(websocket) {
        if (websocket) {
            websocket.on('parking_update', (data) => {
                this.updateOccupancyChart(data);
            });
            
            websocket.on('elevator_status', (data) => {
                this.updateElevatorPerformanceChart(data);
            });
            
            websocket.on('analytics_data', (data) => {
                if (data.hourlyOccupancy) {
                    this.updateOccupancyPatternChart(data.hourlyOccupancy);
                }
                if (data.revenue) {
                    this.updateRevenueChart(data.revenue);
                }
            });
        }
    }
}

// Initialize charts when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.chartManager = new ChartManager();
    
    // Initialize usage heatmap
    setTimeout(() => {
        window.chartManager.createUsageHeatmap();
    }, 1000);
    
    // Handle window resize
    window.addEventListener('resize', () => {
        window.chartManager.resizeCharts();
    });
});

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = ChartManager;
} else {
    window.ChartManager = ChartManager;
}
