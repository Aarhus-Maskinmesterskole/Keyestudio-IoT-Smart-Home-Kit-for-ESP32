# 🌀 Project 07: Fan

Control the 130 DC motor fan with PWM speed control.

## What You'll Learn
- DC motor control with two PWM pins
- Motor direction and speed control
- Button-activated on/off switching

## Pin Connections
| Component | GPIO Pin |
|-----------|----------|
| Fan Motor INA | 19 |
| Fan Motor INB | 18 |
| Button 1 | 16 |

## Motor Control Logic
| Condition | Result |
|-----------|--------|
| INA = 0, INB > 0 | Rotate clockwise |
| INA > 0, INB = 0 | Rotate anticlockwise |
| INA = 0, INB = 0 | Stop |

## Scripts

### 🔹 `fan_demo.py` — Fan Speed Demo
Rotates clockwise, stops, rotates anticlockwise, stops — in a loop.

### 🔹 `fan_button_control.py` — Button-Controlled Fan
Press Button 1 to start the fan, press again to stop.

## How to Run
1. Open the `.py` file in Thonny
2. Click ▶ Run
3. Watch the fan spin! 🌀

---

[← Back to Projects](../../README.md)
