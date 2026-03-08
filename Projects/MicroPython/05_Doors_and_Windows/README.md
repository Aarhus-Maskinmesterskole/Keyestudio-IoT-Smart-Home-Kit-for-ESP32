# 🚪 Project 05: Automatic Doors and Windows

Control the door servo and make the window close automatically when it "rains".

## What You'll Learn
- Servo motor control with PWM
- ADC (analog) reading from rain/steam sensor
- Combining sensors with actuators

## Pin Connections
| Component | GPIO Pin |
|-----------|----------|
| Servo (Door) | 13 |
| Servo (Window) | 5 |
| Rain/Steam Sensor | 34 (ADC) |

## Servo Angle Reference
| Angle | PWM Duty |
|-------|----------|
| 0° | 25 |
| 90° | 77 |
| 180° | 128 |

## Scripts

### 🔹 `servo_door.py` — Control the Door Servo
Makes the door servo rotate between 0°, 90°, and 180°.

### 🔹 `auto_window.py` — Auto-Close Window on Rain
The window opens by default. When the rain sensor detects water (touch it with wet fingers), the window closes automatically.

## How to Run
1. Open the `.py` file in Thonny
2. Click ▶ Run
3. Watch the door/window move! 🚪

---

[← Back to Projects](../../README.md)
