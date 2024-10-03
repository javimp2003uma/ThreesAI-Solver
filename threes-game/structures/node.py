from enum import Enum
import pygame
from state import State

TRANSLATE_MOVES = {
    pygame.K_LEFT: "LEFT",
    pygame.K_RIGHT: "RIGHT",
    pygame.K_UP: "UP",
    pygame.K_DOWN: "DOWN"
}

class MOVEMENTS(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3

class Node:
    def __init__(self, value:State, move_to_node=None, father=None):
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

    def antecesores(self):
        return [] if self.father is None else self.father.antecesores() + [self.father]
    
    def sucesores(self): # Orden de expansion: movimientos ortogonales a sentido horario en los angulos de 90 (los permitidos)
        move_up_state = self.value.clone_state()
        move_up_state.move_up()

        move_right_state = self.value.clone_state()
        move_right_state.move_right()

        move_down_state = self.value.clone_state()
        move_down_state.move_down()

        move_left_state = self.value.clone_state()
        move_left_state.move_left()

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

