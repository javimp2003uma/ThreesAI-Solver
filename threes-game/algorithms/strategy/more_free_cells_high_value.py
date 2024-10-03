from algorithms.strategy.heuristic import Heuristic


class MoreFreeCellsHighValue(Heuristic):

    def evaluate(self, state):
        empty_cells = sum([1 for row in state.grid for cell in row if cell == 0])
        max_tile = max([max(row) for row in state.grid])
        return -max_tile + empty_cells
