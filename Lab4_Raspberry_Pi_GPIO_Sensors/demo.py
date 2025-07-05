#!/usr/bin/env python3
"""
Raspberry Pi GPIO Sensors Laboratory - Interactive Demo
========================================================

This demo script showcases multiple sensors working together to create
an interactive IoT demonstration. It combines several sensor inputs with
visual feedback through LEDs.

Features:
- Ultrasonic distance measurement with color-coded LED feedback
- Button-controlled laser activation
- Touch sensor with RGB color cycling
- Hall effect sensor with magnetic field detection

Author: [Your Name]
Date: 2024
License: MIT
"""

import RPi.GPIO as GPIO
import time
import threading
import signal
import sys

# Pin Configuration
BUTTON_PIN = 11
TOUCH_PIN = 15
HALL_PIN = 16
LASER_PIN = 18
ULTRASONIC_TRIG = 22
ULTRASONIC_ECHO = 24
RGB_R_PIN = 32
RGB_G_PIN = 36
RGB_B_PIN = 38

# Global variables
running = True
current_distance = 0
rgb_pwm = {}

def setup_gpio():
    """Initialize all GPIO pins and PWM objects."""
    print("🔧 Setting up GPIO pins...")
    GPIO.setmode(GPIO.BOARD)
    
    # Input pins
    GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(TOUCH_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(HALL_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(ULTRASONIC_ECHO, GPIO.IN)
    
    # Output pins
    GPIO.setup(LASER_PIN, GPIO.OUT)
    GPIO.setup(ULTRASONIC_TRIG, GPIO.OUT)
    GPIO.setup(RGB_R_PIN, GPIO.OUT)
    GPIO.setup(RGB_G_PIN, GPIO.OUT)
    GPIO.setup(RGB_B_PIN, GPIO.OUT)
    
    # Initialize PWM for RGB LED
    rgb_pwm['R'] = GPIO.PWM(RGB_R_PIN, 1000)
    rgb_pwm['G'] = GPIO.PWM(RGB_G_PIN, 1000)
    rgb_pwm['B'] = GPIO.PWM(RGB_B_PIN, 1000)
    
    for pwm in rgb_pwm.values():
        pwm.start(0)
    
    # Turn off laser initially
    GPIO.output(LASER_PIN, GPIO.HIGH)
    
    print("✅ GPIO setup complete!")

def measure_distance():
    """Measure distance using ultrasonic sensor."""
    try:
        # Send trigger pulse
        GPIO.output(ULTRASONIC_TRIG, GPIO.LOW)
        time.sleep(0.000002)
        GPIO.output(ULTRASONIC_TRIG, GPIO.HIGH)
        time.sleep(0.00001)
        GPIO.output(ULTRASONIC_TRIG, GPIO.LOW)
        
        # Measure echo time
        pulse_start = time.time()
        pulse_end = time.time()
        
        # Wait for echo start
        timeout = time.time() + 0.1  # 100ms timeout
        while GPIO.input(ULTRASONIC_ECHO) == 0:
            pulse_start = time.time()
            if time.time() > timeout:
                return -1
        
        # Wait for echo end
        timeout = time.time() + 0.1
        while GPIO.input(ULTRASONIC_ECHO) == 1:
            pulse_end = time.time()
            if time.time() > timeout:
                return -1
        
        # Calculate distance
        pulse_duration = pulse_end - pulse_start
        distance = pulse_duration * 17150  # Speed of sound = 34300 cm/s
        
        return round(distance, 2)
    
    except Exception as e:
        print(f"❌ Distance measurement error: {e}")
        return -1

def set_rgb_color(r, g, b):
    """Set RGB LED color (0-100 for each channel)."""
    rgb_pwm['R'].ChangeDutyCycle(r)
    rgb_pwm['G'].ChangeDutyCycle(g)
    rgb_pwm['B'].ChangeDutyCycle(b)

def distance_feedback_color(distance):
    """Convert distance to color feedback."""
    if distance < 0:
        return (100, 0, 0)  # Red for error
    elif distance < 10:
        return (100, 0, 100)  # Purple for very close
    elif distance < 20:
        return (100, 0, 0)    # Red for close
    elif distance < 50:
        return (100, 50, 0)   # Orange for medium
    elif distance < 100:
        return (0, 100, 0)    # Green for far
    else:
        return (0, 0, 100)    # Blue for very far

def ultrasonic_thread():
    """Thread for continuous distance monitoring."""
    global current_distance, running
    
    while running:
        try:
            distance = measure_distance()
            current_distance = distance
            
            # Set RGB color based on distance
            r, g, b = distance_feedback_color(distance)
            set_rgb_color(r, g, b)
            
            time.sleep(0.1)  # 10Hz update rate
            
        except Exception as e:
            print(f"❌ Ultrasonic thread error: {e}")
            time.sleep(1)

def button_laser_thread():
    """Thread for button-controlled laser."""
    global running
    
    button_state = True  # Start with button not pressed (pull-up)
    
    while running:
        try:
            new_state = GPIO.input(BUTTON_PIN)
            
            if new_state != button_state:
                button_state = new_state
                
                if not button_state:  # Button pressed (LOW due to pull-up)
                    print("🔴 Laser ON")
                    GPIO.output(LASER_PIN, GPIO.LOW)
                else:  # Button released
                    print("⚫ Laser OFF")
                    GPIO.output(LASER_PIN, GPIO.HIGH)
            
            time.sleep(0.05)  # 20Hz polling
            
        except Exception as e:
            print(f"❌ Button thread error: {e}")
            time.sleep(1)

def sensor_status_thread():
    """Thread for displaying sensor status."""
    global running, current_distance
    
    while running:
        try:
            # Read sensor states
            touch_state = not GPIO.input(TOUCH_PIN)  # Invert for logical reading
            hall_state = not GPIO.input(HALL_PIN)    # Invert for logical reading
            button_state = not GPIO.input(BUTTON_PIN)
            
            # Clear screen and print status
            print("\033[H\033[J", end="")  # Clear terminal
            print("🌟 Raspberry Pi GPIO Sensors Laboratory - Live Demo")
            print("=" * 60)
            print(f"📏 Distance: {current_distance:6.1f} cm" if current_distance >= 0 else "📏 Distance: ERROR")
            print(f"🔴 Laser:    {'ON ' if button_state else 'OFF'}")
            print(f"👆 Touch:    {'ON ' if touch_state else 'OFF'}")
            print(f"🧲 Magnetic: {'DETECTED' if hall_state else 'NONE'}")
            print("=" * 60)
            print("💡 RGB LED shows distance: Purple(<10cm) Red(<20cm) Orange(<50cm) Green(<100cm) Blue(>100cm)")
            print("🔘 Press button to control laser")
            print("🛑 Press Ctrl+C to exit")
            
            time.sleep(0.5)  # 2Hz update rate
            
        except Exception as e:
            print(f"❌ Status thread error: {e}")
            time.sleep(1)

def cleanup():
    """Clean up GPIO resources."""
    global running
    running = False
    
    print("\n🛑 Shutting down...")
    
    # Stop PWM
    for pwm in rgb_pwm.values():
        pwm.stop()
    
    # Turn off outputs
    GPIO.output(LASER_PIN, GPIO.HIGH)
    set_rgb_color(0, 0, 0)
    
    # Cleanup GPIO
    GPIO.cleanup()
    print("✅ Cleanup complete!")

def signal_handler(sig, frame):
    """Handle Ctrl+C gracefully."""
    cleanup()
    sys.exit(0)

def main():
    """Main demo function."""
    print("🌟 Raspberry Pi GPIO Sensors Laboratory")
    print("🚀 Starting Interactive Demo...")
    print("⚠️  WARNING: Do not look directly into laser light!")
    
    # Setup signal handler
    signal.signal(signal.SIGINT, signal_handler)
    
    try:
        # Initialize hardware
        setup_gpio()
        
        # Start background threads
        threads = [
            threading.Thread(target=ultrasonic_thread, daemon=True),
            threading.Thread(target=button_laser_thread, daemon=True),
            threading.Thread(target=sensor_status_thread, daemon=True)
        ]
        
        for thread in threads:
            thread.start()
        
        # Keep main thread alive
        while running:
            time.sleep(1)
            
    except Exception as e:
        print(f"❌ Demo error: {e}")
        cleanup()

if __name__ == "__main__":
    main() 