"""
Software I2C implementation for MicroPython.
Used by the MFRC522 RFID module.
"""

from machine import Pin
import time


class SoftI2C:
    """Bit-bang I2C implementation."""

    def __init__(self, scl, sda, freq=100000):
        self.scl = Pin(scl, Pin.OPEN_DRAIN, value=1)
        self.sda = Pin(sda, Pin.OPEN_DRAIN, value=1)
        self.delay = 1000000 // freq // 2  # Half-period in microseconds

    def _delay(self):
        time.sleep_us(self.delay)

    def _start(self):
        self.sda(1)
        self.scl(1)
        self._delay()
        self.sda(0)
        self._delay()
        self.scl(0)
        self._delay()

    def _stop(self):
        self.sda(0)
        self._delay()
        self.scl(1)
        self._delay()
        self.sda(1)
        self._delay()

    def _write_byte(self, data):
        for i in range(8):
            self.sda((data >> (7 - i)) & 1)
            self._delay()
            self.scl(1)
            self._delay()
            self.scl(0)
            self._delay()
        # Read ACK
        self.sda(1)
        self._delay()
        self.scl(1)
        self._delay()
        ack = self.sda()
        self.scl(0)
        self._delay()
        return ack

    def _read_byte(self, ack):
        data = 0
        self.sda(1)
        for i in range(8):
            self.scl(1)
            self._delay()
            data = (data << 1) | self.sda()
            self.scl(0)
            self._delay()
        # Send ACK/NACK
        self.sda(0 if ack else 1)
        self._delay()
        self.scl(1)
        self._delay()
        self.scl(0)
        self._delay()
        self.sda(1)
        return data

    def writeto(self, addr, buf):
        self._start()
        self._write_byte(addr << 1)
        for b in buf:
            self._write_byte(b)
        self._stop()

    def readfrom(self, addr, nbytes):
        self._start()
        self._write_byte((addr << 1) | 1)
        data = []
        for i in range(nbytes):
            data.append(self._read_byte(i < nbytes - 1))
        self._stop()
        return bytes(data)

    def writeto_mem(self, addr, reg, buf):
        self._start()
        self._write_byte(addr << 1)
        self._write_byte(reg)
        for b in buf:
            self._write_byte(b)
        self._stop()

    def readfrom_mem(self, addr, reg, nbytes):
        self._start()
        self._write_byte(addr << 1)
        self._write_byte(reg)
        self._start()
        self._write_byte((addr << 1) | 1)
        data = []
        for i in range(nbytes):
            data.append(self._read_byte(i < nbytes - 1))
        self._stop()
        return bytes(data)
