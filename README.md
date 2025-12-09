Raspberry Pi + NFC — Sistema de pases de lista escolar
Descripción
Repositorio con el código y la documentación para un sistema de pases de lista escolares basado en una Raspberry Pi y un lector NFC. Al acercar la tarjeta o tag NFC del estudiante, el dispositivo registra la asistencia localmente (CSV/JSON) y opcionalmente la sincroniza con una API externa o Google Sheets.
Características principales
- Registro automático de asistencia mediante NFC.
- Soporte para lectores comunes: RC522 (SPI) y PN532 (I2C/SPI).
- Almacenamiento local en CSV y opción de sincronización vía API.
- Configuración mediante config.yaml.
- Logs con timestamps y mensajes de confirmación.

Hardware y conexión
Componentes recomendados
- Raspberry Pi (3/4/Zero con pines GPIO).
- Lector NFC: RC522 o PN532.
- Tarjetas/tags NFC para estudiantes.
- Cables jumper y fuente de alimentación estable.
Conexión ejemplo RC522 (SPI)
- SDA → GPIO 8 (CE0)
- SCK → GPIO 11 (SCLK)
- MOSI → GPIO 10 (MOSI)
- MISO → GPIO 9 (MISO)
- RST → GPIO 25 (o pin libre)
- 3.3V → 3.3V
- GND → GND
Conexión ejemplo PN532 (I2C)
- SDA → SDA (GPIO 2)
- SCL → SCL (GPIO 3)
- VCC → 3.3V
- GND → GND
Importante: usar 3.3V para módulos que no soporten 5V; verificar la documentación del módulo.


Instalación y configuración
Requisitos de software
- Raspberry Pi OS actualizado.
- Python 3.7+.
- Habilitar SPI o I2C según el lector: sudo raspi-config → Interfaces.
- Entorno virtual recomendado.

sudo apt update && sudo apt upgrade -y
sudo raspi-config   # habilitar SPI o I2C según corresponda

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
