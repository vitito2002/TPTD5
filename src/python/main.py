import json
import numpy as np
import os  
"""
# from algoritmos import FB, calcular_error 
# Importa las funciones de fuerzabruta.py
"""
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

def main():
	# Ejemplo para leer una instancia con json
	instance_name = "titanium.json"
	filename = "data/" + instance_name
	 # Verificar si el archivo existe
	if not os.path.exists(filename):
		print(f"Error: No se encontró el archivo {filename}")
		return
	 # Verificar si el archivo existe
	
	with open(filename) as f:
		instance = json.load(f)
	
	K = 5 #gato encerrado cantidad de breakpoints
	m = 6
	n = 6
	Nodo = instance["n"]
	puntos = instance # diccionario
	# Ejemplo para definir una grilla de m x n.
	grid_x = np.linspace(min(instance["x"]), max(instance["x"]), num=m, endpoint=True)
	grid_y = np.linspace(min(instance["y"]), max(instance["y"]), num=n, endpoint=True)


	# TODO: aca se deberia ejecutar el algoritmo.
	result = FB(n, m, K, puntos, res=None)


	best = {}
	best['sol'] = [None]*(Nodo+1)
	best['obj'] = BIG_NUMBER
	
	# Posible ejemplo (para la instancia titanium) de formato de solucion, y como exportarlo a JSON.
	# La solucion es una lista de tuplas (i,j), donde:
	# - i indica el indice del punto de la discretizacion de la abscisa
	# - j indica el indice del punto de la discretizacion de la ordenada.
	best['sol'] = [(0, 0), (1, 0), (2, 0), (3, 2), (4, 0), (5, 0)]
	best['obj'] = 5.927733333333335

	# Represetnamos la solucion con un diccionario que indica:
	# - n: cantidad de breakpoints
	# - x: lista con las coordenadas de la abscisa para cada breakpoint
	# - y: lista con las coordenadas de la ordenada para cada breakpoint
	solution = {}
	solution['n'] = len(best['sol'])
	solution['x'] = [grid_x[x[0]] for x in best['sol']]
	solution['y'] = [grid_y[x[1]] for x in best['sol']]
	solution['obj'] = best['obj']

	# Se guarda el archivo en formato JSON
	with open('solution_' + instance_name, 'w') as f:
		json.dump(solution, f)
	print("Resultado de la función FB:", result)

if __name__ == "__main__":
	main()