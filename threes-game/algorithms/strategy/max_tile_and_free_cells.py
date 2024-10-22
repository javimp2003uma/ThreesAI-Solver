from algorithms.strategy.heuristic import Heuristic


class MaxTileAndFreeCells(Heuristic):
    """
    Heuristic that evaluates a state based on the maximum tile value,
    the number of empty cells, and the count of low-value tiles.

    This heuristic computes a score by considering the highest tile on the 
    grid, the bonus for empty cells, and a penalty for low-value tiles.

    Methods:
        evaluate(state): Evaluates the state based on the heuristic formula.
    """

    def evaluate(self, state):
        """
        Evaluates the given state based on the maximum tile value, the number 
        of empty cells, and the count of low-value tiles.

        Args:
            state: An object representing the current state, which must implement 
                   a grid property (2D list) with numerical tile values.

        Returns:
            int: The computed heuristic score, calculated as:
                  max_tile + (2 * empty_cells) - low_tiles_count
        """
        empty_cells = sum(1 for row in state.grid for cell in row if cell == 0)

        max_tile = max(max(row) for row in state.grid)

        low_tiles_count = sum(1 for row in state.grid for cell in row if cell in {1, 2, 3})

        return max_tile + 2 * empty_cells - low_tiles_count
