from algorithms.strategy.heuristic import Heuristic


class MaxTilesCombinationPotential(Heuristic):
    """
    Heuristic that evaluates a state based on the maximum tile value,
    the number of empty cells, combination potential, and mobility score.

    This heuristic computes a score by considering the highest tile on the 
    grid, the bonus for empty cells, the potential for tile combinations, 
    and the mobility of tiles.

    Methods:
        evaluate(state): Evaluates the state based on the heuristic formula.
    """

    def evaluate(self, state):
        max_tile = max(max(row) for row in state.grid)
        empty_cells = sum(1 for row in state.grid for cell in row if cell == 0)
        
        combination_potential = 0
        mobility_score = 0
        
        for i in range(4):
            for j in range(4):
                current_tile = state.grid[i][j]
                if current_tile != 0:
                    if i > 0 and state.grid[i - 1][j] == current_tile:
                        combination_potential += 1
                    if i < 3 and state.grid[i + 1][j] == current_tile:
                        combination_potential += 1
                    if j > 0 and state.grid[i][j - 1] == current_tile:
                        combination_potential += 1
                    if j < 3 and state.grid[i][j + 1] == current_tile:
                        combination_potential += 1
                    
                    if i > 0 and state.grid[i - 1][j] == 0:
                        mobility_score += 1
                    if i < 3 and state.grid[i + 1][j] == 0:
                        mobility_score += 1
                    if j > 0 and state.grid[i][j - 1] == 0:
                        mobility_score += 1
                    if j < 3 and state.grid[i][j + 1] == 0:
                        mobility_score += 1
        
        return -max_tile + empty_cells + 2 * combination_potential + mobility_score - 0.5 * (empty_cells - combination_potential)
