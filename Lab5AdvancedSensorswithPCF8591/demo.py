#!/usr/bin/env python3
"""
IoT Lab 5: Advanced Sensors with PCF8591 - Demo Script
=====================================================

This demo script showcases multiple sensors working together:
- DHT11 for humidity and temperature
- Photoresistor for light level
- Sound sensor for audio level
- Joystick for user input
- Thermistor for precise temperature

Usage: python3 demo.py
"""

import PCF8591 as ADC
import RPi.GPIO as GPIO
import time
import math
import datetime
import sys

# GPIO Setup
DHT_PIN = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(DHT_PIN, GPIO.IN)

# Global variables
running = True
log_file = f"sensor_log_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

def setup():
    """Initialize all sensors"""
    print("🚀 Initializing IoT Lab 5 - Advanced Sensors Demo")
    print("=" * 50)
    
    try:
        ADC.setup(0x48)
        print("✅ PCF8591 ADC/DAC initialized successfully")
        
        # Create CSV log file header
        with open(log_file, 'w') as f:
            f.write("timestamp,temperature_dht,humidity,light_level,sound_level,temperature_thermistor,joystick_state\n")
        print(f"✅ Data logging initialized: {log_file}")
        
        return True
    except Exception as e:
        print(f"❌ Setup failed: {e}")
        return False

def read_dht11():
    """Read DHT11 sensor (simplified version)"""
    try:
        # This is a simplified version - in real implementation, 
        # you'd use the full DHT11 protocol from humid.py
        return 25.0, 60.0  # Mock values for demo
    except:
        return None, None

def read_photoresistor():
    """Read light level from photoresistor"""
    try:
        return ADC.read(0)
    except:
        return 0

def read_sound_sensor():
    """Read sound level"""
    try:
        return ADC.read(1)
    except:
        return 0

def read_thermistor():
    """Read temperature from thermistor"""
    try:
        analog_val = ADC.read(2)
        if analog_val == 0:
            return 0
        
        vr = 5 * float(analog_val) / 255
        rt = 10000 * vr / (5 - vr)
        temp = 1/(((math.log(rt / 10000)) / 3950) + (1 / (273.15+25)))
        temp = temp - 273.15
        return round(temp, 2)
    except:
        return 0

def read_joystick():
    """Read joystick position"""
    try:
        x_val = ADC.read(0)
        y_val = ADC.read(1)
        btn_val = ADC.read(2)
        
        # Determine direction
        if x_val <= 30:
            return "UP"
        elif x_val >= 225:
            return "DOWN"
        elif y_val >= 225:
            return "LEFT"
        elif y_val <= 30:
            return "RIGHT"
        elif btn_val <= 30:
            return "PRESSED"
        else:
            return "CENTER"
    except:
        return "ERROR"

def display_sensor_data(temp_dht, humidity, light, sound, temp_therm, joystick):
    """Display sensor data in a formatted way"""
    print("\n" + "=" * 60)
    print(f"📊 SENSOR READINGS - {datetime.datetime.now().strftime('%H:%M:%S')}")
    print("=" * 60)
    
    print(f"🌡️  DHT11 Temperature: {temp_dht}°C")
    print(f"💧 Humidity: {humidity}%")
    print(f"🌟 Light Level: {light}/255 ({light/255*100:.1f}%)")
    print(f"🔊 Sound Level: {sound}/255 ({sound/255*100:.1f}%)")
    print(f"🌡️  Thermistor Temp: {temp_therm}°C")
    print(f"🕹️  Joystick: {joystick}")
    
    # Status indicators
    if light < 50:
        print("🌙 Environment: Dark")
    elif light > 200:
        print("☀️  Environment: Bright")
    else:
        print("🌤️  Environment: Normal")
    
    if sound > 100:
        print("📢 Audio: Loud environment detected")
    elif sound < 20:
        print("🔇 Audio: Quiet environment")
    
    if temp_therm > 30:
        print("🔥 Temperature Alert: High temperature!")
    elif temp_therm < 10:
        print("❄️  Temperature Alert: Low temperature!")

def log_data(temp_dht, humidity, light, sound, temp_therm, joystick):
    """Log sensor data to CSV file"""
    try:
        timestamp = datetime.datetime.now().isoformat()
        with open(log_file, 'a') as f:
            f.write(f"{timestamp},{temp_dht},{humidity},{light},{sound},{temp_therm},{joystick}\n")
    except Exception as e:
        print(f"⚠️  Logging error: {e}")

def main_loop():
    """Main sensor reading loop"""
    global running
    
    print("\n🔄 Starting continuous sensor monitoring...")
    print("Press Ctrl+C to stop\n")
    
    try:
        while running:
            # Read all sensors
            temp_dht, humidity = read_dht11()
            light_level = read_photoresistor()
            sound_level = read_sound_sensor()
            temp_thermistor = read_thermistor()
            joystick_state = read_joystick()
            
            # Display data
            display_sensor_data(
                temp_dht, humidity, light_level, 
                sound_level, temp_thermistor, joystick_state
            )
            
            # Log data
            log_data(
                temp_dht, humidity, light_level,
                sound_level, temp_thermistor, joystick_state
            )
            
            # Check for joystick commands
            if joystick_state == "PRESSED":
                print("\n🛑 Joystick pressed - pausing for 3 seconds...")
                time.sleep(3)
            
            # Wait before next reading
            time.sleep(2)
            
    except KeyboardInterrupt:
        print("\n\n🛑 Stopping sensor monitoring...")
        running = False

def cleanup():
    """Clean up resources"""
    try:
        GPIO.cleanup()
        print("✅ GPIO cleanup completed")
        print(f"📁 Data saved to: {log_file}")
        print("👋 Thank you for using IoT Lab 5!")
    except:
        pass

if __name__ == "__main__":
    print("🌡️📡 IoT Lab 5: Advanced Sensors with PCF8591")
    print("=" * 50)
    
    if not setup():
        print("❌ Setup failed. Exiting...")
        sys.exit(1)
    
    try:
        main_loop()
    finally:
        cleanup() 