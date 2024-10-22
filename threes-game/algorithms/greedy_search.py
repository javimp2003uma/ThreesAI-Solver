from .search_algorithm import SearchAlgorithm
from state import State
from structures.node import Node
import numpy as np

class GreedySearch(SearchAlgorithm):

    def __init__(self, initial_state: State, heuristic, headless = False):
        self.headless = headless
        self.heuristic = heuristic
        self.result, self.path, self.moves_list = self.run_algorithm(initial_state.clone_state())
        self.it = 0

    def run_algorithm(self, s):
        current_node = Node(s)  # 1. Crear nodo raíz con el estado inicial
        path = [current_node]  # 2. Crear una lista para almacenar el camino

        while True:
            if not self.headless:
                print(f"Estado actual, PROFUNDIDAD: {len(path)-1}")

            if current_node.value.completed_state():  # 3. Verificar si el estado actual es el objetivo
                return "ÉXITO", path, current_node.moves_list()  # Devolver el camino y la lista de movimientos

            successors = current_node.sucesores_sin_antecesores()  # 4. Obtener sucesores del estado actual

            if not successors:  # Si no hay sucesores, no hay más opciones
                return "FRACASO", [], []

            # 5. Elegir el sucesor con el mejor valor heurístico
            best_successor = min(successors, key=lambda node: self.heuristic.evaluate(node.value))
            best_successor.father = current_node  # Apuntar al nodo padre

            current_node = best_successor  # Moverse al mejor sucesor
            path.append(current_node)  # Añadir el nuevo nodo al camino

    def get_next_move(self):
        if self.result != "FRACASO" and self.it < len(self.moves_list):
            next_move = self.moves_list[self.it]
            self.it += 1
            return next_move
        return None
