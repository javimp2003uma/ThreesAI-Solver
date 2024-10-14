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
        
        # Ajustar la heurística usando el puntaje actual y el impacto de la próxima colocación
        heuristicValue = currentScore + (totalMaxScore - currentScore) * 0.5 + positionFactor
        
        return heuristicValue
    
    def calculateProbablePosition(self, state):
        """
        Calcula la posición probable donde el próximo número aparecerá basado en el
        movimiento reciente y el estado actual del tablero.
        
        Args:
            state (State): El estado actual del juego.
            
        Returns:
            tuple: La fila y columna donde es más probable que aparezca el próximo número.
        """
        size = state.size
        next_number = state.next_number
        grid = state.grid
        
        # Obtener todas las celdas vacías
        empty_cells = [(r, c) for r in range(size) for c in range(size) if grid[r, c] == 0]
        
        # Si no hay celdas vacías (caso extremo), no hay lugar para colocar
        if not empty_cells:
            return None
        
        # Evaluar celdas vacías y priorizar las que tienen adyacentes fusionables
        probable_positions = []
        for (r, c) in empty_cells:
            # Evaluar si tiene vecinos que puedan fusionarse con el próximo número
            if (r > 0 and state.can_merge(next_number, grid[r - 1, c])) or \
               (r < size - 1 and state.can_merge(next_number, grid[r + 1, c])) or \
               (c > 0 and state.can_merge(next_number, grid[r, c - 1])) or \
               (c < size - 1 and state.can_merge(next_number, grid[r, c + 1])):
                probable_positions.append((r, c))
        
        # Si hay posiciones adecuadas para fusionar, elegir una al azar
        if probable_positions:
            return state.rnd.choice(probable_positions)
        
        # Si no se encontraron posiciones adecuadas, elegir una vacía al azar
        return state.rnd.choice(empty_cells)
    
    def evaluatePositionImpact(self, state, next_number, probable_position):
        """
        Evalúa el impacto de colocar el próximo número en la posición probable.
        
        Args:
            state (State): El estado actual del juego.
            next_number (int): El próximo número que se colocará en el tablero.
            probable_position (tuple): La posición donde se colocará el número.
            
        Returns:
            float: Un valor que representa el impacto de esta colocación en la heurística.
        """
        if probable_position is None:
            return 0
        
        r, c = probable_position
        size = state.size
        grid = state.grid
        impact_value = 0
        
        # Evaluar vecinos adyacentes para determinar posibles fusiones
        if r > 0 and state.can_merge(next_number, grid[r - 1, c]):
            impact_value += 10  # Fusiones verticales arriba
        if r < size - 1 and state.can_merge(next_number, grid[r + 1, c]):
            impact_value += 10  # Fusiones verticales abajo
        if c > 0 and state.can_merge(next_number, grid[r, c - 1]):
            impact_value += 10  # Fusiones horizontales a la izquierda
        if c < size - 1 and state.can_merge(next_number, grid[r, c + 1]):
            impact_value += 10  # Fusiones horizontales a la derecha
        
        # Penalizar ubicaciones que no tienen vecinos fusionables
        if impact_value == 0:
            impact_value -= 5
        
        # Evaluar la cercanía al borde para valores pequeños
        if next_number in [1, 2] and (r in [0, size - 1] or c in [0, size - 1]):
            impact_value += 5  # Incentivar colocar números bajos en los bordes
        
        return impact_value
