from algorithms.strategy.heuristic import Heuristic

class MaxTilesCombinationPotential(Heuristic):

    def evaluate(self, state):
        max_tile = max(max(row) for row in state.grid)
        empty_cells = sum(1 for row in state.grid for cell in row if cell == 0)
        
        combination_potential = 0
        mobility_score = 0
        
        # Evaluar combinaciones y movilidad
        for i in range(4):
            for j in range(4):
                current_tile = state.grid[i][j]
                if current_tile != 0:
                    # Sumar potencial de combinaciones
                    if i > 0 and state.grid[i-1][j] == current_tile:  # arriba
                        combination_potential += 1
                    if i < 3 and state.grid[i+1][j] == current_tile:  # abajo
                        combination_potential += 1
                    if j > 0 and state.grid[i][j-1] == current_tile:  # izquierda
                        combination_potential += 1
                    if j < 3 and state.grid[i][j+1] == current_tile:  # derecha
                        combination_potential += 1
                    
                    # Evaluar movilidad (celdas adyacentes vacías)
                    if i > 0 and state.grid[i-1][j] == 0:  # arriba
                        mobility_score += 1
                    if i < 3 and state.grid[i+1][j] == 0:  # abajo
                        mobility_score += 1
                    if j > 0 and state.grid[i][j-1] == 0:  # izquierda
                        mobility_score += 1
                    if j < 3 and state.grid[i][j+1] == 0:  # derecha
                        mobility_score += 1
        
        # Heurística combinada
        return -max_tile + empty_cells + 2 * combination_potential + mobility_score - 0.5 * (empty_cells - combination_potential)
