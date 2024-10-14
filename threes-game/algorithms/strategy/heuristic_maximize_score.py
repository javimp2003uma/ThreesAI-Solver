import random as rnd
import numpy as np
class HeuristicMaximizeScore:
    def evaluate(self, state):
        # Calcular el máximo puntaje alcanzable en el estado actual
        totalMaxScore = state.maxPoints()
        
        # Evaluar el puntaje actual del estado
        currentScore = state.total_points()
        
        # Obtener el próximo número y la posición probable donde aparecerá
        nextNumber = state.next_number
        probablePosition = self.calculateProbablePosition(state)
        
        # Factor para evaluar la colocación del próximo número
        positionFactor = self.evaluatePositionImpact(state, nextNumber, probablePosition)
        
        # Factor para evaluar la cantidad de celdas vacías
        emptyCellsFactor = self.evaluateEmptyCells(state)
        
        # Factor para evaluar la distribución de números grandes
        distributionFactor = self.evaluateLargeNumberDistribution(state)
        
        # Ajustar la heurística usando el puntaje actual, el impacto de la próxima colocación, la distribución
        # de los números grandes y la cantidad de celdas vacías
        heuristicValue = (
            currentScore + 
            (totalMaxScore - currentScore) * 0.5 + 
            positionFactor + 
            emptyCellsFactor + 
            distributionFactor
        )
        
        return heuristicValue
    
    def calculateProbablePosition(self, state):
        """
        Calcula la posición probable donde el próximo número aparecerá.
        """
        size = state.size
        next_number = state.next_number
        grid = state.grid
        
        # Obtener todas las celdas vacías
        empty_cells = [(r, c) for r in range(size) for c in range(size) if grid[r, c] == 0]
        
        if not empty_cells:
            return None
        
        # Evaluar celdas vacías y priorizar las que tienen adyacentes fusionables
        probable_positions = []
        for (r, c) in empty_cells:
            if (r > 0 and state.can_merge(next_number, grid[r - 1, c])) or \
               (r < size - 1 and state.can_merge(next_number, grid[r + 1, c])) or \
               (c > 0 and state.can_merge(next_number, grid[r, c - 1])) or \
               (c < size - 1 and state.can_merge(next_number, grid[r, c + 1])):
                probable_positions.append((r, c))
        
        if probable_positions:
            return rnd.choice(probable_positions)
        
        # Elegir la celda vacía con más vecinos vacíos
        max_neighbors = -1
        best_position = None
        for (r, c) in empty_cells:
            empty_neighbors = sum(
                1 for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]
                if 0 <= r + dr < size and 0 <= c + dc < size and grid[r + dr, c + dc] == 0
            )
            if empty_neighbors > max_neighbors:
                max_neighbors = empty_neighbors
                best_position = (r, c)
                
        return best_position if best_position else rnd.choice(empty_cells)
    
    def evaluatePositionImpact(self, state, next_number, probable_position):
        """
        Evalúa el impacto de colocar el próximo número en la posición probable.
        """
        if probable_position is None:
            return -100  # Penalizar posiciones inválidas
        
        r, c = probable_position
        size = state.size
        grid = state.grid
        impact_value = 0
        
        # Evaluar vecinos adyacentes para determinar posibles fusiones
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < size and 0 <= nc < size and state.can_merge(next_number, grid[nr, nc]):
                impact_value += 20
        
        # Penalizar ubicaciones sin fusiones potenciales cercanas
        if impact_value == 0:
            impact_value -= 10
        
        # Evaluar proximidad a los bordes para números bajos
        if next_number in [1, 2] and (r in [0, size - 1] or c in [0, size - 1]):
            impact_value += 5
        
        return impact_value
    
    def evaluateEmptyCells(self, state):
        """
        Evalúa la cantidad de celdas vacías en el tablero.
        """
        empty_cells = np.sum(state.grid == 0)
        return empty_cells * 5  # Dar un peso mayor si hay más celdas vacías
    
    def evaluateLargeNumberDistribution(self, state):
        """
        Evalúa la distribución de números grandes en el tablero.
        """
        size = state.size
        grid = state.grid
        large_numbers = [(r, c) for r in range(size) for c in range(size) if grid[r, c] >= 48]
        distribution_value = 0
        
        for (r, c) in large_numbers:
            if r in [0, size - 1] or c in [0, size - 1]:
                distribution_value += 10  # Incentivar mantener números grandes en los bordes
            else:
                distribution_value -= 5  # Penalizar números grandes en el centro
        
        return distribution_value
