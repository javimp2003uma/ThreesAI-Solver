from algorithms.strategy.heuristic import Heuristic

class MaxTileAndFreeCells(Heuristic):

    def evaluate(self, state):
        # Contar las celdas vacías
        empty_cells = sum([1 for row in state.grid for cell in row if cell == 0])
        
        # Encontrar el valor máximo en el tablero
        max_tile = max([max(row) for row in state.grid])
        
        # Contar las fichas bajas (por ejemplo, fichas de valor 1, 2 y 3)
        low_tiles_count = sum([1 for row in state.grid for cell in row if cell in {1, 2, 3}])

        # Heurística: max_tile + bonus por celdas vacías - penalización por fichas bajas
        # Ajustar los pesos según sea necesario
        return max_tile + 2 * empty_cells - low_tiles_count
