import board
import digitalio
import time
# Configura el pin GP0 como salida
rele_pin = digitalio.DigitalInOut(board.GP19)
rele_pin.direction = digitalio.Direction.OUTPUT

# Función para activar el electroimán
def activar_electroiman():
    rele_pin.value = True  # Activa el relé (electroimán encendido)
    print("Electroimán activado")
     
# Función para desactivar el electroimán
def desactivar_electroiman():
    rele_pin.value = False  # Desactiva el relé (electroimán apagado)
    print("Electroimán desactivado")
# Activar y desactivar el electroimán con un intervalo
