from umqtt.simple import MQTTClient
from machine import Pin, ADC
import network
import time


WIFI_SSID = "RaspBerry 7"
WIFI_PASSWORD = "linux4321"


MQTT_BROKER = "192.168.137.164"
MQTT_USER = ""
MQTT_PASSWORD = ""
MQTT_CLIENT_ID = "sensor_lm35"
MQTT_PORT = 1883
MQTT_TOPIC_PUB = "mc/temperaturalm35"

# Configuración del sensor LM35 en el pin GPIO 34 (canal ADC)
SENSOR_PIN = 34
sensor = ADC(Pin(SENSOR_PIN))
sensor.atten(ADC.ATTN_11DB)  

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

# Función para convertir valor analógico a grados Celsius
def convertir_a_celsius(valor_analogico):
    # Convertir valor analógico a voltaje
    voltaje = (valor_analogico / 4095.0) * 3.6  
    # Convertir voltaje a temperatura en grados Celsius
    temperatura = voltaje * 100
    temperatura = round(temperatura, 1)
    return temperatura

# Conectar a WiFi y MQTT
if conectar_wifi():
    client = conectar_broker()

# Bucle principal
while True:
    # Leer valor analógico del sensor
    valor_analogico = sensor.read()
    
    # Convertir a grados Celsius usando la función
    temperatura = convertir_a_celsius(valor_analogico)
    print(f"Valor analógico: {valor_analogico} | Temperatura: {temperatura}°C")
    client.publish(MQTT_TOPIC_PUB, str(temperatura))
    time.sleep(5)
