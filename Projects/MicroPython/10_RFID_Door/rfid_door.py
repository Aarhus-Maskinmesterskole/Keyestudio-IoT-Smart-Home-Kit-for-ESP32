"""
Project 10.1 — RFID Card Door Access
======================================
Swipe the white card to open the door.
Press Button 1 to close the door.
Wrong card shows "error".

⚠️  REQUIRED: Upload mfrc522_i2c.py, mfrc522_config.py, and soft_iic.py first!

Pins:
  RFID RC522 via I2C: SDA = GPIO 21, SCL = GPIO 22, addr = 0x28
  Servo (Door) = GPIO 13
  Button 1 = GPIO 16

Note: The default correct UID sum is 510.
      Run this code and swipe your card to find your card's UID sum.
      Then change the value in the code if needed.
"""

from machine import Pin, PWM
import time
from mfrc522_i2c import mfrc522

# Set up door servo
pwm = PWM(Pin(13))
pwm.freq(50)

# Set up button
button1 = Pin(16, Pin.IN, Pin.PULL_UP)

# Set up RFID reader (I2C address 0x28)
addr = 0x28
scl = 22
sda = 21
rc522 = mfrc522(scl, sda, addr)
rc522.PCD_Init()
rc522.ShowReaderDetails()  # Print reader info

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# CHANGE THIS to your card's UID sum!
CORRECT_UID_SUM = 510
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

data = 0

while True:
    # Check for RFID card
    if rc522.PICC_IsNewCardPresent():
        if rc522.PICC_ReadCardSerial() == True:
            print("Card UID:")

            # Calculate UID sum
            for i in rc522.uid.uidByte[0 : rc522.uid.size]:
                data = data + i

            print("UID sum:", data)

            if data == CORRECT_UID_SUM:
                pwm.duty(128)  # Open door (180°)
                print("✅ Door OPEN")
            else:
                print("❌ Wrong card!")

            data = 0  # Reset for next card

    # Button 1 → Close door
    btn_val1 = button1.value()
    if btn_val1 == 0:
        pwm.duty(25)  # Close door (0°)
        print("🔒 Door CLOSED")

    time.sleep(1)
