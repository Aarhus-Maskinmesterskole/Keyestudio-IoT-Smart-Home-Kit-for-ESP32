# 📦 CoAP Server — Letvægts IoT-protokol til dit Smart Home!

> **Styr dit smart home med CoAP — en protokol designet specifikt til IoT-enheder!**
> CoAP er som HTTP, men meget lettere og hurtigere — perfekt til sensorer og microcontrollers! 🏠⚡

---

## 🤔 Hvad er CoAP?

**CoAP** (Constrained Application Protocol) er en letvægts-protokol designet til **bittesmå enheder** som ESP32, Arduino, og sensorer. Tænk på det som en **mini-version af HTTP** der bruger **UDP** i stedet for TCP.

| | HTTP | CoAP |
|--|------|------|
| **Transport** | TCP (tung) | UDP (let) |
| **Header størrelse** | ~700 bytes | **4 bytes** |
| **Overhead** | Stor | Minimal |
| **Designet til** | Websider | IoT-enheder |
| **Port** | 80 | **5683** |
| **Metoder** | GET, POST, PUT... | GET, PUT, POST, DELETE |

### Hvornår vælge CoAP?

✅ **Enheder med begrænset hukommelse** — CoAP er meget mindre end HTTP  
✅ **Batteri-drevne sensorer** — UDP bruger mindre strøm  
✅ **Mange enheder på netværket** — CoAP er mere effektiv per-besked  
✅ **Machine-to-machine** — perfekt til kommunikation mellem enheder  
✅ **Lære IoT-protokoller** — forstå hvordan "rigtige" IoT-systemer virker  

### Hvornår IKKE vælge CoAP?

❌ Hvis du vil styre via en **browser** → brug HTTP Server  
❌ Hvis du har brug for **live-opdateringer** → brug WebSocket  
❌ Hvis du vil bruge en **sky-tjeneste** → brug MQTT  

---

## ⭐ Hvad kan scriptet?

| Ressource | GET | PUT | Beskrivelse |
|-----------|-----|-----|-------------|
| `/sensors` | ✅ | — | Hent alle sensor- og aktuatordata |
| `/temperature` | ✅ | — | Temperatur i °C |
| `/humidity` | ✅ | — | Luftfugtighed i % |
| `/motion` | ✅ | — | Bevægelsessensor (0/1) |
| `/gas` | ✅ | — | MQ2 gassensor (analog 0-4095, høj = mere gas) |
| `/rain` | ✅ | — | Regnsensor (analog 0-4095) |
| `/led` | ✅ | ✅ | LED status / kontrol (on/off) |
| `/fan` | ✅ | ✅ | Blæser status / kontrol (on/off) |
| `/door` | ✅ | ✅ | Dør status / kontrol (open/close) |
| `/window` | ✅ | ✅ | Vindue status / kontrol (open/close) |
| `/rgb` | ✅ | ✅ | RGB lampe farve (0-4) |
| `/buzzer` | ✅ | ✅ | Buzzer kontrol (on/off/play) |

---

## 📋 Sådan gør du (trin for trin)

### Trin 1: Åbn scriptet i Thonny

Du skal kun uploade **1 fil** — alt er indbygget (ligesom HTTP-serveren):

1. Åbn **Thonny** på din computer
2. Forbind din ESP32 med USB-kablet
3. Klik **File** → **Open** → find filen:
   ```
   Projects/Full MicroPython scripts/CoAP Server/coap_smart_home.py
   ```
4. Filen åbner sig i Thonny

### Trin 2: Skriv dit WiFi-navn og password

Find disse to linjer i toppen af `coap_smart_home.py`:

```python
WIFI_NAME = 'YOUR_WIFI_NAME'           # ← Put your WiFi name here
WIFI_PASSWORD = 'YOUR_WIFI_PASSWORD'   # ← Put your WiFi password here
```

**Skift dem til dit eget WiFi:**

```python
WIFI_NAME = 'MitWiFi'           # ← Dit WiFi-navn
WIFI_PASSWORD = 'MitPassword'   # ← Din WiFi-kode
```

> ⚠️ **VIGTIGT:** Hold de små `'` tegn rundt om teksten!

### Trin 3: Kør scriptet! 🚀

1. Klik den grønne **▶ Run** knap (eller tryk F5)
2. Vent et par sekunder...
3. I bunden af Thonny ser du:

```
=============================================
  ✅ WiFi Connected!
  📡 Network: MitWiFi

  📦 CoAP server at:
  👉 coap://192.168.1.100:5683
=============================================
```

---

## 🔧 Sådan henter du data med CoAP

### Installer en CoAP client

Du skal bruge en CoAP client for at snakke med serveren. Her er dine muligheder:

**Linux/Mac (anbefalet):**
```bash
# Installer libcoap (inkluderer coap-client)
# Ubuntu/Debian:
sudo apt install libcoap3-bin

# Mac:
brew install libcoap
```

**Python (alle platforme):**
```bash
pip install aiocoap
```

**Node-RED:**
- Installer `node-red-contrib-coap` via Palette Manager

---

### 📥 Hent sensordata (GET)

**Hent ALLE data på én gang:**
```bash
coap-client -m get coap://192.168.1.100/sensors
```

Svar:
```json
{"temperature":23,"humidity":45,"motion":0,"gas":512,"rain":1234,"led":0,"fan":"off","door":"closed","window":"closed","rgb":"off"}
```

**Hent én sensor ad gangen:**
```bash
# Temperatur
coap-client -m get coap://192.168.1.100/temperature
# → {"temperature": 23}

# Luftfugtighed
coap-client -m get coap://192.168.1.100/humidity
# → {"humidity": 45}

# Bevægelse
coap-client -m get coap://192.168.1.100/motion
# → {"motion": 0}

# Gas
coap-client -m get coap://192.168.1.100/gas
# → {"gas": 512}

# Regn
coap-client -m get coap://192.168.1.100/rain
# → {"rain": 1234}
```

**Hent aktuator-status:**
```bash
# LED status
coap-client -m get coap://192.168.1.100/led
# → {"led": 0}

# Blæser status
coap-client -m get coap://192.168.1.100/fan
# → {"fan": "off"}

# Dør status
coap-client -m get coap://192.168.1.100/door
# → {"door": "closed"}

# Vindue status
coap-client -m get coap://192.168.1.100/window
# → {"window": "closed"}

# RGB farve
coap-client -m get coap://192.168.1.100/rgb
# → {"rgb": "off"}
```

---

### 📤 Send kommandoer (PUT)

**Styr LED:**
```bash
# Tænd LED
coap-client -m put coap://192.168.1.100/led -e "on"

# Sluk LED
coap-client -m put coap://192.168.1.100/led -e "off"
```

**Styr blæser:**
```bash
coap-client -m put coap://192.168.1.100/fan -e "on"
coap-client -m put coap://192.168.1.100/fan -e "off"
```

**Styr dør og vindue:**
```bash
coap-client -m put coap://192.168.1.100/door -e "open"
coap-client -m put coap://192.168.1.100/door -e "close"

coap-client -m put coap://192.168.1.100/window -e "open"
coap-client -m put coap://192.168.1.100/window -e "close"
```

**Skift RGB-farve:**
```bash
coap-client -m put coap://192.168.1.100/rgb -e "0"   # Sluk
coap-client -m put coap://192.168.1.100/rgb -e "1"   # Rød
coap-client -m put coap://192.168.1.100/rgb -e "2"   # Grøn
coap-client -m put coap://192.168.1.100/rgb -e "3"   # Blå
coap-client -m put coap://192.168.1.100/rgb -e "4"   # Hvid
```

**Styr buzzer:**
```bash
coap-client -m put coap://192.168.1.100/buzzer -e "on"
coap-client -m put coap://192.168.1.100/buzzer -e "off"
coap-client -m put coap://192.168.1.100/buzzer -e "play"  # Spil melodi
```

---

### 🐍 Python eksempler (med aiocoap)

```python
import asyncio
from aiocoap import Context, Message, GET, PUT

async def main():
    ctx = await Context.create_client_context()
    
    # Hent alle sensordata
    request = Message(code=GET, uri="coap://192.168.1.100/sensors")
    response = await ctx.request(request).response
    print("Sensorer:", response.payload.decode())
    
    # Hent kun temperatur
    request = Message(code=GET, uri="coap://192.168.1.100/temperature")
    response = await ctx.request(request).response
    print("Temp:", response.payload.decode())
    
    # Tænd LED
    request = Message(code=PUT, uri="coap://192.168.1.100/led", payload=b"on")
    response = await ctx.request(request).response
    print("LED:", response.payload.decode())

asyncio.run(main())
```

---

### 🔴 Node-RED eksempel

1. Tilføj en **coap request** node
2. Sæt method til `GET`
3. Sæt URL til `coap://192.168.1.100/sensors`
4. Forbind til en **json** node → **debug** node
5. Deploy og se sensordata i debug-panelet!

For at styre enheder:
1. Tilføj en **coap request** node
2. Sæt method til `PUT`
3. Sæt URL til `coap://192.168.1.100/led`
4. Send payload `on` eller `off` fra en **inject** node

---

## 🧠 Hvordan virker CoAP? (for de nysgerrige)

```
Din computer                         ESP32 (port 5683)
    │                                   │
    │── [CON] GET /temperature ────────►│ ← CoAP request (UDP)
    │                                   │ ← ESP32 læser sensor
    │◄── [ACK] 2.05 {"temp":23} ───────│ ← CoAP response (4 byte header!)
    │                                   │
    │── [CON] PUT /led  "on" ──────────►│ ← Styr aktuator
    │                                   │ ← ESP32 tænder LED
    │◄── [ACK] 2.04 {"led":1} ─────────│ ← Bekræftelse
```

**CoAP response koder (ligesom HTTP status koder):**
- `2.01` Created — ny ressource oprettet
- `2.04` Changed — ressource opdateret (PUT success)
- `2.05` Content — data returneret (GET success)
- `4.00` Bad Request — fejl i request
- `4.04` Not Found — ressource findes ikke
- `4.05` Method Not Allowed — forkert metode

---

## 📁 Filer i denne mappe

| Fil | Beskrivelse | Upload til ESP32? |
|-----|-------------|-------------------|
| `coap_smart_home.py` | Smart home CoAP server (alt-i-én, inkl. CoAP library) | ✅ Ja — kopier og kør! |
| `microcoap.py` | CoAP library som separat fil (valgfrit, til genbrug i andre projekter) | Valgfrit |
| `README.md` | Denne manual | Nej |

---

## 🆘 Hjælp! Det virker ikke!

### "ImportError" eller "ModuleNotFoundError"
- Sørg for du kører den nye `coap_smart_home.py` — den har alt indbygget
- Hvis du bruger den gamle version med separate filer, upload `microcoap.py` til ESP32'ens rod

### "WiFi connection failed"
- Tjek WiFi-navn og password
- Sørg for ESP32 er tæt på routeren

### coap-client virker ikke
- Tjek at din computer er på **samme WiFi** som ESP32'en
- Tjek at IP-adressen er korrekt (se Thonny Shell)
- Prøv: `coap-client -m get coap://IP/sensors`

### Ingen svar på requests
- Tjek at serveren kører (du skal se "CoAP server listening" i Thonny)
- Prøv at genstarte ESP32 og kør scriptet igen

---

[← Tilbage til hovedsiden](../../../README.md)