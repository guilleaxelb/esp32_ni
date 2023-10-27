# Germán Andrés Xander 2023

from machine import Pin, Timer, unique_id
import dht
import time
import json
import ubinascii
from collections import OrderedDict
from settings import SERVIDOR_MQTT
from umqtt.robust import MQTTClient

CLIENT_ID = ubinascii.hexlify(unique_id()).decode('utf-8')

mqtt = MQTTClient(CLIENT_ID, SERVIDOR_MQTT,
                  port=8883, keepalive=10, ssl=True)

led = Pin(2, Pin.OUT)
d = dht.DHT22(Pin(25))
contador = 0
temperatura_superior = 27.0  # Temperatura superior
temperatura_inferior = 26.0  # Temperatura inferior
publicado = False            # bandera
  
def transmitir(pin):
    global publicado
    print("publicando con el ID:")
    print(CLIENT_ID)
    mqtt.connect()
    mqtt.publish(f"iot/{CLIENT_ID}",datos)
    mqtt.disconnect()
    publicado = True

while True:
    try:
        d.measure()
        temperatura = d.temperature()
        humedad = d.humidity()
        datos = json.dumps(OrderedDict([
            ('temperatura',temperatura),
            ('humedad',humedad)
        ]))
        print(datos)
        print(publicado)
        
        # Comprueba si la temperatura supera el límite superior
        if temperatura > temperatura_superior and not publicado:
            transmitir(None)  # Publica el mensaje
        elif temperatura < temperatura_inferior:
            publicado = False  # Restablece la bandera para futuros mensajes
    except OSError as e:
        print("sin sensor")
    time.sleep(5)
