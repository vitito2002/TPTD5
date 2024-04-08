def calcular_error(inicio, fin, punto):
    #funcion lineal y=mx+b
    pendiente = (fin[1] - inicio[1]) / (fin[0] - inicio[0])
    ordenada = inicio[1] - pendiente * inicio[0]

    # Calculate the y-coordinate corresponding to the x-coordinate of point c on the line
    distancia_a_punto = pendiente * punto["x"][0] + ordenada

    # Calculate the error in terms of y-coordinate
    error = abs(punto["y"][0] - distancia_a_punto)

    return error