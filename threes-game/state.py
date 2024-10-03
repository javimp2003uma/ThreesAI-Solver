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
        return np.array_equal(self.grid, other.grid)  # Compara los valores que determinan la equivalencia

    def __hash__(self):
        return hash(self.grid.tobytes())  # Devuelve el hash del valor

    def clone_state(self):
        state = State(self.seed, self.size)
        state.grid = np.array(self.grid)
        state.has_merged = self.has_merged
        return state

    def move_left(self):
            self.has_merged = [[0] * self.size for _ in range(self.size)]
            for r in range(self.size):
                for c in range(1, self.size):
                    if self.grid[r][c] != 0:
                        self.shift_tile(r, c, 0, -1)
            self.add_random_tile()

    def move_right(self):
        self.has_merged = [[0] * self.size for _ in range(self.size)]
        for r in range(self.size):
            for c in range(self.size - 2, -1, -1):
                if self.grid[r][c] != 0:
                    self.shift_tile(r, c, 0, 1)
        self.add_random_tile()

    def move_up(self):
        self.has_merged = [[0] * self.size for _ in range(self.size)]
        for r in range(1, self.size):
            for c in range(self.size):
                if self.grid[r][c] != 0:
                    self.shift_tile(r, c, -1, 0)
        self.add_random_tile()

    def move_down(self):
        self.has_merged = [[0] * self.size for _ in range(self.size)]
        for r in range(self.size - 2, -1, -1):
            for c in range(self.size):
                if self.grid[r][c] != 0:
                    self.shift_tile(r, c, 1, 0)
        self.add_random_tile()

    def shift_tile(self, r, c, delta_row, delta_col):
        current_r, current_c = r, c
        while True:
            new_r, new_c = current_r + delta_row, current_c + delta_col
            if not (0 <= new_r < self.size and 0 <= new_c < self.size):
                break
            if self.grid[new_r][new_c] == 0:
                self.grid[new_r][new_c] = self.grid[current_r][current_c]
                self.grid[current_r][current_c] = 0
                current_r, current_c = new_r, new_c
            elif self.can_merge(self.grid[current_r][current_c], self.grid[new_r][new_c]) and not self.has_merged[new_r][new_c]:
                self.grid[new_r][new_c] += self.grid[current_r][current_c]
                self.grid[current_r][current_c] = 0
                self.has_merged[new_r][new_c] = 1
                break
            else:
                break

    def can_merge(self, a, b):
        if (a == 1 and b == 2) or (a == 2 and b == 1):
            return True
        if a >= 3 and a == b:
            return True
        return False

    def add_random_tile(self):
        empty_cells = [(r, c) for r in range(self.size) for c in range(self.size) if self.grid[r][c] == 0]
        if empty_cells:
            row, col = rnd.choice(empty_cells)
            self.grid[row][col] = rnd.randint(1, self.size-1)

    def completed_state(self):
        for r in range(self.size):
            for c in range(self.size):
                if self.grid[r][c] == 0:
                    return False

        for r in range(self.size):
            for c in range(self.size):
                if c + 1 < self.size and self.can_merge(self.grid[r][c], self.grid[r][c + 1]):
                    return False
                if r + 1 < self.size and self.can_merge(self.grid[r][c], self.grid[r + 1][c]):
                    return False

        return True

    def total_points(self):
        total = 0
        for r in range(self.size):
            for c in range(self.size):
                if self.grid[r][c] >= 3:
                    total += 3 ** (1 + math.log2(self.grid[r][c] / 3))
        return total