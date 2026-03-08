# 📦 Library Files

These library files need to be uploaded to your ESP32 before running certain projects.

## How to Upload

1. Open **Thonny IDE**
2. Go to **View** → **Files** (shows file browser panels)
3. In the left panel ("This computer"), navigate to this `lib/` folder
4. **Right-click** on the file you need → Select **"Upload to /"**
5. The file will be saved to the root of the ESP32's filesystem

## Which files do I need?

| File | Required by | Description |
|------|-------------|-------------|
| `i2c_lcd.py` | Projects 08, 09, 11 | I2C driver for LCD1602 display |
| `lcd_api.py` | Projects 08, 09, 11 | LCD API base class |
| `mfrc522_i2c.py` | Project 10 | RFID RC522 I2C driver |
| `mfrc522_config.py` | Project 10 | RFID RC522 configuration |
| `soft_iic.py` | Project 10 | Software I2C implementation |

> 💡 **Tip:** You can upload all 5 files at once — they don't take much space and then every project will work.

---

[← Back to main README](../README.md)
