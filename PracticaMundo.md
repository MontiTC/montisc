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
