// Car Parking Vending System - Web HMI Main JavaScript

class ParkingSystemHMI {
    constructor() {
        this.ws = null;
        this.reconnectInterval = 5000;
        this.isConnected = false;
        this.systemData = {
            totalSpaces: 300,
            occupiedSpaces: 0,
            availableSpaces: 300,
            occupancyRate: 0,
            todayRevenue: 0,
            todayTransactions: 0,
            avgDuration: '0h 0m',
            elevators: [
                { id: 1, level: 1, status: 'Idle', load: 0, speed: 0 },
                { id: 2, level: 1, status: 'Idle', load: 0, speed: 0 },
                { id: 3, level: 1, status: 'Idle', load: 0, speed: 0 }
            ],
            parkingSpaces: [],
            operations: [],
            maintenanceItems: [],
            logs: []
        };
        
        this.initializeWebSocket();
        this.initializeUI();
        this.initializeCharts();
        this.startTimeUpdate();
        this.initializeParkingGrid();
    }

    // WebSocket Connection Management
    initializeWebSocket() {
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        const wsUrl = `${protocol}//${window.location.host}/ws`;
        
        try {
            this.ws = new WebSocket(wsUrl);
            
            this.ws.onopen = () => {
                console.log('WebSocket connected');
                this.isConnected = true;
                this.updateConnectionStatus(true);
                this.requestInitialData();
            };
            
            this.ws.onmessage = (event) => {
                this.handleWebSocketMessage(event);
            };
            
            this.ws.onclose = () => {
                console.log('WebSocket disconnected');
                this.isConnected = false;
                this.updateConnectionStatus(false);
                this.scheduleReconnect();
            };
            
            this.ws.onerror = (error) => {
                console.error('WebSocket error:', error);
                this.updateConnectionStatus(false);
            };
        } catch (error) {
            console.error('Failed to initialize WebSocket:', error);
            this.updateConnectionStatus(false);
            this.scheduleReconnect();
        }
    }

    scheduleReconnect() {
        setTimeout(() => {
            if (!this.isConnected) {
                console.log('Attempting to reconnect...');
                this.initializeWebSocket();
            }
        }, this.reconnectInterval);
    }

    updateConnectionStatus(connected) {
        const networkLight = document.getElementById('networkLight');
        if (connected) {
            networkLight.className = 'indicator-light';
            networkLight.style.backgroundColor = 'var(--success-color)';
        } else {
            networkLight.className = 'indicator-light danger';
            networkLight.style.backgroundColor = 'var(--danger-color)';
        }
    }

    sendWebSocketMessage(message) {
        if (this.ws && this.ws.readyState === WebSocket.OPEN) {
            this.ws.send(JSON.stringify(message));
        } else {
            console.warn('WebSocket not connected');
        }
    }

    handleWebSocketMessage(event) {
        try {
            const data = JSON.parse(event.data);
            
            switch (data.type) {
                case 'system_status':
                    this.updateSystemStatus(data.payload);
                    break;
                case 'parking_update':
                    this.updateParkingData(data.payload);
                    break;
                case 'elevator_status':
                    this.updateElevatorStatus(data.payload);
                    break;
                case 'operation_update':
                    this.updateOperations(data.payload);
                    break;
                case 'maintenance_alert':
                    this.handleMaintenanceAlert(data.payload);
                    break;
                case 'emergency_alert':
                    this.handleEmergencyAlert(data.payload);
                    break;
                case 'log_entry':
                    this.addLogEntry(data.payload);
                    break;
                default:
                    console.log('Unknown message type:', data.type);
            }
        } catch (error) {
            console.error('Error parsing WebSocket message:', error);
        }
    }

    requestInitialData() {
        this.sendWebSocketMessage({
            type: 'request_initial_data'
        });
    }

    // UI Initialization
    initializeUI() {
        this.initializeTabNavigation();
        this.initializeControls();
        this.initializeEventListeners();
        this.updateSystemIndicators();
    }

    initializeTabNavigation() {
        const tabButtons = document.querySelectorAll('.tab-button');
        const tabContents = document.querySelectorAll('.tab-content');

        tabButtons.forEach(button => {
            button.addEventListener('click', () => {
                const targetTab = button.getAttribute('data-tab');
                
                // Remove active class from all tabs and contents
                tabButtons.forEach(btn => btn.classList.remove('active'));
                tabContents.forEach(content => content.classList.remove('active'));
                
                // Add active class to clicked tab and corresponding content
                button.classList.add('active');
                document.getElementById(targetTab).classList.add('active');
                
                // Refresh charts when switching to analytics tab
                if (targetTab === 'analytics') {
                    this.refreshCharts();
                }
            });
        });
    }

    initializeControls() {
        // System control buttons
        document.getElementById('systemStart').addEventListener('click', () => {
            this.sendSystemCommand('start');
        });

        document.getElementById('systemStop').addEventListener('click', () => {
            this.sendSystemCommand('stop');
        });

        document.getElementById('emergencyStop').addEventListener('click', () => {
            this.sendSystemCommand('emergency_stop');
        });

        document.getElementById('systemReset').addEventListener('click', () => {
            this.sendSystemCommand('reset');
        });

        // Level selector
        document.getElementById('levelSelect').addEventListener('change', (e) => {
            this.updateParkingGridView(e.target.value);
        });

        // View controls
        document.getElementById('gridViewBtn').addEventListener('click', () => {
            this.switchParkingView('grid');
        });

        document.getElementById('3dViewBtn').addEventListener('click', () => {
            this.switchParkingView('3d');
        });

        // Log controls
        document.getElementById('clearLogs').addEventListener('click', () => {
            this.clearLogs();
        });

        document.getElementById('exportLogs').addEventListener('click', () => {
            this.exportLogs();
        });

        document.getElementById('logLevel').addEventListener('change', (e) => {
            this.filterLogs(e.target.value);
        });

        document.getElementById('logSearch').addEventListener('input', (e) => {
            this.searchLogs(e.target.value);
        });
    }

    initializeEventListeners() {
        // Window resize handler
        window.addEventListener('resize', () => {
            this.resizeCharts();
        });

        // Keyboard shortcuts
        document.addEventListener('keydown', (e) => {
            if (e.ctrlKey) {
                switch (e.key) {
                    case '1':
                        e.preventDefault();
                        this.switchTab('overview');
                        break;
                    case '2':
                        e.preventDefault();
                        this.switchTab('parking');
                        break;
                    case '3':
                        e.preventDefault();
                        this.switchTab('operations');
                        break;
                    case 'e':
                        e.preventDefault();
                        this.sendSystemCommand('emergency_stop');
                        break;
                }
            }
        });
    }

    // System Status Updates
    updateSystemStatus(data) {
        this.systemData = { ...this.systemData, ...data };
        
        // Update summary statistics
        document.getElementById('totalSpaces').textContent = this.systemData.totalSpaces;
        document.getElementById('occupiedSpaces').textContent = this.systemData.occupiedSpaces;
        document.getElementById('availableSpaces').textContent = this.systemData.availableSpaces;
        document.getElementById('occupancyRate').textContent = `${this.systemData.occupancyRate}%`;
        
        // Update revenue
        document.getElementById('todayRevenue').textContent = `$${this.systemData.todayRevenue.toFixed(2)}`;
        document.getElementById('todayTransactions').textContent = this.systemData.todayTransactions;
        document.getElementById('avgDuration').textContent = this.systemData.avgDuration;
        
        // Update system status indicators
        this.updateSystemIndicators();
        
        // Update charts
        this.updateOccupancyChart();
    }

    updateSystemIndicators() {
        const systemLight = document.getElementById('systemLight');
        const safetyLight = document.getElementById('safetyLight');
        
        // System status
        if (this.systemData.systemStatus === 'running') {
            systemLight.className = 'indicator-light';
        } else if (this.systemData.systemStatus === 'warning') {
            systemLight.className = 'indicator-light warning';
        } else {
            systemLight.className = 'indicator-light danger';
        }
        
        // Safety status
        if (this.systemData.safetyStatus === 'ok') {
            safetyLight.className = 'indicator-light';
        } else if (this.systemData.safetyStatus === 'warning') {
            safetyLight.className = 'indicator-light warning';
        } else {
            safetyLight.className = 'indicator-light danger';
        }
        
        // Update status text
        document.getElementById('plcStatus').textContent = this.systemData.plcStatus || 'Online';
        document.getElementById('paymentStatus').textContent = this.systemData.paymentStatus || 'Online';
        document.getElementById('safetySystemStatus').textContent = this.systemData.safetyStatus || 'OK';
    }

    // Parking Grid Management
    initializeParkingGrid() {
        const grid = document.getElementById('parkingGrid');
        grid.innerHTML = '';
        
        // Initialize parking spaces (300 total, 20 per level)
        for (let level = 1; level <= 15; level++) {
            for (let space = 1; space <= 20; space++) {
                const spaceId = `${level}-${space}`;
                const spaceElement = document.createElement('div');
                spaceElement.className = 'parking-space available';
                spaceElement.id = `space-${spaceId}`;
                spaceElement.textContent = `${level}.${space}`;
                spaceElement.title = `Level ${level}, Space ${space}`;
                
                spaceElement.addEventListener('click', () => {
                    this.showSpaceDetails(spaceId);
                });
                
                grid.appendChild(spaceElement);
                
                this.systemData.parkingSpaces.push({
                    id: spaceId,
                    level: level,
                    space: space,
                    status: 'available',
                    vehicle: null,
                    lastUpdated: new Date()
                });
            }
        }
    }

    updateParkingData(data) {
        if (data.spaces) {
            data.spaces.forEach(spaceData => {
                const spaceElement = document.getElementById(`space-${spaceData.id}`);
                if (spaceElement) {
                    spaceElement.className = `parking-space ${spaceData.status}`;
                    
                    // Update space data
                    const spaceIndex = this.systemData.parkingSpaces.findIndex(s => s.id === spaceData.id);
                    if (spaceIndex !== -1) {
                        this.systemData.parkingSpaces[spaceIndex] = {
                            ...this.systemData.parkingSpaces[spaceIndex],
                            ...spaceData
                        };
                    }
                }
            });
        }
    }

    updateParkingGridView(level) {
        const spaces = document.querySelectorAll('.parking-space');
        
        if (level === 'all') {
            spaces.forEach(space => space.style.display = 'flex');
        } else {
            spaces.forEach(space => {
                const spaceLevel = space.id.split('-')[1].split('.')[0];
                space.style.display = spaceLevel === level ? 'flex' : 'none';
            });
        }
    }

    switchParkingView(view) {
        const gridView = document.getElementById('parkingGrid');
        const view3D = document.getElementById('parking3D');
        const gridBtn = document.getElementById('gridViewBtn');
        const view3DBtn = document.getElementById('3dViewBtn');
        
        if (view === 'grid') {
            gridView.style.display = 'grid';
            view3D.style.display = 'none';
            gridBtn.classList.add('active');
            view3DBtn.classList.remove('active');
        } else {
            gridView.style.display = 'none';
            view3D.style.display = 'block';
            gridBtn.classList.remove('active');
            view3DBtn.classList.add('active');
            this.initialize3DView();
        }
    }

    showSpaceDetails(spaceId) {
        const spaceData = this.systemData.parkingSpaces.find(s => s.id === spaceId);
        if (spaceData) {
            const details = `
                Space: ${spaceData.id}
                Status: ${spaceData.status}
                Level: ${spaceData.level}
                ${spaceData.vehicle ? `Vehicle: ${spaceData.vehicle.plateNumber}` : ''}
                Last Updated: ${spaceData.lastUpdated.toLocaleString()}
            `;
            alert(details);
        }
    }

    // Elevator Management
    updateElevatorStatus(data) {
        if (data.elevators) {
            data.elevators.forEach(elevator => {
                const elevatorIndex = this.systemData.elevators.findIndex(e => e.id === elevator.id);
                if (elevatorIndex !== -1) {
                    this.systemData.elevators[elevatorIndex] = {
                        ...this.systemData.elevators[elevatorIndex],
                        ...elevator
                    };
                }
                
                // Update UI elements
                document.getElementById(`elevator${elevator.id}Level`).textContent = elevator.level;
                document.getElementById(`elevator${elevator.id}StatusText`).textContent = elevator.status;
                document.getElementById(`elevator${elevator.id}Load`).textContent = `${elevator.load} kg`;
                document.getElementById(`elevator${elevator.id}Speed`).textContent = `${elevator.speed} m/s`;
                
                // Update elevator car position
                const elevatorCar = document.getElementById(`elevator${elevator.id}Car`);
                const position = ((15 - elevator.level) / 14) * 180; // 180px is shaft height minus car height
                elevatorCar.style.top = `${position}px`;
                
                // Update status text
                document.getElementById(`elevator${elevator.id}Status`).textContent = elevator.status;
            });
        }
    }

    // Operations Management
    updateOperations(data) {
        const operationsList = document.getElementById('currentOperations');
        operationsList.innerHTML = '';
        
        if (data.operations) {
            this.systemData.operations = data.operations;
            
            data.operations.forEach(operation => {
                const operationElement = document.createElement('div');
                operationElement.className = `operation-item ${operation.status === 'active' ? 'active' : ''}`;
                operationElement.innerHTML = `
                    <div>
                        <strong>${operation.type}</strong><br>
                        Vehicle: ${operation.vehicleId}<br>
                        Status: ${operation.status}
                    </div>
                    <div>
                        Started: ${new Date(operation.startTime).toLocaleTimeString()}<br>
                        Progress: ${operation.progress}%
                    </div>
                `;
                operationsList.appendChild(operationElement);
            });
        }
        
        // Update queue statistics
        if (data.queue) {
            document.getElementById('entryQueue').textContent = data.queue.entry || 0;
            document.getElementById('exitQueue').textContent = data.queue.exit || 0;
            document.getElementById('avgWaitTime').textContent = `${data.queue.avgWaitTime || 0} min`;
        }
    }

    // System Commands
    sendSystemCommand(command) {
        this.sendWebSocketMessage({
            type: 'system_command',
            command: command,
            timestamp: new Date().toISOString()
        });
        
        this.addLogEntry({
            level: 'info',
            message: `System command sent: ${command}`,
            timestamp: new Date()
        });
    }

    controlElevator(elevatorId, action) {
        this.sendWebSocketMessage({
            type: 'elevator_command',
            elevatorId: elevatorId,
            action: action,
            timestamp: new Date().toISOString()
        });
        
        this.addLogEntry({
            level: 'info',
            message: `Elevator ${elevatorId} command: ${action}`,
            timestamp: new Date()
        });
    }

    // Maintenance and Diagnostics
    handleMaintenanceAlert(data) {
        this.addLogEntry({
            level: 'warning',
            message: `Maintenance alert: ${data.message}`,
            timestamp: new Date()
        });
        
        // Add to maintenance list
        this.updateMaintenanceList();
    }

    updateMaintenanceList() {
        const maintenanceList = document.getElementById('maintenanceList');
        maintenanceList.innerHTML = '';
        
        const maintenanceItems = [
            { task: 'Elevator 1 Monthly Inspection', dueDate: '2025-06-15', status: 'due-soon' },
            { task: 'Hydraulic System Service', dueDate: '2025-06-10', status: 'overdue' },
            { task: 'Safety System Test', dueDate: '2025-06-20', status: 'scheduled' },
            { task: 'Motor Lubrication', dueDate: '2025-06-25', status: 'scheduled' }
        ];
        
        maintenanceItems.forEach(item => {
            const itemElement = document.createElement('div');
            itemElement.className = `maintenance-item ${item.status}`;
            itemElement.innerHTML = `
                <div>
                    <strong>${item.task}</strong><br>
                    Due: ${item.dueDate}
                </div>
                <div class="maintenance-status">${item.status.replace('-', ' ')}</div>
            `;
            maintenanceList.appendChild(itemElement);
        });
    }

    runDiagnostics(system) {
        const resultsDiv = document.getElementById('diagnosticResults');
        resultsDiv.innerHTML = `<p>Running ${system} diagnostics...</p>`;
        
        this.sendWebSocketMessage({
            type: 'run_diagnostics',
            system: system,
            timestamp: new Date().toISOString()
        });
        
        // Simulate diagnostic results
        setTimeout(() => {
            const results = this.generateDiagnosticResults(system);
            resultsDiv.innerHTML = results;
        }, 3000);
    }

    generateDiagnosticResults(system) {
        const results = {
            motors: 'All motors operating within normal parameters. No issues detected.',
            elevators: 'Elevator systems functional. Minor calibration needed on Elevator 2.',
            safety: 'All safety systems operational. Emergency stops tested successfully.',
            communication: 'Network communication stable. All devices responding.'
        };
        
        return `<p><strong>${system.charAt(0).toUpperCase() + system.slice(1)} Diagnostics Complete:</strong></p><p>${results[system]}</p>`;
    }

    // Emergency Handling
    handleEmergencyAlert(data) {
        const modal = document.getElementById('emergencyModal');
        const message = document.getElementById('emergencyMessage');
        
        message.textContent = data.message;
        modal.style.display = 'block';
        
        // Add to logs
        this.addLogEntry({
            level: 'critical',
            message: `EMERGENCY: ${data.message}`,
            timestamp: new Date()
        });
        
        // Play alarm sound if available
        this.playAlarmSound();
    }

    acknowledgeEmergency() {
        const modal = document.getElementById('emergencyModal');
        modal.style.display = 'none';
        
        this.sendWebSocketMessage({
            type: 'emergency_acknowledge',
            timestamp: new Date().toISOString()
        });
        
        this.addLogEntry({
            level: 'info',
            message: 'Emergency alert acknowledged by operator',
            timestamp: new Date()
        });
    }

    playAlarmSound() {
        // Create audio element for alarm sound
        const audio = new Audio('data:audio/wav;base64,UklGRnoGAABXQVZFZm10IBAAAAABAAEAQB8AAEAfAAABAAgAZGF0YQoGAACBhYqFbF1fdJivrJBhNjVgodDbq2EcBj+a2/LDciUFLIHO8tiJNwgZaLvt559NEAxQp+PwtmMcBjiR1/LMeSwFJHfH8N2QQAoUXrTp66hVFApGn+DyvmMZBC2J0e/Cdykd');
        audio.play().catch(e => console.log('Could not play alarm sound:', e));
    }

    // Logging System
    addLogEntry(logData) {
        const logEntry = {
            timestamp: logData.timestamp || new Date(),
            level: logData.level || 'info',
            message: logData.message
        };
        
        this.systemData.logs.unshift(logEntry);
        
        // Keep only last 1000 log entries
        if (this.systemData.logs.length > 1000) {
            this.systemData.logs = this.systemData.logs.slice(0, 1000);
        }
        
        this.updateLogsDisplay();
    }

    updateLogsDisplay() {
        const logsDisplay = document.getElementById('logsDisplay');
        const logLevel = document.getElementById('logLevel').value;
        const searchTerm = document.getElementById('logSearch').value.toLowerCase();
        
        let filteredLogs = this.systemData.logs;
        
        // Filter by level
        if (logLevel !== 'all') {
            filteredLogs = filteredLogs.filter(log => log.level === logLevel);
        }
        
        // Filter by search term
        if (searchTerm) {
            filteredLogs = filteredLogs.filter(log => 
                log.message.toLowerCase().includes(searchTerm)
            );
        }
        
        logsDisplay.innerHTML = '';
        
        filteredLogs.slice(0, 100).forEach(log => {
            const logElement = document.createElement('div');
            logElement.className = `log-entry ${log.level}`;
            logElement.innerHTML = `
                <span class="log-timestamp">${log.timestamp.toLocaleString()}</span>
                <span class="log-level">[${log.level.toUpperCase()}]</span>
                <span class="log-message">${log.message}</span>
            `;
            logsDisplay.appendChild(logElement);
        });
    }

    clearLogs() {
        if (confirm('Are you sure you want to clear all logs?')) {
            this.systemData.logs = [];
            this.updateLogsDisplay();
        }
    }

    exportLogs() {
        const logsText = this.systemData.logs.map(log => 
            `${log.timestamp.toISOString()} [${log.level.toUpperCase()}] ${log.message}`
        ).join('\n');
        
        const blob = new Blob([logsText], { type: 'text/plain' });
        const url = URL.createObjectURL(blob);
        
        const a = document.createElement('a');
        a.href = url;
        a.download = `parking_system_logs_${new Date().toISOString().split('T')[0]}.txt`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        
        URL.revokeObjectURL(url);
    }

    filterLogs(level) {
        this.updateLogsDisplay();
    }

    searchLogs(term) {
        this.updateLogsDisplay();
    }

    // Utility Functions
    switchTab(tabName) {
        const tabButton = document.querySelector(`[data-tab="${tabName}"]`);
        if (tabButton) {
            tabButton.click();
        }
    }

    startTimeUpdate() {
        this.updateCurrentTime();
        setInterval(() => {
            this.updateCurrentTime();
        }, 1000);
    }

    updateCurrentTime() {
        const now = new Date();
        const timeString = now.toLocaleString();
        document.getElementById('currentTime').textContent = timeString;
    }

    // Initialize charts (placeholder - will be implemented in charts.js)
    initializeCharts() {
        // Charts will be initialized in charts.js
        console.log('Charts initialization placeholder');
    }

    updateOccupancyChart() {
        // Chart update will be implemented in charts.js
        console.log('Occupancy chart update placeholder');
    }

    refreshCharts() {
        // Chart refresh will be implemented in charts.js
        console.log('Charts refresh placeholder');
    }

    resizeCharts() {
        // Chart resize will be implemented in charts.js
        console.log('Charts resize placeholder');
    }

    initialize3DView() {
        // 3D view will be implemented in 3d-view.js
        console.log('3D view initialization placeholder');
    }
}

// Global functions for button handlers
function controlElevator(elevatorId, action) {
    if (window.parkingHMI) {
        window.parkingHMI.controlElevator(elevatorId, action);
    }
}

function runDiagnostics(system) {
    if (window.parkingHMI) {
        window.parkingHMI.runDiagnostics(system);
    }
}

function acknowledgeEmergency() {
    if (window.parkingHMI) {
        window.parkingHMI.acknowledgeEmergency();
    }
}

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.parkingHMI = new ParkingSystemHMI();
    
    // Add initial log entries
    window.parkingHMI.addLogEntry({
        level: 'info',
        message: 'Web HMI system initialized',
        timestamp: new Date()
    });
    
    window.parkingHMI.addLogEntry({
        level: 'info',
        message: 'Connecting to PLC system...',
        timestamp: new Date()
    });
    
    // Initialize maintenance list
    window.parkingHMI.updateMaintenanceList();
});
