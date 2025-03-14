from umqtt.simple import MQTTClient
from machine import Pin, PWM
import network
import time

# Configuración de WiFi
WIFI_SSID = "RaspBerry 7"
WIFI_PASSWORD = "linux4321"

# Configuración MQTT
MQTT_BROKER = "192.168.137.26"
MQTT_USER = ""
MQTT_PASSWORD = ""
MQTT_CLIENT_ID = "led_rgb_esp32"
MQTT_PORT = 1883
MQTT_TOPIC_PUB = "led/rgb"

PIN_RED = 25   
PIN_GREEN = 26 
PIN_BLUE = 27  

# Configuración PWM para controlar el brillo de cada color
led_red = PWM(Pin(PIN_RED), freq=1000)
led_green = PWM(Pin(PIN_GREEN), freq=1000)
led_blue = PWM(Pin(PIN_BLUE), freq=1000)

colors = [(255, 0, 0, "rojo"), (0, 255, 0, "verde"), (0, 0, 255, "azul"), (255, 255, 0, "amarillo"), (0, 255, 255, "cian"), (255, 0, 255, "magenta")]


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


def set_color(r, g, b):
    led_red.duty(int(r * 1023 / 255))
    led_green.duty(int(g * 1023 / 255))
    led_blue.duty(int(b * 1023 / 255))


if conectar_wifi():
    client = conectar_broker()
    index = 0
    while True:
        try:
            r, g, b, color_name = colors[index]
            set_color(r, g, b)
            client.publish(MQTT_TOPIC_PUB, color_name)
            print(f"Color enviado: {color_name}")
            index = (index + 1) % len(colors)  # Cambia al siguiente color
            time.sleep(3)  # Espera 3 segundos antes de cambiar
        except OSError as e:
            print(f"Error MQTT: {e}")
            client = conectar_broker()  # Reintentar conexión
