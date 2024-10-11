from algorithms.strategy.heuristic import Heuristic

class MaxValueAndAdjacent(Heuristic):

    def evaluate(self, state):
        max_tile = max(max(row) for row in state.grid)
        empty_cells = sum(1 for row in state.grid for cell in row if cell == 0)
        
        # Evaluar celdas adyacentes de alto valor
        adjacent_value_sum = 0
        for i in range(len(state.grid)):
            for j in range(len(state.grid[i])):
                if state.grid[i][j] == max_tile:
                    # Sumar valores de las celdas adyacentes
                    if i > 0: adjacent_value_sum += state.grid[i-1][j]  # arriba
                    if i < 3: adjacent_value_sum += state.grid[i+1][j]  # abajo
                    if j > 0: adjacent_value_sum += state.grid[i][j-1]  # izquierda
                    if j < 3: adjacent_value_sum += state.grid[i][j+1]  # derecha

        # Heurística combinada
        return -max_tile + empty_cells + 0.1 * adjacent_value_sum
