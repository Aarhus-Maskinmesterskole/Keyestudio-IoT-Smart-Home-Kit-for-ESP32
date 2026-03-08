# 📺 Project 08: LCD1602 Display

Display text on the LCD1602 screen and create a gas alarm system.

## ⚠️ Required Library Files
Upload these to your ESP32 first! (See [lib/README.md](../../../lib/README.md))
- `i2c_lcd.py`
- `lcd_api.py`

## What You'll Learn
- I2C communication with LCD1602
- Displaying text and sensor values
- Gas sensor alarm system

## Pin Connections
| Component | GPIO Pin |
|-----------|----------|
| LCD1602 SDA | 21 (I2C) |
| LCD1602 SCL | 22 (I2C) |
| Gas Sensor (MQ2) | 23 |

## Scripts

### 🔹 `lcd_hello.py` — Display Hello
Shows "Hello" on line 1 and "keyestudio" on line 2 of the LCD.

### 🔹 `gas_alarm.py` — Gas Alarm System
Displays "Safety" normally. When the gas sensor detects dangerous gas, displays "dangerous".

## How to Run
1. **First:** Upload `i2c_lcd.py` and `lcd_api.py` to the ESP32 (see lib/README.md)
2. Open the `.py` file in Thonny
3. Click ▶ Run
4. Check the LCD display! 📺

---

[← Back to Projects](../../README.md)
