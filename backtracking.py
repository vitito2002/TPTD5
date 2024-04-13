
def calcular_error():
	return 1

def estimar_error_y ():
	return 2


def BT(grid_x, grid_y, x, y, _k, sol):

    if (len(grid_x) < _k - (len(sol))):
        return {'error':1e10}

        # CASO BASE: # alcance los breakpoints pedidos
    elif len(sol) == _k:
        # DEVUELVO combinacion de breakpoints con error correspondiente #¿QUIZAS ARMAR UN DICC COMO VARIABLE PRIMERO?
        return {'error':calcular_error(sol, x, y), 'puntos':sol.copy()}
    
    else:
        # armo una solucion con error altisimo para despues ir reemplazando
        mejores_breakpoints = {'error':9999999999999999999999}
        
        if (_k - (len(sol)) == 1):
            grid_x = [grid_x[-1]]   

        # itero sobre filas
        for i in grid_y:
            # sumo breakpoint
            sol.append((grid_x[0],i))
			
            if (calcular_error(sol, x, y) < mejores_breakpoints['error']):
                recursion = BT(grid_x[1:],grid_y, x, y, _k, sol)			
                if recursion['error'] < mejores_breakpoints['error']:
                    mejores_breakpoints = recursion

            sol.pop()

        if len(sol)>0 :
            # recorto valores de gridX y hago recursion
            recursion = BT(grid_x[1:],grid_y,x,y,_k,sol)

            # si error de la parcial es menor la reemplazo
        if recursion['error'] < mejores_breakpoints['error']:
            mejores_breakpoints = recursion

        return mejores_breakpoints
	