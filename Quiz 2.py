import math

def cos_taylor(x, N):
    """
    Calcula la aproximación de cos(x) usando la serie de Taylor hasta N términos.
    
    Parámetros:
    - x: el valor de x en radianes.
    - N: número de términos a sumar en la serie.
    
    Retorna:
    - La aproximación de cos(x) usando la serie de Taylor.
    """
    cos_approx = 0
    for n in range(N):
        # Término de la serie: (-1)^n * x^(2n) / (2n)!
        term = ((-1)**n * x**(2*n)) / math.factorial(2*n)
        cos_approx += term
    
    return cos_approx

# Ejemplo de uso
x = math.radians(60)  # Convertir 60 grados a radianes
N = 10  # Número de términos de la serie de Taylor

cos_aprox = cos_taylor(x, N)
cos_real = math.cos(x)

print(f"Serie de Taylor de cos(x) para x=60 grados (N={N} términos): {cos_aprox}")
print(f"Valor real de cos(x): {cos_real}")
print(f"Diferencia: {abs(cos_real - cos_aprox)}")
