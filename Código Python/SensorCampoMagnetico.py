import network
from umqtt.simple import MQTTClient
from machine import ADC, Pin
from time import sleep

# Configuración del broker MQTT
MQTT_BROKER = "192.168.137.164"
MQTT_USER = ""
MQTT_PASSWORD = ""
MQTT_CLIENT_ID = "" 
MQTT_SENSOR_TOPIC = "utng/SensorCampoMagnetico"
MQTT_PORT = 1883

# Configuración del pin ADC (conectado a GPIO34)
sensor_analogico = ADC(Pin(34))  # Lectura analógica en GPIO34
sensor_analogico.atten(ADC.ATTN_11DB)  # Permite lecturas de hasta ~3.3V
sensor_analogico.width(ADC.WIDTH_12BIT)  # Resolución de 12 bits (0-4095)

# Conectar a WiFi
def conectar_wifi():
    print("Conectando a WiFi...", end="")
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect('RaspBerry 7', 'linux4321')  
    while not sta_if.isconnected():
        print(".", end="")
        sleep(0.3)
    print(" ¡Conectado!")

# Conectar al broker MQTT
def subscribir():
    client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, port=MQTT_PORT,
                        user=MQTT_USER, password=MQTT_PASSWORD, keepalive=60)
    client.connect()
    print(f"Conectado a {MQTT_BROKER}")
    print(f"Suscrito al tópico {MQTT_SENSOR_TOPIC}")
    return client

# Conectar a WiFi
conectar_wifi()

# Conectar a MQTT
client = subscribir()

# Ciclo de lectura del sensor de campo magnético
while True:
    valor_analogico = sensor_analogico.read()  # Lectura analógica (0-4095)
    
    # Si el valor es bajo, significa que hay campo magnético
    if valor_analogico < 1024:
        mensaje = "Detecta campo magnético"
    else:
        mensaje = "No se detecta campo magnético"

    print(mensaje)  # Mostrar en consola
    client.publish(MQTT_SENSOR_TOPIC, mensaje.encode())  # Publicar en MQTT

    sleep(0.5)  # Espera antes de la siguiente lectura