# Lab Requirements - GTI 700

## Course Information

**Course**: GTI 700 - Distributed Systems  
**Lab**: Laboratory 1  
**Team**: Équipe 5  
**Academic Session**: Fall 2024  

## Team Members

- **Chartier, Guyllaume**
- **Djelloud, Mohamed-Amine**
- **Kandiah Ariyanayagam, Thanushai**

## Objective

Design and implement a distributed IoT monitoring system using two Raspberry Pi devices to demonstrate fundamental concepts of distributed systems, including:

- Inter-device communication
- RESTful API design
- Real-time data processing
- Web-based user interfaces
- Hardware interfacing

## Technical Requirements

### Hardware Requirements

#### Raspberry Pi Configuration
- **2x Raspberry Pi** (Model 3B+ or 4)
- **1x DHT11 Temperature/Humidity Sensor**
- **Connecting Wires** (minimum 3)
- **Network Connectivity** (WiFi or Ethernet)

#### Sensor Specifications
- **Model**: DHT11
- **Measurement Range**: 
  - Temperature: 0-50°C (±2°C accuracy)
  - Humidity: 20-90% RH (±5% accuracy)
- **Interface**: Single digital pin communication
- **Power**: 3.3V or 5V

### Software Requirements

#### Programming Environment
- **Language**: JavaScript (Node.js)
- **Runtime**: Node.js v14 or higher
- **Framework**: Express.js for web services

#### Required Libraries
- **Backend**:
  - `express` - Web framework
  - `cors` - Cross-origin resource sharing
  - `node-dht-sensor` - DHT sensor interface
- **Frontend**:
  - `express` - Static file server
  - `chart.js` - Data visualization (CDN)

### System Architecture Requirements

#### Distributed Architecture
- **Raspberry Pi A**: Backend API server with sensor interface
- **Raspberry Pi B**: Frontend web interface server
- **Communication**: HTTP/REST API between devices

#### API Requirements
- **RESTful Design**: Resource-based URLs
- **JSON Responses**: Structured data format
- **Error Handling**: Appropriate HTTP status codes
- **CORS Support**: Cross-origin requests enabled

## Functional Requirements

### 1. Data Collection (Backend - Pi A)

#### Sensor Interface
- [x] Connect DHT11 sensor to GPIO pin 17
- [x] Read temperature and humidity every 3 seconds
- [x] Validate sensor readings
- [x] Store readings in memory with timestamps

#### Data Storage
- [x] Maintain history of 720 readings (1 hour)
- [x] Implement circular buffer for memory efficiency
- [x] Provide data persistence during operation
- [x] Handle data overflow gracefully

### 2. API Services (Backend - Pi A)

#### Temperature Endpoints
- [x] `GET /capteurs/temp` - Latest temperature
- [x] `GET /capteurs/temp/:n` - Last n readings
- [x] `GET /capteurs/temp/:n/moy` - Average of n readings

#### Humidity Endpoints
- [x] `GET /capteurs/hum` - Latest humidity
- [x] `GET /capteurs/hum/:n` - Last n readings
- [x] `GET /capteurs/hum/:n/moy` - Average of n readings

#### Error Handling
- [x] Invalid parameter handling (400 errors)
- [x] No data available handling (404 errors)
- [x] Sensor error handling
- [x] French error messages

### 3. Web Interface (Frontend - Pi B)

#### User Interface
- [x] Real-time dashboard displaying current values
- [x] Historical data tables (30 latest readings)
- [x] Average calculations display
- [x] Interactive charts for trend visualization

#### Real-time Updates
- [x] Automatic data refresh every 5 seconds
- [x] Chart updates with new data points
- [x] Error handling for network issues
- [x] User-friendly error messages

#### Responsive Design
- [x] Mobile and desktop compatibility
- [x] Professional styling with CSS
- [x] Two-column layout for temperature/humidity
- [x] Charts with proper scaling and legends

## Implementation Checklist

### Phase 1: Hardware Setup ✅
- [x] Raspberry Pi OS installation
- [x] Node.js installation
- [x] DHT11 sensor wiring
- [x] GPIO configuration
- [x] Network connectivity setup

### Phase 2: Backend Development ✅
- [x] Express.js server setup
- [x] Sensor module implementation
- [x] API endpoint development
- [x] Data storage management
- [x] Error handling implementation

### Phase 3: Frontend Development ✅
- [x] Static file server setup
- [x] HTML interface creation
- [x] CSS styling implementation
- [x] JavaScript API integration
- [x] Chart.js visualization

### Phase 4: Integration Testing ✅
- [x] Inter-device communication testing
- [x] API endpoint validation
- [x] Web interface functionality
- [x] Real-time data flow verification
- [x] Error scenario testing

### Phase 5: Documentation ✅
- [x] README with setup instructions
- [x] API documentation
- [x] Architecture documentation
- [x] Deployment guides
- [x] Code comments and structure

## Performance Criteria

### System Performance
- **API Response Time**: < 100ms for all endpoints
- **Data Collection**: Consistent 3-second intervals
- **Memory Usage**: < 100MB per Pi device
- **Uptime**: 99%+ during demonstration period

### User Experience
- **Interface Responsiveness**: < 1 second page loads
- **Real-time Updates**: 5-second refresh intervals
- **Data Accuracy**: Match DHT11 specifications
- **Error Recovery**: Graceful handling of network issues

## Academic Learning Objectives

### Distributed Systems Concepts
- [x] **Communication Protocols**: HTTP/REST API design
- [x] **Data Consistency**: Real-time synchronization
- [x] **Fault Tolerance**: Error handling and recovery
- [x] **Scalability**: Modular architecture design

### Practical Skills Development
- [x] **Hardware Integration**: GPIO and sensor interfacing
- [x] **Web Development**: Full-stack JavaScript application
- [x] **API Design**: RESTful service architecture
- [x] **System Integration**: Multi-device coordination

### Professional Practices
- [x] **Version Control**: Git repository management
- [x] **Documentation**: Comprehensive project documentation
- [x] **Code Quality**: Clean, readable, commented code
- [x] **Testing**: System validation and error handling

## Evaluation Criteria

### Technical Implementation (40%)
- System architecture and design quality
- Code organization and best practices
- API design and implementation
- Hardware integration success

### Functionality (30%)
- Complete feature implementation
- Real-time data collection and display
- Error handling and robustness
- User interface quality

### Documentation (20%)
- Setup and deployment instructions
- API documentation completeness
- Architecture explanation
- Code comments and clarity

### Presentation (10%)
- System demonstration
- Technical explanation ability
- Q&A response quality
- Professional presentation

## Deliverables

### Code Repository
- [x] Complete source code with proper structure
- [x] Installation and setup scripts
- [x] Configuration files
- [x] README with clear instructions

### Documentation Package
- [x] System architecture documentation
- [x] API reference documentation
- [x] Deployment guide
- [x] User manual

### Demo Materials
- [ ] Live system demonstration
- [ ] Performance metrics documentation
- [ ] Screenshots and videos
- [ ] Test results and validation

## Success Metrics

### Technical Success
- ✅ Both Pi devices operational
- ✅ Sensor data collection functional
- ✅ API endpoints responding correctly
- ✅ Web interface displaying real-time data
- ✅ Inter-device communication established

### Academic Success
- ✅ Distributed system concepts demonstrated
- ✅ RESTful API principles applied
- ✅ Hardware-software integration achieved
- ✅ Professional documentation standards met
- ✅ Team collaboration successful

## Challenges and Solutions

### Technical Challenges
- **GPIO Permission Issues**: Resolved with user group management
- **Network Configuration**: Addressed with proper IP configuration
- **Sensor Reliability**: Handled with error checking and validation
- **Cross-origin Requests**: Solved with CORS middleware

### Academic Challenges
- **Distributed System Complexity**: Managed with clear architecture separation
- **Real-time Requirements**: Met with efficient polling and caching
- **Documentation Standards**: Achieved with comprehensive writing
- **Team Coordination**: Successful with clear role definition

## Future Enhancements

### Technical Improvements
- Database persistence for historical data
- Multiple sensor support
- Authentication and security features
- Mobile application development

### Academic Extensions
- Load balancing implementation
- Microservices architecture
- Container deployment
- Cloud integration

---
**Submission Date**: December 2024  
**Repository**: https://github.com/shadowfeuer/Labo_1_GTI_700_Equipe_5  
**Status**: Complete ✅ 