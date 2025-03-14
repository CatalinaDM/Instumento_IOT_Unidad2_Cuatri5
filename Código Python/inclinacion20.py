from umqtt.simple import MQTTClient
from machine import Pin
import network
import time

# Configuración WiFi
WIFI_SSID = "RaspBerry 7"
WIFI_PASSWORD = "linux4321"

# Configuración MQTT
MQTT_BROKER = "192.168.137.164"
MQTT_USER = ""
MQTT_PASSWORD = ""
MQTT_CLIENT_ID = "tilt_sensor_SW520D"
MQTT_PORT = 1883
MQTT_TOPIC_PUB = "mc/tilt_sensor_SW520D"


TILT_PIN = 5  
tilt = Pin(TILT_PIN, Pin.IN, Pin.PULL_UP)  # Entrada con pull-up

# Función para conectar a WiFi
def conectar_wifi():
    print("Conectando a WiFi...", end="")
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect(WIFI_SSID, WIFI_PASSWORD)

    start_time = time.time()
    while not sta_if.isconnected():
        if time.time() - start_time > 10:
            print("\nError al conectar a WiFi: Tiempo de espera agotado")
            return False
        print(".", end="")
        time.sleep(0.3)
    
    print("\nWiFi Conectada!")
    print("IP:", sta_if.ifconfig()[0])
    return True

# Función para conectar al broker MQTT
def conectar_broker():
    client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, port=MQTT_PORT, user=MQTT_USER, password=MQTT_PASSWORD)
    client.connect()
    print(f"Conectado a MQTT Broker: {MQTT_BROKER}, Topic: {MQTT_TOPIC_PUB}")
    return client

# Conectar a WiFi y MQTT
if conectar_wifi():
    client = conectar_broker()

estado_anterior = tilt.value()  # Guarda el estado inicial

# Bucle principal
while True:
    estado_actual = tilt.value()  
    print(f"Estado del SW-520D: {estado_actual}")  # Mostrar en consola

    # Publicar en MQTT solo si hay cambio de estado
    if estado_actual != estado_anterior:
        client.publish(MQTT_TOPIC_PUB, str(estado_actual))
        print(f"Publicado: {estado_actual}")
        estado_anterior = estado_actual  # Actualizar estado anterior

    time.sleep(0.5)  # Pequeño retraso para evitar lecturas repetidas
