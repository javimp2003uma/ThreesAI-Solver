from algorithms.strategy.heuristic import Heuristic


class MaxAchievableMinusCurrentScore(Heuristic):
    """
    Heuristic that calculates the difference between the maximum achievable score
    and the current score.

    This heuristic evaluates a given state by determining the total maximum score
    and subtracting the total points currently achieved.

    Methods:
        evaluate(state): Evaluates the state by calculating the difference 
                         between max achievable points and total points.
    """

    def evaluate(self, state):
        """
        Evaluates the given state by calculating the difference between the maximum 
        achievable score and the current total score.

        Args:
            state: An object representing the current state, which must implement 
                   methods to retrieve maximum points and total points.

        Returns:
            int: The difference between the maximum achievable score and the current 
                 total points.
        """
        total_max_score = state.max_points()
        return total_max_score - state.total_points()
