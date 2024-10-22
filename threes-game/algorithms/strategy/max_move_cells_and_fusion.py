from algorithms.strategy.heuristic import Heuristic


class MaxMoveCellsAndFusion(Heuristic):

    def evaluate(self, state):
        fusiones_posibles = 0
        movimientos_necesarios = 0
        
        # Recorremos el grid de state para evaluar fusiones y estimar movimientos necesarios
        for i in range(state.grid.shape[0]):
            for j in range(state.grid.shape[1]):
                valor_actual = state.grid[i, j]
                
                if valor_actual != 0:
                    # Verificar si puede fusionarse con una celda adyacente
                    for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:  # Arriba, abajo, izquierda, derecha
                        ni, nj = i + di, j + dj
                        if 0 <= ni < state.grid.shape[0] and 0 <= nj < state.grid.shape[1]:
                            if state.grid[ni, nj] == valor_actual:  # Fusión posible
                                fusiones_posibles += 1
                            elif state.grid[ni, nj] == 0:  # Celda vacía cerca
                                movimientos_necesarios += 1
        
        # Cuanto más fusiones, menor el coste heurístico
        # Cuantos más movimientos necesarios, mayor el coste, pero compensado por fusiones posibles
        return movimientos_necesarios - fusiones_posibles