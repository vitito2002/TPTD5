import json
import numpy as np
import time
import matplotlib.pyplot as plt

BIG_NUMBER = 1e10 # Revisar si es necesario.

def main():

	jsons = ['aspen_simulation.json', 'ethanol_water_vle.json', 'optimistic_instance.json', 'titanium.json', 'toy_instance.json']
	# Ejemplo para leer una instancia con json
	instance_name = "optimistic_instance.json"
	filename = "data/" + instance_name
	with open(filename) as f:
		instance = json.load(f)
	
	K = instance["n"]
	m = 6
	n = 6
	N = 5
	
	# Ejemplo para definir una grilla de m x n
 
	# np.linspace genera:
 		# M puntos equiespaciados en grid_x desde el valor minimo hasta el maximo de instance["x"]
		# N puntos equiespaciados en grid_y desde el ...

	grid_x = np.linspace(min(instance["x"]), max(instance["x"]), num=m, endpoint=True)
	grid_y = np.linspace(min(instance["y"]), max(instance["y"]), num=n, endpoint=True)
	x = instance['x']
	y = instance['y']

	sol= [] 

#/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


	def calcular_error(sol, x, y):

		error_funcion = 0
		
		# para iterar los breakpoints
		for i, (primer, ultimo) in enumerate(zip(sol[:-1], sol[1:])):

			# me fijo si cada punto del json esta en el dominio entre breakpoints
			x_en_rango = [punto for punto in x if primer[0] <= punto <= ultimo[0]]
			
			# guardo el y de cada uno de los puntos de x_en_rango para despues poder calcular el error 
			primer_y, ultimo_y = [x.index(x_en_rango[0]), x.index(x_en_rango[-1]) + 1]
			y_en_rango = y[primer_y:ultimo_y]

			# armo tramo entre los dos breakpoints para despues distancia a punto
			pendiente = (ultimo[1] - primer[1]) / (ultimo[0] - primer[0])
			ordenada_al_origen = primer[1] - pendiente * primer[0]

			# defino funcion y calculo el error para cada punto
			diferencia = [
				abs(pendiente * punto + ordenada_al_origen - y_en_rango[j]) 
				for j, punto in enumerate(x_en_rango)
			]

			# sumo todos los errores :)
			error_funcion += np.sum(diferencia)
		
		return error_funcion


#/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

	# FUNCION FUERZA BRUTA
	def FB(grid_x, grid_y, x, y, _k, sol):

		if (len(grid_x) < _k - (len(sol))):
			return {'error':1e10}

         # CASO BASE: # alcance los breakpoints pedidos
		elif len(sol) == _k: # y que no haya llegado al final
            # DEVUELVO combinacion de breakpoints con error correspondiente #¿QUIZAS ARMAR UN DICC COMO VARIABLE PRIMERO?
			if grid_x.size == 0 : # ultima breakpoint en grilla
				return {'error':calcular_error(sol, x, y), 'puntos':sol.copy()}
			else:
				return {'error':1e10}
        
		else:
            # armo una solucion con error altisimo para despues ir reemplazando
			mejores_breakpoints = {'error':1e10}

			# itero sobre filas
			for i in grid_y:
                # sumo breakpoint
				sol.append((grid_x[0],i))
                # recorto valores de gridX y hago recursion
				recursion = FB(grid_x[1:],grid_y,x,y,_k,sol)

                # si error de la parcial es menor la reemplazo
				if recursion['error'] < mejores_breakpoints['error']:
					mejores_breakpoints = recursion

                # saco el ultimo elemento asi pruebo con otras opciones
				sol.pop()

			if len(sol)>0 :
                # recorto valores de gridX y hago recursion
				recursion = FB(grid_x[1:],grid_y,x,y,_k,sol)

                # si error de la parcial es menor la reemplazo
			if recursion['error'] < mejores_breakpoints['error']:
				mejores_breakpoints = recursion

			return mejores_breakpoints

	
#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

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

#/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
	
	print('JSON: ',instance_name," con ",m,"filas ",n, "columnas y ",N,"breakpoints:")

	comienzo_timer_FB = time.time()
	FuerzaBruta = FB(grid_x, grid_y, x, y, N, sol)
	fin_timer_FB = time.time()

	timer_FB = fin_timer_FB - comienzo_timer_FB
	print('Fuerza Bruta: ', FuerzaBruta,'\n''Tiempo de ejecucion FB: ',timer_FB)

#/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
	comienzo_timer_BT = time.time()
	BackTracking = BT(grid_x,grid_y,x,y,N,sol)
	fin_timer_BT = time.time()

	timer_BT = fin_timer_BT - comienzo_timer_BT

	print('Backtracking: ', BackTracking,'\n''Tiempo de ejecucion BT   : ',timer_BT)

#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


# Seccion PROGRE DINAMICA

	def calcular_error_MEMO(sol, x, y, memo):

		# key va a ser dos breakpoints {(x1,y1),(x2,y2)}
		clave = tuple(sol)

		if clave in memo:
			return memo[clave],memo
		
		else:

			error_funcion = 0
			
			# para iterar los breakpoints
			for i, (primer, ultimo) in enumerate(zip(sol[:-1], sol[1:])):

				# me fijo si cada punto del json esta en el dominio entre breakpoints
				x_en_rango = [punto for punto in x if primer[0] <= punto <= ultimo[0]]
				
				# guardo el y de cada uno de los puntos de x_en_rango para despues poder calcular el error 
				primer_y, ultimo_y = [x.index(x_en_rango[0]), x.index(x_en_rango[-1]) + 1]
				y_en_rango = y[primer_y:ultimo_y]

				# armo tramo entre los dos breakpoints para despues distancia a punto
				pendiente = (ultimo[1] - primer[1]) / (ultimo[0] - primer[0])
				ordenada_al_origen = primer[1] - pendiente * primer[0]

				# defino funcion y calculo el error para cada punto
				diferencia = [
					abs(pendiente * punto + ordenada_al_origen - y_en_rango[j]) 
					for j, punto in enumerate(x_en_rango)
				]

				# sumo todos los errores :)
				error_funcion += np.sum(diferencia)

				memo[clave] = error_funcion
			
			return error_funcion, memo
		

	def PD(grid_x, grid_y, x, y, _k, sol, memo):

		if (len(grid_x) < _k - (len(sol))):
			return {'error':1e10}, memo

			# CASO BASE: # alcance los breakpoints pedidos
		elif len(sol) == _k:

			# DEVUELVO combinacion de breakpoints con error correspondiente #¿QUIZAS ARMAR UN DICC COMO VARIABLE PRIMERO?
			return {'error': calcular_error_MEMO(sol, x, y, memo)[0], 'puntos': sol.copy()}, calcular_error_MEMO(sol, x, y, memo)[1]
		
		else:
			# armo una solucion con error altisimo para despues ir reemplazando
			mejores_breakpoints = {'error':9999999999999999999999}
			
			if (_k - (len(sol)) == 1):
				grid_x = [grid_x[-1]]   

			# itero sobre filas
			for i in grid_y:
				# sumo breakpoint
				sol.append((grid_x[0],i))
				
				if (calcular_error_MEMO(sol, x, y, memo)[0] < mejores_breakpoints['error']):
					recursion, memo = PD(grid_x[1:],grid_y, x, y, _k, sol, memo)			
					if recursion['error'] < mejores_breakpoints['error']:
						mejores_breakpoints = recursion

				sol.pop()

			if len(sol)>0 :
				# recorto valores de gridX y hago recursion
				recursion, memo =PD(grid_x[1:],grid_y,x,y,_k,sol, memo)

				# si error de la parcial es menor la reemplazo
			if recursion['error'] < mejores_breakpoints['error']:
				mejores_breakpoints = recursion

			return mejores_breakpoints, memo

	pitulon = {}

	#/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
	
	comienzo_timer_PD = time.time()
	ProgramacionDinamica = (PD(grid_x,grid_y,x,y,N,sol,pitulon)[0])
	fin_timer_PD = time.time()

	timer_PD = fin_timer_PD - comienzo_timer_PD

	print('Programacion Dinamica: ', ProgramacionDinamica,'\n''Tiempo de ejecucion PD   : ',timer_PD)

#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


	# T = 7

	# times_FB = []
	# times_BT = []
	# times_PD = []

	# for t in range(T):
	# 	comienzo_timer_FB = time.time()
	# 	FuerzaBruta = FB(grid_x, grid_y, x, y, N, sol)
	# 	fin_timer_FB = time.time()
	# 	timer_FB = fin_timer_FB - comienzo_timer_FB
	# 	times_FB.append(timer_FB)

	# 	comienzo_timer_BT = time.time()
	# 	BackTracking = BT(grid_x,grid_y,x,y,N,sol)
	# 	fin_timer_BT = time.time()
	# 	timer_BT = fin_timer_BT - comienzo_timer_BT
	# 	times_BT.append(timer_BT)

	# 	comienzo_timer_PD = time.time()
	# 	ProgramacionDinamica = (PD(grid_x,grid_y,x,y,N,sol,pitulon)[0])
	# 	fin_timer_PD = time.time()
	# 	timer_PD = fin_timer_PD - comienzo_timer_PD
	# 	times_PD.append(timer_PD)

	# avg_time_FB = sum(times_FB) / T
	# best_time_FB = min(times_FB)
	# worst_time_FB = max(times_FB)

	# avg_time_BT = sum(times_BT) / T
	# best_time_BT = min(times_BT)
	# worst_time_BT = max(times_BT)

	# avg_time_PD = sum(times_PD) / T
	# best_time_PD = min(times_PD)
	# worst_time_PD = max(times_PD)

	#  # Imprime los resultados
	# print(T,"iteraciones para la instancia JSON ",instance_name," en Python")

	# print("\nFuerza Bruta:")
	# print("Tiempo promedio:", avg_time_FB)
	# print("Mejor tiempo:", best_time_FB)
	# print("Peor tiempo:", worst_time_FB)

	# print("\nBackTracking:")
	# print("Tiempo promedio:", avg_time_BT)
	# print("Mejor tiempo:", best_time_BT)
	# print("Peor tiempo:", worst_time_BT)

	# print("\nProgramación Dinámica:")
	# print("Tiempo promedio:", avg_time_PD)
	# print("Mejor tiempo:", best_time_PD)
	# print("Peor tiempo:", worst_time_PD)


	best = {}
	best['sol'] = [None]*(N+1)
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
	# solution['x'] = [grid_x[x[0]] for x in best['sol']]
	# solution['y'] = [grid_y[x[1]] for x in best['sol']]
	solution['x'] = [grid_x[min(x[0], len(grid_x) - 1)] for x in best['sol']]
	solution['y'] = [grid_y[min(x[1], len(grid_y) - 1)] for x in best['sol']]

	solution['obj'] = best['obj']

	# Se guarda el archivo en formato JSON
	with open('solution_' + instance_name, 'w') as f:
		json.dump(solution, f)
	
	# Obtener los breakpoints generados por tu algoritmo
	solucion = FB(grid_x,grid_y,x,y,5,sol)['puntos']

	# Extraer los valores de x e y de los breakpoints
	x_solucion = [p[0] for p in solucion]
	y_solucion = [p[1] for p in solucion]

	# Definir los límites de los ejes x e y basados en los breakpoints generados
	min_x = min(x_solucion)
	max_x = max(x_solucion)
	min_y = min(y_solucion)
	max_y = max(y_solucion)
	###########################################################GRAFICOOO#######################################################
	# Crear el gráfico
	plt.figure(figsize=(10, 6))
	solucion = FB(grid_x,grid_y,x,y,N,sol)['puntos']

	x_solucion = [p[0] for p in solucion]
	y_solucion = [p[1] for p in solucion]

	plt.plot(x_solucion, y_solucion, marker='o', color='blue', label='Puntos de la solución')

	plt.scatter(x, y, marker='o', label='Puntos del JSON')  # marker='o'' agrega puntos en los puntos de datos
	plt.xlabel('Coordenada X')
	plt.ylabel('Coordenada Y')

	plt.xticks(grid_x)  # Establece los ticks del eje x en los valores de grid_x
	plt.yticks(grid_y)  # Establece los ticks del eje y en los valores de grid_y

	plt.title('Gráfico de ' + instance_name[:-5])
	plt.grid(True)  # Mostrar cuadrícula
	plt.legend()  # Mostrar leyenda
	plt.show()
	
	
if __name__ == "__main__":
	main()