def onda_cuadrada(amplitud, frecuencia):
    # Defino la pendiente de la ecuación lineal que relaciona la frecuencia con los píxeles horizontales
    m_frecuencia = 51.2
    b_frecuencia = -51.2
    c_pixeles = m_frecuencia * frecuencia + b_frecuencia

    # Defino la ecuación que relaciona la amplitud con los píxeles verticales
    m_amplitud = 1.28
    y_amplitud = m_amplitud * amplitud

    # Defino la posición del punto x usando la ecuación de la recta
    x = 12
    posicion = x % c_pixeles

    # Determino si el punto X está en el lado positivo o negativo de la onda
    if posicion < c_pixeles / 2:
        y = y_amplitud
    else:
        y = -y_amplitud

    print("La amplitud es:")
    print(y_amplitud)
    return y

# Asignar valores
amplitud = 10
frecuencia = 128

# Llamar a la función y obtener los resultados
y = onda_cuadrada(amplitud, frecuencia)

print("El punto en Y que le corresponde a la coordenada en x ingresada es:")
print(y)