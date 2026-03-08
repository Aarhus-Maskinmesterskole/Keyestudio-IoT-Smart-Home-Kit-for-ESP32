"""
Project 6.2 — Button-Controlled Atmosphere Lamp
=================================================
Use Button 1 to go to the previous color, Button 2 to go to the next.
Colors: Off → Red → Green → Blue → White

Pins:
  SK6812 RGB LEDs = GPIO 26 (4 LEDs)
  Button 1 = GPIO 16 (previous color)
  Button 2 = GPIO 27 (next color)
"""

from machine import Pin
import neopixel
import time

# Set up buttons
button1 = Pin(16, Pin.IN, Pin.PULL_UP)
button2 = Pin(27, Pin.IN, Pin.PULL_UP)

# Set up NeoPixel: 4 LEDs on GPIO 26
pin = Pin(26, Pin.OUT)
np = neopixel.NeoPixel(pin, 4)

# Brightness: 0-255
brightness = 100

# Define colors: Off, Red, Green, Blue, White
colors = [
    [0, 0, 0],                                # 0 = Off
    [brightness, 0, 0],                       # 1 = Red
    [0, brightness, 0],                       # 2 = Green
    [0, 0, brightness],                       # 3 = Blue
    [brightness, brightness, brightness]      # 4 = White
]

count = 0  # Current color index


def set_color(index):
    """Set all 4 LEDs to the color at the given index."""
    for j in range(0, 4):
        np[j] = colors[index]
    np.write()
    time.sleep_ms(50)


# Start with LEDs off
set_color(0)

while True:
    # Button 1 → Previous color
    btn_val1 = button1.value()
    if btn_val1 == 0:
        time.sleep(0.01)  # Debounce
        while btn_val1 == 0:
            btn_val1 = button1.value()
        if btn_val1 == 1:
            count = count - 1
            if count <= 0:
                count = 0
            print("Color index:", count)

    # Button 2 → Next color
    btn_val2 = button2.value()
    if btn_val2 == 0:
        time.sleep(0.01)  # Debounce
        while btn_val2 == 0:
            btn_val2 = button2.value()
        if btn_val2 == 1:
            count = count + 1
            if count >= 4:
                count = 4
            print("Color index:", count)

    # Update the LEDs
    set_color(count)
