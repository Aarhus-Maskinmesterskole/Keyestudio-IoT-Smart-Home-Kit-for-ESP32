"""
Project 9.1 — Temperature & Humidity Display
==============================================
Reads temperature and humidity from the DHT11 sensor
and displays them on the LCD1602.

⚠️  REQUIRED: Upload i2c_lcd.py and lcd_api.py to ESP32 first!

Pins:
  DHT11 Sensor = GPIO 17
  LCD1602 via I2C: SDA = GPIO 21, SCL = GPIO 22
"""

import machine
import time
import dht
from machine import SoftI2C, Pin
from i2c_lcd import I2cLcd

# Set up DHT11 sensor on GPIO 17
DHT = dht.DHT11(machine.Pin(17))

# Set up LCD
DEFAULT_I2C_ADDR = 0x27
i2c = SoftI2C(scl=Pin(22), sda=Pin(21), freq=100000)
lcd = I2cLcd(i2c, DEFAULT_I2C_ADDR, 2, 16)

while True:
    # Read sensor data
    DHT.measure()

    # Get values
    temp = DHT.temperature()
    hum = DHT.humidity()

    # Print to shell
    print('Temperature:', temp, '°C', 'Humidity:', hum, '%')

    # Display on LCD
    lcd.move_to(1, 0)
    lcd.putstr('T= {} C   '.format(temp))    # Line 1: Temperature

    lcd.move_to(1, 1)
    lcd.putstr('H= {} %RH '.format(hum))     # Line 2: Humidity

    time.sleep_ms(1000)  # Read every 1 second
