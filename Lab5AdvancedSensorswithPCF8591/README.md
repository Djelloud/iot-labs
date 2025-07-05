# IoT Lab 5: Advanced Sensors with PCF8591 🌡️📡

A comprehensive Internet of Things (IoT) laboratory project demonstrating the integration of multiple sensors with the PCF8591 ADC/DAC chip and Raspberry Pi. This project showcases real-world sensor data acquisition, processing, and control applications.

## 🎯 Project Overview

This lab explores advanced sensor interfacing techniques using the PCF8591 8-bit ADC/DAC chip, which provides:
- 4 analog input channels (0-3.3V)
- 1 analog output channel (0-3.3V)
- I2C communication interface
- Real-time sensor data acquisition

## 🔧 Hardware Components

### Required Components:
- **Raspberry Pi** (any model with GPIO pins)
- **PCF8591 ADC/DAC Module** (I2C address: 0x48)
- **DHT11** - Digital humidity and temperature sensor
- **Analog Joystick** - 2-axis analog joystick with push button
- **Photoresistor** - Light-dependent resistor (LDR)
- **Rotary Encoder** - Digital rotary encoder with push button
- **Sound Sensor** - Analog microphone/sound level detector
- **Thermistor** - Temperature-sensitive resistor
- **Jumper Wires** and **Breadboard**

### Pin Connections:
```
PCF8591 Module:
- VCC → 3.3V
- GND → Ground
- SDA → GPIO 2 (Pin 3)
- SCL → GPIO 3 (Pin 5)

DHT11:
- VCC → 3.3V
- GND → Ground  
- DATA → GPIO 17 (Pin 11)

Rotary Encoder:
- CLK → GPIO 11 (Pin 23)
- DT → GPIO 12 (Pin 32)
- SW → GPIO 13 (Pin 33)
```

## 🚀 Features

### 1. **Environmental Monitoring**
- **Temperature & Humidity**: DHT11 sensor for ambient conditions
- **Light Level**: Photoresistor for ambient light measurement
- **Sound Level**: Microphone sensor for audio level detection

### 2. **User Interface**
- **Analog Joystick**: 2-axis position control with button input
- **Rotary Encoder**: Digital position encoder with reset button

### 3. **Temperature Measurement**
- **Thermistor**: Precision temperature measurement with mathematical conversion
- **Threshold Alerts**: Configurable temperature warnings

## 📁 Project Structure

```
Lab5AdvancedSensorswithPCF8591/
├── PCF8591.py          # Main PCF8591 driver module
├── pcf.py              # Basic PCF8591 usage example
├── humid.py            # DHT11 humidity & temperature sensor
├── joystick.py         # Analog joystick interface
├── photoresistor.py    # Light sensor interface
├── rotary.py           # Rotary encoder interface
├── sound.py            # Sound level sensor interface
├── thermistor.py       # Temperature sensor with thermistor
└── README.md           # This file
```

## 🛠️ Setup Instructions

### 1. **System Prerequisites**
```bash
# Update system packages
sudo apt update && sudo apt upgrade -y

# Install required Python packages
sudo apt install python3-pip python3-dev -y
pip3 install RPi.GPIO smbus2
```

### 2. **Enable I2C Interface**
```bash
# Enable I2C interface
sudo raspi-config
# Navigate to: Interface Options → I2C → Enable

# Verify I2C is working
sudo i2cdetect -y 1
# Should show device at address 0x48
```

### 3. **Clone and Run**
```bash
# Clone the repository
git clone https://github.com/yourusername/Lab5AdvancedSensorswithPCF8591.git
cd Lab5AdvancedSensorswithPCF8591

# Make scripts executable
chmod +x *.py

# Run individual sensor examples
python3 humid.py          # Humidity & temperature
python3 joystick.py       # Joystick control
python3 photoresistor.py  # Light sensor
python3 rotary.py         # Rotary encoder
python3 sound.py          # Sound sensor
python3 thermistor.py     # Temperature sensor
```

## 📊 Usage Examples

### Environmental Monitoring
```python
# Example: Reading humidity and temperature
python3 humid.py
# Output: humidity: 45 %, Temperature: 23 C
```

### Joystick Control
```python
# Example: Joystick direction detection
python3 joystick.py
# Output: up, down, left, right, pressed, home
```

### Light Sensor
```python
# Example: Light level monitoring
python3 photoresistor.py
# Output: Value: 128 (0-255 range)
```

### Temperature with Thermistor
```python
# Example: Precise temperature measurement
python3 thermistor.py
# Output: temperature = 24.5 C
```

## 🔬 Technical Details

### PCF8591 Communication
- **Protocol**: I2C (Inter-Integrated Circuit)
- **Address**: 0x48 (default)
- **Resolution**: 8-bit (0-255)
- **Voltage Range**: 0-3.3V
- **Channels**: 4 analog inputs, 1 analog output

### DHT11 Specifications
- **Humidity**: 20-90% RH (±5% accuracy)
- **Temperature**: 0-50°C (±2°C accuracy)
- **Communication**: Single-wire digital protocol

### Sensor Calibration
```python
# Temperature conversion formula (thermistor)
temp = 1/(((math.log(Rt / 10000)) / 3950) + (1 / (273.15+25)))
temp = temp - 273.15  # Convert to Celsius
```

## 🎛️ Advanced Features

### Real-time Data Logging
```python
# Example: Log sensor data to file
import datetime
with open('sensor_data.csv', 'a') as f:
    timestamp = datetime.datetime.now()
    f.write(f"{timestamp},{temperature},{humidity},{light_level}\n")
```

### Threshold Alerts
```python
# Example: Temperature alert system
if temperature > 30:
    print("⚠️  High temperature alert!")
elif temperature < 10:
    print("🧊 Low temperature alert!")
```

## 🔧 Troubleshooting

### Common Issues:

1. **I2C Device Not Found**
   ```bash
   # Check I2C connection
   sudo i2cdetect -y 1
   # Verify wiring and power connections
   ```

2. **Permission Denied**
   ```bash
   # Add user to i2c group
   sudo usermod -a -G i2c $USER
   sudo reboot
   ```

3. **DHT11 Reading Errors**
   ```bash
   # Increase reading delay
   time.sleep(2)  # Add delay between readings
   ```

## 📈 Future Enhancements

- [ ] **Web Dashboard**: Real-time sensor monitoring via web interface
- [ ] **Data Visualization**: Charts and graphs for sensor trends
- [ ] **MQTT Integration**: IoT cloud connectivity
- [ ] **Mobile App**: Smartphone control and monitoring
- [ ] **Machine Learning**: Predictive analytics for sensor data

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for:
- Bug fixes
- New sensor integrations
- Documentation improvements
- Code optimizations

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🎓 Educational Value

This lab provides hands-on experience with:
- **Analog-to-Digital Conversion**: Understanding ADC principles
- **I2C Communication**: Serial communication protocols
- **Sensor Physics**: Real-world sensor applications
- **Python Programming**: GPIO and hardware interfacing
- **IoT Concepts**: Connected device fundamentals

## 🌟 Acknowledgments

- SunFounder for DHT11 sensor implementation reference
- Raspberry Pi Foundation for GPIO library
- PCF8591 datasheet and application notes

---

**Made with ❤️ for IoT Education**

*Feel free to ⭐ this repository if you found it helpful!* 