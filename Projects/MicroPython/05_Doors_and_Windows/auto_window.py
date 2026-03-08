"""
Project 5.2 — Auto-Close Window on Rain
=========================================
The window opens by default. When the rain/steam sensor detects water
(voltage > 0.6V), the window closes automatically.

Pins:
  Servo (Window) = GPIO 5
  Rain/Steam Sensor = GPIO 34 (ADC input)
"""

from machine import ADC, Pin, PWM
import time

# Set up window servo on GPIO 5 at 50Hz
pwm = PWM(Pin(5))
pwm.freq(50)

# Set up rain sensor on GPIO 34 (analog input)
adc = ADC(Pin(34))
adc.atten(ADC.ATTN_11DB)    # Full range: 0-3.3V
adc.width(ADC.WIDTH_12BIT)  # 12-bit resolution: 0-4095

try:
    while True:
        # Read sensor value and convert to voltage
        adc_val = adc.read()
        voltage = adc_val / 4095.0 * 3.3

        print("ADC:", adc_val, "Voltage:", round(voltage, 2), "V")

        if voltage > 0.6:
            # Rain detected! → Close window
            pwm.duty(46)
            print("Rain detected! Window CLOSING")
        else:
            # No rain → Open window
            pwm.duty(100)
            print("No rain. Window OPEN")

        time.sleep(0.1)

except:
    pass
