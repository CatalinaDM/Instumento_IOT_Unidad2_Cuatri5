from machine import Pin, reset
import time
import network
from umqtt.simple import MQTTClient


WIFI_SSID = "RaspBerry 7"
WIFI_PASSWORD = "linux4321"


MQTT_CLIENT_ID = "esp32_vibration_sensor"
MQTT_BROKER = "192.168.137.164"
MQTT_PORT = 1883
MQTT_TOPIC = "vibration_sensor"


vibration_sensor_pin = Pin(14, Pin.IN)

def conectar_wifi():
    print("Conectando a WiFi...", end="")
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect(WIFI_SSID, WIFI_PASSWORD)
    
    tiempo_max_espera = 10  # Espera máxima de 10 segundos
    while not sta_if.isconnected() and tiempo_max_espera > 0:
        print(".", end="")
        time.sleep(1)
        tiempo_max_espera -= 1

    if sta_if.isconnected():
        print("\nWiFi Conectada!")
    else:
        print("\nNo se pudo conectar a WiFi")
        reset() 


def llegada_mensaje(topic, msg):
    print(f"Mensaje recibido en {topic.decode()}: {msg.decode()}")


def conectar_mqtt():
    client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, port=MQTT_PORT)
    client.set_callback(llegada_mensaje)  # Asignar la función para recibir mensajes
    try:
        client.connect()
        client.subscribe(MQTT_TOPIC)  # Suscribirse al tópico de vibración
        print(f"Conectado a MQTT {MQTT_BROKER} y suscrito a {MQTT_TOPIC}")
        return client
    except Exception as e:
        print(f"Error al conectar a MQTT: {e}")
        reset()  

conectar_wifi()

client = conectar_mqtt()

ultimo_valor = None
while True:
    try:
  
        valor_vibracion = vibration_sensor_pin.value()

        # Solo publica si el valor ha cambiado
        if valor_vibracion != ultimo_valor:
            mensaje = str(valor_vibracion)
            print(f" Publicando valor de vibración: {mensaje}")
            client.publish(MQTT_TOPIC, mensaje)
            ultimo_valor = valor_vibracion  

        # Revisar si hay mensajes en el tópico (para ver los valores publicados)
        client.check_msg()

    except Exception as e:
        print(f"Error en la lectura del sensor: {e}")

    time.sleep(1)  