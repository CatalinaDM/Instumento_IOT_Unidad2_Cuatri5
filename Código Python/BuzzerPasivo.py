import MQTTClient
from machine import Pin, PWM
import network
import time

# Configuración WiFi
WIFI_SSID = "RaspBerry 7"
WIFI_PASSWORD = "linux4321"

# Configuración MQTT
MQTT_BROKER = "192.168.137.164"
MQTT_USER = ""
MQTT_PASSWORD = ""
MQTT_CLIENT_ID = "buzzer_melodia"
MQTT_PORT = 1883
MQTT_TOPIC_PUB = "mc/buzzerP"

# Configuración del buzzer pasivo
BUZZER_PIN = 4  # GPIO para el buzzer (D2 en ESP8266)
buzzer = PWM(Pin(BUZZER_PIN))

# Notas musicales (frecuencias en Hz)
notas = {
    'C4': 262,
    'D4': 294,
    'E4': 330,
    'F4': 349,
    'G4': 392,
    'A4': 440,
    'B4': 494,
    'C5': 523
}

# Melodía (Ejemplo de "Do Re Mi Fa Sol La Si Do")
melodia = [
    ('C4', 0.5),
    ('D4', 0.5),
    ('E4', 0.5),
    ('F4', 0.5),
    ('G4', 0.5),
    ('A4', 0.5),
    ('B4', 0.5),
    ('C5', 0.5)
]

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

# Función para reproducir una nota
def reproducir_nota(nota, duracion):
    if nota in notas:
        frecuencia = notas[nota]
        buzzer.freq(frecuencia)
        buzzer.duty(512)  # 50% del ciclo de trabajo para el sonido
        time.sleep(duracion)
        buzzer.duty(0)  # Apagar el sonido
        time.sleep(0.05)  # Pausa corta entre notas

# Función para reproducir la melodía
def reproducir_melodia():
    print("Reproduciendo melodía...")
    client.publish(MQTT_TOPIC_PUB, "Activado")
    for nota, duracion in melodia:
        reproducir_nota(nota, duracion)
    buzzer.duty(0)  # Apagar el buzzer al terminar
    print("Melodía terminada.")

# Conectar a WiFi y MQTT
if conectar_wifi():
    client = conectar_broker()

# Bucle principal
while True:
    # Reproduce la melodía
    reproducir_melodia()
    
    # Publicar el estado "Desactivado"
    print("Buzzer Desactivado")
    client.publish(MQTT_TOPIC_PUB, "Desactivado")
    
    # Esperar 3 segundos antes de volver a iniciar la melodía
    time.sleep(3)