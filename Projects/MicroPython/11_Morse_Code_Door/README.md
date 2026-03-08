# 🔐 Project 11: Morse Code Door

Use Morse code as a password to open the door!

## ⚠️ Required Library Files
Upload these to your ESP32 first! (See [lib/README.md](../../../lib/README.md))
- `i2c_lcd.py`
- `lcd_api.py`

## What You'll Learn
- Button press duration detection (short = dot, long = dash)
- String comparison for password checking
- LCD display feedback

## Pin Connections
| Component | GPIO Pin |
|-----------|----------|
| Button 1 | 16 (input password) |
| Button 2 | 27 (confirm password) |
| Servo (Door) | 13 |
| LCD1602 SDA | 21 (I2C) |
| LCD1602 SCL | 22 (I2C) |

## How It Works
1. LCD shows "Enter password"
2. **Short press** Button 1 → adds `.` (dot)
3. **Long press** Button 1 → adds `-` (dash)
4. Press **Button 2** to confirm
5. Default password: `-.-` (dash-dot-dash)
6. ✅ Correct → Door opens + LCD shows "open"
7. ❌ Wrong → Door stays closed + LCD shows "error"

## Scripts

### 🔹 `morse_door.py` — Morse Code Password Door
Enter the Morse code password to open the door.

## How to Run
1. **First:** Upload `i2c_lcd.py` and `lcd_api.py` to the ESP32
2. Open `morse_door.py` in Thonny
3. Click ▶ Run
4. Enter the password: long-short-long (-.-) 🔐

---

[← Back to Projects](../../README.md)
