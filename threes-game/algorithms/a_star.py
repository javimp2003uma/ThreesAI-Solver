import heapq
from .search_algorithm import SearchAlgorithm
from state import State
from structures.node import Node

class AStar(SearchAlgorithm):

    def __init__(self, initial_state: State, heuristic, headless=False):
        self.headless = headless
        self.heuristic = heuristic
        self.result, self.path, self.moves_list = self.run_algorithm(initial_state.clone_state())
        self.it = 0

    def run_algorithm(self, s):
        g_cost = {s: 0}
        f_cost = {s: self.heuristic.evaluate(s)}

        A = Node(s)
        ABIERTOS = []
        heapq.heappush(ABIERTOS, (f_cost[s], A))
        open_set = {s: A}  # Diccionario para nodos en ABIERTOS
        CERRADOS = set()  # Conjunto para nodos en CERRADOS

        while ABIERTOS:
            _, n = heapq.heappop(ABIERTOS)
            open_set.pop(n.value, None)
            CERRADOS.add(n.value)

            if not self.headless:
                print(f"ABIERTOS: {len(ABIERTOS)} | CERRADOS: {len(CERRADOS)} | PROFUNDIDAD: {len(n.antecesores())}")

            if n.value.completed_state():
                return "ÉXITO", n.antecesores() + [n], n.moves_list()

            M = n.sucesores_sin_antecesores()

            for n2 in M:
                tentative_g_cost = g_cost[n.value] + n.value.edge_cost(n2.value)

                # # Pathmax: Asegurar consistencia en la heurística
                # if self.heuristic.evaluate(n2.value) < self.heuristic.evaluate(n.value):
                #     raise Exception("La heurística no es monotona")

                f_cost_n2 = tentative_g_cost + self.heuristic.evaluate(n2.value)

                if n2.value not in CERRADOS and (n2.value not in g_cost or tentative_g_cost < g_cost[n2.value]):
                    n2.father = n
                    g_cost[n2.value] = tentative_g_cost
                    f_cost[n2.value] = f_cost_n2

                    if n2.value not in open_set:
                        heapq.heappush(ABIERTOS, (f_cost[n2.value], n2))
                        open_set[n2.value] = n2

        return "FRACASO", [], []

    def get_next_move(self):
        if self.result != "FRACASO" and self.it < len(self.moves_list):
            next_move = self.moves_list[self.it]
            self.it += 1
            return next_move
        return None
