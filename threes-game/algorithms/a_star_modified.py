import heapq
from .search_algorithm import SearchAlgorithm
from state import State
from structures.node import Node
from .strategy.dijkstra import Dijkstra

class AStarModified(SearchAlgorithm):
    """Class that implements the A* algorithm for pathfinding."""

    def __init__(self, initial_state: State, heuristic, headless=False):
        """
        Initializes the A* algorithm.

        :param initial_state: The initial state from which to start the search.
        :param heuristic: The heuristic function used for cost estimation.
        :param headless: Indicates whether the search runs without a graphical interface.
        """
        self.headless = headless
        self.heuristic = Dijkstra()
        self.result, self.path, self.moves_list = self.run_algorithm(initial_state.clone_state())
        self.it = 0

    def run_algorithm(self, s):
        """
        Executes the A* algorithm to find the shortest path.

        :param s: The initial state from which the algorithm runs.
        :return: A tuple indicating the result of the search,
                 the path found, and the list of moves.
        """
        g_cost = {s: 0}  # Cost from the start to each node
        f_cost = {s: self.heuristic.evaluate(s)}  # Estimated total cost (g + h)

        A = Node(s, f_cost=self.heuristic.evaluate(s))  # Create a search tree A with root at s
        OPEN_SET = []  # List of OPEN nodes with s
        heapq.heappush(OPEN_SET, (f_cost[s], A))  # Initialize the OPEN set with s
        open_set = {s: A}  # Dictionary for nodes in OPEN_SET
        CLOSED_SET = set()  # Create an empty CLOSED set

        while OPEN_SET:
            _, n = heapq.heappop(OPEN_SET)  # Select the node with the lowest f_cost
            open_set.pop(n.value, None)  # Remove n from OPEN_SET
            CLOSED_SET.add(n.value)  # Add n to CLOSED_SET
            if not self.headless:
                print(f"OPEN_SET: {len(OPEN_SET)} | CLOSED_SET: {len(CLOSED_SET)} | DEPTH: {len(n.antecesores())}")

            if n.value.completed_state():  # If n is the goal
                return "SUCCESS", n.antecesores() + [n], n.moves_list()  # Return the found path

            M = n.sucesores_sin_antecesores()  # Expand n to get its successors

            for n2 in M:  # For each successor n2
                tentative_g_cost = (n.value.edge_cost(n2.value)) / (1 + len(n.antecesores()))  # Cost to reach n2
                print(g_cost[n.value], tentative_g_cost)
                f_cost_n2 = tentative_g_cost + self.heuristic.evaluate(n2.value)
                n2.update_f_cost(tentative_g_cost, self.heuristic.evaluate(n2.value))
                # If n2 is new
                if n2.value not in CLOSED_SET and n2.value not in open_set:
                    n2.father = n  # Pointer of n2 to n
                    g_cost[n2.value] = tentative_g_cost
                    f_cost[n2.value] = f_cost_n2
                    heapq.heappush(OPEN_SET, (f_cost[n2.value], n2))  # Add n2 to OPEN_SET
                    open_set[n2.value] = n2  # Add n2 to the OPEN set

                # If n2 is not new, but the g(n2) cost is lower through the new path
                elif tentative_g_cost < g_cost[n2.value]:
                    n2.father = n  # Pointer of n2 to n
                    g_cost[n2.value] = tentative_g_cost  # Update g_cost
                    f_cost[n2.value] = f_cost_n2  # Update f_cost

                    if n2.value not in CLOSED_SET:  # If n2 is not in CLOSED_SET, add it to OPEN_SET
                        heapq.heappush(OPEN_SET, (f_cost[n2.value], n2))  # Add the node to OPEN_SET
                        open_set[n2.value] = n2  # Add n2 to the OPEN set

        return "FAILURE", [], []  # If OPEN_SET is empty, return 'FAILURE'.

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
