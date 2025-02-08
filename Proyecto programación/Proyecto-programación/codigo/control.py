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
servo1 = pwmio.PWMOut(board.GP16, frequency=50)
servo2 = pwmio.PWMOut(board.GP17, frequency=50)  
servo3 = pwmio.PWMOut(board.GP18, frequency=50)  
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
# Página HTML con tres sliders
html = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Control Remoto</title>
    <style>
        body {
            font-family: 'Orbitron', sans-serif;
            background: radial-gradient(circle, #1a1a1a, #000);
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            overflow: hidden;
            color: #00ffcc;
            text-transform: uppercase;
        }

        h1 {
            font-size: 2.5rem;
            letter-spacing: 5px;
            margin-bottom: 20px;
            text-shadow: 0 0 10px #00ffcc, 0 0 20px #00ffcc;
            animation: glow 1.5s infinite alternate;
        }

        @keyframes glow {
            0% {
                text-shadow: 0 0 10px #00ffcc, 0 0 20px #00ffcc;
            }
            100% {
                text-shadow: 0 0 20px #00ffcc, 0 0 40px #00ffcc;
            }
        }

        .control-panel {
            background: rgba(0, 0, 0, 0.8);
            padding: 30px;
            border-radius: 20px;
            border: 2px solid #00ffcc;
            box-shadow: 0 0 20px rgba(0, 255, 204, 0.5);
            text-align: center;
            width: 400px;
            position: relative;
        }

        .control-group {
            margin-bottom: 25px;
        }

        .control-group label {
            display: block;
            font-size: 1.2rem;
            margin-bottom: 10px;
            color: #00ffcc;
            text-shadow: 0 0 5px #00ffcc;
        }

        .control-group input[type="range"] {
            -webkit-appearance: none;
            width: 100%;
            height: 15px;
            background: rgba(0, 255, 204, 0.2);
            border-radius: 10px;
            outline: none;
            opacity: 0.9;
            transition: opacity 0.2s;
        }

        .control-group input[type="range"]:hover {
            opacity: 1;
        }

        .control-group input[type="range"]::-webkit-slider-thumb {
            -webkit-appearance: none;
            appearance: none;
            width: 25px;
            height: 25px;
            background: #00ffcc;
            border-radius: 50%;
            cursor: pointer;
            box-shadow: 0 0 15px #00ffcc;
        }

        .control-group input[type="range"]::-moz-range-thumb {
            width: 25px;
            height: 25px;
            background: #00ffcc;
            border-radius: 50%;
            cursor: pointer;
            box-shadow: 0 0 15px #00ffcc;
        }

        .angle-display {
            font-size: 1.5rem;
            font-weight: bold;
            color: #00ffcc;
            text-shadow: 0 0 10px #00ffcc;
        }

        .control-panel p {
            margin: 10px 0;
            color: #00ffcc;
        }

        /* Efecto de escaneo */
        .scan-line {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 2px;
            background: linear-gradient(to right, transparent, #00ffcc, transparent);
            animation: scan 3s linear infinite;
        }

        @keyframes scan {
            0% {
                top: 0;
            }
            100% {
                top: 100%;
            }
        }

        /* Botón de emergencia */
        .emergency-button {
            margin-top: 20px;
            padding: 10px 20px;
            font-size: 1.2rem;
            color: #ff0000;
            background: rgba(255, 0, 0, 0.1);
            border: 2px solid #ff0000;
            border-radius: 10px;
            cursor: pointer;
            text-shadow: 0 0 10px #ff0000;
            box-shadow: 0 0 10px rgba(255, 0, 0, 0.5);
            transition: background 0.3s, transform 0.3s;
        }

        .emergency-button:hover {
            background: rgba(255, 0, 0, 0.3);
            transform: scale(1.1);
        }

        /* Efecto de sonido (opcional) */
        audio {
            display: none;
        }
    </style>
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap" rel="stylesheet">
</head>
<body>
    <div class="control-panel">
        <div class="scan-line"></div>
        <h1>Control Remoto</h1>
        
        <!-- Slider para el primer servomotor (90 a 180) -->
        <div class="control-group">
            <label for="slider1">Servo 1</label>
            <input type="range" id="slider1" min="90" max="180" value="135" oninput="updateServo1(this.value)">
            <p>Ángulo: <span class="angle-display" id="angleValue1">135</span>°</p>
        </div>

        <!-- Slider para el segundo servomotor (0 a 180) -->
        <div class="control-group">
            <label for="slider2">Servo 2</label>
            <input type="range" id="slider2" min="0" max="180" value="90" oninput="updateServo2(this.value)">
            <p>Ángulo: <span class="angle-display" id="angleValue2">90</span>°</p>
        </div>

        <!-- Slider para el tercer servomotor (0 a 180) -->
        <div class="control-group">
            <label for="slider3">Servo 3</label>
            <input type="range" id="slider3" min="0" max="180" value="90" oninput="updateServo3(this.value)">
            <p>Ángulo: <span class="angle-display" id="angleValue3">90</span>°</p>
        </div>

        <!-- Botón de emergencia -->
        <button class="emergency-button" onclick="emergencyStop()">¡Emergencia!</button>
    </div>

    <!-- Efecto de sonido (opcional) -->
    <audio id="clickSound" src="https://www.soundjay.com/button/beep-07.mp3"></audio>

    <script>
        // Función para enviar el ángulo del primer servo
        function updateServo1(value) {
            document.getElementById("angleValue1").innerText = value;
            var xhr = new XMLHttpRequest();
            xhr.open("GET", "/set_servo1?value=" + value, true);
            xhr.send();
            playClickSound();
        }

        // Función para enviar el ángulo del segundo servo
        function updateServo2(value) {
            document.getElementById("angleValue2").innerText = value;
            var xhr = new XMLHttpRequest();
            xhr.open("GET", "/set_servo2?value=" + value, true);
            xhr.send();
            playClickSound();
        }

        // Función para enviar el ángulo del tercer servo
        function updateServo3(value) {
            document.getElementById("angleValue3").innerText = value;
            var xhr = new XMLHttpRequest();
            xhr.open("GET", "/set_servo3?value=" + value, true);
            xhr.send();
            playClickSound();
        }

        // Función para el botón de emergencia
        function emergencyStop() {
            alert("¡Modo de emergencia activado! Todos los servos se detendrán.");
            // Aquí puedes agregar la lógica para detener los servos
            playClickSound();
        }

        // Función para reproducir sonido (opcional)
        function playClickSound() {
            var audio = document.getElementById("clickSound");
            audio.currentTime = 0;
            audio.play();
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


