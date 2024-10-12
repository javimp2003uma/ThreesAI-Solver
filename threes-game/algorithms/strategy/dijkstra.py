from algorithms.strategy.heuristic import Heuristic


class Dijkstra(Heuristic):

    def evaluate(self, state):
        return 0