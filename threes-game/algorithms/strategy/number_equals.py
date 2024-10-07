from algorithms.strategy.heuristic import Heuristic


class NumberEquals(Heuristic):

    def evaluate(self, state):
        matchs = 0      
        rows = len(state.grid)
        cols = len(state.grid[0])

        for row in range(rows):
            for col in range(cols):
                value = state.grid[row][col]
                if value != 0:
                    for k in range(cols):
                        if k != col and value == 1 and state.grid[row][k] == 2:
                            matchs += 1
                            break
                        elif k != col and value == 2 and state.grid[row][k] == 1:
                            matchs += 1
                            break
                        elif k != col and value == state.grid[row][k]:
                            matchs += 1
                            break

                    for k in range(rows):
                        if k != row and value == 1 and state.grid[k][col] == 2:
                            matchs += 1
                            break
                        elif k != row and value == 2 and state.grid[k][col] == 1:
                            matchs += 1
                            break
                        elif k != row and value == state.grid[k][col]:
                            matchs += 1
                            break

        return 16 - matchs
                
            

    def getMatches(row, grid):
        matches = 0
        for col in range(len(grid[row])):
            if grid[row][col] == grid[row + 1][col]:
                matches += 1

