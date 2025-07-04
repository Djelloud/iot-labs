# 📸 Demo Setup - Mock Mode

This guide helps you run the IoT monitoring system in mock mode for taking screenshots and demonstrations **without requiring Raspberry Pi hardware**.

## 🚀 Quick Start

### 1. Start the Backend (Mock Sensor Data)
```bash
cd iot-web-monitoring-system/backend
npm install
npm start
```

You should see:
```
Mock IoT server listening at http://localhost:8080
🔄 Mock sensor data generation active
📊 API endpoints ready for testing
📸 Ready for screenshots and demonstration
```

### 2. Start the Frontend (Web Interface)
Open a new terminal:
```bash
cd iot-web-monitoring-system/frontend
npm install
npm start
```

You should see:
```
Frontend server listening at http://localhost:8889
```

### 3. Open Web Interface
Navigate to: **http://localhost:8889/affichage**

## 📊 What You'll See

The mock system generates realistic data:
- **Temperature**: 18-28°C with natural variations
- **Humidity**: 45-85% with realistic fluctuations
- **Updates**: Every 3 seconds with new readings
- **History**: Pre-seeded with 30 initial readings
- **Charts**: Live updating graphs

## 📸 Perfect for Screenshots

The system provides:
- ✅ **Immediate data** - No waiting for sensor readings
- ✅ **Realistic values** - Professional-looking data
- ✅ **Live updates** - Dynamic charts and tables
- ✅ **Professional UI** - Clean, modern interface
- ✅ **Full functionality** - All features working

## 🔧 API Testing

You can test the API endpoints directly:

```bash
# Current readings
curl http://localhost:8080/capteurs/temp
curl http://localhost:8080/capteurs/hum

# Historical data (last 10 readings)
curl http://localhost:8080/capteurs/temp/10
curl http://localhost:8080/capteurs/hum/10

# Averages
curl http://localhost:8080/capteurs/temp/30/moy
curl http://localhost:8080/capteurs/hum/30/moy

# Debug stats
curl http://localhost:8080/debug/stats
```

## 📱 Screenshots Tips

For best screenshots:
1. **Wait 30 seconds** after startup for charts to populate
2. **Use full screen** for professional appearance
3. **Refresh page** if you want different data patterns
4. **Try different browser zoom levels** (90%, 100%, 110%)

## 🎯 Demo Scenarios

### Scenario 1: Normal Operation
- Shows stable readings with minor variations
- Perfect for showing system reliability

### Scenario 2: Environmental Changes
- Restart the backend to see different base values
- Shows system responsiveness to changes

### Scenario 3: Historical Analysis
- Let run for 5+ minutes to see trend development
- Shows long-term monitoring capabilities

## 🛠️ Troubleshooting

### Backend won't start
```bash
# Check if port is in use
netstat -ano | findstr :8080
# Kill process if needed
taskkill /PID [PID_NUMBER] /F
```

### Frontend shows "Error fetching data"
- Ensure backend is running first
- Check http://localhost:8080/capteurs/temp in browser
- Verify no firewall blocking localhost connections

### No data visible
- Wait 30 seconds for mock data generation
- Check browser console for errors
- Refresh the page

## 🔄 Switching to Real Hardware

When you get your Raspberry Pi:
1. Uncomment the `require("node-dht-sensor")` line in `sensor_module.js`
2. Comment out the mock data generation code
3. Install `node-dht-sensor` package
4. Update the frontend script URL to your Pi's IP

---
*Ready for professional screenshots and demonstrations!* 📸✨ 