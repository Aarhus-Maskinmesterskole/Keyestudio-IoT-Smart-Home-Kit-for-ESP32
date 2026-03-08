"""
Project 8.1 — LCD1602 Display Hello
=====================================
Displays "Hello" on line 1 and "keyestudio" on line 2.

⚠️  REQUIRED: Upload i2c_lcd.py and lcd_api.py to ESP32 first!

Pins:
  LCD1602 via I2C: SDA = GPIO 21, SCL = GPIO 22
  I2C Address: 0x27
"""

from time import sleep_ms, ticks_ms
from machine import I2C, Pin
from i2c_lcd import I2cLcd

# LCD I2C address (default for most modules)
DEFAULT_I2C_ADDR = 0x27

# Set up I2C and LCD (2 rows, 16 columns)
i2c = I2C(scl=Pin(22), sda=Pin(21), freq=400000)
lcd = I2cLcd(i2c, DEFAULT_I2C_ADDR, 2, 16)

# Display text
lcd.move_to(1, 0)        # Column 1, Row 0 (first line)
lcd.putstr('Hello')

lcd.move_to(1, 1)        # Column 1, Row 1 (second line)
lcd.putstr('keyestudio')

# ============================================
# Useful LCD commands to try in the REPL:
# ============================================
# lcd.putstr('Hello world')    # Print text
# lcd.clear()                  # Clear display
# lcd.move_to(2, 1)            # Move cursor
# lcd.show_cursor()            # Show cursor
# lcd.hide_cursor()            # Hide cursor
# lcd.blink_cursor_on()        # Blinking cursor
# lcd.blink_cursor_off()       # Stop blinking
# lcd.display_off()            # Blank display
# lcd.display_on()             # Unblank display
# lcd.backlight_off()          # Turn off backlight
# lcd.backlight_on()           # Turn on backlight
