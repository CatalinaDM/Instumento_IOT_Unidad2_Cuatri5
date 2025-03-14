from umqtt.simple import MQTTClient
from machine import Pin
import network
import time


WIFI_SSID = "RaspBerry 7"
WIFI_PASSWORD = "linux4321"


MQTT_BROKER = "192.168.137.164"
MQTT_USER = ""
MQTT_PASSWORD = ""
MQTT_CLIENT_ID = "sensor_impacto_esp32"
MQTT_PORT = 1883
MQTT_TOPIC_PUB = "mc/impacto"


sensor_impacto = Pin(27, Pin.IN)


ultimo_estado = None  


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


if conectar_wifi():
    client = conectar_broker()

while True:
    impacto_detectado = sensor_impacto.value()  # (1 = impacto detectado, 0 = sin impacto)

    if impacto_detectado != ultimo_estado:  
        if impacto_detectado == 1:
            mensaje = "Impacto detectado"
        else:
            mensaje = "Sin impactos"

        print(f"ESTADO: {mensaje}")
        client.publish(MQTT_TOPIC_PUB, mensaje) 
        ultimo_estado = impacto_detectado  # Actualizar el último estado

    time.sleep(1) 
