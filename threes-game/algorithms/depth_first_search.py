from .search_algorithm import SearchAlgorithm
from state import State
from structures.node import Node

class DepthFirstSearch(SearchAlgorithm):
    """Class that implements the Depth-First Search (DFS) algorithm for pathfinding."""

    def __init__(self, initial_state: State, heuristic, headless=False):
        """
        Initializes the Depth-First Search algorithm.

        :param initial_state: The initial state from which to start the search.
        :param heuristic: The heuristic function used (not utilized in DFS).
        :param headless: If True, disables console output for debugging.
        """
        self.headless = headless
        self.result, self.path, self.moves_list = self.run_algorithm(initial_state.clone_state())
        self.it = 0

    def run_algorithm(self, s):
        """
        Executes the Depth-First Search algorithm to find the shortest path.

        :param s: The initial state from which the algorithm runs.
        :return: A tuple indicating the result of the search,
                 the path found, and the list of moves.
        """
        A = Node(s)  # 1. Create a search tree with root at s
        OPEN_SET = [Node(s)]  # 1. Initialize the OPEN set with s

        CLOSED_SET = []  # 2. Create an empty CLOSED set

        while True:
            if not OPEN_SET:  # 3. If OPEN_SET is empty, return failure
                return "FAILURE", [], []

            n = OPEN_SET.pop()  # 4. Select the last node from OPEN_SET and remove it
            CLOSED_SET.append(n)  # 4. Add n to CLOSED_SET
            if not self.headless: 
                print(f"OPEN_SET: {len(OPEN_SET)} | CLOSED_SET: {len(CLOSED_SET)} | DEPTH: {len(n.antecesores())}")

            if n.value.completed_state():  # 5. If n is the goal, return the path from s to n
                return "SUCCESS", n.antecesores() + [n], n.moves_list()

            M = n.sucesores_sin_antecesores()  # 6. Expand n to get its successors

            for n2 in M:  # 7. For each successor n2 in M
                if n2 not in OPEN_SET and n2 not in CLOSED_SET:  # a. If n2 is new
                    n2.father = n  # i. Pointer from n2 to n
                    OPEN_SET.append(n2)  # ii. Add n2 to OPEN_SET
                else:  # b. If n2 is not new, ignore it
                    pass

            # 8. The OPEN_SET is already sorted by age due to how nodes are added
            # 9. Repeat from step 3 (it's a while loop, so it will continue)

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
