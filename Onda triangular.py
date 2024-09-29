import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

def generar_onda_triangular(x_pixels, y_pixels, frecuencia, amplitud):
    # Parámetros de la señal
    tiempo_total = 1 / frecuencia  # Tiempo para un ciclo completo
    tiempo = np.linspace(0, tiempo_total, x_pixels)  # Espaciado de tiempo basado en los píxeles x
    
    # Generar onda triangular normalizada (de -1 a 1)
    onda_triangular = signal.sawtooth(2 * np.pi * frecuencia * tiempo, width=0.5)
    
    # Ajustar la amplitud (voltaje pico a pico)
    onda_triangular = (onda_triangular * (amplitud / 2))  # Ajustar para que sea de 0 a amplitud
    
    # Escalar los valores de la onda al rango de los píxeles en y
    y_valores = (onda_triangular - np.min(onda_triangular)) * (y_pixels / np.ptp(onda_triangular))
    
    # Graficar la onda triangular
    plt.figure(figsize=(10, 5))
    plt.plot(tiempo, y_valores)
    plt.title(f'Onda Triangular - Frecuencia: {frecuencia} Hz, Amplitud: {amplitud} Vp-p')
    plt.xlabel('Tiempo (s)')
    plt.ylabel('Pixeles (escala en y)')
    plt.grid(True)
    plt.show()

# Ejemplo de uso con 500 píxeles en el eje x, 300 en el eje y, frecuencia de 5 Hz y amplitud de 10 Vp-p
generar_onda_triangular(500, 300, 5, 10)
