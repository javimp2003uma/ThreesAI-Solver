import numpy as np
import random as rnd

class State:
    def __init__(self, seed, size=4):
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
        allZeros = False
        for r in range(self.size):
            for c in range(self.size):
                if self.grid[r][c] == 0:
                    allZeros = True
        if allZeros:
            for r in range(self.size):
                for c in range(self.size):
                    # complete the code
                    pass

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