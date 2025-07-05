# ⚡ Quick Start Guide

Get your Raspberry Pi GPIO sensors running in 5 minutes!

## 🚀 Fast Setup

### 1. Clone and Navigate
```bash
git clone https://github.com/yourusername/raspberry-pi-gpio-sensors
cd raspberry-pi-gpio-sensors
```

### 2. Install Dependencies
```bash
# Option 1: Using package manager (recommended)
sudo apt update
sudo apt install python3-rpi.gpio

# Option 2: Using pip
pip3 install -r requirements.txt
```

### 3. Test Your Setup
```bash
# Test individual sensors
sudo python3 button.py          # Button + LED feedback
sudo python3 ultrasonic.py      # Distance measurement
sudo python3 rgb_led.py         # RGB color cycling

# Run comprehensive demo
sudo python3 demo.py            # Multi-sensor interactive demo
```

## 🎯 Essential Commands

### Individual Sensor Tests
```bash
sudo python3 button.py          # 🔘 Button with red/green LED
sudo python3 touch.py           # 👆 Touch sensor with feedback  
sudo python3 hall.py            # 🧲 Magnetic field detection
sudo python3 tilt.py            # ⚖️ Orientation sensing
sudo python3 laser.py           # 🔴 Laser on/off (SAFETY!)
sudo python3 photo_interrupter.py # 📷 Light barrier detection
sudo python3 color_led.py       # 🌈 Dual-color LED patterns
sudo python3 rgb_led.py         # 🎨 Full RGB color cycling
sudo python3 ultrasonic.py      # 📏 Distance measurement
```

### Interactive Demo
```bash
sudo python3 demo.py
# Features:
# - Real-time distance measurement with RGB feedback
# - Button-controlled laser activation  
# - Touch and magnetic field detection
# - Live status dashboard
```

## 🔧 Hardware Quick Setup

### Minimal Wiring (Ultrasonic Example)
```
Raspberry Pi    →    HC-SR04
─────────────────────────────
5V (Pin 2)      →    VCC
GND (Pin 6)     →    GND  
Pin 11          →    TRIG
Pin 12          →    ECHO
```

### RGB LED Wiring
```
Raspberry Pi    →    RGB LED
─────────────────────────────
Pin 32 + 220Ω   →    Red
Pin 36 + 220Ω   →    Green  
Pin 38 + 220Ω   →    Blue
GND (Pin 34)    →    Cathode(-)
```

## ⚠️ Important Notes

### Safety First
- **Always use `sudo`** for GPIO access
- **Power off Pi** before wiring changes
- **Never look into laser** directly
- **Check connections** before powering on

### Troubleshooting
```bash
# Check GPIO status
gpio readall

# Test Python GPIO library
python3 -c "import RPi.GPIO; print('GPIO library OK')"

# Stop running scripts
Ctrl + C

# If GPIO busy error
sudo python3 -c "import RPi.GPIO; RPi.GPIO.cleanup()"
```

## 📱 Expected Output Examples

### Ultrasonic Sensor
```
🌟 Ultrasonic Distance Sensor - Continuous Monitoring
═══════════════════════════════════════════════════════
📏 Range: 2cm - 400cm | Accuracy: ±3mm
🔄 Sampling: 3x averaged | Update: ~3Hz
═══════════════════════════════════════════════════════
#   1 │  15.2 cm │ █░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ │
#   2 │  23.8 cm │ ██░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ │
```

### Demo Mode
```
🌟 Raspberry Pi GPIO Sensors Laboratory - Live Demo
════════════════════════════════════════════════════════════
📏 Distance:   45.3 cm
🔴 Laser:     OFF
👆 Touch:     OFF  
🧲 Magnetic:  NONE
════════════════════════════════════════════════════════════
💡 RGB LED shows distance: Purple(<10cm) Red(<20cm) Orange(<50cm)
🔘 Press button to control laser
🛑 Press Ctrl+C to exit
```

## 🎓 Next Steps

1. **Customize pin assignments** in individual files
2. **Combine sensors** for custom applications
3. **Add data logging** with timestamps
4. **Create web interface** for remote monitoring
5. **Integrate with IoT platforms** (MQTT, ThingSpeak)

## 📞 Need Help?

- 📖 **Full Documentation**: See `README.md`
- 🔌 **Wiring Diagrams**: See `CIRCUIT_DIAGRAMS.md`  
- 🐛 **Issues**: Create GitHub issue
- 💡 **Ideas**: Contribute via pull request

---

🚀 **Ready to build IoT projects? You've got the tools!** 