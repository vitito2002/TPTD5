import json
import numpy as np
import time

"""

M: numero total de filas en la grilla
N: numero total de columnas en la grilla

instance: instancia actual del problema
j: indice de la fila actual de la grilla
i: indice de la columna actual de la grilla

lista_k: lista de breakpoints acumulados
error_total: error total acumulado
caminos : diccionario con combinaciones de breakpoints y error correspondiente


VALORES PARAMETROS:
_grid_x: valores de coordenadas X de la grilla
_grid_y: valores de coordenadas Y de la grilla
_x, _y: arrays de puntos de json
_k: cant de breakpoints
_lista_breakpoints: almacenar solucion parcial

VALORES DE LA FUNCION:

"""
def main ():

    instance_name = "titanium.json"
    filename = "././data/" + instance_name
    with open(filename) as f:
        instance = json.load(f)

    K = instance["n"]
    m = 6
    n = 6
    N = 5 # Tome N como numero de Breakpoints
	
	# Ejemplo para definir una grilla de m x n.
    _grid_x = np.linspace(min(instance["x"]), max(instance["x"]), num=m, endpoint=True)
    _grid_y = np.linspace(min(instance["y"]), max(instance["y"]), num=n, endpoint=True)
    _x = instance['x']
    _y = instance['y']

    sol= []

    def calcular_error (_lista_breakpoints, x, y): # error entre _lista_breakpoints (conjunto de breakpoints (coordenadas) y datos del JSON (x,y))
        # recorre lista breakpoints
        i = 0 
        # acumula error
        error = 0 

        # recorre breakpoints en lista 
        while i < len(_lista_breakpoints) - 1:

            # primero tengo que ver, para cada tramo de la funcion, cuales puntos del JSON estan en ese dominio (osea estan entre esos 2 breakpoints)

            # subconjunto de coordenadas X entre ambos breakpoints
            sub_x = []
            for punto in x:
                if _lista_breakpoints[i][0] <= punto <= _lista_breakpoints[i+1][0]:
                    sub_x.append(punto)
            
            menor_y = x.index(sub_x[0]) # primer 'y' del subconjunto
            mayor_y = x.index(sub_x[-1])+1 # ultimo 'y' del subconjunto
            sub_y = y[menor_y:mayor_y]
            sub_x = np.array(sub_x)

            # Calcula la estimación para cada punto utilizando la fórmula de la recta.
            prediccion = (((_lista_breakpoints[i + 1][1] - _lista_breakpoints[i][1]) / (_lista_breakpoints[i + 1][0] - _lista_breakpoints[i][0])) * (sub_x - _lista_breakpoints[i][0])) + _lista_breakpoints[i][1]

            # Calcula el error entre `prediccion` y `sub_y`.
            diferencia = np.abs(prediccion - sub_y)
            error_total = np.sum(diferencia)

            error += error_total

            i += 1

        return error


    def FB(_grid_x, _grid_y, _x, _y, _k, _lista_breakpoints):

        if (len(_grid_x) < _k - (len(_lista_breakpoints))):
            return {'error':1e10}

         # CASO BASE: # alcance los breakpoints pedidos
        elif len(_lista_breakpoints) == _k:
            # DEVUELVO combinacion de breakpoints con error correspondiente #¿QUIZAS ARMAR UN DICC COMO VARIABLE PRIMERO?
            return {'error':calcular_error(_lista_breakpoints, _x, _y), 'puntos':_lista_breakpoints.copy()}
        
        else:
            # armo una solucion con error altisimo para despues ir reemplazando
            mejores_breakpoints = {'error':9999999999999999999999}
            
            if (_k - (len(_lista_breakpoints)) == 1):
                _grid_x = [_grid_x[-1]]
                
            # itero sobre filas
            for i in _grid_y:
                # sumo breakpoint
                _lista_breakpoints.append((_grid_x[0],i))
                # recorto valores de gridX y hago recursion
                recursion = FB(_grid_x[1:],_grid_y,_x,_y,_k,_lista_breakpoints)

                # si error de la parcial es menor la reemplazo
                if recursion['error'] < mejores_breakpoints['error']:
                    mejores_breakpoints = recursion

                # saco el ultimo elemento asi pruebo con otras opciones
                _lista_breakpoints.pop()

            if len(_lista_breakpoints)>0 :
                # recorto valores de gridX y hago recursion
                recursion = FB(_grid_x[1:],_grid_y,_x,_y,_k,_lista_breakpoints)

                # si error de la parcial es menor la reemplazo
                if recursion['error'] < mejores_breakpoints['error']:
                    mejores_breakpoints = recursion

            return mejores_breakpoints
        
    inicio_fuerzabruta = time.time()
    print('Brute Force ',FB(_grid_x,_grid_y,_x,_y,5,sol))
    fin_fuerzabruta = time.time()
    tiempo_fuerzabruta = fin_fuerzabruta - inicio_fuerzabruta
    print(tiempo_fuerzabruta)

    best = {}
    best['sol'] = [None]*(N+1)
    best['obj'] = 1e10

    solution = {}
    solution['n'] = len(best['sol'])
    solution['x'] = [_grid_x[x[0]] for x in best['sol']]
    solution['y'] = [_grid_y[x[1]] for x in best['sol']]
    solution['obj'] = best['obj']

    with open('solution_' + instance_name, 'w') as f:
        json.dump(solution, f)

	
if __name__ == "__main__":
	main()