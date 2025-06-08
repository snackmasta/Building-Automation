// WebSocket Communication Handler for Car Parking Vending System

class WebSocketHandler {
    constructor() {
        this.ws = null;
        this.reconnectAttempts = 0;
        this.maxReconnectAttempts = 10;
        this.reconnectInterval = 1000;
        this.heartbeatInterval = 30000;
        this.heartbeatTimer = null;
        this.messageQueue = [];
        this.listeners = new Map();
        
        this.setupHeartbeat();
    }

    connect(url = null) {
        const wsUrl = url || this.getWebSocketUrl();
        
        try {
            this.ws = new WebSocket(wsUrl);
            this.setupEventHandlers();
        } catch (error) {
            console.error('Failed to create WebSocket connection:', error);
            this.handleConnectionError();
        }
    }

    getWebSocketUrl() {
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        const host = window.location.host;
        return `${protocol}//${host}/ws/parking-system`;
    }

    setupEventHandlers() {
        this.ws.onopen = (event) => {
            console.log('WebSocket connection established');
            this.reconnectAttempts = 0;
            this.emit('connection_open', event);
            this.startHeartbeat();
            this.processMessageQueue();
        };

        this.ws.onmessage = (event) => {
            this.handleMessage(event);
        };

        this.ws.onclose = (event) => {
            console.log('WebSocket connection closed:', event.code, event.reason);
            this.emit('connection_close', event);
            this.stopHeartbeat();
            this.handleReconnection();
        };

        this.ws.onerror = (error) => {
            console.error('WebSocket error:', error);
            this.emit('connection_error', error);
            this.handleConnectionError();
        };
    }

    handleMessage(event) {
        try {
            const data = JSON.parse(event.data);
            
            // Handle heartbeat responses
            if (data.type === 'heartbeat_response') {
                this.emit('heartbeat_received', data);
                return;
            }

            // Emit specific message type events
            this.emit(data.type, data);
            this.emit('message', data);

            // Log received message for debugging
            console.log('Received WebSocket message:', data.type);
        } catch (error) {
            console.error('Error parsing WebSocket message:', error);
            this.emit('parse_error', { error, rawData: event.data });
        }
    }

    send(data) {
        const message = {
            ...data,
            timestamp: new Date().toISOString(),
            id: this.generateMessageId()
        };

        if (this.isConnected()) {
            try {
                this.ws.send(JSON.stringify(message));
                console.log('Sent WebSocket message:', message.type);
            } catch (error) {
                console.error('Error sending WebSocket message:', error);
                this.queueMessage(message);
            }
        } else {
            this.queueMessage(message);
        }
    }

    queueMessage(message) {
        this.messageQueue.push(message);
        console.log(`Message queued (${this.messageQueue.length} in queue):`, message.type);
    }

    processMessageQueue() {
        while (this.messageQueue.length > 0 && this.isConnected()) {
            const message = this.messageQueue.shift();
            try {
                this.ws.send(JSON.stringify(message));
                console.log('Sent queued message:', message.type);
            } catch (error) {
                console.error('Error sending queued message:', error);
                this.messageQueue.unshift(message); // Put it back at the front
                break;
            }
        }
    }

    isConnected() {
        return this.ws && this.ws.readyState === WebSocket.OPEN;
    }

    handleReconnection() {
        if (this.reconnectAttempts < this.maxReconnectAttempts) {
            this.reconnectAttempts++;
            const delay = Math.min(this.reconnectInterval * Math.pow(2, this.reconnectAttempts - 1), 30000);
            
            console.log(`Attempting to reconnect (${this.reconnectAttempts}/${this.maxReconnectAttempts}) in ${delay}ms`);
            
            setTimeout(() => {
                this.connect();
            }, delay);
        } else {
            console.error('Max reconnection attempts reached');
            this.emit('max_reconnect_attempts_reached');
        }
    }

    handleConnectionError() {
        // Implement connection error handling logic
        this.emit('connection_error_handled');
    }

    setupHeartbeat() {
        this.heartbeatTimer = setInterval(() => {
            if (this.isConnected()) {
                this.send({
                    type: 'heartbeat',
                    clientTime: Date.now()
                });
            }
        }, this.heartbeatInterval);
    }

    startHeartbeat() {
        if (this.heartbeatTimer) {
            clearInterval(this.heartbeatTimer);
        }
        this.setupHeartbeat();
    }

    stopHeartbeat() {
        if (this.heartbeatTimer) {
            clearInterval(this.heartbeatTimer);
            this.heartbeatTimer = null;
        }
    }

    // Event handling system
    on(event, callback) {
        if (!this.listeners.has(event)) {
            this.listeners.set(event, []);
        }
        this.listeners.get(event).push(callback);
    }

    off(event, callback) {
        if (this.listeners.has(event)) {
            const callbacks = this.listeners.get(event);
            const index = callbacks.indexOf(callback);
            if (index > -1) {
                callbacks.splice(index, 1);
            }
        }
    }

    emit(event, data = null) {
        if (this.listeners.has(event)) {
            this.listeners.get(event).forEach(callback => {
                try {
                    callback(data);
                } catch (error) {
                    console.error(`Error in event listener for ${event}:`, error);
                }
            });
        }
    }

    generateMessageId() {
        return `msg_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    }

    disconnect() {
        this.stopHeartbeat();
        if (this.ws) {
            this.ws.close(1000, 'Client disconnecting');
        }
    }

    // Specific message sending methods
    sendSystemCommand(command, parameters = {}) {
        this.send({
            type: 'system_command',
            command: command,
            parameters: parameters
        });
    }

    sendElevatorCommand(elevatorId, action, parameters = {}) {
        this.send({
            type: 'elevator_command',
            elevatorId: elevatorId,
            action: action,
            parameters: parameters
        });
    }

    requestSystemStatus() {
        this.send({
            type: 'request_system_status'
        });
    }

    requestParkingData() {
        this.send({
            type: 'request_parking_data'
        });
    }

    requestElevatorStatus() {
        this.send({
            type: 'request_elevator_status'
        });
    }

    requestOperationsData() {
        this.send({
            type: 'request_operations_data'
        });
    }

    requestMaintenanceData() {
        this.send({
            type: 'request_maintenance_data'
        });
    }

    requestAnalyticsData(timeRange = '24h') {
        this.send({
            type: 'request_analytics_data',
            timeRange: timeRange
        });
    }

    sendDiagnosticCommand(system, test = 'full') {
        this.send({
            type: 'diagnostic_command',
            system: system,
            test: test
        });
    }

    acknowledgeEmergency(emergencyId) {
        this.send({
            type: 'emergency_acknowledge',
            emergencyId: emergencyId
        });
    }

    sendMaintenanceUpdate(itemId, status, notes = '') {
        this.send({
            type: 'maintenance_update',
            itemId: itemId,
            status: status,
            notes: notes
        });
    }

    requestLogs(level = 'all', limit = 100) {
        this.send({
            type: 'request_logs',
            level: level,
            limit: limit
        });
    }

    // Configuration methods
    updateConfiguration(section, settings) {
        this.send({
            type: 'update_configuration',
            section: section,
            settings: settings
        });
    }

    requestConfiguration(section = 'all') {
        this.send({
            type: 'request_configuration',
            section: section
        });
    }

    // Real-time subscription methods
    subscribeToRealTimeData(dataTypes = ['parking', 'elevators', 'operations']) {
        this.send({
            type: 'subscribe_realtime',
            dataTypes: dataTypes,
            interval: 1000 // 1 second updates
        });
    }

    unsubscribeFromRealTimeData(dataTypes = []) {
        this.send({
            type: 'unsubscribe_realtime',
            dataTypes: dataTypes
        });
    }

    // File transfer methods
    requestFileUpload(fileName, fileType, fileSize) {
        this.send({
            type: 'request_file_upload',
            fileName: fileName,
            fileType: fileType,
            fileSize: fileSize
        });
    }

    requestFileDownload(fileName, fileType) {
        this.send({
            type: 'request_file_download',
            fileName: fileName,
            fileType: fileType
        });
    }

    // User authentication
    authenticate(username, password) {
        this.send({
            type: 'authenticate',
            username: username,
            password: password
        });
    }

    logout() {
        this.send({
            type: 'logout'
        });
    }

    // System backup and restore
    requestSystemBackup() {
        this.send({
            type: 'request_system_backup'
        });
    }

    requestSystemRestore(backupId) {
        this.send({
            type: 'request_system_restore',
            backupId: backupId
        });
    }

    // Performance monitoring
    requestPerformanceMetrics(timeRange = '1h') {
        this.send({
            type: 'request_performance_metrics',
            timeRange: timeRange
        });
    }

    // Error reporting
    reportClientError(error, context = {}) {
        this.send({
            type: 'client_error_report',
            error: {
                message: error.message,
                stack: error.stack,
                name: error.name
            },
            context: context,
            userAgent: navigator.userAgent,
            url: window.location.href
        });
    }
}

// Message type constants
const MESSAGE_TYPES = {
    // System control
    SYSTEM_COMMAND: 'system_command',
    SYSTEM_STATUS: 'system_status',
    
    // Elevator control
    ELEVATOR_COMMAND: 'elevator_command',
    ELEVATOR_STATUS: 'elevator_status',
    
    // Parking management
    PARKING_UPDATE: 'parking_update',
    PARKING_REQUEST: 'parking_request',
    
    // Operations
    OPERATION_START: 'operation_start',
    OPERATION_UPDATE: 'operation_update',
    OPERATION_COMPLETE: 'operation_complete',
    
    // Maintenance
    MAINTENANCE_ALERT: 'maintenance_alert',
    MAINTENANCE_UPDATE: 'maintenance_update',
    
    // Emergency
    EMERGENCY_ALERT: 'emergency_alert',
    EMERGENCY_ACKNOWLEDGE: 'emergency_acknowledge',
    
    // Analytics
    ANALYTICS_DATA: 'analytics_data',
    PERFORMANCE_METRICS: 'performance_metrics',
    
    // Diagnostics
    DIAGNOSTIC_COMMAND: 'diagnostic_command',
    DIAGNOSTIC_RESULT: 'diagnostic_result',
    
    // Logging
    LOG_ENTRY: 'log_entry',
    LOG_REQUEST: 'log_request',
    
    // Configuration
    CONFIG_UPDATE: 'config_update',
    CONFIG_REQUEST: 'config_request',
    
    // Real-time data
    REALTIME_DATA: 'realtime_data',
    SUBSCRIBE_REALTIME: 'subscribe_realtime',
    UNSUBSCRIBE_REALTIME: 'unsubscribe_realtime',
    
    // Authentication
    AUTHENTICATE: 'authenticate',
    AUTH_RESPONSE: 'auth_response',
    LOGOUT: 'logout',
    
    // File operations
    FILE_UPLOAD: 'file_upload',
    FILE_DOWNLOAD: 'file_download',
    
    // System management
    SYSTEM_BACKUP: 'system_backup',
    SYSTEM_RESTORE: 'system_restore',
    
    // Heartbeat
    HEARTBEAT: 'heartbeat',
    HEARTBEAT_RESPONSE: 'heartbeat_response',
    
    // Error handling
    ERROR: 'error',
    CLIENT_ERROR_REPORT: 'client_error_report'
};

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { WebSocketHandler, MESSAGE_TYPES };
} else {
    window.WebSocketHandler = WebSocketHandler;
    window.MESSAGE_TYPES = MESSAGE_TYPES;
}
