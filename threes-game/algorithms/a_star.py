from .search_algorithm import SearchAlgorithm
from state import State
from structures.node import Node
import heapq  # Usamos una cola de prioridad para A*


class AStar(SearchAlgorithm):

    def __init__(self, initial_state: State, heuristic):
        # Ejecuta el algoritmo A* y almacena el resultado, la ruta y la lista de movimientos
        self.heuristic = heuristic
        self.result, self.path, self.moves_list = self.run_algorithm(initial_state.clone_state())
        self.it = 0  # Iterador para devolver los movimientos uno por uno


    def run_algorithm(self, s):
        g_cost = {s: 0}  # Coste desde el inicio hasta cada nodo
        f_cost = {s: self.heuristic.evaluate(s)}  # Coste estimado total (g + h)

        A = Node(s)  # PASO 1 Crear un árbol de búsqueda A con raíz en s
        ABIERTOS = []  # PASO 1 ista de nodos ABIERTOS con s.
        heapq.heappush(ABIERTOS, (f_cost[s], Node(s)))  # PASO 1 ista de nodos ABIERTOS con s. 
        CERRADOS = []  # PASO 2 Crear una lista de nodos CERRADOS vacía. 

        while ABIERTOS:

            _, n = heapq.heappop(ABIERTOS)  # PASO 4 Seleccionar n <- primero(ABIERTOS).(menor f_cost)
            CERRADOS.append(n)  # PASO 4 Borrar n de ABIERTOS y añadirlo a CERRADOS.
            print(f"ABIERTOS: {len(ABIERTOS)} | CERRADOS: {len(CERRADOS)} | PROFUNDIDAD: {len(n.antecesores())}")
            if n.value.completed_state():  #PASO 5. Si n es objetivo, 
                return "ÉXITO", n.antecesores() + [n], n.moves_list() #PASO 5 entonces devolver el camino de s hasta n en A.

            M = n.sucesores_sin_antecesores()  # PASO 6 Expandir n. M <- sucesores(n, G) – antecesores(n, A). 

            for n2 in M:  #PASO 7. Para cada n2 en M,
                tentative_g_cost = g_cost[n.value] + 1  # Coste desde el nodo inicial hasta n2

                # # PASO 7a. Si n2 es nuevo (n2 no está ABIERTO ni CERRADO), 
                # if n2 not in ABIERTOS and n2 not in CERRADOS: 
                #     #PASO 7a.i. Puntero de n2 hacia n
                #     n2.father = n
                #         # Aquí actualizamos g_cost y f_cost para n2
                #     g_cost[n2.value] = tentative_g_cost  # Actualizar g_cost para el nuevo nodo
                #     f_cost[n2.value] = tentative_g_cost + self.heuristic(n2)  # Calcular f(n2)

                #     #PASO 7a.ii. Añadir n2 a ABIERTOS
                #     print(f"Coste2: {f_cost[n2.value]}")
                #     heapq.heappush(ABIERTOS, (f_cost[n2.value], n2))

                #Paso 4b. Si n2 no es nuevo, y el valor de g(n2) es menor a través del nuevo camino,
                if n2.value not in g_cost or tentative_g_cost < g_cost[n2.value]:
                    n2.father = n  #Paso 4b.i. Puntero de n2 hacia n(padre)
                    g_cost[n2.value] = tentative_g_cost  # Actualizar g_cost
                    f_cost[n2.value] = tentative_g_cost + self.heuristic.evaluate(n2.value)  # Actualizar f_cost

                    if n2 not in CERRADOS:  #Paso 4b.ii. Si n2 no está en CERRADOS, añadirlo a ABIERTOS
                        heapq.heappush(ABIERTOS, (f_cost[n2.value], n2))  # Añadir el nodo a ABIERTOS

            #PASO 8. Ordenar ABIERTOS por f_cost
            #PASO 9. Volver a 3 (es un bucle while, ya lo hace)

        return "FRACASO", [], []  # #PASO 3 Si ABIERTOS está vacía, entonces devolver ‘FRACASO’. 

    def heuristic(self, state: State):
        """
        Función heurística. Puede ser mejorada según el problema.
        Aquí evaluamos el número de celdas vacías y la ficha más alta como heurística.
        """
        empty_cells = sum([1 for row in state.grid for cell in row if cell == 0])
        max_tile = max([max(row) for row in state.grid])
        return -max_tile + empty_cells  # Queremos fichas grandes y más espacios vacíos
        # return 0
    def get_next_state(self):
        if self.result != "FRACASO" and self.it < len(self.moves_list):
            next_state = self.path[self.it + 1].value # El primer state es el estado inicial
            next_move = self.moves_list[self.it]
            self.it = self.it + 1
            return next_state, next_move
        return None, None
