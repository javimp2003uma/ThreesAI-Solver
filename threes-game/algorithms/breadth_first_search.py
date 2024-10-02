from .search_algorithm import SearchAlgorithm
from state import State

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
        move_left_state = Node(self.value.clone_state().move_left(), "a")
        move_right_state = Node(self.value.clone_state().move_right(), "d")
        move_up_state = Node(self.value.clone_state().move_up(), "w")
        move_down_state = Node(self.value.clone_state().move_down(), "s")

        possible_moves = [move_left_state, move_right_state, move_up_state, move_down_state]
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

    def __init__(self, initial_state):
        self.path, self.moves_list = self.run_algorithm(initial_state)
        self.it = 0

    def run_algorithm(self, s): # se q se puede refactorizar pila, lo estoy haciendo literalmente como el pseudocodigo primero
        A = Node(s) # 1. Crear arbol de busqueda con raiz en s
        ABIERTOS = [Node(s)] # 1. Una lista de abiertos con s

        CERRADOS = [] # 2. Crear una lista de cerrados vacia

        while True:
            if ABIERTOS == []: # 3. Si abiertos esta vacia devolver fracaso
                return "FRACASO"
            
            n = ABIERTOS.pop() # 4. Seleccionar primero de abiertos y borrarlo de abiertos
            CERRADOS.append(n) # 4. añadirlo a cerrados

            if n.value.completedState(): # 5. Si n es objetivo devolvemos el camino de s hasta n en A
                return n.antecesores() + [n.value], n.moves_list()
            
            M = n.sucesores_sin_antecesores() # 6. Expandimos n

            for n2 in M: # 7. Para cada n2 en M
                if n2 not in ABIERTOS and n2 not in CERRADOS: # a. Si n2 es nuevo
                    n2.father = n # i. Puntero de n2 a n
                    ABIERTOS.append(n2) # ii. Lo añadimos a abuiertos
                else: # b. Si no es nuevo lo ignoramos
                    pass

            # 8. Ordenamos abiertos por antiguedad (ya estan ordenados por antiguedad)
            # 9. Volvemos a 3 (es un bucle while, ya lo hace)


    def get_next_move(self):
        if self.path != "FRACASO":
            next_move = self.moves_list[self.it]
            self.it = self.it + 1
            return next_move
        return None