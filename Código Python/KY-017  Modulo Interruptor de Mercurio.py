import machine
import time
import network
from umqtt.simple import MQTTClient


MERCURY_PIN = 15 
sensor = machine.Pin(MERCURY_PIN, machine.Pin.IN)

# Configuración de la red WiFi
WIFI_SSID = 'LEO'
WIFI_PASSWORD = '94941890'


MQTT_BROKER = '192.168.137.191'  
MQTT_PORT = 1883
MQTT_TOPIC = 'mc/mercurioInclinacion'


def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(WIFI_SSID, WIFI_PASSWORD)

    while not wlan.isconnected():
        time.sleep(1)
    
    print('Conectado a WiFi:', wlan.ifconfig())


connect_wifi()


client = MQTTClient('ESP32_client', MQTT_BROKER, port=MQTT_PORT)
client.connect()
print("Conectado al broker MQTT")


try:
    while True:
        estado = sensor.value()  
        
        # Convertir estado a string y enviar por MQTT
        mensaje = str(estado)
        print("Enviando:", mensaje)
        client.publish(MQTT_TOPIC, mensaje)

        time.sleep(1) 

except KeyboardInterrupt:
    print("Programa detenido por el usuario")
    client.disconnect()
