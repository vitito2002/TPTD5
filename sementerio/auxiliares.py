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

inicio = (1, 1)
fin = (3, 4)
punto = { "x": [2.0], "y": [1.0] }

error = calcular_error(inicio, fin, punto)
print("Error:", error)
