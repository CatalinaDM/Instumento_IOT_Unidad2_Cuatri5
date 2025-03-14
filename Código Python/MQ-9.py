from umqtt.simple import MQTTClient
from machine import Pin, ADC
import network
import time

WIFI_SSID = "RaspBerry 7"
WIFI_PASSWORD = "linux4321"


MQTT_BROKER = "192.168.137.164"
MQTT_USER = ""
MQTT_PASSWORD = ""
MQTT_CLIENT_ID = "gas_sensor_MQ9"
MQTT_PORT = 1883
MQTT_TOPIC_PUB = "mc/gasSensorMQ9"


MQ9_PIN = 32 
mq9 = ADC(Pin(MQ9_PIN))


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



if conectar_wifi():
    client = conectar_broker()

valor_anterior = mq9.read()  # Lee el valor inicial

# Bucle principal
while True:
    valor_actual = mq9.read() 
    print(f"Valor del MQ-9: {valor_actual}") 

    # Publicar en MQTT solo si hay cambio de valor significativo
    if abs(valor_actual - valor_anterior) > 10:  # Evita publicaciones repetidas con un margen de 10
        client.publish(MQTT_TOPIC_PUB, str(valor_actual))
        print(f"Publicado en MQTT: {valor_actual}")
        
        valor_anterior = valor_actual  

    time.sleep(1)  
