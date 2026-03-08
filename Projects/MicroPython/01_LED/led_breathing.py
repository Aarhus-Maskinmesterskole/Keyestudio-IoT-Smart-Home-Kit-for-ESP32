"""
Project 1.2 — Breathing LED
============================
Makes the LED smoothly fade in and out using PWM.
The LED gradually gets brighter, then dimmer, like breathing.

Pin: GPIO 12 = Yellow LED (PWM)
"""

import time
from machine import Pin, PWM

# Set up PWM on GPIO 12 with 10kHz frequency, starting duty cycle = 0
pwm = PWM(Pin(12, Pin.OUT), 10000)

try:
    while True:
        # Fade IN: brightness goes from 0 to 1023
        for i in range(0, 1023):
            pwm.duty(i)
            time.sleep_ms(1)

        # Fade OUT: brightness goes from 1023 to 0
        for i in range(0, 1023):
            pwm.duty(1023 - i)
            time.sleep_ms(1)

except:
    # Clean up PWM when stopping (important!)
    pwm.deinit()
