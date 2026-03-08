"""
Project 2.1 — Read Button Values
=================================
Reads the state of Button 1 and Button 2 and prints them to the shell.
  - Value 1 = Button NOT pressed
  - Value 0 = Button IS pressed

Pins:
  Button 1 = GPIO 16
  Button 2 = GPIO 27
"""

from machine import Pin
import time

# Set up buttons with internal pull-up resistors
button1 = Pin(16, Pin.IN, Pin.PULL_UP)
button2 = Pin(27, Pin.IN, Pin.PULL_UP)

while True:
    btn_val1 = button1.value()  # Read Button 1
    btn_val2 = button2.value()  # Read Button 2

    print("button1 =", btn_val1)
    print("button2 =", btn_val2)

    time.sleep(0.1)  # Small delay
