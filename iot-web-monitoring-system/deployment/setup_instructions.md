# Setup Instructions

## Prerequisites

### Hardware Requirements
- 2x Raspberry Pi (Model 3B+ or 4 recommended)
- 1x DHT11 Temperature/Humidity sensor
- Jumper wires (3 minimum)
- Breadboard (optional)
- SD cards (16GB+ recommended)

### Software Requirements
- Raspberry Pi OS (Bullseye or newer)
- Node.js (v14 or higher)
- Git
- Internet connection for both Pi devices

## Network Configuration

### Option 1: Same Network Setup (Recommended for Development)
Both Raspberry Pi devices should be connected to the same WiFi network.

1. **Backend Pi (Pi A)**: Will run on port 8080
2. **Frontend Pi (Pi B)**: Will run on port 8889

### Option 2: Distributed Network Setup
For production-like setup with different networks, configure port forwarding on your router.

## Hardware Setup

### DHT11 Sensor Wiring to Raspberry Pi A
```
DHT11 Pin    → Raspberry Pi Pin
VCC (3.3V)   → Pin 1 (3.3V)
GND          → Pin 6 (Ground)
DATA         → Pin 11 (GPIO 17)
```

### Wiring Diagram
```
Raspberry Pi A          DHT11 Sensor
┌─────────────┐        ┌──────────────┐
│  Pin 1 (3.3V)│────────│ VCC          │
│             │        │              │
│  Pin 6 (GND)│────────│ GND          │
│             │        │              │
│ Pin 11(GPIO17)│──────│ DATA         │
│             │        │              │
└─────────────┘        └──────────────┘
```

## Software Installation

### 1. Raspberry Pi OS Setup (Both Pi devices)

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Node.js
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# Verify installation
node --version
npm --version

# Install Git
sudo apt install git -y
```

### 2. Project Setup

#### On Both Raspberry Pi devices:

```bash
# Clone the repository
git clone https://github.com/shadowfeuer/Labo_1_GTI_700_Equipe_5.git
cd Labo_1_GTI_700_Equipe_5/iot-web-monitoring-system
```

#### Backend Setup (Raspberry Pi A)

```bash
# Navigate to backend directory
cd backend/

# Install dependencies
npm install

# Install DHT sensor library (requires compilation)
npm install node-dht-sensor

# For Raspberry Pi, you might need to install additional dependencies
sudo apt install build-essential python3-dev

# Test the installation
npm start
```

If you encounter permission issues with GPIO:
```bash
# Add user to gpio group
sudo usermod -a -G gpio $USER

# Reboot to apply changes
sudo reboot
```

#### Frontend Setup (Raspberry Pi B)

```bash
# Navigate to frontend directory
cd frontend/

# Install dependencies
npm install

# Start the frontend server
npm start
```

## Configuration

### 1. Network Configuration

#### Backend Configuration (server.js)
If you need to change the backend IP or port:

```javascript
const port = 8080; // Change port if needed
app.listen(port, '0.0.0.0', () => { // Listen on all interfaces
    console.log(`Server running on http://0.0.0.0:${port}`);
});
```

#### Frontend Configuration (script.js)
Update the API base URL in `frontend/public/script.js`:

```javascript
// Replace with your Backend Pi's IP address
const API_BASE_URL = 'http://192.168.1.100:8080'; // Change IP as needed
```

### 2. Sensor Configuration

In `backend/sensor_module.js`, you can modify:

```javascript
this.sensor = { 
    name: "Capteur 1",
    type: 11,        // DHT11 = 11, DHT22 = 22
    pin: 17          // Change GPIO pin if needed
};

this.interval = 3000;        // Reading interval in ms
this.maxHistorySize = 720;   // Max readings to store
```

## Starting the System

### Manual Start

#### Terminal 1 - Backend (Raspberry Pi A):
```bash
cd backend/
npm start
```

#### Terminal 2 - Frontend (Raspberry Pi B):
```bash
cd frontend/
npm start
```

### Automatic Start (Systemd Services)

#### Backend Service (Raspberry Pi A)

Create service file:
```bash
sudo nano /etc/systemd/system/iot-backend.service
```

Service content:
```ini
[Unit]
Description=IoT Backend API Server
After=network.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/iot-web-monitoring-system/backend
ExecStart=/usr/bin/node server.js
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable iot-backend.service
sudo systemctl start iot-backend.service
```

#### Frontend Service (Raspberry Pi B)

Create service file:
```bash
sudo nano /etc/systemd/system/iot-frontend.service
```

Service content:
```ini
[Unit]
Description=IoT Frontend Web Server
After=network.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/iot-web-monitoring-system/frontend
ExecStart=/usr/bin/node frontend-server.js
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable iot-frontend.service
sudo systemctl start iot-frontend.service
```

## Testing

### 1. Hardware Test
```bash
# On Backend Pi, test sensor reading
cd backend/
node -e "
const sensor = require('node-dht-sensor');
const reading = sensor.read(11, 17);
console.log('Temperature:', reading.temperature, '°C');
console.log('Humidity:', reading.humidity, '%');
console.log('Valid:', reading.isValid);
"
```

### 2. API Test
```bash
# Test from any device on the network
curl http://[BACKEND_PI_IP]:8080/capteurs/temp
curl http://[BACKEND_PI_IP]:8080/capteurs/hum
```

### 3. Web Interface Test
Open a browser and navigate to:
```
http://[FRONTEND_PI_IP]:8889/affichage
```

## Troubleshooting

### Common Issues

#### "Permission denied" for GPIO
```bash
sudo usermod -a -G gpio $USER
sudo reboot
```

#### "Module not found: node-dht-sensor"
```bash
cd backend/
sudo npm install node-dht-sensor --unsafe-perm
```

#### "Address already in use"
```bash
# Kill process using the port
sudo lsof -ti:8080 | xargs sudo kill -9
sudo lsof -ti:8889 | xargs sudo kill -9
```

#### Network connectivity issues
```bash
# Check if services are running
sudo systemctl status iot-backend
sudo systemctl status iot-frontend

# Check network connectivity
ping [OTHER_PI_IP]

# Check firewall
sudo ufw status
```

### Logs

#### Check service logs:
```bash
# Backend logs
sudo journalctl -u iot-backend.service -f

# Frontend logs
sudo journalctl -u iot-frontend.service -f
```

#### Check manual execution logs:
```bash
cd backend/
npm start 2>&1 | tee backend.log
```

## Security Considerations

### Development Environment
- CORS is enabled for all origins
- No authentication required
- Services run on standard user account

### Production Deployment
For production use, consider:
- Implementing authentication
- Using HTTPS
- Restricting CORS origins
- Running services with limited privileges
- Setting up firewall rules

## Performance Optimization

### For Better Performance:
1. **Increase sensor reading interval** if needed
2. **Reduce history size** for lower memory usage
3. **Use PM2** for process management
4. **Enable gzip compression** in Express

### Example PM2 Setup:
```bash
# Install PM2
sudo npm install -g pm2

# Start services with PM2
pm2 start backend/server.js --name "iot-backend"
pm2 start frontend/frontend-server.js --name "iot-frontend"

# Save PM2 configuration
pm2 save
pm2 startup
```

---
*Last updated: December 2024* 