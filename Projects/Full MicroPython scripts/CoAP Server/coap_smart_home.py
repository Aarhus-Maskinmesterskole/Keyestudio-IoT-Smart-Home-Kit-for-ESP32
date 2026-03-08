"""
Build by AI in Antigravity 2026-03-08

🏠 Smart Home CoAP Server (Alt-i-én fil)
==========================================
This script turns your ESP32 into a CoAP server.
Use CoAP tools (coap-client, aiocoap, Node-RED) to read sensor
data and control actuators over the lightweight IoT protocol!

CoAP runs on UDP port 5683 — much lighter than HTTP!

You can:
  ✅ Read temperature, humidity, motion, gas, rain (GET)
  ✅ Read device states: LED, fan, door, window, RGB (GET)
  ✅ Control devices: LED, fan, door, window, RGB, buzzer (PUT)
  ✅ Get all data at once with GET /sensors

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️  CHANGE THESE TWO LINES TO YOUR WIFI! ⚠️
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# STEP 1: Change these to YOUR WiFi!
WIFI_NAME = 'YOUR_WIFI_NAME'           # ← Put your WiFi name here
WIFI_PASSWORD = 'YOUR_WIFI_PASSWORD'   # ← Put your WiFi password here
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

import network
import socket
import struct
import time
import json
import gc
import dht
import neopixel
from machine import Pin, PWM, ADC


# ═════════════════════════════════════
# BUILT-IN CoAP LIBRARY (RFC 7252)
# No extra files needed!
# ═════════════════════════════════════

COAP_PORT = 5683
COAP_VERSION = 1

# Method codes
COAP_GET = 1
COAP_POST = 2
COAP_PUT = 3
COAP_DELETE = 4

# Response codes
COAP_CREATED = 65       # 2.01
COAP_DELETED = 66       # 2.02
COAP_VALID = 67         # 2.03
COAP_CHANGED = 68       # 2.04
COAP_CONTENT = 69       # 2.05
COAP_BAD_REQUEST = 128  # 4.00
COAP_NOT_FOUND = 132    # 4.04
COAP_METHOD_NOT_ALLOWED = 133  # 4.05

# Message types
COAP_CON = 0   # Confirmable
COAP_NON = 1   # Non-confirmable
COAP_ACK = 2   # Acknowledgement
COAP_RST = 3   # Reset

# Option numbers
OPT_URI_PATH = 11
OPT_CONTENT_FORMAT = 12

# Content formats
CT_TEXT = 0
CT_JSON = 50


def coap_parse(data):
    """Parse raw bytes into a dict with CoAP message fields."""
    if len(data) < 4:
        return None

    byte0 = data[0]
    tkl = byte0 & 0x0F
    pkt = {
        'ver': (byte0 >> 6) & 0x03,
        'type': (byte0 >> 4) & 0x03,
        'code': data[1],
        'mid': struct.unpack('!H', data[2:4])[0],
        'token': b'',
        'options': [],
        'payload': b''
    }

    offset = 4
    if tkl > 0:
        pkt['token'] = data[offset:offset + tkl]
        offset += tkl

    # Parse options
    prev_opt = 0
    while offset < len(data):
        if data[offset] == 0xFF:
            offset += 1
            break
        delta = (data[offset] >> 4) & 0x0F
        length = data[offset] & 0x0F
        offset += 1

        if delta == 13:
            delta = data[offset] + 13
            offset += 1
        elif delta == 14:
            delta = struct.unpack('!H', data[offset:offset+2])[0] + 269
            offset += 2
        if length == 13:
            length = data[offset] + 13
            offset += 1
        elif length == 14:
            length = struct.unpack('!H', data[offset:offset+2])[0] + 269
            offset += 2

        opt_num = prev_opt + delta
        pkt['options'].append((opt_num, data[offset:offset + length]))
        offset += length
        prev_opt = opt_num

    if offset < len(data):
        pkt['payload'] = data[offset:]

    return pkt


def coap_get_uri(pkt):
    """Extract URI path from parsed CoAP packet."""
    parts = []
    for num, val in pkt['options']:
        if num == OPT_URI_PATH:
            parts.append(val.decode())
    return '/'.join(parts)


def coap_build_response(msg_type, code, msg_id, token, payload=b''):
    """Build a CoAP response as bytes."""
    if isinstance(payload, str):
        payload = payload.encode()
    tkl = len(token)
    byte0 = (COAP_VERSION << 6) | (msg_type << 4) | tkl
    data = struct.pack('!BBH', byte0, code, msg_id) + token
    if payload:
        # Content-Format option: delta=12, length=1, value=50 (JSON)
        data += struct.pack('!BB', (OPT_CONTENT_FORMAT << 4) | 1, CT_JSON)
        data += b'\xFF' + payload
    return data


# ═════════════════════════════════════
# SET UP ALL THE SMART HOME COMPONENTS
# ═════════════════════════════════════

# LED (GPIO 12)
led = Pin(12, Pin.OUT)
led.value(0)

# Buttons (GPIO 16 and 27)
button1 = Pin(16, Pin.IN, Pin.PULL_UP)
button2 = Pin(27, Pin.IN, Pin.PULL_UP)

# PIR Motion Sensor (GPIO 14)
pir = Pin(14, Pin.IN)

# Passive Buzzer (GPIO 25) — plain pin = fully silent
buzzer_pin = 25
Pin(buzzer_pin, Pin.OUT).value(0)

# Door Servo (GPIO 13)
door_servo = PWM(Pin(13), freq=50)
door_servo.duty(25)
door_open = False

# Window Servo (GPIO 5)
window_servo = PWM(Pin(5), freq=50)
window_servo.duty(25)
window_open = False

# Fan Motor (GPIO 19 = forward, GPIO 18 = backward)
fan_forward = Pin(19, Pin.OUT)
fan_backward = Pin(18, Pin.OUT)
fan_forward.value(0)
fan_backward.value(0)
fan_on = False

# SK6812 RGB Atmosphere Lamp (GPIO 26, 4 LEDs)
np_pin = Pin(26, Pin.OUT)
np = neopixel.NeoPixel(np_pin, 4)
current_color = 0

# Rain/Steam Sensor (GPIO 34, ADC)
rain_adc = ADC(Pin(34))
rain_adc.atten(ADC.ATTN_11DB)
rain_adc.width(ADC.WIDTH_12BIT)

# MQ2 Gas Sensor (GPIO 35, ADC) — analog, 0-4095
gas_adc = ADC(Pin(35))
gas_adc.atten(ADC.ATTN_11DB)
gas_adc.width(ADC.WIDTH_12BIT)

# DHT11 Temperature & Humidity Sensor (GPIO 17)
dht_sensor = dht.DHT11(Pin(17))


# ═════════════════════════════════════
# HELPER FUNCTIONS
# ═════════════════════════════════════

def set_rgb(color_index):
    global current_color
    current_color = color_index
    b = 80
    colors = [(0,0,0), (b,0,0), (0,b,0), (0,0,b), (b,b,b)]
    c = colors[color_index]
    for i in range(4):
        np[i] = c
    np.write()

COLOR_NAMES = ["off", "red", "green", "blue", "white"]

def buzzer_off():
    try:
        PWM(Pin(buzzer_pin)).deinit()
    except:
        pass
    Pin(buzzer_pin, Pin.OUT).value(0)


def play_buzzer_tone():
    b = PWM(Pin(buzzer_pin))
    for note in [523, 659, 784, 1047]:
        b.freq(note)
        b.duty(512)
        time.sleep_ms(150)
    b.deinit()
    Pin(buzzer_pin, Pin.OUT).value(0)


set_rgb(0)


# ═════════════════════════════════════
# CoAP RESOURCE HANDLERS
# Each handler takes (method, payload)
# and returns (response_code, json_string)
# ═════════════════════════════════════

def res_sensors(method, payload):
    if method != COAP_GET:
        return COAP_METHOD_NOT_ALLOWED, '{"error":"use GET"}'
    try:
        dht_sensor.measure()
        t, h = dht_sensor.temperature(), dht_sensor.humidity()
    except:
        t, h = None, None
    return COAP_CONTENT, json.dumps({
        "temperature": t, "humidity": h,
        "motion": pir.value(), "gas": gas_adc.read(),
        "rain": rain_adc.read(), "led": led.value(),
        "fan": "on" if fan_on else "off",
        "door": "open" if door_open else "closed",
        "window": "open" if window_open else "closed",
        "rgb": COLOR_NAMES[current_color]
    })


def res_temperature(method, payload):
    if method != COAP_GET:
        return COAP_METHOD_NOT_ALLOWED, '{"error":"use GET"}'
    try:
        dht_sensor.measure()
        v = dht_sensor.temperature()
    except:
        v = None
    return COAP_CONTENT, json.dumps({"temperature": v})


def res_humidity(method, payload):
    if method != COAP_GET:
        return COAP_METHOD_NOT_ALLOWED, '{"error":"use GET"}'
    try:
        dht_sensor.measure()
        v = dht_sensor.humidity()
    except:
        v = None
    return COAP_CONTENT, json.dumps({"humidity": v})


def res_motion(method, payload):
    if method != COAP_GET:
        return COAP_METHOD_NOT_ALLOWED, '{"error":"use GET"}'
    return COAP_CONTENT, json.dumps({"motion": pir.value()})


def res_gas(method, payload):
    if method != COAP_GET:
        return COAP_METHOD_NOT_ALLOWED, '{"error":"use GET"}'
    return COAP_CONTENT, json.dumps({"gas": gas_adc.read()})


def res_rain(method, payload):
    if method != COAP_GET:
        return COAP_METHOD_NOT_ALLOWED, '{"error":"use GET"}'
    return COAP_CONTENT, json.dumps({"rain": rain_adc.read()})


def res_led(method, payload):
    if method == COAP_GET:
        return COAP_CONTENT, json.dumps({"led": led.value()})
    elif method == COAP_PUT:
        cmd = payload.decode().strip().lower()
        if cmd == "on":
            led.value(1)
        elif cmd == "off":
            led.value(0)
        return COAP_CHANGED, json.dumps({"led": led.value()})
    return COAP_METHOD_NOT_ALLOWED, '{"error":"use GET or PUT"}'


def res_fan(method, payload):
    global fan_on
    if method == COAP_GET:
        return COAP_CONTENT, json.dumps({"fan": "on" if fan_on else "off"})
    elif method == COAP_PUT:
        cmd = payload.decode().strip().lower()
        if cmd == "on":
            fan_on = True
            fan_forward.value(0)
            fan_backward.value(1)
        elif cmd == "off":
            fan_on = False
            fan_forward.value(0)
            fan_backward.value(0)
        return COAP_CHANGED, json.dumps({"fan": "on" if fan_on else "off"})
    return COAP_METHOD_NOT_ALLOWED, '{"error":"use GET or PUT"}'


def res_door(method, payload):
    global door_open
    if method == COAP_GET:
        return COAP_CONTENT, json.dumps({"door": "open" if door_open else "closed"})
    elif method == COAP_PUT:
        cmd = payload.decode().strip().lower()
        if cmd == "open":
            door_open = True
            door_servo.duty(128)
        elif cmd == "close":
            door_open = False
            door_servo.duty(25)
        return COAP_CHANGED, json.dumps({"door": "open" if door_open else "closed"})
    return COAP_METHOD_NOT_ALLOWED, '{"error":"use GET or PUT"}'


def res_window(method, payload):
    global window_open
    if method == COAP_GET:
        return COAP_CONTENT, json.dumps({"window": "open" if window_open else "closed"})
    elif method == COAP_PUT:
        cmd = payload.decode().strip().lower()
        if cmd == "open":
            window_open = True
            window_servo.duty(128)
        elif cmd == "close":
            window_open = False
            window_servo.duty(25)
        return COAP_CHANGED, json.dumps({"window": "open" if window_open else "closed"})
    return COAP_METHOD_NOT_ALLOWED, '{"error":"use GET or PUT"}'


def res_rgb(method, payload):
    if method == COAP_GET:
        return COAP_CONTENT, json.dumps({"rgb": COLOR_NAMES[current_color]})
    elif method == COAP_PUT:
        try:
            c = int(payload.decode().strip())
            if 0 <= c <= 4:
                set_rgb(c)
        except:
            pass
        return COAP_CHANGED, json.dumps({"rgb": COLOR_NAMES[current_color]})
    return COAP_METHOD_NOT_ALLOWED, '{"error":"use GET or PUT"}'


def res_buzzer(method, payload):
    if method == COAP_PUT:
        cmd = payload.decode().strip().lower()
        if cmd == "on":
            b = PWM(Pin(buzzer_pin))
            b.freq(1000)
            b.duty(512)
        elif cmd == "off":
            buzzer_off()
        elif cmd == "play":
            play_buzzer_tone()
        return COAP_CHANGED, json.dumps({"buzzer": cmd})
    elif method == COAP_GET:
        return COAP_CONTENT, '{"buzzer":"ready"}'
    return COAP_METHOD_NOT_ALLOWED, '{"error":"use GET or PUT"}'


# ═════════════════════════════════════
# RESOURCE TABLE
# ═════════════════════════════════════

RESOURCES = {
    "sensors": res_sensors,
    "temperature": res_temperature,
    "humidity": res_humidity,
    "motion": res_motion,
    "gas": res_gas,
    "rain": res_rain,
    "led": res_led,
    "fan": res_fan,
    "door": res_door,
    "window": res_window,
    "rgb": res_rgb,
    "buzzer": res_buzzer,
}


# ═════════════════════════════════════
# CONNECT TO WIFI
# ═════════════════════════════════════

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print(f"Connecting to WiFi: {WIFI_NAME}...")
        wlan.connect(WIFI_NAME, WIFI_PASSWORD)
        for i in range(20):
            if wlan.isconnected():
                break
            time.sleep(1)
            print(f"  Trying... ({i+1}/20)")
    if wlan.isconnected():
        ip = wlan.ifconfig()[0]
        print()
        print("=" * 45)
        print("  ✅ WiFi Connected!")
        print(f"  📡 Network: {WIFI_NAME}")
        print()
        print(f"  📦 CoAP server at:")
        print(f"  👉 coap://{ip}:5683")
        print("=" * 45)
        return ip
    else:
        print("❌ WiFi connection failed!")
        return None


# ═════════════════════════════════════
# CoAP SERVER MAIN LOOP
# ═════════════════════════════════════

def start_server():
    ip = connect_wifi()
    if not ip:
        return

    # Open UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('0.0.0.0', COAP_PORT))
    sock.setblocking(False)

    print()
    print(f"  CoAP server listening on UDP port {COAP_PORT}")
    print()
    print("  Available resources:")
    print("  GET  coap://IP/sensors      → all data")
    print("  GET  coap://IP/temperature")
    print("  GET  coap://IP/humidity")
    print("  GET  coap://IP/motion")
    print("  GET  coap://IP/gas")
    print("  GET  coap://IP/rain")
    print("  GET  coap://IP/led          (+ PUT: on/off)")
    print("  GET  coap://IP/fan          (+ PUT: on/off)")
    print("  GET  coap://IP/door         (+ PUT: open/close)")
    print("  GET  coap://IP/window       (+ PUT: open/close)")
    print("  GET  coap://IP/rgb          (+ PUT: 0-4)")
    print("  PUT  coap://IP/buzzer       (on/off/play)")
    print()

    while True:
        try:
            # Check for incoming CoAP packet
            try:
                data, addr = sock.recvfrom(256)
            except OSError:
                time.sleep_ms(10)
                continue

            pkt = coap_parse(data)
            if pkt is None:
                continue

            uri = coap_get_uri(pkt)
            method = pkt['code']

            print(f"{'GET' if method == COAP_GET else 'PUT'} /{uri} from {addr[0]}")

            # Find and call resource handler
            if uri in RESOURCES:
                try:
                    code, resp_payload = RESOURCES[uri](method, pkt['payload'])
                except Exception as e:
                    print("  Error:", e)
                    code = COAP_BAD_REQUEST
                    resp_payload = json.dumps({"error": str(e)})
            else:
                code = COAP_NOT_FOUND
                resp_payload = json.dumps({"error": "not found", "uri": uri})

            # Send response
            resp_type = COAP_ACK if pkt['type'] == COAP_CON else COAP_NON
            response = coap_build_response(resp_type, code, pkt['mid'], pkt['token'], resp_payload)
            sock.sendto(response, addr)

            gc.collect()

        except KeyboardInterrupt:
            print("\nStopping server...")
            sock.close()
            break
        except Exception as e:
            print("Error:", e)


# ═════════════════════════════════════
# RUN EVERYTHING!
# ═════════════════════════════════════

print()
print("🏠 Smart Home CoAP Server")
print("Starting up...")
print()

start_server()
