"""
Project 12.1 — WiFi Station Mode
==================================
Connects the ESP32 to your WiFi network and prints the IP address.

⚠️  CHANGE the WiFi name and password below before running!

No extra wiring needed — the ESP32 has built-in WiFi.
"""

import time
import network

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# CHANGE THESE to your WiFi credentials!
ssid_router = 'YOUR_WIFI_NAME'         # ← Your WiFi name
password_router = 'YOUR_WIFI_PASSWORD'  # ← Your WiFi password
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


def STA_Setup(ssid, password):
    """Connect to WiFi in Station mode."""
    print("WiFi Setup starting...")
    print("Connecting to:", ssid)

    sta_if = network.WLAN(network.STA_IF)

    if not sta_if.isconnected():
        # Activate WiFi and connect
        sta_if.active(True)
        sta_if.connect(ssid, password)

        # Wait for connection
        print("Connecting", end="")
        while not sta_if.isconnected():
            print(".", end="")
            time.sleep(0.5)

    # Connected!
    print()
    print("=" * 40)
    print("✅ WiFi Connected!")
    print("   Network:", ssid)
    print("   IP Address:", sta_if.ifconfig()[0])
    print("   Subnet:", sta_if.ifconfig()[1])
    print("   Gateway:", sta_if.ifconfig()[2])
    print("   DNS:", sta_if.ifconfig()[3])
    print("=" * 40)


# Run the WiFi setup
try:
    STA_Setup(ssid_router, password_router)
except Exception as e:
    print("WiFi connection failed:", e)
