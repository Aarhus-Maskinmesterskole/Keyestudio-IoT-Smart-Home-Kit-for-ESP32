# 🔑 Project 10: RFID Door

Use the RFID RC522 card reader to open the door by swiping a card.

## ⚠️ Required Library Files
Upload these to your ESP32 first! (See [lib/README.md](../../../lib/README.md))
- `mfrc522_i2c.py`
- `mfrc522_config.py`
- `soft_iic.py`

## What You'll Learn
- RFID card reading via I2C
- Card UID identification
- Servo control based on RFID authentication

## Pin Connections
| Component | GPIO Pin |
|-----------|----------|
| RFID RC522 (I2C) | SDA=21, SCL=22, addr=0x28 |
| Servo (Door) | 13 |
| Button 1 | 16 |

## How It Works
- Swipe the **white card** (included in kit) → Door opens
- Swipe the **blue key fob** → Shows "error" (wrong card)
- Press **Button 1** → Door closes

> 💡 **Note:** The default UID check is `510`. Your card might have a different UID. Run the code and check the printed value to find your card's UID sum.

## Scripts

### 🔹 `rfid_door.py` — RFID Card Access
Swipe the card to open, press button to close.

## How to Run
1. **First:** Upload the 3 RFID library files to the ESP32
2. Open `rfid_door.py` in Thonny
3. Click ▶ Run
4. Swipe your card! 🔑

---

[← Back to Projects](../../README.md)
