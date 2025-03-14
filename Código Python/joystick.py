from umqtt.simple import MQTTClient
from machine import Pin, ADC
import network
import time


WIFI_SSID = "RaspBerry 7"
WIFI_PASSWORD = "linux4321"


MQTT_BROKER = "192.168.137.164"
MQTT_USER = ""
MQTT_PASSWORD = ""
MQTT_CLIENT_ID = "joystick_client"
MQTT_PORT = 1883
MQTT_TOPIC_PUB = "joystick/posicion"

# Pines del joystick
JOY_X_PIN = 34
JOY_Y_PIN = 35  


# Inicialización de los pines analógicos
joy_x = ADC(Pin(JOY_X_PIN))
joy_y = ADC(Pin(JOY_Y_PIN))
joy_x.atten(ADC.ATTN_11DB)  
joy_y.atten(ADC.ATTN_11DB)

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

# Función para leer los valores del joystick
def leer_joystick():
    x_val = joy_x.read()
    y_val = joy_y.read()
    print(f"Joystick X: {x_val}, Y: {y_val}")
    return x_val, y_val

if conectar_wifi():
    client = conectar_broker()

while True:
    x, y = leer_joystick()
    payload = f"x: {x}, y: {y}"  
    print("Enviando:", payload) 
    client.publish(MQTT_TOPIC_PUB, payload)
    time.sleep(0.5)
