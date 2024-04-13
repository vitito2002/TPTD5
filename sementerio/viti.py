def calcular_error(inicio, fin, punto):
    #funcion lineal y=mx+b
    if punto["x"][0] < inicio[0] or punto["x"][0] > fin[0]:
        raise ValueError("La coordenada x del punto está fuera del dominio de la línea")
    
    pendiente = (fin[1] - inicio[1]) / (fin[0] - inicio[0])
    ordenada = inicio[1] - pendiente * inicio[0]

    # Calculate the y-coordinate corresponding to the x-coordinate of point c on the line
    distancia_a_punto = pendiente * punto["x"][0] + ordenada

    # Calculate the error in terms of y-coordinate
    error = abs(punto["y"][0] - distancia_a_punto)

    return error

def FB(N, M, K, puntos, res=None):
    # Función recursiva de fuerza bruta para buscar la solución óptima
    if res is None:
        res = []  # Inicializa una nueva lista vacía si res no se proporciona

    # Caso base:
    if N > len(puntos["x"]) or M > len(puntos["y"]) or M < 0 or (K > 0 and N == len(puntos["x"])) or (K == 0 and N < len(puntos["x"])):
        return []  # Devuelve una lista vacía si no se cumple alguna de estas condiciones
    elif K == 0 and N == len(puntos["x"]):
        return res  # Devuelve el resultado final si K es 0 y N es igual al número de puntos

    # Caso inductivo:
    mejor_error = float('inf')  # Inicializa el mejor error con un valor infinito
    mejor_solucion = None

    for i in range(1, N + 1):
        for j in range(-M, M + 1):
            nueva_solucion = res[:] + [(i, j)]
            error_total = sum(calcular_error(puntos["x"][nueva_solucion[k][0]], puntos["x"][nueva_solucion[k+1][0]], puntos) for k in range(len(nueva_solucion) - 1))
            
            if error_total < mejor_error:
                mejor_error = error_total
                mejor_solucion = nueva_solucion

    # Llama recursivamente a la función con las nuevas coordenadas y K-1
    return FB(N, M, K - 1, puntos, mejor_solucion)


BIG_NUMBER = 1e10 # Revisar si es necesario.
