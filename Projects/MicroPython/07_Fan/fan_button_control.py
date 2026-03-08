"""
Project 7.2 — Button-Controlled Fan
=====================================
Press Button 1 to start the fan, press again to stop.

Pins:
  Fan Motor INA = GPIO 19
  Fan Motor INB = GPIO 18
  Button 1 = GPIO 16
"""

from machine import Pin, PWM
import time

# Set up motor pins with 10kHz PWM
INA = PWM(Pin(19, Pin.OUT), 10000)
INB = PWM(Pin(18, Pin.OUT), 10000)

# Set up button
button1 = Pin(16, Pin.IN, Pin.PULL_UP)

count = 0

try:
    while True:
        btn_val1 = button1.value()

        if btn_val1 == 0:  # Button pressed
            time.sleep(0.01)  # Debounce

            # Wait for button release
            while btn_val1 == 0:
                btn_val1 = button1.value()

            if btn_val1 == 1:  # Button released
                count = count + 1
                print("Press count:", count)

                # Toggle fan: odd = ON, even = OFF
                if count % 2 == 1:
                    INA.duty(0)
                    INB.duty(700)
                    print("Fan ON")
                else:
                    INA.duty(0)
                    INB.duty(0)
                    print("Fan OFF")

except:
    INA.duty(0)
    INB.duty(0)
    INA.deinit()
    INB.deinit()
