import urequests
from mfrc522 import MFRC522

import ujson
import time
from machine import Pin
import network
import utime  


SSID = "iCUCEI"
PASSWORD = ""

azul=Pin(18,Pin.OUT)

def conectar_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('Conectando a la red Wi-Fi...')
        wlan.connect(SSID, PASSWORD)
        while not wlan.isconnected():
            time.sleep(1)
    print('Conexión Wi-Fi establecida:', wlan.ifconfig())
    azul.value(1)
    time.sleep(1)
    azul.value(0)

# Enviar datos al servidor
def enviar_datos(id_tarjeta):
    url = "http://192.168.100.11:5000/verificar_asistencia"  # Usa tu IP local aquí
    
    # Obtener la fecha actual usando utime
    fecha = utime.localtime()
    fecha_str = "{:04}-{:02}-{:02}".format(fecha[0], fecha[1], fecha[2])  # Formato: YYYY-MM-DD
    
    data = {
        "id": id_tarjeta,
        "fecha": fecha_str
    }
    headers = {"Content-Type": "application/json"}
    try:
        response = urequests.post(url, headers=headers, json=data)
        print(response.json())
        status_code = response.status_code
        print(response.status_code)
        return status_code
        response.close()
        
    except Exception as e:
        print("Error al enviar los datos:", e)
        
        
# Conectar al Wi-Fi
conectar_wifi()

lector = MFRC522(spi_id=0, sck=2, miso=4, mosi=3, cs=1, rst=0)

verde=Pin(12,Pin.OUT)
rojo=Pin(13,Pin.OUT)
# Leer tarjeta NFC y enviar los datos
def leer_tarjeta():
    while True:
        lector.init()
        (stat, tag_type) = lector.request(lector.REQIDL)
        if stat == lector.OK:
            (stat, uid) = lector.SelectTagSN()
            if stat == lector.OK:
                identificador = int.from_bytes(bytes(uid), "little", False)
                print("UID de la tarjeta:", identificador)
            
                resultado = enviar_datos(identificador)
                if resultado == 200:  # Si el código es 200 (éxito)
                    verde.value(1)  # Enciende el LED verde
                    time.sleep(1)   # Espera 1 segundo
                    verde.value(0)  # Apaga el LED verde
                elif resultado == 500 or 404:  # Si el código es 500 (error)
                    rojo.value(1)   # Enciende el LED rojo
                    time.sleep(1)   # Espera 1 segundo
                    rojo.value(0)   # Apaga el LED rojo
                else:
                    print("Código de respuesta no manejado:", resultado)
                

# Ejecutar lectura de la tarjeta
leer_tarjeta()


