from umqtt.simple import MQTTClient
from machine import ADC, Pin
import network
import time


WIFI_SSID = "RaspBerry 7"
WIFI_PASSWORD = "linux4321"

MQTT_BROKER = "192.168.137.164"
MQTT_USER = ""
MQTT_PASSWORD = ""
MQTT_CLIENT_ID = "sensor_gas_mq6"
MQTT_PORT = 1883
MQTT_TOPIC_PUB = "mc/gasMQ6"


sensor_analogico = ADC(Pin(34))  # Pin(entrada analógica)
sensor_analogico.atten(ADC.ATTN_11DB)  # Rango de lectura de 0 a 3.3V
sensor_digital = Pin(27, Pin.IN)  #Pin(entrada digital)

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

# 🔌 Función para conectar al broker MQTT
def conectar_broker():
    client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, port=MQTT_PORT, user=MQTT_USER, password=MQTT_PASSWORD)
    client.connect()
    print(f"Conectado a MQTT Broker: {MQTT_BROKER}")
    return client


def leer_concentracion_gas():
    valor_analogico = sensor_analogico.read()  # Lectura AO (0-4095)
    valor_digital = sensor_digital.value()  # Lectura DO (0 o 1)

    print(f"Valor AO: {valor_analogico} | DO: {valor_digital}")

    # Definir niveles de gas en base a la lectura analógica
    if valor_analogico < 1000:
        estado_gas = "Bajo nivel gas"
    elif valor_analogico < 2500:
        estado_gas = "Moderado - Precaución con el gas"
    else:
        estado_gas = "Alto - ¡Peligro se detecta mucho gas!"

    # Evaluar la salida digital
    if valor_digital == 1:
        estado_gas += " (No se detecto gas)"
    else:
        estado_gas += " (Se detecta gas, ¡¡¡CUIDADOOOO!!!)"

    return estado_gas


if conectar_wifi():
    client = conectar_broker()


while True:
    estado_gas = leer_concentracion_gas()
    print(f"Concentración de gas: {estado_gas}")


    client.publish(MQTT_TOPIC_PUB, estado_gas)

    time.sleep(3) 
