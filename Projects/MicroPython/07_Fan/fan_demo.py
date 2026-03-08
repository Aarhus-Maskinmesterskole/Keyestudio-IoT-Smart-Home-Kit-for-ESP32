"""
Project 7.1 — Fan Speed Demo
==============================
Rotates the fan clockwise, stops, rotates anticlockwise, stops — in a loop.

Pins:
  Fan Motor INA = GPIO 19 (IN+)
  Fan Motor INB = GPIO 18 (IN-)

Motor control:
  INA=0, INB=700 → Clockwise
  INA=600, INB=0 → Anticlockwise
  INA=0, INB=0   → Stop
"""

from machine import Pin, PWM
import time

# Set up motor pins with 10kHz PWM
INA = PWM(Pin(19, Pin.OUT), 10000)  # INA = IN+
INB = PWM(Pin(18, Pin.OUT), 10000)  # INB = IN-

try:
    while True:
        # Rotate counterclockwise for 2 seconds
        INA.duty(0)
        INB.duty(700)
        print("Counterclockwise")
        time.sleep(2)

        # Stop for 1 second
        INA.duty(0)
        INB.duty(0)
        print("Stop")
        time.sleep(1)

        # Rotate clockwise for 2 seconds
        INA.duty(600)
        INB.duty(0)
        print("Clockwise")
        time.sleep(2)

        # Stop for 1 second
        INA.duty(0)
        INB.duty(0)
        print("Stop")
        time.sleep(1)

except:
    # Clean up: stop motor and release PWM
    INA.duty(0)
    INB.duty(0)
    INA.deinit()
    INB.deinit()
