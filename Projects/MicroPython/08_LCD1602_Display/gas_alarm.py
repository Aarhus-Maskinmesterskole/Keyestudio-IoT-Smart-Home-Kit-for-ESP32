"""
Project 8.2 — Gas Alarm System
================================
Displays "Safety" on the LCD in normal conditions.
When the MQ2 gas sensor detects dangerous gas, displays "dangerous".

⚠️  REQUIRED: Upload i2c_lcd.py and lcd_api.py to ESP32 first!

Pins:
  LCD1602 via I2C: SDA = GPIO 21, SCL = GPIO 22
  Gas Sensor (MQ2) = GPIO 23
"""

from time import sleep_ms, ticks_ms
from machine import SoftI2C, Pin
from i2c_lcd import I2cLcd
import time

# LCD setup
DEFAULT_I2C_ADDR = 0x27
i2c = SoftI2C(scl=Pin(22), sda=Pin(21), freq=100000)
lcd = I2cLcd(i2c, DEFAULT_I2C_ADDR, 2, 16)

# Gas sensor setup (digital read)
gas = Pin(23, Pin.IN, Pin.PULL_UP)

while True:
    gas_val = gas.value()
    print("gas =", gas_val)

    # Show gas value on LCD line 2
    lcd.move_to(1, 1)
    lcd.putstr('val: {}'.format(gas_val))

    # Show status on LCD line 1
    if gas_val == 1:
        lcd.move_to(1, 0)
        lcd.putstr('Safety   ')       # Spaces to clear old text
    else:
        lcd.move_to(1, 0)
        lcd.putstr('dangerous')

    time.sleep(0.1)
