# 🌡️ Project 09: Temperature and Humidity

Read temperature and humidity from the DHT11 sensor and display on the LCD.

## ⚠️ Required Library Files
Upload these to your ESP32 first! (See [lib/README.md](../../../lib/README.md))
- `i2c_lcd.py`
- `lcd_api.py`

## What You'll Learn
- DHT11 temperature/humidity sensor reading
- Displaying live sensor data on LCD1602

## Pin Connections
| Component | GPIO Pin |
|-----------|----------|
| XHT11/DHT11 Sensor | 17 |
| LCD1602 SDA | 21 (I2C) |
| LCD1602 SCL | 22 (I2C) |

## Scripts

### 🔹 `temp_humidity.py` — Temperature & Humidity Display
Shows temperature (°C) on line 1 and humidity (%RH) on line 2 of the LCD.

## How to Run
1. **First:** Upload `i2c_lcd.py` and `lcd_api.py` to the ESP32
2. Open `temp_humidity.py` in Thonny
3. Click ▶ Run
4. Breathe on the sensor to see humidity rise! 🌡️

---

[← Back to Projects](../../README.md)
