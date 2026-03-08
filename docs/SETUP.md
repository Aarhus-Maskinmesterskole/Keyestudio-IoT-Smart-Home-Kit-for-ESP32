# 🛠️ Setup Guide — Getting Started with ESP32 + MicroPython

This guide will help you set up everything you need to start programming your Keyestudio Smart Home Kit.

---

## Step 1: Install Thonny IDE

Thonny is a free, beginner-friendly Python IDE that works with MicroPython on ESP32.

1. Go to [thonny.org](https://thonny.org/)
2. Download for your operating system (Windows / Mac / Linux)
3. Install and open Thonny

---

## Step 2: Connect the ESP32 Board

1. Use the **USB cable** from the kit to connect the ESP32 PLUS board to your computer
2. Wait for the driver to install (if needed)

### ⚠️ Windows Driver Note
If your computer doesn't recognize the board, you may need to install the **CP2102 USB driver**:
- Download from: [Silicon Labs CP210x Drivers](https://www.silabs.com/developers/usb-to-uart-bridge-vcp-drivers)
- Install and restart your computer

---

## Step 3: Configure Thonny for ESP32

1. Open Thonny
2. Go to **Tools** → **Options** → **Interpreter**
3. Select **MicroPython (ESP32)** from the dropdown
4. Select the correct **COM port** (or `/dev/ttyUSB0` on Linux)
5. Click **OK**

---

## Step 4: Install MicroPython Firmware

If your ESP32 doesn't already have MicroPython firmware:

1. In Thonny, go to **Tools** → **Options** → **Interpreter**
2. Click **"Install or update MicroPython"** (bottom right)
3. Select:
   - **Target port**: Your ESP32's COM port
   - **MicroPython family**: ESP32
   - **Variant**: Espressif • ESP32
4. Click **Install**
5. Wait for the installation to complete (~30 seconds)
6. Click **Close** and then **OK**

You should now see the MicroPython REPL (`>>>`) in the Shell window at the bottom of Thonny.

---

## Step 5: Upload Library Files

Some projects require library files on the ESP32. Here's how to upload them:

1. In Thonny, go to **View** → **Files** (to show the file browser)
2. In the left panel ("This computer"), navigate to the `lib/` folder of this repo
3. Right-click on a library file (e.g., `i2c_lcd.py`)
4. Select **"Upload to /"** 
5. Repeat for each library file needed

### Which libraries are needed?

| Project | Libraries to upload |
|---------|-------------------|
| 08 LCD1602 Display | `i2c_lcd.py`, `lcd_api.py` |
| 09 Temp & Humidity | `i2c_lcd.py`, `lcd_api.py` |
| 10 RFID Door | `mfrc522_i2c.py`, `mfrc522_config.py`, `soft_iic.py` |
| 11 Morse Code Door | `i2c_lcd.py`, `lcd_api.py` |

---

## Step 6: Run Your First Program! 🎉

1. Open `Projects/MicroPython/01_LED/led_blink.py` in Thonny
2. Click the green **▶ Run** button (or press F5)
3. Watch the yellow LED on the smart home blink! 💡

### 💡 Tip: Run vs Save
- **▶ Run** (F5): Runs the script once (stops when you disconnect)
- **Save to ESP32**: Save the file as `main.py` on the ESP32 to run it automatically on boot

---

## Troubleshooting

### "Cannot connect to ESP32"
- Try a different USB cable (some are charge-only, without data)
- Try a different USB port
- Install the CP2102 driver (see Step 2)
- Press the **EN/Reset** button on the ESP32 board

### "Module not found" error
- You need to upload the required library files (see Step 5)
- Make sure the file is saved to the root `/` of the ESP32, not in a subfolder

### "Permission denied" (Linux/Mac)
- Add your user to the `dialout` group: `sudo usermod -a -G dialout $USER`
- Log out and log back in

---

[← Back to main README](../README.md)
