import pygame
from state import State

class Node:
    """Represents a node in the search algorithm."""

    def __init__(self, value: State, move_to_node=None, father=None, f_cost=0):
        """
        Initializes a node.

        :param value: The state associated with this node.
        :param move_to_node: The move that leads to this node.
        :param father: The parent node of this node.
        :param f_cost: The total cost of this node.
        """
        self.value = value
        self.move_to_node = move_to_node
        self.father = father
        self.f_cost = f_cost

    def __eq__(self, other):
        """Checks if two nodes are equal based on their state value."""
        if not isinstance(other, Node):
            return False
        return self.value == other.value
    
    def __lt__(self, other):
        """Defines the comparison between two nodes based on their f_cost."""
        return self.f_cost < other.f_cost

    def __hash__(self):
        """Returns the hash of the node based on its value."""
        return hash(self.value)
    
    def moves_list(self):
        """
        Returns the list of moves taken to reach this node.

        :return: A list of moves from the root to this node.
        """
        return [] if self.father is None else self.father.moves_list() + [self.move_to_node]

    def antecesores(self):
        """
        Returns the list of ancestors of this node.

        :return: A list of ancestor nodes.
        """
        return [] if self.father is None else self.father.antecesores() + [self.father]
    
    def sucesores(self):
        """
        Generates the successor nodes based on possible moves.

        The order of expansion is orthogonal movements in clockwise direction.

        :return: A list of valid successor nodes.
        """
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
        """
        Returns successors that are not ancestors.

        :return: A list of successors that are not ancestors.
        """
        sucesores = self.sucesores()
        antecesores = self.antecesores()

        return [move for move in sucesores if move not in antecesores]

    def update_f_cost(self, g_cost, h_cost):
        """
        Updates the f_cost of the node.

        :param g_cost: The cost from the start node to this node.
        :param h_cost: The heuristic cost to reach the goal from this node.
        """
        self.f_cost = g_cost + h_cost
