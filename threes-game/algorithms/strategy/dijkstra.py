from algorithms.strategy.heuristic import Heuristic


class Dijkstra(Heuristic):
    """
    Class that implements Dijkstra's algorithm, inheriting from the Heuristic class.

    Dijkstra's algorithm is used to find the shortest path from a starting node
    to all other nodes in a weighted graph.

    Methods:
        evaluate(state): Evaluates the given state. In this case, always returns 0.
    """

    def evaluate(self, state):
        """
        Evaluates the provided state.

        This method is a specific implementation for Dijkstra's algorithm,
        which in this case does not evaluate the state meaningfully and always
        returns 0.

        Args:
            state: The state to be evaluated.

        Returns:
            int: Always returns 0.
        """
        return 0
