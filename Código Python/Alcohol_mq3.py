from umqtt.simple import MQTTClient
from machine import Pin, ADC
import network
import time

# Configuración WiFi
WIFI_SSID = "RaspBerry 7"
WIFI_PASSWORD = "linux4321"

# Configuración MQTT
MQTT_BROKER = "192.168.137.164"
MQTT_USER = ""
MQTT_PASSWORD = ""
MQTT_CLIENT_ID = "sensor_mq3"
MQTT_PORT = 1883
MQTT_TOPIC_PUB = "mc/estadoAlcohol_mq3"


MQ3_PIN = 34 
sensor_alcohol = ADC(Pin(MQ3_PIN))


sensor_alcohol.atten(ADC.ATTN_11DB)  

# Función para conectar a WiFi
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

# Función para conectar al broker MQTT
def conectar_broker():
    client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, port=MQTT_PORT, user=MQTT_USER, password=MQTT_PASSWORD)
    client.connect()
    print(f"Conectado a MQTT Broker: {MQTT_BROKER}")
    return client

# Función para leer el valor del MQ-3 y clasificar el estado
def leer_estado_alcohol():
    valor = sensor_alcohol.read()
    print(f"Valor MQ-3: {valor}")

    # Clasificación del estado
    if valor < 1599:
        estado = "Sin alcohol"
    elif valor > 1600:
        estado = "Alto nivel de alcohol"
    else:
        estado = "Sin datos especificos"

    print(f"Estado: {estado}")
    return estado


if conectar_wifi():
    client = conectar_broker()


while True:
   
    estado_alcohol = leer_estado_alcohol()
    

    client.publish(MQTT_TOPIC_PUB, estado_alcohol)
    
    # Esperar 5 segundos antes de la siguiente lectura
    time.sleep(5)