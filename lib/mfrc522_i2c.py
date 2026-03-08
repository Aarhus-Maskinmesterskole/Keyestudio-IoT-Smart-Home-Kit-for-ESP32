"""
MFRC522 RFID reader I2C driver for MicroPython.
Works with the Keyestudio MFRC522 I2C RFID module.

Based on the Keyestudio ESP32 Smart Home Kit tutorial.
"""

from machine import Pin
from soft_iic import SoftI2C
from mfrc522_config import Reg, Cmd, MI_OK, MI_NOTAGERR, MI_ERR, MAX_LEN
import time


class UID:
    """Holds card UID data."""
    def __init__(self):
        self.size = 0
        self.uidByte = [0] * 10
        self.sak = 0


class mfrc522:
    """MFRC522 RFID reader using I2C communication."""

    def __init__(self, scl, sda, addr=0x28):
        self.i2c = SoftI2C(scl, sda)
        self.addr = addr
        self.uid = UID()

    def _wreg(self, reg, val):
        self.i2c.writeto_mem(self.addr, reg, bytearray([val]))

    def _rreg(self, reg):
        data = self.i2c.readfrom_mem(self.addr, reg, 1)
        return data[0]

    def _sflags(self, reg, mask):
        self._wreg(reg, self._rreg(reg) | mask)

    def _cflags(self, reg, mask):
        self._wreg(reg, self._rreg(reg) & (~mask))

    def _tocard(self, cmd, send):
        recv = []
        bits = irq_en = wait_irq = n = 0
        stat = MI_ERR

        if cmd == Cmd.PCD_AUTHENT:
            irq_en = 0x12
            wait_irq = 0x10
        if cmd == Cmd.PCD_TRANSCEIVE:
            irq_en = 0x77
            wait_irq = 0x30

        self._wreg(Reg.CommIEnReg, irq_en | 0x80)
        self._cflags(Reg.CommIrqReg, 0x80)
        self._sflags(Reg.FIFOLevelReg, 0x80)
        self._wreg(Reg.CommandReg, Cmd.PCD_IDLE)

        for c in send:
            self._wreg(Reg.FIFODataReg, c)

        self._wreg(Reg.CommandReg, cmd)

        if cmd == Cmd.PCD_TRANSCEIVE:
            self._sflags(Reg.BitFramingReg, 0x80)

        i = 2000
        while True:
            n = self._rreg(Reg.CommIrqReg)
            i -= 1
            if ~((i != 0) and ~(n & 0x01) and ~(n & wait_irq)):
                break

        self._cflags(Reg.BitFramingReg, 0x80)

        if i:
            if (self._rreg(Reg.ErrorReg) & 0x1B) == 0x00:
                stat = MI_OK

                if n & irq_en & 0x01:
                    stat = MI_NOTAGERR

                if cmd == Cmd.PCD_TRANSCEIVE:
                    n = self._rreg(Reg.FIFOLevelReg)
                    lbits = self._rreg(Reg.ControlReg) & 0x07
                    if lbits != 0:
                        bits = (n - 1) * 8 + lbits
                    else:
                        bits = n * 8

                    if n == 0:
                        n = 1
                    if n > MAX_LEN:
                        n = MAX_LEN

                    for _ in range(n):
                        recv.append(self._rreg(Reg.FIFODataReg))
            else:
                stat = MI_ERR

        return stat, recv, bits

    def _crc(self, data):
        self._cflags(Reg.DivIrqReg, 0x04)
        self._sflags(Reg.FIFOLevelReg, 0x80)

        for c in data:
            self._wreg(Reg.FIFODataReg, c)

        self._wreg(Reg.CommandReg, Cmd.PCD_CALCCRC)

        i = 0xFF
        while True:
            n = self._rreg(Reg.DivIrqReg)
            i -= 1
            if not ((i != 0) and not (n & 0x04)):
                break

        return [self._rreg(Reg.CRCResultRegL), self._rreg(Reg.CRCResultRegM)]

    def PCD_Init(self):
        """Initialize the MFRC522 module."""
        self.PCD_Reset()
        self._wreg(Reg.TModeReg, 0x8D)
        self._wreg(Reg.TPrescalerReg, 0x3E)
        self._wreg(Reg.TReloadRegL, 30)
        self._wreg(Reg.TReloadRegH, 0)
        self._wreg(Reg.TxASKReg, 0x40)
        self._wreg(Reg.ModeReg, 0x3D)
        self.AntennaOn()

    def PCD_Reset(self):
        """Reset the MFRC522 module."""
        self._wreg(Reg.CommandReg, Cmd.PCD_RESETPHASE)

    def AntennaOn(self):
        """Turn on the antenna."""
        temp = self._rreg(Reg.TxControlReg)
        if ~(temp & 0x03):
            self._sflags(Reg.TxControlReg, 0x03)

    def AntennaOff(self):
        """Turn off the antenna."""
        self._cflags(Reg.TxControlReg, 0x03)

    def PICC_IsNewCardPresent(self):
        """Check if a new card is present."""
        self._wreg(Reg.BitFramingReg, 0x07)
        stat, recv, bits = self._tocard(Cmd.PCD_TRANSCEIVE, [Cmd.PICC_REQIDL])
        if stat == MI_OK and bits == 0x10:
            return True
        return False

    def PICC_ReadCardSerial(self):
        """Read the card serial number."""
        ser_chk = 0
        ser = [Cmd.PICC_ANTICOLL, 0x20]

        self._wreg(Reg.BitFramingReg, 0x00)
        stat, recv, bits = self._tocard(Cmd.PCD_TRANSCEIVE, ser)

        if stat == MI_OK:
            if len(recv) == 5:
                for i in range(4):
                    ser_chk = ser_chk ^ recv[i]
                if ser_chk != recv[4]:
                    stat = MI_ERR
            else:
                stat = MI_ERR

        if stat == MI_OK:
            self.uid.size = 5
            self.uid.uidByte = recv
            return True
        return False

    def ShowReaderDetails(self):
        """Print reader details to the console."""
        v = self._rreg(Reg.VersionReg)
        print("MFRC522 Software Version: 0x{:02X}".format(v))
        if v == 0x91:
            print("  = v1.0")
        elif v == 0x92:
            print("  = v2.0")
        else:
            print("  (unknown)")
