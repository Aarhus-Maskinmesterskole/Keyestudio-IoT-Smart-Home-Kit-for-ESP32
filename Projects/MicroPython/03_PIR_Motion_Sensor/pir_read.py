"""
Project 3.1 — Read PIR Motion Sensor
======================================
Reads the PIR sensor value and prints if someone is nearby.
  - Value 1 = Motion detected!
  - Value 0 = No motion

Pin: GPIO 14 = PIR Motion Sensor
"""

from machine import Pin
import time

# Set up PIR sensor as input
PIR = Pin(14, Pin.IN)

while True:
    value = PIR.value()
    print(value, end=" ")

    if value == 1:
        print("Some body is in this area!")
    else:
        print("No one!")

    time.sleep(0.1)
