from .search_algorithm import SearchAlgorithm
from state import State
from structures.node import Node
import numpy as np

class GreedySearch(SearchAlgorithm):
    """Class that implements the Greedy Search algorithm for pathfinding."""

    def __init__(self, initial_state: State, heuristic, headless=False):
        """
        Initializes the Greedy Search algorithm.

        :param initial_state: The initial state from which to start the search.
        :param heuristic: The heuristic function used to evaluate successors.
        :param headless: If True, disables console output for debugging.
        """
        self.headless = headless
        self.heuristic = heuristic
        self.result, self.path, self.moves_list = self.run_algorithm(initial_state.clone_state())
        self.it = 0

    def run_algorithm(self, s):
        """
        Executes the Greedy Search algorithm to find the shortest path.

        :param s: The initial state from which the algorithm runs.
        :return: A tuple indicating the result of the search,
                 the path found, and the list of moves.
        """
        current_node = Node(s)  # 1. Create root node with the initial state
        path = [current_node]  # 2. Create a list to store the path

        while True:
            if not self.headless:
                print(f"Current state, DEPTH: {len(path) - 1}")

            if current_node.value.completed_state():  # 3. Check if the current state is the goal
                return "SUCCESS", path, current_node.moves_list()  # Return the path and the list of moves

            successors = current_node.sucesores_sin_antecesores()  # 4. Get successors of the current state

            if not successors:  # If there are no successors, there are no more options
                return "FAILURE", [], []

            # 5. Choose the successor with the best heuristic value
            best_successor = min(successors, key=lambda node: self.heuristic.evaluate(node.value))
            best_successor.father = current_node  # Point to the parent node

            current_node = best_successor  # Move to the best successor
            path.append(current_node)  # Add the new node to the path

    def get_next_move(self):
        """
        Gets the next move in the sequence of moves.

        :return: The next move, or None if the end has been reached.
        """
        if self.result != "FAILURE" and self.it < len(self.moves_list):
            next_move = self.moves_list[self.it]
            self.it += 1
            return next_move
        return None
