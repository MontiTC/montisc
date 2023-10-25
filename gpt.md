#Codigo en Python
```
"""
Instituto Tecnologico de Tijuana
Programador: Montijo Perez Jose Alejandro
No.Control: 20212676
Raspberry pi W
Materia: Sistemas Programables
Practica: Prompt con ChatGPT api mediante un boton con un oled display

"""
import json
import network
import time
import urequests

from machine import Pin, I2C
from ssd1306 import SSD1306_I2C #Libreria añadida para controlar el oled

i2c=I2C(0,sda=Pin(0), scl=Pin(1), freq=400000) #Asignamos los pines a utilizar con el oled
oled = SSD1306_I2C(128, 64, i2c)

def chat_gpt(ssid, password, endpoint, api_key, model, prompt, max_tokens):
    """
        Description: This is a function to hit chat gpt api and get
            a response.
        
        Parameters:
        
        ssid[str]: The name of your internet connection
        password[str]: Password for your internet connection
        endpoint[str]: API enpoint
        api_key[str]: API key for access
        model[str]: AI model (see openAI documentation)
        prompt[str]: Input to the model
        max_tokens[int]: The maximum number of tokens to
            generate in the completion.
        
        Returns: Simply prints the response
    """
    # Just making our internet connection
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    
    # Wait for connect or fail
    max_wait = 10
    while max_wait > 0:
      if wlan.status() < 0 or wlan.status() >= 3:
        break
      max_wait -= 1
      print('waiting for connection...')
      time.sleep(1)
    # Handle connection error
    if wlan.status() != 3:
       print(wlan.status())
       raise RuntimeError('network connection failed')
    else:
      print('connected')
      print(wlan.status())
      status = wlan.ifconfig()
    
    ## Begin formatting request
    headers = {'Content-Type': 'application/json',
               "Authorization": "Bearer " + api_key}
    data = {"model": model,
            "prompt": prompt,
            "max_tokens": max_tokens}
    
    print("Attempting to send Prompt")
    r = urequests.post("https://api.openai.com/v1/{}".format(endpoint),
                       json=data,
                       headers=headers)
    
    if r.status_code >= 300 or r.status_code < 200:
        print("There was an error with your request \n" +
              "Response Status: " + str(r.text))
    else:
        print("Success")
        response_data = json.loads(r.text)
        completion = response_data["choices"][0]["text"]
        print(completion)
        oled.fill(0)
        oled.text(completion,0,0)
        oled.show()
    r.close()

#Para el boton
button_pin = machine.Pin(14, machine.Pin.IN, machine.Pin.PULL_UP)

def button_pressed(pin):
    print("¡Botón presionado!")
    chat_gpt('TecNM-ITT-Docentes',
         'tecnm2022!',
         "completions",
         "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",
         "text-davinci-001",
         "Quien gano el superbowl 45, solo dime el equipo",
         50)

# Asocia la función al evento de cambio en el pin del botón
button_pin.irq(trigger=machine.Pin.IRQ_FALLING, handler=button_pressed)

# El programa principal sigue ejecutándose
while True:
    pass
```
