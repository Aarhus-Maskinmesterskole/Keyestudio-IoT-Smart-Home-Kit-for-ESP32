"""
Project 1.1 — LED Blink
========================
Makes the yellow LED blink on and off every second.

Pin: GPIO 12 = Yellow LED
"""

from machine import Pin
import time

# Set up the LED on GPIO 12 as output
led = Pin(12, Pin.OUT)

# Blink forever
while True:
    led.value(1)    # Turn LED ON
    time.sleep(1)   # Wait 1 second
    led.value(0)    # Turn LED OFF
    time.sleep(1)   # Wait 1 second
