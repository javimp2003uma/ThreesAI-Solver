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
        Executes a move in the specified direction and generates the next number.
        Parameters:
        direction (str): The direction to move the tiles. 
                         Must be one of 'LEFT', 'RIGHT', 'UP', or 'DOWN'.
        Raises:
        ValueError: If the direction is not one of 'LEFT', 'RIGHT', 'UP', or 'DOWN'.
        """
        if direction == 'LEFT':
            self.move_left()
        elif direction == 'RIGHT':
            self.move_right()
        elif direction == 'UP':
            self.move_up()
        elif direction == 'DOWN':
            self.move_down()
        else:
            raise ValueError("Invalid direction. Use 'LEFT', 'RIGHT', 'UP', or 'DOWN'.")

        self.gen_next_number()

    def move_left(self):
        """
        Moves all tiles in the grid to the left. This method updates the grid by shifting
        tiles to the left, merging tiles when possible, and then adding a new random tile
        to the grid.

        The method performs the following steps:
        1. Resets the `has_merged` matrix to track which tiles have merged during this move.
        2. Iterates through each row and shifts non-zero tiles to the left.
        3. Calls `shift_tile` to handle the actual shifting and merging of tiles.
        4. Adds a new random tile to the grid after all possible shifts and merges.

        Note:
            - The `shift_tile` method is responsible for the logic of shifting and merging tiles.
            - The `add_random_tile` method is responsible for adding a new tile to the grid.

        """
        self.has_merged = [[0] * self.size for _ in range(self.size)]
        for r in range(self.size):
            for c in range(1, self.size):
                if self.grid[r][c] != 0:
                    self.shift_tile(r, c, 0, -1)  
        self.add_random_tile(0, -1)  

    def move_right(self):
        """
        Moves all tiles in the grid to the right. This method updates the grid by shifting
        tiles to the right and merging them according to the game rules. After shifting and 
        merging, a new random tile is added to the grid.

        The method performs the following steps:
        1. Resets the `has_merged` matrix to track which tiles have merged during this move.
        2. Iterates through each row and shifts tiles to the right.
        3. Calls `shift_tile` to handle the movement and merging of tiles.
        4. Adds a new random tile to the grid in a position affected by the move.

        Note:
        - The `shift_tile` method is responsible for the actual shifting and merging logic.
        - The `add_random_tile` method adds a new tile to the grid after the move.

        Returns:
            None
        """
        self.has_merged = [[0] * self.size for _ in range(self.size)]
        for r in range(self.size):
            for c in range(self.size - 2, -1, -1):
                if self.grid[r][c] != 0:
                    self.shift_tile(r, c, 0, 1)  
        self.add_random_tile(0, 1) 

    def move_up(self):
        """
        Executes a move up action in the game. This involves shifting all tiles
        upwards, merging tiles if possible, and then adding a new random tile
        to the grid.

        The method performs the following steps:
        1. Resets the has_merged matrix to track which tiles have merged during this move.
        2. Iterates through each column, starting from the second row, and shifts tiles upwards.
        3. Calls the shift_tile method to handle the actual shifting and merging of tiles.
        4. Adds a new random tile to the grid after all possible shifts and merges are done.

        Note:
        - The grid is assumed to be a square matrix.
        - The shift_tile method is expected to handle the logic for shifting and merging tiles.
        - The add_random_tile method is expected to handle the logic for adding a new tile to the grid.

        Returns:
        None
        """
        self.has_merged = [[0] * self.size for _ in range(self.size)]
        for r in range(1, self.size):
            for c in range(self.size):
                if self.grid[r][c] != 0:
                    self.shift_tile(r, c, -1, 0)  
        self.add_random_tile(-1, 0) 

    def move_down(self):
        """
        Moves all tiles in the grid downwards. This method updates the grid by shifting
        tiles down, merging them if possible, and then adding a new random tile at the top.

        The method performs the following steps:
        1. Resets the `has_merged` matrix to track which tiles have merged during this move.
        2. Iterates over the grid from the second-to-last row to the first row.
        3. For each tile that is not empty, attempts to shift it downwards.
        4. After all possible shifts and merges, adds a new random tile at the top.

        Note:
        - The `shift_tile` method is used to handle the actual shifting and merging of tiles.
        - The `add_random_tile` method is used to add a new tile after the move.

        Returns:
        None
        """
        self.has_merged = [[0] * self.size for _ in range(self.size)]
        for r in range(self.size - 2, -1, -1):
            for c in range(self.size):
                if self.grid[r][c] != 0:
                    self.shift_tile(r, c, 1, 0)  
        self.add_random_tile(1, 0)  

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
            None
        """
        new_r, new_c = r + delta_row, c + delta_col
        if (0 <= new_r < self.size and 0 <= new_c < self.size):
            if self.grid[new_r][new_c] == 0:
                self.grid[new_r][new_c] = self.grid[r][c]
                self.grid[r][c] = 0
            elif self.can_merge(self.grid[r][c], self.grid[new_r][new_c]) and not self.has_merged[new_r][new_c]:
                self.grid[new_r][new_c] += self.grid[r][c]
                self.grid[r][c] = 0
                self.has_merged[new_r][new_c] = 1

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
            int: The difference in total points between the given state (e2) and the current state.
        """
        return e2.total_points() - self.total_points()

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
