"""
Build by AI in Antigravity 2026-03-08

🏠 Smart Home HTTP Server
===========================
This script turns your ESP32 into a web server.
Open a web page on your phone or computer to control your entire smart home!

You can:
  ✅ Turn the LED on/off
  ✅ Control the fan
  ✅ Open/close the door
  ✅ Open/close the window
  ✅ Change the atmosphere lamp color
  ✅ Play a buzzer sound
  ✅ See temperature and humidity
  ✅ See if someone is moving (PIR)
  ✅ See if there is dangerous gas

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
import time
import json
import gc
import dht
import neopixel
from machine import Pin, PWM, ADC, SoftI2C

# ─────────────────────────────────────
# SET UP ALL THE SMART HOME COMPONENTS
# ─────────────────────────────────────

# LED (GPIO 12)
led = Pin(12, Pin.OUT)
led.value(0)

# Buttons (GPIO 16 and 27)
button1 = Pin(16, Pin.IN, Pin.PULL_UP)
button2 = Pin(27, Pin.IN, Pin.PULL_UP)

# PIR Motion Sensor (GPIO 14)
pir = Pin(14, Pin.IN)

# Passive Buzzer (GPIO 25) — start as plain pin = fully silent
buzzer_pin = 25
Pin(buzzer_pin, Pin.OUT).value(0)  # LOW = no sound at all

# Door Servo (GPIO 13)
door_servo = PWM(Pin(13), freq=50)
door_servo.duty(25)  # Start closed (0°)
door_open = False

# Window Servo (GPIO 5)
window_servo = PWM(Pin(5), freq=50)
window_servo.duty(25)  # Start closed
window_open = False

# Fan Motor (GPIO 19 = forward, GPIO 18 = backward) - digital pins
fan_forward = Pin(19, Pin.OUT)
fan_backward = Pin(18, Pin.OUT)
fan_forward.value(0)
fan_backward.value(0)
fan_on = False

# SK6812 RGB Atmosphere Lamp (GPIO 26, 4 LEDs)
np_pin = Pin(26, Pin.OUT)
np = neopixel.NeoPixel(np_pin, 4)
current_color = 0  # 0=off, 1=red, 2=green, 3=blue, 4=white

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

# ─────────────────────────────────────
# HELPER FUNCTIONS
# ─────────────────────────────────────

def set_rgb(color_index):
    """Set all 4 RGB LEDs to a color. 0=off, 1=red, 2=green, 3=blue, 4=white"""
    global current_color
    current_color = color_index
    brightness = 80
    colors = [
        (0, 0, 0),                                # 0 = Off
        (brightness, 0, 0),                       # 1 = Red
        (0, brightness, 0),                       # 2 = Green
        (0, 0, brightness),                       # 3 = Blue
        (brightness, brightness, brightness),     # 4 = White
    ]
    c = colors[color_index]
    for i in range(4):
        np[i] = c
    np.write()


def read_sensors():
    """Read all sensor values and return them."""
    # Temperature & Humidity
    try:
        dht_sensor.measure()
        temp = dht_sensor.temperature()
        hum = dht_sensor.humidity()
    except:
        temp = "--"
        hum = "--"

    # PIR Motion
    motion = "Yes! 🏃" if pir.value() == 1 else "No 😌"

    # Gas
    gas_val = gas_adc.read()
    gas_status = "⚠️ Danger!" if gas_val > 2000 else "Safe ✅"

    # Rain
    rain_val = rain_adc.read()
    rain_voltage = rain_val / 4095.0 * 3.3
    rain_status = "🌧️ Wet!" if rain_voltage > 0.6 else "Dry ☀️"

    return temp, hum, motion, gas_status, rain_status





def buzzer_off():
    """Ensure buzzer is fully silent (no PWM hum)."""
    try:
        PWM(Pin(buzzer_pin)).deinit()
    except:
        pass
    Pin(buzzer_pin, Pin.OUT).value(0)


def play_buzzer_tone():
    """Play a short happy tone on the buzzer."""
    b = PWM(Pin(buzzer_pin))
    notes = [523, 659, 784, 1047]
    for note in notes:
        b.freq(note)
        b.duty(512)
        time.sleep_ms(150)
    b.deinit()
    Pin(buzzer_pin, Pin.OUT).value(0)


# Start with everything off
set_rgb(0)

# ─────────────────────────────────────
# THE WEB PAGE (HTML)
# ─────────────────────────────────────

CSS = """*{margin:0;padding:0;box-sizing:border-box}
body{font-family:'Segoe UI',Arial,sans-serif;background:linear-gradient(135deg,#0f0c29,#302b63,#24243e);color:#fff;min-height:100vh;padding:20px}
h1{text-align:center;font-size:2em;margin:10px 0 10px;background:linear-gradient(90deg,#f093fb,#f5576c,#4facfe);-webkit-background-clip:text;-webkit-text-fill-color:transparent}
.sub{text-align:center;color:#aaa;margin-bottom:20px;font-size:.9em}
.hamburger{position:fixed;top:14px;left:14px;z-index:1001;cursor:pointer;background:rgba(255,255,255,.12);border:none;color:#fff;font-size:1.5em;padding:8px 12px;border-radius:10px;backdrop-filter:blur(6px)}
#overlay{display:none;position:fixed;inset:0;background:rgba(0,0,0,.5);z-index:999}
#overlay.show{display:block}
#sidemenu{position:fixed;top:0;left:-310px;width:290px;height:100%;background:#1a1a2e;z-index:1000;transition:left .3s ease;overflow-y:auto;padding:20px;border-right:1px solid rgba(255,255,255,.1)}
#sidemenu.show{left:0}
.mhead{font-size:1.15em;font-weight:bold;margin:8px 0 16px;color:#4facfe}
.mclose{float:right;background:none;border:none;color:#888;font-size:1.3em;cursor:pointer}
.api-item{background:rgba(255,255,255,.05);border-radius:10px;padding:10px;margin-bottom:8px}
.api-m{display:inline-block;padding:2px 7px;border-radius:4px;font-size:.7em;font-weight:bold;margin-right:5px}
.api-m.put{background:#f5576c33;color:#f5576c}.api-m.get{background:#43e97b33;color:#43e97b}
.api-p{font-weight:bold;font-size:.9em}
.api-d{color:#aaa;font-size:.75em;margin:3px 0}
.api-item code{display:block;background:#000;padding:4px 7px;border-radius:5px;font-size:.68em;margin-top:3px;color:#4facfe;word-break:break-all}
.mlink{display:block;text-align:center;color:#4facfe;text-decoration:none;margin-top:14px;font-size:.85em;padding:8px;background:rgba(79,172,254,.1);border-radius:8px}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:15px;max-width:900px;margin:0 auto}
.card{background:rgba(255,255,255,.08);backdrop-filter:blur(10px);border-radius:16px;padding:20px;border:1px solid rgba(255,255,255,.1)}
.card h2{font-size:1.1em;margin-bottom:12px;color:#f0f0f0}
.sr{display:flex;justify-content:space-between;padding:6px 0;border-bottom:1px solid rgba(255,255,255,.05);font-size:.95em}
.sl{color:#aaa}.sv{font-weight:bold;color:#4facfe}
.btn{display:inline-block;padding:12px 24px;margin:5px;border:none;border-radius:12px;font-size:1em;font-weight:bold;cursor:pointer;text-decoration:none;color:#fff;transition:transform .1s;text-align:center}
.btn:active{transform:scale(.95)}
.btn-on{background:linear-gradient(135deg,#43e97b,#38f9d7);color:#000}
.btn-off{background:linear-gradient(135deg,#fa709a,#fee140);color:#000}
.btn-blue{background:linear-gradient(135deg,#4facfe,#00f2fe);color:#000}
.btn-purple{background:linear-gradient(135deg,#a18cd1,#fbc2eb);color:#000}
.btn-sm{padding:8px 14px;font-size:.85em;margin:3px;border-radius:8px}
.st{display:inline-block;padding:4px 12px;border-radius:20px;font-size:.85em;font-weight:bold}
.st-on{background:#43e97b33;color:#43e97b}.st-off{background:#fa709a33;color:#fa709a}
.brow{margin-top:10px}
.foot{text-align:center;margin-top:20px}
.foot a{color:#4facfe;text-decoration:none;font-size:.9em}
.apic{max-width:700px;margin:0 auto}
.apic .card{margin-bottom:12px}
.tag{display:inline-block;padding:2px 10px;border-radius:5px;font-size:.75em;font-weight:bold;margin-right:6px}
.tag.put{background:#f5576c33;color:#f5576c}.tag.get{background:#43e97b33;color:#43e97b}
.pr{font-size:.85em;color:#bbb;margin:6px 0}
.pr code{background:#000;padding:2px 6px;border-radius:4px;color:#4facfe;font-size:.85em}
.ex{background:#000;padding:8px 10px;border-radius:8px;font-size:.78em;color:#4facfe;margin:8px 0;font-family:monospace;word-break:break-all}
"""

SIDEMENU = """<div id="overlay" onclick="toggleMenu()"></div>
<div id="sidemenu">
<button class="mclose" onclick="toggleMenu()">&times;</button>
<div class="mhead">API Endpoints</div>
<div class="api-item"><span class="api-m get">GET</span><span class="api-p">/sensors</span><div class="api-d">Read all data (JSON)</div><code>curl http://IP/sensors</code></div>
<hr style="border-color:rgba(255,255,255,.1);margin:10px 0">
<div class="mhead" style="font-size:1em;margin:4px 0 8px">PUT (send commands)</div>
<div class="api-item"><span class="api-m put">PUT</span><span class="api-p">/led</span><div class="api-d">Body: on/off</div></div>
<div class="api-item"><span class="api-m put">PUT</span><span class="api-p">/fan</span><div class="api-d">Body: on/off</div></div>
<div class="api-item"><span class="api-m put">PUT</span><span class="api-p">/door</span><div class="api-d">Body: open/close</div></div>
<div class="api-item"><span class="api-m put">PUT</span><span class="api-p">/window</span><div class="api-d">Body: open/close</div></div>
<div class="api-item"><span class="api-m put">PUT</span><span class="api-p">/rgb</span><div class="api-d">Body: 0-4</div></div>
<div class="api-item"><span class="api-m put">PUT</span><span class="api-p">/buzzer</span><div class="api-d">Body: on/off</div></div>
<a class="mlink" href="/api">Full API docs</a>
</div>"""

JS = """<script>
function toggleMenu(){document.getElementById('sidemenu').classList.toggle('show');document.getElementById('overlay').classList.toggle('show')}
</script>"""


def build_web_page(page="home"):
    """Build the HTML web page. page='home' or 'api'."""
    global current_color

    if page == "api":
        body = """<h1>API Documentation</h1>
<p class="sub">Use from curl, Node-RED, Python, or any HTTP client</p>
<div class="apic">
  <div class="card" style="border-color:rgba(79,172,254,.3)"><h2><span class="tag get">GET</span> /sensors</h2><p>Read all sensor data + device states as JSON</p>
    <div class="ex">curl http://IP/sensors</div>
    <div class="pr"><b>Returns:</b> temperature, humidity, motion, gas, rain, led, fan, door, window, rgb</div></div>
  <div class="card"><h2>PUT Endpoints</h2><p style="color:#aaa;font-size:.85em">Send data in request body</p>
    <div class="pr"><span class="tag put">PUT</span> <code>/led</code> body: on/off</div>
    <div class="pr"><span class="tag put">PUT</span> <code>/fan</code> body: on/off</div>
    <div class="pr"><span class="tag put">PUT</span> <code>/door</code> body: open/close</div>
    <div class="pr"><span class="tag put">PUT</span> <code>/window</code> body: open/close</div>
    <div class="pr"><span class="tag put">PUT</span> <code>/rgb</code> body: 0-4</div>
    <div class="pr"><span class="tag put">PUT</span> <code>/buzzer</code> body: on/off</div>
    <div class="ex">curl -X PUT http://IP/led -d "on"</div></div>
</div>
<div class="foot" style="margin-top:20px"><a href="/">Back to control panel</a></div>"""
    else:
        temp, hum, motion, gas_status, rain_status = read_sensors()
        color_names = ["Off", "Red", "Green", "Blue", "White"]
        body = """<h1>Smart Home Control</h1>
<p class="sub">Control your home from any device on the network</p>
<div class="grid">
  <div class="card"><h2>Sensors</h2>
    <div class="sr"><span class="sl">Temperature</span><span class="sv">""" + str(temp) + """ C</span></div>
    <div class="sr"><span class="sl">Humidity</span><span class="sv">""" + str(hum) + """ %</span></div>
    <div class="sr"><span class="sl">Motion</span><span class="sv">""" + str(motion) + """</span></div>
    <div class="sr"><span class="sl">Gas</span><span class="sv">""" + str(gas_status) + """</span></div>
    <div class="sr"><span class="sl">Rain</span><span class="sv">""" + str(rain_status) + """</span></div>
  </div>
  <div class="card"><h2>LED</h2>
    <p>Status: <span class="st """ + ("st-on" if led.value() else "st-off") + """">""" + ("ON" if led.value() else "OFF") + """</span></p>
    <div class="brow"><a class="btn btn-on" href="/led/on">Turn ON</a><a class="btn btn-off" href="/led/off">Turn OFF</a></div>
  </div>
  <div class="card"><h2>Fan</h2>
    <p>Status: <span class="st """ + ("st-on" if fan_on else "st-off") + """">""" + ("ON" if fan_on else "OFF") + """</span></p>
    <div class="brow"><a class="btn btn-on" href="/fan/on">Turn ON</a><a class="btn btn-off" href="/fan/off">Turn OFF</a></div>
  </div>
  <div class="card"><h2>Door</h2>
    <p>Status: <span class="st """ + ("st-on" if door_open else "st-off") + """">""" + ("OPEN" if door_open else "CLOSED") + """</span></p>
    <div class="brow"><a class="btn btn-on" href="/door/open">Open</a><a class="btn btn-off" href="/door/close">Close</a></div>
  </div>
  <div class="card"><h2>Window</h2>
    <p>Status: <span class="st """ + ("st-on" if window_open else "st-off") + """">""" + ("OPEN" if window_open else "CLOSED") + """</span></p>
    <div class="brow"><a class="btn btn-on" href="/window/open">Open</a><a class="btn btn-off" href="/window/close">Close</a></div>
  </div>
  <div class="card"><h2>Atmosphere Lamp</h2>
    <p>Color: <span class="sv">""" + color_names[current_color] + """</span></p>
    <div class="brow">
      <a class="btn btn-sm btn-off" href="/rgb/0">Off</a>
      <a class="btn btn-sm" href="/rgb/1" style="background:#e74c3c">Red</a>
      <a class="btn btn-sm" href="/rgb/2" style="background:#2ecc71">Green</a>
      <a class="btn btn-sm" href="/rgb/3" style="background:#3498db">Blue</a>
      <a class="btn btn-sm" href="/rgb/4" style="background:#ecf0f1;color:#333">White</a>
    </div>
  </div>
  <div class="card"><h2>Buzzer</h2>
    <div class="brow"><a class="btn btn-purple" href="/buzzer/play">Play Sound</a></div>
  </div>
</div>
<div class="foot"><a href="/">Refresh</a> &middot; <a href="/api">API Docs</a></div>"""

    return """<!DOCTYPE html><html><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Smart Home</title><style>""" + CSS + """</style></head><body>
<button class="hamburger" onclick="toggleMenu()">&#9776;</button>
""" + SIDEMENU + body + JS + """</body></html>"""


# ─────────────────────────────────────
# CONNECT TO WIFI
# ─────────────────────────────────────

def connect_wifi():
    """Connect to WiFi and return the IP address."""
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    if not wlan.isconnected():
        print("Connecting to WiFi:", WIFI_NAME)
        wlan.connect(WIFI_NAME, WIFI_PASSWORD)

        # Wait up to 15 seconds
        for i in range(30):
            if wlan.isconnected():
                break
            print(".", end="")
            time.sleep(0.5)
        print()

    if wlan.isconnected():
        ip = wlan.ifconfig()[0]
        print()
        print("=" * 45)
        print("  ✅ WiFi Connected!")
        print("  📡 Network:", WIFI_NAME)
        print()
        print("  🌐 Open this in your browser:")
        print("  👉 http://" + ip)
        print("=" * 45)
        print()
        return ip
    else:
        print("❌ WiFi connection failed!")
        print("Check your WIFI_NAME and WIFI_PASSWORD")
        return None


# ─────────────────────────────────────
# START THE WEB SERVER
# ─────────────────────────────────────

def start_server(ip):
    """Start the HTTP web server."""
    global led, fan_on, door_open, window_open, current_color

    # Create server socket
    addr = socket.getaddrinfo(ip, 80)[0][-1]
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(addr)
    s.listen(3)

    print("🏠 Smart Home Server is running!")
    print("Waiting for connections...")
    print()
    print("Endpoints:")
    print("  GET  /          Web UI (control panel)")
    print("  GET  /api       API documentation page")
    print("  GET  /sensors   Read all sensors (JSON)")
    print("  PUT  /led       Body: on / off")
    print("  PUT  /fan       Body: on / off")
    print("  PUT  /door      Body: open / close")
    print("  PUT  /window    Body: open / close")
    print("  PUT  /rgb       Body: 0-4")
    print("  PUT  /buzzer    Body: on / off")
    print("  GET  /led/on    (browser-friendly shortcuts)")
    print()

    while True:
        try:
            conn, client_addr = s.accept()

            request = conn.recv(1024).decode('utf-8')

            # Parse method, path, and body from HTTP request
            method = "GET"
            path = "/"
            body = ""
            try:
                first_line = request.split("\r\n")[0]
                parts = first_line.split(" ")
                method = parts[0]
                path = parts[1]
                # Extract body (after the blank line)
                body_parts = request.split("\r\n\r\n")
                if len(body_parts) > 1:
                    body = body_parts[1].strip()
            except:
                pass

            print(method, path, body if body else "")

            # ── PUT endpoints (for curl, Node-RED, Python, etc.) ──
            if method == "PUT" and path == "/led":
                if body.lower() == "on":
                    led.value(1)
                elif body.lower() == "off":
                    led.value(0)
                resp = json.dumps({"led": led.value()})
                conn.send("HTTP/1.1 200 OK\r\nContent-Type: application/json\r\nAccess-Control-Allow-Origin: *\r\nConnection: close\r\n\r\n")
                conn.send(resp)
                conn.close()
                continue

            elif method == "PUT" and path == "/fan":
                if body.lower() == "on":
                    fan_on = True
                    fan_forward.value(0)
                    fan_backward.value(1)
                elif body.lower() == "off":
                    fan_on = False
                    fan_forward.value(0)
                    fan_backward.value(0)
                resp = json.dumps({"fan": "on" if fan_on else "off"})
                conn.send("HTTP/1.1 200 OK\r\nContent-Type: application/json\r\nAccess-Control-Allow-Origin: *\r\nConnection: close\r\n\r\n")
                conn.send(resp)
                conn.close()
                continue

            elif method == "PUT" and path == "/door":
                if body.lower() == "open":
                    door_open = True
                    door_servo.duty(128)
                elif body.lower() == "close":
                    door_open = False
                    door_servo.duty(25)
                resp = json.dumps({"door": "open" if door_open else "closed"})
                conn.send("HTTP/1.1 200 OK\r\nContent-Type: application/json\r\nAccess-Control-Allow-Origin: *\r\nConnection: close\r\n\r\n")
                conn.send(resp)
                conn.close()
                continue

            elif method == "PUT" and path == "/window":
                if body.lower() == "open":
                    window_open = True
                    window_servo.duty(128)
                elif body.lower() == "close":
                    window_open = False
                    window_servo.duty(25)
                resp = json.dumps({"window": "open" if window_open else "closed"})
                conn.send("HTTP/1.1 200 OK\r\nContent-Type: application/json\r\nAccess-Control-Allow-Origin: *\r\nConnection: close\r\n\r\n")
                conn.send(resp)
                conn.close()
                continue

            elif method == "PUT" and path == "/rgb":
                try:
                    c = int(body.strip())
                    if 0 <= c <= 4:
                        set_rgb(c)
                except:
                    pass
                color_names = ["off", "red", "green", "blue", "white"]
                resp = json.dumps({"rgb": color_names[current_color]})
                conn.send("HTTP/1.1 200 OK\r\nContent-Type: application/json\r\nAccess-Control-Allow-Origin: *\r\nConnection: close\r\n\r\n")
                conn.send(resp)
                conn.close()
                continue

            elif method == "PUT" and path == "/buzzer":
                if body.lower() == "on":
                    b = PWM(Pin(buzzer_pin))
                    b.freq(1000)
                    b.duty(512)
                elif body.lower() == "off":
                    buzzer_off()
                resp = json.dumps({"buzzer": body.lower()})
                conn.send("HTTP/1.1 200 OK\r\nContent-Type: application/json\r\nAccess-Control-Allow-Origin: *\r\nConnection: close\r\n\r\n")
                conn.send(resp)
                conn.close()
                continue

            # ── Handle CORS preflight (for browser fetch/Node-RED) ──
            elif method == "OPTIONS":
                conn.send("HTTP/1.1 204 No Content\r\nAccess-Control-Allow-Origin: *\r\nAccess-Control-Allow-Methods: GET,PUT,OPTIONS\r\nAccess-Control-Allow-Headers: Content-Type\r\nConnection: close\r\n\r\n")
                conn.close()
                continue

            # ── GET /sensors → JSON (all data in one) ──
            elif method == "GET" and path == "/sensors":
                temp, hum, motion, gas_status, rain_status = read_sensors()
                data = json.dumps({
                    "temperature": temp,
                    "humidity": hum,
                    "motion": 1 if pir.value() else 0,
                    "gas": gas_adc.read(),
                    "rain": rain_adc.read(),
                    "led": led.value(),
                    "fan": "on" if fan_on else "off",
                    "door": "open" if door_open else "closed",
                    "window": "open" if window_open else "closed",
                    "rgb": current_color
                })
                conn.send("HTTP/1.1 200 OK\r\nContent-Type: application/json\r\nAccess-Control-Allow-Origin: *\r\nConnection: close\r\n\r\n")
                conn.send(data)
                conn.close()
                gc.collect()
                continue

            # ── GET individual sensors → JSON (cheap, no HTML) ──
            elif method == "GET" and path == "/temperature":
                try:
                    dht_sensor.measure()
                    v = dht_sensor.temperature()
                except:
                    v = None
                resp = json.dumps({"temperature": v})
                conn.send("HTTP/1.1 200 OK\r\nContent-Type: application/json\r\nAccess-Control-Allow-Origin: *\r\nConnection: close\r\n\r\n")
                conn.send(resp)
                conn.close()
                continue

            elif method == "GET" and path == "/humidity":
                try:
                    dht_sensor.measure()
                    v = dht_sensor.humidity()
                except:
                    v = None
                resp = json.dumps({"humidity": v})
                conn.send("HTTP/1.1 200 OK\r\nContent-Type: application/json\r\nAccess-Control-Allow-Origin: *\r\nConnection: close\r\n\r\n")
                conn.send(resp)
                conn.close()
                continue

            elif method == "GET" and path == "/motion":
                conn.send("HTTP/1.1 200 OK\r\nContent-Type: application/json\r\nAccess-Control-Allow-Origin: *\r\nConnection: close\r\n\r\n")
                conn.send(json.dumps({"motion": pir.value()}))
                conn.close()
                continue

            elif method == "GET" and path == "/gas":
                conn.send("HTTP/1.1 200 OK\r\nContent-Type: application/json\r\nAccess-Control-Allow-Origin: *\r\nConnection: close\r\n\r\n")
                conn.send(json.dumps({"gas": gas_adc.read()}))
                conn.close()
                continue

            elif method == "GET" and path == "/rain":
                conn.send("HTTP/1.1 200 OK\r\nContent-Type: application/json\r\nAccess-Control-Allow-Origin: *\r\nConnection: close\r\n\r\n")
                conn.send(json.dumps({"rain": rain_adc.read()}))
                conn.close()
                continue

            # ── GET individual actuator states → JSON ──
            elif method == "GET" and path == "/led":
                conn.send("HTTP/1.1 200 OK\r\nContent-Type: application/json\r\nAccess-Control-Allow-Origin: *\r\nConnection: close\r\n\r\n")
                conn.send(json.dumps({"led": led.value()}))
                conn.close()
                continue

            elif method == "GET" and path == "/fan":
                conn.send("HTTP/1.1 200 OK\r\nContent-Type: application/json\r\nAccess-Control-Allow-Origin: *\r\nConnection: close\r\n\r\n")
                conn.send(json.dumps({"fan": "on" if fan_on else "off"}))
                conn.close()
                continue

            elif method == "GET" and path == "/door":
                conn.send("HTTP/1.1 200 OK\r\nContent-Type: application/json\r\nAccess-Control-Allow-Origin: *\r\nConnection: close\r\n\r\n")
                conn.send(json.dumps({"door": "open" if door_open else "closed"}))
                conn.close()
                continue

            elif method == "GET" and path == "/window":
                conn.send("HTTP/1.1 200 OK\r\nContent-Type: application/json\r\nAccess-Control-Allow-Origin: *\r\nConnection: close\r\n\r\n")
                conn.send(json.dumps({"window": "open" if window_open else "closed"}))
                conn.close()
                continue

            elif method == "GET" and path == "/rgb":
                cn = ["off", "red", "green", "blue", "white"]
                conn.send("HTTP/1.1 200 OK\r\nContent-Type: application/json\r\nAccess-Control-Allow-Origin: *\r\nConnection: close\r\n\r\n")
                conn.send(json.dumps({"rgb": cn[current_color]}))
                conn.close()
                continue

            # ── GET browser-friendly endpoints ──
            # These send a redirect to save memory (no HTML rebuild needed)
            cmd_done = False
            if path == "/led/on":
                led.value(1)
                cmd_done = True
            elif path == "/led/off":
                led.value(0)
                cmd_done = True
            elif path == "/fan/on":
                fan_on = True
                fan_forward.value(0)
                fan_backward.value(1)
                cmd_done = True
            elif path == "/fan/off":
                fan_on = False
                fan_forward.value(0)
                fan_backward.value(0)
                cmd_done = True
            elif path == "/door/open":
                door_open = True
                door_servo.duty(128)
                cmd_done = True
            elif path == "/door/close":
                door_open = False
                door_servo.duty(25)
                cmd_done = True
            elif path == "/window/open":
                window_open = True
                window_servo.duty(128)
                cmd_done = True
            elif path == "/window/close":
                window_open = False
                window_servo.duty(25)
                cmd_done = True
            elif path.startswith("/rgb/"):
                try:
                    color = int(path.split("/rgb/")[1])
                    if 0 <= color <= 4:
                        set_rgb(color)
                except:
                    pass
                cmd_done = True
            elif path == "/buzzer/play":
                play_buzzer_tone()
                cmd_done = True

            # Commands: send a lightweight redirect back to /
            if cmd_done:
                conn.send("HTTP/1.1 302 Found\r\nLocation: /\r\nConnection: close\r\n\r\n")
                conn.close()
                gc.collect()
                continue

            # ── Send web page back (only for / and /api) ──
            gc.collect()
            if path == "/api":
                response = build_web_page("api")
            else:
                response = build_web_page("home")
            conn.send("HTTP/1.1 200 OK\r\n")
            conn.send("Content-Type: text/html; charset=utf-8\r\n")
            conn.send("Access-Control-Allow-Origin: *\r\n")
            conn.send("Connection: close\r\n\r\n")
            conn.sendall(response)
            conn.close()
            gc.collect()

        except Exception as e:
            print("Error:", e)
            try:
                conn.close()
            except:
                pass


# ─────────────────────────────────────
# RUN EVERYTHING!
# ─────────────────────────────────────

print()
print("🏠 Smart Home HTTP Server")
print("=" * 30)

ip = connect_wifi()

if ip:
    start_server(ip)
else:
    print()
    print("Fix your WiFi settings and try again!")
