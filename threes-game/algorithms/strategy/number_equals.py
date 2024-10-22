from algorithms.strategy.heuristic import Heuristic


class NumberEquals(Heuristic):
    """
    Heuristic that evaluates a state based on the matches of numbers 
    in the grid and their positions.

    This heuristic counts matches based on specific rules related to the 
    placement of numbers 1 and 2, as well as the values of the grid cells.

    Methods:
        evaluate(state): Evaluates the state based on the heuristic formula.
    """

    def evaluate(self, state):
        matches = 0
        rows = len(state.grid)
        cols = len(state.grid[0])

        for row in range(rows):
            for col in range(cols):
                value = state.grid[row][col]

                if value != 0 and (row == 0 or col == 0 or row == rows - 1 or col == cols - 1):
                    next_number = state.next_number
                    if next_number == 1 and value == 2:
                        matches += 2 if row == col else 1
                    elif next_number == 2 and value == 1:
                        matches += 2 if row == col else 1
                    elif value not in {1, 2} and next_number == value:
                        matches += 2 if row == col else 1

                if value != 0:
                    for k in range(cols):
                        if k != col:
                            if value == 1 and state.grid[row][k] == 2:
                                matches += 1
                                break
                            elif value == 2 and state.grid[row][k] == 1:
                                matches += 1
                                break
                            elif value not in {1, 2} and value == state.grid[row][k]:
                                matches += 1
                                break

                    for k in range(rows):
                        if k != row:
                            if value == 1 and state.grid[k][col] == 2:
                                matches += 1
                                break
                            elif value == 2 and state.grid[k][col] == 1:
                                matches += 1
                                break
                            elif value not in {1, 2} and value == state.grid[k][col]:
                                matches += 1
                                break

        return 16 - matches

    def get_matches(self, row, grid):
        matches = 0
        for col in range(len(grid[row])):
            if grid[row][col] == grid[row + 1][col]:
                matches += 1
        return matches
