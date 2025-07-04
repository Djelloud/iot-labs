# System Architecture

## Overview

The IoT Web Monitoring System is a distributed application designed to collect, process, and visualize environmental data from DHT11 sensors. The system follows a microservices architecture with clear separation of concerns between data collection, API services, and user interface components.

## High-Level Architecture

```
┌─────────────────┐    HTTP API     ┌─────────────────┐
│   Raspberry Pi B │ ◄──────────────► │   Raspberry Pi A │
│   (Frontend)     │                 │   (Backend)      │
│                 │                 │                 │
│ ┌─────────────┐ │                 │ ┌─────────────┐ │
│ │Web Interface│ │                 │ │ REST API    │ │
│ │   Server    │ │                 │ │   Server    │ │
│ └─────────────┘ │                 │ └─────────────┘ │
│                 │                 │        │        │
│                 │                 │        │        │
│                 │                 │ ┌─────────────┐ │
│                 │                 │ │   Sensor    │ │
│                 │                 │ │   Module    │ │
│                 │                 │ └─────────────┘ │
│                 │                 │        │        │
└─────────────────┘                 │        │        │
                                    │ ┌─────────────┐ │
                                    │ │ DHT11 Sensor│ │
                                    │ │ (Hardware)  │ │
                                    │ └─────────────┘ │
                                    └─────────────────┘
```

## Component Architecture

### 1. Backend System (Raspberry Pi A)

#### 1.1 REST API Server (`server.js`)
- **Framework**: Express.js
- **Port**: 8080
- **Responsibilities**:
  - Handle HTTP requests
  - Route API endpoints
  - Return formatted responses
  - CORS management
  - Error handling

#### 1.2 Sensor Module (`sensor_module.js`)
- **Purpose**: Hardware abstraction layer
- **Responsibilities**:
  - DHT11 sensor interface
  - Data collection scheduling
  - In-memory data storage
  - Statistical calculations
  - Data validation

#### 1.3 Hardware Interface (`temp_and_hum_recorder.js`)
- **Library**: node-dht-sensor
- **GPIO**: Pin 17
- **Responsibilities**:
  - Low-level sensor communication
  - Raw data reading
  - Hardware error handling

### 2. Frontend System (Raspberry Pi B)

#### 2.1 Web Server (`frontend-server.js`)
- **Framework**: Express.js
- **Port**: 8889
- **Responsibilities**:
  - Serve static files
  - Handle web requests
  - Route management

#### 2.2 Web Interface (`public/`)
- **Technologies**: HTML5, CSS3, JavaScript (ES6)
- **Visualization**: Chart.js
- **Responsibilities**:
  - User interface rendering
  - Real-time data fetching
  - Data visualization
  - Responsive design

## Data Flow

### 1. Data Collection Flow
```
DHT11 Sensor → GPIO Pin 17 → node-dht-sensor → Sensor Module → In-Memory Storage
```

### 2. API Request Flow
```
Web Interface → HTTP Request → Express Server → Sensor Module → JSON Response
```

### 3. Real-time Update Flow
```
JavaScript Timer → API Request → Data Processing → Chart Update → UI Refresh
```

## Data Models

### 1. Sensor Reading
```javascript
{
  timestamp: "2024-12-03 15:30:27",  // ISO format string
  temperature: 23.5,                // Float, 1 decimal place
  humidity: 65.2                    // Float, 1 decimal place
}
```

### 2. History Entry
```javascript
[
  "2024-12-03 15:30:27",  // Timestamp
  23.5                    // Value (temperature or humidity)
]
```

### 3. API Response (History)
```javascript
[
  ["2024-12-03 15:30:24", 23.5],
  ["2024-12-03 15:30:27", 23.6],
  ["2024-12-03 15:30:30", 23.4]
]
```

## Storage Architecture

### In-Memory Storage
- **Type**: JavaScript Arrays
- **Structure**: Circular buffer implementation
- **Capacity**: 720 readings per metric
- **Retention**: ~1 hour at 3-second intervals
- **Persistence**: None (data lost on restart)

### Storage Schema
```javascript
class SensorModule {
  temperatureHistory: Array<[string, number]>  // Max 720 entries
  humidityHistory: Array<[string, number]>     // Max 720 entries
}
```

## Network Architecture

### Development Setup
```
WiFi Network (192.168.1.x)
├── Raspberry Pi A: 192.168.1.100:8080 (Backend)
└── Raspberry Pi B: 192.168.1.101:8889 (Frontend)
```

### Production Setup
```
Internet
├── Router (Port Forwarding)
│   ├── 8080 → Pi A (Backend)
│   └── 8889 → Pi B (Frontend)
└── Local Network
    ├── Pi A: 192.168.1.100
    └── Pi B: 192.168.1.101
```

## API Architecture

### RESTful Design Principles
- **Resource-based URLs**: `/capteurs/temp`, `/capteurs/hum`
- **HTTP Methods**: GET only (read-only system)
- **Stateless**: No session management
- **JSON responses**: Structured data format

### Endpoint Structure
```
/capteurs/{metric}[/{count}[/moy]]

Where:
- metric: 'temp' or 'hum'
- count: Number of readings (optional)
- moy: Average calculation flag (optional)
```

## Security Architecture

### Development Security
- **Authentication**: None
- **CORS**: Enabled for all origins
- **HTTPS**: Not implemented
- **Input Validation**: Basic parameter checking

### Production Considerations
- **Authentication**: JWT or API keys recommended
- **CORS**: Restrict to specific origins
- **HTTPS**: SSL/TLS encryption
- **Rate Limiting**: Prevent API abuse
- **Input Sanitization**: Comprehensive validation

## Performance Architecture

### Backend Performance
- **Sensor Reading**: 3-second intervals
- **API Response Time**: < 10ms typical
- **Memory Usage**: ~50MB baseline
- **CPU Usage**: < 5% typical

### Frontend Performance
- **Update Frequency**: 5-second intervals
- **Chart Rendering**: Hardware-accelerated
- **Memory Usage**: ~100MB in browser
- **Network Bandwidth**: ~1KB per update

## Scalability Considerations

### Current Limitations
- Single sensor per backend
- In-memory storage only
- No horizontal scaling
- Manual configuration

### Scaling Strategies
1. **Database Integration**: PostgreSQL or InfluxDB
2. **Multiple Sensors**: Sensor array support
3. **Load Balancing**: Multiple backend instances
4. **Containerization**: Docker deployment
5. **Message Queues**: Redis or RabbitMQ

## Error Handling Architecture

### Backend Error Handling
```javascript
try {
  // Sensor reading
} catch (error) {
  console.error(`Sensor error: ${error.message}`);
  // Continue operation
}
```

### Frontend Error Handling
```javascript
fetch(apiUrl)
  .then(response => response.json())
  .catch(error => {
    console.error('API Error:', error);
    displayErrorMessage(error);
  });
```

## Monitoring and Logging

### Current Logging
- **Backend**: Console output with timestamps
- **Frontend**: Browser console
- **Sensor**: Reading validation logs

### Production Monitoring
- **Application Logs**: winston or bunyan
- **System Metrics**: Prometheus + Grafana
- **Error Tracking**: Sentry
- **Uptime Monitoring**: Pingdom or similar

## Technology Stack

### Backend Stack
```
┌─────────────────┐
│    Express.js   │  ← Web Framework
├─────────────────┤
│     Node.js     │  ← Runtime Environment
├─────────────────┤
│  node-dht-sensor│  ← Hardware Library
├─────────────────┤
│   Raspberry Pi  │  ← Hardware Platform
└─────────────────┘
```

### Frontend Stack
```
┌─────────────────┐
│   Chart.js      │  ← Visualization
├─────────────────┤
│  Vanilla JS     │  ← Client Logic
├─────────────────┤
│   HTML5/CSS3    │  ← UI Layer
├─────────────────┤
│   Express.js    │  ← Static Server
├─────────────────┤
│     Node.js     │  ← Runtime Environment
└─────────────────┘
```

## Deployment Architecture

### Current Deployment
- **Manual**: SSH and git clone
- **Dependencies**: npm install
- **Process Management**: Node.js directly

### Recommended Deployment
- **Process Manager**: PM2 or systemd
- **Reverse Proxy**: nginx
- **SSL Termination**: Let's Encrypt
- **Monitoring**: System health checks

## Future Enhancements

### Short-term Improvements
1. **Database persistence**
2. **Authentication system**
3. **Error recovery mechanisms**
4. **Configuration management**

### Long-term Vision
1. **Multi-sensor support**
2. **Machine learning analytics**
3. **Mobile application**
4. **Cloud integration**
5. **Real-time alerting**

---
*Architecture Version: 1.0*
*Last updated: December 2024* 