# 🏠 Keyestudio IoT Smart Home Kit for ESP32

[![MicroPython](https://img.shields.io/badge/MicroPython-Ready-green?logo=micropython)](https://micropython.org/)
[![ESP32](https://img.shields.io/badge/Board-ESP32_PLUS-blue)](https://docs.keyestudio.com/projects/KS5009/en/latest/docs/index.html)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

> **Beginner-friendly MicroPython code for the [Keyestudio IoT Smart Home Kit (KS5009)](https://docs.keyestudio.com/projects/KS5009/en/latest/docs/index.html).**
> Every script is copy-paste ready — just open Thonny, paste, and run! 🚀

---

## ⚡ Quick Start (3 steps)

1. **Install Thonny** — Download from [thonny.org](https://thonny.org/) and install MicroPython firmware → [Setup Guide](docs/SETUP.md)
2. **Clone this repo** — `git clone https://github.com/your-user/Keyestudio-IoT-Smart-Home-Kit-for-ESP32.git`
3. **Open a `.py` file in Thonny** — Click ▶ Run and watch the magic! ✨

> 📖 **First time?** Read the full [Setup Guide](docs/SETUP.md) for step-by-step instructions with screenshots.

---

## 📋 Projects Overview

| # | Project | What it does | Files |
|---|---------|-------------|-------|
| 01 | [💡 LED](Projects/MicroPython/01_LED/) | Blink & breathing LED | `led_blink.py`, `led_breathing.py` |
| 02 | [🔘 Table Lamp](Projects/MicroPython/02_Table_Lamp/) | Button-controlled lamp | `button_read.py`, `table_lamp.py` |
| 03 | [👋 PIR Motion Sensor](Projects/MicroPython/03_PIR_Motion_Sensor/) | Detect movement, turn on LED | `pir_read.py`, `pir_led.py` |
| 04 | [🎵 Play Music](Projects/MicroPython/04_Play_Music/) | Buzzer plays Happy Birthday | `happy_birthday.py` |
| 05 | [🚪 Doors & Windows](Projects/MicroPython/05_Doors_and_Windows/) | Servo door + auto-close window | `servo_door.py`, `auto_window.py` |
| 06 | [🌈 Atmosphere Lamp](Projects/MicroPython/06_Atmosphere_Lamp/) | RGB LED effects + button control | `rgb_demo.py`, `rgb_button_control.py` |
| 07 | [🌀 Fan](Projects/MicroPython/07_Fan/) | Motor fan + button control | `fan_demo.py`, `fan_button_control.py` |
| 08 | [📺 LCD1602 Display](Projects/MicroPython/08_LCD1602_Display/) | Text display + gas alarm | `lcd_hello.py`, `gas_alarm.py` |
| 09 | [🌡️ Temp & Humidity](Projects/MicroPython/09_Temperature_Humidity/) | DHT11 sensor on LCD | `temp_humidity.py` |
| 10 | [🔑 RFID Door](Projects/MicroPython/10_RFID_Door/) | Swipe card to open door | `rfid_door.py` |
| 11 | [🔐 Morse Code Door](Projects/MicroPython/11_Morse_Code_Door/) | Morse password door lock | `morse_door.py` |
| 12 | [📶 WiFi](Projects/MicroPython/12_WiFi/) | Connect to WiFi network | `wifi_station.py` |

---

## 🔌 Pin Mapping (Quick Reference)

| Component | GPIO Pin |
|-----------|----------|
| Yellow LED | 12 |
| Button 1 | 16 |
| Button 2 | 27 |
| PIR Motion Sensor | 14 |
| Passive Buzzer | 25 |
| Servo (Door) | 13 |
| Servo (Window) | 5 |
| SK6812 RGB LEDs | 26 |
| Fan Motor INA | 19 |
| Fan Motor INB | 18 |
| Gas Sensor (MQ2) | 23 |
| Rain/Steam Sensor | 34 (ADC) |
| DHT11 Temp/Humidity | 17 |
| I2C SCL | 22 |
| I2C SDA | 21 |
| RFID RC522 (I2C) | SDA=21, SCL=22, addr=0x28 |
| LCD1602 (I2C) | SDA=21, SCL=22, addr=0x27 |

📖 Full pin reference → [docs/PIN_MAP.md](docs/PIN_MAP.md)

---

## 📁 Folder Structure

```
├── README.md                      ← You are here
├── docs/
│   ├── SETUP.md                   ← Getting started guide
│   └── PIN_MAP.md                 ← Complete pin reference
├── lib/                           ← Library files (upload to ESP32)
│   ├── i2c_lcd.py
│   ├── lcd_api.py
│   ├── mfrc522_i2c.py
│   ├── mfrc522_config.py
│   └── soft_iic.py
├── Projects/
│   └── MicroPython/               ← 12 beginner projects
│       ├── 01_LED/
│       ├── 02_Table_Lamp/
│       ├── ...
│       └── 12_WiFi/
└── Kit list/                      ← Hardware parts list
```

---

## 📚 Library Files

Some projects need extra library files on your ESP32. See [lib/README.md](lib/README.md) for instructions.

| Library | Needed by | Purpose |
|---------|-----------|---------|
| `i2c_lcd.py` + `lcd_api.py` | Projects 8, 9, 11 | LCD1602 display driver |
| `mfrc522_i2c.py` + `mfrc522_config.py` + `soft_iic.py` | Project 10 | RFID RC522 card reader |

---

## 🔗 Official Resources

- 📖 [Keyestudio Official Tutorial](https://docs.keyestudio.com/projects/KS5009/en/latest/docs/index.html)
- 🛒 [Kit Product Page](https://www.keyestudio.com/)
- 📦 [MicroPython Documentation](https://docs.micropython.org/en/latest/)
- 💻 [Thonny IDE](https://thonny.org/)
- 💻 [MicroPython Firmware](https://micropython.org/download/esp32/)
-  [Antigravity IDE](https://antigravity.dev/) 

---

## 🤝 Contributing

Found a bug or want to add a project? Pull requests are welcome!

## 📄 License

This project is open source. The code examples are based on the [Keyestudio KS5009 tutorial](https://docs.keyestudio.com/projects/KS5009/en/latest/docs/index.html).