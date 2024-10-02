from .search_algorithm import SearchAlgorithm
from state import State

class Node:
    def __init__(self, value: State, father=None):
        self.value = value
        self.father = father

    def sucesores(self):
        move_left_state = self.value.clone_state().move_left()
        move_right_state = self.value.clone_state().move_right()
        move_up_state = self.value.clone_state().move_up()
        move_down_state = self.value.clone_state().move_down()

        possible_moves = [move_left_state, move_right_state, move_up_state, move_down_state]
        valid_moves = [move for move in possible_moves if move != self.value]

        return list(set(valid_moves))

    def antecesores(self):
        return [] if self.father is None else [self.father] + self.father.antecesores()

    def sucesores_sin_antecesores(self):
        sucesores = set(self.sucesores())  
        antecesores = set(self.antecesores()) 
        
        return list(sucesores - antecesores)


class BreadthFirstSearch(SearchAlgorithm):

    def __init__(self, initial_state):
        self.path = self.run_algorithm(initial_state)

    def run_algorithm(self, s):
        ABIERTOS = [Node(s)]
        CERRADOS = []

        A = Node(s)

        while True:
            if ABIERTOS == []:
                return "FRACASO"
            
            n = ABIERTOS[0]

            if n.value.completedState():
                return None # Camino desde S hasta N en A
            
            M = n.sucesores_sin_antecesores()

    def get_next_move(self):
        return "w"