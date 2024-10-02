import numpy as np
import random as rnd
import math

class State:
    def __init__(self, seed, size=4):
        self.seed = seed
        rnd.seed(seed)

        self.size = size

        posx1 = rnd.randint(0, size-1)
        posy1 = rnd.randint(0, size-1)
        posx2 = rnd.randint(0, size-1)
        posy2 = rnd.randint(0, size-1)

        while posx2 == posy2 and posy2 == posy1:
            posy2 = rnd.randint(0, size-1)
            posx2 = rnd.randint(0, size-1)

        # Cuadrícula inicial (NumPy array)
        grid_array = np.zeros((size, size), dtype=int)
        grid_array[posx1][posy1] = 1
        grid_array[posx2][posy2] = 2

        self.grid = np.array(grid_array)
        self.has_merged = np.zeros_like(self.grid)
    
    def __eq__(self, other):
        if not isinstance(other, State):
            return False
        return self.grid == other.grid  # Compara los valores que determinan la equivalencia

    def __hash__(self):
        return hash(self.grid)  # Devuelve el hash del valor

    def clone_state(self):
        state = State(self.seed, self.size)
        state.grid = np.array(self.grid)
        state.has_merged = self.has_merged
        return state

    # Función para mover la cuadrícula hacia la izquierda
    def move_left(self):
        self.has_merged.fill(0)
        for r in range(self.size):
            for c in range(1, self.size):  # Comenzar desde la segunda columna
                if self.grid[r][c] != 0:
                    self.shift_tile(r, c, 0, -1)  # Mover a la izquierda (-1 en la columna)
        self.add_random_tile()


    # Función para mover la cuadrícula hacia la derecha
    def move_right(self):
        self.has_merged.fill(0)
        for r in range(self.size):
            for c in range(self.size - 2, -1, -1):  # Comenzar desde la penúltima columna
                if self.grid[r][c] != 0:
                    self.shift_tile(r, c, 0, 1)  # Mover a la derecha (+1 en la columna)
        self.add_random_tile()


    # Función para mover la cuadrícula hacia arriba
    def move_up(self):
        self.has_merged.fill(0)
        for r in range(1, self.size):  # Comenzar desde la segunda fila
            for c in range(self.size):
                if self.grid[r][c] != 0:
                    self.shift_tile(r, c, -1, 0)  # Mover hacia arriba (-1 en la fila)
        self.add_random_tile()


    # Función para mover la cuadrícula hacia abajo
    def move_down(self):
        self.has_merged.fill(0)
        for r in range(self.size - 2, -1, -1):  # Comenzar desde la penúltima fila
            for c in range(self.size):
                if self.grid[r][c] != 0:
                    self.shift_tile(r, c, 1, 0)  # Mover hacia abajo (+1 en la fila)
        self.add_random_tile()


    # Función para mover una ficha en la dirección dada (delta_row, delta_col)
    def shift_tile(self, r, c, delta_row, delta_col):
        new_r, new_c = r + delta_row, c + delta_col
        if 0 <= new_r < self.size and 0 <= new_c < self.size:
            # Si la celda de destino está vacía, mueve la ficha
            if self.grid[new_r][new_c] == 0:
                self.grid[new_r][new_c] = self.grid[r][c]
                self.grid[r][c] = 0
            # Si la celda de destino tiene una ficha, intenta fusionar
            elif self.can_merge(self.grid[r][c], self.grid[new_r][new_c]) and not self.has_merged[new_r][new_c]:
                self.grid[new_r][new_c] = self.grid[r][c] + self.grid[new_r][new_c]
                self.grid[r][c] = 0
                self.has_merged[new_r][new_c] = 1  # Marcar como fusionado

    def completedState(self):
        # Check if there's any empty space
        for r in range(self.size):
            for c in range(self.size):
                if self.grid[r][c] == 0:
                    return False  # There's an empty cell, so the game is not over

        # Check if there's any possible merge
        for r in range(self.size):
            for c in range(self.size):
                # Check right and down only to avoid redundant checks
                if c + 1 < self.size and self.can_merge(self.grid[r][c], self.grid[r][c + 1]):
                    return False  # A merge is possible to the right
                if r + 1 < self.size and self.can_merge(self.grid[r][c], self.grid[r + 1][c]):
                    return False  # A merge is possible downward

        # No empty spaces and no possible merges
        return True

    # Reglas de fusión (1 + 2, 2 + 1, o n + n si n >= 3)
    def can_merge(self, a, b):
        if (a == 1 and b == 2) or (a == 2 and b == 1):
            return True
        if a >= 3 and a == b:
            return True
        return False
    
    # Agrega una ficha en cualquier celda vacía después de un movimiento válido
    def add_random_tile(self):
        empty_cells = [(r, c) for r in range(self.size) for c in range(self.size) if self.grid[r][c] == 0]
        if empty_cells:
            row, col = rnd.choice(empty_cells)
            self.grid[row][col] = rnd.choice([1, 2, 3])  # Insertar ficha aleatoria
        
    def contarPuntosTotales(self):
        total = 0
        for r in range(self.size):
            for c in range(self.size):
                total += 3 ** (1 + math.log2(self.grid[r][c] / 3))
        return total