from .search_algorithm import SearchAlgorithm
from structures.node import Node, MOVEMENTS
from state import State


class DepthFirstSearch(SearchAlgorithm):

    def __init__(self, initial_state: State, heuristic):
        self.result, self.path, self.moves_list = self.run_algorithm(initial_state.clone_state())
        self.it = 0

    def run_algorithm(self, s):
        A = Node(s)  # 1. Crear arbol de busqueda con raiz en s
        ABIERTOS = [Node(s)]  # 1. Una lista de abiertos con s

        CERRADOS = []  # 2. Crear una lista de cerrados vacia

        while True:
            if ABIERTOS == []:  # 3. Si abiertos esta vacia devolver fracaso
                return "FRACASO", [], []

            n = ABIERTOS.pop()  # 4. Seleccionar primero de abiertos y borrarlo de abiertos
            CERRADOS.append(n)  # 4. añadirlo a cerrados
            #print(n.value.grid)
            print(f"ABIERTOS: {len(ABIERTOS)} | CERRADOS: {len(CERRADOS)} | PROFUNDIDAD: {len(n.antecesores())}")

            if n.value.completed_state():  # 5. Si n es objetivo devolvemos el camino de s hasta n en A
                return "ÉXITO", n.antecesores() + [n], n.moves_list()

            M = n.sucesores_sin_antecesores()  # 6. Expandimos n

            for n2 in M:  # 7. Para cada n2 en M
                if n2 not in ABIERTOS and n2 not in CERRADOS:  # a. Si n2 es nuevo
                    n2.father = n  # i. Puntero de n2 a n
                    ABIERTOS.append(n2)  # ii. Lo añadimos a abiertos
                else:  # b. Si no es nuevo lo ignoramos
                    pass

            # 8. Ordenamos abiertos por antiguedad (ya estan ordenados por antiguedad)
            # 9. Volvemos a 3 (es un bucle while, ya lo hace)

    #def get_next_move(self):
    #    if self.result != "FRACASO" and self.it < len(self.moves_list):
    #        next_move = self.moves_list[self.it]
    #        self.it = self.it + 1
    #        return next_move
    #    return None

    def get_next_state(self):
        if self.result != "FRACASO" and self.it < len(self.moves_list):
            next_state = self.path[self.it + 1].value  # El primer state es el estado inicial
            next_move = self.moves_list[self.it]
            self.it = self.it + 1
            return next_state, next_move
        return None, None
