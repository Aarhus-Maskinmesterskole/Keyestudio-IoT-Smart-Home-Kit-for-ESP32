"""
I2C LCD driver for MicroPython.
Works with PCF8574-based I2C LCD backpacks (common with 1602/2004 LCDs).

Based on: https://github.com/dhylands/python_lcd
License: MIT
"""

from lcd_api import LcdApi
from machine import I2C
import time


# PCF8574 pin mapping for LCD
MASK_RS = 0x01
MASK_RW = 0x02
MASK_E = 0x04
SHIFT_BACKLIGHT = 3
SHIFT_DATA = 4


class I2cLcd(LcdApi):
    """Implements a HD44780 character LCD connected via PCF8574 on I2C."""

    def __init__(self, i2c, i2c_addr, num_lines, num_columns):
        self.i2c = i2c
        self.i2c_addr = i2c_addr
        self.i2c.writeto(self.i2c_addr, bytearray([0]))
        time.sleep_ms(20)
        # Send reset 3 times
        self.hal_write_init_nibble(self.LCD_FUNCTION_RESET)
        time.sleep_ms(5)
        self.hal_write_init_nibble(self.LCD_FUNCTION_RESET)
        time.sleep_ms(1)
        self.hal_write_init_nibble(self.LCD_FUNCTION_RESET)
        time.sleep_ms(1)
        # Put LCD into 4-bit mode
        self.hal_write_init_nibble(self.LCD_FUNCTION)
        time.sleep_ms(1)
        LcdApi.__init__(self, num_lines, num_columns)
        cmd = self.LCD_FUNCTION
        if num_lines > 1:
            cmd |= self.LCD_FUNCTION_2LINES
        self.hal_write_command(cmd)

    def hal_write_init_nibble(self, nibble):
        """Writes an initialization nibble to the LCD."""
        byte = ((nibble >> 4) & 0x0f) << SHIFT_DATA
        self.i2c.writeto(self.i2c_addr, bytearray([byte | MASK_E]))
        self.i2c.writeto(self.i2c_addr, bytearray([byte]))

    def hal_backlight_on(self):
        """Turns the backlight on."""
        self.i2c.writeto(self.i2c_addr, bytearray([1 << SHIFT_BACKLIGHT]))

    def hal_backlight_off(self):
        """Turns the backlight off."""
        self.i2c.writeto(self.i2c_addr, bytearray([0]))

    def hal_write_command(self, cmd):
        """Write a command to the LCD."""
        self._hal_write(cmd, 0)

    def hal_write_data(self, data):
        """Write data to the LCD."""
        self._hal_write(data, MASK_RS)

    def _hal_write(self, data, mode):
        """Write to the LCD using 4-bit mode."""
        if self.backlight:
            mode |= (1 << SHIFT_BACKLIGHT)
        # High nibble
        bits = mode | (((data >> 4) & 0x0f) << SHIFT_DATA)
        self.i2c.writeto(self.i2c_addr, bytearray([bits | MASK_E]))
        self.i2c.writeto(self.i2c_addr, bytearray([bits]))
        # Low nibble
        bits = mode | ((data & 0x0f) << SHIFT_DATA)
        self.i2c.writeto(self.i2c_addr, bytearray([bits | MASK_E]))
        self.i2c.writeto(self.i2c_addr, bytearray([bits]))
        if data <= 3:
            # The home and clear commands require a worst case delay of 4.1ms
            time.sleep_ms(5)
