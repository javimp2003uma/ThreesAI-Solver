import heapq
from .search_algorithm import SearchAlgorithm
from state import State
from structures.node import Node

class AStarMax(SearchAlgorithm):

    def __init__(self, initial_state: State, heuristic, headless=False):
        # Ejecuta el algoritmo A* y almacena el resultado, la ruta y la lista de movimientos
        self.headless = headless
        self.heuristic = heuristic
        self.result, self.path, self.moves_list = self.run_algorithm(initial_state.clone_state())
        self.it = 0

    def run_algorithm(self, s):
        g_cost = {s: 0}  # Coste desde el inicio hasta cada nodo
        f_cost = {s: self.heuristic.evaluate(s)}  # Coste estimado total (g + h)

        A = Node(s, f_cost=self.heuristic.evaluate(s))  # Crear un árbol de búsqueda A con raíz en s
        ABIERTOS = []  # Lista de nodos ABIERTOS con s.
        heapq.heappush(ABIERTOS, (f_cost[s], A))  # Añadir s a ABIERTOS
        open_set = {s: A}  # Diccionario para nodos en ABIERTOS
        CERRADOS = set()  # Conjunto de nodos CERRADOS

        while ABIERTOS:

            _, n = heapq.heappop(ABIERTOS)  # Seleccionar el nodo con mayor f_cost
            open_set.pop(n.value, None)  # Eliminar n de ABIERTOS
            CERRADOS.add(n.value)  # Añadir n a CERRADOS

            if not self.headless: 
                print(f"ABIERTOS: {len(ABIERTOS)} | CERRADOS: {len(CERRADOS)} | PROFUNDIDAD: {len(n.antecesores())}")

            if n.value.completed_state():  # Si n es objetivo,
                return "ÉXITO", n.antecesores() + [n], n.moves_list()  # Devolver el camino de s hasta n en A.

            M = n.sucesores_sin_antecesores()  # Expandir n

            for n2 in M:  # Para cada sucesor n2 de n,
                edge_cost = n.value.edge_cost(n2.value)

                if edge_cost < 0:
                    raise Exception("Arco negativo")
                
                # Se mantiene la verificación de monotonía
                #if self.heuristic.evaluate(n.value) - self.heuristic.evaluate(n2.value) > edge_cost:
                #    raise Exception("No monotono")
                
                tentative_g_cost = g_cost[n.value] + edge_cost  # Coste desde el nodo inicial hasta n2
                print(tentative_g_cost)
                # Cambiar la lógica para maximizar
                f_cost_n2 = tentative_g_cost + self.heuristic.evaluate(n2.value)
                n2.update_f_cost(tentative_g_cost, self.heuristic.evaluate(n2.value))

                # Si n2 es nuevo
                if n2.value not in CERRADOS and n2.value not in open_set: 
                    n2.father = n  # Puntero de n2 hacia n
                    g_cost[n2.value] = tentative_g_cost  # Actualizar g_cost
                    f_cost[n2.value] = f_cost_n2  # Actualizar f_cost
                    heapq.heappush(ABIERTOS, (-f_cost[n2.value], n2))  # Usar -f_cost para maximizar
                    open_set[n2.value] = n2  # Añadir n2 al conjunto ABIERTOS

                # Si n2 no es nuevo, y el valor de g(n2) es menor a través del nuevo camino,
                elif tentative_g_cost > g_cost[n2.value]:  # Cambia a > para maximizar
                    n2.father = n  # Puntero de n2 hacia n
                    g_cost[n2.value] = tentative_g_cost  # Actualizar g_cost
                    f_cost[n2.value] = f_cost_n2  # Actualizar f_cost

                    if n2.value not in CERRADOS:  # Si n2 no está en CERRADOS, añadirlo a ABIERTOS
                        heapq.heappush(ABIERTOS, (-f_cost[n2.value], n2))  # Usar -f_cost para maximizar
                        open_set[n2.value] = n2  # Añadir n2 al conjunto ABIERTOS

        return "FRACASO", [], []  # Si ABIERTOS está vacía, devolver ‘FRACASO’.

    def get_next_move(self):
        if self.result != "FRACASO" and self.it < len(self.moves_list):
            next_move = self.moves_list[self.it]
            self.it += 1
            return next_move
        return None
