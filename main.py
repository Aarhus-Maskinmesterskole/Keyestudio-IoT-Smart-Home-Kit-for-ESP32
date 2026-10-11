# Velkommen til denne video hvor vi vil få ESP32 til at host en HTTP PUT methode server
#
# Curl eksempler (skift IP ud med ESP32's IP fra serial monitor):
#
#   Styr LED:
#     curl -X PUT http://192.168.1.100/led -d "on"
#     curl -X PUT http://192.168.1.100/led -d "off"
#
#   Styr blæser:
#     curl -X PUT http://192.168.1.100/fan -d "forward"
#     curl -X PUT http://192.168.1.100/fan -d "backward"
#     curl -X PUT http://192.168.1.100/fan -d "stop"
#
#   Læs sensor data:
#     curl http://192.168.1.100/sensors
#
#   Styr servo (vinkel 0-180):
#     curl -X PUT http://192.168.1.100/servo -d "90"
#
#   Styr buzzer:
#     curl -X PUT http://192.168.1.100/buzz -d "on"
#     curl -X PUT http://192.168.1.100/buzz -d "off"
#
# LCD: kræver lcd_api.py og i2c_lcd.py uploadet til ESP32
#   mpremote cp lcd_api.py :lcd_api.py
#   mpremote cp i2c_lcd.py :i2c_lcd.py

import socket
import my_wifi
import machine
import dht
import json
from machine import I2C
from machine_i2c_lcd import I2cLcd

ssid = "Zyxel_C39A"
password = "8FQBM4J8A3"
my_wifi.my_wifi(ssid,password)

# ====================== sensor ==============================
temp_humid_sensor = dht.DHT11(machine.Pin(17))
steam_sensor = machine.Pin(34,machine.Pin.IN)
move_detection = machine.Pin(14,machine.Pin.IN)

mq2 = machine.ADC(machine.Pin(35))   # MQ2 gas sensor (analog) - detecterer røg, LPG, CO
mq2.atten(machine.ADC.ATTN_11DB)     # 0-3.3V range → 0-4095
mq2.width(machine.ADC.WIDTH_12BIT)

# LCD 16x2 via I2C (SDA=21, SCL=22, adresse typisk 0x27 eller 0x3F)
i2c = I2C(0, sda=machine.Pin(21), scl=machine.Pin(22), freq=400000)
lcd = I2cLcd(i2c, 0x27, 2, 16)
lcd.putstr("Starter...")


# ====================== aktuatorer ==========================
led = machine.Pin(12,machine.Pin.OUT)
led_state = 0

left_btn = machine.Pin(16,machine.Pin.IN, machine.Pin.PULL_UP)
right_btn = machine.Pin(27,machine.Pin.IN, machine.Pin.PULL_UP)

fan_forward = machine.Pin(19,machine.Pin.OUT)
fan_backward = machine.Pin(18,machine.Pin.OUT)  # var skrevet fan_forward to gange, det er nok backward

servo = machine.PWM(machine.Pin(26), freq=50)   # Servo motor
servo.duty(77)                                   # Start i midten (90 grader)

buzz = machine.PWM(machine.Pin(25), freq=1000)  # Passiv buzzer
buzz.duty(0)                                     # Start med lyd slukket

def set_servo(angle):
    # Konverter 0-180 grader til PWM duty (10-bit: 0-1023)
    # 0.5ms (duty≈26) = 0°,  1.5ms (duty≈77) = 90°,  2.5ms (duty≈128) = 180°
    duty = int(26 + (angle / 180) * 102)
    servo.duty(duty)

# ====================== webserver ===========================
addr = socket.getaddrinfo("0.0.0.0",80)[0][-1]

s = socket.socket()
s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
s.bind(addr)
s.listen(1)

print("Server kører på", addr)
lcd.clear()
lcd.putstr("Server klar!")

while True:
    # Tjek om en knap er holdt nede og styr blæseren
    if not left_btn.value():
        fan_forward.value(1)
        fan_backward.value(0)
        print("Blæser: fremad (knap)")
    elif not right_btn.value():
        fan_forward.value(0)
        fan_backward.value(1)
        print("Blæser: baglæns (knap)")

    cl, _ = s.accept()
    try:
        request = cl.recv(1024).decode()

        # Browser sender en tom request hvis den lukker forbindelsen
        if not request:
            cl.close()
            continue

        # Body kan mangle på GET requests - undgå crash
        parts_body = request.split("\r\n\r\n")
        body = parts_body[1].strip() if len(parts_body) > 1 else ""

        # Parse metode og sti fra request linjen, fx: "PUT /led HTTP/1.1"
        request_line = request.split("\r\n")[0]
        parts = request_line.split(" ")
        method = parts[0] if len(parts) > 0 else ""
        path = parts[1] if len(parts) > 1 else ""

        print(method, path)

        if method == 'PUT' and path == '/led':
            # Styr LED'en
            if body.lower() == 'on':
                led.value(1)
                led_state = led.value()
            elif body.lower() == 'off':
                led.value(0)
                led_state = led.value()
            response = "HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\n" + str(led_state)
            print("LED state:", led_state)

        elif method == 'PUT' and path == '/fan':
            # Styr blæseren via HTTP
            if body.lower() == 'forward':
                fan_forward.value(1)
                fan_backward.value(0)
            elif body.lower() == 'backward':
                fan_forward.value(0)
                fan_backward.value(1)
            elif body.lower() == 'stop':
                fan_forward.value(0)
                fan_backward.value(0)
            response = "HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\nBlæser opdateret: " + body
            print("Blæser:", body)

        elif method == 'PUT' and path == '/servo':
            # Styr servo vinkel 0-180
            try:
                angle = int(body)
                angle = max(0, min(180, angle))  # Klamp til 0-180
                set_servo(angle)
                response = "HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\nServo: " + str(angle) + " grader"
                print("Servo:", angle)
            except ValueError:
                response = "HTTP/1.1 400 Bad Request\r\nContent-Type: text/plain\r\n\r\nSend et tal mellem 0 og 180"

        elif method == 'PUT' and path == '/buzz':
            # Tænd/sluk buzzer
            if body.lower() == 'on':
                buzz.freq(1000)
                buzz.duty(512)   # 50% duty = fuld lydstyrke
            elif body.lower() == 'off':
                buzz.duty(0)
            response = "HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\nBuzzer: " + body
            print("Buzzer:", body)

        elif method == 'GET' and path == '/sensors':
            # Læs sensor data og send det tilbage som JSON
            try:
                temp_humid_sensor.measure()
                temp = temp_humid_sensor.temperature()
                humid = temp_humid_sensor.humidity()
            except Exception as e:
                print("Sensor fejl:", e)
                temp = 0
                humid = 0

            motion = move_detection.value()

            gas = mq2.read()

            # Opdater LCD med aktuelle værdier
            lcd.clear()
            lcd.move_to(0, 0)
            lcd.putstr("Temp: {}C".format(temp))
            lcd.move_to(0, 1)
            lcd.putstr("Humi: {}%".format(humid))

            data = json.dumps({
                "temperature": temp,
                "humidity": humid,
                "steam": steam_sensor.value(),
                "motion": motion,
                "gas": gas,              # 0-4095, høj værdi = mere gas/røg
                "led": led_state,
                "fan_forward": fan_forward.value(),
                "fan_backward": fan_backward.value()
            })
            response = "HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n\r\n" + data
            print("Sensor data sendt")

        else:
            # Browser prøver også /favicon.ico og lignende - bare 404
            response = "HTTP/1.1 404 Not Found\r\nContent-Type: text/plain\r\n\r\n404 Not Found"

        cl.send(response.encode())

    except OSError as e:
        print("Forbindelsesfejl:", e)
    finally:
        cl.close()
