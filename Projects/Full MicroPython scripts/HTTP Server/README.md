# 🌐 HTTP Server — Styr dit Smart Home fra en hjemmeside!

> **Styr hele dit smart home fra din telefon eller computer!**
> Du åbner bare en hjemmeside, og så kan du trykke på knapper for at tænde lys, starte blæseren, åbne døren og meget mere! 🏠✨

---

## 🤔 Hvad er en HTTP Server?

Forestil dig, at din ESP32 bliver til en **lille hjemmeside** — ligesom Google eller YouTube, men den kører bare på dit eget WiFi! 

Når du skriver en adresse i din browser (fx `http://192.168.1.100`), sender den en besked til ESP32'en, og ESP32'en svarer med en flot side med knapper. Når du trykker på en knap, sender den en ny besked, og ESP32'en tænder lyset, starter blæseren, osv.

**Det er det nemmeste at forstå**, fordi det virker præcis ligesom en normal hjemmeside! 🌐

---

## 🆚 Hvorfor HTTP og ikke de andre protokoller?

| Protokol | Hvad er det? | Hvornår bruger man den? | Sværhed |
|----------|-------------|------------------------|---------|
| **🌐 HTTP Server** | En hjemmeside på din ESP32 | Når du vil styre alt fra en **browser** (telefon/PC) | ⭐ Let |
| 📨 MQTT | En besked-service (som SMS til maskiner) | Mange enheder der skal snakke sammen i **sky-tjenester** | ⭐⭐ Mellem |
| 📦 CoAP | Mini-HTTP til bittesmå enheder | Enheder med **meget lidt batteri** og hukommelse | ⭐⭐⭐ Svær |
| 🏭 Modbus TCP | Fabriksprotokol | **Industrielle maskiner** og PLC'er | ⭐⭐⭐ Svær |
| 🔌 WebSocket | To-vejs live-forbindelse | **Spil og live dashboards** der opdaterer sig selv | ⭐⭐ Mellem |

### Hvorfor vælge HTTP? 🏆

✅ **Nemmest at bruge** — du skal bare åbne en browser, ingen app eller ekstra software!  
✅ **Virker på alle enheder** — telefon, tablet, computer, alt med en browser  
✅ **Perfekt til smart home** — du kan se status og styre alt fra én side  
✅ **Ingen server i skyen** — alt kører lokalt på dit WiFi, ingen internet nødvendigt  
✅ **Nemt at forstå** — det er bare en hjemmeside!  

### Hvornår skal man IKKE vælge HTTP?

❌ Hvis du har 100+ enheder → brug MQTT  
❌ Hvis enheden kører på et lille batteri → brug CoAP  
❌ Hvis du skal styre en fabrik → brug Modbus  
❌ Hvis du vil have live-opdateringer uden at trykke refresh → brug WebSocket

---

## ⭐ Hvad kan scriptet?

| Funktion | Hvad sker der? |
|----------|----------------|
| 💡 LED | Tænd og sluk den gule LED |
| 🌀 Blæser | Start og stop blæseren |
| 🚪 Dør | Åbn og luk døren (servo motor) |
| 🪟 Vindue | Åbn og luk vinduet (servo motor) |
| 🌈 Farvelys | Skift farve: Rød, Grøn, Blå, Hvid, Slukket |
| 🔔 Buzzer | Spil en lyd! |
| 🌡️ Temperatur | Se temperaturen i °C |
| 💧 Luftfugtighed | Se luftfugtigheden i % |
| 👋 Bevægelse | Ser om nogen bevæger sig (PIR sensor) |
| ⛽ Gas | Alarm hvis der er farlig gas |
| 🌧️ Regn | Ser om regnsensoren er våd |

---

## 📋 Sådan gør du (trin for trin)

### Trin 1: Upload library-filer

Du skal først uploade 2 filer til din ESP32. Disse filer er IKKE nødvendige for HTTP Serveren alene, men sørg for at dit ESP32 board har MicroPython firmware installeret (se [Setup Guide](../../../docs/SETUP.md)).

### Trin 2: Åbn scriptet i Thonny

1. Åbn **Thonny** på din computer
2. Forbind din ESP32 med USB-kablet
3. Klik **File** → **Open** → find filen:
   ```
   Projects/Full MicroPython scripts/HTTP Server/http_smart_home.py
   ```
4. Filen åbner sig i Thonny

### Trin 3: Skriv dit WiFi-navn og password

Find disse to linjer i toppen af scriptet:

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

### Trin 4: Kør scriptet! 🚀

1. Klik den grønne **▶ Run** knap (eller tryk F5)
2. Vent et par sekunder...
3. I bunden af Thonny (i "Shell") ser du noget som dette:

```
=============================================
  ✅ WiFi Connected!
  📡 Network: MitWiFi

  🌐 Open this in your browser:
  👉 http://192.168.1.100
=============================================
```

### Trin 5: Åbn hjemmesiden! 🌐

1. Tag din **telefon** eller åbn en **browser** på din computer
2. Skriv adressen fra Shell (fx `http://192.168.1.100`)
3. Du ser nu en flot side med knapper! 🎉

### Trin 6: Styr dit hus! 🏠

- Tryk på **"Turn ON"** ved LED'en → Lyset tænder! 💡
- Tryk på **"Open"** ved døren → Døren åbner! 🚪
- Tryk på den **røde knap** ved farvelyset → Lampen bliver rød! 🔴
- Tryk på **"Play Sound"** → Buzzeren spiller! 🎵
- Se temperatur, luftfugtighed og sensor-status øverst! 🌡️

> 💡 **Tip:** Tryk på **"🔄 Refresh sensor data"** i bunden for at opdatere sensorværdierne.

---

## 🆘 Hjælp! Det virker ikke!

### "WiFi connection failed"
- Tjek at du har skrevet WiFi-navnet og koden rigtigt
- Tjek at `'` tegnene er der
- Sørg for at din ESP32 er tæt nok på din WiFi-router

### "Siden kan ikke indlæses" i browseren
- Sørg for at din telefon/computer er på **samme WiFi** som ESP32'en
- Prøv at skrive adressen igen (den fra Shell i Thonny)
- Vent 10 sekunder og prøv igen

### Scriptet stopper / crasher
- Tryk **Stop** (🔴) i Thonny
- Tryk **▶ Run** igen
- Hvis det stadig crasher, tryk på **EN/Reset** knappen på ESP32-boardet

### Sensorerne viser "--"
- Det er normalt de første par sekunder
- Tryk "Refresh" igen efter et par sekunder

---

## 📡 API Reference — Alle Endpoints

> **Brug disse endpoints fra curl, Python, Node-RED, eller enhver HTTP client!**
> Erstat `IP` med din ESP32's IP-adresse (fx `192.168.1.100`).

### 📥 GET — Hent sensordata (JSON)

| Endpoint | Beskrivelse | Response eksempel |
|----------|-------------|-------------------|
| `GET /sensors` | **Hent ALT** (sensorer + states) | `{"temperature":23,"humidity":45,"motion":0,"gas":512,"rain":1234,"led":0,"fan":"off","door":"closed","window":"closed","rgb":0}` |
| `GET /temperature` | Temperatur i °C | `{"temperature": 23}` |
| `GET /humidity` | Luftfugtighed i % | `{"humidity": 45}` |
| `GET /motion` | PIR bevægelsessensor (0/1) | `{"motion": 0}` |
| `GET /gas` | MQ2 gassensor (analog 0-4095, høj = mere gas) | `{"gas": 512}` |
| `GET /rain` | Regnsensor (analog 0-4095) | `{"rain": 1234}` |

### 🔧 GET — Hent aktuator-states (JSON)

| Endpoint | Beskrivelse | Response eksempel |
|----------|-------------|-------------------|
| `GET /led` | LED-status (0=off, 1=on) | `{"led": 0}` |
| `GET /fan` | Blæser-status | `{"fan": "off"}` |
| `GET /door` | Dør-status | `{"door": "closed"}` |
| `GET /window` | Vindue-status | `{"window": "closed"}` |
| `GET /rgb` | RGB-farve | `{"rgb": "off"}` |

### 📤 PUT — Send kommandoer (JSON)

| Endpoint | Body | Beskrivelse | Response eksempel |
|----------|------|-------------|-------------------|
| `PUT /led` | `on` / `off` | Tænd/sluk LED | `{"led": 1}` |
| `PUT /fan` | `on` / `off` | Start/stop blæser | `{"fan": "on"}` |
| `PUT /door` | `open` / `close` | Åbn/luk dør | `{"door": "open"}` |
| `PUT /window` | `open` / `close` | Åbn/luk vindue | `{"window": "open"}` |
| `PUT /rgb` | `0`-`4` | Skift farve (0=off, 1=rød, 2=grøn, 3=blå, 4=hvid) | `{"rgb": "green"}` |
| `PUT /buzzer` | `on` / `off` | Tænd/sluk buzzer | `{"buzzer": "on"}` |

### 🌐 GET — Browser-venlige shortcuts

Disse virker direkte i browserens adressefelt:

```
/led/on   /led/off
/fan/on   /fan/off
/door/open   /door/close
/window/open   /window/close
/rgb/0   /rgb/1   /rgb/2   /rgb/3   /rgb/4
/buzzer/play
```

### 💻 Eksempler

**curl:**
```bash
# Hent alle sensordata
curl http://IP/sensors

# Hent kun temperatur
curl http://IP/temperature

# Tænd LED
curl -X PUT http://IP/led -d "on"

# Skift RGB til grøn
curl -X PUT http://IP/rgb -d "2"

# Hent LED-status
curl http://IP/led
```

**Python:**
```python
import requests

# Hent alle data
data = requests.get("http://IP/sensors").json()
print(f"Temperatur: {data['temperature']}°C")

# Tænd blæser
requests.put("http://IP/fan", data="on")

# Hent kun dør-status
door = requests.get("http://IP/door").json()
print(f"Dør: {door['door']}")
```

**Node-RED:**
- Brug en **http request** node med method `GET` og URL `http://IP/sensors`
- Parse JSON output med en **json** node
- Brug en **http request** node med method `PUT` og URL `http://IP/led` og payload `on`

---

## 🧠 Hvordan virker det? (for de nysgerrige)

```
Din telefon                           ESP32
    │                                   │
    │── "GET /led/on" ────────────────►│ ← Du trykker "Turn ON"
    │                                   │ ← ESP32 tænder LED'en
    │◄── redirect til / ──────────────│ ← ESP32 sender redirect
    │── "GET /" ──────────────────────►│ ← Browser henter ny side
    │◄── HTML side med knapper ────────│ ← ESP32 sender websiden
    │                                   │
    │── "GET /sensors" ───────────────►│ ← curl/Python/Node-RED
    │◄── {"temperature":23,...} ────────│ ← JSON svar (lille, hurtigt)
```

1. **Browser:** Sender `GET /led/on` → ESP32 tænder LED → sender redirect → browser henter ny side
2. **API (curl/Python):** Sender `GET /sensors` → ESP32 svarer med lille JSON (ingen HTML!)
3. **PUT commands:** Sender `PUT /led` med body `on` → ESP32 tænder LED → svarer med JSON status

---

## 📁 Filer i denne mappe

| Fil | Beskrivelse |
|-----|-------------|
| `http_smart_home.py` | Hele scriptet — kopier ind og kør! |
| `README.md` | Denne manual du læser nu |

---

[← Tilbage til hovedsiden](../../../README.md)