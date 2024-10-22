from algorithms.strategy.heuristic import Heuristic
import numpy as np


class MinNonFreeCells(Heuristic):
    """
    Heuristic that evaluates a state based on the number of non-empty cells.

    This heuristic computes a score by summing the number of cells that are not free (non-zero).

    Methods:
        evaluate(state): Evaluates the state based on the heuristic formula.
    """

    def evaluate(self, state):
        return np.sum(state.grid != 0)
