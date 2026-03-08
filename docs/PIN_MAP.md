# 🔌 Complete Pin Mapping — ESP32 Smart Home Kit

This is the complete pin reference for all sensors and modules on the Keyestudio IoT Smart Home Kit (KS5009).

---

## GPIO Pin Reference

| GPIO | Component | Type | Notes |
|------|-----------|------|-------|
| **5** | Servo (Window) | PWM Output | 180° servo, controls window open/close |
| **12** | Yellow LED | Digital Output | Simple LED module |
| **13** | Servo (Door) | PWM Output | 180° servo, controls door open/close |
| **14** | PIR Motion Sensor | Digital Input | HIGH = motion detected |
| **16** | Button 1 | Digital Input (PULL_UP) | LOW when pressed |
| **17** | XHT11 / DHT11 | Digital (1-Wire) | Temperature & humidity sensor |
| **18** | Fan Motor INB | PWM Output | 130 DC motor negative control |
| **19** | Fan Motor INA | PWM Output | 130 DC motor positive control |
| **21** | I2C SDA | I2C Data | Shared by LCD1602 + RFID RC522 |
| **22** | I2C SCL | I2C Clock | Shared by LCD1602 + RFID RC522 |
| **23** | Gas Sensor (MQ2) | Digital Input (PULL_UP) | HIGH = gas detected |
| **25** | Passive Buzzer | PWM Output | Frequency controlled for tones |
| **26** | SK6812 RGB LEDs | Digital Output (NeoPixel) | 4 addressable RGB LEDs |
| **27** | Button 2 | Digital Input (PULL_UP) | LOW when pressed |
| **34** | Rain/Steam Sensor | ADC Input | Analog value 0–4096 |

---

## I2C Devices

| Device | I2C Address | SDA | SCL |
|--------|-------------|-----|-----|
| LCD1602 Display | `0x27` | GPIO 21 | GPIO 22 |
| RFID RC522 Module | `0x28` | GPIO 21 | GPIO 22 |

---

## Fan Motor Control Logic

The 130 DC motor uses two PWM pins (INA and INB). The difference determines direction:

| Condition | Result |
|-----------|--------|
| `INA - INB ≤ -45` | Rotate clockwise |
| `INA - INB ≥ 45` | Rotate anticlockwise |
| `INA == 0, INB == 0` | Stop |

PWM duty cycle range: **0–1023**

---

## Servo Angle Reference

The servos use 50Hz PWM. Duty cycle values for angles:

| Angle | Duty Cycle |
|-------|-----------|
| 0° | 25 |
| 45° | 51 |
| 90° | 77 |
| 135° | 102 |
| 180° | 128 |

---

## Visual Pin Layout

```
ESP32 PLUS Board — Smart Home Kit Connections

          ┌─────────────────────┐
          │                     │
  LED ◄───┤ GPIO 12             │
  BTN1 ──►│ GPIO 16             │
  BTN2 ──►│ GPIO 27             │
  PIR ───►│ GPIO 14             │
  BUZ ◄───┤ GPIO 25             │
  DHT ◄──►│ GPIO 17             │
  GAS ───►│ GPIO 23             │
  RAIN ──►│ GPIO 34 (ADC)       │
  RGB ◄───┤ GPIO 26             │
          │                     │
  DOOR ◄──┤ GPIO 13 (Servo)     │
  WIN ◄───┤ GPIO 5  (Servo)     │
  FAN+ ◄──┤ GPIO 19 (INA)       │
  FAN- ◄──┤ GPIO 18 (INB)       │
          │                     │
  SDA ◄──►│ GPIO 21 (I2C)       │
  SCL ◄──►│ GPIO 22 (I2C)       │
          │                     │
          └─────────────────────┘
```

---

[← Back to main README](../README.md)
