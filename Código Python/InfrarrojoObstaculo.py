from umqtt.simple import MQTTClient
from machine import Pin
import network
import time


WIFI_SSID = "RaspBerry 7"
WIFI_PASSWORD = "linux4321"


MQTT_BROKER = "192.168.137.164"
MQTT_USER = ""
MQTT_PASSWORD = ""
MQTT_CLIENT_ID = "sensor_obstaculo_esp32"
MQTT_PORT = 1883
MQTT_TOPIC_PUB = "mc/infrarrojoObstaculo"


sensor_ir = Pin(27, Pin.IN)


ultimo_estado = None

# Función para conectar a 
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

# Conectar a WiFi y MQTT
if conectar_wifi():
    client = conectar_broker()

while True:
    
    obstaculo_detectado = sensor_ir.value()  # 0 = obstáculo detectado, 1 = camino libre
    
    if obstaculo_detectado != ultimo_estado:
        if obstaculo_detectado == 0:
            mensaje = "Obstáculo detectado"
        else:
            mensaje = "Camino libre"

        print(mensaje)
    
        try:
            client.publish(MQTT_TOPIC_PUB, mensaje)  # Publicar en MQTT
        except OSError as e:
            print(f"Error al publicar en MQTT: {e}")
            client = conectar_broker()  # Reintentar la conexión

    # Actualizar el estado anterior
    ultimo_estado = obstaculo_detectado