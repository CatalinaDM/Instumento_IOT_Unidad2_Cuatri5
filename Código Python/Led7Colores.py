from umqtt.simple import MQTTClient
from machine import Pin, PWM
import network
import time

# 🌐 Configuración WiFi
WIFI_SSID = "RaspBerry 7"
WIFI_PASSWORD = "linux4321"


MQTT_BROKER = "192.168.137.164"
MQTT_USER = ""
MQTT_PASSWORD = ""
MQTT_CLIENT_ID = "led_rgb_esp32"
MQTT_PORT = 1883
MQTT_TOPIC_PUB = "mc/led7Colores"

# 🎨 Colores RGB
COLORES = {
    "Rojo": (255, 0, 0),
    "Verde": (0, 255, 0),
    "Azul": (0, 0, 255),
    "Amarillo": (255, 255, 0),
    "Cian": (0, 255, 255),
    "Magenta": (255, 0, 255),
    "Blanco": (255, 255, 255)
}

# 🔌 Pines PWM para el LED RGB
PIN_ROJO = PWM(Pin(26), freq=1000)
PIN_VERDE = PWM(Pin(27), freq=1000)
PIN_AZUL = PWM(Pin(25), freq=1000)

# 🔌 Función para conectar a WiFi
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

# 🔌 Función para conectar a MQTT
def conectar_broker():
    client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, port=MQTT_PORT, user=MQTT_USER, password=MQTT_PASSWORD)
    client.connect()
    print(f"Conectado a MQTT Broker: {MQTT_BROKER}")
    return client

# 🎨 Función para cambiar el color del LED
def set_color(rgb):
    r, g, b = rgb
    PIN_ROJO.duty(int(r * 1023 / 255))
    PIN_VERDE.duty(int(g * 1023 / 255))
    PIN_AZUL.duty(int(b * 1023 / 255))

# 🚀 Iniciar conexión
if conectar_wifi():
    client = conectar_broker()

# 🔄 Ciclo de cambio de colores
color_actual = None
colores_lista = list(COLORES.keys())  # Lista de nombres de colores
indice = 0

while True:
    color_nombre = colores_lista[indice]  # Nombre del color actual
    color_rgb = COLORES[color_nombre]  # Valores RGB

    if color_actual != color_nombre:
        set_color(color_rgb)  # Cambiar color del LED
        print(f"Color: {color_nombre}")
        
        try:
            client.publish(MQTT_TOPIC_PUB, color_nombre)  # Publicar color en MQTT
        except OSError as e:
            print(f"Error al publicar en MQTT: {e}")
            client = conectar_broker()  # Reintentar conexión

        color_actual = color_nombre  # Guardar el último color publicado

    indice = (indice + 1) % len(COLORES)  # Pasar al siguiente color
    time.sleep(3)  # Esperar 3 segundos antes del siguiente cambio
