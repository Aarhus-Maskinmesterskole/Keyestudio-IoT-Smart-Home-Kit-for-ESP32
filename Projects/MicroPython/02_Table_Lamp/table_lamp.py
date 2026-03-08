"""
Project 2.2 — Table Lamp
=========================
Click Button 1 to toggle the LED on/off, just like a table lamp.
Counts button presses — odd = LED ON, even = LED OFF.

Pins:
  Button 1 = GPIO 16
  Yellow LED = GPIO 12
"""

from machine import Pin
import time

# Set up button and LED
button1 = Pin(16, Pin.IN, Pin.PULL_UP)
led = Pin(12, Pin.OUT)

count = 0

while True:
    btn_val1 = button1.value()  # Read button state

    if btn_val1 == 0:  # Button is pressed
        time.sleep(0.01)  # Debounce delay

        # Wait for button release
        while btn_val1 == 0:
            btn_val1 = button1.value()

        if btn_val1 == 1:  # Button released
            count = count + 1
            print("Press count:", count)

            # Toggle LED: odd count = ON, even count = OFF
            if count % 2 == 1:
                led.value(1)  # LED ON
            else:
                led.value(0)  # LED OFF

    time.sleep(0.1)
