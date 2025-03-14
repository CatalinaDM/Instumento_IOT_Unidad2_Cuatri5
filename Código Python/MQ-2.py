import machine
import time
import network
from umqtt.simple import MQTTClient


MQ2_PIN = 34  
sensor_gas = machine.ADC(machine.Pin(MQ2_PIN))
sensor_gas.atten(machine.ADC.ATTN_11DB)  # Ajuste para rango de voltaje de 0 a 3.3V
sensor_gas.width(machine.ADC.WIDTH_12BIT)  # Resolución de 12 bits (0-4095)

UMBRAL_GAS = 2000  


WIFI_SSID = 'RaspBerry 7'
WIFI_PASSWORD = 'linux4321'


MQTT_BROKER = '192.168.137.164'  
MQTT_PORT = 1883
MQTT_TOPIC = 'mc/gasMQ2'

# Función para conectar a WiFi
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(WIFI_SSID, WIFI_PASSWORD)
    while not wlan.isconnected():
        time.sleep(1)
    print('Conectado a WiFi')


connect_wifi()


def mqtt_callback(topic, msg):
    print('Mensaje recibido:', topic.decode(), msg.decode())

# Crear el cliente MQTT y configurar la conexión
client = MQTTClient('ESP32_client', MQTT_BROKER, port=MQTT_PORT)
client.set_callback(mqtt_callback)
client.connect()

try:
    while True:
        valor = sensor_gas.read()  # Leer el valor del sensor (0-4095)
        print(f"Nivel de gas detectado: {valor}")

       
        client.publish(MQTT_TOPIC, str(valor))

       
        if valor > UMBRAL_GAS:
            print("¡Alerta! Nivel alto de gas detectado ")
            client.publish(MQTT_TOPIC, "⚠ ¡Nivel alto de gas detectado! ")

        time.sleep(5)  

except KeyboardInterrupt:
    print("Programa detenido")
    client.disconnect()