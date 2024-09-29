def lineas_brazo(a1, a2, a3, theta2, theta3, z0):
    # Coordenadas del punto (x0, y0, z0)
    x0, y0, z0 = 0, 0, z0

    # Coordenadas del punto (x1, y1, z1)
    x1, y1, z1 = 0, a1, 0

    # Calcular (x2, y2, z2) para la línea a2
    x2 = x1 + a2 * (theta2 + 180)  
    y2 = y1 + a2 * (theta2 + 180)
    z2 = z1  

    # Calcular (x3, y3, z3) para la línea a3
    x3 = x2 + a3 * (theta2 + theta3) 
    y3 = y2 + a3 * (theta2 + theta3)
    z3 = z2 

    return (x2, y2, z2), (x3, y3, z3)