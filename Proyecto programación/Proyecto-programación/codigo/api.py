from ov7670 import OV7670_30x40_RGB565 as CAM
import digitalio
import busio
import board
import time

# Configuración de la cámara
cam1 = CAM(
    d0_d7pinslist=[
        board.GP0, board.GP1, board.GP2, board.GP3,
        board.GP4, board.GP5, board.GP6, board.GP7,
    ],
    plk=board.GP8,
    xlk=board.GP9,
    sda=board.GP20,
    scl=board.GP21,
    hs=board.GP12,
    vs=board.GP13,
    ret=board.GP14,
    pwdn=board.GP15
)

def print_image_sample(image):
    print("Muestra de los primeros 10 píxeles de la imagen:", image[:10])

def detect_capacitor(image):
    width, height = 30, 40  # Tamaño de la imagen de la cámara
    total_intensity = 0
    sum_x = 0
    sum_y = 0
    pixel_count = 0
    background_pixels = []
    object_pixels = []
    block_size = 2  # Aumentar el tamaño del bloque para reducir la cantidad de píxeles procesados

    # Procesamiento de píxeles para estimar el fondo y los objetos
    for y in range(0, height, block_size):
        for x in range(0, width, block_size):
            pixel_values = []
            for dy in range(block_size):
                for dx in range(block_size):
                    if y + dy < height and x + dx < width:
                        pixel = image[(y + dy) * width + (x + dx)]
                        r = (pixel >> 11) & 0x1F
                        g = (pixel >> 5) & 0x3F
                        b = pixel & 0x1F
                        intensity = (r * 0.299 + g * 0.587 + b * 0.114) * 255 / 31
                        pixel_values.append(intensity)
            
            avg_intensity = sum(pixel_values) / len(pixel_values)
            background_pixels.append(avg_intensity)
    
    # Calcular umbral de fondo y objeto
    background_threshold = sum(sorted(background_pixels)[-50:]) / 50 - 5  # Ajustar umbral
    object_threshold = background_threshold - 5  # Reducir la diferencia de intensidad

    print(f"Umbral de fondo estimado: {background_threshold:.2f}, Umbral de objeto: {object_threshold:.2f}")

    # Verificar los píxeles de objeto detectados
    for y in range(0, height, block_size):
        for x in range(0, width, block_size):
            pixel_values = []
            for dy in range(block_size):
                for dx in range(block_size):
                    if y + dy < height and x + dx < width:
                        pixel = image[(y + dy) * width + (x + dx)]
                        r = (pixel >> 11) & 0x1F
                        g = (pixel >> 5) & 0x3F
                        b = pixel & 0x1F
                        intensity = (r * 0.299 + g * 0.587 + b * 0.114) * 255 / 31
                        pixel_values.append(intensity)
            
            avg_intensity = sum(pixel_values) / len(pixel_values)
            
            if avg_intensity > background_threshold:
                continue  # Ignorar píxeles del fondo

            # Si la intensidad promedio de un bloque es menor que el umbral de objeto, es posible que haya un objeto
            if avg_intensity < object_threshold:
                total_intensity += (255 - avg_intensity)
                sum_x += x * (255 - avg_intensity)
                sum_y += y * (255 - avg_intensity)
                pixel_count += 1
                object_pixels.append((x, y))

    if total_intensity == 0 or pixel_count < 10:
        print("No se detectó un objeto.")
        return None, None

    object_x = sum_x // total_intensity
    object_y = sum_y // total_intensity

    print(f"Objeto detectado en ({object_x}, {object_y}) con {pixel_count} bloques de píxeles")
    return object_x, object_y

def api():
    image = cam1()  # Capturar imagen
    print_image_sample(image)  # Depuración
    return detect_capacitor(image)
