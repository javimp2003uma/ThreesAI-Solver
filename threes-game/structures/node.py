import pygame

from state import State

class Node:
    def __init__(self, value:State, move_to_node=None, father=None, f_cost = 0):
        self.value = value
        self.move_to_node = move_to_node
        self.father = father
        self.f_cost = f_cost

    def __eq__(self, other):
        if not isinstance(other, Node):
            return False
        return self.value == other.value
    
    def __lt__(self, other):
        # Aquí puedes definir cómo comparar dos nodos
        return self.f_cost < other.f_cost

    def __hash__(self):
        return hash(self.value)
    
    def moves_list(self):
        return [] if self.father is None else self.father.moves_list() + [self.move_to_node]

    def antecesores(self):
        return [] if self.father is None else self.father.antecesores() + [self.father]
    
    def sucesores(self): # Orden de expansion: movimientos ortogonales a sentido horario en los angulos de 90 (los permitidos)
        move_up_state = self.value.clone_state()
        move_up_state.move("UP")

        move_right_state = self.value.clone_state()
        move_right_state.move("RIGHT")

        move_down_state = self.value.clone_state()
        move_down_state.move("DOWN")

        move_left_state = self.value.clone_state()
        move_left_state.move("LEFT")

        move_up_node = Node(move_up_state, pygame.K_UP)
        move_right_node = Node(move_right_state, pygame.K_RIGHT)
        move_down_node = Node(move_down_state, pygame.K_DOWN)
        move_left_node = Node(move_left_state, pygame.K_LEFT)

        possible_moves = [move_up_node, move_right_node, move_down_node, move_left_node]
        valid_moves = [move for move in possible_moves if move != self]

        unique_moves = []
        for move in valid_moves:
            if move not in unique_moves:
                unique_moves.append(move)
       
        return unique_moves

    def sucesores_sin_antecesores(self):
        sucesores = self.sucesores()
        antecesores = self.antecesores()

        return [move for move in sucesores if move not in antecesores]

    def update_f_cost(self, g_cost, h_cost):
        self.f_cost = g_cost + h_cost
