#Codigo en python para encender el Led de la Pico W mediante una interfaz web.
```
"""
Instituto Tecnologico de Tijuana
Programador: Montijo Perez Jose Alejandro
No.Control: 20212676
Raspberry pi W
Materia: Sistemas Programables
Practica: Embedded web server prender Led de la Picow

"""
from machine import ADC
import utime
import framebuf
import sys
from machine import Pin, I2C
from ssd1306 import SSD1306_I2C #Libreria añadida para controlar el oled

i2c=I2C(0,sda=Pin(0), scl=Pin(1), freq=400000) #Asignamos los pines a utilizar con el oled
oled = SSD1306_I2C(128, 64, i2c)

try:
  import usocket as socket
except:
  import socket

from machine import Pin
import network

#ssid = 'TP-Link_575C'
#password = 'MulitaWIFI2021'

import gc
gc.collect()

ssid = 'AndroidAP53F6'
password = 'aifd8540'

station = network.WLAN(network.STA_IF)

station.active(True)
station.connect(ssid, password)
print("print")
while station.isconnected() == False:
  pass

print('Connection successful')
print(station.ifconfig()[0])

led = Pin('LED', Pin.OUT)
led_state = "OFF"

def web_page():
    html = """<html>

<head>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.7.2/css/all.css"
     integrity="sha384-fnmOCqbTlWIlj8LyTjo7mOUStjsKC4pOpQbqyi7RrhN7udi9RwhKkMHpvLbHG9Sr" crossorigin="anonymous">
    <style>
        html {
            font-family: Arial;
            display: inline-block;
            margin: 0px auto;
            text-align: center;
        }

        .button {
            background-color: #ce1b0e;
            border: none;
            color: white;
            padding: 16px 40px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            margin: 4px 2px;
            cursor: pointer;
        }

        .button1 {
            background-color: #000000;
        }
    </style>
</head>

<body>
    <h2>Raspberry Pi Pico Web Server</h2>
    <p>LED state: <strong>""" + led_state + """</strong></p>
    <p>
        <i class="fas fa-lightbulb fa-3x" style="color:#c81919;"></i>
        <a href=\"led_on\"><button class="button">LED ON</button></a>
    </p>
    <p>
        <i class="far fa-lightbulb fa-3x" style="color:#000000;"></i>
        <a href=\"led_off\"><button class="button button1">LED OFF</button></a>
    </p>
</body>

</html>"""
    return html


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 8010))
s.listen(5)

prendido = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
0x00, 0x01, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x03, 0x00, 0x03, 0x00, 
0x01, 0x83, 0x06, 0x00, 0x00, 0x1f, 0xe0, 0x00, 0x00, 0x3f, 0xf0, 0x00, 0x00, 0x3f, 0xf0, 0x00, 
0x00, 0x7f, 0xf8, 0x00, 0x00, 0x7f, 0xf8, 0x00, 0x0e, 0x7f, 0xf9, 0xc0, 0x00, 0x7f, 0xf8, 0x00, 
0x00, 0x7f, 0xf8, 0x00, 0x00, 0x3f, 0xf0, 0x00, 0x00, 0x1f, 0xe0, 0x00, 0x00, 0x0f, 0xc0, 0x00, 
0x00, 0x0f, 0xc0, 0x00, 0x00, 0x0f, 0xc0, 0x00, 0x00, 0x07, 0x80, 0x00, 0x00, 0x07, 0x80, 0x00, 
0x00, 0x07, 0x80, 0x00, 0x00, 0x07, 0x80, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]


img=framebuf.FrameBuffer(bytearray(prendido), 30, 30, framebuf.MONO_HLSB)
while True:
    try:
        conn, addr = s.accept()
        conn.settimeout(3.0)
        print('Received HTTP GET connection request from %s' % str(addr))
        request = conn.recv(1024)
        conn.settimeout(None)
        request = str(request)
        print('GET Rquest Content = %s' % request)
        led_on = request.find('/led_on')
        led_off = request.find('/led_off')
        
        if led_on == 6:
            oled.fill(0)
            oled.text(station.ifconfig()[0],0,0)
            print('LED ON -> GPIO25')
            led_state = "ON"
            led.on()
            oled.blit(img,50,25) ##Imagen del oled
            oled.show()
        if led_off == 6:
            oled.fill(0)
            oled.text(station.ifconfig()[0],0,0)
            print('LED OFF -> GPIO25')
            led_state = "OFF"
            led.off()
            
            oled.show()
            
        response = web_page()
        conn.send('HTTP/1.1 200 OK\n')
        conn.send('Content-Type: text/html\n')
        conn.send('Connection: close\n\n')
        conn.sendall(response)
        conn.close()
    except OSError as e:
        conn.close()
        print('Connection closed')
        
    oled.show()
```
