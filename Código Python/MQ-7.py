from umqtt.simple import MQTTClient
from machine import Pin, ADC
import network
import time

# Configuración de WiFi
WIFI_SSID = "RaspBerry 7"
WIFI_PASSWORD = "linux4321"

# Configuración MQTT
MQTT_BROKER = "192.168.137.164"
MQTT_USER = ""
MQTT_PASSWORD = ""
MQTT_CLIENT_ID = "sensor_mq7_esp32"
MQTT_PORT = 1883
MQTT_TOPIC_PUB = "mc/mq7"


PIN_MQ7 = 34  # GPIO34 (ESP32) - Ajustar según tu conexión
mq7 = ADC(Pin(PIN_MQ7))
mq7.atten(ADC.ATTN_11DB)  # Configurar el rango de lectura (0-3.3V)

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

# Función para obtener el nivel de CO en PPM (Aproximado)
def leer_mq7():
    valor_adc = mq7.read()  # Lee el valor analógico (0-4095)
    voltaje = valor_adc * (3.3 / 4095) 
    ppm = valor_adc * (1000 / 4095)  
    return ppm

# Conectar a WiFi y MQTT
if conectar_wifi():
    client = conectar_broker()

while True:
    try:
        ppm = leer_mq7()
        mensaje = f"Nivel de CO: {ppm:.2f} PPM"
        print(mensaje)
        
        client.publish(MQTT_TOPIC_PUB, mensaje) 
        
        time.sleep(5)  
    except OSError as e:
        print(f"Error MQTT: {e}")
        client = conectar_broker()  # Reintentar conexión
