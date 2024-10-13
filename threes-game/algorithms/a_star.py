import heapq
from .search_algorithm import SearchAlgorithm
from state import State
from structures.node import Node

class AStar(SearchAlgorithm):

    def __init__(self, initial_state: State, heuristic, headless=False):
        # Ejecuta el algoritmo A* y almacena el resultado, la ruta y la lista de movimientos
        self.headless = headless
        self.heuristic = heuristic
        self.result, self.path, self.moves_list = self.run_algorithm(initial_state.clone_state())
        self.it = 0

    def run_algorithm(self, s):
        g_cost = {s: 0}  # Coste desde el inicio hasta cada nodo
        f_cost = {s: self.heuristic.evaluate(s)}  # Coste estimado total (g + h)

        A = Node(s)  # PASO 1 Crear un árbol de búsqueda A con raíz en s
        ABIERTOS = []  # PASO 1 Lista de nodos ABIERTOS con s.
        heapq.heappush(ABIERTOS, (f_cost[s], A))  # PASO 1 Lista de nodos ABIERTOS con s. 
        open_set = {s: A}  # Diccionario para nodos en ABIERTOS
        CERRADOS = set()  # PASO 2 Crear un conjunto de nodos CERRADOS vacía. 

        while ABIERTOS:

            _, n = heapq.heappop(ABIERTOS)  # PASO 4 Seleccionar n <- primero(ABIERTOS).(menor f_cost)
            open_set.pop(n.value, None)  # Eliminar n de ABIERTOS
            CERRADOS.add(n.value)  # PASO 4 Borrar n de ABIERTOS y añadirlo a CERRADOS.
            if not self.headless: 
                print(f"ABIERTOS: {len(ABIERTOS)} | CERRADOS: {len(CERRADOS)} | PROFUNDIDAD: {len(n.antecesores())}")

            if n.value.completed_state():  # PASO 5. Si n es objetivo, 
                return "ÉXITO", n.antecesores() + [n], n.moves_list()  # PASO 5 entonces devolver el camino de s hasta n en A.

            M = n.sucesores_sin_antecesores()  # PASO 6 Expandir n. M <- sucesores(n, G) – antecesores(n, A). 

            for n2 in M:  # PASO 7. Para cada n2 en M,
                tentative_g_cost = g_cost[n.value] + n.value.edge_cost(n2.value)  # Coste desde el nodo inicial hasta n2

                # Restriccion de monotonía
                # if(self.heuristic.evaluate(n.value)- self.heuristic.evaluate(n2.value) > n.value.edge_cost(n2.value)):
                #     raise Exception("Heuristic is not monotonous")
                f_cost_n2 = tentative_g_cost + self.heuristic.evaluate(n2.value)

                # PASO 7a. Si n2 es nuevo (n2 no está ABIERTO ni CERRADO), 
                if n2.value not in CERRADOS and n2.value not in open_set: 
                    # PASO 7a.i. Puntero de n2 hacia n
                    n2.father = n
                    # Añadir valores de g y f
                    g_cost[n2.value] = tentative_g_cost
                    f_cost[n2.value] = f_cost_n2
                    # PASO 7a.ii. Añadir n2 a ABIERTOS
                    heapq.heappush(ABIERTOS, (f_cost[n2.value], n2))
                    open_set[n2.value] = n2  # Añadir n2 al conjunto ABIERTOS

                # Paso 4b. Si n2 no es nuevo, y el valor de g(n2) es menor a través del nuevo camino,
                elif  tentative_g_cost < g_cost[n2.value]:
                    n2.father = n  # Paso 4b.i. Puntero de n2 hacia n(padre)
                    g_cost[n2.value] = tentative_g_cost  # Actualizar g_cost
                    f_cost[n2.value] = f_cost_n2  # Actualizar f_cost

                    if n2.value not in CERRADOS:  # Paso 4b.ii. Si n2 no está en CERRADOS, añadirlo a ABIERTOS
                        heapq.heappush(ABIERTOS, (f_cost[n2.value], n2))  # Añadir el nodo a ABIERTOS
                        open_set[n2.value] = n2  # Añadir n2 al conjunto ABIERTOS

                #Simplificación del código 
                # if n2.value not in CERRADOS and (n2.value not in g_cost or tentative_g_cost < g_cost[n2.value]):
                #     n2.father = n
                #     g_cost[n2.value] = tentative_g_cost
                #     f_cost[n2.value] = f_cost_n2

                #     if n2.value not in open_set:
                #         heapq.heappush(ABIERTOS, (f_cost[n2.value], n2))
                #         open_set[n2.value] = n2




        return "FRACASO", [], []  # PASO 3 Si ABIERTOS está vacía, entonces devolver ‘FRACASO’. 

    def get_next_move(self):
        if self.result != "FRACASO" and self.it < len(self.moves_list):
            next_move = self.moves_list[self.it]
            self.it += 1
            return next_move
        return None
