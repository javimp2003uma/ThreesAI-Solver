from algorithms.strategy.heuristic import Heuristic


class NumberEquals(Heuristic):

    def evaluate(self, state):
        matchs = 0
        rows = len(state.grid)
        cols = len(state.grid[0])

        for row in range(rows):
            for col in range(cols):

                value = state.grid[row][col]

                if (value != 0) and (row == 0 or col == 0 or row == rows - 1 or col == cols - 1):
                    next_number = state.next_number
                    if next_number == 1 and value == 2:
                        if row == col:
                            matchs += 2
                        else:
                            matchs += 1
                    elif next_number == 2 and value == 1:
                        if row == col:
                            matchs += 2
                        else:
                            matchs += 1
                    elif value != 1 and value != 2 and next_number == value:
                        if row == col:
                            matchs += 2
                        else:
                            matchs += 1

                if value != 0:
                    for k in range(cols):
                        if k != col and value == 1 and state.grid[row][k] == 2:
                            matchs += 1
                            break
                        elif k != col and value == 2 and state.grid[row][k] == 1:
                            matchs += 1
                            break
                        elif value != 1 and value != 2 and k != col and value == state.grid[row][k]:
                            matchs += 1
                            break

                    for k in range(rows):
                        if k != row and value == 1 and state.grid[k][col] == 2:
                            matchs += 1
                            break
                        elif k != row and value == 2 and state.grid[k][col] == 1:
                            matchs += 1
                            break
                        elif value != 1 and value != 2 and k != row and value == state.grid[k][col]:
                            matchs += 1
                            break

        return 16 - matchs

    def getMatches(row, grid):
        matches = 0
        for col in range(len(grid[row])):
            if grid[row][col] == grid[row + 1][col]:
                matches += 1
