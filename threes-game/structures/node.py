from enum import Enum
import pygame
from state import State


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
    
