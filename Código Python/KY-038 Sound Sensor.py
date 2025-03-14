from machine import Pin, ADC, reset
import time
import network
from umqtt.simple import MQTTClient


WIFI_SSID = "RaspBerry 7"
WIFI_PASSWORD = "linux4321"


MQTT_CLIENT_ID = "esp32_sound_sensor"
MQTT_BROKER = "192.168.137.164"
MQTT_PORT = 1883
MQTT_TOPIC = "sound_sensor_ky038"

sound_digital = Pin(14, Pin.IN)  # Salida digital (D0) a GPIO14
sound_analog = ADC(Pin(34))  # Salida analógica (A0) a GPIO36
sound_analog.atten(ADC.ATTN_11DB)  # Rango de 0 a 3.3V

# 📌 Función para conectar a WiFi
def conectar_wifi():
    print("Conectando a WiFi...", end="")
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect(WIFI_SSID, WIFI_PASSWORD)
    
    tiempo_max_espera = 10  # Espera máxima de 10 segundos
    while not sta_if.isconnected() and tiempo_max_espera > 0:
        print(".", end="")
        time.sleep(1)
        tiempo_max_espera -= 1

    if sta_if.isconnected():
        print("\nWiFi Conectada!")
    else:
        print("\nNo se pudo conectar a WiFi")
        reset()  # Reiniciar el ESP32 si no se conecta

# 📌 Función para conectar a MQTT
def conectar_mqtt():
    client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, port=MQTT_PORT)
    try:
        client.connect()
        print(f"Conectado a MQTT {MQTT_BROKER}")
        return client
    except Exception as e:
        print(f"Error al conectar a MQTT: {e}")
        reset()  # Reiniciar si falla

# 🚀 **Inicio del código**
conectar_wifi()
client = conectar_mqtt()

ultimo_valor = None

while True:
    try:
        # Leer valores del sensor
        sonido_digital = sound_digital.value()
        sonido_analogico = sound_analog.read()

        # Publicar solo si el valor digital cambia
        if sonido_digital != ultimo_valor:
            mensaje = f"D:{sonido_digital}, A:{sonido_analogico}"
            print(f" Publicando: {mensaje}")
            client.publish(MQTT_TOPIC, mensaje)
            ultimo_valor = sonido_digital

        time.sleep(0.5)  # Leer cada 500 ms

    except Exception as e:
        print(f"Error: {e}")
        time.sleep(1)
