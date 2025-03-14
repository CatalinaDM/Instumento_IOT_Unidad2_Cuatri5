from umqtt.simple import MQTTClient
from machine import Pin
import network
import time


WIFI_SSID = "RaspBerry 7"
WIFI_PASSWORD = "linux4321"

# Configuración MQTT
MQTT_BROKER = "192.168.137.164"
MQTT_USER = ""
MQTT_PASSWORD = ""
MQTT_CLIENT_ID = "led_bicolor_esp32"
MQTT_PORT = 1883
MQTT_TOPIC_PUB = "led/bicolor"


PIN_ROJO = 25  # GPIO25 - Rojo
PIN_VERDE = 26  # GPIO26 - Verde

# Configuración de pines como salida
led_rojo = Pin(PIN_ROJO, Pin.OUT)
led_verde = Pin(PIN_VERDE, Pin.OUT)

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
    print(f"Conectado a MQTT Broker: {MQTT_BROKER}")
    return client

# Función para cambiar el color del LED y publicar el estado
def alternar_led(client):
    while True:
        # Encender rojo
        led_rojo.value(1)
        led_verde.value(0)
        print("Rojo encendido")
        client.publish(MQTT_TOPIC_PUB, "rojo")
        time.sleep(3)

        # Encender verde
        led_rojo.value(0)
        led_verde.value(1)
        print("amarillo encendido")
        client.publish(MQTT_TOPIC_PUB, "amarillo")
        time.sleep(3)

# Conectar a WiFi y MQTT
if conectar_wifi():
    client = conectar_broker()
    alternar_led(client)
