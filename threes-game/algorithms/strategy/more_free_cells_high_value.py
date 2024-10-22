from algorithms.strategy.heuristic import Heuristic


class MoreFreeCellsHighValue(Heuristic):
    """
    Heuristic that evaluates a state based on the number of empty cells 
    and the highest tile value.

    This heuristic computes a score by combining the count of empty cells 
    and the negative value of the maximum tile on the grid.

    Methods:
        evaluate(state): Evaluates the state based on the heuristic formula.
    """

    def evaluate(self, state):
        empty_cells = sum(1 for row in state.grid for cell in row if cell == 0)
        max_tile = max(max(row) for row in state.grid)
        return -max_tile + empty_cells
