"""
Project 3.2 — PIR Motion-Activated LED
========================================
LED turns on when motion is detected, turns off when still.

Pins:
  PIR Motion Sensor = GPIO 14
  Yellow LED = GPIO 12
"""

from machine import Pin
import time

# Set up PIR sensor and LED
PIR = Pin(14, Pin.IN)
led = Pin(12, Pin.OUT)

while True:
    value = PIR.value()
    print(value)

    if value == 1:
        led.value(1)  # Motion detected → LED ON
    else:
        led.value(0)  # No motion → LED OFF

    time.sleep(0.1)
