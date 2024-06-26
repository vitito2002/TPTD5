
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


def FB(N, M, K, res=None): # VER COMO METER EL JSON ACA
    if res is None:
        res = []  # Si res no se proporciona, inicializa una nueva lista vacía

    # Caso base:
    if N > 6 or M > 6 or M < 0 or (K > 0 and N == 6) or (K == 0 and N < 6):
        return []  # Devuelve una lista vacía si no se cumple alguna de estas condiciones
    elif K == 0 and N == 6:
        return res  # Devuelve el resultado final si K es 0 y N es 6

    # Caso inductivo:
    for i in range(1, N + 1): # REVISAR N+1
        for j in range(-M, M + 1): # REVISAR M+1
            # Llama recursivamente a la función FB con las coordenadas actuales y K-1, pasando res como parámetro
            # La función FB modificará la lista res en cada llamada, acumulando los nodos del camino
            return min(calcular_error(FB(i, j, K - 1, res[:] + [(i, j)])))  # Se pasa una copia de la lista res # CHEQUEAR COMO FUNCIONA ESTO DE [:]

def BT(N, M, K, res=None): # VER COMO METER EL JSON ACA
    if res is None:
        res = []  # Si res no se proporciona, inicializa una nueva lista vacía

    # Caso base:
    if N > 6 or M > 6 or M < 0 or (K > 0 and N == 6) or (K == 0 and N < 6): #PODAS FB
        return []  # Devuelve una lista vacía si no se cumple alguna de estas condiciones
    elif K == N+1:
        return # tramo solo se puede mover de a 1
    elif K == 0 and N == 6:
        return res  # Devuelve el resultado final si K es 0 y N es 6

    # Caso inductivo:
    for i in range(1, N + 1): # REVISAR N+1
        for j in range(-M, M + 1): # REVISAR M+1
            # Llama recursivamente a la función FB con las coordenadas actuales y K-1, pasando res como parámetro
            # La función FB modificará la lista res en cada llamada, acumulando los nodos del camino
            return min(calcular_error(FB(i, j, K - 1, res[:] + [(i, j)])))  # Se pasa una copia de la lista res # CHEQUEAR COMO FUNCIONA ESTO DE [:]
        

"""
FACTIBILIDAD

- si k=n+1, y en una grilla no hay ningun punto directamente pasar al siguiente
if k=n+1 {tramo de res solo se puede mover n=1}
!!¡¡ dentro de esta poda tenemos que ver lo de que si no hay ningun punto del json en esa grilla en especifica, ni en la siguiente, el tramo actual puede ir a cualquier lado
- si k > n+1, no se puede, retornar error
- si quedan k breakpoints y n grillas, el tramo actual no puede ser mas grande que X grillas
if k<N/K {tramo de res solo se puede mover n=[1,2,3]} VER COMO FORMULAR Y LOS X DE N

OPTIMALIDAD
- si error actual es mayor a error minimo, dejar de iterar
"""