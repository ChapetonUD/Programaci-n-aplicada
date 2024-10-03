import socketpool
import wifi
import pwmio
import board

# Conectar a la red Wi-Fi
wifi.radio.connect("Chipi", "sapinpepin")
pool = socketpool.SocketPool(wifi.radio)

print("wifi.radio:", wifi.radio.hostname, wifi.radio.ipv4_address)
s = pool.socket()
s.bind(('', 80))
s.listen(5)

# Configuración de los servomotores
servo1 = pwmio.PWMOut(board.GP0, frequency=50)
servo2 = pwmio.PWMOut(board.GP1, frequency=50)  
servo3 = pwmio.PWMOut(board.GP2, frequency=50)  
min_duty = 1638  # 2.5% de duty cycle
max_duty = 8192  # 12.5% de duty cycle

# Función para mapear el ángulo a un valor de duty cycle
def map_angle_to_duty(angle):
    return min_duty + (max_duty - min_duty) * angle // 180

# Inicializar los servomotores en 0 grados
servo1.duty_cycle = map_angle_to_duty(0)
servo2.duty_cycle = map_angle_to_duty(0)
servo3.duty_cycle = map_angle_to_duty(0)
print("Servos inicializados a 0 grados")

# Página HTML con tres sliders
html = """
<!DOCTYPE html>
<html>
<head>
    <title>Control de Servos</title>
</head>
<body>
    <h1>Control de Servos</h1>
    
    <!-- Slider para el primer servomotor -->
    <label for="slider1">Angulo del Servo 1:</label>
    <input type="range" id="slider1" min="90" max="180" value="90" oninput="updateServo1(this.value)">
    <p>Angulo seleccionado Servo 1: <span id="angleValue1">45</span> grados</p>

    <!-- Slider para el segundo servomotor (base) -->
    <label for="slider2">Angulo del Servo 2 (Base):</label>
    <input type="range" id="slider2" min="0" max="180" value="0" oninput="updateServo2(this.value)">
    <p>Angulo seleccionado Servo 2 (Base): <span id="angleValue2">90</span> grados</p>

    <!-- Slider para el tercer servomotor (nuevo) -->
    <label for="slider3">Angulo del Servo 3:</label>
    <input type="range" id="slider3" min="0" max="180" value="0" oninput="updateServo3(this.value)">
    <p>Angulo seleccionado Servo 3: <span id="angleValue3">90</span> grados</p>

    <script>
        // Función para enviar el ángulo del primer servo
        function updateServo1(value) {
            document.getElementById("angleValue1").innerText = value;
            var xhr = new XMLHttpRequest();
            xhr.open("GET", "/set_servo1?value=" + value, true);
            xhr.send();
        }

        // Función para enviar el ángulo del segundo servo
        function updateServo2(value) {
            document.getElementById("angleValue2").innerText = value;
            var xhr = new XMLHttpRequest();
            xhr.open("GET", "/set_servo2?value=" + value, true);
            xhr.send();
        }

        // Función para enviar el ángulo del tercer servo
        function updateServo3(value) {
            document.getElementById("angleValue3").innerText = value;
            var xhr = new XMLHttpRequest();
            xhr.open("GET", "/set_servo3?value=" + value, true);
            xhr.send();
        }
    </script>
</body>
</html>
"""

while True:
    conn, addr = s.accept()
    print('Got a connection from %s' % str(addr))
    
    # Recibir datos del cliente
    buffer = bytearray(1024)  # Crear un buffer mutable
    bytes_received, address = conn.recvfrom_into(buffer)  # Recibir datos en el buffer
    request = buffer[:bytes_received].decode('utf-8')
    print("Received request:", request)

    # Analizar la solicitud del cliente
    if "GET / " in request:
        # Si la solicitud es para la página principal
        response = "HTTP/1.1 200 OK\nContent-Type: text/html\n\n" + html
        conn.send(response.encode('utf-8'))
    
    elif "GET /set_servo1?value=" in request:
        # Si la solicitud es para ajustar el ángulo del primer servo
        angle = int(request.split("value=")[-1].split(" ")[0])
        print(f"Ángulo recibido Servo 1: {angle} grados")
        
        # Ajustar el primer servomotor basado en el ángulo recibido
        duty_cycle = map_angle_to_duty(angle)
        servo1.duty_cycle = duty_cycle
        print(f"Duty cycle ajustado Servo 1: {duty_cycle}")
        
        response = "HTTP/1.1 200 OK\nContent-Type: text/plain\n\nÁngulo recibido Servo 1"
        conn.send(response.encode('utf-8'))

    elif "GET /set_servo2?value=" in request:
        # Si la solicitud es para ajustar el ángulo del segundo servo (base)
        angle = int(request.split("value=")[-1].split(" ")[0])
        print(f"Ángulo recibido Servo 2 (Base): {angle} grados")
        
        # Ajustar el segundo servomotor (base) basado en el ángulo recibido
        duty_cycle = map_angle_to_duty(angle)
        servo2.duty_cycle = duty_cycle
        print(f"Duty cycle ajustado Servo 2 (Base): {duty_cycle}")
        
        response = "HTTP/1.1 200 OK\nContent-Type: text/plain\n\nÁngulo recibido Servo 2 (Base)"
        conn.send(response.encode('utf-8'))

    elif "GET /set_servo3?value=" in request:
        # Si la solicitud es para ajustar el ángulo del tercer servo
        angle = int(request.split("value=")[-1].split(" ")[0])
        print(f"Ángulo recibido Servo 3: {angle} grados")
        
        # Ajustar el tercer servomotor basado en el ángulo recibido
        duty_cycle = map_angle_to_duty(angle)
        servo3.duty_cycle = duty_cycle
        print(f"Duty cycle ajustado Servo 3: {duty_cycle}")
        
        response = "HTTP/1.1 200 OK\nContent-Type: text/plain\n\nÁngulo recibido Servo 3"
        conn.send(response.encode('utf-8'))

    conn.close()


