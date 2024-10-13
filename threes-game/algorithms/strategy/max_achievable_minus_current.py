from algorithms.strategy.heuristic import Heuristic

class MaxAchievableMinusCurrentScore(Heuristic):

    def evaluate(self, state):
        # Calcular el puntaje máximo posible en el juego (suponiendo que 768 es el valor maximo por casilla)
        totalMaxScore = state.maxPoints()

        # Calcular el heuristico basado en el estado actual
        return totalMaxScore - state.total_points()