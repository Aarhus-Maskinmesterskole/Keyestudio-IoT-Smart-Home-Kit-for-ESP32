"""
Project 4.1 — Play Happy Birthday
===================================
Plays the Happy Birthday melody on the passive buzzer using PWM.
Each buzzer.freq() call sets the tone, and sleep() controls duration.

Pin: GPIO 25 = Passive Buzzer
"""

from machine import Pin, PWM
from time import sleep

# Set up buzzer on GPIO 25
buzzer = PWM(Pin(25))
buzzer.duty(1000)  # Set volume (duty cycle)

# 🎵 Happy Birthday melody
buzzer.freq(294)
sleep(0.25)
buzzer.freq(440)
sleep(0.25)
buzzer.freq(392)
sleep(0.25)
buzzer.freq(532)
sleep(0.25)
buzzer.freq(494)
sleep(0.25)
buzzer.freq(392)
sleep(0.25)
buzzer.freq(440)
sleep(0.25)
buzzer.freq(392)
sleep(0.25)
buzzer.freq(587)
sleep(0.25)
buzzer.freq(532)
sleep(0.25)
buzzer.freq(392)
sleep(0.25)
buzzer.freq(784)
sleep(0.25)
buzzer.freq(659)
sleep(0.25)
buzzer.freq(532)
sleep(0.25)
buzzer.freq(494)
sleep(0.25)
buzzer.freq(440)
sleep(0.25)
buzzer.freq(698)
sleep(0.25)
buzzer.freq(659)
sleep(0.25)
buzzer.freq(532)
sleep(0.25)
buzzer.freq(587)
sleep(0.25)
buzzer.freq(532)
sleep(0.5)

# Stop the buzzer
buzzer.duty(0)
