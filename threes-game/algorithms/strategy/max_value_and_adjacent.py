from algorithms.strategy.heuristic import Heuristic


class MaxValueAndAdjacent(Heuristic):
    """
    Heuristic that evaluates a state based on the maximum tile value,
    the number of empty cells, and the sum of adjacent tile values.

    This heuristic computes a score by considering the highest tile on the 
    grid, the bonus for empty cells, and the contribution of adjacent tile values.

    Methods:
        evaluate(state): Evaluates the state based on the heuristic formula.
    """

    def evaluate(self, state):
        max_tile = max(max(row) for row in state.grid)
        empty_cells = sum(1 for row in state.grid for cell in row if cell == 0)
        
        adjacent_value_sum = 0
        for i in range(len(state.grid)):
            for j in range(len(state.grid[i])):
                if state.grid[i][j] == max_tile:
                    if i > 0:
                        adjacent_value_sum += state.grid[i - 1][j]
                    if i < 3:
                        adjacent_value_sum += state.grid[i + 1][j]
                    if j > 0:
                        adjacent_value_sum += state.grid[i][j - 1]
                    if j < 3:
                        adjacent_value_sum += state.grid[i][j + 1]

        return -max_tile + empty_cells + 0.1 * adjacent_value_sum
