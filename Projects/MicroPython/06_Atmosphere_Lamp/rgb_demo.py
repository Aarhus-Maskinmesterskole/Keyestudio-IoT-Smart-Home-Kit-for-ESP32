"""
Project 6.1 — RGB SK6812 Demo
===============================
Cycles through red, green, blue, white, and off on all 4 RGB LEDs.

Pin: GPIO 26 = SK6812 NeoPixel (4 LEDs)
"""

from machine import Pin
import neopixel
import time

# Set up NeoPixel: 4 LEDs on GPIO 26
pin = Pin(26, Pin.OUT)
np = neopixel.NeoPixel(pin, 4)

# Brightness: 0-255 (100 is a nice level, not too bright)
brightness = 100

# Define colors as (R, G, B)
colors = [
    [brightness, 0, 0],                      # Red
    [0, brightness, 0],                      # Green
    [0, 0, brightness],                      # Blue
    [brightness, brightness, brightness],    # White
    [0, 0, 0]                                # Off
]

# Cycle through all colors forever
while True:
    for i in range(0, 5):
        # Set all 4 LEDs to the same color
        for j in range(0, 4):
            np[j] = colors[i]
        np.write()            # Send data to LEDs
        time.sleep_ms(50)     # Small delay between LEDs

        time.sleep_ms(500)    # Show each color for 0.5 seconds
    time.sleep_ms(500)
