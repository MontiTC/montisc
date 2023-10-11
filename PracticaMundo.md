# Practica de mostrar Hola mundo y hora Internet en un Oled utilizando una Rasberry PI

## Hola Mundo

Codigo Python 
```
from machine import Pin, I2C
from ssd1306 import SSD1306_I2C

i2c=I2C(0,sda=Pin(0), scl=Pin(1), freq=400000)
oled = SSD1306_I2C(128, 64, i2c)

oled.text("Hola Mundo", 0, 0)
oled.show()
```
![Imagen de la practica](Mundo.jpg)

## Hora Internet

Codigo Python 
```
import ntptime
import time

from machine import Pin, I2C
from ssd1306 import SSD1306_I2C

i2c=I2C(0,sda=Pin(0), scl=Pin(1), freq=400000)
oled = SSD1306_I2C(128, 64, i2c)

# Configura el servidor NTP (puedes cambiarlo si lo deseas)
ntp_server = "pool.ntp.org"

# Intenta obtener la hora de Internet
try:
    ntptime.settime()
    print("Hora de Internet obtenida correctamente.")
except Exception as e:
    print("Error al obtener la hora de Internet:", e)

# Imprime la hora actual
rtc_time = time.localtime()
print("Hora actual: {}/{}/{} {}:{}:{}".format(
    rtc_time[1], rtc_time[2], rtc_time[0],
    rtc_time[3], rtc_time[4], rtc_time[5]))

oled.text("{}/{}/{} {}:{}:{}".format(
    rtc_time[1], rtc_time[2], rtc_time[0],
    rtc_time[3], rtc_time[4], rtc_time[5]),0,0)
oled.show()
```
![Imagen de la practica](HoraI.jpg)
