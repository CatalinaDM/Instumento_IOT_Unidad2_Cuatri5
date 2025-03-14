import network
from umqtt.simple import MQTTClient
from machine import Pin, PWM
from time import sleep

# Configuración del broker MQTT
MQTT_BROKER = "broker.emqx.io"
MQTT_USER = ""
MQTT_PASSWORD = ""
MQTT_CLIENT_ID = "esp32_rgb"
MQTT_TOPIC = "mc/rgb_led"
MQTT_LOG_TOPIC = "mc/rgb_led"
MQTT_PORT = 1883

# Configuración de pines PWM para el LED RGB
pin_red = PWM(Pin(2), freq=1000)
pin_green = PWM(Pin(5), freq=1000)
pin_blue = PWM(Pin(18), freq=1000)

# Diccionario para convertir RGB en nombres de colores
COLOR_NAMES = {
    (255, 0, 0): "Rojo",
    (0, 255, 0): "Verde",
    (0, 0, 255): "Azul"
}

# Función para establecer el color del LED
def set_rgb(r, g, b):
    pin_red.duty(int(r * 1023 / 255))
    pin_green.duty(int(g * 1023 / 255))
    pin_blue.duty(int(b * 1023 / 255))
    color_name = COLOR_NAMES.get((r, g, b), f"Desconocido ({r},{g},{b})")
    print(f"Color actual: {color_name}")
    client.publish(MQTT_LOG_TOPIC, color_name)  # Publicar el nombre del color

# Función para conectar a WiFi
def conectar_wifi():
    print("Conectando WiFi...", end="")
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect('RaspBerry 7', 'linux4321')
    while not sta_if.isconnected():
        print(".", end="")
        sleep(0.3)
    print(" Conectado!")

# Función para conectarse al broker MQTT
def subscribir():
    global client
    client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, port=MQTT_PORT,
                        user=MQTT_USER, password=MQTT_PASSWORD, keepalive=0)
    client.connect()
    print(f"Conectado a {MQTT_BROKER}, suscrito a {MQTT_TOPIC}")
    return client

# Conectar a WiFi
conectar_wifi()
# Conectar a MQTT
client = subscribir()

# Ciclo automático de cambio de color cada 10 segundos
while True:
    for color in [(255, 0, 0), (0, 255, 0), (0, 0, 255)]:  # Rojo, Verde, Azul
        set_rgb(*color)
        sleep(10)  # Cambiar cada 10 segundos
