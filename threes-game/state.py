import numpy as np
import random as rnd
import math

class State:
    """
    State class represents the state of the Threes game.
    Attributes:
        seed (int): The seed for the random number generator.
        rnd (Random): Random number generator instance.
        size (int): Size of the game grid.
        grid (ndarray): The game grid.
        has_merged (ndarray): Array to track merged tiles.
        next_number (int): The next number to be added to the grid.
    Methods:
        __init__(seed, size=4):
            Initializes the State with a given seed and grid size.
        __eq__(other):
            Checks equality between two State instances.
        __hash__():
            Returns the hash of the State instance.
        gen_next_number():
            Generates the next number to be added to the grid.
        populate_initial_tiles(num_tiles=8):
            Populates the initial tiles on the grid.
        clone_state():
            Clones the current state.
        move(direction):
            Moves the tiles in the specified direction.
        move_left():
            Moves the tiles to the left.
        move_right():
            Moves the tiles to the right.
        move_up():
            Moves the tiles up.
        move_down():
            Moves the tiles down.
        shift_tile(r, c, delta_row, delta_col):
            Shifts a tile in the specified direction.
        add_random_tile(delta_row, delta_col):
            Adds a random tile to the grid after a move.
        can_merge(a, b):
            Checks if two tiles can be merged.
        completed_state():
            Checks if the game is in a completed state.
        edge_cost(e2):
            Calculates the edge cost between two states.
        total_points():
            Calculates the total points of the current state.
    """
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
        """
        Generates the next number to be placed on the grid based on the current state of the game.
        The method calculates the maximum value present on the grid and determines the valid numbers
        that can be generated (1, 2, or 3). It then calculates the probabilities for each of these
        numbers and uses a random value to select the next number to be placed on the grid.
        The probabilities are normalized so that their sum equals 1, and cumulative probabilities are
        calculated to facilitate the random selection process.
        Attributes:
            self.grid (np.ndarray): The current state of the game grid.
            self.rnd (np.random.RandomState): Random state for generating random values.
            self.next_number (int): The next number to be placed on the grid.
        Returns:
            None
        """
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
        """
        Populates the initial tiles on the game grid.
        This method initializes a grid of zeros with the specified size and randomly
        places a given number of tiles (num_tiles) on the grid. Each tile is assigned
        a random value between 1 and 3.
        Args:
            num_tiles (int): The number of tiles to place on the grid. Default is 8.
        Returns:
            np.ndarray: A 2D numpy array representing the game grid with the initial tiles.
        """
        grid_array = np.zeros((self.size, self.size), dtype=int)
        positions = self.rnd.sample(range(self.size * self.size), num_tiles)
        for pos in positions:
            row, col = divmod(pos, self.size)
            grid_array[row, col] = self.rnd.randint(1, 3)

        return grid_array

    def clone_state(self):
        """
        Creates a deep copy of the current state.

        Returns:
            State: A new instance of State with the same properties as the current state.
        """
        state = State(self.seed, self.size)
        state.rnd.setstate(self.rnd.getstate())
        state.grid = np.array(self.grid)
        state.has_merged = self.has_merged
        state.next_number = self.next_number
        return state

    def move(self, direction):
        """
        Moves the game state in the specified direction.

        Parameters:
        direction (str): The direction to move the game state. 
                         Must be one of 'LEFT', 'RIGHT', 'UP', or 'DOWN'.

        Raises:
        ValueError: If the direction is not one of 'LEFT', 'RIGHT', 'UP', or 'DOWN'.
        """
        directions = {
            'LEFT': (0, -1),
            'RIGHT': (0, 1),
            'UP': (-1, 0),
            'DOWN': (1, 0)
        }
        if direction in directions:
            delta_row, delta_col = directions[direction]
            self.move_in_direction(delta_row, delta_col)
            
        else:
            raise ValueError("Invalid direction. Use 'LEFT', 'RIGHT', 'UP', or 'DOWN'.")

    def move_in_direction(self, delta_row, delta_col):
        """
        Moves the tiles in the grid in the specified direction and merges them if possible.
        Parameters:
        delta_row (int): The change in row direction. Use 1 for down, -1 for up, and 0 for no vertical movement.
        delta_col (int): The change in column direction. Use 1 for right, -1 for left, and 0 for no horizontal movement.
        This method resets the merge state of the tiles, shifts the tiles in the specified direction,
        and merges them if they are the same and can be merged according to the game rules. After moving
        and merging, it adds a new random tile to the grid.
        """
        self.has_merged.fill(False)  # Resetear el estado de fusiones
        has_move = False
        if delta_col != 0:  # Movimiento horizontal
            if delta_col == 1:  # Movimiento a la derecha
                for r in range(self.size):
                    for c in range(self.size - 1, -1, -1):
                        if self.grid[r][c] != 0:
                           if self.shift_tile(r, c, 0, 1):  # Desplazar a la derecha
                                    has_move=True
            elif delta_col == -1:  # Movimiento a la izquierda
                for r in range(self.size):
                    for c in range(self.size):
                        if self.grid[r][c] != 0:
                           if self.shift_tile(r, c, 0, -1):  # Desplazar a la izquierda
                                 has_move=True

        elif delta_row != 0:  # Movimiento vertical
            if delta_row == 1:  # Movimiento hacia abajo
                for r in range(self.size - 1, -1, -1):
                    for c in range(self.size):
                        if self.grid[r][c] != 0:
                            if self.shift_tile(r, c, 1, 0):  # Desplazar hacia abajo
                                has_move=True
            elif delta_row == -1:  # Movimiento hacia arriba
                for r in range(self.size):
                    for c in range(self.size):
                        if self.grid[r][c] != 0:
                            if self.shift_tile(r, c, -1, 0):  # Desplazar hacia arriba
                                has_move=True
        if has_move:
            self.add_random_tile(delta_row, delta_col)


    def shift_tile(self, r, c, delta_row, delta_col):
        """
        Shifts a tile from position (r, c) to a new position determined by the delta_row and delta_col.
        
        If the new position is within the grid bounds and is empty, the tile is moved to the new position.
        If the new position contains a tile that can be merged with the current tile and has not been merged yet,
        the tiles are merged, and the current tile's position is set to empty.
        
        Args:
            r (int): The row index of the current tile.
            c (int): The column index of the current tile.
            delta_row (int): The row change to determine the new position.
            delta_col (int): The column change to determine the new position.
        
        Returns:
            bool: True if the tile was moved or merged, False otherwise.
        """
        new_r, new_c = r + delta_row, c + delta_col
        if (0 <= new_r < self.size and 0 <= new_c < self.size):
            if self.grid[new_r][new_c] == 0:
                self.grid[new_r][new_c] = self.grid[r][c]
                self.grid[r][c] = 0
                return True
            elif self.can_merge(self.grid[r][c], self.grid[new_r][new_c]) and not self.has_merged[new_r][new_c]:
                self.grid[new_r][new_c] += self.grid[r][c]
                self.grid[r][c] = 0
                self.has_merged[new_r][new_c] = 1
                return True
        return False

    def add_random_tile(self, delta_row, delta_col):
        """
        Adds a random tile to the grid based on the direction of movement.
        Parameters:
        delta_row (int): The change in the row index (vertical movement).
                         -1 for up, 1 for down, 0 for horizontal movement.
        delta_col (int): The change in the column index (horizontal movement).
                         -1 for left, 1 for right, 0 for vertical movement.
        The method places the next_number tile in an appropriate empty spot
        based on the direction of movement and then generates the next number.
        """
        if delta_row == 0:  # Horizontal movement
            if delta_col == -1:  # Left
                row = [(r) for r in range(self.size) if self.grid[r][self.size-1] == 0]
                if row:
                    self.grid[self.rnd.choice(row)][self.size-1] = self.next_number
                    self.gen_next_number()
            else:  # Right
                row = [(r) for r in range(self.size) if self.grid[r][0] == 0]
                if row:
                    self.grid[self.rnd.choice(row)][0] = self.next_number
                    self.gen_next_number()
        else:  # Vertical movement
            if delta_row == -1:  # Up
                col = [(c) for c in range(self.size) if self.grid[self.size-1][c] == 0]
                if col:
                    self.grid[self.size-1][self.rnd.choice(col)] = self.next_number
                    self.gen_next_number()

            else:  # Down
                col = [(c) for c in range(self.size) if self.grid[0][c] == 0]
                if col:
                    self.grid[0][self.rnd.choice(col)] = self.next_number
                    self.gen_next_number()

    def can_merge(self, a, b):
        """
        Determines if two tiles can be merged in the game.

        Args:
            a (int): The value of the first tile.
            b (int): The value of the second tile.

        Returns:
            bool: True if the tiles can be merged, False otherwise.

        The tiles can be merged if:
        - One tile is 1 and the other is 2.
        - Both tiles have the same value and are greater than or equal to 3.
        """
        return (a == 1 and b == 2) or (a == 2 and b == 1) or (a >= 3 and a == b)

    def completed_state(self):
        """
        Check if the current state of the game is completed.

        A state is considered completed if there are no empty cells (cells with value 0)
        and no adjacent cells can be merged. The function checks for possible merges
        both horizontally and vertically.

        Returns:
            bool: True if the state is completed, False otherwise.
        """
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

    def edge_cost(self, e2):
        """
        Calculate the cost of transitioning from the current state to another state.

        Args:
            e2 (State): The state to which the transition is being evaluated.

        Returns:
            float: The cost based on the number of cells that have changed between
                the current state and the new state.
        """
        celdas_movidas = sum(
            self.grid[i, j] != e2.grid[i, j]
            for i in range(self.grid.shape[0])
            for j in range(self.grid.shape[1])
        )
        return 1 / celdas_movidas if celdas_movidas > 0 else 0


    def total_points(self):
        """
        Calculate the total points of the current game state.

        The points are calculated based on the values in the grid. Each value
        greater than or equal to 3 contributes to the total points. The formula
        used for each value is 3 raised to the power of (1 + log2(value / 3)).

        Returns:
            int: The total points of the current game state.
        """
        return sum(3 ** (1 + math.log2(val / 3)) for val in self.grid.flatten() if val >= 3)
    
    def max_points(self):
        """
        Calculate the maximum possible points that can be achieved in the game.
        This assumes that all cells in the grid have the value 768.
        
        Args:
            size (int): The size of the grid (e.g., 4 for a 4x4 grid).
        
        Returns:
            int: The maximum possible points that can be achieved in the grid.
        """
        max_tile_value = 768
        points_per_tile = 3 ** (1 + math.log2(max_tile_value / 3))  # Points for a single 768 tile
        total_points = points_per_tile * (self.size ** 2)  # Multiply by total number of tiles
        return total_points
