from algorithms.strategy.heuristic import Heuristic
import numpy as np

class MinNonFreeCells(Heuristic):

    def evaluate(self, state):
        return np.sum(state.grid != 0)
