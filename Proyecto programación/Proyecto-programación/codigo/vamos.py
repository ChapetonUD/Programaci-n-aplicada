import pwmio
import board
import time
from api import api  # Importar la función api para la detección de objetos
from pruebaIman import activar_electroiman, desactivar_electroiman  # Importar las funciones del electroimán

# Configuración de los servomotores
servo_codo = pwmio.PWMOut(board.GP16, frequency=50)  # Servo del codo en GP16
servo_base = pwmio.PWMOut(board.GP17, frequency=50)  # Servo de la base en GP17
servo_hombro = pwmio.PWMOut(board.GP18, frequency=50)  # Servo del hombro en GP18

# Parámetros de los servomotores
min_duty = 1638  # 2.5% de duty cycle (0 grados)
max_duty = 8192  # 12.5% de duty cycle (180 grados)

# Función para mapear el ángulo a un valor de duty cycle
def map_angle_to_duty(angle):
    return min_duty + (max_duty - min_duty) * angle // 180

# Función para mover un servomotor a un ángulo específico
def move_servo(servo, angle):
    duty_cycle = map_angle_to_duty(angle)
    servo.duty_cycle = duty_cycle

# Posición inicial (0, 0, 0)
def set_home_position():
    move_servo(servo_hombro, 140)   # Hombro en 0 grados
    time.sleep(1)
    move_servo(servo_codo, 90)     # Codo en 0 grados
    time.sleep(1)
    move_servo(servo_base, 30)    # Base en 30 grados
    time.sleep(1)
    print("Posición inicial (0, 0, 0) establecida.")

# Función para mover el brazo hacia el objeto
def move_to_object(object_x, object_y):
    # Mover el brazo en el eje X con el hombro
    move_servo(servo_hombro, 10)  # Esto sigue moviendo el hombro de izquierda a derecha
    time.sleep(1)

    # Mover el codo normalmente, si es necesario
    move_servo(servo_codo, 40)
    time.sleep(1)
    
    # Ajustar el ángulo del hombro para que baje más
    # A medida que object_y aumenta, el brazo debe bajar más
    # Mapeamos object_y (en el rango 0-40) a un rango de ángulos para el hombro (por ejemplo, de 30 a 150 grados)
    
    hombro_angle = int(30+ (object_y / 40) * 120)  # Mapeo de Y a ángulo del hombro
    print(f"Moviendo hombro a {hombro_angle} grados basado en Y: {object_y}")
    
    move_servo(servo_hombro, hombro_angle)  # Mueve el hombro
    time.sleep(1)

    print("Brazo movido hacia el objeto.")

# Función principal
def main():
    # Activar el electroimán al inicio del ciclo
    activar_electroiman()
    print("Electroimán activado al inicio.")
    
    # Establecer la posición inicial al iniciar el programa
    set_home_position()

    # Temporizador para controlar cuándo se desactiva el electroimán
    electroimán_tiempo = 10  # En segundos, por ejemplo 10 segundos
    start_time = time.time()  # Guarda el tiempo actual al principio del ciclo

    while True:
        # Detectar un objeto usando la cámara
        object_x, object_y = api()  # Llamar a la función api para obtener la posición del objeto

        if object_x is not None and object_y is not None:
            print(f"Objeto detectado en ({object_x}, {object_y}). Moviendo brazo...")

            # Mover el brazo hacia el objeto, con el ajuste para "agacharlo"
            move_to_object(object_x, object_y)

            # Mantener la posición durante 5 segundos
            time.sleep(5)

            # Rotar la base 90 grados después de 5 segundos
            move_servo(servo_base, 120)  # Cambia el ángulo de la base a 120 grados
            time.sleep(1)

            # Volver a la posición inicial (0, 0, 0)
            set_home_position()

        else:
            print("No se detectó ningún objeto.")

        # Verificar si el electroimán debe desactivarse después del intervalo de tiempo
        if time.time() - start_time >= electroimán_tiempo:
            desactivar_electroiman()
            print(f"Electroimán desactivado después de {electroimán_tiempo} segundos.")
            start_time = time.time()  # Reiniciar el contador del electroimán para que siga en su ciclo

        time.sleep(1)  # Esperar 1 segundo antes de la siguiente detección

# Ejecutar la función principal
main()
