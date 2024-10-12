import numpy as np
import random as rnd
import math

class State:
    def __init__(self, seed, size=4):
        self.seed = seed
        self.rnd = rnd.Random(seed)

        self.size = size

        self.grid = self.populate_initial_tiles((size * size) // 2)     
        self.has_merged = np.zeros_like(self.grid)
    
        self.gen_next_number()

    def __eq__(self, other):
        return isinstance(other, State) and np.array_equal(self.grid, other.grid)

    def __hash__(self):
        return hash(self.grid.tobytes())
    
    def gen_next_number(self):
        max_value = np.max(self.grid)

        valid_numbers = [1, 2, 3]
        current_value = 3
        while current_value <= max_value // 2:
            current_value *= 2

        probabilities = [val for val in valid_numbers]#if val < 3 else 1 / (3 ** (1 + math.log2(val / 3))) for val in valid_numbers]
        total_probability = sum(probabilities)
        probabilities = [p / total_probability for p in probabilities]

        cumulative_probabilities = np.cumsum(probabilities)
        random_value = self.rnd.random()

        for i, cumulative_probability in enumerate(cumulative_probabilities):
            if random_value < cumulative_probability:
                self.next_number = valid_numbers[i]
                return

    def populate_initial_tiles(self, num_tiles=8):
        grid_array = np.zeros((self.size, self.size), dtype=int)
        positions = self.rnd.sample(range(self.size * self.size), num_tiles)
        for pos in positions:
            row, col = divmod(pos, self.size)
            grid_array[row, col] = self.rnd.randint(1, 3)

        return grid_array

    def clone_state(self):
        state = State(self.seed, self.size)
        state.rnd.setstate(self.rnd.getstate())
        state.grid = np.array(self.grid)
        state.has_merged = self.has_merged
        state.next_number = self.next_number
        return state

    def move(self, direction):   
        if direction == 'LEFT':
            self.move_left()
        elif direction == 'RIGHT':
            self.move_right()
        elif direction == 'UP':
            self.move_up()
        elif direction == 'DOWN':
            self.move_down()
        self.gen_next_number()

    def move_left(self):
        self.has_merged = [[0] * self.size for _ in range(self.size)]
        for r in range(self.size):
            for c in range(1, self.size):
                if self.grid[r][c] != 0:
                    self.shift_tile(r, c, 0, -1)  # Desplazarse solo 1 posición
        self.add_random_tile(0, -1)  # Generar nueva ficha en el lado contrario

    def move_right(self):
        self.has_merged = [[0] * self.size for _ in range(self.size)]
        for r in range(self.size):
            for c in range(self.size - 2, -1, -1):
                if self.grid[r][c] != 0:
                    self.shift_tile(r, c, 0, 1)  # Desplazarse solo 1 posición
        self.add_random_tile(0, 1)  # Generar nueva ficha en el lado contrario

    def move_up(self):
        self.has_merged = [[0] * self.size for _ in range(self.size)]
        for r in range(1, self.size):
            for c in range(self.size):
                if self.grid[r][c] != 0:
                    self.shift_tile(r, c, -1, 0)  # Desplazarse solo 1 posición
        self.add_random_tile(-1, 0)  # Generar nueva ficha en el lado contrario

    def move_down(self):
        self.has_merged = [[0] * self.size for _ in range(self.size)]
        for r in range(self.size - 2, -1, -1):
            for c in range(self.size):
                if self.grid[r][c] != 0:
                    self.shift_tile(r, c, 1, 0)  # Desplazarse solo 1 posición
        self.add_random_tile(1, 0)  # Generar nueva ficha en el lado contrario

    def shift_tile(self, r, c, delta_row, delta_col):
        new_r, new_c = r + delta_row, c + delta_col
        if (0 <= new_r < self.size and 0 <= new_c < self.size):
            # Mover la ficha solo si la posición está vacía
            if self.grid[new_r][new_c] == 0:
                self.grid[new_r][new_c] = self.grid[r][c]
                self.grid[r][c] = 0
            elif self.can_merge(self.grid[r][c], self.grid[new_r][new_c]) and not self.has_merged[new_r][new_c]:
                self.grid[new_r][new_c] += self.grid[r][c]
                self.grid[r][c] = 0
                self.has_merged[new_r][new_c] = 1

    def add_random_tile(self, delta_row, delta_col):
        # Encuentra el lado opuesto del movimiento
        if delta_row == 0:  # Movimiento horizontal
            if delta_col == -1:  # Izquierda
                # Aparecer en la columna derecha
                row = [(r) for r in range(self.size) if self.grid[r][self.size-1] == 0]
                if row:
                    self.grid[self.rnd.choice(row)][self.size-1] = self.next_number
                    self.gen_next_number()
            else:  # Derecha
                # Aparecer en la columna izquierda
                row = [(r) for r in range(self.size) if self.grid[r][0] == 0]
                if row:
                    self.grid[self.rnd.choice(row)][0] = self.next_number
                    self.gen_next_number()
        else:  # Movimiento vertical
            if delta_row == -1:  # Arriba
                # Aparecer en la fila de abajo
                col = [(c) for c in range(self.size) if self.grid[self.size-1][c] == 0]
                if col:
                    self.grid[self.size-1][self.rnd.choice(col)] = self.next_number
                    self.gen_next_number()
                    
            else:  # Abajo
                # Aparecer en la fila de arriba
                col = [(c) for c in range(self.size) if self.grid[0][c] == 0]
                if col:
                    self.grid[0][self.rnd.choice(col)] = self.next_number
                    self.gen_next_number()
            
    def can_merge(self, a, b):
        return (a == 1 and b == 2) or (a == 2 and b == 1) or (a >= 3 and a == b)

    def completed_state(self):
        if np.any(self.grid == 0):
            return False
        for r in range(self.size):
            for c in range(self.size - 1):
                if self.can_merge(self.grid[r, c], self.grid[r, c + 1]):
                    return False
        for c in range(self.size):
            for r in range(self.size - 1):
                if self.can_merge(self.grid[r, c], self.grid[r + 1, c]):
                    return False
        return True

    def total_points(self):
        return sum(3 ** (1 + math.log2(val / 3)) for val in self.grid.flatten() if val >= 3)