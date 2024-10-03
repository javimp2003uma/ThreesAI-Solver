from .search_algorithm import SearchAlgorithm
from state import State
import pygame

class Node:
    def __init__(self, value: State, move_to_node=None, father=None):
        self.value = value
        self.move_to_node = move_to_node
        self.father = father

    def __eq__(self, other):
        if not isinstance(other, Node):
            return False
        return self.value == other.value

    def __hash__(self):
        return hash(self.value)
    
    def moves_list(self):
        return [] if self.father is None else self.father.moves_list() + [self.move_to_node]

    def sucesores(self): # No se si funciona bien
        move_left_state = self.value.clone_state()
        move_left_state.move_left()

        move_right_state = self.value.clone_state()
        move_right_state.move_right()

        move_up_state = self.value.clone_state()
        move_up_state.move_up()

        move_down_state = self.value.clone_state()
        move_down_state.move_down()

        move_left_node = Node(move_left_state, pygame.K_LEFT)
        move_right_node = Node(move_right_state, pygame.K_RIGHT)
        move_up_node = Node(move_up_state, pygame.K_UP)
        move_down_node = Node(move_down_state, pygame.K_DOWN)

        possible_moves = [move_left_node, move_right_node, move_up_node, move_down_node]
        valid_moves = [move for move in possible_moves if move != self.value]
        unique_moves = list(set(valid_moves))

        return unique_moves

    def antecesores(self):
        return [] if self.father is None else self.father.antecesores() + [self.father]

    def sucesores_sin_antecesores(self):
        sucesores = set(self.sucesores())  
        antecesores = set(self.antecesores()) 
        
        return list(sucesores - antecesores)


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