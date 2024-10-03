from .search_algorithm import SearchAlgorithm
from state import State
import pygame

from structures.node import Node


class BreadthFirstSearch(SearchAlgorithm):

    def __init__(self, initial_state : State):
        self.result, self.path, self.moves_list = self.run_algorithm(initial_state.clone_state())
        self.it = 0

    def run_algorithm(self, s): # se q se puede refactorizar pila, lo estoy haciendo literalmente como el pseudocodigo primero
        A = Node(s) # 1. Crear arbol de busqueda con raiz en s
        ABIERTOS = [Node(s)] # 1. Una lista de abiertos con s

        CERRADOS = [] # 2. Crear una lista de cerrados vacia

        while True:
            if ABIERTOS == []: # 3. Si abiertos esta vacia devolver fracaso
                return "FRACASO", [], []

            n = ABIERTOS.pop() # 4. Seleccionar primero de abiertos y borrarlo de abiertos
            CERRADOS.append(n) # 4. añadirlo a cerrados

            if n.value.completedState(): # 5. Si n es objetivo devolvemos el camino de s hasta n en A
                return "ÉXITO", n.antecesores() + [n.value], n.moves_list()
            
            M = n.sucesores_sin_antecesores() # 6. Expandimos n

            for n2 in M: # 7. Para cada n2 en M
                if n2 not in ABIERTOS and n2 not in CERRADOS: # a. Si n2 es nuevo
                    n2.father = n # i. Puntero de n2 a n
                    ABIERTOS.append(n2) # ii. Lo añadimos a abiertos
                else: # b. Si no es nuevo lo ignoramos
                    pass

            # 8. Ordenamos abiertos por antiguedad (ya estan ordenados por antiguedad)
            # 9. Volvemos a 3 (es un bucle while, ya lo hace)


    def get_next_move(self):
        if self.result != "FRACASO" and self.it < len(self.moves_list):
            next_move = self.moves_list[self.it]
            self.it = self.it + 1
            return next_move
        return None
    

class DepthFirstSearch(SearchAlgorithm):

    def __init__(self, initial_state: State):
        self.result, self.path, self.moves_list = self.run_algorithm(initial_state.clone_state())
        self.it = 0

    def run_algorithm(self, s):
        A = Node(s)  # Crear nodo raíz
        ABIERTOS = [Node(s)]  # Pila de abiertos (DFS usa pila)
        CERRADOS = []  # Lista de cerrados

        while True:
            if not ABIERTOS:  # Si abiertos está vacía, devolver fracaso
                return "FRACASO", [], []

            n = ABIERTOS.pop()  # Extraer el último nodo de ABIERTOS (función de pila)
            CERRADOS.append(n)  # Añadir a cerrados

            if n.value.completedState():  # Verificar si es el estado objetivo
                return "ÉXITO", n.antecesores() + [n.value], n.moves_list()

            M = n.sucesores_sin_antecesores()  # Expandir el nodo

            for n2 in M:  # Para cada sucesor
                if n2 not in ABIERTOS and n2 not in CERRADOS:  # Si el nodo no está en ABIERTOS ni CERRADOS
                    n2.father = n  # Crear puntero hacia el padre
                    ABIERTOS.append(n2)  # Añadirlo a la pila de ABIERTOS
                else:
                    pass  # Ignorar si ya ha sido explorado

    def get_next_move(self):
        if self.result != "FRACASO" and self.it < len(self.moves_list):
            next_move = self.moves_list[self.it]
            self.it += 1
            return next_move
        return None