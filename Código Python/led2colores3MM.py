from umqtt.simple import MQTTClient
from machine import Pin
import network
import time


WIFI_SSID = "RaspBerry 7"
WIFI_PASSWORD = "linux4321"


MQTT_BROKER = "192.168.137.164"
MQTT_USER = ""
MQTT_PASSWORD = ""
MQTT_CLIENT_ID = "led_control_esp32"
MQTT_PORT = 1883
MQTT_TOPIC_SUB = "sensor/led-2-colores3mm"


led_rojo = Pin(25, Pin.OUT)
led_verde = Pin(26, Pin.OUT)


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
    client.set_callback(mqtt_callback)  # Asigna función de recepción
    client.connect()
    client.subscribe(MQTT_TOPIC_SUB)  
    print(f"Conectado a MQTT Broker: {MQTT_BROKER} y suscrito a {MQTT_TOPIC_SUB}")
    return client


def mqtt_callback(topic, msg):
    mensaje = msg.decode('utf-8')
    print({mensaje})

    if mensaje == "rojo":
        led_rojo.value(1)
        led_verde.value(0)
        print("LED Rojo encendido")

    elif mensaje == "amarillo":
        led_rojo.value(0)
        led_verde.value(1)
        print("LED Amarilla encendido")

    elif mensaje == "apagado":
        led_rojo.value(0)
        led_verde.value(0)
        print("LED Apagado")


if conectar_wifi():
    client = conectar_broker()

while True:
    try:
        client.check_msg()  # Escucha mensajes MQTT
        time.sleep(1)
        
    except Exception as e:
        print("Error en la conexión MQTT:", e)
        time.sleep(5)
        client = conectar_broker()  # Reintenta conexión si falla
