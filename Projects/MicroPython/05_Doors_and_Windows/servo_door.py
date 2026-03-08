"""
Project 5.1 — Control the Door Servo
======================================
Makes the door servo rotate between 0°, 90°, and 180°.

Pin: GPIO 13 = Door Servo

Servo angle to duty cycle:
  0°   → duty = 25
  90°  → duty = 77
  180° → duty = 128
"""

from machine import Pin, PWM
import time

# Set up servo on GPIO 13 at 50Hz (standard for servos)
pwm = PWM(Pin(13))
pwm.freq(50)

# Angle constants
angle_0 = 25     # 0 degrees
angle_90 = 77    # 90 degrees
angle_180 = 128  # 180 degrees

while True:
    pwm.duty(angle_0)    # Door position: 0°
    time.sleep(1)

    pwm.duty(angle_90)   # Door position: 90°
    time.sleep(1)

    pwm.duty(angle_180)  # Door position: 180°
    time.sleep(1)
