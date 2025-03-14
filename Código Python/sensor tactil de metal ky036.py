from umqtt.simple import MQTTClient
from machine import Pin
import network
import time


WIFI_SSID = "RaspBerry 7"
WIFI_PASSWORD = "linux4321"


MQTT_BROKER = "192.168.137.164"
MQTT_USER = ""
MQTT_PASSWORD = ""
MQTT_CLIENT_ID = "sensor_ky036_esp32"
MQTT_PORT = 1883
MQTT_TOPIC_PUB = "mc/ky036"


PIN_DO = 15  
sensor_digital = Pin(PIN_DO, Pin.IN)


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


def conectar_broker():
    client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, port=MQTT_PORT, user=MQTT_USER, password=MQTT_PASSWORD)
    client.connect()
    print(f"Conectado a MQTT Broker: {MQTT_BROKER}")
    return client


def leer_sensor():
    return sensor_digital.value()  # 0-false (sin contacto) o 1 (contacto detectado) true

if conectar_wifi():
    client = conectar_broker()

while True:
    try:
        contacto = leer_sensor()
        
        if contacto:  #if contacto == 1:.
            mensaje = "Sensor presionado"
        else:
            mensaje = "Sensor NO presionado"

        print(mensaje)
        client.publish(MQTT_TOPIC_PUB, mensaje)  

        time.sleep(1)  

    except OSError as e:
        print(f"Error MQTT: {e}")
        client = conectar_broker()  # Reintentar conexión
