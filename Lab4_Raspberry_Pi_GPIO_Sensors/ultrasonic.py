#!/usr/bin/env python3
"""
Ultrasonic Distance Sensor Controller
=====================================

This module provides precise distance measurement using the HC-SR04 ultrasonic sensor.
The sensor uses sound waves to measure distances with accuracy up to ±3mm.

Technical Specifications:
- Operating Voltage: 5V DC
- Measuring Range: 2cm - 400cm
- Measuring Angle: 15 degrees
- Trigger Pulse: 10µs minimum
- Echo Pulse: Proportional to distance

Pin Configuration:
- TRIG: Pin 11 (GPIO 17) - Trigger output
- ECHO: Pin 12 (GPIO 18) - Echo input

Author: [Your Name]
Date: 2024
License: MIT
"""

import RPi.GPIO as GPIO
import time
import statistics
from typing import Optional, List

# Hardware Configuration
TRIG_PIN = 11  # GPIO 17 - Trigger output pin
ECHO_PIN = 12  # GPIO 18 - Echo input pin

# Physical Constants
SOUND_SPEED = 34300  # cm/s at 20°C, standard atmospheric pressure
TIMEOUT_DURATION = 0.1  # 100ms timeout for echo detection

# Measurement Parameters
MEASUREMENT_SAMPLES = 3  # Number of samples for averaging
SAMPLE_DELAY = 0.06  # Delay between samples (60ms)
TRIGGER_PULSE_WIDTH = 0.00001  # 10µs trigger pulse width

class UltrasonicSensor:
    """
    HC-SR04 Ultrasonic Distance Sensor Controller
    
    This class provides methods for accurate distance measurement using
    ultrasonic sound wave reflection timing.
    """
    
    def __init__(self, trig_pin: int = TRIG_PIN, echo_pin: int = ECHO_PIN):
        """
        Initialize the ultrasonic sensor.
        
        Args:
            trig_pin (int): GPIO pin number for trigger output
            echo_pin (int): GPIO pin number for echo input
        """
        self.trig_pin = trig_pin
        self.echo_pin = echo_pin
        self.is_initialized = False
        
    def setup(self) -> None:
        """Initialize GPIO pins and configure sensor."""
        try:
            GPIO.setmode(GPIO.BOARD)
            GPIO.setup(self.trig_pin, GPIO.OUT)
            GPIO.setup(self.echo_pin, GPIO.IN)
            
            # Ensure trigger starts LOW
            GPIO.output(self.trig_pin, GPIO.LOW)
            time.sleep(0.1)  # Allow sensor to settle
            
            self.is_initialized = True
            print(f"✅ Ultrasonic sensor initialized (TRIG: Pin {self.trig_pin}, ECHO: Pin {self.echo_pin})")
            
        except Exception as e:
            print(f"❌ Sensor initialization failed: {e}")
            raise
    
    def _send_trigger_pulse(self) -> None:
        """Send a 10µs trigger pulse to start measurement."""
        GPIO.output(self.trig_pin, GPIO.LOW)
        time.sleep(0.000002)  # 2µs low pulse
        
        GPIO.output(self.trig_pin, GPIO.HIGH)
        time.sleep(TRIGGER_PULSE_WIDTH)  # 10µs high pulse
        GPIO.output(self.trig_pin, GPIO.LOW)
    
    def _measure_echo_time(self) -> Optional[float]:
        """
        Measure the echo pulse duration.
        
        Returns:
            float: Echo pulse duration in seconds, or None if timeout
        """
        # Wait for echo start (LOW to HIGH)
        timeout_start = time.time()
        while GPIO.input(self.echo_pin) == GPIO.LOW:
            pulse_start = time.time()
            if (pulse_start - timeout_start) > TIMEOUT_DURATION:
                return None
        
        # Wait for echo end (HIGH to LOW)
        timeout_start = time.time()
        while GPIO.input(self.echo_pin) == GPIO.HIGH:
            pulse_end = time.time()
            if (pulse_end - timeout_start) > TIMEOUT_DURATION:
                return None
        
        return pulse_end - pulse_start
    
    def measure_distance(self) -> Optional[float]:
        """
        Measure distance using ultrasonic sensor.
        
        Returns:
            float: Distance in centimeters, or None if measurement failed
            
        Notes:
            - Returns None for out-of-range or failed measurements
            - Accuracy: ±3mm under ideal conditions
            - Range: 2cm - 400cm
        """
        if not self.is_initialized:
            print("❌ Sensor not initialized. Call setup() first.")
            return None
        
        try:
            # Send trigger pulse
            self._send_trigger_pulse()
            
            # Measure echo time
            echo_duration = self._measure_echo_time()
            
            if echo_duration is None:
                return None
            
            # Calculate distance: distance = (time × speed) / 2
            # Division by 2 because sound travels to object and back
            distance_cm = (echo_duration * SOUND_SPEED) / 2
            
            # Validate measurement range
            if 2.0 <= distance_cm <= 400.0:
                return round(distance_cm, 2)
            else:
                return None
                
        except Exception as e:
            print(f"❌ Distance measurement error: {e}")
            return None
    
    def measure_distance_averaged(self, samples: int = MEASUREMENT_SAMPLES) -> Optional[float]:
        """
        Measure distance with multiple samples and return averaged result.
        
        Args:
            samples (int): Number of measurements to average
            
        Returns:
            float: Averaged distance in centimeters, or None if all measurements failed
        """
        measurements: List[float] = []
        
        for i in range(samples):
            distance = self.measure_distance()
            if distance is not None:
                measurements.append(distance)
            
            if i < samples - 1:  # Don't delay after last measurement
                time.sleep(SAMPLE_DELAY)
        
        if not measurements:
            return None
        
        # Return median for better noise rejection
        return round(statistics.median(measurements), 2)
    
    def cleanup(self) -> None:
        """Clean up GPIO resources."""
        try:
            GPIO.cleanup()
            self.is_initialized = False
            print("✅ GPIO cleanup complete")
        except Exception as e:
            print(f"❌ Cleanup error: {e}")

def continuous_monitoring():
    """Continuous distance monitoring with enhanced features."""
    sensor = UltrasonicSensor()
    
    try:
        sensor.setup()
        
        print("\n🌟 Ultrasonic Distance Sensor - Continuous Monitoring")
        print("=" * 55)
        print("📏 Range: 2cm - 400cm | Accuracy: ±3mm")
        print("🔄 Sampling: 3x averaged | Update: ~3Hz")
        print("🛑 Press Ctrl+C to exit")
        print("=" * 55)
        
        measurement_count = 0
        
        while True:
            # Get averaged measurement
            distance = sensor.measure_distance_averaged()
            measurement_count += 1
            
            if distance is not None:
                # Create visual bar graph
                bar_length = int(min(distance / 10, 40))  # Scale for display
                bar = "█" * bar_length + "░" * (40 - bar_length)
                
                print(f"#{measurement_count:4d} │ {distance:6.1f} cm │ {bar} │")
                
                # Distance-based alerts
                if distance < 10:
                    print("      │  ⚠️  VERY CLOSE!")
                elif distance < 30:
                    print("      │  🔶 Close")
                elif distance > 200:
                    print("      │  🔷 Far")
                    
            else:
                print(f"#{measurement_count:4d} │  ERROR   │ {'?' * 40} │ ❌ Out of range")
            
            time.sleep(0.2)  # ~3Hz update rate
            
    except KeyboardInterrupt:
        print("\n\n🛑 Monitoring stopped by user")
    except Exception as e:
        print(f"\n❌ Error during monitoring: {e}")
    finally:
        sensor.cleanup()

# Legacy compatibility functions
def setup():
    """Legacy function for backward compatibility."""
    global sensor
    sensor = UltrasonicSensor()
    sensor.setup()

def distance():
    """Legacy function for backward compatibility."""
    global sensor
    return sensor.measure_distance()

def loop():
    """Legacy function for backward compatibility."""
    while True:
        dis = distance()
        if dis is not None:
            print(f"{dis} cm")
        else:
            print("ERROR - Out of range")
        print()
        time.sleep(0.3)

def destroy():
    """Legacy function for backward compatibility."""
    global sensor
    sensor.cleanup()

if __name__ == "__main__":
    # Use enhanced monitoring by default
    continuous_monitoring()
    
    # Uncomment below for legacy mode:
    # setup()
    # try:
    #     loop()
    # except KeyboardInterrupt:
    #     destroy()
