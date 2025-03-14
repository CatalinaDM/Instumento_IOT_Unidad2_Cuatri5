from umqtt.simple import MQTTClient
from machine import ADC, Pin
import network
import time

# Configuración WiFi
WIFI_SSID = "RaspBerry 7"
WIFI_PASSWORD = "linux4321"

# Configuración MQTT
MQTT_BROKER = "192.168.137.164"
MQTT_USER = ""
MQTT_PASSWORD = ""
MQTT_CLIENT_ID = "sensor_luz"
MQTT_PORT = 1883
MQTT_TOPIC_PUB = "mc/luzEstadoFotoresistencia"

sensor_luz = ADC(Pin(34))  
sensor_luz.atten(ADC.ATTN_11DB)  

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

# Función para leer la intensidad de luz
def leer_intensidad_luz():
    valor = sensor_luz.read()  # Leer el valor analógico (0-4095)
    print(f"Valor del sensor de luz: {valor}")
    
    # Clasificación de la luz en rangos
    if valor < 1000:
        return "Iluminado"
    elif valor < 3000:
        return "Medio oscuro"
    else:
        return "Muy oscuro"

# Conectar a WiFi y MQTT
if conectar_wifi():
    client = conectar_broker()

# Bucle principal
while True:
    # Leer el estado de la luz
    estado_luz = leer_intensidad_luz()
    print(f"Estado de luz: {estado_luz}")
    
    # Publicar el estado de la luz en MQTT
    client.publish(MQTT_TOPIC_PUB, estado_luz)
    
    
    time.sleep(3)
