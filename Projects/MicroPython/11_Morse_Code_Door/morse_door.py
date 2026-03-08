"""
Project 11.1 — Morse Code Password Door
==========================================
Enter a Morse code password to open the door.
  - Short press Button 1 = "." (dot)
  - Long press Button 1 = "-" (dash)
  - Press Button 2 = Confirm password

Default password: -.- (dash-dot-dash)

⚠️  REQUIRED: Upload i2c_lcd.py and lcd_api.py to ESP32 first!

Pins:
  Button 1 = GPIO 16 (input)
  Button 2 = GPIO 27 (confirm)
  Servo (Door) = GPIO 13
  LCD1602 I2C: SDA = GPIO 21, SCL = GPIO 22
"""

from machine import Pin, PWM
from time import sleep_ms
from machine import SoftI2C
from i2c_lcd import I2cLcd

# LCD setup
DEFAULT_I2C_ADDR = 0x27
i2c = SoftI2C(scl=Pin(22), sda=Pin(21), freq=100000)
lcd = I2cLcd(i2c, DEFAULT_I2C_ADDR, 2, 16)

# Button setup
button1 = Pin(16, Pin.IN, Pin.PULL_UP)
button2 = Pin(27, Pin.IN, Pin.PULL_UP)

# Door servo setup
pwm = PWM(Pin(13))
pwm.freq(50)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# CHANGE THIS to set your own password!
correct_password = "-.-"
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

password = ""       # Current input
time_count = 0      # Track button press duration

lcd.putstr("Enter password")

while True:
    btn_val1 = button1.value()

    if btn_val1 == 0:  # Button 1 pressed
        sleep_ms(10)   # Debounce

        # Count how long the button is held
        while btn_val1 == 0:
            time_count = time_count + 1
            sleep_ms(200)  # Count in 200ms steps
            btn_val1 = button1.value()

        if btn_val1 == 1:  # Button released
            if time_count > 3:
                # Long press (> 600ms) → Dash "-"
                password = password + "-"
            else:
                # Short press → Dot "."
                password = password + "."

            lcd.clear()
            lcd.putstr('{}'.format(password))
            print("Password so far:", password)
            time_count = 0

    # Button 2 = Confirm password
    btn_val2 = button2.value()

    if btn_val2 == 0:
        if password == correct_password:
            # ✅ Correct password!
            lcd.clear()
            lcd.putstr("open")
            pwm.duty(128)          # Open door (180°)
            print("✅ Door OPEN!")
            password = ""          # Reset
            sleep_ms(1000)
        else:
            # ❌ Wrong password!
            lcd.clear()
            lcd.putstr("error")
            pwm.duty(25)           # Close door (0°)
            print("❌ Wrong password!")
            sleep_ms(2000)

            lcd.clear()
            lcd.putstr("enter again")
            password = ""          # Reset
